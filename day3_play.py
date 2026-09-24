"""
Day 3 草稿本
============
不是作业，是给你"看清楚每一步到底返回了什么"用的。
随便改、随便加 print、随便跑。跑完把想明白的东西抄回 day3_pandas_practice.py。

怎么跑：双击 run.bat 选这个文件，或在 VS Code 终端里
    python day3_play.py
想一行一行试，就在 VS Code 里新建 day3_play.ipynb（Jupyter 已装），
每个格子写一个表达式，回车立刻出结果 —— 学 pandas 最快的方式。
"""

import pandas as pd
from pathlib import Path

CSV = Path(__file__).parent / "stations_obs.csv"
df = pd.read_csv(CSV)


def show(title, x):
    print(f"\n--- {title} ---")
    print("类型:", type(x).__name__)
    print(x)


# 1. 先看数据长什么样
show("前 8 行", df.head(8))
show("每列有多少个非空值", df.count())
show("数值列的统计概览", df[["t2m", "rh", "precip", "wind"]].describe())

# 2. 取一列：df['列名']，出来的是 Series（一列数据）
show("取一列 df['t2m']", df["t2m"].head())

# 3. 唯一值：unique() 出来是 ndarray，要列表/排序就用 sorted
show("station 的唯一值", df["station"].unique())
show("唯一值排序后（q03 要的就是这个）", sorted(df["station"].unique()))

# 4. 布尔索引：条件是一个 True/False 的 Series，sum() 就是计数
show("条件 df['t2m'] > 25", (df["t2m"] > 25).head())
show("条件计数（q07 要这个）", (df["t2m"] > 25).sum())
show("isin（q09 要这个）", df["station"].isin(["NJ", "SH"]).sum())

# 5. 按位置/标签取值
show("iloc 按位置取第 5 行（q06）", df.iloc[5])
show("idxmax 找最大值那行的标签（q10）", df["t2m"].idxmax())
show("再用 loc 取这一行的 station", df.loc[df["t2m"].idxmax(), "station"])

# 6. groupby vs transform：这两个的区别是 Day 3 最值钱的东西
g = df.groupby("station")["t2m"].mean()
t = df.groupby("station")["t2m"].transform("mean")
show("groupby：每站一个数（4 行）", g)
show("transform：跟原表一样长（360 行），方便相减", t.head(8))
show("相减就是距平（q23）", (df["t2m"] - t).head(8))

# 7. 时间和透视
d = pd.to_datetime(df["date"])
show("date 转 datetime", d.head())
show("取月份", d.dt.month.unique())
tmp = df.copy()
tmp["date"] = d
show("设成索引后按月重采样", tmp.set_index("date")["t2m"].resample("ME").mean())

print("\n看懂了就回去写题。写一个跑一次，别憋大的。")
