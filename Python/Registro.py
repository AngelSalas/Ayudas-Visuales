from tkinter import *
from tkinter import messagebox
import Administrador
import mariadb
import tkinter as tk
import os
import sys

class Registro(tk.Toplevel):
    def __init__(self, parent):
        
        super().__init__(parent)
        self.parent=parent
        #Parametros para crear la ventana
        self.title("Registro")
        self.geometry("350x350+0+0")
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
        global nombre
        global numero
        global entrada_nombre
        global entrada_numero

        #Declaracion de variables para capturar el resultado de cada Entry
        self.nombre=StringVar()
        self.numero=StringVar()
        
        #Creacion de los controladores que estaran presentes en la ventana
        Label(self, text="Introduzca sus datos", bg="LightGreen", width="300", height="2", font=("Calibri", 20)).pack()
        Label(self, text="").pack()
        
        etiqueta_nombre=Label(self, text="Nombre", font=("Calibri", 15))
        etiqueta_nombre.pack()
        
        entrada_nombre=Entry(self, textvariable=self.nombre, font=("Calibri", 15))
        entrada_nombre.pack()
        entrada_nombre.focus()
        
        Label(self, text="").pack()
        
        etiqueta_numero= Label(self, text="Numero de empleado", font=("Calibri", 15))
        etiqueta_numero.pack()
        
        entrada_numero=Entry(self, textvariable=self.numero, font=("Calibri", 15))
        entrada_numero.pack()
        
        Label(self, text="").pack()
        
        Button(self, text="Registrarse", width=10, height=1, bg="LightGreen", command=self.registro, font=("Calibri", 15)).pack()
        
        Label(self, text="").pack()
        
        Button(self, text="Volver", width=5, height=1, bg="SteelBlue1", command=self.volver, font=("Calibri", 15)).pack()
        
        self.parent.withdraw()
    #Metodo para volver a la ventana principal
    def volver(self):
        Administrador.Administrador(self.parent)
        self.destroy()
        #Cierra la conexion a la base de datos
        self.conn.close()
    
    #Metodo para registrar usuarios 
    def registro(self):
        try:
            #Se crea la varible contador
            contador=0
            #Se busca un empleado con el numero de empleado especificado por el usuario
            self.cur.execute("SELECT NumEmpleado FROM Empleado WHERE NumEmpleado=?", (self.numero.get(),))
            #Si se encuentra un empleado se suma 1 al contador
            for NumEmpleado in self.cur:
                contador=contador+1
            #Si el contador es igual o mayor a 1 solo se muestra un mensaje y se limpia el Entry de numero
            if contador>=1:
                messagebox.showinfo(message="Ya existe un usuario con dicho numero", title="Numero existente")
                entrada_numero.delete(0, 'end')
                entrada_numero.focus()
            #Si no se encuentra el empleado con dicho numero de parte se agrega a la base de datos
            else:
                #Se comprueban todos los campos
                if str(self.nombre.get()).isspace() ==False and str(self.nombre.get())!="" and str(self.numero.get()).isspace()==False and str(self.numero.get())!="":
                    #Se inserta en la tabla Empleado todos los datos necesarios y se limpian todos los Entry
                    self.cur.execute("INSERT INTO Empleado (Nombre,NumEmpleado) VALUES (?, ?)", (str(self.nombre.get()),str(self.numero.get())))
                    messagebox.showinfo(message="Se ha registrado con exito", title="Exito")
                    entrada_nombre.delete(0, 'end')
                    entrada_numero.delete(0, 'end')
                    entrada_nombre.focus()
                #Si el llenado de los campos es incorrecto se muestra un mensaje
                else:
                    messagebox.showinfo(message="Ingrese su nombre o numero de empleado", title="Error")
                    entrada_nombre.focus()
        except mariadb.Error as e: 
            print(f"Error: {e}")
    
        #Se hace el commit a la base de datos
        self.conn.commit()
        
       