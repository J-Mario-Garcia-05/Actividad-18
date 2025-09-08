import tkinter as tk
from tkinter import messagebox

class Participante:
    def __init__(self, nombre, institucion):
        self._nombre = nombre
        self._institucion = institucion

    def mostrar_info(self):
        return f"{self._nombre} - {self._institucion}"


class BandaEscolar(Participante):
    categorias_validas = ["Primaria", "Básico", "Diversificado"]
    criterios_validos = ["ritmo", "uniformidad", "coreografía", "alineación", "puntualidad"]

    def __init__(self, nombre, institucion, categoria):
        super().__init__(nombre, institucion)
        self._categoria = None
        self._puntajes = {}
        self.set_categoria(categoria)

    def set_categoria(self, categoria):
        if categoria not in BandaEscolar.categorias_validas:
            raise ValueError(f"Categoría inválida: {categoria}")
        self._categoria = categoria

    def registrar_puntajes(self, puntajes):
        if set(puntajes.keys()) != set(BandaEscolar.criterios_validos):
            raise ValueError("Faltan o sobran criterios de evaluación.")
        for criterio, valor in puntajes.items():
            if not (0 <= valor <= 10):
                raise ValueError(f"Puntaje inválido en {criterio}: {valor}")
        self._puntajes = puntajes

    @property
    def total(self):
        return sum(self._puntajes.values()) if self._puntajes else 0

    def mostrar_info(self):
        info = f"{self._nombre} - {self._institucion} ({self._categoria})"
        if self._puntajes:
            info += f" | Total: {self.total}"
        return info


class Concurso:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
        self._bandas = {}

    def inscribir_banda(self, banda):
        if banda._nombre in self._bandas:
            raise ValueError(f"La banda '{banda._nombre}' ya está inscrita.")
        self._bandas[banda._nombre] = banda

    def registrar_evaluacion(self, nombre_banda, puntajes):
        if nombre_banda not in self._bandas:
            raise ValueError(f"No existe la banda {nombre_banda}")
        self._bandas[nombre_banda].registrar_puntajes(puntajes)

    def listar_bandas(self):
        return [banda.mostrar_info() for banda in self._bandas.values()]

    def ranking(self):
        bandas_ordenadas = sorted(
            self._bandas.values(),
            key=lambda b: b.total,
            reverse=True
        )
        return bandas_ordenadas

    def guardar_en_archivo(self, archivo):
        with open(archivo, "w", encoding="utf-8") as f:
            for banda in self._bandas.values():
                linea = f"{banda._nombre}|{banda._institucion}|{banda._categoria}"
                if banda._puntajes:
                    puntajes_str = ",".join(f"{k}:{v}" for k, v in banda._puntajes.items())
                    linea += f"|{puntajes_str}"
                f.write(linea + "\n")

    def cargar_desde_archivo(self, archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split("|")
                    nombre, institucion, categoria = partes[:3]
                    banda = BandaEscolar(nombre, institucion, categoria)

                    if len(partes) == 4:  # tiene puntajes
                        puntajes = {}
                        for item in partes[3].split(","):
                            crit, val = item.split(":")
                            puntajes[crit] = int(val)
                        banda.registrar_puntajes(puntajes)

                    self.inscribir_banda(banda)
        except FileNotFoundError:
            print(f"⚠ Archivo {archivo} no encontrado, iniciando concurso vacío.")


class ConcursoBandasApp:
    ARCHIVO_AUTOSAVE = "bandas.txt"

    def centrar_ventana(self, ventana, ancho, alto):
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = int((pantalla_ancho - ancho) / 2)
        y = int((pantalla_alto - alto) / 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def __init__(self):
        self.concurso = Concurso("Concurso de Bandas - Quetzaltenango", "2025-09-14")
        self.concurso.cargar_desde_archivo(self.ARCHIVO_AUTOSAVE)

        self.ventana = tk.Tk()
        self.ventana.iconbitmap("Festival de bandas.ico")
        self.ventana.title("Concurso de Bandas - Quetzaltenango")
        self.ventana.geometry("600x350")
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir_guardando)

        self.menu()

        tk.Label(
            self.ventana,
            text="Sistema de Inscripción y Evaluación de Bandas Escolares\nConcurso 14 de Septiembre - Quetzaltenango",
            font=("Arial", 12, "bold"),
            justify="center"
        ).pack(pady=50)

        self.centrar_ventana(self.ventana, 500, 300)

        self.ventana.mainloop()

    def menu(self):
        barra = tk.Menu(self.ventana)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Inscribir Banda", command=self.inscribir_banda)
        opciones.add_command(label="Registrar Evaluación", command=self.registrar_evaluacion)
        opciones.add_command(label="Listar Bandas", command=self.listar_bandas)
        opciones.add_command(label="Ver Ranking", command=self.ver_ranking)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.salir_guardando)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.ventana.config(menu=barra)

    def inscribir_banda(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.iconbitmap("Festival de bandas.ico")
        ventana.title("Inscribir Banda")
        self.centrar_ventana(ventana, 400, 300)

        tk.Label(ventana, text="Nombre de la Banda:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack(pady=5)

        tk.Label(ventana, text="Institución:").pack(pady=5)
        entry_institucion = tk.Entry(ventana)
        entry_institucion.pack(pady=5)

        tk.Label(ventana, text="Categoría:").pack(pady=5)
        categoria_var = tk.StringVar(value="Primaria")
        tk.OptionMenu(ventana, categoria_var, *BandaEscolar.categorias_validas).pack(pady=5)

        def guardar_banda():
            try:
                banda = BandaEscolar(entry_nombre.get(), entry_institucion.get(), categoria_var.get())
                self.concurso.inscribir_banda(banda)
                messagebox.showinfo("Éxito", "Banda inscrita correctamente.")
                ventana.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar", command=guardar_banda).pack(pady=10)

    def registrar_evaluacion(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.iconbitmap("Festival de bandas.ico")
        ventana.title("Registrar Evaluación")
        self.centrar_ventana(ventana, 400, 400)

        tk.Label(ventana, text="Seleccionar Banda:").pack(pady=5)
        nombres = list(self.concurso._bandas.keys())
        if not nombres:
            tk.Label(ventana, text="No hay bandas inscritas.").pack(pady=20)
            return

        banda_var = tk.StringVar(value=nombres[0])
        tk.OptionMenu(ventana, banda_var, *nombres).pack(pady=5)

        entradas = {}
        for crit in BandaEscolar.criterios_validos:
            tk.Label(ventana, text=f"{crit.capitalize()}:").pack(pady=2)
            e = tk.Entry(ventana)
            e.pack(pady=2)
            entradas[crit] = e

        def guardar_puntajes():
            try:
                puntajes = {c: int(e.get()) for c, e in entradas.items()}
                self.concurso.registrar_evaluacion(banda_var.get(), puntajes)
                messagebox.showinfo("Éxito", "Evaluación registrada.")
                ventana.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar Evaluación", command=guardar_puntajes).pack(pady=10)

    def listar_bandas(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.iconbitmap("Festival de bandas.ico")
        ventana.title("Listado de Bandas")
        self.centrar_ventana(ventana, 400, 300)

        bandas = self.concurso.listar_bandas()
        if not bandas:
            tk.Label(ventana, text="No hay bandas inscritas.").pack(pady=20)
        else:
            for b in bandas:
                tk.Label(ventana, text=b).pack(anchor="w", padx=10, pady=2)

    def ver_ranking(self):
        ventana = tk.Toplevel(self.ventana)

        ventana.title("Ranking Final")
        self.centrar_ventana(ventana, 450, 350)

        bandas = self.concurso.ranking()
        if not bandas:
            tk.Label(ventana, text="No hay evaluaciones registradas.").pack(pady=20)
        else:
            tk.Label(ventana, text="Posición | Banda - Institución (Categoría) | Total",
                     font=("Arial", 10, "bold")).pack(pady=10)
            for pos, banda in enumerate(bandas, start=1):
                tk.Label(ventana,
                         text=f"{pos}. {banda._nombre} - {banda._institucion} ({banda._categoria}) | {banda.total}"
                         ).pack(anchor="w", padx=10, pady=2)

    # Guardado automático al salir
    def salir_guardando(self):
        self.concurso.guardar_en_archivo(self.ARCHIVO_AUTOSAVE)
        self.ventana.destroy()


if __name__ == "__main__":
    ConcursoBandasApp()
