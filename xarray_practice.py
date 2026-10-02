"""
第 2 周 · xarray 练习（12 题，自动判分）
=======================================

数据：era5_z500_20260101.nc
      2026-01-01 00:00 UTC，500 hPa 位势，东亚 15–60°N / 70–140°E
      变量名 z，单位 m**2 s**-2（位势，不是位势高度）

怎么用：跟 Day 2 / Day 3 一样 —— 每个函数里的
            return None
        换成你的答案，保存，然后跑本文件。最后会打印 "结果：n / 12 通过"。

跑法（三选一）：
    1. 双击 run.bat
    2. 把本文件拖到 run.bat 上
    3. & "C:\\Users\\18172\\miniconda3\\envs\\ai-met\\python.exe" "xarray_practice.py"

------------------------------------------------------------
动手之前，先把这三句话吃下去，12 题全是它的变体
------------------------------------------------------------
1. 一份 nc 文件里有三样东西：
      dim（维度）—— 数据的坐标轴，如 latitude / longitude / valid_time
      coord（坐标）—— 坐标轴上的标签值，如 latitude = 60, 59.75, ...
      data_var（变量）—— 数据本身，这里就是 z
   三者混在一起看很容易糊，记住：dim 是"轴"，coord 是"轴上的刻度"，var 是"格子里的数"。

2. sel 按【坐标值】取，isel 按【下标】取。
   z.sel(latitude=60)  和第 0 行是同一条线，因为 60°N 正好是第一个格点。
   但 z.sel(latitude=32, longitude=118.8) 里的 118.8 不在网格上（网格是 70, 70.25, ...），
   不加 method="nearest" 会直接报 KeyError。加了才会"找最近的"。

3. ERA5 的 latitude 是从【北往南】排的（60 递减到 15）。
   所以切片要"从大到小"写：slice(40, 20) 才有东西，slice(20, 40) 是空的。
   这个坑不报错，只是悄悄给你 0 行。
------------------------------------------------------------
"""

import sys
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import xarray as xr

# Windows 控制台是 GBK，遇到编码不了的字会直接把脚本打断，这里兜一下
try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

NC = "era5_z500_20260101.nc"
G = 9.80665  # m/s2，位势 -> 位势高度（gpm）


def load():
    return xr.open_dataset(NC)


# ============================================================
# 一、摸清结构（3 题）
# ============================================================


def q01():
    """z 的维度名，按原顺序返回【列表】。
    骨架：z.dims 是元组 -> list() 一下就成列表"""
    ds = load()
    z = ds["z"]
    return None


def q02():
    """纬度、经度各有多少个格点，返回 [n_lat, n_lon]。
    骨架：ds.latitude.size 就是一个整数"""
    ds = load()
    return None


def q03():
    """这份数据是哪个等压面？返回层次数值（浮点，如 500.0）。
    骨架：ds.pressure_level 是长度 1 的坐标 -> 取 [0] -> float()"""
    ds = load()
    return None


# ============================================================
# 二、sel 与 isel（4 题）—— 今天的核心
# ============================================================


def q04():
    """用代码证明 isel(latitude=0) 和 sel(latitude=60) 取到的是同一条线。
    返回 True / False。
    骨架：两个 DataArray 都有 .equals() 方法"""
    ds = load()
    z = ds["z"]
    return None


def q05():
    """用 isel 取【最南边】那一行（不用写 15 这个数字），返回它的纬度值。
    骨架：index = -1 表示倒数第一个"""
    ds = load()
    z = ds["z"]
    return None


def q06():
    """南京在 32°N, 118.8°E。取最近的格点，返回它【实际落在】的 [纬度, 经度]。
    骨架：sel(...) 之后 .latitude / .longitude 上再 sel 一次，或直接读回来"""
    ds = load()
    z = ds["z"]
    return None


def q07():
    """接上题，返回该格点的位势值（单位 m**2 s**-2，保留 2 位小数）。
    骨架：取出来是个 1×1 的 DataArray，用 .item() 才能变成普通数字"""
    ds = load()
    z = ds["z"]
    return None


# ============================================================
# 三、切片的方向坑（2 题）
# ============================================================


def q08():
    """返回 [slice(20,40) 取到几行, slice(40,20) 取到几行]。
    骨架：z.sel(latitude=slice(20, 40)).sizes["latitude"]"""
    ds = load()
    z = ds["z"]
    return None


def q09():
    """东亚 40–20°N / 100–125°E 这个区域的平均位势，保留 2 位小数。
    骨架：纬度记得从大到小写"""
    ds = load()
    z = ds["z"]
    return None


# ============================================================
# 四、降维与单位换算（3 题）
# ============================================================


def q10():
    """沿【经度】方向做平均之后，还剩哪些维度？返回维度名列表。
    骨架：z.mean(dim="longitude") —— 被平均掉的那个维度会消失"""
    ds = load()
    z = ds["z"]
    return None


def q11():
    """把位势换成位势高度（gpm，除以 G），返回南京格点的值，保留 2 位小数。
    骨架：先 .item() 拿到数，再 / G"""
    ds = load()
    z = ds["z"]
    return None


def q12():
    """z 里有两个长度为 1 的维度（valid_time、pressure_level），
    用 .squeeze() 挤掉它们，返回结果的 shape。
    骨架：.squeeze().shape 是个元组 -> list()"""
    ds = load()
    z = ds["z"]
    return None


# ============================================================
# 判分（下面不用改）
# ============================================================
import numpy as np

_passed = []


def _is_numlike(x):
    if isinstance(x, bool):
        return False
    if isinstance(x, (int, float, np.integer, np.floating)):
        return True
    return False


def _close(got, expected):
    try:
        a = np.asarray(got, dtype=float)
        b = np.asarray(expected, dtype=float)
        return a.shape == b.shape and bool(np.allclose(a, b, atol=1e-6))
    except Exception:
        return False


def check(label, fn, expected):
    try:
        got = fn()
    except Exception as e:
        got = "ERROR: %s: %s" % (type(e).__name__, e)

    ok = False
    try:
        if got is None or isinstance(got, str):
            ok = False
        elif isinstance(expected, bool):
            ok = isinstance(got, (bool, np.bool_)) and bool(got) is expected
        elif _is_numlike(expected) or isinstance(expected, (list, tuple, np.ndarray)):
            if not _is_numlike(got) and not isinstance(got, (list, tuple, np.ndarray)):
                ok = False
            else:
                if isinstance(got, (list, tuple)) and got and isinstance(got[0], str):
                    ok = list(got) == list(expected)
                else:
                    ok = _close(got, expected)
        else:
            ok = got == expected
    except Exception:
        ok = False

    if got is None:
        mark = "  ○  未作答"
    else:
        mark = "  √ " if ok else "  × "
    print("%s %-24s 你给的: %r" % (mark, label, got))
    if not ok and got is not None:
        print("       正确答案: %r" % (expected,))
    _passed.append(ok)


print("第 2 周 · xarray 练习")
print("=" * 52)

check("q01 z 的维度名", q01, ["valid_time", "pressure_level", "latitude", "longitude"])
check("q02 格点数 [lat, lon]", q02, [181, 281])
check("q03 等压面层次", q03, 500.0)

check("q04 isel(0) == sel(60)", q04, True)
check("q05 最南边那行的纬度", q05, 15.0)
check("q06 南京最近格点", q06, [32.0, 118.75])
check("q07 南京格点值", q07, 54501.61)

check("q08 切片方向 [0, 81]", q08, [0, 81])
check("q09 区域平均", q09, 55224.31)

check("q10 均值后剩余维度", q10, ["valid_time", "pressure_level", "latitude"])
check("q11 南京位势高度 gpm", q11, 5557.62)
check("q12 squeeze 后 shape", q12, [181, 281])

print("=" * 52)
n_ok = sum(_passed)
print("结果：%d / %d 通过" % (n_ok, len(_passed)))
if n_ok == len(_passed):
    print("全对了。Day 3(xarray) 收工，记得 git add / commit / push")
else:
    print("没过的题先自己想，卡超过 10 分钟再来问我")
print("=" * 52)
