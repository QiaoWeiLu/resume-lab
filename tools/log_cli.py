"""Day4：把日志解析器变成命令行工具（argparse）。

目标：让脚本能被命令行调用，别人不需要改代码就能用。

用法：
    python tools/log_cli.py tools\\sample.log
    python tools/log_cli.py tools\\sample.log --top 3
    python tools/log_cli.py tools\\sample.log --level ERROR

三个函数要你填：
    build_parser  —— 声明命令行有哪些参数
    report        —— 拿到参数后，把结果打印出来
    main          —— 把上面两步接起来

跑法：python tools/log_cli.py            （无参数时跑自测）
"""

import argparse
import contextlib
import io

from log_parse import (
    count_levels,
    module_messages,
    parse_log,
    read_text,
    time_span,
)


def build_parser():
    """创建一个参数解析器，声明三个参数：

    1. path        位置参数（必填），日志文件路径，help 写"日志文件路径"
    2. --top       可选，type=int，默认 10，help 写"显示前 N 条，默认 10"
    3. --level     可选，choices=["INFO", "WARN", "ERROR", "DEBUG"]，默认 None，
                   help 写"只统计某个级别"

    提示：
        p = argparse.ArgumentParser(description="车载日志解析工具")
        p.add_argument(...)      ← 三个参数，三次调用
        return p
    """
    p = argparse.ArgumentParser(description="车载日志解析工具")
    p.add_argument("path", help="日志文件路径")
    p.add_argument("--top", type=int, default=10, help="显示前 N 条，默认 10")
    p.add_argument(
        "--level",
        choices=["INFO", "WARN", "ERROR", "DEBUG"],
        default=None,
        help="只统计某个级别",
    )      
    return p


def report(path, top=10, level=None):
    """读取并解析日志，把结果打印到屏幕。输出必须严格长这样：

    总行数: 26, 有效: 25, 脏行: 1
    时间跨度: 2026-11-24 08:00:01 ~ 2026-11-24 08:20:05
    级别统计: INFO=15 WARN=4 ERROR=4 DEBUG=2
    模块消息（前 3 条）:
      system | boot sequence started
      ...

    规则：
    - 文件读不出来（read_text 返回 ""）→ 只打印一行 `文件读取失败或不存在: {path}` 就返回
    - 时间跨度用 time_span(records)
    - 级别统计格式：`键=值` 用空格连起来，顺序用 counts 的 most_common()（次数多的在前）
    - 如果 level 不是 None，先过滤 records 再取消息，并额外打印一行 `级别过滤: ERROR`
        （注意：时间跨度用过滤前的全部记录算）
    - 消息行格式：两个空格 + 模块 + " | " + 消息
    """
    text = read_text(path)
    if text == "":
        print(f"文件读取失败或不存在: {path}")
        return

    records, dirty = parse_log(text)
    print(f"总行数: {len(text.splitlines())}, 有效: {len(records)}, 脏行: {dirty}")

    start, end = time_span(records)
    print(f"时间跨度: {start} ~ {end}")

    counts = count_levels(records)
    print("级别统计: " + " ".join(f"{k}={v}" for k, v in counts.most_common()))

    if level is not None:
        records = [r for r in records if r["level"] == level]
        print(f"级别过滤: {level}")

    pairs = module_messages(records)[:top]
    print(f"模块消息（前 {top} 条）:")
    for mod, msg in pairs:
        print(f"  {mod} | {msg}")


def main(argv=None):
    """解析参数并调用 report。

    提示：args = build_parser().parse_args(argv)
          report(args.path, args.top, args.level)
    """
    args = build_parser().parse_args(argv)
    report(args.path, args.top, args.level)


# ---------------------------------------------------------------- 自测区
def _run(args):
    """跑一次 main，把屏幕输出抓成字符串返回（不用手动看终端）。"""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main(args)
    return buf.getvalue()


def _check():
    # 1 无选项：默认输出
    out = _run(["tools/sample.log"])
    assert "总行数: 26" in out, out
    assert "有效: 25" in out and "脏行: 1" in out, out
    assert "时间跨度: 2026-11-24 08:00:01 ~ 2026-11-24 08:20:05" in out, out
    assert "INFO=15" in out and "ERROR=4" in out, out
    print("[通过] 1 默认运行")

    # 2 --top 限制条数
    out = _run(["tools/sample.log", "--top", "2"])
    assert "前 2 条" in out, out
    assert out.count(" | ") == 2, out
    print("[通过] 2 --top 生效")

    # 3 --level 过滤
    out = _run(["tools/sample.log", "--level", "ERROR"])
    assert "级别过滤: ERROR" in out, out
    assert out.count(" | ") == 4, out
    print("[通过] 3 --level 过滤")

    # 4 文件读不出来
    out = _run(["tools/no_such_file.log"])
    assert "文件读取失败或不存在" in out, out
    print("[通过] 4 文件不存在不崩")

    print("\n全部通过。")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        main()
    else:
        _check()
