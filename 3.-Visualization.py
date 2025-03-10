import os
import subprocess

# Obtener la ruta del escritorio
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Si el sistema está en español, verifica "Escritorio" en lugar de "Desktop"
if not os.path.exists(desktop_path):
    desktop_path = os.path.join(os.path.expanduser("~"), "Escritorio")

# Carpetas de entrada y salida
input_dir = os.path.join(desktop_path, "Taxonomic_results")
output_dir = os.path.join(desktop_path, "Visualization_files")

# Crear la carpeta de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Verificar si la carpeta de entrada existe
if not os.path.isdir(input_dir):
    print(f"❌ Error: La carpeta '{input_dir}' no existe.")
    exit(1)

# Iterar sobre todos los archivos .qza en el directorio de entrada
for filename in os.listdir(input_dir):
    if filename.endswith('.qza'):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, f'{filename[:-4]}_taxonomy.qzv')  # Sufijo _taxonomy

        # Verifica si el archivo de salida ya existe
        if os.path.exists(output_file_path):
            print(f"⚠️ El archivo {os.path.basename(output_file_path)} ya existe. Deteniendo el proceso.")
            exit(1)  # Detiene completamente el script

        # Comando para tabular los metadatos
        command = [
            'qiime', 'metadata', 'tabulate',
            '--m-input-file', input_file_path,
            '--o-visualization', output_file_path
        ]

        # Ejecutar el comando
        print(f'📊 Generando visualización para {filename}...')
        try:
            subprocess.run(command, check=True)
            print(f'✅ Visualización creada: {output_file_path}')
        except subprocess.CalledProcessError as e:
            print(f'❌ Error al generar visualización para {filename}: {e}')

print("✅ Proceso de visualización completado.")
