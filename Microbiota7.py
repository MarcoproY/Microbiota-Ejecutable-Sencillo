import tkinter as tk
from tkinter import *
import os
import sys
import threading
import subprocess
from tkinter import scrolledtext

# Bandera para controlar el paro
stop_flag = False
qiime2_env = None  # Variable global para almacenar el entorno seleccionado

def get_qiime2_envs():
    """Obtiene los entornos de Conda y filtra los que contienen 'qiime2'."""
    try:
        result = subprocess.run("conda env list", shell=True, capture_output=True, text=True)
        env_lines = result.stdout.splitlines()
        qiime_envs = [line.split()[0] for line in env_lines if "qiime2" in line]
        return qiime_envs
    except Exception as e:
        salida_texto.insert(tk.END, f"❌ Error al obtener entornos: {e}\n")
        return []

def select_qiime2_env():
    """Abre una ventana emergente para seleccionar un entorno Qiime2."""
    global qiime2_env
    env_list = get_qiime2_envs()

    if not env_list:
        salida_texto.insert(tk.END, "❌ No se encontraron entornos de Qiime2.\n")
        return

    def set_env():
        global qiime2_env
        qiime2_env = env_var.get()
        salida_texto.insert(tk.END, f"✅ Entorno seleccionado: {qiime2_env}\n")
        top.destroy()

    top = Toplevel()
    top.title("Seleccionar entorno Qiime2")
    top.geometry("300x150")

    Label(top, text="Seleccione un entorno Qiime2:", font=("Arial", 10, "bold")).pack(pady=10)

    env_var = StringVar(top)
    env_var.set(env_list[0])  # Valor por defecto

    dropdown = OptionMenu(top, env_var, *env_list)
    dropdown.pack(pady=10)

    Button(top, text="Seleccionar", command=set_env).pack(pady=10)

    top.resizable(False, False)

def activate_selected_env():
    """Activa el entorno Qiime2 seleccionado."""
    global qiime2_env
    if not qiime2_env:
        salida_texto.insert(tk.END, "❌ No se ha seleccionado un entorno Qiime2.\n")
        return

    salida_texto.insert(tk.END, f"🔹 Activando entorno: {qiime2_env}...\n")
    salida_texto.update()

    salida_texto.insert(tk.END, f"✅ Entorno {qiime2_env} activado.\n")

def initiate_download():
    """Descarga archivos .fasta y los guarda en el escritorio en la carpeta Fasta_Files."""
    global stop_flag
    stop_flag = False
    srr_err = opcion.get()
    start_srr = int(e1.get())
    end_srr = int(e2.get())

    # Ruta del escritorio
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    fasta_dir = os.path.join(desktop_path, "Fasta_Files")

    os.makedirs(fasta_dir, exist_ok=True)

    if srr_err == 1:
        id_list = [f"SRR{num}" for num in range(start_srr, end_srr + 1)]
    else:
        id_list = [f"ERR{num}" for num in range(start_srr, end_srr + 1)]

    for seq_id in id_list:
        if stop_flag:
            break
        
        fasta_file = os.path.join(fasta_dir, f"{seq_id}.fasta")
        
        if os.path.exists(fasta_file):
            salida_texto.insert(tk.END, f"⚠️ {seq_id} ya existe, omitiendo descarga.")
            salida_texto.update()
            continue

        try:
            salida_texto.insert(tk.END, f"📥 Descargando {seq_id}...")
            salida_texto.update()
            subprocess.run(["prefetch", seq_id], check=True)
            subprocess.run(["fastq-dump", "--fasta", "--outdir", fasta_dir, seq_id], check=True)
            salida_texto.insert(tk.END, f"✅ {seq_id} procesado y guardado en {fasta_dir}.")
        except subprocess.CalledProcessError as e:
            salida_texto.insert(tk.END, f"❌ Error al procesar {seq_id}: {e}")

    salida_texto.insert(tk.END, "✅ Todas las descargas han finalizado correctamente.")
    salida_texto.update()


def create_env4():
    """Ejecuta los scripts dentro del entorno seleccionado de Qiime2."""
    global stop_flag, qiime2_env
    if not qiime2_env:
        salida_texto.insert(tk.END, "❌ No se ha seleccionado un entorno Qiime2.\n")
        return

    # Ruta del directorio donde están los scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Obtener las rutas absolutas de los scripts
    scripts = [
        os.path.join(script_dir, "1.-import_to_quiime.py"),
        os.path.join(script_dir, "2.-Taxonomic.py"),
        os.path.join(script_dir, "3.-Visualization.py")
    ]

    for script in scripts:
        if stop_flag:
            break
        comando = f"conda run -n {qiime2_env} python {script}"
        salida_texto.insert(tk.END, f"🚀 Ejecutando {script}...\n")
        salida_texto.update()
        resultado_script = subprocess.run(comando, shell=True, capture_output=True, text=True)

        if resultado_script.stdout:
            salida_texto.insert(tk.END, f"✅ Salida de {script}:\n{resultado_script.stdout}\n")
        else:
            salida_texto.insert(tk.END, f"❌ Error al ejecutar {script}:\n{resultado_script.stderr}\n")

    salida_texto.insert(tk.END, "✅ Todos los scripts de Qiime2 se han ejecutado correctamente.\n")
    salida_texto.update()

def stop_process():
    """Detiene los procesos en ejecución."""
    global stop_flag
    stop_flag = True
    salida_texto.insert(tk.END, "⛔ Proceso detenido.\n")
    salida_texto.update()

def start_download_thread():
    threading.Thread(target=initiate_download, daemon=True).start()

def start_taxonomic_analysis_thread():
    threading.Thread(target=create_env4, daemon=True).start()

# Interfaz gráfica
master = tk.Tk()
master.title("Download SRR & ERR Data from NCBI")

# Paso 1 - Frame
frame1 = Frame(master, padx=10, pady=10)
frame1.grid(row=0, column=0, columnspan=4, pady=10)

tk.Label(frame1, text="Paso 1: Select SRR or ERR").grid(row=0, column=0, columnspan=2)
tk.Label(frame1, text="Initial ID: ").grid(row=1, column=0)
tk.Label(frame1, text="Final ID: ").grid(row=2, column=0)

e1 = tk.Entry(frame1)
e2 = tk.Entry(frame1)
e1.grid(row=1, column=1)
e2.grid(row=2, column=1)

opcion = IntVar(value=1)
tk.Radiobutton(frame1, text='SRR', variable=opcion, value=1).grid(row=1, column=2, sticky=tk.W, pady=4)
tk.Radiobutton(frame1, text='ERR', variable=opcion, value=2).grid(row=2, column=2, sticky=tk.W, pady=4)

# Paso 2 - Frame
frame2 = Frame(master, padx=10, pady=10)
frame2.grid(row=1, column=0, columnspan=4, pady=10)

tk.Label(frame2, text="Paso 2: Select and Activate Qiime2 Environment").grid(row=0, column=0, columnspan=2)
tk.Button(frame2, text='1.- Select Qiime2 Env', command=select_qiime2_env).grid(row=1, column=0, pady=4)
tk.Button(frame2, text='2.- Activate Selected Env', command=activate_selected_env).grid(row=1, column=1, pady=4)

# Paso 3 - Frame
frame3 = Frame(master, padx=10, pady=10)
frame3.grid(row=2, column=0, columnspan=4, pady=10)

tk.Label(frame3, text="Paso 3: Start Processes").grid(row=0, column=0, columnspan=4)
tk.Button(frame3, text='Initiate Download', command=start_download_thread).grid(row=1, column=0, pady=4)
tk.Button(frame3, text='Taxonomic Analysis', command=start_taxonomic_analysis_thread).grid(row=1, column=1, pady=4)
tk.Button(frame3, text='Stop Process', command=stop_process).grid(row=1, column=2, pady=4)
tk.Button(frame3, text='Close App', command=master.quit).grid(row=1, column=3, pady=4)

# Salida de texto
salida_texto = scrolledtext.ScrolledText(master, width=80, height=20)
salida_texto.grid(row=3, column=0, columnspan=4, pady=10)

master.mainloop()
