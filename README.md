# 自动化GUI工具开发框架 - Relax

[TOC]

## 使用方法

* 创建自动化流程JSON文件，示例：

```json
{
  "flow_name": "替换镜像",
  "phases": {
    "获取镜像包": {
      "handler": "get_images.ImagesAcquirer",
      "progress": 30
    },
    "上传镜像包": {
      "handler": "upload_images.ImagesUploader",
      "progress": 50
    },
    "导出配置": {
      "handler": "export_config.ConfigExporter",
      "progress": 60
    },
    "替换镜像": {
      "handler": "update_images.ImagesUpdater",
      "progress": 75
    },
    "恢复配置": {
      "handler": "recover_config.ConfigRecovery",
      "progress": 100
    }
  }
}
```

* 编写流程JSON文件中写的python模块和类，需要继承Phase抽象类，实现run和clean方法，示例：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from relax.flow.phase import Phase
import time


class ImagesUpdater(Phase):
    def run(self):
        self.log.info("ImagesUpdater start")
        time.sleep(1)
        self.log.info("ImagesUpdater end")

        return 0

    def clean(self):
        return 0
```

* 编写main.py，通常不需要改动：

```python
#!/usr/bin/env python
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
```

* 运行main.py，会显示GUI界面，点击流程按钮启动自动化流程。
* 示例程序在代码根目录的example目录中。
