import tkinter as tk
from tkinter import messagebox
import json

def iniciar_servidor ():
    #de momento aqui no hay nada    
    pass

def detener_servidor ():
    #de momento aqui no hay nada
    pass

def enviar_nivel ():
    #de momento aqui no hay nada
    pass

def parada_de_emergencia():
    #de momento aqui no hay nada
    pass

#definicion y tamaño de la ventana

v = tk.Tk()
v.title("INTERFASE ENVASADORA")
v["bg"]="#ffffff"
v.geometry("1200x700")

#definicion de los 3 framesutilizados principalmente

#ferame de control de agua y conceccion

fr1 = tk.Frame(v, bg="#ffffff", width=400, height=700)
fr1.grid(row=0, column=0)

#frame de monitoreo de datos y estacion

fr2 = tk.Frame(v, bg="lightblue", width=400, height=700)
fr2.grid(row=0, column=1)

#frame de historial de datos recibidos

fr3 = tk.Frame(v, bg="#ffffff", width=400, height=700)
fr3.grid(row=0, column=2)

#sub frame1 niv 1

sf1n1 = tk.Frame(fr1, bg="#ffffff", width=400, height=50)
sf1n1.pack()
sf1n1.pack_propagate(False)
sf2n1 = tk.Frame(fr1, bg="#8b8b8b", width=400, height=650)
sf2n1.pack()
sf2n1.pack_propagate(False)

#botones frame 1 subframe 1 nivel 1

iniserv = tk.Button(sf1n1, text="iniciar servidor", width=24, height=1, command=iniciar_servidor,bg="#ffffff")
iniserv.grid(row=0,column=0,padx=10,pady=5)
iniserv.grid_propagate(False)
detserv = tk.Button(sf1n1, text="detener servidor", width=24, height=1, command=detener_servidor,bg="#ffffff", fg="#000000")
detserv.grid(row=0,column=1,padx=10,pady=5)
detserv.grid_propagate(False)

#subfame 1 subreames nivel 2

sf1n2 =tk.Frame(sf2n1, bg="#ffffff", width=200, height=650)
sf1n2.grid(row=0,column=0)
sf1n2.grid_propagate(False)
sf2n2 =tk.Frame(sf2n1, bg="#d69393", width=200, height=650)
sf2n2.grid(row=0,column=1)
sf2n2.grid_propagate(False)

#contenido subframe 1 nivel 2 

sf1n3 = tk.Frame(sf1n2,bg="#00F5E9", width=180,height=630, highlightbackground="#000000", highlightthickness=2)
sf1n3.pack(padx=10, pady=10)

#contenido subframe 2 nivel 2 sub frames nivel 3

sf2n3 = tk.Frame(sf2n2,bg="#FF0000", width=200,height=325)
sf2n3.pack()
sf2n2.pack_propagate(False)
sf3n3 = tk.Frame(sf2n2,bg="#00F54A", width=200,height=325)
sf3n3.pack()
sf3n3.pack_propagate(False)

#estad

estado_botella = tk.Label(sf2n3, text="ESPERANDO \nCONECCION", justify="center",fg="#FF0000", font=("Rockwell",10))
estado_botella.pack()
estado_botella.pack_propagate(False)



v.mainloop()