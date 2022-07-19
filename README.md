# 自动化GUI工具开发框架 - Relax

[TOC]

## 开发流程

### 安装relax框架

```powershell
> pip install relax-x.x.x.tar.gz
```

### JSON流程文件编写

* 创建自动化流程JSON文件，可以是多个，放在同一目录下，自动化流程JSON文件中的`flow_name`和其他JSON文件不能重复。
* 在自动化流程JSON文件中按顺序在`phases`数组中添加阶段，各阶段名称`phase_name`不能重复。
* 每个阶段中的`handler`的格式为"去掉后缀的python文件名.python文件中的类名"，名称自定义。
* 每个阶段中的`progress`表示该阶段完成后的整体进度。

```json
{
  "flow_name": "替换镜像",
  "phases": [
    {
      "phase_name": "获取镜像包",
      "handler": "get_images.ImagesAcquirer",
      "progress": 30
    },
    {
      "phase_name": "上传镜像包",
      "handler": "upload_images.ImagesUploader",
      "progress": 50
    },
    {
      "phase_name": "导出配置",
      "handler": "export_config.ConfigExporter",
      "progress": 60
    },
    {
      "phase_name": "替换镜像",
      "handler": "update_images.ImagesUpdater",
      "progress": 75
    },
    {
      "phase_name": "恢复配置",
      "handler": "recover_config.ConfigRecovery",
      "progress": 100
    }
  ]
}
```

### 生成并完成各阶段的处理类

* 执行代码生成工具，会根据JSON流程文件自动生成代码，当前已存在文件不会覆盖：
  
```powershell
> python json_to_module.py JSON流程文件所在目录
```

* 用户只需要完善继承自Phase抽象类的具体类的run和clean方法，run方法是该阶段具体执行的内容，clean方法是无论成功还是失败都要执行的方法，用于清理临时文件，示例：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from relax.flow.phase import Phase
from relax.log_manager.log import Log
import time


class ImagesUpdater(Phase):
    def run(self):
        Log().info("ImagesUpdater start")
        time.sleep(1)
        Log().info("ImagesUpdater end")

        return 0

    def clean(self):
        Log().info("ImagesUpdater clean")
        return 0
```

* main.py也是自动生成的，通常不需要改动：

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

## 打包方法

* 执行以下命令在dist目录下生成relax-x.x.x.tar.gz，x.x.x为setup.py中写的version：

```powershell
> python setup.py sdist
```

* 生成的压缩包可以通过以下命令安装：

```powershell
> pip install relax-x.x.x.tar.gz
```
