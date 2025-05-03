import tkinter as tk
from datetime import datetime, timedelta
import winsound  # Для Windows (если Linux/Mac, можно использовать 'playsound'


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер с обратным отсчётом")
        self.root.configure(bg="#87CEEB")  # Голубой фон

        self.is_running = False
        self.remaining_time = timedelta()

        # Поля для ввода минут и секунд
        self.minutes_var = tk.StringVar(value="0")
        self.seconds_var = tk.StringVar(value="10")  # По умолчанию 10 секунд

        tk.Label(root, text="Минуты:", bg="#87CEEB", fg="white", font=("Arial", 12)).pack()
        tk.Entry(root, textvariable=self.minutes_var, font=("Arial", 12), justify="center").pack()

        tk.Label(root, text="Секунды:", bg="#87CEEB", fg="white", font=("Arial", 12)).pack()
        tk.Entry(root, textvariable=self.seconds_var, font=("Arial", 12), justify="center").pack()

        # Время на таймере
        self.time_var = tk.StringVar()
        self.time_var.set("00:00")

        self.label = tk.Label(
            root, textvariable=self.time_var,
            font=("Arial", 48), bg="#87CEEB", fg="white"
        )
        self.label.pack(pady=20)

        # Кнопки
        button_style = {
            "font": ("Arial", 14),
            "bg": "#4682B4",
            "fg": "white",
            "activebackground": "#5F9EA0",
            "relief": tk.RAISED,
            "borderwidth": 3
        }

        self.start_button = tk.Button(root, text="Старт", command=self.start_timer, **button_style)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.stop_button = tk.Button(root, text="Стоп", command=self.stop_timer, **button_style)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.reset_button = tk.Button(root, text="Сброс", command=self.reset_timer, **button_style)
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=5)

    def start_timer(self):
        if not self.is_running:
            try:
                minutes = int(self.minutes_var.get())
                seconds = int(self.seconds_var.get())
                if minutes < 0 or seconds < 0:
                    raise ValueError("Время не может быть отрицательным")
                self.remaining_time = timedelta(minutes=minutes, seconds=seconds)
                self.is_running = True
                self.update_timer()
            except ValueError:
                self.time_var.set("Ошибка!")

    def stop_timer(self):
        self.is_running = False

    def reset_timer(self):
        self.is_running = False
        self.time_var.set("00:00")

    def update_timer(self):
        if self.is_running and self.remaining_time.total_seconds() > 0:
            mins, secs = divmod(int(self.remaining_time.total_seconds()), 60)
            self.time_var.set(f"{mins:02d}:{secs:02d}")
            self.remaining_time -= timedelta(seconds=1)
            self.root.after(1000, self.update_timer)
        elif self.is_running:
            self.is_running = False
            self.time_var.set("00:00")
            self.play_alarm()  # Звуковое оповещение

    def play_alarm(self):
        # Проигрываем звук (Windows)
        winsound.Beep(1000, 2000)  # Частота 1000 Гц, длительность 2000 мс
        # Для Linux/Mac можно использовать 'playsound':
        # from playsound import playsound
        # playsound("alarm.mp3")


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()