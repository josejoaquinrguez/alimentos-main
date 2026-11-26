
import customtkinter as ctk
import sys
import os

ruta_principal = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(ruta_principal)

import main

# Configuración de apariencia
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Ventana principal
app = ctk.CTk()
app.title("Mi Despensa")
app.geometry("1100x700")
app.minsize(900, 600)

# Distribución principal
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Menú lateral
menu = ctk.CTkFrame(app, width=220, corner_radius=0)
menu.grid(row=0, column=0, sticky="nsew")
menu.grid_propagate(False)

# Zona de contenido
contenido = ctk.CTkFrame(app, corner_radius=0)
contenido.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
contenido.grid_columnconfigure(0, weight=1)


# Función para cambiar de sección

def mostrar_seccion(seccion):

    # Limpiar el contenido anterior
    for elemento in contenido.winfo_children():
        elemento.destroy()

    # APARTADO INICIO
    if seccion == "Inicio":

        despensa = main.cargar_despensa()

        titulo_seccion = ctk.CTkLabel(
            contenido,
            text="Resumen de tu despensa",
            font=("Arial", 28, "bold")
        )
        titulo_seccion.pack(pady=(40, 20))

        tarjeta = ctk.CTkFrame(contenido)
        tarjeta.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(
            tarjeta,
            text="Productos diferentes",
            font=("Arial", 18)
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            tarjeta,
            text=str(len(despensa)),
            font=("Arial", 32, "bold")
        ).pack(pady=(0, 15))

        ctk.CTkLabel(
            contenido,
            text="Inventario actual",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 10))

        for nombre, cantidad in despensa.items():

            fila = ctk.CTkFrame(contenido)
            fila.pack(fill="x", padx=30, pady=4)

            ctk.CTkLabel(
                fila,
                text=nombre,
                font=("Arial", 16)
            ).pack(side="left", padx=20, pady=10)

            ctk.CTkLabel(
                fila,
                text=f"Cantidad: {cantidad}",
                font=("Arial", 16)
            ).pack(side="right", padx=20, pady=10)

    # APARTADO AÑADIR PRODUCTO
    elif seccion == "Añadir producto":

        titulo = ctk.CTkLabel(
            contenido,
            text="Añadir producto",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=(40, 30))

        formulario = ctk.CTkFrame(contenido)
        formulario.pack(padx=40, pady=10, fill="x")

        # Nombre
        ctk.CTkLabel(
            formulario,
            text="Nombre del producto"
        ).pack(anchor="w", padx=20, pady=(20, 5))

        entrada_nombre = ctk.CTkEntry(
            formulario,
            placeholder_text="Ej. Leche"
        )
        entrada_nombre.pack(fill="x", padx=20, pady=5)

        # Cantidad
        ctk.CTkLabel(
            formulario,
            text="Cantidad"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        entrada_cantidad = ctk.CTkEntry(
            formulario,
            placeholder_text="Ej. 3"
        )
        entrada_cantidad.pack(fill="x", padx=20, pady=5)

        # Categoría
        ctk.CTkLabel(
            formulario,
            text="Categoría"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        selector_categoria = ctk.CTkOptionMenu(
            formulario,
            values=[
                "Seleccionar categoría",
                "Comida",
                "Bebida",
                "Limpieza",
                "Higiene"
            ]
        )
        selector_categoria.pack(anchor="w", padx=20, pady=5)

        # Mensaje de información
        mensaje = ctk.CTkLabel(
            formulario,
            text=""
        )
        mensaje.pack(pady=10)

        # Función para guardar el producto
        def guardar_producto():

            producto = entrada_nombre.get().strip()
            cantidad_texto = entrada_cantidad.get().strip()

            if not producto:
                mensaje.configure(
                    text="Debes escribir un producto.",
                    text_color="red"
                )
                return

            try:
                cantidad = int(cantidad_texto)
            except ValueError:
                mensaje.configure(
                    text="Introduce una cantidad válida.",
                    text_color="red"
                )
                return

            if cantidad <= 0:
                mensaje.configure(
                    text="La cantidad debe ser mayor que cero.",
                    text_color="red"
                )
                return

            despensa = main.cargar_despensa()
            categorias = main.cargar_categorias()

            # Buscar si el producto ya existe
            existente = main.buscar_producto(despensa, producto)

            if existente:
                producto = existente

            # Comprobar si ya tiene categoría
            categoria_existente = main.buscar_producto(
                categorias, producto
            )

            categoria_seleccionada = selector_categoria.get()

            if categoria_seleccionada != "Seleccionar categoría":
                categoria = categoria_seleccionada

            elif categoria_existente:
                categoria = categorias[categoria_existente]

            else:
                categoria = main.detectar_categoria(producto)

            if not categoria:
                mensaje.configure(
                    text="Selecciona una categoría.",
                    text_color="red"
                )
                return

            # Actualizar inventario
            if producto in despensa:
                despensa[producto] += cantidad
            else:
                despensa[producto] = cantidad

            # Guardar datos
            categorias[producto] = categoria

            main.guardar_despensa(despensa)
            main.guardar_categorias(categorias)

            mensaje.configure(
                text=f"{producto} añadido correctamente.",
                text_color="green"
            )

            entrada_nombre.delete(0, "end")
            entrada_cantidad.delete(0, "end")
            selector_categoria.set("Seleccionar categoría")

        # Botón guardar
        boton_guardar = ctk.CTkButton(
            formulario,
            text="Añadir producto",
            height=40,
            command=guardar_producto
        )
        boton_guardar.pack(pady=(10, 25))

    # RESTO DE APARTADOS
    else:

        titulo_seccion = ctk.CTkLabel(
            contenido,
            text=seccion,
            font=("Arial", 28, "bold")
        )
        titulo_seccion.pack(pady=(60, 20))

        descripcion = ctk.CTkLabel(
            contenido,
            text=f"Bienvenido al apartado: {seccion}",
            font=("Arial", 16)
        )
        descripcion.pack()



# Título del menú
titulo = ctk.CTkLabel(
    menu,
    text="MI DESPENSA",
    font=("Arial", 24, "bold")
)
titulo.pack(pady=(30, 40))

# Opciones del menú
opciones = [
    "Inicio",
    "Ver productos",
    "Añadir producto",
    "Consumir producto",
    "Lista de compra",
    "Reposición",
    "Categorías"
]

# Crear botones
for opcion in opciones:

    boton = ctk.CTkButton(
        menu,
        text=opcion,
        height=40,
        command=lambda seccion=opcion: mostrar_seccion(seccion)
    )

    boton.pack(fill="x", padx=15, pady=6)


# Mostrar inicio al abrir la aplicación
mostrar_seccion("Inicio")

# Ejecutar aplicación
app.mainloop()
