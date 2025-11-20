# gui.py — запускай только этот файл
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import hashlib
from Hunter import PumpHunterCore

hunter = PumpHunterCore()
threading.Thread(target=hunter.run, daemon=True).start()

root = tk.Tk()
root.title("Pump Hunter Pro 2025")
root.geometry("1440x920")
root.minsize(1200, 700)
root.configure(bg="#0d1117")

# Стиль
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#161b22", foreground="#c9d1d9", fieldbackground="#161b22", rowheight=30, font=("Consolas", 11, "bold"))
style.configure("Treeview.Heading", background="#21262d", foreground="#58a6ff", font=("Segoe UI", 12, "bold"))
style.map("Treeview", background=[("selected", "#1f6feb")])

# Заголовок
header = tk.Frame(root, bg="#0d1117")
header.pack(fill="x", pady=(15,20), padx=25)

tk.Label(header, text="PUMP", font=("Impact", 42, "bold"), fg="#ff006e", bg="#0d1117").pack(side="left")
tk.Label(header, text="HUNTER", font=("Impact", 42, "bold"), fg="#58a6ff", bg="#0d1117").pack(side="left", padx=(0,10))
tk.Label(header, text="PRO 2025", font=("Arial Black", 18), fg="#8b949e", bg="#0d1117").pack(side="left", pady=10)

stats = tk.Frame(header, bg="#0d1117")
stats.pack(side="right")
tk.Label(stats, text="PUMPS:", font=("Arial", 18, "bold"), fg="#39ff14", bg="#0d1117").pack(side="left", padx=15)
lbl_pumps = tk.Label(stats, text="0", font=("Segoe UI", 40, "bold"), fg="#39ff14", bg="#0d1117")
lbl_pumps.pack(side="left")
tk.Label(stats, text="НОВЫЕ:", font=("Arial", 18, "bold"), fg="#ffeb3b", bg="#0d1117").pack(side="left", padx=(40,10))
lbl_new = tk.Label(stats, text="0", font=("Segoe UI", 40, "bold"), fg="#ffeb3b", bg="#0d1117")
lbl_new.pack(side="left")

# Поиск
search_fr = tk.Frame(root, bg="#0d1117")
search_fr.pack(fill="x", padx=25, pady=5)
tk.Label(search_fr, text="Поиск:", fg="#8b949e", bg="#0d1117").pack(side="left")
filter_var = tk.StringVar()
tk.Entry(search_fr, textvariable=filter_var, width=40, font=("Consolas", 13), bg="#21262d", fg="white", insertbackground="white").pack(side="left", padx=10, ipady=7)

# Таблица
tree = ttk.Treeview(root, columns=("coin","price","change","status"), show="headings")
tree.pack(fill="both", expand=True, padx=25, pady=10)

tree.heading("coin", text="ПАРА")
tree.heading("price", text="ЦЕНА")
tree.heading("change", text="1M %")
tree.heading("status", text="СТАТУС")
tree.column("coin", width=200, anchor="w")
tree.column("price", width=180, anchor="center")
tree.column("change", width=130, anchor="center")
tree.column("status", width=150, anchor="center")

tree.tag_configure("pump", background="#002200", foreground="#00ffaa")
tree.tag_configure("dump", background="#330011", foreground="#ff6b6b")

# Лог
log = scrolledtext.ScrolledText(root, height=11, bg="#000000", fg="#39ff14", font=("Consolas", 11))
log.pack(fill="x", padx=25, pady=(0,20))

# ← Переменные, которые раньше вызывали ошибку
displayed_alerts = set()
last_table_hash = ""

def update_gui():
    global last_table_hash

    while True:
        try:
            # Счётчики
            lbl_pumps.config(text=str(sum(1 for a in hunter.alerts if a["type"] == "PUMP")))
            lbl_new.config(text=str(len(hunter.new_listings)))

            # Таблица (обновляем только при реальном изменении)
            data = hunter.get_table_data()
            current_hash = hashlib.md5("".join(str(round(r[2], 3)) for r in data[:50]).encode()).hexdigest()
            if current_hash != last_table_hash:
                last_table_hash = current_hash
                filt = filter_var.get().lower()
                tree.delete(*tree.get_children())
                for sym, price, ch, status in data:
                    if filt and filt not in sym.lower(): continue
                    tag = "pump" if status == "PUMP" else "dump" if status == "DUMP" else ""
                    tree.insert("", "end", values=(sym, f"${price:,.2f}", f"{ch:+.2f}", status), tags=(tag,))

            # Лог алертов
            for alert in reversed(hunter.alerts):
                key = (alert["type"], alert["coin"], alert["time"])
                if key in displayed_alerts: continue
                displayed_alerts.add(key)

                color = {"PUMP": "#00ffaa", "DUMP": "#ff6b6b", "NEW": "#ffff66"}.get(alert["type"], "#ffffff")
                txt = f"[{alert['time']}] "
                if alert["type"] == "PUMP":
                    txt += f"PUMP {alert['coin']} +{alert['change']}% ×{alert['vol']}"
                elif alert["type"] == "DUMP":
                    txt += f"DUMP {alert['coin']} {alert['change']:+}%"
                else:
                    txt += f"НОВЫЙ ЛИСТИНГ → {alert['coin']}"
                log.insert("1.0", txt + "\n")
                log.see("1.0")

            if len(displayed_alerts) > 2000:
                displayed_alerts.clear()

        except Exception as e:
            print(f"[GUI] {e}")
        time.sleep(0.95)

threading.Thread(target=update_gui, daemon=True).start()
root.mainloop()