import customtkinter as ctk

# Configuración de apariencia
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Crear ventana principal
app = ctk.CTk()
app.title("Mi Despensa")
app.geometry("900x600")

# Título
titulo = ctk.CTkLabel(
    app,
    text="MI DESPENSA",
    font=("Arial", 28, "bold")
)
titulo.pack(pady=30)

# Mantener la ventana abierta
app.mainloop()