import os
import subprocess

# Ruta completa de la carpeta 'Fasta_Files' en el escritorio
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Si el sistema está en español, verifica "Escritorio" en lugar de "Desktop"
if not os.path.exists(desktop_path):
    desktop_path = os.path.join(os.path.expanduser("~"), "Escritorio")

# Carpeta de entrada con archivos .fasta
input_folder = os.path.join(desktop_path, "Fasta_Files")

# Carpeta de salida para los archivos .qza en el escritorio
output_folder = os.path.join(desktop_path, "Archivos_Qza")

# Crear la carpeta de salida si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Verifica si la carpeta de entrada existe
if not os.path.isdir(input_folder):
    print(f"❌ Error: La carpeta '{input_folder}' no existe.")
    exit(1)

# Recorre todos los archivos en la carpeta de entrada
for filename in os.listdir(input_folder):
    if filename.endswith(".fasta"):
        fasta_path = os.path.join(input_folder, filename)
        qza_path = os.path.join(output_folder, filename.replace(".fasta", ".qza"))

        # Verifica si el archivo de salida ya existe
        if os.path.exists(qza_path):
            print(f"⚠️ El archivo {os.path.basename(qza_path)} ya existe. Deteniendo el proceso.")
            exit(1)  # Detiene completamente el script

        # Comando para importar a QIIME 2
        command = [
            "qiime", "tools", "import",
            "--type", "FeatureData[Sequence]",
            "--input-path", fasta_path,
            "--output-path", qza_path
        ]

        # Ejecuta el comando en la terminal
        try:
            subprocess.run(command, check=True)
            print(f"✅ Importado: {filename} -> {os.path.basename(qza_path)}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al importar {filename}: {e}")

print("✅ Proceso completado. Los archivos .qza están en la carpeta 'Archivos_Qza'.")
