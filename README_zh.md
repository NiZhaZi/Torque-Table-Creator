# RPM 与扭矩表（Python 图形界面）

一个轻量、跨平台的 Tkinter 应用，根据少量输入生成简化的 **RPM–扭矩** 对照表。应用会计算 **最大功率对应的转速 N**，并显示最大功率对应的 **马力值（hp）**。结果可复制，或导出为 CSV/JSON。

## 功能特点

- 纯 Tkinter/ttk 图形界面（无需额外 GUI 框架）
- 输入项：
  - **最大扭矩（Nm）**
  - **最大功率（kW）**
  - **最大转速（RPM）**
  - **超过 N 后的扭矩下降幅度（%）** —— 作用于“最大功率转速 N”之后的区间
  - **转速步进（RPM step）**
- 输出项：
  - **最大功率转速 N（rpm）** = `9549 * P(kW) / T(Nm)`
  - **最大功率马力（hp）** = `P(kW) * 1.341`
  - 从 `0` 到 `最大转速` 按 `步进` 生成 `(rpm, torque)` 列表
- 结果可导出为 **CSV** 或 **JSON**
- 一键 **复制表格**（以成对数值的形式）
- 内置多语言（界面可选）：`en`、`es`、`fr`、`de`、`ja`

## 模型原理（快速说明）

- 当 `rpm < N`：扭矩恒为 **最大扭矩**。
- 当 `rpm >= N`：扭矩计算为 `T = (9549 * P / rpm) * (1 - decrease/100)`。
- `N = 9549 * P / T`，其中 `P` 单位为 kW，`T` 单位为 Nm。  
  常数 **9549** 用于 kW 与 Nm 到 RPM 的换算。

> 该模型仅用于快速生成表格与可视化，属于简化的“玩具模型”，并非真实的发动机特性图。

---

## 运行依赖

- **Python 3.8+**
- Tkinter 支持：
  - Linux（Debian/Ubuntu）：`sudo apt-get install python3-tk`
  - macOS：官方 Python 通常已包含 Tk；若使用 Homebrew Python，请安装与之匹配的 Tk 版本。
  - Windows：标准 Python 安装程序默认包含 Tk。

可选（用于打包为独立可执行文件）：

- **CMake ≥ 3.20**
- **PyInstaller**（下述 CMake 构建会自动安装/升级）

---

## 源码运行

```bash
python3 rpmtt_gui.py
```

如果系统内存在多个 Python 版本，请显式选择包含 Tk 支持的版本，例如 `python` 或 `python3.11`。

---

## 使用 CMake（PyInstaller）打包独立可执行文件

仓库包含的 `CMakeLists.txt` 会调用 PyInstaller 生成平台专属的分发包（Windows/Linux：单一可执行文件；macOS：`.app` 包）。

### 构建

```bash
# 配置
cmake -S . -B build

# 构建（会自动安装/升级 PyInstaller）
cmake --build build
```

### 产物位置

- **Windows：** `build/pyinstaller/dist/rpmtt_gui.exe`
- **Linux：** `build/pyinstaller/dist/rpmtt_gui`
- **macOS：** `build/pyinstaller/dist/rpmtt_gui.app`

### （可选）安装到指定前缀

```bash
cmake --install build --prefix dist_install
```

### 自定义打包

- 在 `CMakeLists.txt` 中为 PyInstaller 添加图标参数：
  - Windows：`--icon your.ico`
  - macOS：`--icon your.icns`
- 若希望在 macOS 上强制产出“单文件 CLI 可执行”（而非 `.app`），可移除 `--windowed`（运行时会弹出终端窗口）。

---

## 使用步骤

1. 选择 **语言**。
2. 填写：
   - **最大扭矩（Nm）**（必须 `> 0`）
   - **最大功率（kW）**（必须 `> 0`）
   - **最大转速（RPM）**（必须 `> 0`）
   - **超过 N 后的扭矩下降幅度（%）**（范围 `0–<100`）
   - **转速步进（RPM step）**（必须 `> 0` 且 `<= 最大转速`）
3. 点击 **Calculate**。  
   界面会更新 **最大功率转速 N** 与 **最大功率（hp）**，并重新生成表格。
4. 视需要使用 **Copy table**、**Export CSV** 或 **Export JSON**。
5. 点击 **Reset** 恢复默认值。

---

## 文件格式

- **CSV：** 两列：`rpm, torque(Nm)`
- **JSON：** 数组的数组：`[[rpm, torque], ...]`

---

## 故障排查

- **提示找不到 Tkinter / 无法启动 GUI**  
  请确认系统已安装 `python3-tk`（Linux）或使用了带 Tk 的 Python 版本。
- **表格为空 / 校验错误**  
  请检查所有输入是否落在上述有效范围。
- **Linux 上字体/控件显示异常**  
  建议安装现代主题或确认 Tk 版本较新。

---

## 致谢

- 基于 **Tkinter/ttk** 构建。
- 通过 **CMake** 调用 **PyInstaller** 完成打包。
