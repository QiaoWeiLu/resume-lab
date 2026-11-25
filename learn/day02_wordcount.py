# Day2 词频统计 2026-11-25
# 规则：函数只负责算，读写文件/打印放在函数外；每个函数都要有 docstring 说明的返回值。
# 用法：填完函数体按 Ctrl+F5，逐题看到「通过」为止。

from collections import Counter

# ---------------------------------------------------------------- 1
def read_text(path):
    """读文件并返回全文（字符串）。
    要求：
    - 文件不存在时返回 ""，不许抛异常（用 try/except FileNotFoundError）
    - 用 encoding='utf-8', errors='replace' 兜底编码问题
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except FileNotFoundError:
        return ""


# ---------------------------------------------------------------- 2
def tokenize(text):
    """把文本切成单词列表，返回 list[str]。
    要求：
    - 全部转小写
    - 标点换成空格（建议用 str.maketrans 或逐个 replace）
    - 用 .split() 按空白切分，自动去掉空字符串
    示例：tokenize("Hello, world! hello.") -> ['hello', 'world', 'hello']
    """
    text = text.lower()                      # ① 全小写
    for ch in ",.!?;:\"'()":                 # ② 标点逐个换成空格
        text = text.replace(ch, " ")
    return text.split()


# ---------------------------------------------------------------- 3
def count_with_counter(words):
    """用 Counter 统计，返回 Counter 对象。"""
    return Counter(words)


# ---------------------------------------------------------------- 4
def count_manual(words):
    """用普通字典手写累计，返回 dict[str, int]。
    要求：不许 import Counter，用 d.get(word, 0) + 1 的思路。
    """
    c = {}
    for word in words:
        c[word] = c.get(word, 0) + 1
    return c    


# ---------------------------------------------------------------- 5
def top_n(counts, n=10):
    """返回前 n 名，形如 [('hello', 2), ('world', 1)]。
    counts 可能是 Counter 也可能是普通 dict，两种都要能用。
    提示：Counter 用 most_common(n)；dict 用 sorted(counts.items(), key=..., reverse=True)。
    """
    if hasattr(counts, "most_common"):
        return counts.most_common(n)
    return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:n]


# ================================================================
# 自测区：不用改。运行整个文件，逐题看到「通过」就说明这题做完了。
# ================================================================
import tempfile
import os

SAMPLE = "Hello, world! Hello pytest.\nWorld is big; hello, world."


def _check(name, fn):
    try:
        fn()
        print(f"[通过] {name}")
    except NotImplementedError:
        print(f"[待做] {name}")
    except Exception as e:
        print(f"[出错] {name} -> {type(e).__name__}: {e}")


def _test_1():
    assert read_text("这个文件一定不存在_abc.txt") == ""
    fd, p = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    try:
        assert read_text(p) == ""          # 空文件返回空字符串
        with open(p, "w", encoding="utf-8") as f:
            f.write("中文 English")
        assert read_text(p) == "中文 English"
    finally:
        os.remove(p)


def _test_2():
    assert tokenize("Hello, world! hello.") == ["hello", "world", "hello"]
    assert tokenize("  A  b\n c ") == ["a", "b", "c"]


def _test_3():
    c = count_with_counter(tokenize(SAMPLE))
    assert isinstance(c, Counter)
    assert c["hello"] == 3 and c["world"] == 3


def _test_4():
    c = count_manual(tokenize(SAMPLE))
    assert isinstance(c, dict) and not isinstance(c, Counter)
    assert c["hello"] == 3 and c["world"] == 3


def _test_5():
    words = tokenize(SAMPLE)
    assert top_n(count_with_counter(words), 2)[0][1] == 3
    assert top_n(count_manual(words), 2)[0][1] == 3
    assert len(top_n(count_manual(words), 10)) <= 10


if __name__ == "__main__":
    _check("1 读文件（不存在/空/正常）", _test_1)
    _check("2 切词", _test_2)
    _check("3 Counter 统计", _test_3)
    _check("4 字典手写统计", _test_4)
    _check("5 取前 N 名", _test_5)
