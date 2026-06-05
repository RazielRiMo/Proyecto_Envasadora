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
    try:
        nivel = int(textbox.get())
        if ((nivel <= 100) & (nivel >=0)):
            #aqui se supone envia el datos
            pass
        else:
            raise ValueError("el numero tiene que ser entre 0 y 100")
    except ValueError as er:
        messagebox.showerror("ERROR", str(er))

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

fr1 = tk.Frame(v,
               bg="#ffffff",
               width=400,
               height=700)
fr1.grid(row=0, column=0)

#frame de monitoreo de datos y estacion

fr2 = tk.Frame(v,
               bg="lightblue",
               width=400,
               height=700)
fr2.grid(row=0, column=1)

#frame de historial de datos recibidos

fr3 = tk.Frame(v,
               bg="#ffffff",
               width=400,
               height=700)
fr3.grid(row=0, column=2)

#sub frame1 niv 1

sf1n1 = tk.Frame(fr1,
                 bg="#ffffff",
                 width=400,
                 height=50)

sf1n1.pack()
sf1n1.pack_propagate(False)

sf2n1 = tk.Frame(fr1,
                 bg="#8b8b8b",
                 width=400,
                 height=650)

sf2n1.pack()
sf2n1.pack_propagate(False)

#botones frame 1 subframe 1 nivel 1

iniserv = tk.Button(
    sf1n1,
    text="iniciar servidor",
    width=24,
    height=1,
    command=iniciar_servidor,
    bg="#ffffff")

iniserv.grid(row=0, column=0, padx=10, pady=5)
iniserv.grid_propagate(False)

detserv = tk.Button(sf1n1,
                    text="detener servidor",
                    width=24, height=1,
                    command=detener_servidor,
                    bg="#ffffff",
                    fg="#000000")

detserv.grid(row=0,column=1,padx=10,pady=5)
detserv.grid_propagate(False)

#subfame 1 subreames nivel 2

sf1n2 =tk.Frame(sf2n1,
                bg="#ffffff",
                width=200,
                height=650)

sf1n2.grid(row=0,column=0)
sf1n2.grid_propagate(False)

sf2n2 =tk.Frame(sf2n1,
                bg="#d69393",
                width=200,
                height=650)

sf2n2.grid(row=0,column=1)
sf2n2.grid_propagate(False)

#contenido subframe 1 nivel 2 

sf1n3 = tk.Frame(sf1n2,
                 bg="#00F5E9",
                 width=180,
                 height=630,
                 highlightbackground="#000000",
                 highlightthickness=2)

sf1n3.pack(padx=10, pady=10)

#contenido subframe 2 nivel 2 sub frames nivel 3

sf2n3 = tk.Frame(sf2n2,
                 bg="#FFFFFF",
                 width=200,
                 height=250)

sf2n3.pack()
sf2n3.pack_propagate(False)

sf3n3 = tk.Frame(sf2n2,
                 bg="#FFFFFF",
                 width=200,
                 height=400)

sf3n3.pack()
sf3n3.pack_propagate(False)

#label estado de botella

estado_botella = tk.Label(sf2n3,
                          text="ESPERANDO\nCONECCION",
                          justify="center",
                          fg="#FF0000",
                          font=("Rockwell",10),
                          bg="#ffffff",
                          height=2,
                          width=28)

estado_botella.pack(pady=10)
estado_botella.pack_propagate(False)

#label explicacion

label1 = tk.Label(sf2n3,
                  text="Digite la cantidad\nque desea llenar",
                  justify="center",
                  fg="#000000",
                  font=("Consolas", 10),
                  bg="#ffffff",
                  height=2,
                  width=28)

label1.pack(pady=10)
label1.pack_propagate(False)

#text box para la digitacion en mililitros

textbox = tk.Entry(sf2n3,
                   width=30,
                   bg="#ffffff",
                   fg="#000000",
                   highlightbackground="#000000",
                   highlightthickness=2,
                   justify="center")

textbox.pack(padx=10,pady=10, ipady=6)
textbox.pack_propagate(False)

#boton de llenado

llenar = tk.Button(sf2n3,
                   text="LLENAR",
                   width=24,
                   height=2,
                   command=enviar_nivel,
                   bg="#ffffff",
                   fg="#000000")

llenar.pack(padx=10,pady=10)
llenar.pack_propagate(False)

#contenido subframe 3 nivel 3

label2 = tk.Label(sf3n3,
                  text="ESTADO\nDEL TANQUE",
                  justify="center",
                  font=("Consolas", 15),
                  width=20,
                  height=2,
                  bg="#ffffff",
                  fg="#000000")

label2.pack(pady=10)

#subframe de nivel 4

estado_tanque = tk.Frame(sf3n3,
                         bg="#B40488",
                         highlightbackground="#000000",
                         highlightthickness=2,
                         width=180,
                         height=350)

estado_tanque.pack(padx=10,pady=10)
estado_tanque.pack_propagate(False)

v.mainloop()