# 测试能力重建计划

车载方向 Python 与测试工程复训项目。目标不是"学完 Python"，而是把车载测试里最常遇到的三类活儿做成能跑的工具：**日志解析、用例管理、自动化执行**。

当前进度：第 1 周（2026.11.24 起）。

## 第一周成果

`tools/log_cli.py` —— 一个能解析域控制器运行日志的命令行工具。

```
2026-11-24 08:06:40 ERROR [perception] lane detection timeout
2026-11-24 08:05:30 WARN  [can] cycle time 12ms exceeds 10ms
```

给它一个日志文件，它按行解析成结构化记录，统计各级别条数、时间跨度，并列出"哪个模块说了什么"。

### 用法

```bash
python tools/log_cli.py tools\sample.log
python tools/log_cli.py tools\sample.log --top 3
python tools/log_cli.py tools\sample.log --level ERROR
python tools/log_cli.py --help
```

### 实际输出

```
总行数: 26, 有效: 25, 脏行: 1
时间跨度: 2026-11-24 08:00:01 ~ 2026-11-24 08:20:05
级别统计: INFO=15 WARN=4 ERROR=4 DEBUG=2
模块消息（前 10 条）:
  system | boot sequence started
  system | config loaded from default.json
  camera | front camera stream opened
  perception | model version v2.3 loaded
  perception | image brightness below threshold
  ...
```

```
$ python tools/log_cli.py --help
usage: log_cli.py [-h] [--top TOP] [--level {INFO,WARN,ERROR,DEBUG}] path

车载日志解析工具

positional arguments:
  path                  日志文件路径

options:
  -h, --help            show this help message and exit
  --top TOP             显示前 N 条，默认 10
  --level {INFO,WARN,ERROR,DEBUG}
                        只统计某个级别
```

### 实现要点

- **正则命名分组**解析日志行，用 `groupdict()` 直接得到字段字典，加字段不用改取值代码
- **三种异常分开处理**：文件不存在（`FileNotFoundError`，打开时抛）、编码不对（`UnicodeDecodeError`，读取时抛，自动回退 GBK）、格式不符的脏行（不是异常，`search` 返回 `None`，跳过并计数）
- **两种统计实现**：`Counter` 与手写字典各写一遍，用于对比标准库封装与底层原理
- **argparse** 提供位置参数与两个选项，`--help` 文档自动生成

`tools/log_parse.py` 是纯逻辑层（5 个函数 + 断言自测），`tools/log_cli.py` 是命令行层。分开是为了下一周接入 pytest。

## 目录结构

```
learn/    每天的语法练习脚本（day01_basics.py 10 题、day02_wordcount.py 5 题）
tools/    日志分析工具，第一周成果
tests/    pytest 用例（第二周开始）
docs/     学习笔记（w1d1.md / w1d2.md / w1d3.md）
reports/  测试报告输出
```

## 进度

| 日期 | 主题 | 产出 |
|---|---|---|
| 11.24 Day1 | 语法热身 10 题 | `learn/day01_basics.py`（10/10 通过） |
| 11.25 Day2 | 容器与统计（set / dict / Counter） | `learn/day02_wordcount.py`（5/5 通过）+ `docs/w1d2.md` |
| 11.27 Day3 | 文件与日志解析、正则命名分组 | `tools/log_parse.py`（5/5 通过，并通过"换日志不改代码"验收） |
| 11.28 Day4 | 命令行工具 argparse | `tools/log_cli.py`（4/4 通过） |

（11.26 家中事务，已顺延）

## 下一步

第二周：pytest 用例化 + GitHub Actions 持续集成，把 `tools/` 里的函数变成有断言、有报告、有 CI 绿灯的工程项目。

## 环境

Python 3.11.9 / Git 2.56.1 / VS Code 1.147.0（Windows 11）
