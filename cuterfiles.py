import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# Abrir archivo
def select_file():
    Tk().withdraw()  # Oculta la ventana principal de Tkinter
    archivo_seleccionado = askopenfilename(
        title="Seleccione un archivo .xlsx, .csv, .json o .parquet",
        filetypes=[("Archivos Excel", "*.xlsx"), ("Archivos Json", "*.json"),
                   ("Archivos Parquet", "*.parquet"), ("Archivos CSV", "*.csv")]
    )
    if archivo_seleccionado:
        print(f"Archivo seleccionado: {archivo_seleccionado}")
    else:
        raise ValueError("No se seleccionó ningún archivo.")
    return archivo_seleccionado


# Cargar el archivo Excel o CSV
def load_file(ruta_archivo):
    extension = os.path.splitext(ruta_archivo)[1]  # Obtener la extensión del archivo
    if extension == '.xlsx':
        return pd.read_excel(ruta_archivo)
    elif extension == '.csv':
        return pd.read_csv(ruta_archivo)
    elif extension == '.json':
        return pd.read_json(ruta_archivo)  # Carga un archivo JSON
    elif extension == '.parquet':
        return pd.read_parquet(ruta_archivo, engine='auto')  # Carga un archivo Parquet
    else:
        raise ValueError("El archivo debe ser .xlsx, .csv, .json o .parquet")


# Contar filas y dividir en paquetes
def cut_save(df, filas_por_paquete, carpeta_salida, formato_salida='xlsx'):
    os.makedirs(carpeta_salida, exist_ok=True)  # Crear la carpeta de salida si no existe
    total_filas = len(df)

    # Dividir el DataFrame en partes de 'filas_por_paquete' filas
    for i, inicio in enumerate(range(0, total_filas, filas_por_paquete)):
        fin = min(inicio + filas_por_paquete, total_filas)
        paquete = df.iloc[inicio:fin]

        # Crear el nombre del archivo basado en el formato de salida
        if formato_salida == 'xlsx':
            nombre_archivo = os.path.join(carpeta_salida, f"paquete_{i:04}.xlsx")
            paquete.to_excel(nombre_archivo, index=False)
        elif formato_salida == 'csv':
            nombre_archivo = os.path.join(carpeta_salida, f"paquete_{i:04}.csv")
            paquete.to_csv(nombre_archivo, index=False)
        elif formato_salida == 'json':
            nombre_archivo = os.path.join(carpeta_salida, f"paquete_{i:04}.json")
            paquete.to_json(nombre_archivo, orient='records', lines=True)
        elif formato_salida == 'parquet':
            nombre_archivo = os.path.join(carpeta_salida, f"paquete_{i:04}.parquet")
            paquete.to_parquet(nombre_archivo, index=False)
        else:
            raise ValueError("Formato de salida no soportado")

        print(f"Archivo guardado: {nombre_archivo} - Filas {inicio + 1} a {fin}")


# Uso del script
def main():
    try:
        # Inputs del usuario
        ruta_archivo = select_file()
        print("=========Bienvenidos a CutterFile's by RacoonRoach=========")
        carpeta_salida = input("Introduce la carpeta donde almacenar los paquetes: ")
        filas_por_paquete = int(input("Introduce la cantidad de filas por paquete: "))
        formato_salida = input("Introduce el formato de salida (xlsx, csv, json, parquet): ").strip().lower()

        # Validar formato de salida
        if formato_salida not in {'xlsx', 'csv', 'json', 'parquet'}:
            raise ValueError("El formato de salida debe ser uno de: xlsx, csv, json, parquet")

        # Cargar archivo y dividir en paquetes
        df = load_file(ruta_archivo)
        cut_save(df, filas_por_paquete, carpeta_salida, formato_salida)
        print("El proceso se completó exitosamente. Los paquetes se guardaron en la carpeta:", carpeta_salida)

    except Exception as e:
        print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    main()
