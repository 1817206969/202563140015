"""
Week 2 · 下载 850/500/200 hPa 位势高度（2026 年 1 月整月）
==========================================================
给后面的「距平图」和「纬度-气压剖面图」准备数据。

一次请求拿三样东西：
    - 一个月 × 4 次/天 = 124 个时次  -> 能算气候态、算距平、画时间序列
    - 850 / 500 / 200 三个层次        -> 能画垂直剖面

输出：era5_z_3lev_202601.nc
"""

import os
import sys

import cdsapi

OUT = "era5_z_3lev_202601.nc"
AREA = [60, 70, 15, 140]  # 北 西 南 东


def main():
    if os.path.exists(OUT) and os.path.getsize(OUT) > 0:
        print("已存在，跳过：", OUT)
        return
    c = cdsapi.Client()
    print("提交请求：2026-01 全月，geopotential，850/500/200 hPa ...")
    sys.stdout.flush()
    c.retrieve(
        "reanalysis-era5-pressure-levels",
        {
            "product_type": "reanalysis",
            "variable": ["geopotential"],
            "pressure_level": ["850", "500", "200"],
            "year": "2026",
            "month": ["01"],
            "day": [f"{d:02d}" for d in range(1, 32)],
            "time": ["00:00", "06:00", "12:00", "18:00"],
            "area": AREA,
            "format": "netcdf",
        },
        OUT,
    )
    print("下载完成 ->", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
