# Day1 基础热身 2026-11-24
# 规则：每个函数都要 def 定义、有参数、有返回值；不要在文件顶层直接写逻辑。
# 用法：把每个函数里的 raise 那行删掉，换成你自己的实现，然后按 Ctrl+F5 运行看结果。

# ---------------------------------------------------------------- 1
def mult_table():
    """打印九九乘法表（1~9 行，每行 1~9 列，列到行号为止）。
    提示：内层 print 用 end=' ' 控制不换行，每行结束后单独 print() 换行。
    """
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(f"{j}*{i}={i*j}", end=' ')
        print()


# ---------------------------------------------------------------- 2
def sum_1_to_100():
    """用循环自己算 1 到 100 的和并返回。
    提示：循环里累加，不许直接 return 5050。
    """
    total = 0
    for i in range(1, 101):
        total += i
    return total



# ---------------------------------------------------------------- 3
def is_prime(n):
    """判断 n 是否素数，返回 True / False。
    提示：1 和小于 1 的数不是素数；试除到 i * i <= n 即可。
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# ---------------------------------------------------------------- 4
def reverse_str(s):
    """返回反转后的字符串（手写循环，不许用 s[::-1]）。
    写完后在文件末尾自己再补一个 reverse_str_slice(s) 用切片做一遍，比较结果。
    """
    result = ""
    for i in range(len(s) - 1, -1, -1):
        result += s[i]
    return result


# ---------------------------------------------------------------- 5
def fizzbuzz(n):
    """返回字符串：3 的倍数 Fizz，5 的倍数 Buzz，同时满足 FizzBuzz，其它返回 str(n)。
    提示：先判 15 的倍数，顺序错了 15 会先被 3 抢走。
    """
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


# ---------------------------------------------------------------- 6
def dedup(lst):
    """按原顺序去重，返回新列表（例如 [3,1,3,2,1] -> [3,1,2]）。
    写完后在注释里回答一句：为什么用 set 去重会丢顺序？
    答：
    """
    result, seen = [], set()
    for x in lst:
        if x not in seen:
           seen.add(x)
           result.append(x)
    return result

# ---------------------------------------------------------------- 7
def my_max(lst):
    """返回列表最大值，不许用内置 max()。
    提示：先把第一个元素当候选，再逐个比较；空列表返回 None。
    """
    if not lst:
        return None
    max_value = lst[0]
    for num in lst[1:]:
        if num > max_value:
            max_value = num
    return max_value



# ---------------------------------------------------------------- 8
def c2f(c):
    """摄氏度转华氏度，返回数值。公式：F = C × 9/5 + 32。"""
    raw = c * 9 / 5 + 32
    return raw


# ---------------------------------------------------------------- 9
def is_leap(year):
    """判断闰年，返回 True / False。
    提示：能被 4 整除，且（不能被 100 整除 或 能被 400 整除）。
    """
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False


# ---------------------------------------------------------------- 10
def calc(a, b, op):
    """传入两个数和运算符字符串（'+' '-' '*' '/'），返回计算结果。
    提示：用 if / elif 分支；除数为 0 时返回字符串提示，不能让程序崩掉。
    """
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            return "除数不能为 0"
        return a / b
    else:
        return "无效的运算符"


# ================================================================
# 以下是自测区，不用改。运行整个文件，逐题看到「通过」就说明这题做完了。
# ================================================================
def _check(name, fn):
    try:
        fn()
        print(f"[通过] {name}")
    except NotImplementedError:
        print(f"[待做] {name}")
    except Exception as e:
        print(f"[出错] {name} -> {type(e).__name__}: {e}")


def _test_1():
    mult_table()


def _test_2():
    assert sum_1_to_100() == 5050, "1 到 100 的和应为 5050"


def _test_3():
    assert is_prime(2) and is_prime(7) and is_prime(97)
    assert not is_prime(1) and not is_prime(9) and not is_prime(100)


def _test_4():
    assert reverse_str("abcd") == "dcba"
    assert reverse_str("测试") == "试测"


def _test_5():
    assert fizzbuzz(15) == "FizzBuzz"
    assert fizzbuzz(9) == "Fizz"
    assert fizzbuzz(10) == "Buzz"
    assert fizzbuzz(7) == "7"


def _test_6():
    assert dedup([3, 1, 3, 2, 1]) == [3, 1, 2]


def _test_7():
    assert my_max([3, 9, 2]) == 9
    assert my_max([-5, -2, -9]) == -2
    assert my_max([]) is None


def _test_8():
    assert abs(c2f(0) - 32) < 1e-9
    assert abs(c2f(100) - 212) < 1e-9


def _test_9():
    assert is_leap(2024) is True
    assert is_leap(1900) is False
    assert is_leap(2000) is True


def _test_10():
    assert calc(2, 3, "+") == 5
    assert calc(6, 3, "/") == 2
    r = calc(1, 0, "/")
    assert isinstance(r, str), "除以 0 应该返回提示字符串"


if __name__ == "__main__":
    _check("1 九九乘法表", _test_1)
    _check("2 1~100 求和", _test_2)
    _check("3 素数判断", _test_3)
    _check("4 字符串反转", _test_4)
    _check("5 FizzBuzz", _test_5)
    _check("6 列表去重", _test_6)
    _check("7 不用 max() 求最大值", _test_7)
    _check("8 摄氏度转华氏度", _test_8)
    _check("9 闰年判断", _test_9)
    _check("10 四则运算函数", _test_10)