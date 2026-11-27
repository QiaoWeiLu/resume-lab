"""Day3：车载日志解析 —— 正则命名分组 + 三类异常。

目标：把一份自动驾驶域控制器的运行日志，解析成结构化数据并做四项统计。

格式（每行）：
    2026-11-24 09:12:33 ERROR [perception] lane detection timeout
    └─日期──┘ └─时间──┘ └级别┘ └──模块──┘ └──────消息──────┘

约定：
- 空行忽略，不计入脏行。
- 格式不符的行（脏行）跳过并计数，程序不许崩。
- 文件不存在 → 返回空字符串，不抛异常。
- 编码：先按 utf-8 读，失败再按 gbk 读。

跑法：python tools\\log_parse.py
"""

import re

# ---------------------------------------------------------------- 正则模式
# 七个分组，用 re.VERBOSE 分行写、带注释。字段说明：
#   date   四位年-两位月-两位日
#   time   两位:两位:两位
#   level  一个或多个字母数字下划线
#   module 方括号里的一串
#   msg    剩下的全部（.+ 至少一个字符）
#
# 提示：方括号 [ ] 在正则里是"字符集"语法，要匹配字面的方括号必须转义成 \[ \]。
LOG_RE = re.compile(
    r"""
    (?P<date>\d{4}-\d{2}-\d{2})\s+
    (?P<time>\d{2}:\d{2}:\d{2})\s+
    (?P<level>\w+)\s+
    \[(?P<module>\w+)\]\s+
    (?P<msg>.+)
    """,
    re.VERBOSE,
)


def read_text(path):
    """读文件全文。

    - 文件不存在 → 返回 ""（捕获 FileNotFoundError）
    - 先 utf-8，读失败（UnicodeDecodeError）再试 gbk
    - 两次都失败 → 返回 ""
    """
    raise NotImplementedError


def parse_log(text):
    """把整段文本解析成 (records, dirty)。

    records：list[dict]，每个 dict 有 date/time/level/module/msg 五个键
    dirty：int，脏行条数

    步骤建议：
        1. text.splitlines() 逐行
        2. line.strip()，空的跳过（continue）
        3. LOG_RE.search(line)，None 就是脏行，dirty += 1
        4. 否则 m.groupdict() 直接得到一个五键字典，append 进 records
    """
    raise NotImplementedError


def count_levels(records):
    """统计各级别条数，返回 dict，例如 {'INFO': 15, 'WARN': 4}。

    提示：可以直接用 Counter，也可以用 dict.get —— 你昨晚两种都写过。
    """
    raise NotImplementedError


def time_span(records):
    """返回 (最早时间, 最晚时间) 两个字符串，格式 'YYYY-MM-DD HH:MM:SS'。

    提示：日期时间写成 'YYYY-MM-DD HH:MM:SS' 这种格式时，
    字符串比大小就等于时间比大小（因为高位在左边）。所以不用转 datetime。
    """
    raise NotImplementedError


def module_messages(records):
    """返回 list[tuple[str, str]]，每项是 (module, msg)。

    提示：这就是昨晚 `for k, v in d.items()` 反过来用的场景 ——
    从字典里取两个键拼成元组：`(r["module"], r["msg"])`。
    """
    raise NotImplementedError


# ---------------------------------------------------------------- 自测区
SAMPLE = """\
2026-11-24 08:00:01 INFO [system] boot sequence started
2026-11-24 08:00:03 DEBUG [system] config loaded from default.json
2026-11-24 08:00:05 INFO [camera] front camera stream opened
2026-11-24 08:00:08 INFO [perception] model version v2.3 loaded
2026-11-24 08:00:12 WARN [perception] image brightness below threshold
2026-11-24 08:00:15 INFO [planner] route buffer initialized
2026-11-24 08:00:20 INFO [control] steering loop ready
2026-11-24 08:00:25 DEBUG [can] 120 frames received
2026-11-24 08:05:11 INFO [planner] route updated
2026-11-24 08:05:30 WARN [can] cycle time 12ms exceeds 10ms
2026-11-24 08:06:02 INFO [perception] lane detection ok
2026-11-24 08:06:40 ERROR [perception] lane detection timeout
2026-11-24 08:06:41 WARN [perception] fallback to previous lane
2026-11-24 08:06:45 INFO [perception] lane detection recovered
this line is broken and should be skipped
2026-11-24 08:10:00 INFO [can] frame count reset
2026-11-24 08:10:30 ERROR [control] steering angle out of range
2026-11-24 08:10:31 INFO [control] steering angle clamped
2026-11-24 08:12:00 WARN [system] cpu usage 85%
2026-11-24 08:12:30 INFO [system] 系统自检完成
2026-11-24 08:15:00 INFO [planner] obstacle ahead id 7
2026-11-24 08:15:02 INFO [planner] re-planning triggered
2026-11-24 08:15:10 ERROR [can] bus off event
2026-11-24 08:15:12 INFO [can] bus recovered
2026-11-24 08:20:00 INFO [system] heartbeat
2026-11-24 08:20:05 ERROR [camera] stream frozen
"""


def _check():
    # 1 读文件：不存在 / utf-8 正常 / gbk 正常
    assert read_text("tools/no_such_file.log") == "", "不存在的文件应返回空字符串"
    assert "lane detection timeout" in read_text("tools/sample.log"), "utf-8 文件读取失败"
    assert "系统自检完成" in read_text("tools/sample_gbk.log"), "gbk 文件应能读出来"
    print("[通过] 1 读文件（不存在 / gbk 兼容）")

    # 2 解析：25 行有效 + 1 行脏行，总数 26 行
    records, dirty = parse_log(SAMPLE)
    assert len(SAMPLE.splitlines()) == 26
    assert dirty == 1, f"脏行应为 1，得到 {dirty}"
    assert len(records) == 25, f"有效行应为 25，得到 {len(records)}"
    assert records[0] == {
        "date": "2026-11-24",
        "time": "08:00:01",
        "level": "INFO",
        "module": "system",
        "msg": "boot sequence started",
    }
    print("[通过] 2 逐行解析 + 脏行计数")

    # 3 级别统计
    levels = count_levels(records)
    assert levels == {"INFO": 15, "WARN": 4, "ERROR": 4, "DEBUG": 2}, levels
    print("[通过] 3 级别统计")

    # 4 时间跨度
    assert time_span(records) == ("2026-11-24 08:00:01", "2026-11-24 08:20:05")
    print("[通过] 4 时间跨度")

    # 5 模块 + 消息
    pairs = module_messages(records)
    assert len(pairs) == 25
    assert pairs[0] == ("system", "boot sequence started")
    assert pairs[11] == ("perception", "lane detection timeout")
    print("[通过] 5 模块与消息列表")

    print("\n全部通过。")


if __name__ == "__main__":
    _check()
