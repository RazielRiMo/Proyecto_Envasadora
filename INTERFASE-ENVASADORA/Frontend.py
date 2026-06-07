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
        
        self.x=0
        self.y=100
        
        self.automatico = tk.BooleanVar(value=True)
        self.nivel = tk.IntVar(value=50)
        self.objetosventana()
        #self.refrescarventana()

    def objetosventana(self):
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
        self.frame_info = ttk.Frame(v,
                            width=400,
                            height=700,
                            style="seguimiento.TFrame")
        
        self.frame_info.grid(row=0, column=1)
        self.frame_info.grid_propagate(False)
        
        #frame de historial de datos recibidos
        
        self.style.configure("registro.TFrame", background="#ffffff")
        self.frame_registro = ttk.Frame(v,
                            width=400,
                            height=700,
                            style="registro.TFrame")
        
        self.frame_registro.grid(row=0, column=2)
        self.frame_registro.grid_propagate(False)

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

        self.style.configure("iniserv.TButton", background="#ffffff", padding=(0,9))
        self.iniserv = ttk.Button(self.iniciar_detener_servidor,
                                style="iniserv.TButton",
                                text="iniciar servidor",
                                width=24,
                                command=self.iniciar_servidor)

        self.iniserv.grid(row=0, column=0, padx=25, pady=5, sticky="w")
        self.iniserv.grid_propagate(False)

        self.style.configure("detserv.TButton", background="#ffffff", padding=(0,9))
        self.detserv = ttk.Button(self.iniciar_detener_servidor,
                                style="detserv.TButton",  
                                text="detener servidor",
                                width=24,
                                command=self.detener_servidor)

        self.detserv.grid(row=0,column=1,padx=25,pady=5, sticky="e")
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
        self.contenedor_nivel =ttk.Frame(self.caja_control_nivel,
                        style="conniv.TFrame",
                        width=200,
                        height=650)

        self.contenedor_nivel.grid(row=0,column=1)
        self.contenedor_nivel.grid_propagate(False)

        #contenido subframe 1 nivel 2 

        self.style.configure("nivgr.TFrame", background="#1BE4FF", borderwidth=2, relief="solid")
        nivel_grafico = ttk.Frame(self.contenedor_nivel_grafico,
                        style="nivgr.TFrame",
                        width=180,
                        height=630)

        nivel_grafico.pack(padx=10, pady=10)

        #contenido subframe 2 nivel 2 sub frames nivel 3

        self.style.configure("nomeacuerdo.TFrame", background="#FFFFFF")
        self.sf2n3 = ttk.Frame(self.contenedor_nivel,
                        style="nomeacuerdo.TFrame",
                        width=200,
                        height=250)

        self.sf2n3.pack()
        self.sf2n3.pack_propagate(False)

        self.style.configure("niputidea.TFrame", background="#FFFFFF")
        self.sf3n3 = ttk.Frame(self.contenedor_nivel,
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

        self.style.configure("llenar.TButton", background= "#ffffff", padding=(0,9))
        self.llenar = ttk.Button(self.sf2n3,
                        text="LLENAR",
                        width=24,
                        command=self.enviar_nivel,
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
        
        #FRame Principal2
        
        ## Frame DE IP
        
        self.style.configure("IDframe.TFrame", background="#ffffff")
        self.IDfame = ttk.Frame(self.frame_info,
                                style="IDframe.TFrame",
                                width=400,
                                height=50,)
        
        self.IDfame.pack()
        self.IDfame.pack_propagate(False)
        
        ##Frame de informacion
        
        self.style.configure("info.TFrame", background="#ffffff")
        self.info = ttk.Frame(self.frame_info,
                              style="info.TFrame",
                              width=400,
                              height=600)
        
        self.info.pack()
        self.info.pack_propagate(False)
        
        ##Frame de boton de emergrncia
        
        self.style.configure("emergencia.TFrame", background="#ffffff")
        self.emer = ttk.Frame(self.frame_info,
                              style="emergencia.TFrame",
                              width=400,
                              height=50)
        
        self.emer.pack()
        self.emer.pack_propagate(False)
        
        ###label de ip
        
        self.style.configure("IP.TLabel", background="#ffffff", foreground="#000000", font=("Consolas", 10))
        self.labelIP = ttk.Label(self.IDfame,
                                 text="IP:0.0.0.0",
                                 width=28,
                                 style="IP.TLabel")
        
        self.labelIP.grid(column=0, row=0)
        self.labelIP.grid_propagate(False)
        
        ###label de estado del servidor
        
        self.style.configure("estadoserv.TLabel", background="#FFFFFF", foreground="#FF0000", font=("Consolas", 10), padding=(0,15))
        self.estados = ttk.Label(self.IDfame,
                                 text="SERVIDOR DETENIDO",
                                 width=28,
                                 style="estadoserv.TLabel")
        
        self.estados.grid(column=1, row=0)
        self.estados.grid_propagate(False)
        
        ###sub frames de informacion
        
        self.style.configure("titulo.TFrame", background="#ffffff")
        self.titulo = ttk.Frame(self.info,
                                style="titulo.TFrame",
                                width=400,
                                height=50)
        
        self.titulo.pack()
        self.titulo.pack_propagate(False)
        
        self.style.configure("titulo.TLabel",  background="#ffffff", foreground="#000000", font=("Consolas", 15), padding=(0,15,0,0))
        self.titu = ttk.Label(self.titulo,
                              style="titulo.TLabel",
                              text="ESTACION DE LA BOTELLA",
                              justify="center",
                              anchor="center")
        
        self.titu.pack()
        self.titu.pack_propagate(False)
        
        self.style.configure("estacion.TFrame", background="#ffffff")
        self.estacion = ttk.Frame(self.info,
                                  width=400,
                                  height=200,
                                  style="estacion.TFrame")
        
        self.estacion.pack()
        self.estacion.pack_propagate(False)
        
        self.style.configure("auto.TFrame", background="#ffffff")
        self.auto = ttk.Frame(self.info,
                              style="auto.TFrame",
                              width=400,
                              height=50)
        
        self.auto.pack()
        self.auto.pack_propagate(False)
        
        self.style.configure("radio.TRadiobutton", background="#ffffff", font=("Consolas", 10))
        self.automat = ttk.Radiobutton(self.auto,
                                       text="automatico",
                                       variable=self.automatico,
                                       value=True,
                                       style="radio.TRadiobutton",
                                       command=self.enviar_auto)
        
        self.automat.grid(column=0, row=0)
        self.automat.grid_propagate(False)
        
        self.manual = ttk.Radiobutton(self.auto,
                                      text="manual",
                                      style="radio.TRadiobutton",
                                      variable=self.automatico,
                                      value=False,
                                      command=self.enviar_auto)
        
        self.manual.grid(column=1, row=0)
        self.manual.grid_propagate(False)
        
        self.style.configure("informacion.TFrame", background="#FFFFFF")
        self.informacion = ttk.Frame(self.info,
                                     width=400,
                                     height=300,
                                     style="informacion.TFrame")
        
        self.informacion.pack()
        self.informacion.pack_propagate(False)
        self.informacion.grid_propagate(False)
        self.informacion.grid_columnconfigure(0, weight=1)
        self.informacion.grid_columnconfigure(1, weight=1)
        for fila in range(3):
            self.informacion.grid_rowconfigure(fila, weight=1, uniform="info")
        
        self.style.configure("margen.TFrame", background="#000000")
        self.margen = ttk.Frame(self.estacion,
                                style="margen.TFrame",
                                height=184,
                                width=384)
        
        self.margen.pack(padx=8,pady=8)
        self.margen.pack_propagate(False)
        
        self.style.configure("contenedor.TFrame", background="#ffffff")
        self.contenedor = ttk.Frame(self.margen,
                                    width=380,
                                    height=180,
                                    style="contenedor.TFrame")
        
        self.contenedor.pack(padx=2, pady=2)
        self.contenedor.pack_propagate(False)
        self.contenedor.grid_propagate(False)
        self.contenedor.grid_columnconfigure(0, minsize=127)
        self.contenedor.grid_columnconfigure(1, minsize=127)
        self.contenedor.grid_columnconfigure(2, minsize=126)
        self.contenedor.grid_rowconfigure(0, minsize=180)
        
        self.style.configure("inicio.TFrame", background="#ffffff")
        self.inicio = ttk.Frame(self.contenedor,
                                width=127,
                                height=180,
                                style="inicio.TFrame")
        
        self.inicio.grid(column=0, row=0, sticky="nsew")
        self.inicio.grid_propagate(False)
        
        self.style.configure("inicio.TLabel", background="#ffffff", foreground="#000000", font=("Consolas", 15))
        self.labelini = ttk.Label(self.inicio,
                                  style="inicio.TLabel",
                                  text="INICIO",
                                  justify="center",
                                  anchor="center")
        self.labelini.pack(fill="both", expand=True, padx=10)
        
        self.style.configure("llenado.TFrame", background="#ffffff")
        self.llenado = ttk.Frame(self.contenedor,
                                 width=127,
                                 height=180,
                                 style="llenado.TFrame")
        
        self.llenado.grid(column=1,row=0, sticky="nsew")
        self.llenado.grid_propagate(False)
        
        self.style.configure("llenado.TLabel", background="#ffffff", foreground="#000000", font=("Consolas", 15))
        self.labelll = ttk.Label(self.llenado,
                                 style="llenado.TLabel",
                                 text="LLENADO",
                                 justify="center",
                                 anchor="center")
        
        self.labelll.pack(fill="both", expand=True, padx=10)
        
        self.style.configure("listo.TFrame", background="#ffffff")
        self.listo = ttk.Frame(self.contenedor,
                               style="listo.TFrame",
                               width=126,
                               height=180)
        
        self.listo.grid(column=2,row=0, sticky="nsew")
        self.listo.grid_propagate(False)
        
        self.style.configure("listo.TLabel", background="#ffffff", foreground="#000000", font=("Consolas", 15))
        self.labelis = ttk.Label(self.listo,
                                 style="listo.TLabel",
                                 justify="center",
                                 anchor="center",
                                 text="LISTO")
        
        self.labelis.pack(fill="both", expand=True)
        
        self.style.configure("la.TLabel", background="#ffffff", foreground="#000000", font=("Consolas", 13))
        self.l1 = ttk.Label(self.informacion,
                            text="Distancia:",
                            justify="left",
                            anchor="w",
                            style="la.TLabel")
        
        self.l1.grid(column=0, row=0, sticky="w", padx=(10, 0))
        self.l1.grid_propagate(False)
        
        self.l2 = ttk.Label(self.informacion,
                            text="ultima configuracion:",
                            justify="left",
                            anchor="w",
                            style="la.TLabel")
        
        self.l2.grid(column=0, row=1, sticky="w", padx=(10, 0))
        self.l2.grid_propagate(False)
        
        self.l3 = ttk.Label(self.informacion,
                            text="ultimo timestamp:",
                            justify="left",
                            anchor="w",
                            style="la.TLabel")
        
        self.l3.grid(column=0, row=2, sticky="w", padx=(10, 0))
        
        self.distancia = ttk.Label(self.informacion,
                                   text="OUT",
                                   justify="right",
                                   anchor="e",
                                   style="la.TLabel")
        
        self.distancia.grid(column=1, row=0, sticky="e", padx=(0, 10))
        self.distancia.grid_propagate(False)
        
        self.savelevel = ttk.Label(self.informacion,
                                   text="50ml",
                                   justify="right",
                                   anchor="e",
                                   style="la.TLabel")
        
        self.savelevel.grid(column=1, row=1, sticky="e", padx=(0, 10))
        self.savelevel.grid_propagate(False)
        
        self.timestamp = ttk.Label(self.informacion,
                                   text="00/00/00 00:00:00",
                                   justify="right",
                                   anchor="e",
                                   style="la.TLabel")
        
        self.timestamp.grid(column=1, row=2, sticky="e", padx=(0, 10))
        self.timestamp.grid_propagate(False)
        
        self.style.configure("emergencia.TButton", background="#ffffff", font=("Consolas", 15))
        self.emergencia = ttk.Button(self.emer,
                                     text="PARADA DE EMERGECIA",
                                     command=self.parada_de_emergencia,
                                     width=30,
                                     style="emergencia.TButton")
        
        self.emergencia.pack()
        self.emergencia.pack_propagate(False)
        
        ###FRAME 3 Registro
        
        self.style.configure("blanco.TFrame", background = "#ffffff")
        
        self.regedit = ttk.Frame(self.frame_registro,
                                 style="blanco.TFrame",
                                 width=400,
                                 height=50)
        self.regedit.pack()
        self.regedit.pack_propagate(False)
        
        self.aislar_registro = ttk.Frame(self.frame_registro,
                                         style="blanco.TFrame",
                                         width=400,
                                         height=650)
        
        self.aislar_registro.pack()
        self.aislar_registro.pack_propagate(False)
        
        self.l4 = ttk.Label(self.regedit,
                            style="label2.TLabel",
                            text="REGISTRO",
                            width=30,
                            justify="center",
                            anchor="center")
        
        self.l4.pack(pady=10)
        self.l4.pack_propagate(False)
        
        self.style.configure("registro.TFrame", background="#cacaca")
        self.contenedor_registro = ttk.Frame(self.aislar_registro,
                                             style="registro.TFrame",
                                             width=380,
                                             height=650)
        
        self.contenedor_registro.pack(padx=10, pady=10)
        self.contenedor_registro.pack_propagate(False)
        
        columnas = ("dis", "niv", "crc", "tp")
        self.tree = ttk.Treeview(self.contenedor_registro,
                                 columns=columnas,
                                 show="headings",
                                 height=30)
        
        self.tree.heading("dis", text="dis")
        self.tree.heading("niv", text="niv")
        self.tree.heading("crc", text="crc")
        self.tree.heading("tp", text="tp")
        
        self.tree.column("dis", width=50, anchor="center")
        self.tree.column("niv", width=50, anchor="center")
        self.tree.column("crc", width=50, anchor="center")
        self.tree.column("tp", width=250, anchor="center")
        self.tree.grid(column=0, row=0, sticky="nsew")
        
    def enviar_auto(self):
        pass
        
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
