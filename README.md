# AI 气象学习记录 · ly

南京信息工程大学 · 大气科学 · 大二

方向：AI 气象（数据驱动天气预报与气候预测）。目标是一年内具备进组干活的
能力，同时打竞赛出成果。

## 这周要做的（第 2 周：气象数据入门）

- 用 xarray 啃熟 NetCDF：dim / coord / variable，`sel` 与 `isel` 的区别
- ERA5 等压面数据（500 hPa 位势高度）下载到出图
- 画一张能放进报告的图：填色 + 等值线 + 经纬网 + 国界 + 规范标题

## 进度

- **2026-09-16**：环境配好（conda 环境 `ai-met`，Python 3.11）；首次提交；
  ERA5 第一份数据下载成功（2026-01-01 东亚 2m 温度）并出图
- **2026-09-17**：Day 2 NumPy 练习 30/30（轴、广播、布尔索引、缺测）；
  Day 3 Pandas 练习开工（`day3_pandas_practice.py` + 站点观测数据
  `stations_obs.csv`，4 站 × 90 天 × 360 行）
- **2026-09-24**：Day 3 Pandas 30 题全过（groupby / transform / 缺测 / merge / pivot）
- **2026-09-25**：ERA5 500 hPa 位势高度图（`week2_500hpa.py` / `week2_z500_20260101.png`）
- **2026-09-26 ~ 10-01**：无提交
- **2026-10-02**：xarray 12 题练习（`xarray_practice.py`）；
  后台下载 2026-01 整月 × 850/500/200 三层位势（`era5_z_3lev_202601.nc`），
  为「距平图」和「纬度–气压剖面图」备料

## 第 1 周复盘（9.16–9.24）

**做了什么**
- 搭齐环境：conda `ai-met`（numpy / pandas / xarray / cartopy / metpy）
- 打通 ERA5 下载 → xarray 读取 → cartopy 出图的完整链路
- NumPy 30 题、Pandas 30 题全部通过
- GitHub 仓库 `202563140015` 建起来，累计提交 10 次

**卡在哪**
- 环境上耗了最多时间：机器上有个 MSYS2 自带的 Python 排在 PATH 最前面，
  导致 `python` 一直指向没有包的那个，折腾了好几轮才定位
- Pandas 的丢分几乎不在概念，全在链式调用的细节：漏括号、`sum` 写成 `sum`、
  算完不存变量、把列当独立变量用

**下周改什么**
- 不再在环境问题上纠缠：跑脚本一律用完整路径或 `run.bat`
- 每道题先想清楚"这一步返回的是标量、Series 还是 DataFrame"再动手
- 保证每天有一次提交

## 目录说明

| 文件 | 内容 |
|---|---|
| `AI气象学习路线-ly.md` | 一年的主线规划、子方向、竞赛与进组清单 |
| `第1周任务卡-9.17至9.22.md` | 逐日任务、网课资源、避坑 |
| `era5_first_look.py` | ERA5 单层数据（2m 温度）下载 + 出图 |
| `era5_first_figure.png` | 第一张真实数据图 |
| `week2_500hpa.py` | 第 2 周：ERA5 等压面 500 hPa 位势高度，出版级配图 |
| `week2_download_3lev.py` | 下载 2026-01 整月 × 850/500/200 三层位势高度 |
| `xarray_practice.py` | xarray 12 题，带自动判分（dim/coord、sel vs isel、切片、降维） |
| `day2_numpy_practice.py` | Day 2 NumPy 30 题，带自动判分（已全对） |
| `day3_pandas_practice.py` | Day 3 Pandas 30 题，带自动判分（已全对） |
| `day3_play.py` | Pandas 草稿本，打印每一步的返回类型与值 |
| `stations_obs.csv` | 练习数据：4 站点 2025 年 1–3 月逐日观测（含 -999 缺测） |
| `run.bat` | 双击即可用 ai-met 环境跑脚本，绕开 VS Code 解释器问题 |