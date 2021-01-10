from tkinter import *
import tkinter as tk
import mariadb
import time
import sys
import os

class Sistema(tk.Toplevel):
    def __init__(self, parent, nombre, numero, empleadoid):
        super().__init__(parent)
        #Parametros para crear la ventana
        self.title("Sistema de apoyo")
        self.geometry("1000x530+0+0")
        self.protocol("WM_DELETE_WINDOW", self.volver)
        self.parent=parent

        #Variables recibidas a instanciar (para que se pueda ver nombre, numero y id de empleado en la ventana)
        self.nombre=tk.StringVar()
        self.numero=tk.StringVar()
        self.id=tk.StringVar()
        self.nombre.set(nombre)
        self.numero.set(numero)
        self.id.set(empleadoid)

        #Declaracion de variables para capturar el resultado de cada Entry
        self.codigo=StringVar()
        self.version=StringVar()
        self.familia=StringVar()
        self.orden=StringVar()
        self.partes=StringVar()
        self.partesrechazadas=StringVar()
        self.partesaceptadas=StringVar()
        self.ruta=StringVar()
        self.parte=StringVar()
        self.diagramaid=StringVar()
        self.tiempo = StringVar()
        self.text=StringVar()

        #Se asigna el texto que se mostrara en  el boton
        self.text.set("Mostrar diagrama")
        self.bandera=0

        #Declaracion de variables globales para los controles tipo Entry
        global entrada_codigo
        global entrada_orden
        global entrada_partes
        global entrada_partesrechazadas
        global entrada_partesaceptadas

        #Se conecta a la base de datos
        try:
                self.conn = mariadb.connect(
                    user="admin",
                    password="1309",
                    host="localhost",
                    port=3306,
                    database="Visuales"

                )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cur = self.conn.cursor()

        #Creacion de los controladores que estaran presentes en la ventana
        self.label_timestamp=Label(self, textvariable=self.tiempo, font=("Calibri", 15))
        self.label_timestamp.pack()
        self.update_time()

        self.label_nombre=Label(self, textvariable=self.nombre, font=("Calibri", 18))
        self.label_nombre.place(x=0,y=0)
        
        Label(self, text="Orden", font=("Calibri", 15)).place(x=160,y=405)
        entrada_orden=Entry(self, textvariable=self.orden, font=("Calibri", 15))
        entrada_orden.place(x=90,y=430)
        
        Label(self, text="Partes requeridas", font=("Calibri", 15)).place(x=120,y=465)
        entrada_partes=Entry(self, textvariable=self.partes, font=("Calibri", 15))
        entrada_partes.place(x=90,y=490)
        
        Label(self, text="Partes aceptadas", font=("Calibri", 15)).place(x=730,y=405)
        entrada_partesaceptadas=Entry(self, textvariable=self.partesaceptadas, font=("Calibri", 15))
        entrada_partesaceptadas.place(x=700,y=430)
        
        Label(self, text="Partes rechazadas", font=("Calibri", 15)).place(x=725,y=465)
        entrada_partesrechazadas=Entry(self, textvariable=self.partesrechazadas, font=("Calibri", 15))
        entrada_partesrechazadas.place(x=700,y=490)
        
        self.label_numero=Label(self, textvariable=self.numero, font=("Calibri", 15))
        self.label_numero.place(x=0,y=25)
        
        self.label_familia=Label(self, textvariable=self.familia, font=("Calibri", 15))
        self.label_familia.place(x=160,y=25)
        
        self.label_version=Label(self, textvariable=self.version, font=("Calibri", 15))
        self.label_version.place(x=450,y=25)
        
        self.label_parte=Label(self, textvariable=self.parte, font=("Calibri", 15))
        self.label_parte.place(x=600,y=25)
        
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
        Label(self, text="").pack()
  
        
        Label(self, text="Escanee codigo", font=("Calibri", 15)).pack()
        entrada_codigo=Entry(self, textvariable=self.codigo, font=("Calibri", 15))
        entrada_codigo.pack()
        entrada_codigo.focus()
        Label(self, text="").pack()
        Button(self, textvariable=self.text, bg="LightGreen", command=self.diagrama, font=("Calibri", 15)).pack()
        Button(self, text="Cerrar sesion", bg="SteelBlue1", command=self.volver, font=("Calibri", 15)).place(relx=0.85, rely=0.02)
        
        self.parent.withdraw()
    
    #Metodo para volver a la ventana principal
    def volver(self):
        self.parent.deiconify()
        self.destroy()
        #Se cierra la conexion a la base de datos
        self.conn.close()
    
    #Metodo que mantiene actualizando el tiempo que se muestra en la ventana    
    def update_time(self):
        #Se toma el tiempo local
        self.ts = time.localtime()
        #Se le da formato, Horas:Minutos:Segundos dia/mes/año
        self.readable = time.strftime("%H:%M:%S %d/%m/%Y",self.ts)
        #Se le asigna a la variable ligada al label
        self.tiempo.set(self.readable)
        #Se llama a si mismo cada segundo
        self.label_timestamp.after(1000, self.update_time)
    
    #Metodo para consultar diagramas y update de la tabla Log
    def diagrama(self):
        #Si bandera igual a 0
        if self.bandera == 0:
            #Se crea controlador donde se mostrara imagen
            self.mostrar_imagen=Label()
            #Se crea variable tipo PhotoImage
            self.imagen=PhotoImage()
            #Se limpia la imagen
            self.mostrar_imagen.config(image='')
            #Se limpian las variables
            self.familia.set(f"")
            self.version.set(f"")
            self.parte.set(f"")
            
            self.contador=0
            
            #Se busca el diagrama por el numero de parte (codigo de barras)
            self.cur.execute("SELECT DiagramaID, RutaImagen, Familia, Version, NumeroParte FROM Diagrama WHERE NumeroParte=?",(self.codigo.get(), ))
            #Si encuentra el diagrama guarda su ruta y suma el contador
            for DiagramaID, RutaImagen, Familia, Version, NumeroParte in self.cur:
                self.ruta=RutaImagen
                self.contador=self.contador+1
            #Si el contador es mayor o igual a 1
            if self.contador>=1:
                #Variables usadas para mostrarlas en la ventana
                #Se asigna el id del diagrama consultado
                self.diagramaid.set(DiagramaID)
                #Se asigna la familia del diagrama consultado
                self.familia.set(f"Familia: {Familia}")
                #Se asigna la version del diagrama consultado
                self.version.set(f"Version: {Version}")
                #Se asigna el numero de parte del diagrama consultado
                self.parte.set(f"Numero de parte: {NumeroParte}")
                try:
                    #Se le asigna a la variable imagen la ruta de la imagen consultada
                    self.imagen.config(file=self.ruta)
                    #Se asigna la imagen que se mostrara en el label
                    self.mostrar_imagen=Label(self, image=self.imagen).place(relx=0.5, rely=0.42, anchor=CENTER)
                    #Se cambia el texto de Mostrar Diagrama a Terminar Orden
                    self.text.set("Terminar orden")
                    self.bandera=1
                    #Se deshabilita la opcion de volver a consultar diagrama hasta que se termine con la orden
                    entrada_codigo.config(state='disabled')
                #Mensaje si la ruta de imagen no es correcta
                except:
                    messagebox.showinfo(message="La ruta de imagen no es correcta", title="Error")  
            #Mensaje si el codigo del diagrama no existe en la base de datos
            else:
                messagebox.showinfo(message="El codigo no existe", title="Error")
            #Se limpia la ruta
            self.ruta=""
            entrada_orden.focus()
        #Si bandera es igual a 1
        elif self.bandera==1:
            try:  
                #Se comprueban todos los campos
                if str(self.orden.get()).isspace() ==False and str(self.orden.get())!="" and int(self.partes.get())>0 and int(self.partesaceptadas.get())>0 and int(self.partesrechazadas.get())>0:
                    #Se comprueba que el total de partes sea igual a las rechazadas + las aceptadas
                    if (int(self.partesaceptadas.get())+int(self.partesrechazadas.get()))== int(self.partes.get()):
                        #Se cambia el texto del boton a Mostrar Diagrama
                        self.text.set("Mostrar diagrama")
                        #Se regresa la bandera a 0
                        self.bandera=0
                        #Se inserta en la tabla Log todos los datos requeridos
                        self.cur.execute("INSERT INTO Log (Fecha, FKEmpleadoID, FKDiagramaID, NumOrden, Partes, PartesRe, PartesAc) VALUES (default, ?, ?, ?, ?, ?, ?)", (int(str(self.id.get())), int(str(self.diagramaid.get())), str(self.orden.get()), int(self.partes.get()), int(self.partesrechazadas.get()), int(self.partesaceptadas.get())))
                        #Se hace commit a la base de datos
                        self.conn.commit()
                        #Se regresa entrada_codigo de disabled a normal
                        entrada_codigo.config(state='normal')
                        #Se limpian Entrys
                        entrada_codigo.delete(0, 'end')
                        entrada_orden.delete(0, 'end')
                        entrada_partes.delete(0, 'end')
                        entrada_partesaceptadas.delete(0, 'end')
                        entrada_partesrechazadas.delete(0, 'end')
                        entrada_codigo.focus()
            #Mensaje si no se capturan bien los datos o la suma de las partes no son iguales
            except:
                messagebox.showinfo(message="Incongruencia en los datos capturados", title="Error")
                entrada_orden.focus()
        
                
        
            
    
        
   