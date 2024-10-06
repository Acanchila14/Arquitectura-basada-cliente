import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os
import subprocess

# URL del servidor Flask
SERVER_URL = "http://127.0.0.1:5000"

# Variable para almacenar el archivo seleccionado
selected_file = None

# Función para cargar un archivo al servidor

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            with open(file_path, 'rb') as file:
                response = requests.post(f"{SERVER_URL}/upload", files={'file': file})
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
            else:
                messagebox.showerror("Error", "Error al cargar el archivo.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

# Función para ver los archivos cargados
def view_uploaded_files():
    global selected_file  # Usar la variable global para almacenar el archivo seleccionado
    try:
        response = requests.get(f"{SERVER_URL}/files")
        if response.status_code == 200:
            files = response.json()  # Esperamos recibir un JSON con la lista de archivos
            if files:
                # Limpiar la lista de archivos antes de mostrar los nuevos
                for widget in files_frame.winfo_children():
                    widget.destroy()

                # Mostrar los archivos en el frame
                for file_name in files:
                    file_label = tk.Label(files_frame, text=file_name, anchor='w', cursor='hand2')
                    file_label.pack(fill='x', padx=10, pady=2)

                    # Configurar la etiqueta para seleccionar el archivo al hacer clic
                    file_label.bind("<Button-1>", lambda event, name=file_name: select_file(name))
            else:
                messagebox.showinfo("Archivos", "No hay archivos cargados.")
        else:
            messagebox.showerror("Error", "No se pudo obtener la lista de archivos.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la lista de archivos: {e}")

# Función para seleccionar un archivo
def select_file(file_name):
    global selected_file
    selected_file = file_name
    messagebox.showinfo("Archivo Seleccionado", f"Seleccionaste: {selected_file}")

# Función para abrir el archivo
def open_file():
    global selected_file
    if selected_file:
        file_path = os.path.join('uploads', selected_file)  # Ruta del archivo en la carpeta de uploads
        if os.path.isfile(file_path):  # Verificar que el archivo existe
            try:
                # Abrir el archivo con el programa predeterminado
                if os.name == 'nt':  # Para Windows
                    os.startfile(file_path)
                elif os.name == 'posix':  # Para MacOS o Linux
                    subprocess.call(['open', file_path])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")
        else:
            messagebox.showerror("Error", "El archivo no existe.")
    else:
        messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")

# Función para eliminar un archivo
def delete_file():
    global selected_file
    if selected_file:
        response = requests.delete(f"{SERVER_URL}/delete/{selected_file}")
        if response.status_code == 200:
            messagebox.showinfo("Éxito", "Archivo eliminado correctamente.")
            selected_file = None  # Reiniciar la variable después de eliminar
            view_uploaded_files()  # Actualizar la lista de archivos
        else:
            messagebox.showerror("Error", "No se pudo eliminar el archivo.")
    else:
        messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")

# Crear la ventana principal de la GUI
root = tk.Tk()
root.title("Cargar Archivos")

# Obtener la resolución de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Centrar la ventana en la pantalla
window_width = 600
window_height = 400
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Frame para contener los archivos cargados
files_frame = tk.Frame(root)
files_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Botón para cargar archivo
upload_button = tk.Button(root, text="Cargar Archivo", command=upload_file)
upload_button.pack(pady=10)

# Botón para ver archivos cargados
view_button = tk.Button(root, text="Ver Archivos Cargados", command=view_uploaded_files)
view_button.pack(pady=10)

# Botón para abrir el archivo seleccionado
open_button = tk.Button(root, text="Abrir Archivo Seleccionado", command=open_file)
open_button.pack(pady=10)

# Botón para eliminar archivo
delete_button = tk.Button(root, text="Eliminar Archivo Seleccionado", command=delete_file)
delete_button.pack(pady=10)

# Ejecutar la ventana principal
root.mainloop()
