import tkinter as tk
import random

ANCHO, ALTO = 800, 500
ANCHO_TABLERO, ALTO_TABLERO = 600, 400
FILAS, COLUMNAS = 5, 8
TAM_CASILLA_X = ANCHO_TABLERO // COLUMNAS
TAM_CASILLA_Y = ALTO_TABLERO // FILAS

class TorresWars:
    def __init__(self, root):
        self.root = root
        self.root.title(" Bienvenido a TORRES WAR")
        self.root.resizable(False, False)

        # Monedas y Mejoras (Se define mejora_monedas para corregir el error)
        self.monedas = 300
        self.mejora_daño = 0
        self.mejora_monedas = 0

        # Costos de mejoras
        self.costo_mejora_daño = 150
        self.costo_mejora_monedas = 100

        # Precios de Estructuras
        self.COSTO_Ganancia = 50
        self.COSTO_torreta = 100

        self.crear_pantalla_bienvenida()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- PANTALLA MENU ---
    def crear_pantalla_bienvenida(self):
        self.limpiar_pantalla()
        frame = tk.Frame(self.root, bg="#113856", width=ANCHO, height=ALTO)
        frame.pack_propagate(False)
        frame.pack()

        tk.Label(
            frame, text="TORRES WAR", 
            font=("Impact", 36), fg="#ffffff", bg="#1f6ef6"
        ).pack(pady=40)

        tk.Label(
            frame, text="Defiende Tu Territorio - creado por Julio Ixcoteyac", 
            font=("Arial", 14), fg="white", bg="#1e272e"
        ).pack(pady=10)

        tk.Button(
            frame, text="JUGAR", font=("Arial", 18, "bold"), 
            bg="#4cd137", fg="white", width=15, command=self.iniciar_juego
        ).pack(pady=15)

        tk.Button(
            frame, text="MEJORAS", font=("Arial", 16, "bold"), 
            bg="#4de20d", fg="white", width=15, command=self.crear_pantalla_mejoras
        ).pack(pady=10)

    def crear_pantalla_mejoras(self):
        self.limpiar_pantalla()
        self.frame_tienda = tk.Frame(self.root, bg="#2c5185", width=ANCHO, height=ALTO)
        self.frame_tienda.pack_propagate(False)
        self.frame_tienda.pack()

        tk.Label(
            self.frame_tienda, text="TIENDA DE MEJORAS", 
            font=("Impact", 28), fg="#e1b12c", bg="#2c5185"
        ).pack(pady=20)

        self.lbl_monedas_tienda = tk.Label(
            self.frame_tienda, text=f"Monedas Disponibles: {self.monedas}", 
            font=("Arial", 16, "bold"), fg="#fbc531", bg="#2c5185"
        )
        self.lbl_monedas_tienda.pack(pady=10)

        self.btn_mejora1 = tk.Button(
            self.frame_tienda, 
            text=f"Aumentar Dano de Proyectil (Nivel {self.mejora_daño})\nCosto: {self.costo_mejora_daño} monedas", 
            font=("Arial", 12), bg="#44bd32", fg="white", width=40,
            command=self.comprar_daño
        )
        self.btn_mejora1.pack(pady=15)

        self.btn_mejora2 = tk.Button(
            self.frame_tienda, 
            text=f"Monedas Iniciales +25 (Nivel {self.mejora_monedas})\nCosto: {self.costo_mejora_monedas} monedas", 
            font=("Arial", 12), bg="#00a8ff", fg="white", width=40,
            command=self.comprar_monedas
        )
        self.btn_mejora2.pack(pady=15)

        tk.Button(
            self.frame_tienda, text="VOLVER AL MENU", font=("Arial", 12, "bold"), 
            bg="#e84118", fg="white", command=self.crear_pantalla_bienvenida
        ).pack(pady=20)

    def comprar_daño(self):
        if self.monedas >= self.costo_mejora_daño:
            self.monedas -= self.costo_mejora_daño
            self.mejora_daño += 1
            self.costo_mejora_daño += 50
            self.actualizar_tienda()

    def comprar_monedas(self):
        if self.monedas >= self.costo_mejora_monedas:
            self.monedas -= self.costo_mejora_monedas
            self.mejora_monedas += 1
            self.costo_mejora_monedas += 40
            self.actualizar_tienda()

    def actualizar_tienda(self):
        self.lbl_monedas_tienda.config(text=f"Monedas Disponibles: {self.monedas}")
        self.btn_mejora1.config(text=f"Aumentar Dano de Proyectil (Nivel {self.mejora_daño})\nCosto: {self.costo_mejora_daño} monedas")
        self.btn_mejora2.config(text=f"Monedas Iniciales +25 (Nivel {self.mejora_monedas})\nCosto: {self.costo_mejora_monedas} monedas")

    # --- LOGICA DEL JUEGO ---
    def iniciar_juego(self):
        self.limpiar_pantalla()
        
        self.monedas = 200 + (self.mejora_monedas * 25)
        self.torre_seleccionada = None
        self.juego_activo = True

        self.torre = []
        self.soldado = []
        self.proyectiles = []

        self.canvas = tk.Canvas(self.root, width=ANCHO, height=ALTO, bg="#4E2EA4")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click_canvas)

        self.spawn_timer = 0
        self.moneda_timer = 0
        self.bucle_juego()

    def on_click_canvas(self, event):
        x, y = event.x, event.y

        # Panel Superior
        if y < 60:
            if 200 <= x <= 320:
                self.torre_seleccionada = "generador"
            elif 330 <= x <= 450:
                self.torre_seleccionada = "torreta"
            elif 700 <= x <= 780:
                self.juego_activo = False
                self.crear_pantalla_bienvenida()
            return

        # Tablero de Juego
        if 60 <= y <= 60 + ALTO_TABLERO and x <= ANCHO_TABLERO:
            fila = (y - 60) // TAM_CASILLA_Y
            col = x // TAM_CASILLA_X

            for p in self.torre:
                if p["fila"] == fila and p["col"] == col:
                    return

            if self.torre_seleccionada == "generador" and self.monedas >= self.COSTO_Ganancia:
                self.monedas -= self.COSTO_Ganancia
                self.torre.append({"tipo": "generador", "fila": fila, "col": col, "hp": 100, "cooldown": 0})
            elif self.torre_seleccionada == "torreta" and self.monedas >= self.COSTO_torreta:
                self.monedas -= self.COSTO_torreta
                self.torre.append({"tipo": "torreta", "fila": fila, "col": col, "hp": 100, "cooldown": 0})

            self.torre_seleccionada = None

    def bucle_juego(self):
        if not self.juego_activo:
            return

        self.actualizar_estado()
        self.dibujar_juego()
        self.root.after(50, self.bucle_juego)

    def actualizar_estado(self):
        self.moneda_timer += 1
        if self.moneda_timer >= 100:
            self.monedas += 25
            self.moneda_timer = 0

# Aparecer Soldados
        self.spawn_timer += 1
        tiempo_espera = max(
            30, 120 - (self.moneda_timer // 10)
        )  # Nunca baja de 30 frames

        if self.spawn_timer >= tiempo_espera:
            fila = random.randint(0, FILAS - 1)
            self.soldado.append(
                {"x": ANCHO_TABLERO, "fila": fila, "hp": 100, "vx": 1.5}
            )
            self.spawn_timer = 0

        for p in self.torre:
            if p["tipo"] == "generador":
                p["cooldown"] += 1
                if p["cooldown"] >= 150:
                    self.monedas += 25
                    p["cooldown"] = 0
            elif p["tipo"] == "torreta":
                p["cooldown"] += 1
                soldado_en_fila = [z for z in self.soldado if z["fila"] == p["fila"] and z["x"] > p["col"] * TAM_CASILLA_X]
                if p["cooldown"] >= 40 and soldado_en_fila:
                    px = (p["col"] * TAM_CASILLA_X) + TAM_CASILLA_X
                    py = 60 + (p["fila"] * TAM_CASILLA_Y) + (TAM_CASILLA_Y // 2)
                    daño_total = 20 + (self.mejora_daño * 10)
                    self.proyectiles.append({"x": px, "y": py, "fila": p["fila"], "daño": daño_total})
                    p["cooldown"] = 0

        for pr in self.proyectiles[:]:
            pr["x"] += 7
            if pr["x"] > ANCHO_TABLERO:
                self.proyectiles.remove(pr)
                continue

            for z in self.soldado:
                if z["fila"] == pr["fila"] and abs(z["x"] - pr["x"]) < 15:
                    z["hp"] -= pr["daño"]
                    if pr in self.proyectiles:
                        self.proyectiles.remove(pr)
                    break

        for z in self.soldado[:]:
            if z["hp"] <= 0:
                self.soldado.remove(z)
                self.monedas += 15
                continue

            comiendo = False
            for p in self.torre[:]:
                px = p["col"] * TAM_CASILLA_X
                if p["fila"] == z["fila"] and abs(z["x"] - px) < 20:
                    comiendo = True
                    p["hp"] -= 1
                    if p["hp"] <= 0:
                        self.torre.remove(p)
                    break

            if not comiendo:
                z["x"] -= z["vx"]

            if z["x"] <= 0:
                self.juego_activo = False
                self.canvas.create_text(ANCHO//2, ALTO//2, text="¡LOS SOLDADOS VENCIERON TU BASE!", font=("Impact", 24), fill="red")
                self.root.after(3000, self.crear_pantalla_bienvenida)

    def dibujar_juego(self):
        self.canvas.delete("all")

        # Tablero
        for i in range(FILAS + 1):
            self.canvas.create_line(0, 60 + i * TAM_CASILLA_Y, ANCHO_TABLERO, 60 + i * TAM_CASILLA_Y, fill="#2ecc71", width=2)
        for j in range(COLUMNAS + 1):
            self.canvas.create_line(j * TAM_CASILLA_X, 60, j * TAM_CASILLA_X, 60 + ALTO_TABLERO, fill="#2ecc71", width=2)

        # UI Superior
        self.canvas.create_rectangle(0, 0, ANCHO, 60, fill="#1e272e")
        self.canvas.create_text(90, 30, text=f"MONEDAS: {self.monedas}", font=("Arial", 14, "bold"), fill="#fbc531")

        # Botones de Selección
        color_generador = "#f1c40f" if self.torre_seleccionada == "generador" else "#34495e"
        self.canvas.create_rectangle(200, 5, 320, 55, fill=color_generador, outline="white")
        self.canvas.create_text(260, 30, text="Generador\n(50)", font=("Arial", 10, "bold"), fill="white")

        color_torreta = "#260743" if self.torre_seleccionada == "torreta" else "#34495e"
        self.canvas.create_rectangle(330, 5, 450, 55, fill=color_torreta, outline="white")
        self.canvas.create_text(390, 30, text="Torreta\n(100)", font=("Arial", 10, "bold"), fill="white")

        self.canvas.create_rectangle(700, 10, 780, 50, fill="#e74016")
        self.canvas.create_text(740, 30, text="Menu", font=("Arial", 12, "bold"), fill="white")

        # Dibujar torres
        for p in self.torre:
            cx = (p["col"] * TAM_CASILLA_X) + (TAM_CASILLA_X // 2)
            cy = 60 + (p["fila"] * TAM_CASILLA_Y) + (TAM_CASILLA_Y // 2)
            if p["tipo"] == "generador":
                self.canvas.create_oval(cx-20, cy-20, cx+20, cy+20, fill="#f1c40f", outline="orange", width=2)
            else:
                self.canvas.create_oval(cx-20, cy-20, cx+20, cy+20, fill="#03010C", outline="black", width=2)

        # Dibujar Proyectiles
        for pr in self.proyectiles:
            self.canvas.create_oval(pr["x"]-6, pr["y"]-6, pr["x"]+6, pr["y"]+6, fill="#e4190e")

        # Dibujar soldado
        for z in self.soldado:
            zy = 60 + (z["fila"] * TAM_CASILLA_Y) + (TAM_CASILLA_Y // 2)
            self.canvas.create_rectangle(z["x"]-15, zy-25, z["x"]+15, zy+25, fill="#3daeb7", outline="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = TorresWars(root)
    root.mainloop()