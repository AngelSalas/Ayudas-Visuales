from tkinter import *
from tkinter import messagebox
import mariadb
import Administrador
import tkinter as tk
import os
import sys

class Modificar(tk.Toplevel):
    def __init__(self, parent):
        
        super().__init__(parent)
        self.parent=parent
        #Parametros para crear la ventana
        self.title("Modificacion de diagramas")
        self.geometry("1000x520+0+0")
        self.protocol("WM_DELETE_WINDOW", self.volver)
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

        # Get Cursor
        self.cur = self.conn.cursor()

        #Declaracion de variables globales para los controles tipo Entry
        global entrada_version
        global entrada_numero
        global entrada_familia
        global entrada_ruta

        #Declaracion de variables para capturar el resultado de cada Entry
        self.numero=StringVar()
        self.familia=StringVar()
        self.version=StringVar()
        self.ruta=StringVar()

        #Creacion de los controladores que estaran presentes en la ventana
        Label(self, text="").pack()
        
        etiqueta_numero=Label(self, text="Numero de parte", font=("Calibri", 15))
        etiqueta_numero.pack()
        
        entrada_numero=Entry(self, textvariable=self.numero, font=("Calibri", 15))
        entrada_numero.pack()
        entrada_numero.focus()
        
        etiqueta_familia= Label(self, text="Familia", font=("Calibri", 15))
        etiqueta_familia.pack()
        
        entrada_familia=Entry(self, textvariable=self.familia, font=("Calibri", 15))
        entrada_familia.pack()
        
        etiqueta_version= Label(self, text="Version", font=("Calibri", 15))
        etiqueta_version.pack()
        
        entrada_version=Entry(self, textvariable=self.version, font=("Calibri", 15))
        entrada_version.pack()
        
        etiqueta_ruta= Label(self, text="Nombre del archivo con extension, ejemplo(Archivo.png)", font=("Calibri", 15))
        etiqueta_ruta.pack()
        
        entrada_ruta=Entry(self, textvariable=self.ruta, font=("Calibri", 15))
        entrada_ruta.pack()
        
        Label(self, text="").pack()
        Label(self, text="Para agregar o editar un diagrama es necesario que llene todos los campos",fg="Blue", font=("Calibri", 15)).pack()
        
        Button(self, text="Agregar", width=10, height=1, bg="LightGreen", command=self.agregar, font=("Calibri", 15)).pack()
        
        Label(self, text="").pack()
        
        Button(self, text="Editar", width=10, height=1, bg="gold2", command=self.editar, font=("Calibri", 15)).pack()
        
        Label(self, text="").pack()
        Label(self, text="Para borrar un diagrama solo se necesita el numero de parte",fg="Blue", font=("Calibri", 15)).pack()
        Button(self, text="Borrar", width=10, height=1, bg="coral1", command=self.borrar, font=("Calibri", 15)).pack()
        
        Label(self, text="").pack()
        
        Button(self, text="Volver", width=5, height=1, bg="SteelBlue1", command=self.volver, font=("Calibri", 15)).place(relx=.914, rely=.015)
        
        self.parent.withdraw()

    #Metodo para volver a la ventana principal
    def volver(self):
        Administrador.Administrador(self.parent)
        self.destroy()
        #Cierra la conexion a la base de datos
        self.conn.close()
    
    #Metodo para agregar diagramas
    def agregar(self):
        try:
            #Se crea la varible contador
            contador=0
            #Se busca un diagrama con el numero de parte especificado por el usuario
            self.cur.execute("SELECT NumeroParte FROM Diagrama WHERE NumeroParte=?", (self.numero.get(),))
            #Si se encuentra un diagrama se suma 1 al contador
            for NumeroParte in self.cur:
                contador=contador+1
            #Si el contador es igual o mayor a 1 solo se muestra un mensaje y se limpia el Entry de numero
            if contador>=1:
                messagebox.showinfo(message="Ya existe un diagrama con dicho numero de parte", title="Numero existente")
                entrada_numero.delete(0, 'end')
                entrada_numero.focus()
            #Si no se encuentra el diagrama con dicho numero de parte se agrega a la base de datos
            else:
                #Se comprueban todos los campos
                if str(self.familia.get()).isspace() ==False and str(self.familia.get())!="" and str(self.numero.get()).isspace()==False and str(self.numero.get())!="" and str(self.version.get()).isspace()==False and str(self.version.get())!="" and str(self.ruta.get()).isspace()==False and str(self.ruta.get())!="":
                    #Se inserta en la tabla Diagrama todos los datos necesarios y se limpian todos los Entry
                    self.cur.execute("INSERT INTO Diagrama (Familia,RutaImagen,Version,NumeroParte) VALUES (?, ?, ?, ?)", (str(self.familia.get()),"Diagramas/"+str(self.ruta.get()), str(self.version.get()), str(self.numero.get())))
                    messagebox.showinfo(message="Se agrego el diagrama con exito", title="Exito")
                    entrada_version.delete(0, 'end')
                    entrada_familia.delete(0, 'end')
                    entrada_ruta.delete(0, 'end')
                    entrada_numero.delete(0, 'end')
                    entrada_numero.focus()
                #Si el llenado de los campos es incorrecto se muestra un mensaje
                else:
                    messagebox.showinfo(message="Asegurese que lleno todos los campos", title="Error")
                    entrada_numero.focus()
        except mariadb.Error as e: 
            print(f"Error: {e}")
        #Se hace el commit a la base de datos
        self.conn.commit()
    
    #Metodo para editar diagramas existentes
    def editar(self):
        try:
            #Se crea la variable contador
            contador=0
            #Se busca un diagrama con el numero de parte especificado por el usuario
            self.cur.execute("SELECT NumeroParte FROM Diagrama WHERE NumeroParte=?", (self.numero.get(),))
            #Si se encuentra un diagrama se suma 1 al contador
            for NumeroParte in self.cur:
                contador=contador+1
            #Si el contador es menor a 1 se muestra el mensaje de diagrama inexistente y se limpia el Entry de numero
            if contador<1:
                messagebox.showinfo(message="No existe un diagrama con dicho numero de parte", title="Error")
                entrada_numero.delete(0, 'end')
                entrada_numero.focus()
            #Si contador es mayor a 1
            else:
                #Se comprueban todos los campos
                if str(self.familia.get()).isspace() ==False and str(self.familia.get())!="" and str(self.version.get()).isspace()==False and str(self.version.get())!="" and str(self.ruta.get()).isspace()==False and str(self.ruta.get())!="":
                    #Se hace un update al a tabla diagrama con los datos especificados por el usuario al diagrama con el numero de parte especificado
                    #se muetra un mensaje y se limpian las Entry
                    self.cur.execute("UPDATE Diagrama SET Familia=?, Version=?, RutaImagen=? WHERE NumeroParte=?",(str(self.familia.get()),str(self.version.get()),"Diagramas/"+str(self.ruta.get()), str(self.numero.get())))
                    messagebox.showinfo(message="Se modifico el diagrama con exito", title="Exito")
                    entrada_version.delete(0, 'end')
                    entrada_familia.delete(0, 'end')
                    entrada_ruta.delete(0, 'end')
                    entrada_numero.delete(0, 'end')
                    entrada_numero.focus()
                #Si el llenado de los campos es incorrecto se muestra un mensaje
                else:
                    messagebox.showinfo(message="Asegurese que lleno todos los campos", title="Error")
                    entrada_numero.focus()
        except mariadb.Error as e: 
            print(f"Error: {e}")
        #Se hace el commit a la base de datos
        self.conn.commit()
        
    #Metodo que permite borrar un diagrama existente
    def borrar(self):
        try:
            #Se crea la variable contador
            contador=0
            #Se busca un diagrama con el numero de parte especificado por el usuario
            self.cur.execute("SELECT NumeroParte FROM Diagrama WHERE NumeroParte=?", (self.numero.get(),))
            #Si se encuentra un diagrama se suma 1 al contador
            for NumeroParte in self.cur:
                contador=contador+1
            #Si el contador es menor a 1 se muestra el mensaje de diagrama inexistente y se limpia el Entry de numero
            if contador<1:
                messagebox.showinfo(message="No existe un diagrama con dicho numero de parte", title="Numero existente")
                entrada_numero.delete(0, 'end')
                entrada_numero.focus()
            else:
                #Se comprueban todos los campos
                if str(self.numero.get()).isspace() ==False and str(self.numero.get())!="":
                    #Se borra el diagrama con el numero de parte especificado, se muestra mensaje y se limpian las Entry
                    self.cur.execute("DELETE FROM Diagrama WHERE NumeroParte=?",(str(self.numero.get()),))
                    messagebox.showinfo(message="Se borro el diagrama con exito", title="Exito")
                    entrada_version.delete(0, 'end')
                    entrada_familia.delete(0, 'end')
                    entrada_ruta.delete(0, 'end')
                    entrada_numero.delete(0, 'end')
                    entrada_numero.focus()
                #Si el llenado de los campos es incorrecto se muestra un mensaje
                else:
                    messagebox.showinfo(message="Asegurese que lleno el campo >Numero<", title="Error")
                    entrada_numero.focus()
        except mariadb.Error as e: 
            print(f"Error: {e}")
        #Se hace el commit a la base de datos
        self.conn.commit()
        