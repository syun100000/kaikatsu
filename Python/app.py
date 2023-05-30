import tkinter as tk
from tkinter import ttk
__VERSION__ = "0.1"
class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("快活クラブ料金計算システム")

        # Create labels and entry fields for user input
        tk.Label(master, text="年齢:").grid(row=0, column=0)
        self.age_entry = tk.Entry(master)
        self.age_entry.grid(row=0, column=1)

        tk.Label(master, text="滞在時間（分）:").grid(row=1, column=0)
        self.duration_entry = tk.Entry(master)
        self.duration_entry.grid(row=1, column=1)

        tk.Label(master, text="入店時刻:").grid(row=2, column=0)
        self.checkin_time_entry = ttk.Combobox(master, values=[f"{i:02d}:00" for i in range(24)], width=8)
        self.checkin_time_entry.grid(row=2, column=1)

        tk.Label(master, text="30分料金:").grid(row=3, column=0)
        self.first_30min_fee_entry = tk.Entry(master)
        self.first_30min_fee_entry.grid(row=3, column=1)

        tk.Label(master, text="10分ごとの料金:").grid(row=4, column=0)
        self.every_10min_fee_entry = tk.Entry(master)
        self.every_10min_fee_entry.grid(row=4, column=1)

        tk.Label(master, text="3時間パック料金:").grid(row=5, column=0)
        self.pack_3hr_fee_entry = tk.Entry(master)
        self.pack_3hr_fee_entry.grid(row=5, column=1)

        tk.Label(master, text="6時間パック料金:").grid(row=6, column=0)
        self.pack_6hr_fee_entry = tk.Entry(master)
        self.pack_6hr_fee_entry.grid(row=6, column=1)

        tk.Label(master, text="9時間パック料金:").grid(row=7, column=0)
        self.pack_9hr_fee_entry = tk.Entry(master)
        self.pack_9hr_fee_entry.grid(row=7, column=1)

        tk.Label(master, text="12時間パック料金:").grid(row=8, column=0)
        self.pack_12hr_fee_entry = tk.Entry(master)
        self.pack_12hr_fee_entry.grid(row=8, column=1)

        tk.Label(master, text="15時間パック料金:").grid(row=9, column=0)
        self.pack_15hr_fee_entry = tk.Entry(master)
        self.pack_15hr_fee_entry.grid(row=9, column=1)

        tk.Label(master, text="18時間パック料金:").grid(row=10, column=0)
        self.pack_18hr_fee_entry = tk.Entry(master)
        self.pack_18hr_fee_entry.grid(row=10, column=1)

        tk.Label(master, text="21時間パック料金:").grid(row=11, column=0)
        self.pack_21hr_fee_entry = tk.Entry(master)
        self.pack_21hr_fee_entry.grid(row=11, column=1)

        tk.Label(master, text="24時間パック料金:").grid(row=12, column=0)
        self.pack_24hr_fee_entry = tk.Entry(master)
        self.pack_24hr_fee_entry.grid(row=12, column=1)

        tk.Label(master, text="ナイト8時間パック料金:").grid(row=13, column=0)
        self.night_8hr_fee_entry = tk.Entry(master)
        self.night_8hr_fee_entry.grid(row=13, column=1)

        self.student_discount_var = tk.BooleanVar()
        tk.Checkbutton(master, text="学生割引適用", variable=self.student_discount_var).grid(row=14, column=0)

        # Add button to calculate fee
        tk.Button(master, text="料金を計算", command=self.calculate_fee).grid(row=15, column=0, columnspan=2)

        # Add label to display calculated fee
        tk.Label(master, text="料金:").grid(row=16, column=0)
        self.fee_label = tk.Label(master, text="")
        self.fee_label.grid(row=16, column=1)

    def calculate_fee(self):
        age = int(self.age_entry.get())
        duration = int(self.duration_entry.get())
        checkin_time = self.checkin_time_entry.get()
        first_30min_fee = int(self.first_30min_fee_entry.get())
        every_10min_fee = int(self.every_10min_fee_entry.get())
        pack_fees = [
            int(self.pack_3hr_fee_entry.get()),
            int(self.pack_6hr_fee_entry.get()),
            int(self.pack_9hr_fee_entry.get()),
            int(self.pack_12hr_fee_entry.get()),
            int(self.pack_15hr_fee_entry.get()),
            int(self.pack_18hr_fee_entry.get()),
            int(self.pack_21hr_fee_entry.get()),
            int(self.pack_24hr_fee_entry.get())
        ]
        night_8hr_fee = int(self.night_8hr_fee_entry.get())
        student_discount = self.student_discount_var.get()

        fee = 0

        if age <= 12:
            fee = 0
        else:
            checkin_hour = int(checkin_time.split(':')[0])
            night_pack_available = checkin_hour >= 20 or checkin_hour < 4

            pack_index = duration // 180
            if pack_index > 7:
                pack_index = 7

            pack_fee = pack_fees[pack_index]

            if age >= 65:
                pack_fee = int(pack_fee * 0.9)
            elif student_discount:
                pack_fee = int(pack_fee * 0.8)

            regular_fee = first_30min_fee
            remaining_duration = duration - 30
            while remaining_duration > 0:
                regular_fee += every_10min_fee
                remaining_duration -= 10

            fee = min(pack_fee, regular_fee)

            if night_pack_available and duration <= 480:
                fee = min(fee, night_8hr_fee)

        self.fee_label.config(text=str(fee) + "円")

root = tk.Tk()
app = CalculatorGUI(root)
root.mainloop()
