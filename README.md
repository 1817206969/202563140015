# AI 气象学习记录 · ly

南京信息工程大学 · 大气科学 · 大二

方向：AI 气象（数据驱动天气预报与气候预测）。目标是一年内具备进组干活的
能力，同时打竞赛出成果。

## 这周要做的

- 搭好 Python 环境（conda + xarray + cartopy + PyTorch）
- 打通 ERA5 数据下载到出图的完整链路
- 养成每天提交一次的习惯

## 进度

- **2026-09-16**：环境配好（conda 环境 `ai-met`，Python 3.11）；首次提交；
  ERA5 第一份数据下载成功（2026-01-01 东亚 2m 温度）并出图
- **2026-09-17**：Day 2 NumPy 练习 30/30（轴、广播、布尔索引、缺测）；
  Day 3 Pandas 练习开工（`day3_pandas_practice.py` + 站点观测数据
  `stations_obs.csv`，4 站 × 90 天 × 360 行）

## 目录说明

| 文件 | 内容 |
|---|---|
| `AI气象学习路线-ly.md` | 一年的主线规划、子方向、竞赛与进组清单 |
| `第1周任务卡-9.17至9.22.md` | 逐日任务、网课资源、避坑 |
| `era5_first_look.py` | ERA5 下载 + 出图脚本（第一个可复现的东西） |
| `era5_first_figure.png` | 第一张真实数据图 |
| `day2_numpy_practice.py` | Day 2 NumPy 30 题，带自动判分（已全对） |
| `day3_pandas_practice.py` | Day 3 Pandas 30 题，带自动判分 |
| `stations_obs.csv` | 练习数据：4 站点 2025 年 1–3 月逐日观测（含 -999 缺测） |
| `run.bat` | 双击即可用 ai-met 环境跑脚本，绕开 VS Code 解释器问题 |
