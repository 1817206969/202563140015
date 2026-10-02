"""
Week 2 · 500 hPa 位势高度场
============================

做的事情：从 ERA5 下载等压面资料（500 hPa 位势高度），画一张能放进报告里的图。
对比第一周的 era5_first_look.py，这次多三样东西：
    1. 等压面变量（多了一个 level 维度）
    2. 位势高度单位换算：m2/s2 -> gpm（除以 9.80665）
    3. 出版级配图：填色 + 等值线 + 经纬网 + 国界 + 规范标题

跑之前：已配好 .cdsapirc（第一周做过），直接
    python week2_500hpa.py
想换日期，改下面的 DATE 就行。
"""

import os

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

DATE = "2026-01-01"
TIME = "00:00"
LEVEL = "500"
AREA = [60, 70, 15, 140]  # 北 西 南 东

NC_FILE = f"era5_z{LEVEL}_{DATE.replace('-', '')}.nc"
PNG_FILE = f"week2_z{LEVEL}_{DATE.replace('-', '')}.png"

G = 9.80665  # m/s2，把位势 m2/s2 换成位势高度 gpm


def download():
    import cdsapi

    y, m, d = DATE.split("-")
    print(f"向 CDS 提交请求：{DATE} {TIME} {LEVEL} hPa（首次可能排队几分钟）...")
    c = cdsapi.Client()
    c.retrieve(
        "reanalysis-era5-pressure-levels",
        {
            "product_type": "reanalysis",
            "variable": ["geopotential"],
            "pressure_level": [LEVEL],
            "year": y,
            "month": [m],
            "day": [d],
            "time": [TIME],
            "area": AREA,
            "format": "netcdf",
        },
        NC_FILE,
    )
    print("下载完成 ->", NC_FILE)


def get_time_dim(da):
    """新版 CDS 时间维叫 valid_time，旧版叫 time"""
    return "valid_time" if "valid_time" in da.dims else "time"


def plot():
    ds = xr.open_dataset(NC_FILE)
    print("\n=== 数据结构 ===")
    print(ds)

    da = ds["z"]
    tdim = get_time_dim(da)

    # 去掉时间和层次这两个长度为 1 的维度，剩下 (lat, lon)
    da = da.isel({tdim: 0})
    if "pressure_level" in da.dims:
        da = da.isel(pressure_level=0)
    elif "level" in da.dims:
        da = da.isel(level=0)

    tstr = str(da[tdim].values)[:16]
    # m2/s2 -> gpm，这是气象上的习惯单位
    z = da / G
    z.attrs["units"] = "gpm"

    fig, ax = plt.subplots(
        figsize=(11, 7), subplot_kw={"projection": ccrs.PlateCarree()}
    )

    # 填色
    cf = z.plot.contourf(
        ax=ax,
        transform=ccrs.PlateCarree(),
        cmap="Spectral_r",
        levels=np.arange(4800, 6000, 40),
        extend="both",
        cbar_kwargs={"label": "Geopotential height (gpm)", "shrink": 0.85, "pad": 0.02},
    )
    # 等值线：气象上习惯每 60 gpm 一根
    cs = z.plot.contour(
        ax=ax,
        transform=ccrs.PlateCarree(),
        levels=np.arange(4800, 6000, 60),
        colors="k",
        linewidths=0.8,
    )
    ax.clabel(cs, inline=True, fontsize=8, fmt="%d")

    ax.add_feature(cfeature.COASTLINE, linewidth=0.6)
    ax.add_feature(cfeature.BORDERS, linewidth=0.4, linestyle=":")

    ax.set_title(f"ERA5 {LEVEL} hPa Geopotential Height   {tstr} UTC", fontsize=13)
    ax.set_extent([70, 140, 15, 60], crs=ccrs.PlateCarree())

    gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="gray", alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False

    # 注意：这里故意不用 bbox_inches="tight"。
    # cartopy 的 gridlines(draw_labels=True) 和 set_extent 一起用时，
    # tight 裁剪会把画布算错，最后只剩一根色标。改用固定边距。
    fig.subplots_adjust(left=0.06, right=0.88, top=0.93, bottom=0.08)
    plt.savefig(PNG_FILE, dpi=150)
    print("出图 ->", PNG_FILE)


if __name__ == "__main__":
    if not os.path.exists(NC_FILE):
        download()
    else:
        print("数据已存在，跳过下载：", NC_FILE)
    plot()
