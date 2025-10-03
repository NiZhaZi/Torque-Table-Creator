# RPM & Torque Table (Python GUI)

A lightweight cross-platform Tkinter app that generates a simple RPM–Torque table for an engine/motor based on a few inputs. It also shows the RPM at max power (`N`) and the horsepower equivalent of the provided max power. Results can be copied, or exported to CSV/JSON.

## Features

- Clean Tkinter GUI (no external GUI frameworks)
- Inputs:
  - **Max torque (Nm)**
  - **Max power (kW)**
  - **Max RPM**
  - **Torque decrease after N (%)** — applies beyond the RPM at max power
  - **RPM step**
- Outputs:
  - **N at max power (rpm)** = `9549 * P(kW) / T(Nm)`
  - **Max power (hp)** = `P(kW) * 1.341`
  - Table of `(rpm, torque)` pairs from `0` → `Max RPM` in `step` increments
- Export results to **CSV** or **JSON**
- **Copy table** to clipboard as a list of pairs
- Built-in internationalization (selectable in the UI): `en`, `es`, `fr`, `de`, `ja`

## How the model works (quick math)

- For `rpm < N`: torque is constant at **Max torque**.
- For `rpm >= N`: torque follows `T = (9549 * P / rpm) * (1 - decrease/100)`.
- `N = 9549 * P / T`, with `P` in kW and `T` in Nm.  
  The constant 9549 converts kW and Nm to RPM.

> This is a simple toy model meant for quick table generation and visualization—not a physical engine map.

---

## Requirements

- **Python 3.8+**
- Tkinter support:
  - Linux (Debian/Ubuntu): `sudo apt-get install python3-tk`
  - macOS: Official Python usually includes Tk; for Homebrew Python, install a Tk build that matches your Python.
  - Windows: Standard Python installer includes Tk by default.

Optional (for packaging to an executable):

- **CMake ≥ 3.20**
- **PyInstaller** (installed automatically by CMake build below)

---

## Running from source

```bash
python3 rpmtt_gui.py
```

If multiple Python versions are installed, explicitly use the one that has Tk support, e.g. `python` or `python3.11`.

---

## Building a standalone executable with CMake (PyInstaller)

This repository includes a `CMakeLists.txt` that calls PyInstaller to create a platform-specific bundle (Windows/Linux: single executable; macOS: `.app` bundle).

### Build

```bash
# Configure
cmake -S . -B build

# Build (this will install/upgrade PyInstaller automatically)
cmake --build build
```

### Output locations

- **Windows:** `build/pyinstaller/dist/rpmtt_gui.exe`
- **Linux:** `build/pyinstaller/dist/rpmtt_gui`
- **macOS:** `build/pyinstaller/dist/rpmtt_gui.app`

### (Optional) Install to a prefix

```bash
cmake --install build --prefix dist_install
```

### Customizing the bundle

- Add an app icon with PyInstaller flags (edit the command in `CMakeLists.txt`):
  - Windows: `--icon your.ico`
  - macOS: `--icon your.icns`
- To force a CLI single-file on macOS (instead of `.app`), remove `--windowed` (a terminal window will appear when running).

---

## Using the app

1. Select **Language**.
2. Enter:
   - **Max torque (Nm)** (must be `> 0`)
   - **Max power (kW)** (must be `> 0`)
   - **Max RPM** (must be `> 0`)
   - **Torque decrease after N (%)** (range `0–<100`)
   - **RPM step** (must be `> 0` and `<= Max RPM`)
3. Click **Calculate**.  
   The labels for **N at max power** and **Max power (hp)** update, and the table repopulates.
4. Use **Copy table**, **Export CSV**, or **Export JSON** as needed.
5. **Reset** restores sensible defaults.

---

## File formats

- **CSV:** Two columns: `rpm, torque(Nm)`
- **JSON:** Array of arrays: `[[rpm, torque], ...]`

---

## Troubleshooting

- **Tkinter not found / GUI won’t start**  
  Ensure `python3-tk` (Linux) or a Tk-enabled Python is installed.
- **Empty table / validation error**  
  Make sure all inputs are within the valid ranges listed above.
- **Fonts/controls look odd on Linux**  
  Install a modern theme or ensure you’re using a current Tk build.

---

## Acknowledgements

- Built with **Tkinter/ttk**.
- Packaging powered by **PyInstaller** through **CMake**.
