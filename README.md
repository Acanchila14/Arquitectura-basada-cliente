# Arquitectura-basada-cliente

**SERVIDOR**
      
Este código es una aplicación web escrita en Python que utiliza el framework Flask para crear un servidor que maneja la carga, eliminación y listado de archivos. Vamos a desglosarlo y explicar su propósito, cómo funciona, y cómo podrías usarlo.

  **Descripción General:**
  
    Este código establece un servidor Flask que gestiona tres operaciones principales:
    

**Subir archivos:** *Permite que los usuarios suban archivos al servidor.*

**Eliminar archivos:** *Permite a los usuarios eliminar archivos que ya han subido.*

**Listar archivos**: *Muestra la lista de los archivos que se han subido al servidor.*


**Explicación de las secciones:**

   1. **Importaciones y configuración inicial:**


              from flask import Flask, request, jsonify
              import os
              
              app = Flask(__name__)
              UPLOAD_FOLDER = 'uploads'
              app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


   2. ***Creación de la carpeta de subidas:***

  
              if not os.path.exists(UPLOAD_FOLDER):
             os.makedirs(UPLOAD_FOLDER)


   3. **Eliminar un archivo:**


              @app.route('/delete/<filename>', methods=['DELETE'])
                  def delete_file(filename):
                      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                      if os.path.exists(file_path):
                          os.remove(file_path)
                          return jsonify({'message': 'Archivo eliminado correctamente.'}), 200
                      else:
                          return jsonify({'message': 'Archivo no encontrado.'}), 404

              
  4. **Subir un archivo:**


              @app.route('/upload', methods=['POST'])
                  def upload_file():
                      if 'file' not in request.files:
                          return 'No file part', 400
                      file = request.files['file']
                      if file.filename == '':
                          return 'No selected file', 400
                      file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                      return 'File uploaded successfully', 200


  5. **Listar los archivos subidos:**


             @app.route('/files', methods=['GET'])
                  def list_files():
                      files = os.listdir(app.config['UPLOAD_FOLDER'])
                      return jsonify(files), 200



 6. **Ejecutar la aplicación:**



              if __name__ == '__main__':
                app.run(debug=True)




**¿Para qué sirve?**


*Este servidor es útil si necesitas manejar archivos de manera remota. Puedes usarlo para*:


  - Subir archivos desde una interfaz de usuario.
    
  - Eliminar archivos que ya no son necesarios.
    
  - Obtener una lista de archivos disponibles en el servidor.



**CLIENTE (GUI)**

  *Este código es una aplicación GUI (Interfaz Gráfica de Usuario) desarrollada en Python utilizando Tkinter para interactuar con un servidor Flask. La aplicación permite al usuario subir, ver, abrir y eliminar archivos en un servidor remoto. Vamos a desglosarlo, entender su propósito y cómo puedes utilizarlo.*


**Descripción General:**


   La aplicación tiene las siguientes funcionalidades:
   

  *Subir archivos*: Permite al usuario seleccionar un archivo en su computadora y cargarlo en el servidor Flask.


  *Ver archivos cargados*: Lista todos los archivos que están almacenados en el servidor.


  *Abrir un archivo*: Abre un archivo seleccionado localmente.


  *Eliminar un archiv*o: Permite eliminar un archivo previamente cargado en el servidor.


  La interfaz gráfica es gestionada por Tkinter, y la comunicación con el servidor Flask se realiza utilizando la librería requests para hacer solicitudes HTTP.

**Explicación de las principales secciones del código:**


**1. Importaciones y configuración inicial:**


          import tkinter as tk
          from tkinter import filedialog, messagebox
          import requests
          import os
          import subprocess



**2. Función para cargar un archivo al servidor:**


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
    
              

**3. Función para ver los archivos cargados:**


                def view_uploaded_files():
    global selected_file
    try:
        response = requests.get(f"{SERVER_URL}/files")
        if response.status_code == 200:
            files = response.json()
            if files:
                for widget in files_frame.winfo_children():
                    widget.destroy()

                for file_name in files:
                    file_label = tk.Label(files_frame, text=file_name, anchor='w', cursor='hand2')
                    file_label.pack(fill='x', padx=10, pady=2)
                    file_label.bind("<Button-1>", lambda event, name=file_name: select_file(name))
            else:
                messagebox.showinfo("Archivos", "No hay archivos cargados.")
        else:
            messagebox.showerror("Error", "No se pudo obtener la lista de archivos.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener la lista de archivos: {e}")




**4. Seleccionar archivo:**



            def select_file(file_name):
            global selected_file
            selected_file = file_name
            messagebox.showinfo("Archivo Seleccionado", f"Seleccionaste: {selected_file}")



**5. Abrir archivo:**


                    def open_file():
            global selected_file
            if selected_file:
                file_path = os.path.join('uploads', selected_file)
                if os.path.isfile(file_path):
                    try:
                        if os.name == 'nt':
                            os.startfile(file_path)
                        elif os.name == 'posix':
                            subprocess.call(['open', file_path])
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")
                else:
                    messagebox.showerror("Error", "El archivo no existe.")
            else:
                messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")



**6. Eliminar archivo:**


            

                  def delete_file():
        global selected_file
        if selected_file:
            response = requests.delete(f"{SERVER_URL}/delete/{selected_file}")
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Archivo eliminado correctamente.")
                selected_file = None
                view_uploaded_files()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el archivo.")
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo.")



**7. Interfaz gráfica (Tkinter):**



            root = tk.Tk()
            root.title("Cargar Archivos")
            root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
            
            files_frame = tk.Frame(root)
            files_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            upload_button = tk.Button(root, text="Cargar Archivo", command=upload_file)
            upload_button.pack(pady=10)
            
            view_button = tk.Button(root, text="Ver Archivos Cargados", command=view_uploaded_files)
            view_button.pack(pady=10)
            
            open_button = tk.Button(root, text="Abrir Archivo Seleccionado", command=open_file)
            open_button.pack(pady=10)
            
            delete_button = tk.Button(root, text="Eliminar Archivo Seleccionado", command=delete_file)
            delete_button.pack(pady=10)
            
            root.mainloop()

                
