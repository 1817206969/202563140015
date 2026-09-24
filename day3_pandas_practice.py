"""
Day 3 · Pandas 练习（带自动判分）
================================

怎么用：
1. 每个函数里 `return None` 的地方改成你的答案
2. 终端运行 `python day3_pandas_practice.py`
3. 看结果：✅ 通过 / ❌ 不对 / ⬜ 没做

数据：stations_obs.csv —— 4 个站点 2025 年 1–3 月逐日观测，360 行
    date    日期（字符串，需要自己转 datetime）
    station 站号：NJ 南京 / SH 上海 / BJ 北京 / GZ 广州
    city    城市名
    t2m     2 米气温，℃
    rh      相对湿度，%
    precip  降水量，mm，-999 表示缺测
    wind    风速，m/s

每题开头先写 df = load()，拿到一份干净副本。
卡住先自己想，再查官方文档：https://pandas.pydata.org/docs/reference/
"""

import numpy as np
import pandas as pd
from pathlib import Path

CSV = Path(__file__).parent / "stations_obs.csv"

# 站点信息表（第 6 组 merge 用）
STATION_INFO = pd.DataFrame(
    {
        "station": ["NJ", "SH", "BJ", "GZ"],
        "province": ["江苏", "上海", "北京", "广东"],
        "lat": [32.06, 31.23, 39.90, 23.13],
        "lon": [118.80, 121.47, 116.41, 113.26],
    }
)


def load():
    """每次返回一份干净的副本，随便改，不影响下一题"""
    return pd.read_csv(CSV)


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
        elif isinstance(expected, (list, tuple)):
            assert len(got) == len(expected), f"长度不对：{len(got)} vs {len(expected)}"
            if all(isinstance(x, (int, float, np.integer, np.floating)) for x in expected):
                for g, e in zip(got, expected):
                    assert np.isclose(float(g), float(e), rtol=1e-4, atol=1e-4), (
                        f"得到 {list(got)}，期望 {list(expected)}"
                    )
            else:
                assert list(got) == list(expected), f"得到 {list(got)}，期望 {list(expected)}"
        else:
            assert np.isclose(float(got), float(expected), rtol=1e-4, atol=1e-4), (
                f"得到 {got}，期望 {expected}"
            )
        print(f"  ✅ {name}")
        _passed.append(True)
    except AssertionError as e:
        print(f"  ❌ {name}  {e}")
        _passed.append(False)
    except Exception as e:
        print(f"  ❌ {name}  {type(e).__name__}：多半是类型不对")
        _passed.append(False)


def section(title):
    print(f"\n{title}")
    print("-" * 46)


# ============================================================
# 一、读进来，看一眼
# ============================================================
section("【一】读进来，看一眼")


def q01():
    """读 CSV，返回行数。提示：len(df)"""
    df = load()
    return len(df)


def q02():
    """返回所有列名的列表。提示：list(df.columns)"""
    df = load()
    return list(df.columns)


def q03():
    """返回 station 列的唯一值（排序后）列表。提示：sort + unique"""
    df = load()
    # unique() 出来是 numpy 数组且无序，外面套 sorted() 才是排好序的列表
    return sorted(df["station"].unique())


def q04():
    """返回 t2m 的均值，保留 2 位小数。提示：round(float(...), 2)"""
    df = load()
    # mean() 出来是 numpy 浮点数，float() 转成普通小数，round() 留 2 位
    return round(float(df["t2m"].mean()), 2)


def q05():
    """返回 t2m 的最大值，保留 2 位小数"""
    df = load()
    return round(float(df["t2m"].max()), 2)


# ============================================================
# 二、挑数据：loc / iloc / 布尔索引
# ============================================================
section("【二】挑数据：loc / iloc / 布尔索引")


def q06():
    """用 iloc 取第 5 行（下标 5），返回它的 city。返回字符串"""
    df = load()
    return df.iloc[5]["city"]


def q07():
    """气温高于 25℃ 的记录有多少条？返回整数。
    提示：(df['t2m'] > 25).sum()"""
    df = load()
    return (df['t2m'] > 25).sum()


def q08():
    """气温 > 20 且 湿度 < 60 的记录有多少条？
    注意多条件用 & 连接，每个条件都要加括号"""
    df = load()
    # 两个条件各自加括号，用 & 连起来，整体再加一层括号才能 .sum()
    return ((df["t2m"] > 20) & (df["rh"] < 60)).sum()


def q09():
    """station 属于 ['NJ', 'SH'] 的记录有多少条？提示：isin"""
    df = load()
    # isin 收的是「一个平铺的列表」，不是列表套列表
    return df["station"].isin(["NJ", "SH"]).sum()


def q10():
    """气温最高的那条记录，是哪个站？返回站号字符串。
    提示：idxmax 拿到行标签，再 loc 取值"""
    df = load()
    return df.loc[df["t2m"].idxmax(),"station"]


# ============================================================
# 三、造新列：算术 / 分箱 / apply
# ============================================================
section("【三】造新列：算术 / 分箱")


def q11():
    """新增华氏温度列 t2m_f = t2m * 9/5 + 32，返回它的均值（保留 2 位）"""
    df = load()
    # 整列一起算，pandas 会自动对每个元素运算，不用写循环
    df["t2m_f"] = df["t2m"] * 9 / 5 + 32
    return round(float(df["t2m_f"].mean()), 2)


def q12():
    """用 pd.cut 给气温分档：(-50,5] 冷 / (5,18] 温和 / (18,60] 热
    返回三档的条数，顺序 [冷, 温和, 热]。
    提示：pd.cut(df['t2m'], bins=[-50,5,18,60], labels=['冷','温和','热'])
    再 value_counts().reindex(['冷','温和','热'])"""
    df = load()
    # pd.cut 的结果要存进变量，不然算完就丢了
    lv = pd.cut(df["t2m"], bins=[-50, 5, 18, 60], labels=["冷", "温和", "热"])
    # value_counts 数每档几条，reindex 把顺序固定成 冷/温和/热
    return lv.value_counts().reindex(["冷", "温和", "热"]).tolist()


def q13():
    """在【热】这一档里，平均相对湿度是多少？保留 2 位"""
    df = load()
    lv = pd.cut(df["t2m"], bins=[-50, 5, 18, 60], labels=["冷", "温和", "热"])
    # 题目要求保留 2 位，mean() 的裸结果位数太长，判分会不认
    return round(float(df.loc[lv == "热", "rh"].mean()), 2)


def q14():
    """把风速换成 km/h（乘 3.6），返回最大值，保留 2 位"""
    df = load()
    # wind 是 df 里的一列，得写成 df["wind"]；还要 .max() 才是最大值
    return round(float((df["wind"] * 3.6).max()), 2)


# ============================================================
# 四、时间：这才是气象数据的骨架
# ============================================================
section("【四】时间：气象数据的骨架")


def q15():
    """把 date 列用 pd.to_datetime 转成时间，返回出现过的月份（排序）列表。
    提示：pd.to_datetime(df['date']).dt.month.unique()"""
    df = load()
    # 先把字符串日期转成 datetime，存进变量；之后才能用 .dt 取月份
    d = pd.to_datetime(df["date"])
    return sorted(d.dt.month.unique().tolist())


def q16():
    """数据跨度多少天？（最大日期减最小日期的天数）返回整数"""
    df = load()
    d = pd.to_datetime(df["date"])
    return int((d.max()-d.min()).days)


def q17():
    """把 date 转成 datetime 后设为索引，按月重采样求 t2m 月均值，
    返回 3 个月均值的列表（保留 2 位）。
    提示：df.set_index('date')['t2m'].resample('ME').mean()"""
    df = load()
    d = pd.to_datetime(df["date"])
    # set_index 要的是「已经转好的时间」，不是原来那列字符串
    df = df.set_index(d)
    return df["t2m"].resample("ME").mean().round(2).tolist()


# ============================================================
# 五、groupby：分组统计，日常用得最多
# ============================================================
section("【五】groupby：用得最多的一个")


def q18():
    """按 station 分组求 t2m 均值，按站号排序后返回列表（保留 2 位）。
    顺序是 BJ / GZ / NJ / SH"""
    df = load()
    # groupby 得到「每站一个数」，sort_index 按站号排序，round 留 2 位
    return df.groupby("station")["t2m"].mean().sort_index().round(2).tolist()


def q19():
    """按 station 分组求 precip 总和（先别管 -999），返回列表（保留 1 位）。
    你会看到很离谱的负数 —— 这就是没处理缺测的下场"""
    df = load()
    # sum 是方法，要写 sum()；写成 sum 拿到的是函数本身，后面接不了 .round
    return df.groupby("station")["precip"].sum().round(1).tolist()


def q20():
    """按 station 分组，同时对 t2m 和 rh 求均值，返回结果的 shape，如 (4, 2)。
    提示：df.groupby('station')[['t2m','rh']].mean().shape"""
    df = load()
    return df.groupby('station')[["t2m","rh"]].mean().shape


def q21():
    """先加一列 month（从 date 里取月份），再按 ['station','month'] 分组求 t2m 均值，
    返回 ('NJ', 2) 这一组的值，保留 2 位。
    提示：多级索引用 .loc[('NJ', 2)]"""
    df = load()
    df["month"] = pd.to_datetime(df["date"]).dt.month
    # 分组后要指明算哪一列、怎么算，再取多级索引 ('NJ', 2)
    g = df.groupby(["station", "month"])["t2m"].mean()
    return round(float(g.loc[("NJ", 2)]), 2)


def q22():
    """按 station 分组，对 t2m 同时求 mean / max / min
    （agg(['mean','max','min'])），返回北京 BJ 的 max，保留 2 位"""
    df = load()
    return df.groupby("station")["t2m"].agg(["mean","max","min"]).loc["BJ","max"]


def q23():
    """算站内距平：每个站的气温减去该站的均值。
    用 transform 得到"跟原表一样长"的站均值再相减：
        df['t2m'] - df.groupby('station')['t2m'].transform('mean')
    返回距平的均值，保留 6 位（应该几乎等于 0）"""
    df = load()
    # 相减得到的是一整列（360 个距平），要再 .mean() 才是题目要的那个数
    anom = df["t2m"] - df.groupby("station")["t2m"].transform("mean")
    return round(float(anom.mean()), 6)


def q24():
    """按 station 分组求 wind 的中位数，中位数最大的那个站是哪个？返回站号。
    提示：.median().idxmax()"""
    df = load()
    return df.groupby(["station"]).wind.median().idxmax()


# ============================================================
# 六、缺测 / merge / pivot：真实数据三件套
# ============================================================
section("【六】缺测 / merge / pivot")


def q25():
    """precip 里 -999 有多少条？返回整数"""
    df = load()
    # 等于 -999 是个布尔条件，sum() 数 True 的个数
    return int((df["precip"] == -999).sum())


def q26():
    """把 -999 换成 NaN 后，缺失值有多少个？
    提示：df['precip'].replace(-999, np.nan).isna().sum()"""
    df = load()
    return df['precip'].replace(-999, np.nan).isna().sum()


def q27():
    """把 -999 换成 NaN，再 fillna(0)，然后按 station 求 precip 总和，
    返回列表（保留 1 位）。这才是人能看的数"""
    df = load()
    # 先把缺测处理干净，再分组求和 —— 顺序反了就是 q19 那种负数
    df["precip"] = df["precip"].replace(-999, np.nan).fillna(0)
    return df.groupby("station")["precip"].sum().round(1).tolist()


def q28():
    """把 STATION_INFO 左连接进 df（on='station'），返回合并后的列数。
    提示：df.merge(STATION_INFO, on='station', how='left')"""
    df = load()
    # merge 出来是一张新表，题目要的是列数，所以取 shape[1]
    return df.merge(STATION_INFO, on="station", how="left").shape[1]


def q29():
    """先加 month 列，再做透视表：
        pivot_table(index='month', columns='station', values='t2m', aggfunc='mean')
    返回它的 shape，如 (3, 4)"""
    df = load()
    df["month"] = pd.to_datetime(df["date"]).dt.month
    pv = df.pivot_table(index="month", columns="station", values="t2m", aggfunc="mean")
    return pv.shape


def q30():
    """接上题的透视表，返回 2 月（month=2）广州 GZ 的月均温，保留 2 位。
    提示：pv.loc[2, 'GZ']"""
    df = load()
    df["month"] = pd.to_datetime(df["date"]).dt.month
    pv = df.pivot_table(index="month", columns="station", values="t2m", aggfunc="mean")
    return round(float(pv.loc[2, "GZ"]), 2)


# ============================================================
# 判分
# ============================================================
print("Day 3 · Pandas 练习")
print("=" * 46)

check("q01 读 CSV 看行数", q01, 360)
check("q02 列名", q02, ["date", "station", "city", "t2m", "rh", "precip", "wind"])
check("q03 站点唯一值", q03, ["BJ", "GZ", "NJ", "SH"])
check("q04 平均气温", q04, 11.34)
check("q05 最高气温", q05, 30.3)

check("q06 iloc 取行", q06, "广州")
check("q07 布尔筛选计数", q07, 10)
check("q08 多条件筛选", q08, 3)
check("q09 isin 筛选", q09, 180)
check("q10 idxmax 定位", q10, "GZ")

check("q11 华氏度均值", q11, 52.42)
check("q12 温度分档计数", q12, [73, 216, 71])
check("q13 热档平均湿度", q13, 69.32)
check("q14 风速换算", q14, 25.56)

check("q15 月份取值", q15, [1, 2, 3])
check("q16 时间跨度", q16, 89)
check("q17 月重采样", q17, [7.37, 11.56, 15.12])

check("q18 站点平均气温", q18, [4.45, 20.47, 9.14, 11.31])
check("q19 降水总和（踩坑）", q19, [-2711.7, -3664.0, -2699.1, -3717.5])
check("q20 多列聚合 shape", q20, [4, 2])
check("q21 两级分组取值", q21, 9.53)
check("q22 agg 多函数", q22, 12.9)
check("q23 transform 算距平", q23, 0.0)
check("q24 中位数最大站", q24, "BJ")

check("q25 缺测计数", q25, 14)
check("q26 转 NaN 后计数", q26, 14)
check("q27 处理后降水总和", q27, [285.3, 332.0, 297.9, 278.5])
check("q28 merge 后列数", q28, 10)
check("q29 透视表 shape", q29, [3, 4])
check("q30 透视表取值", q30, 20.65)

print("\n" + "=" * 46)
n_ok = sum(_passed)
print(f"结果：{n_ok} / {len(_passed)} 通过")
if n_ok == len(_passed):
    print("全对了。Day 3 收工，记得 git add / commit / push")
else:
    print("没过的题先自己想，卡超过 10 分钟再来问我")
print("=" * 46)
