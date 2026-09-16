"""
ERA5 第一次上手：下载 + 画图
================================

运行前必须先配好 .cdsapirc（只做一次）：

1. 登录 https://cds.climate.copernicus.eu/
2. 右上角头像 → Your profile（个人资料）
3. 找到 "API key" / "Show API key" 一栏，复制里面给出的两行内容，
   形如：
       url: https://cds.climate.copernicus.eu/api
       key: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   （不同时期页面给的 url 可能带 /api 或 /api/v2，原样复制即可）
4. 把这两行存成文件 C:\\Users\\18172\\.cdsapirc
   Windows 下用命令行创建：
       type nul > %USERPROFILE%\\.cdsapirc
   然后用记事本打开粘贴，保存。注意文件名开头有个点，没有后缀。

配置好之后运行：
    conda activate ai-met
    python era5_first_look.py
"""

import os
import cdsapi
import xarray as xr
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

NC_FILE = "era5_t2m_20260101.nc"
# 区域框：北纬60、西经70、南纬15、东经140 —— 覆盖东亚
AREA = [60, 70, 15, 140]


def download():
    print("正在向 CDS 提交请求（首次可能要排队几分钟）...")
    c = cdsapi.Client()
    c.retrieve(
        "reanalysis-era5-single-levels",
        {
            "product_type": "reanalysis",
            "variable": ["2m_temperature"],
            "year": "2026",
            "month": ["01"],
            "day": ["01"],
            "time": ["00:00", "06:00", "12:00", "18:00"],
            "area": AREA,
            "format": "netcdf",
        },
        NC_FILE,
    )
    print("下载完成 ->", NC_FILE)


def plot():
    ds = xr.open_dataset(NC_FILE)
    print("\n=== 数据结构 ===")
    print(ds)

    # 新版 CDS 把时间维度命名为 valid_time，旧版是 time
    tdim = "valid_time" if "valid_time" in ds["t2m"].dims else "time"
    da = ds["t2m"].isel({tdim: 0})
    # ERA5 单位是 K，顺便转成摄氏度便于读图
    da_c = da - 273.15
    da_c.attrs["units"] = "degC"

    import cartopy.crs as ccrs

    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.PlateCarree()})
    da_c.plot(ax=ax, transform=ccrs.PlateCarree(), cmap="coolwarm", cbar_kwargs={"label": "2m temperature (degC)"})
    ax.coastlines()
    ax.gridlines(draw_labels=True)
    ax.set_title(f"ERA5 2m temperature  {str(da[tdim].values)[:16]}")
    ax.set_extent([70, 140, 15, 60], crs=ccrs.PlateCarree())
    out = "era5_first_figure.png"
    plt.savefig(out, dpi=120, bbox_inches="tight")
    print("出图 ->", out)


if __name__ == "__main__":
    if not os.path.exists(NC_FILE):
        download()
    else:
        print("数据已存在，跳过下载：", NC_FILE)
    plot()
