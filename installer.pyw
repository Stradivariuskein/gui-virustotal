import winreg
import tkinter as tk
from tkinter import filedialog
import os
import shutil
from tkinter import messagebox

def seleccionar_ruta():
    ruta = filedialog.askdirectory()
    ruta_text.set(ruta)

def instalar():
    ruta = ruta_text.get() 
    if ruta != "":

        ruta += "/scan_virusTotal"
        # Verifica si el directorio ya existe
        if not os.path.exists(ruta):
            # Crea el directorio
            try:
                os.mkdir(ruta)
                os.mkdir(ruta + "/img/")
            except Exception as e:
                messagebox.showerror("Error", e)
        elif not os.path.exists(ruta + "/img"):
            os.mkdir(ruta + "/img/")

        # Copiar cada archivo a la carpeta de destino
        #shutil.copy2("./send_request.py", ruta)
        try:
            shutil.copy2("./scan_virustotal.exe", ruta)
            archivos = os.listdir("./img")
            for imagen in archivos:
                shutil.copy2(f"./img/{imagen}", f"{ruta}/img/{imagen}")

        except Exception as e:
                messagebox.showerror("Error", f"No se puedo instalar\nIntente ejcuntado comeo eadministrador\n{e}")
        
        
        ruta = ruta.replace("/", "\\")

        try:
            clave_padre = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'*\shell', 0, winreg.KEY_WRITE)
            clave_name = winreg.CreateKey(clave_padre, 'Scan VirusTotal')

            # Asignar el valor en la clave del registro
            winreg.SetValueEx(clave_name, "icon", 0, winreg.REG_SZ ,f'{ruta}\\img\\tilde_azul.ico')
            winreg.SetValue(clave_name, 'command', winreg.REG_SZ, f'{ruta}\\scan_virustotal.exe "%V"')
        except Exception as e:
                messagebox.showerror("Error", f"Se instalo pero no se modifico el menu contectual\nIntente ejcuntado comeo eadministrador\n{e}")
            
        ventana.quit()
    else:
        seleccionar_ruta()

# Crear la ventana principal
ventana = tk.Tk()
ventana.iconbitmap("img/tilde_azul.ico")
ventana.title("Instalador")

# Variable de control para la ruta
ruta_text = tk.StringVar()

# Etiqueta y caja de texto para la ruta
etiqueta_ruta = tk.Label(ventana, text="Ruta de instalación:")
etiqueta_ruta.grid(row=0, column=0, padx=10, pady=10)

caja_ruta = tk.Entry(ventana, textvariable=ruta_text, width=50)
caja_ruta.grid(row=1, column=0, padx=10, pady=10)

# Botón para seleccionar ruta
boton_ruta = tk.Button(ventana, text="...", command=seleccionar_ruta)
boton_ruta.grid(row=1, column=1, padx=10, pady=10)

# Botón de instalación
boton_instalar = tk.Button(ventana, text="Instalar", command=instalar)
boton_instalar.grid(row=2, column=0, padx=10, pady=10)



# Iniciar el bucle de eventos
ventana.mainloop()


