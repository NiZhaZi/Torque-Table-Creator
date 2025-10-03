#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, csv, math, platform

I18N = {
    "en": {
        "title": "RPM & Torque Table",
        "language": "Language",
        "torque": "Max torque (Nm)",
        "max_power": "Max power (kW)",
        "max_rpm": "Max RPM",
        "decrease": "Torque decrease after N (%)",
        "step": "RPM step",
        "calculate": "Calculate",
        "reset": "Reset",
        "copy": "Copy table",
        "export_csv": "Export CSV",
        "export_json": "Export JSON",
        "n_label": "N at max power (rpm)",
        "hp_label": "Max power (hp)",
        "table_header_rpm": "rpm",
        "table_header_torque": "torque (Nm)",
        "msg_invalid": "Please enter valid values",
        "msg_copied": "Table copied to clipboard",
        "save_dialog_csv": "Save CSV",
        "save_dialog_json": "Save JSON",
    },
    "zh-CN": {
        "title": "转速-扭矩表",
        "language": "语言",
        "torque": "最大扭矩 (牛米)",
        "max_power": "最大功率 (千瓦)",
        "max_rpm": "最大转速 (转/分)",
        "decrease": "N 之后扭矩衰减 (%)",
        "step": "转速步进",
        "calculate": "计算",
        "reset": "重置",
        "copy": "复制表格",
        "export_csv": "导出 CSV",
        "export_json": "导出 JSON",
        "n_label": "最大功率对应转速 N (rpm)",
        "hp_label": "最大功率对应马力 (hp)",
        "table_header_rpm": "转速 rpm",
        "table_header_torque": "扭矩 Nm",
        "msg_invalid": "请输入有效数值",
        "msg_copied": "表格已复制到剪贴板",
        "save_dialog_csv": "保存 CSV",
        "save_dialog_json": "保存 JSON",
    },
    "es": {
        "title": "Tabla de RPM y Par",
        "language": "Idioma",
        "torque": "Par máximo (Nm)",
        "max_power": "Potencia máxima (kW)",
        "max_rpm": "RPM máximas",
        "decrease": "Caída de par tras N (%)",
        "step": "Paso de RPM",
        "calculate": "Calcular",
        "reset": "Restablecer",
        "copy": "Copiar tabla",
        "export_csv": "Exportar CSV",
        "export_json": "Exportar JSON",
        "n_label": "N a potencia máxima (rpm)",
        "hp_label": "Potencia máxima (hp)",
        "table_header_rpm": "rpm",
        "table_header_torque": "par (Nm)",
        "msg_invalid": "Introduce valores válidos",
        "msg_copied": "Tabla copiada al portapapeles",
        "save_dialog_csv": "Guardar CSV",
        "save_dialog_json": "Guardar JSON",
    },
    "fr": {
        "title": "Table RPM & Couple",
        "language": "Langue",
        "torque": "Couple max (Nm)",
        "max_power": "Puissance max (kW)",
        "max_rpm": "Régime max (tr/min)",
        "decrease": "Baisse de couple après N (%)",
        "step": "Pas de régime",
        "calculate": "Calculer",
        "reset": "Réinitialiser",
        "copy": "Copier le tableau",
        "export_csv": "Exporter CSV",
        "export_json": "Exporter JSON",
        "n_label": "N à puissance max (tr/min)",
        "hp_label": "Puissance max (hp)",
        "table_header_rpm": "tr/min",
        "table_header_torque": "couple (Nm)",
        "msg_invalid": "Veuillez entrer des valeurs valides",
        "msg_copied": "Table copiée dans le presse-papiers",
        "save_dialog_csv": "Enregistrer CSV",
        "save_dialog_json": "Enregistrer JSON",
    },
    "de": {
        "title": "Drehzahl-Drehmoment-Tabelle",
        "language": "Sprache",
        "torque": "Max. Drehmoment (Nm)",
        "max_power": "Max. Leistung (kW)",
        "max_rpm": "Max. Drehzahl (rpm)",
        "decrease": "Drehmomentabfall nach N (%)",
        "step": "Drehzahlschritt",
        "calculate": "Berechnen",
        "reset": "Zurücksetzen",
        "copy": "Tabelle kopieren",
        "export_csv": "CSV exportieren",
        "export_json": "JSON exportieren",
        "n_label": "N bei Maximalleistung (rpm)",
        "hp_label": "Maximale Leistung (hp)",
        "table_header_rpm": "rpm",
        "table_header_torque": "Drehmoment (Nm)",
        "msg_invalid": "Bitte gültige Werte eingeben",
        "msg_copied": "Tabelle in die Zwischenablage kopiert",
        "save_dialog_csv": "CSV speichern",
        "save_dialog_json": "JSON speichern",
    },
    "ja": {
        "title": "回転数とトルクの表",
        "language": "言語",
        "torque": "最大トルク (Nm)",
        "max_power": "最大出力 (kW)",
        "max_rpm": "最大回転数 (rpm)",
        "decrease": "N以降のトルク低下率 (%)",
        "step": "回転数ステップ",
        "calculate": "計算",
        "reset": "リセット",
        "copy": "表をコピー",
        "export_csv": "CSV を出力",
        "export_json": "JSON を出力",
        "n_label": "最大出力時の回転数 N (rpm)",
        "hp_label": "最大出力の馬力 (hp)",
        "table_header_rpm": "rpm",
        "table_header_torque": "トルク (Nm)",
        "msg_invalid": "有効な数値を入力してください",
        "msg_copied": "表をクリップボードにコピーしました",
        "save_dialog_csv": "CSV を保存",
        "save_dialog_json": "JSON を保存",
    },
}

def compute_table(torque, max_power, max_rpm, decrease, step):
    N = 9549.0 * max_power / torque
    hp = max_power * 1.341
    rows = []
    rpm = 0
    while rpm <= max_rpm:
        if rpm >= N:
            base = 0.0 if rpm == 0 else (9549.0 * max_power) / rpm
            tq = base * (1.0 - decrease/100.0)
        else:
            tq = torque
        rows.append((rpm, tq))
        rpm += step
    return N, hp, rows

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.t = I18N[self.lang]
        self.title(self.t["title"])
        self.geometry("920x580")
        self._build_ui()
        self._compute()

    def _build_ui(self):
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")
        ttk.Label(top, text=self.t["language"]).pack(side="left")
        self.lang_var = tk.StringVar(value=self.lang)
        lang_menu = ttk.OptionMenu(top, self.lang_var, self.lang, *list(I18N.keys()), command=self._on_lang_change)
        lang_menu.pack(side="left", padx=6)

        frm = ttk.LabelFrame(self, text="", padding=8)
        frm.pack(fill="x", padx=8, pady=6)

        self.torque_var = tk.DoubleVar(value=150.0)
        self.power_var  = tk.DoubleVar(value=200.0)
        self.maxrpm_var = tk.IntVar(value=15000)
        self.dec_var    = tk.DoubleVar(value=5.0)
        self.step_var   = tk.IntVar(value=500)

        grid = ttk.Frame(frm)
        grid.pack(fill="x")

        def add_field(r, c, label, var, width=12):
            lab = ttk.Label(grid, text=label)
            ent = ttk.Entry(grid, textvariable=var, width=width)
            lab.grid(row=r, column=2*c, sticky="w", padx=4, pady=4)
            ent.grid(row=r, column=2*c+1, sticky="w", padx=4, pady=4)

        add_field(0,0,self.t["torque"], self.torque_var)
        add_field(0,1,self.t["max_power"], self.power_var)
        add_field(0,2,self.t["max_rpm"], self.maxrpm_var)
        add_field(0,3,self.t["decrease"], self.dec_var)
        add_field(0,4,self.t["step"], self.step_var)

        btns = ttk.Frame(frm)
        btns.pack(fill="x", pady=(6,0))
        ttk.Button(btns, text=self.t["calculate"], command=self._compute).pack(side="left")
        ttk.Button(btns, text=self.t["reset"], command=self._reset).pack(side="left", padx=6)
        ttk.Button(btns, text=self.t["copy"], command=self._copy).pack(side="left")
        ttk.Button(btns, text=self.t["export_csv"], command=self._export_csv).pack(side="left", padx=6)
        ttk.Button(btns, text=self.t["export_json"], command=self._export_json).pack(side="left")

        res = ttk.Frame(self, padding=(8,0))
        res.pack(fill="x")
        self.n_label = ttk.Label(res, text=f'{self.t["n_label"]}: —')
        self.n_label.pack(side="left", padx=(0,16))
        self.hp_label = ttk.Label(res, text=f'{self.t["hp_label"]}: —')
        self.hp_label.pack(side="left")

        tbl_frame = ttk.Frame(self, padding=8)
        tbl_frame.pack(fill="both", expand=True)
        columns = ("rpm", "torque")
        self.tree = ttk.Treeview(tbl_frame, columns=columns, show="headings", height=16)
        self.tree.heading("rpm", text=self.t["table_header_rpm"])
        self.tree.heading("torque", text=self.t["table_header_torque"])
        self.tree.column("rpm", width=120, anchor="e")
        self.tree.column("torque", width=160, anchor="e")
        vsb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="left", fill="y")

    def _on_lang_change(self, *_):
        self.lang = self.lang_var.get()
        self.t = I18N.get(self.lang, I18N["en"])
        self.title(self.t["title"])
        for child in self.winfo_children():
            child.destroy()
        self._build_ui()
        self._fill_table()

    def _validate(self):
        try:
            torque = float(self.torque_var.get())
            power  = float(self.power_var.get())
            maxrpm = int(self.maxrpm_var.get())
            dec    = float(self.dec_var.get())
            step   = int(self.step_var.get())
        except Exception:
            messagebox.showerror(title="Error", message=self.t["msg_invalid"])
            return None
        if not (torque>0 and power>0 and maxrpm>0 and step>0 and step<=maxrpm and 0<=dec<100):
            messagebox.showerror(title="Error", message=self.t["msg_invalid"])
            return None
        return torque, power, maxrpm, dec, step

    def _compute(self):
        vals = self._validate()
        if not vals:
            return
        torque, power, maxrpm, dec, step = vals
        self.N, self.hp, self.rows = compute_table(torque, power, maxrpm, dec, step)
        self._fill_table()

    def _fill_table(self):
        self.n_label.config(text=f'{self.t["n_label"]}: {int(round(self.N)) if hasattr(self, "N") else "—"}')
        self.hp_label.config(text=f'{self.t["hp_label"]}: {round(self.hp,2) if hasattr(self, "hp") else "—"}')
        for it in self.tree.get_children():
            self.tree.delete(it)
        if hasattr(self, "rows"):
            for rpm, tq in self.rows:
                self.tree.insert("", "end", values=(rpm, f"{tq:.2f}"))

    def _reset(self):
        self.torque_var.set(150.0)
        self.power_var.set(200.0)
        self.maxrpm_var.set(15000)
        self.dec_var.set(5.0)
        self.step_var.set(500)
        self._compute()

    def _copy(self):
        if not hasattr(self, "rows"):
            return
        s = "\n".join([f"[{rpm}, {tq:.2f}],"
                       for rpm, tq in self.rows])
        self.clipboard_clear()
        self.clipboard_append(s)
        self.update()
        messagebox.showinfo(title="", message=self.t["msg_copied"])

    def _export_csv(self):
        if not hasattr(self, "rows"):
            return
        fn = filedialog.asksaveasfilename(
            title=self.t["save_dialog_csv"],
            defaultextension=".csv",
            filetypes=[("CSV","*.csv"), ("All files","*.*")],
        )
        if not fn:
            return
        with open(fn, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([self.t["table_header_rpm"], self.t["table_header_torque"]])
            for rpm, tq in self.rows:
                w.writerow([rpm, f"{tq:.2f}"])

    def _export_json(self):
        if not hasattr(self, "rows"):
            return
        fn = filedialog.asksaveasfilename(
            title=self.t["save_dialog_json"],
            defaultextension=".json",
            filetypes=[("JSON","*.json"), ("All files","*.*")],
        )
        if not fn:
            return
        obj = {
            "N_rpm": int(round(self.N)),
            "hp": round(self.hp, 2),
            "table": [[rpm, float(f"{tq:.2f}")] for rpm, tq in self.rows],
        }
        with open(fn, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    App().mainloop()
