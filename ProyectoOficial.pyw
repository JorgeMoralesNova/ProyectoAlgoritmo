import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

ventana_principal = Tk()
ventana_principal.title("Ruta de Buses")

img = Image.open("barca.png")
photo = ImageTk.PhotoImage(img)

ventana_principal.iconphoto(False, photo)
ventana_principal.config(bg="#CDE941", cursor="spider")

marco_botones = Frame(ventana_principal, bg="#CDE941")
marco_botones.pack()

global num_registros
global desde
global hasta

def confirmar_Salidas(ventana):
    if messagebox.askyesno("Salir", "¿Estás seguro que deseas salir???"
                                    ""):
        ventana.destroy()

def opcionBuses(bus):
    try:
        conexion = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="",
                                           database="proyecto_algoritmo")

        cursor = conexion.cursor()



        textC = "select descripcion from hoja1 where bus = '" + bus + "'"
        cursor.execute(textC)
        ruta = str(cursor.fetchone())
        text = "el " + bus.replace("_", " ") + " pasa por las siguientes direcciones:\n\n" + ruta.upper()
        messagebox.showinfo("Rutas", text)

    except:
        print(
            "Hay un fallo con el servidor o no está en marcha, una posible solución es desde xamp iniciar(start) en  MySQL por medio de Xampp")


#funcionalidad botones
def opcion(value):
    try:
        conexion = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="",
                                           database="proyecto_algoritmo")

        cursor = conexion.cursor()


        conexion_empresas = mysql.connector.connect(host="localhost",
                                                    user="root",
                                                    passwd="",
                                                    database="proyecto_algoritmo_empresas")

        cursor_empresas = conexion_empresas.cursor()

        cursor_empresas.execute("SELECT COUNT(*) FROM hoja1")
        num_registros = int(cursor_empresas.fetchone()[0])  # cuantos registros hay

    except:
        print("hay un problema con el servidor")


    ventana = Toplevel(ventana_principal, bg="#A7ECB7", cursor="target")
    ventana.iconphoto(False, photo)
    marco = Frame(ventana, bg="#BB9BC4")

    for i in range(num_registros):
        i=i+1

        if value==i:
            cursor_empresas.execute("select LIMITE from  `hoja1` where ID="+ str(i))
            limite=int(cursor_empresas.fetchone()[0])
            if value==1:
                desde=0
                hasta=limite
            else:
                cursor_empresas.execute("select LIMITE from  `hoja1` where ID="+ str(i-1))
                desde=int(cursor_empresas.fetchone()[0])
                hasta=limite

            break

    for i in range(desde, hasta):
        i=i+1

        valuen = str(i)
        cursor.execute("SELECT BUS FROM `hoja1` WHERE ID=" + valuen)
        bus = str(cursor.fetchone()[0])
        bus_nombre = bus.replace(" ", "_").replace(",", "").replace("'", "").lower()

        boton = Button(marco,bg="#8CD852", borderwidth=7, relief="groove",text=bus_nombre.lower().replace("_", " "), command=lambda nombre=bus_nombre: opcionBuses(nombre)).pack()  # si se hace directamente sin la variable nombre, sobreescribe y siempre pasa por parametros el último

    marco.pack()
    boton_salir = Button(ventana, text="Salir", command=lambda: confirmar_Salidas(ventana), bg="red")
    boton_salir.pack()

    ventana.resizable(width=False, height=False)
    ventana.protocol("WM_DELETE_WINDOW", lambda: confirmar_Salidas(ventana))


try:
    conexion_empresas = mysql.connector.connect(host="localhost",
                                                    user="root",
                                                    passwd="",
                                                    database="proyecto_algoritmo_empresas")

    cursor_empresas = conexion_empresas.cursor()
    cursor_empresas.execute("SELECT COUNT(*) FROM hoja1")
    num_registros = int(cursor_empresas.fetchone()[0])  # cuantos registros hay

except: print("hay un problema con el servidor")

empresas = []

# Recorrer los egistros de la consulta y agregarlos a la lista
for i in range(num_registros):

    texto=("SELECT EMPRESA FROM `hoja1` WHERE id ="+ str(i+1))
    cursor_empresas.execute(texto)
    resultado = str(cursor_empresas.fetchone()[0]).upper()
    empresas.append(resultado)

num_filas = 0
num_columnas = 0

for n, empresa in enumerate(empresas):
    if n % 4 == 0:
        num_filas += 1
        num_columnas = 0
    boton = Button(marco_botones, text=empresa, command=lambda value=n + 1: opcion(value), bg="#CCFFFF", borderwidth=7, relief="groove")
    boton.grid(row=num_filas, column=num_columnas, padx=5, pady=5)
    num_columnas += 1

#.................................Boton_busqueda..................................
marco_buscar=Frame(ventana_principal, bg="#CDE941")

#textoBuscar=StringVar()
#..............................................................
def buscar_autobuses():

    direccion_origen = entrada_origen.get()
    direccion_destino = entrada_destino.get()

    cursor.execute("SELECT * FROM hoja1 WHERE descripcion LIKE %s AND descripcion LIKE %s", ('%' + direccion_origen + '%', '%' + direccion_destino + '%'))

    resultados = cursor.fetchall()

    # Comprueba si se encontraron resultados:
    if len(resultados) > 0:

        cadena_resultados = f"Estos autobuses le sirven para ir desde {direccion_origen} hasta {direccion_destino}:\n\n"
        for resultado in resultados:
            cadena_resultados += f"Nombre:\n{resultado[1]}\n\n\nRuta:\n\n {resultado[2]}\n\n"


        messagebox.showinfo("Resultados", cadena_resultados)
    else:

        messagebox.showinfo("Resultados", f"No se encontraron autobuses que conecten {direccion_origen} y {direccion_destino}")


conex = mysql.connector.connect(host="localhost", user="root", passwd="", database="proyecto_algoritmo")

cursor = conex.cursor()


color="#CCFFFF"

label_origen = Label(marco_buscar, text="Dirección de origen:", bg=color)
label_origen.grid(row=0, column=0, padx=10, pady=10)

entrada_origen = Entry(marco_buscar, bg=color)
entrada_origen.grid(row=0, column=1, padx=10, pady=10)

label_destino = Label(marco_buscar, text="Dirección de destino:", bg=color)
label_destino.grid(row=1, column=0, padx=10, pady=10)

entrada_destino = Entry(marco_buscar, bg=color)
entrada_destino.grid(row=1, column=1, padx=10, pady=10)

boton_buscar = Button(marco_buscar, text="Buscar", command=buscar_autobuses, bg=color)
boton_buscar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

marco_buscar.pack()

boton_salir = Button(ventana_principal, text="Salir", command=lambda: confirmar_Salidas(ventana_principal), bg="red")

des = "Esta aplicación, desarrollada en Python con la biblioteca Tkinter,te permite visualizar información actualizada sobre las rutas de autobuses de varias empresas.\n\nLa aplicación se conecta a una base de datos MySQL local para obtener esta información."\
      +"\nPara utilizar la aplicación, simplemente ingresa la dirección de origen y destino de tu viaje y la aplicación te mostrará los autobuses disponibles que cubren esa ruta.\n\nCon esta herramienta, podrás planificar mejor tus viajes y estar informado sobre las opciones de transporte disponibles en tu zona."\
      +"\n\nCabe destacar que, aunque la aplicación está diseñada para mostrar información sobre rutas de autobuses, su estructura y funcionalidad la hacen fácilmente adaptable para mostrar otros tipos de información relacionada con el transporte o cualquier otra temática que se desee.\n\n¡Explora y experimenta con ella!"
boton_creditos = Button(ventana_principal, text="Acerca de",
                        command=lambda: messagebox.showinfo("Acerca de ", des + "\n\n\nCreditos a: ""\nHabit Enrrique Cabrera Arzuza\nDiego Tamara Rodelo\nJulio Orrego Villareal\nJorge de Jesús Morales Nova"),  bg="#6484DA").pack()
boton_salir.pack()

ventana_principal.resizable(width=False, height=False)
ventana_principal.protocol("WM_DELETE_WINDOW", lambda ventana=ventana_principal: confirmar_Salidas(ventana))

ventana_principal.mainloop()

print("\n\n--Se ha cerrado el programa con exito  :)")
