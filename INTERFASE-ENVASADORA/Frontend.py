import tkinter as tk
from tkinter import messagebox, ttk
import json


#definicion y tamaño de la ventana
class Frontend (tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INTERFASE ENVASADORA")
        self.geometry("1200x700")
        self.configure(bg="#ffffff")
        
        self.selected_tp = tk.StringVar(value="todos")
        self.objetosframe1()
        #self.refrescarventana()

    def objetosframe1(self):
        self.style = ttk.Style()
        
        self.style.configure("main.TFrame", background="#ffffff")
        v = ttk.Frame(self, style="main.TFrame")
        v.pack()
        #definicion de los 3 framesutilizados principalmente

        #ferame de control de agua y conceccion
        
        self.style.theme_use("clam")
        self.style.configure("control.TFrame", background = "#ffffff")
        self.Control_de_agua = ttk.Frame(v,
                                        width=400,
                                        height=700,
                                        style="control.TFrame")
        self.Control_de_agua.grid(row=0, column=0)
        self.Control_de_agua.grid_propagate(False)

        #frame de monitoreo de datos y estacion

        self.style.configure("seguimiento.TFrame", background="#FFFFFF")
        self.fr2 = ttk.Frame(v,
                            width=400,
                            height=700,
                            style="seguimiento.TFrame")
        
        self.fr2.grid(row=0, column=1)
        self.fr2.grid_propagate(False)
        
        #frame de historial de datos recibidos
        
        self.style.configure("registro.TFrame", background="#e70000")
        self.fr3 = ttk.Frame(v,
                            width=400,
                            height=700,
                            style="registro.TFrame")
        
        self.fr3.grid(row=0, column=2)
        self.fr3.grid_propagate(False)

        #sub frame1 niv 1
        self.style.configure("inidet.TFrame", background="#ffffff")
        self.iniciar_detener_servidor = ttk.Frame(self.Control_de_agua,
                                            style="inidet.TFrame",
                                            width=400,
                                            height=50)

        self.iniciar_detener_servidor.pack()
        self.iniciar_detener_servidor.pack_propagate(False)

        self.style.configure("controlniv.TFrame", background="#8b8b8b")
        self.caja_control_nivel = ttk.Frame(self.Control_de_agua,
                                        style="controlniv.TFrame",
                                        width=400,
                                        height=650)

        self.caja_control_nivel.pack()
        self.caja_control_nivel.pack_propagate(False)

        #botones frame 1 subframe 1 nivel 1

        self.style.configure("iniserv.TButton", background="#ffffff")
        self.iniserv = ttk.Button(self.iniciar_detener_servidor,
                                style="iniserv.TButton",
                                text="iniciar servidor",
                                width=24,
                                command=iniciar_servidor)

        self.iniserv.grid(row=0, column=0, padx=10, pady=5)
        self.iniserv.grid_propagate(False)

        self.style.configure("detserv.TButton", background="#ffffff")
        self.detserv = ttk.Button(self.iniciar_detener_servidor,
                                style="detserv.TButton",  
                                text="detener servidor",
                                width=24,
                                command=detener_servidor)

        self.detserv.grid(row=0,column=1,padx=10,pady=5)
        self.detserv.grid_propagate(False)

        #subfame 1 subreames nivel 2
        self.style.configure("nivelg.TFrame", background="#ffffff")
        self.contenedor_nivel_grafico =ttk.Frame(self.caja_control_nivel,
                                            width=200,
                                            height=650,
                                            style="nivelg.TFrame")

        self.contenedor_nivel_grafico.grid(row=0,column=0)
        self.contenedor_nivel_grafico.grid_propagate(False)

        self.style.configure("conniv.TFrame", background="#ffffff")
        self.sf2n2 =ttk.Frame(self.caja_control_nivel,
                        style="conniv.TFrame",
                        width=200,
                        height=650)

        self.sf2n2.grid(row=0,column=1)
        self.sf2n2.grid_propagate(False)

        #contenido subframe 1 nivel 2 

        self.style.configure("nivgr.TFrame", background="#1BE4FF", borderwidth=2, relief="solid")
        sf1n3 = ttk.Frame(self.contenedor_nivel_grafico,
                        style="nivgr.TFrame",
                        width=180,
                        height=630)

        sf1n3.pack(padx=10, pady=10)

        #contenido subframe 2 nivel 2 sub frames nivel 3

        self.style.configure("nomeacuerdo.TFrame", background="#FFFFFF")
        self.sf2n3 = ttk.Frame(self.sf2n2,
                        style="nomeacuerdo.TFrame",
                        width=200,
                        height=250)

        self.sf2n3.pack()
        self.sf2n3.pack_propagate(False)

        self.style.configure("niputidea.TFrame", background="#FFFFFF")
        self.sf3n3 = ttk.Frame(self.sf2n2,
                        style="niputidea.TFrame",
                        width=200,
                        height=400)

        self.sf3n3.pack()
        self.sf3n3.pack_propagate(False)

        #label estado de botella

        self.style.configure("estadobotella.TLabel", foreground="#ff0000", background="#ffffff", font=("Rockwell",10))
        estado_botella = ttk.Label(self.sf2n3,
                                text="ESPERANDO\nCONECCION",
                                justify="center",
                                anchor="center",
                                style="estadobotella.TLabel",
                                width=28)

        estado_botella.pack(pady=10)
        estado_botella.pack_propagate(False)

        #label explicacion

        self.style.configure("label1.TLabel", foreground="#000000", background="#ffffff",font=("Consolas", 10))
        label1 = ttk.Label(self.sf2n3,
                        text="Digite la cantidad\nque desea llenar",
                        justify="center",
                        anchor="center",
                        style="label1.TLabel",
                        width=28)

        label1.pack(pady=10)
        label1.pack_propagate(False)

        #text box para la digitacion en mililitros

        self.style.configure("textbox.TEntry", foreground="#000000", fieldbackground="#ffffff", background="#ffffff", bordercolor="#000000")
        self.textbox = ttk.Entry(self.sf2n3,
                        width=30,
                        style="textbox.TEntry",
                        justify="center")

        self.textbox.pack(padx=10,pady=10, ipady=6)
        self.textbox.pack_propagate(False)

        #boton de llenado

        self.style.configure("llenar.TButton", background= "#ffffff")
        self.llenar = ttk.Button(self.sf2n3,
                        text="LLENAR",
                        width=24,
                        command=enviar_nivel,
                        style="llenar.TButton")

        self.llenar.pack(padx=10,pady=10)
        self.llenar.pack_propagate(False)

        #contenido subframe 3 nivel 3

        self.style.configure("label2.TLabel", font=("Consolas", 15),background="#ffffff", foregraund="#000000")
        self.label2 = ttk.Label(self.sf3n3,
                        text="ESTADO\nDEL TANQUE",
                        justify="center",
                        width=20,
                        anchor="center",
                        style="label2.TLabel")

        self.label2.pack(pady=10)

        #subframe de nivel 4

        self.style.configure("estadotanque.TFrame", background="#B40488", borderwidth=2, relief="solid")
        self.estado_tanque = ttk.Frame(self.sf3n3,
                                width=180,
                                height=350,
                                style="estadotanque.TFrame")

        self.estado_tanque.pack(padx=10,pady=10)
        self.estado_tanque.pack_propagate(False)
        
        self.style.configure("lleno.TFrame", background="#00ff00")
        self.lleno = ttk.Frame(self.estado_tanque,
                               width=180,
                               height=90,
                               style="lleno.TFrame")
        
        self.lleno.pack()
        self.lleno.pack_propagate(False)
        
        self.style.configure("medio.TFrame", background="#d9ff00")
        self.medio = ttk.Frame(self.estado_tanque,
                               width=180,
                               height=130,
                               style="medio.TFrame")
        
        self.medio.pack()
        self.medio.pack_propagate(False)
        
        self.style.configure("critico.TFrame", background="#ff0000")
        self.critico = ttk.Frame(self.estado_tanque,
                               width=180,
                               height=90,
                               style="critico.TFrame")
        
        self.critico.pack()
        self.critico.pack_propagate(False)
        
        
    
def refrescarventana(self):
        pass
        
def iniciar_servidor (self):
    #de momento aqui no hay nada    
        pass

def detener_servidor (self):
    #de momento aqui no hay nada
    pass

def enviar_nivel (self):
    #de momento aqui no hay nada
    try:
        nivel = int(self.textbox.get())
        if ((nivel <= 100) & (nivel >=0)):
            #aqui se supone envia el datos
            pass
        else:
            raise ValueError("el numero tiene que ser entre 0 y 100")
    except ValueError as er:
        messagebox.showerror("ERROR", str(er))

def parada_de_emergencia(self):
    #de momento aqui no hay nada
    pass



if __name__ == "__main__":
    app = Frontend()
    app.mainloop()
