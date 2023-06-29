import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import scipy.integrate as spi


class MonteCarloIntegrationGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Monte Carlo Integration")
        self.window.geometry("600x400")

        self.results_shown = False  # Variable para verificar si los resultados se han mostrado

        self.create_widgets()

    def create_widgets(self):
        # Etiqueta y entrada para el número de simulaciones
        simulations_label = ttk.Label(self.window, text="Número de simulaciones:")
        simulations_label.pack(pady=10)
        self.simulations_entry = ttk.Entry(self.window)
        self.simulations_entry.pack()

        # Configurar validación para permitir solo datos numéricos enteros
        vcmd = (self.window.register(self.validate_input), '%P')
        self.simulations_entry.config(validate="key", validatecommand=vcmd)

        # Asociar la tecla de acceso rápido para borrar todos los datos del campo
        self.simulations_entry.bind("<Delete>", self.clear_entry)

        # Crear un marco para contener los botones
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)

        # Crear botón para mostrar los resultados
        show_button = ttk.Button(button_frame, text="Mostrar resultados", command=self.show_results)
        show_button.pack(side="left", padx=5)

        # Crear botón para limpiar la información
        clear_button = ttk.Button(button_frame, text="Limpiar", command=self.clear_results)
        clear_button.pack(side="left", padx=5)

        # Crear área de texto para los resultados
        self.results_text = tk.Text(self.window, height=12, width=70, font=("Arial", 12))
        self.results_text.pack(padx=10, pady=10)

        # Deshabilitar la edición del área de texto de resultados
        self.results_text.configure(state='disabled')

    def validate_input(self, value):
    # Validar que el valor sea un número entero o esté vacío
        if value.strip() == "":
            return True
        try:
            num = int(value)
            if num == 0:
                return False
            elif num < 0:
                messagebox.showerror("Error", "No se deben ingresar números negativos.")
                return False
            return True
        except ValueError:
            return False
        
    def clear_entry(self, event):
        # Borrar todos los datos del campo de entrada
        self.simulations_entry.delete(0, tk.END)

    def monte_carlo_integration(self, num_simulations):
        lower_limit = 2
        upper_limit = 3
        sum_fx = 0

        # Realizar las simulaciones
        for _ in range(num_simulations):
            x = random.uniform(lower_limit, upper_limit)
            fx = 3 * x**2 + 2 * x
            sum_fx += fx

        # Calcular la aproximación de la integral
        integral_approximation = (upper_limit - lower_limit) * sum_fx / num_simulations
        real_integral = 24

        # Resolver la integral usando el método numérico
        result, _ = spi.quad(lambda x: 3*x**2 + 2*x, lower_limit, upper_limit)
        real_integral = result

        # Calcular el porcentaje de error
        error_percentage = (real_integral - integral_approximation) / real_integral * 100

        return real_integral, integral_approximation, error_percentage

    def show_results(self):
        num_simulations = self.simulations_entry.get()

        # Verificar si el campo de entrada está vacío o es 0
        if num_simulations == "" or num_simulations == "0":
            messagebox.showwarning("Campo vacío", "Por favor, ingrese un número de simulaciones.")
            return
        
        num_simulations = int(num_simulations)

        real_integral, integral_approximation, error_percentage = self.monte_carlo_integration(num_simulations)

        # Habilitar la edición del área de texto de resultados
        self.results_text.configure(state='normal')

        # Borrar los resultados anteriores
        self.results_text.delete('1.0', tk.END)

        # Insertar los nuevos resultados
        self.results_text.insert(tk.END, "\t\t\t      Resultados:")
        self.results_text.insert(tk.END, "\n\n")
        self.results_text.insert(tk.END, "Resultado Matemático de la integral: \n")
        self.results_text.insert(tk.END, "  {}\n".format(real_integral), "bold")
        self.results_text.insert(tk.END, "Resultado Aproximado de la Integral por el método de Monte Carlo: \n")
        self.results_text.insert(tk.END, "  {}\n".format(integral_approximation), "bold")
        self.results_text.insert(tk.END, "Porcentaje (%) de error: \n")
        self.results_text.insert(tk.END, "  {}%\n".format(error_percentage), "bold")
        self.results_text.insert(tk.END, "Cantidad de Simulaciones: \n")
        self.results_text.insert(tk.END, "  {}\n".format(num_simulations), "bold")

        # Deshabilitar la edición del área de texto de resultados
        self.results_text.configure(state='disabled')

        # Aplicar etiquetas de formato
        self.results_text.tag_configure("bold", font=("Arial", 12, "bold"))

        self.results_shown = True  # Indicar que los resultados se han mostrado

    def clear_results(self):
        # Verificar si los resultados ya se han mostrado
        if self.results_shown:

            # Limpiar el campo de entrada de simulaciones
            self.simulations_entry.delete(0, tk.END)

            # Habilitar la edición del área de texto de resultados
            self.results_text.configure(state='normal')

            # Borrar los resultados anteriores
            self.results_text.delete('1.0', tk.END)

            # Deshabilitar la edición del área de texto de resultados
            self.results_text.configure(state='disabled')


        else:
            messagebox.showinfo("Limpiar", "El botón Limpiar se utiliza para reiniciar los datos, por favor oprima primero el botón Mostrar resultados.")


# Crear la ventana para la interfaz gráfica
window = tk.Tk()
window.style = ttk.Style()
window.style.theme_use("clam")

app = MonteCarloIntegrationGUI(window)
# Iniciar el ciclo de eventos de la interfaz gráfica
window.mainloop()
