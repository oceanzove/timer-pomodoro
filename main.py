import tkinter
from tkinter import messagebox
import time
from threading import Thread


try:
    import winsound
    def play_sound():
        winsound.Beep(1000, 100)
except ImportError:
    import os
    def play_sound():
        os.system("afplay /System/Library/Sounds/Funk.aiff")


def create_gradient(canvas, width, height):
    gradient = ['#ffefef', '#ffc1c1', '#ff9999', '#ff7070', '#ff4747']
    for i, color in enumerate(gradient):
        canvas.create_rectangle(0,i*(height/len(gradient)), width, (i+1)*(height/len(gradient)), fill=color, outline=color)

def pomodoro_timer(work_time=25, short_break=5, long_break=15, cycles=4):
    # Этот вызов делает функцию play_sound доступной в основном потоке
    root.after(1, play_sound())
    for cycle in range(cycles):
        # Установка времени работы
        set_timer(work_time * 60, f"Работа: Цикл {cycle + 1}. Сосредоточьтесь!")
        # Который или длиный перерыв
        set_timer(long_break * 60 if cycle == cycles - 1 else short_break * 60, "Перерыв. Время отдохнуть!")
    messagebox.showinfo("Завершена", "Таймер закончил работу")

def set_timer(seconds, message):
    while seconds:
        minute, secs = divmod(seconds, 60)
        time_format = '{:02d}:{:02d}'.format(minute, secs)
        label.config(text=time_format)
        message_label.config(text=message)
        root.update_idletasks()
        time.sleep(1)
        seconds -= 1
    play_sound()

def start_thread():
    if not getattr(start_thread, 'running', False):
        start_thread.running = True
        t = Thread(target=pomodoro_timer)
        t.start()


root = tkinter.Tk()
root.title("Timer Pomodoro")

window_width = 350
window_height = 150
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

canvas = tkinter.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill='both', expand=True)
root.update_idletasks()
create_gradient(canvas, window_width, window_height)

label = tkinter.Label(root, text="00:00", font=("Helvetica", 48), bg='white', fg='black')
label.place(relx=0.5, rely=0.3, anchor='center')

message_label = tkinter.Label(root, text='', font=("Helvetica", 14), bg='white', fg='green')
message_label.place(relx=0.5, rely=0.5, anchor='center')

start_button = tkinter.Button(root, text="Start", command=start_thread)
start_button.place(relx=0.5, rely=0.7, anchor='center')


root.mainloop()

start_thread.running = False