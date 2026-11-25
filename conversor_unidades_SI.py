import math
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


CONVERSIONES = {
    "Calorías (cal) a julios (J)": (4.184, 0, "J", "J = cal × 4.184"),
    "Atmósferas (atm) a pascales (Pa)": (101325, 0, "Pa", "Pa = atm × 101325"),
    "Kilómetros por hora (km/h) a metros por segundo (m/s)": (
        1 / 3.6,
        0,
        "m/s",
        "m/s = km/h ÷ 3.6",
    ),
    "Grados Celsius (°C) a kelvin (K)": (
        1,
        273.15,
        "K",
        "K = °C + 273.15",
    ),
    "Grados Celsius (°C) a Fahrenheit (°F)": (
        9 / 5,
        32,
        "°F",
        "°F = (°C × 9/5) + 32",
    ),
}


def main():
    ventana = tk.Tk()
    ventana.title("Conversor al Sistema Internacional")
    ventana.resizable(False, False)

    color_fondo = "#90CAF9"
    color_boton = "#1565C0"
    ventana.configure(background=color_fondo)
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure("TFrame", background=color_fondo)
    estilo.configure("TLabel", background=color_fondo)
    estilo.configure("FondoApp.TFrame", background=color_fondo)
    estilo.configure("FondoApp.TLabel", background=color_fondo)
    estilo.configure("TButton", background=color_boton, foreground="white")
    estilo.configure("TEntry", fieldbackground=color_fondo)
    estilo.configure(
        "TCombobox",
        background=color_fondo,
        fieldbackground=color_fondo,
    )
    estilo.map(
        "TButton",
        background=[("active", color_boton), ("pressed", color_boton)],
        foreground=[("active", "white"), ("pressed", "white")],
    )
    estilo.map(
        "TCombobox",
        background=[("active", color_fondo), ("readonly", color_fondo)],
        fieldbackground=[("readonly", color_fondo)],
    )

    marco = ttk.Frame(ventana, padding=16, style="FondoApp.TFrame")
    marco.grid()
    marco.columnconfigure(0, weight=1)

    cuenta_atras = tk.StringVar()
    ttk.Label(
        marco,
        textvariable=cuenta_atras,
        style="FondoApp.TLabel",
    ).grid(row=0, column=0, sticky="w", pady=(0, 6))

    logo = tk.PhotoImage(file=Path(__file__).resolve().with_name("logo_unir.png"))
    factor_reduccion = max(
        1, math.ceil(max(logo.width() / 130, logo.height() / 76))
    )
    logo = logo.subsample(factor_reduccion, factor_reduccion)
    etiqueta_logo = ttk.Label(marco, image=logo, style="FondoApp.TLabel")
    etiqueta_logo.image = logo
    etiqueta_logo.grid(row=0, column=1, sticky="e", padx=(12, 0), pady=(0, 6))

    ttk.Label(marco, text="Conversión:", style="FondoApp.TLabel").grid(
        row=1, column=0, sticky="w", pady=(0, 6)
    )
    conversion = tk.StringVar(value=next(iter(CONVERSIONES)))
    menu_conversiones = ttk.Combobox(
        marco,
        textvariable=conversion,
        values=list(CONVERSIONES),
        state="readonly",
        width=48,
    )
    menu_conversiones.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))

    ttk.Label(
        marco, text="Número:", style="FondoApp.TLabel"
    ).grid(row=3, column=0, sticky="w", pady=(0, 6))
    entrada_numero = ttk.Entry(marco, width=24)
    entrada_numero.grid(row=4, column=0, sticky="ew", pady=(0, 12))
    entrada_numero.focus()

    resultado = tk.StringVar()
    ttk.Button(
        marco,
        text="Calcular",
        style="TButton",
        command=lambda: calcular(
            conversion.get(), entrada_numero.get(), resultado, formula
        ),
    ).grid(row=5, column=0, sticky="ew", pady=(0, 12))
    ttk.Label(
        marco,
        textvariable=resultado,
        wraplength=360,
        style="FondoApp.TLabel",
    ).grid(row=6, column=0, sticky="w")
    formula = tk.StringVar()
    ttk.Label(
        marco,
        textvariable=formula,
        wraplength=360,
        style="FondoApp.TLabel",
    ).grid(row=7, column=0, sticky="w", pady=(6, 0))

    ventana.bind(
        "<Return>",
        lambda _evento: calcular(
            conversion.get(), entrada_numero.get(), resultado, formula
        ),
    )

    def actualizar_cuenta_atras(segundos):
        cuenta_atras.set(f"Cierre en: {segundos} s")
        if segundos == 0:
            ventana.destroy()
        else:
            ventana.after(1000, actualizar_cuenta_atras, segundos - 1)

    actualizar_cuenta_atras(10)
    ventana.mainloop()


def calcular(conversion, texto_numero, resultado, formula):
    try:
        numero = float(texto_numero.strip().replace(",", "."))
        if not math.isfinite(numero):
            raise ValueError
    except ValueError:
        messagebox.showerror("Número no válido", "Escribe un número válido.")
        return

    factor, desplazamiento, unidad_resultado, regla = CONVERSIONES[conversion]
    valor_convertido = numero * factor + desplazamiento
    resultado.set(f"Resultado: {valor_convertido:.10g} {unidad_resultado}")
    formula.set(f"Fórmula: {regla}")


if __name__ == "__main__":
    main()