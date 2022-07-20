#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : json_to_module.py
@Author: Scott
@Date  : 2022/2/4 12:42
@Desc  : 根据JSON流程文件生成python模块和类
"""
import json
import sys
import os

MAIN_PY = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from relax.app import Relax

# 获取脚本或exe文件的执行路径
if getattr(sys, 'frozen', False):
    ROOT_PATH = os.path.dirname(sys.executable)
else:
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    r = Relax(ROOT_PATH)
    # 框架初始化，启动GUI
    r.init()
'''

MODULE_FILE_HEAD = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
from relax.flow.phase import Phase

'''

PHASE_CLASS = '''
class %s(Phase):
    def __init__(self, phase_name, progress):
        super().__init__(phase_name, progress)

    def run(self):
        return 0

    def clean(self):
        return 0
'''

RELAX_INI = '''
[CONF]
server.ip = 127.0.0.1
server.port = 8200
gui.mode = tkinter
log.level = INFO
'''


def print_usage():
    print("wrong parameters!")
    print("Usage:")
    print("    python json_to_module.py JSON流程文件所在目录")


def parse_handler(json_file):
    handlers = []
    with open(json_file, 'r', encoding='utf-8') as f:
        flow_json = json.load(f)
        for phase in flow_json["phases"]:
            handler = phase["handler"].split(".")
            if len(handler) != 2:
                raise Exception("handler format %s is not right" % phase["handler"])
            file_name = "%s.py" % handler[0]
            class_name = handler[1]
            handlers.append((file_name, class_name))

    return handlers


def get_handlers(json_dir):
    handlers = []
    # 遍历指定目录下的所有JSON流程文件
    for root, dirs, files in os.walk(json_dir):
        json_files = [file for file in files if file.endswith(".json")]
        for json_file in json_files:
            handlers += parse_handler(os.path.join(root, json_file))

    return handlers


def create_class(handlers):
    for file_name, class_name in handlers:
        file_path = os.path.join(root_path, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(MODULE_FILE_HEAD)
                f.write(PHASE_CLASS % class_name)
            continue

        # 如果已存在python文件，查询是否已定义该类，如果未定义该类，创建该类
        with open(file_path, 'r', encoding='utf-8') as f:
            if f.read().find("class %s(" % class_name) != -1:
                continue

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(PHASE_CLASS % class_name)


def _generate_file(file_path, file_content):
    if os.path.isfile(file_path):
        return

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)


def generate_main_py():
    _generate_file(os.path.join(root_path, "main.py"), MAIN_PY)


def generate_relax_ini():
    _generate_file(os.path.join(root_path, "relax.ini"), RELAX_INI)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    root_path = sys.argv[1]
    try:
        flow_handlers = get_handlers(root_path)
    except Exception as e:
        print("parse json_flow failed:", str(e))
        sys.exit(1)

    try:
        create_class(flow_handlers)
    except Exception as e:
        print("create Phase class failed:", str(e))
        sys.exit(1)

    try:
        generate_main_py()
    except Exception as e:
        print("generate main.py failed:", str(e))
        sys.exit(1)

    try:
        generate_relax_ini()
    except Exception as e:
        print("generate relax.ini failed:", str(e))
        sys.exit(1)

    print("flow json to module success")

    sys.exit(0)
