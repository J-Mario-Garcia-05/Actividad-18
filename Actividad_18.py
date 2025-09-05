import tkinter as tk

class Participante:
    def __init__(self, nombre, institucion, categoria):
        self.nombre = nombre
        self.institucion = institucion
        self.__categoria = categoria

    def mostrar_info(self):
        return f'Nombre de la banda: {self.nombre}\t| Institución: {self.institucion}\t| Categoría: {self.__categoria}'

class BandaEscolar(Participante):
    def __init__(self, nombre, institucion, categoria):
        super().__init__(nombre, institucion, categoria)
        self.nombre = nombre
        self.institucion = institucion
        self.__categoria = categoria
        self.__puntaje = {
            "ritmo": 0,
            "uniformidad": 0,
            "coreografia": 0,
            "alineacion": 0,
            "puntualidad": 0
        }

    @property
    def categoria(self):
        return self.__categoria
    @categoria.setter
    def categoria(self, value):
        if value.lower() in ["primaria", "básico", "diversificado"]:
            self.__categoria = value
        else:
            raise ValueError("Categoria no disponible")

    @property
    def puntaje(self):
        return self.__puntaje
    @puntaje.setter
    def puntaje(self, value):
        if 0 <= value <= 10:
            self.__puntaje = value
        else:
            raise ValueError("Puntaje fuera de rango")

class ConcursoBandasApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Concurso de Bandas - Quetzaltenango")
        self.ventana.geometry("500x300")

        self.menu()

        tk.Label(
            self.ventana,
            text="Sistema de Inscripción y Evaluación de Bandas Escolares\nConcurso 14 de Septiembre - Quetzaltenango",
            font=("Arial", 12, "bold"),
            justify="center"
        ).grid(pady=50)

        self.ventana.mainloop()

    def menu(self):
        barra = tk.Menu(self.ventana)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Inscribir Banda", command=self.inscribir_banda)
        opciones.add_command(label="Registrar Evaluación", command=self.registrar_evaluacion)
        opciones.add_command(label="Listar Bandas", command=self.listar_bandas)
        opciones.add_command(label="Ver Ranking", command=self.ver_ranking)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.ventana.config(menu=barra)

    def inscribir_banda(self):
        ventana_inscripcion = tk.Toplevel(self.ventana).title("Inscribir Banda")
        pedir_nombre = tk.Label(ventana_inscripcion, text="Nombre de la banda", font=("Arial", 15, "bold"))
        pedir_nombre.grid(row=0, column=0, padx=5, pady=5)
        nombre = tk.Entry(ventana_inscripcion, font=("Arial", 15, "bold"))
        nombre.grid(row=1, column=0, padx=5, pady=5)

    def registrar_evaluacion(self):
        print("Se abrió la ventana: Registrar Evaluación")
        tk.Toplevel(self.ventana).title("Registrar Evaluación")

    def listar_bandas(self):
        print("Se abrió la ventana: Listado de Bandas")
        tk.Toplevel(self.ventana).title("Listado de Bandas")

    def ver_ranking(self):
        print("Se abrió la ventana: Ranking Final")
        tk.Toplevel(self.ventana).title("Ranking Final")


if __name__ == "__main__":
    ConcursoBandasApp()