import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Task list to hold all added tasks
tasks = []

# Define a function to add a task
def add_task(service_time, relative_deadline, period):
    try:
        service_time = int(service_time)
        relative_deadline = int(relative_deadline)
        period = int(period)
        task = {
            'service_time': service_time,
            'relative_deadline': relative_deadline,
            'period': period,
            'remaining_time': service_time,
            'next_deadline': relative_deadline,
            'arrival_time': 0
        }
        tasks.append(task)
        messagebox.showinfo("Success", f"Task added! Current total tasks: {len(tasks)}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integer values.")

# Define the EDF scheduling algorithm
def edf_schedule(tasks, total_time):
    schedule = []
    for t in range(total_time):
        ready_tasks = [task for task in tasks if t >= task['arrival_time'] and task['remaining_time'] > 0]
        if ready_tasks:
            ready_tasks.sort(key=lambda task: task['next_deadline'])
            task_to_run = ready_tasks[0]
            task_to_run['remaining_time'] -= 1
            schedule.append(f"J{tasks.index(task_to_run) + 1}")
            if task_to_run['remaining_time'] == 0:
                task_to_run['arrival_time'] += task_to_run['period']
                task_to_run['next_deadline'] += task_to_run['period']
                task_to_run['remaining_time'] = task_to_run['service_time']
        else:
            schedule.append("Idle")
    return schedule

# Plot the EDF schedule using Matplotlib
def plot_schedule(schedule, total_time):
    fig, ax = plt.subplots(figsize=(10, 4))
    time = range(total_time)
    ax.step(time, schedule, where='mid', label='Task Execution')
    ax.set_yticks([f"J{i}" for i in range(1, len(set(schedule)))] + ['Idle'])
    ax.set_xticks(range(0, total_time + 1, 1))
    ax.set_ylabel("Tasks")
    ax.set_xlabel("Time")
    ax.set_title("Earliest Deadline First Scheduling")
    plt.grid(True)
    plt.show()

# Define the function to run the scheduler and plot the result
def run_scheduler():
    if tasks:
        total_time = 20  # You can modify this based on user input for total time
        schedule = edf_schedule(tasks, total_time)
        plot_schedule(schedule, total_time)
    else:
        messagebox.showerror("No Tasks", "Please add tasks before running the scheduler.")

# GUI setup using Tkinter
root = tk.Tk()
root.title("EDF Scheduler")

# Input fields for service time, relative deadline, and period
tk.Label(root, text="Service Time").grid(row=0)
tk.Label(root, text="Relative Deadline").grid(row=1)
tk.Label(root, text="Period").grid(row=2)

service_time_entry = tk.Entry(root)
relative_deadline_entry = tk.Entry(root)
period_entry = tk.Entry(root)

service_time_entry.grid(row=0, column=1)
relative_deadline_entry.grid(row=1, column=1)
period_entry.grid(row=2, column=1)

# Add task button
tk.Button(root, text='Add Task', command=lambda: add_task(service_time_entry.get(), relative_deadline_entry.get(), period_entry.get())).grid(row=3, column=1, pady=4)

# Run scheduler button
tk.Button(root, text='Run Scheduler', command=run_scheduler).grid(row=4, column=1, pady=4)

root.mainloop()
