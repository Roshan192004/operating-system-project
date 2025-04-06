
import os
import time
import socket
import tkinter as tk
from tkinter import scrolledtext
from multiprocessing import Process, Queue, Pipe, Semaphore, shared_memory
from datetime import datetime

processes = []
# Global list to track running processes
processes = []

# Update output window
def update_output(output_widget, message):
    """Updates the GUI output area with timestamps."""
    timestamp = datetime.now().strftime("[%H:%M:%S] ")
    output_widget.insert("1.0", timestamp + message)
    output_widget.see("1.0")

# Clear output window
def clear_output(output_widget):
    """Clears the output log."""
    output_widget.delete(1.0, tk.END)

# Separate child function for multiprocessing
def child(pipe):
    """Child process sends data through pipe."""
    pid = os.getpid()
    pipe.send(f"Hello from child process {pid} through pipe")
    pipe.close()

# Monitor Pipes
def monitor_pipes(output_widget):
    """Monitors IPC using pipes."""
    parent_conn, child_conn = Pipe()

    proc = Process(target=child, args=(child_conn,))
    processes.append(proc)
    proc.start()
    proc.join()

    message = f"[PIPE] Received: {parent_conn.recv()}\n"
    update_output(output_widget, message)

# Monitor Shared Memory
def monitor_shared_memory(output_widget):
    """Monitors IPC using shared memory."""
    data = b"Shared Memory Data"
    shm = shared_memory.SharedMemory(create=True, size=len(data))  # Ensure correct size

    # Assign data to shared memory using memoryview
    memoryview(shm.buf)[:len(data)] = data

    message = f"[SHM] Written: {bytes(shm.buf[:len(data)]).decode()} (PID: {os.getpid()})\n"
    update_output(output_widget, message)

    # Clean up
    shm.close()
    shm.unlink()

# Monitor Semaphores
def monitor_semaphore(output_widget):
    """Monitors IPC using semaphores."""
    sem = Semaphore(1)

    sem.acquire()
    update_output(output_widget, f"[SEMAPHORE] Locked (PID: {os.getpid()})\n")

    time.sleep(1)
    sem.release()
    update_output(output_widget, f"[SEMAPHORE] Unlocked (PID: {os.getpid()})\n")

# Socket server process
def socket_server(queue, host, port):
    """Socket server process that sends messages to the queue."""
    pid = os.getpid()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()

        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024)
            queue.put(f"[SOCKET] Received: {data.decode()} (PID: {pid})\n")

# Socket client process
def socket_client(host, port):
    """Socket client sends a message."""
    pid = os.getpid()
    time.sleep(1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        client.sendall(f"Hello from socket client! (PID: {pid})".encode())

# Monitor sockets with queue
def monitor_sockets(output_widget):
    """Monitors IPC using sockets with a Queue."""
    host = '127.0.0.1'
    port = 65432

    queue = Queue()

    server_process = Process(target=socket_server, args=(queue, host, port))
    client_process = Process(target=socket_client, args=(host, port))

    processes.extend([server_process, client_process])

    server_process.start()
    client_process.start()
    def clear_output(output_widget):
           """Clears the output log."""
    output_widget.delete(1.0, tk.END)
    client_process.join()
    server_process.join()

    while not queue.empty():
        message = queue.get()
        
def stop_debugger(output_widget):
      """Stops all running IPC processes."""
      for proc in processes:
          if proc.is_alive():
              proc.terminate()
      update_output(output_widget, "\n[STOPPED] All IPC processes terminated.\n")
update_output(output_widget, message)

# Stop running processes
def stop_debugger(output_widget):
    """Stops all running IPC processes."""
    for proc in processes:
        if proc.is_alive():
            proc.terminate()
    update_output(output_widget, "\n[STOPPED] All IPC processes terminated.\n")

# Run the IPC Debugger
def run_debugger(output_widget):
    """Runs the entire IPC debugger."""
    clear_output(output_widget)
    update_output(output_widget, f"\n---- IPC Debugger (PID: {os.getpid()}) ----\n")
    monitor_pipes(output_widget)
    monitor_shared_memory(output_widget)
output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=20, font=("Courier", 10))
output_text.pack(pady=10)
   
clear_btn = tk.Button(app, text="Clear Log", command=lambda: clear_output(output_text), bg="red", fg="white",
                             font=("Helvetica", 12))
clear_btn.pack(pady=5)
   
       # "Run Debugger" button
btn = tk.Button(app, text="Run Debugger", command=lambda: run_debugger(output_text), bg="green", fg="white",
                       font=("Helvetica", 12))
btn.pack(pady=5)
monitor_semaphore(output_widget)
monitor_sockets(output_widget)
update_output(output_widget, "\nIPC Monitoring Completed!\n")

stop_btn = tk.Button(app, text="Stop Debugger", command=lambda: stop_debugger(output_text), bg="orange", fg="white", font=("Helvetica", 12))
stop_btn.pack(pady=5)
# GUI Setup
def setup_gui():
    """Creates the GUI window."""
    app = tk.Tk()
    app.title("IPC Debugger (Windows Compatible)")
    app.geometry("800x500")
from datetime import datetime
def update_output(output_widget, message):
      """Updates the GUI output area with timestamps."""
      timestamp = datetime.now().strftime("[%H:%M:%S] ")
      output_widget.insert(tk.END, timestamp + message)
      output_widget.see(tk.END)
output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=20, font=("Courier", 10))
output_text.pack(pady=10)

tk.Label(app, text="Inter-Process Communication (IPC) Debugger", font=("Helvetica", 16, "bold")).pack(pady=10)

run_btn = tk.Button(app, text="Run Debugger", command=lambda: run_debugger(output_text), bg="green", fg="white", font=("Helvetica", 12))
run_btn.pack(pady=5)

stop_btn = tk.Button(app, text="Stop Debugger", command=lambda: stop_debugger(output_text), bg="orange", fg="white", font=("Helvetica", 12))
stop_btn.pack(pady=5)

clear_btn = tk.Button(app, text="Clear Log", command=lambda: clear_output(output_text), bg="red", fg="white", font=("Helvetica", 12))
clear_btn.pack(pady=5)

app.mainloop()

# Main Execution
if __name__ == "__main__":
    setup_gui()