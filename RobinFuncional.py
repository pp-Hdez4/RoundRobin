import tkinter as tk
from tkinter import ttk
import threading
import time
from collections import deque

class Process:
    def __init__(self, pid, bt, art):
        self.pid = pid
        self.bt = bt
        self.art = art
        self.remaining_time = bt
        self.status = "Espera"

#función que se ejecuta en un hilo y actualiza el tiempo en segundos
def update_timer():
    global seg, min
    while timer_running:
        seg += 1
        if seg == 60:
            seg = 0
            min += 1
        update_gui()
        time.sleep(1)
#Actualiza el label con el tiempo
def update_gui():
    label5.config(text=f"{min:02d}:{seg:02d}")

def run_scheduler():
    global timer_running
    timer_running = True
    t = threading.Thread(target=update_timer)
    t.start()
    
#lista de 4 procesos 
    proc = [Process(1, 5, 1),
            Process(2, 4, 1),
            Process(3, 3, 2),
            Process(4, 6, 3)]
#wt, waiting time, tat time at turned
    n = len(proc)
    wt = [0] * n
    tat = [0] * n

    for i in range(n):
        wt[i] = 0

    complete = 0
    t = 0
    quantum = 1

    ready_queue = deque()
    running_process = None

    while complete != n:
        # Agregar procesos a la cola de listos que han llegado ready_queue
        for j in range(n):
            if proc[j].art <= t and proc[j].remaining_time > 0:
                ready_queue.append(j)

        if not ready_queue:
            t += 1
            continue

        # Obtener el próximo proceso en la cola de listos
        ejec = ready_queue.popleft()
        if proc[ejec].remaining_time > quantum:
            running_process = ejec  # Establecer el proceso en ejecución
            proc[ejec].status = "Ejecución"
            time.sleep(quantum)
            t += quantum
            proc[ejec].remaining_time -= quantum
            # Vuelve a agregar a la cola de listos
            ready_queue.append(ejec)  
        else:
            running_process = ejec  # Establecer el proceso en ejecución
            proc[ejec].status = "Ejecución"
            time.sleep(proc[ejec].remaining_time)
            t += proc[ejec].remaining_time
            proc[ejec].remaining_time = 0
            complete += 1
            finish_time = t
            wt[ejec] = finish_time - proc[ejec].bt - proc[ejec].art
            if wt[ejec] < 0:
                wt[ejec] = 0
            proc[ejec].status = "Terminado"
            running_process = None  # Limpiar el proceso en ejecución

        # Limpiar la cola de listos y volver a agregar todos los procesos
        ready_queue.clear()
        for j in range(n):
            if proc[j].art <= t and proc[j].remaining_time > 0:
                ready_queue.append(j)

        tree.delete(*tree.get_children())

        for i in range(n):
            tat[i] = proc[i].bt + wt[i]
            if proc[i].status == "Ejecución" and i == ejec:
                tree.insert("", tk.END, values=(proc[i].pid, proc[i].art, proc[i].bt, wt[i], tat[i]), tags=("red",))
            elif proc[i].status == "Ejecución":
                tree.insert("", tk.END, values=(proc[i].pid, proc[i].art, proc[i].bt, wt[i], tat[i]), tags=("lightblue",))
            elif proc[i].status == "Espera":
                tree.insert("", tk.END, values=(proc[i].pid, proc[i].art, proc[i].bt, wt[i], tat[i]), tags=("lightblue",))

        time.sleep(0.5)

    total = t

    for i in range(n):
        tat[i] = proc[i].bt + wt[i]
        children = tree.get_children()
        if i < len(children):
            tree.item(children[i], tags=("lightblue",))
            tree.set(children[i], column="Wait Time", value=wt[i])
            tree.set(children[i], column="Turnaround Time", value=tat[i])

    total_wt = sum(wt)
    total_tat = sum(tat)
    s = total_wt / n
    l = total_tat / n

    if seg == total - 1:
        timer_running = False
        label3.config(text=f"{s:.1f}")
        label4.config(text=f"{l:.1f}")

seg, min = 0, 0
timer_running = False

root = tk.Tk()
root.title("Planificador JSF")

frame = ttk.Frame(root)
frame.pack()

label5 = ttk.Label(frame, text="00:00")
label5.pack()

button1 = ttk.Button(frame, text="Iniciar", command=lambda: threading.Thread(target=run_scheduler).start())
button1.pack()

tree = ttk.Treeview(frame, columns=("Process ID", "Arrival Time", "Burst Time", "Wait Time", "Turnaround Time"))
tree.heading("#1", text="Process ID")
tree.heading("#2", text="Arrival Time")
tree.heading("#3", text="Burst Time")
tree.heading("#4", text="Wait Time")
tree.heading("#5", text="Turnaround Time")

tree.pack()

tree.tag_configure("red", background="red")
tree.tag_configure("lightblue", background="lightblue")

label3 = ttk.Label(frame, text="")
label4 = ttk.Label(frame, text="")
label3.pack()
label4.pack()

root.mainloop()
