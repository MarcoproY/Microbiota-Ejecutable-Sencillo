import os
import subprocess

# Obtener la ruta del escritorio
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Si el sistema está en español, verifica "Escritorio" en lugar de "Desktop"
if not os.path.exists(desktop_path):
    desktop_path = os.path.join(os.path.expanduser("~"), "Escritorio")

# Carpetas de entrada y salida
input_dir = os.path.join(desktop_path, "Archivos_Qza")
output_dir = os.path.join(desktop_path, "Taxonomic_results")

# Ruta al clasificador
classifier_path = 'silva-138-99-nb-classifier.qza'

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
        output_file_path = os.path.join(output_dir, f'taxonomy_{filename}')

        # Verifica si el archivo de salida ya existe
        if os.path.exists(output_file_path):
            print(f"⚠️ El archivo {os.path.basename(output_file_path)} ya existe. Deteniendo el proceso.")
            exit(1)  # Detiene completamente el script

        # Comando de clasificación
        command = [
            'qiime', 'feature-classifier', 'classify-sklearn',
            '--i-classifier', classifier_path,
            '--i-reads', input_file_path,
            '--o-classification', output_file_path,
            '--p-reads-per-batch', '1000'
        ]

        # Ejecutar el comando
        print(f'🔍 Clasificando {filename}...')
        try:
            subprocess.run(command, check=True)
            print(f'✅ Clasificación completa: {filename}, resultado guardado en {output_file_path}.')
        except subprocess.CalledProcessError as e:
            print(f'❌ Error al clasificar {filename}: {e}')

print("✅ Proceso de clasificación completado.")
