"""
Day 2 · NumPy 练习（带自动判分）
================================

怎么用：
1. 每个函数里 `return None` 的地方改成你的答案
2. 终端运行 `python day2_numpy_practice.py`
3. 看结果：✅ 通过 / ❌ 不对 / ⬜ 没做

不要急着看答案。卡住的题先读提示，再查 NumPy 官方文档：
https://numpy.org/doc/stable/reference/routines.html

背景设定：T 是一个假的温度场，单位开尔文 K
    维度顺序 = (时间, 纬度, 经度)，即 T.shape == (4, 3, 5)
    换算：摄氏度 = 开尔文 - 273.15
"""

import numpy as np

np.random.seed(20260917)
T = np.round(np.random.uniform(250, 310, size=(4, 3, 5)), 2)  # (time, lat, lon)

_passed = []


def check(name, fn, expected):
    try:
        got = fn()
    except Exception as e:
        print(f"  ❌ {name}  报错：{type(e).__name__}: {e}")
        _passed.append(False)
        return
    if got is None:
        print(f"  ⬜ {name}  未作答")
        _passed.append(False)
        return
    try:
        if isinstance(expected, str):
            assert str(got) == expected, f"得到 {got}，期望 {expected}"
        elif isinstance(expected, (tuple, list)) and not isinstance(got, np.ndarray):
            assert tuple(got) == tuple(expected), f"得到 {got}，期望 {expected}"
        else:
            np.testing.assert_allclose(
                np.asarray(got, dtype=float),
                np.asarray(expected, dtype=float),
                rtol=1e-5,
            )
        print(f"  ✅ {name}")
        _passed.append(True)
    except AssertionError:
        print(f"  ❌ {name}  结果不对（仔细看维度对不对）")
        _passed.append(False)


def section(title):
    print(f"\n{title}")
    print("-" * 46)


# ============================================================
# 一、创建数组
# ============================================================
section("【一】创建数组")


def q01():
    """创建一维数组 [0 1 2 ... 9]。提示：np.arange(10)"""
    return None


def q02():
    """创建 3 行 4 列的全 0 浮点数组。提示：np.zeros((3, 4))"""
    return None


def q03():
    """创建 2 行 3 列的全 1 数组，dtype 用 np.int32。返回它的 dtype 字符串"""
    return None


def q04():
    """0 到 1 之间等分成 5 个数。提示：np.linspace(0, 1, 5)"""
    return None


def q05():
    """15, 20, 25, 30, 35。提示：np.arange(起点, 终点, 步长)，终点取不到"""
    return None


check("Q01 arange", q01, np.arange(10))
check("Q02 zeros 3x4", q02, np.zeros((3, 4)))
check("Q03 int32 dtype", q03, "int32")
check("Q04 linspace", q04, np.linspace(0, 1, 5))
check("Q05 步长 5", q05, np.array([15, 20, 25, 30, 35]))


# ============================================================
# 二、形状与索引
# ============================================================
section("【二】形状与索引 —— 气象数据天天在用")


def q06():
    """T 的形状。返回 T.shape"""
    return None


def q07():
    """第 0 个时次的温度场，形状应该是 (3, 5)"""
    return None


def q08():
    """最后一个时次的温度场。提示：负索引"""
    return None


def q09():
    """所有时次中，纬度下标 1、经度下标 2 那个格点的时间序列，形状 (4,)"""
    return None


def q10():
    """取第 1 到第 2 个时次（不含 3），所有纬度，经度下标 0 到 1。形状应为 (2, 3, 2)"""
    return None


check("Q06 T.shape", q06, (4, 3, 5))
check("Q07 第 0 时次", q07, T[0])
check("Q08 最后时次", q08, T[-1])
check("Q09 单点时间序列", q09, T[:, 1, 2])
check("Q10 切片", q10, T[1:3, :, :2])


# ============================================================
# 三、轴 axis —— 这一节最重要
# ============================================================
section("【三】轴 axis —— 最容易搞混，务必弄懂")


def q11():
    """时间平均：对每个格点沿 axis=0 求均值。结果形状 (3, 5)"""
    return None


def q12():
    """每个时次的全域平均：对 axis=(1, 2) 求均值。形状 (4,)"""
    return None


def q13():
    """沿经度平均：axis=2。形状 (4, 3)"""
    return None


def q14():
    """整个场的平均温度，一个标量"""
    return None


def q15():
    """整个场的最低温度出现在哪个位置。提示：np.argmin + np.unravel_index，返回元组"""
    return None


check("Q11 时间平均", q11, T.mean(axis=0))
check("Q12 逐时次全域平均", q12, T.mean(axis=(1, 2)))
check("Q13 沿经度平均", q13, T.mean(axis=2))
check("Q14 全场均值", q14, T.mean())
check("Q15 最低温位置", q15, np.unravel_index(np.argmin(T), T.shape))


# ============================================================
# 四、广播 broadcasting
# ============================================================
section("【四】广播 —— NumPy 的灵魂")


def q16():
    """开尔文转摄氏度：T - 273.15"""
    return None


def q17():
    """
    距平：每个时次的场减去全场时间平均（Q11 的结果）。
    时间平均形状是 (3,5)，T 形状是 (4,3,5)，为什么能直接减？想明白这点广播就通了。
    """
    return None


def q18():
    """列向量 + 行向量：np.array([[1],[2],[3]]) + np.array([10, 20])，结果应为 3 行 2 列"""
    return None


def q19():
    """给一维数组 a = np.arange(5) 在第 0 维前面加一个轴，变成形状 (1, 5)。提示：a[np.newaxis, :]"""
    return None


def q20():
    """
    每个纬度减去该纬度的平均值。
    提示：先 T.mean(axis=(0, 2), keepdims=True)，注意 keepdims 的作用
    """
    return None


check("Q16 K 转 ℃", q16, T - 273.15)
check("Q17 距平场", q17, T - T.mean(axis=0))
check("Q18 行列广播", q18, np.array([[11, 12], [21, 22], [31, 32]]))
check("Q19 newaxis", q19, np.arange(5)[np.newaxis, :])
check("Q20 纬向距平", q20, T - T.mean(axis=(0, 2), keepdims=True))


# ============================================================
# 五、布尔索引与缺测处理 —— 处理实测数据必备
# ============================================================
section("【五】布尔索引与缺测")

T_missing = T.copy()
T_missing[0, 0, 0] = -999.0  # 模拟缺测值


def q21():
    """T 中有多少个格点温度高于 300K？返回整数"""
    return None


def q22():
    """把 T 中所有高于 300K 的值取出来，组成一维数组。提示：布尔索引 T[T > 300]"""
    return None


def q23():
    """缺测检测：返回一个布尔数组，标记哪些位置是缺测（-999）"""
    return None


def q24():
    """把缺测值替换成 np.nan，返回处理后的数组。提示：np.where"""
    return None


def q25():
    """对处理后的数组求均值，忽略 nan。提示：np.nanmean"""
    return None


_T_fixed = np.where(T_missing == -999.0, np.nan, T_missing)

check("Q21 高温格点数", q21, int((T > 300).sum()))
check("Q22 布尔索引取值", q22, T[T > 300])
check("Q23 缺测掩码", q23, T_missing == -999.0)
check("Q24 -999 转 nan", q24, _T_fixed)
check("Q25 nanmean", q25, np.nanmean(_T_fixed))


# ============================================================
# 六、变形与拼接
# ============================================================
section("【六】变形与拼接")


def q26():
    """把 T 拉平成 (4, 15)：每个时次一行。提示：reshape"""
    return None


def q27():
    """维度重排：把 T 从 (时间,纬,经) 变成 (经,纬,时间)，形状 (5, 3, 4)。提示：transpose(2, 1, 0)"""
    return None


def q28():
    """把两个 (3, 5) 的场沿时间维拼起来，形状 (2, 3, 5)。提示：np.stack"""
    return None


def q29():
    """把两个 (3, 5) 的场沿纬度方向接起来，形状 (6, 5)。提示：np.concatenate + axis"""
    return None


def q30():
    """把 T 摊成一维。提示：ravel 或 flatten。长度应为 60"""
    return None


check("Q26 reshape", q26, T.reshape(4, 15))
check("Q27 transpose", q27, T.transpose(2, 1, 0))
check("Q28 stack", q28, np.stack([T[0], T[1]], axis=0))
check("Q29 concatenate", q29, np.concatenate([T[0], T[1]], axis=0))
check("Q30 ravel", q30, T.ravel())


# ============================================================
print("\n" + "=" * 46)
n_ok = sum(_passed)
print(f"结果：{n_ok} / {len(_passed)} 通过")
if n_ok == len(_passed):
    print("全对了。Day 2 收工，记得 git add / commit / push")
else:
    print("没过的题先自己想，卡超过 10 分钟再来问我")
print("=" * 46)
