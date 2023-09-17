import threading
from tkinter import Tk, Label, Button, LEFT, Scrollbar, PhotoImage
from tkinter.ttk import Treeview
from ttkthemes import ThemedStyle
from send_request import send_request_file
from PIL.ImageTk import PhotoImage
from PIL import Image, ImageTk
from sys import argv
from time import sleep

stop_scan = False
msj = ""

def agregar_fila(anti_virus, scan, result):
        # Cambiar el estilo de la fila a "rojo" si es un resultado positivo
        #fila_id = tabla.insert("", "end", values=(anti_virus, "", result))
        if scan:
            tabla.insert('', 'end', text="Fila 1", values=(anti_virus, img_cruz, result))
            tabla.image_references.append(img_cruz)

           
        else:
            fila_id = tabla.insert("", "end", values=(anti_virus, "", result))


def salir():
    ventana.quit()

def show_result(response):
    
    if response["positive_relevant"]:
        msj = "Alguno de los antivirus mas relevantes lo detectaron como virus"
        name_img = "Red-Cros.gif"
    elif response["positives"] == 0: 
        msj = "Ningun antivirus lo detecta como virus"
        name_img = "tilde_verde.gif"
    elif response["positives"] <= 5:
        msj = f"{response['positives']} de {response['total']} antivirus lo detectan como virus. Bajas probavilidas de ser un virus aun algunos antivirus lo detectan como virus"
        name_img = "cartel_amarillo.gif"
    else:
        msj = f"{response['positives']} de {response['total']} antivirus lo detectan como virus, aunque los principales antivirus no lo detecta como virus"
        name_img = "cartel_amarillo.gif"
    return [msj, name_img]

 # Configurar el ancho máximo dinámicamente
def ajustar_ancho_max(event):
        ancho_ventana = event.width
        ancho_max = min(ancho_ventana - 20, 286)  # Ajusta el ancho máximo según tus necesidades
        label.configure(wraplength=ancho_max)


def rotar_imagen_grados(imagen, grados):
    # Rotar la imagen en grados
    return imagen.rotate(grados)

def actualizar_imagen():
    global angle_cricle, imagen_rotada, img_circle


    # Rotar la imagen en la iteración actual
    imagen_rotada = rotar_imagen_grados(img_circle, -angle_cricle * 30)  # Rotar 30 grados por iteración
    imagen_tk = ImageTk.PhotoImage(imagen_rotada)

    # Actualizar la imagen en el label
    label.config(image=imagen_tk)
    label.image = imagen_tk

    angle_cricle = (angle_cricle + 1) % 12  # Rotar 30 grados en cada iteración (12 iteraciones para un giro completo)


# Función para actualizar el texto en la etiqueta
def actualizar_texto():
    global i
    dots = "." * i
    label.config(text="Escaneando archivo" + dots)
    
    i = (i + 1) % 4  # Para repetir la secuencia después de 3 iteraciones

# cada 1 segundo actualiza el texto y cada 0.1 segundo rota la imagen
def loop_scan():
    global stop_scan, msj, label, i
    i = 0
    
    ms_sleep = 0.1
    count_seg = 0
    while not stop_scan:
        if count_seg >= 1:
            actualizar_texto()
            count_seg = 0
        else:
            count_seg += ms_sleep

        actualizar_imagen()
        ventana.update()

        sleep(ms_sleep)


def scan_file(archivo): # es solo para poder ejecutarlo en un hilo
    global msj, name_img, stop_scan, response
    response = send_request_file(archivo)
    if response:
        lista = show_result(response)
        msj = lista[0]
        name_img = lista[1]
    else:
        msj = "Error con el servicdor"
        name_img = "Red-Cros.gif"
    stop_scan = True


if __name__ == "__main__":

    ruta_imagen = "./img/circulo.png"

    ruta_ejecucion = argv[0]
    fin_ruta = ruta_ejecucion[::-1].find("\\")
    ruta_ejecucion = ruta_ejecucion[:-fin_ruta]

    # Crear la ventana
    ventana = Tk()
    ventana.iconbitmap(f"{ruta_ejecucion}/img/tilde_azul.ico")
    ventana.title("Analisis virus-total")
    ventana.geometry("250x100")
    img_cruz = Image.open("img/Red-Cros.gif")
    img_tilde = Image.open("img/tilde_verde.gif")



    # Obtener el argumento proporcionado
    try:
        archivo = argv[1]
    except:
        #archivo = "virus2.py"
        archivo = None
        msj = "Ejecute desde consola:\n scan_virustotal.exe 'ruta/del/archivo'"
        img_cruz = img_cruz.resize((25, 25))
        img_cruz = PhotoImage(img_cruz)
        label = Label(ventana, image=img_cruz, compound=LEFT, text=msj, wraplength=200)
        label.grid(row=0, column=0, padx=10, pady=10)

    if archivo:
        # Cargar la imagen y ajustar su tamaño si es necesario
        img_circle = Image.open(ruta_imagen)
        img_circle = img_circle.resize((25, 25), Image.ANTIALIAS)
    


        # Redimensiona la imagen a 12x12 píxeles
        img_cruz = img_cruz.resize((12, 12))
        img_tilde = img_tilde.resize((12, 12))
        img_cruz = PhotoImage(img_cruz)
        img_tilde = PhotoImage(img_tilde)

        msj = "Escaneando archivo..."
        
        # Crear el Label para mostrar el mensaje de escaneo
        imagen_tk = ImageTk.PhotoImage(img_circle)
        label = Label(ventana, compound=LEFT, text=msj, wraplength=200)
        label.grid(row=0, column=0, padx=10, pady=10)
        # Iniciar la rotación de la imagen
        angle_cricle = 0
        actualizar_imagen()

        ventana.columnconfigure(0, weight=1)
        ventana.grid_columnconfigure(0, weight=1)

        response = None

        try:
            hilo = threading.Thread(target=scan_file, args= (archivo,))
            hilo.start()

            loop_scan()
            ventana.geometry("400x400")
                
        except Exception as e:
            msj = f"Erro con la peticion\n{e}"
            name_img = "Red-Cros.gif"




        # Cargar la imagen PNG y convertirla a formato GIF
        icono_tilde = PhotoImage(file=f"{ruta_ejecucion}/img/{name_img}")

        # Crear el cuadro de texto
        #cuadro_texto = tk.Label(ventana, compound=tk.LEFT, image=icono_tilde, text=msj)
        label.config(image=icono_tilde,  text=msj, wraplength=200)

    

        if response:
            # Asociar el evento de cambio de tamaño de la ventana al ajuste del ancho máximo
            ventana.bind("<Configure>", ajustar_ancho_max)
            label.grid(row=0, column=0, padx=10, pady=10)

            # Crear la tabla
            columnas = ("Anti virus", "Virus", "Description")
            tabla = Treeview(ventana, columns=columnas, show="headings")
            # Configurar estilo para filas con resultado positivo
            tabla.tag_configure("rojo", background="#FA5858")

            # Configurar el estilo de la tabla utilizando ttkthemes
            estilo = ThemedStyle(ventana)
            estilo.set_theme("clam")  # Puedes elegir otro tema si lo deseas
            estilo.configure("Treeview", background="#FFFFFF")  # Color de fondo del Treeview
            estilo.configure("Treeview.Heading", background="#E0E0E0")  # Color de fondo de las cabeceras
            estilo.configure("Treeview.Row", background="#FA5858")  # Color de fondo de las filas con resultado positivo



            # Alinear el texto al centro
            tabla.column(columnas[0], anchor="center")
            tabla.column(columnas[1], anchor="center")
            tabla.column(columnas[2], anchor="center")

            # Configurar el ancho de las columnas
            tabla.column(columnas[0], width=100)
            tabla.column(columnas[1], width=50)
            tabla.column(columnas[2], width=200)
            #scroll bar
            scrollbar = Scrollbar(ventana, orient="vertical", command=tabla.yview)
            tabla.configure(yscrollcommand=scrollbar.set)

            for col in columnas:
                tabla.heading(col, text=col)

            for key, value in response["positives_sacans"].items():
                agregar_fila(key,value['detected'], value['result'])

            for key, value in response["relevant_scans"].items():
                agregar_fila(key,value['detected'], value['result'])
            for key, value in response["others_scans"].items():
                agregar_fila(key,value['detected'], value['result'])
            tabla.grid(row=1, column=0, padx=10, pady=10)
            scrollbar.grid(row=1, column=1, sticky="ns")


    # Agregar botón para agregar filas
    boton_agregar = Button(ventana, text="Aceptar", command=salir)
    boton_agregar.grid(row=2, column=0, padx=10, pady=10)

    label.grid(row=0, column=0, padx=10, pady=10)
    ventana.update_idletasks()

    # Iniciar el bucle principal de la ventana
    ventana.mainloop()





