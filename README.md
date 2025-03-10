Microbiota7.py es el archivo principal que manda a llamar al resto de los archivos.
Este repositorio es un respaldo ya que desde aquí se puede hacer un ejecutable en python con la siguiente línea:

pyinstaller --onefile --icon=microbiota1.icns --add-data=1.-import_to_quiime.py:. --add-data=2.-Taxonomic.py:. --add-data=3.-Visualization.py:. --add-data=silva-138-99-nb-classifier.qza:. Microbiota7.py

El único detalle que tengo hasta el momento es que el "icono" no me cambia al que quiero.

Para instalar pyinstaller sería: pip install pyinstaller

Es necesario tener quiime2 instalado. El ejecutable te permite seleccionar la variable de entorno para activar el shell.
