from tkinter import *
import Registro
import Sistema
import Modificar
import Administrador
from tkinter import messagebox
import mariadb
import sys
from Interfaz import Interfaz_Main
import tkinter as tk
import os

class Main(tk.Frame):
#Ventana principal
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent=parent
        
        #Declaracion de variables globales para los controles tipo Entry
        global nombre
        global numero
        global entrada_login_nombre
        global entrada_login_numero
        
        #Declaracion de variables para capturar el resultado de cada Entry
        self.nombre=StringVar()
        self.numero=StringVar()
        self.empleadoid=IntVar()
        #Titulo de la ventana
        self.parent.title("Inicio")

        #Creacion de los controladores que estaran presentes en la ventana
        Label(self, text="Inicie sesion o registrese", bg="LightGreen", width="300", height="2", font=("Calibri", 20)).pack()
        
        Label(self, text="").pack()
        
        Label(self, text="Introduce tu usuario", font=("Calibri", 15)).pack()
        entrada_login_nombre=Entry(self, textvariable=self.nombre, font=("Calibri", 15))
        entrada_login_nombre.pack()
        entrada_login_nombre.focus()
        
        Label(self, text="").pack()
        
        Label(self, text="Introduce tu contrasena", font=("Calibri", 15)).pack()
        entrada_login_numero=Entry(self, textvariable=self.numero, font=("Calibri", 15))
        entrada_login_numero.pack()
        
        Label(self, text="").pack()       
        
        Button(self, text="Iniciar sesion", bg="LightGreen", command=self.valores_sistema, font=("Calibri", 15)).pack()
        
        Label(self, text="").pack()
        #Se llama a la interfaz
        ex=Interfaz_Main()
    
    #Metodo para dar acceso al sistema 
    def valores_sistema(self):
        #Si el nombre y numero coinciden con admin y 1521 respectivamente, se abre la ventana de administrador directamente
        #y se limpian los Entry
        if str(self.nombre.get())=="admin" and str(self.numero.get())=="1521":
            messagebox.showinfo(message="Has iniciado sesion como administrador", title="Inicio exitoso")
            Administrador.Administrador(self.parent)
            entrada_login_numero.delete(0, 'end')
            entrada_login_nombre.delete(0, 'end')
            entrada_login_nombre.focus()
        #Si no coincide procede a buscar si es un empleado registrado
        else:
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
            try:
                #Se declara un contador
                self.contador=0
                #Se ejecuta la consulta donde se busca el empleado con el nombre y contraseña especificada
                self.cur.execute("SELECT EmpleadoID, NumEmpleado, Nombre FROM Empleado WHERE NumEmpleado=? AND Nombre=?", (self.numero.get(), self.nombre.get()))
                #Si la consulta encuentra un resultado se suma 1 al contador
                for EmpleadoID, NumEmpleado, Nombre in self.cur:
                    self.contador=self.contador+1
                #Si el contador es igual o mayor a 1
                if self.contador>=1:
                    #Se guarda el id de empleado en empleadoid
                    self.empleadoid= EmpleadoID
                    messagebox.showinfo(message="Has iniciado sesion", title="Inicio exitoso")
                    #Se llama a la clase Sistema y se le envian como parametros el nombre, contraseña y empleadoid
                    Sistema.Sistema(self.parent, self.nombre.get(), self.numero.get(), self.empleadoid )
                    #Se limpian los Entry
                    entrada_login_numero.delete(0, 'end')
                    entrada_login_nombre.delete(0, 'end')
                    entrada_login_nombre.focus()
                    #Se cierra la conexion con la base de datos
                    self.conn.close()
                #Si no se cumple ninguna condicion se muestra un mensaje
                else:
                    messagebox.showinfo(message="El usuario no existe, porfavor registrese", title="Usuario inexistente")
                    entrada_login_nombre.focus()
            except mariadb.Error as e: 
                print(f"Error: {e}")
#Se llama a la clase para que se ejecute y muestre la ventana ya que es la ventana principal es necesario hacerlo con este metodo
if __name__=="__main__":
    root=tk.Tk()
    Main(root).pack(side="top", fill="both", expand=True)
    root.mainloop()