#Interfaz para la ventana principal
from tkinter import *
import tkinter as tk
class Interfaz_Main(tk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
      
        self.centerWindow()
    #Centra la ventana en la pantalla
    def centerWindow(self):
        w=500
        h=300
        
        sw=self.master.winfo_screenwidth()
        sh=self.master.winfo_screenheight()
        
        x=(sw-w)/2
        y=(sh-h)/2
        self.master.geometry('%dx%d+%d+%d' % (w,h,x,y))
        
