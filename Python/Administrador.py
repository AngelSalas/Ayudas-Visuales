from tkinter import *
from tkinter import messagebox
import Modificar
import csv
import Registro
import mariadb
import tkinter as tk
import os
import time
import sys

class Administrador(tk.Toplevel):
    def __init__(self, parent):
        

        super().__init__(parent)
        self.parent=parent
        #Parametros para crear la ventana
        self.title("Administrador")
        self.geometry("500x520+0+0")
        self.protocol("WM_DELETE_WINDOW", self.volver)
        
        #Creacion de los controladores que estaran presentes en la ventana
        Label(self, text="Panel de administrador", bg="LightGreen", width="500", height="2", font=("Calibri", 35)).pack()

        Label(self, text="").pack()      
               
        Button(self, text="Registro", bg="LightGoldenrod1", width="500", height="2", command=self.valores_registro, font=("Calibri", 25)).pack()
        
        Label(self, text="").pack()        
        
        Button(self, text="Modificar diagramas", bg="CadetBlue1", width="500", height="2",command=self.valores_modificar, font=("Calibri", 25)).pack()
        
        Label(self, text="").pack()
        
        Button(self, text="Descargar log", bg="wheat1",width="500", height="2", command=self.valores_log, font=("Calibri", 25)).pack()
        
        Label(self, text="").pack()
         
        Button(self, text="Volver",bg="SteelBlue1",width="500", height="2", command=self.volver, font=("Calibri", 25)).pack()
        
        self.parent.withdraw()
        
    #Método que llama a la clase registro y destruye el actual
    def valores_registro(self):
        Registro.Registro(self.parent)
        self.destroy()
    
    #Método que llama a la clase modificar y destruye el actual
    def valores_modificar(self):
        Modificar.Modificar(self.parent)
        self.destroy()
    ##Método que crea el archivo de log en su respectiva carpeta
    def valores_log(self):
        #Se guarda la consulta a realizar
        self.QUERY='SELECT * FROM Log;'
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
        #Se ejecuta la consulta
        self.cur.execute(self.QUERY)
        #Se guarda el resultado de la consulta
        self.result=self.cur.fetchall()
        #Se obtiene el tiempo local
        self.ts = time.localtime()
        #Se ordena en horas:minutos:segundos dia-mes-año
        self.readable = time.strftime("%H:%M:%S %d-%m-%Y",self.ts)
        #Se crea el archivo con la direccion, nombre y extension especificada, en este caso el nombre es el tiempo con el formato previamente
        #establecido y se indica como tipo "writable"
        c = csv.writer(open('Logs/'+self.readable+'.csv', 'w'))
        #Se escribe el resultado de la consulta en cada fila y se muestra un mensaje
        for x in self.result:
            c.writerow(x)
        messagebox.showinfo(message="Se ha creado el archivo en la carpeta Logs", title="Exito")
        #Se cierra la conexion a la base de datos
        self.conn.close()
    #Metodo para volver a la ventana principal
    def volver(self):
        self.parent.deiconify()
        self.destroy()

        
