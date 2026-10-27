import json
import os

ARCHIVO = "despensa.json"
ARCHIVO_LISTA = "lista_compra.json"
ARCHIVO_CATEGORIAS = "categorias.json"

def buscar_producto(diccionario, nombre):
    nombre = nombre.strip().casefold()

    for producto in diccionario:
        if producto.strip().casefold() == nombre:
            return producto

    return None


def cargar_categorias():
    try:
        with open(ARCHIVO_CATEGORIAS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}


def guardar_categorias(categorias):
    with open(ARCHIVO_CATEGORIAS, "w", encoding="utf-8") as archivo:
        json.dump(categorias, archivo, ensure_ascii=False, indent=4)


def detectar_categoria(nombre):
    nombre = nombre.strip().casefold()

    palabras_bebida = [
        "agua", "leche", "zumo", "jugo", "refresco",
        "cerveza", "vino", "bebida", "batido"
    ]

    palabras_limpieza = [
        "detergente", "lejia", "lejía", "lavavajillas",
        "limpiador", "limpieza", "suavizante", "fregasuelos",
        "desinfectante", "quitagrasas", "limpiacristales"
    ]

    for palabra in palabras_bebida:
        if palabra in nombre:
            return "Bebida"

    for palabra in palabras_limpieza:
        if palabra in nombre:
            return "Limpieza"

    return None


def elegir_categoria(producto, categorias):
    existente = buscar_producto(categorias, producto)

    if existente is not None:
        categoria_actual = categorias[existente]
        print(f"Categoría guardada: {categoria_actual}")
        respuesta = input(
            "¿Quieres mantenerla? (s/n): "
        ).strip().casefold()

        if respuesta == "s":
            return categoria_actual

    propuesta = detectar_categoria(producto)

    if propuesta:
        print(f"\nCategoría sugerida para {producto}: {propuesta}")
    else:
        print(f"\nNo se ha podido reconocer la categoría de {producto}.")

    print("1. Comida")
    print("2. Bebida")
    print("3. Limpieza")

    if propuesta:
        respuesta = input(
            "Pulsa Enter para aceptar la sugerencia "
            "o escribe 1, 2 o 3 para cambiarla: "
        ).strip()

        if respuesta == "":
            categoria = propuesta
        else:
            categoria = None
    else:
        respuesta = input("Elige una categoría (1, 2 o 3): ").strip()
        categoria = None

    opciones = {
        "1": "Comida",
        "2": "Bebida",
        "3": "Limpieza"
    }

    if categoria is None:
        while respuesta not in opciones:
            respuesta = input(
                "Opción no válida. Elige 1, 2 o 3: "
            ).strip()

        categoria = opciones[respuesta]

    categorias[producto] = categoria
    guardar_categorias(categorias)

    print(f"Categoría guardada: {categoria}")
    return categoria


def cargar_despensa():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return {}


def guardar_despensa(despensa):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(despensa, archivo, ensure_ascii=False, indent=4)


def cargar_lista_compra():
    if os.path.exists(ARCHIVO_LISTA):
        with open(ARCHIVO_LISTA, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return {}


def guardar_lista_compra(lista_compra):
    with open(ARCHIVO_LISTA, "w", encoding="utf-8") as archivo:
        json.dump(lista_compra, archivo, ensure_ascii=False, indent=4)


        


def anadir_lista_compra(lista_compra):
    producto = input("¿Qué producto necesitas comprar? ").strip()

    if not producto:
        print("Debes escribir un nombre de producto.")
        return

    existente = buscar_producto(lista_compra, producto)

    if existente:
        producto = existente

    try:
        cantidad = int(input("¿Cuántas unidades necesitas? "))
    except ValueError:
        print("Debes introducir un número entero.")
        return

    if cantidad <= 0:
        print("La cantidad debe ser mayor que cero.")
        return

    if producto in lista_compra:
        lista_compra[producto] += cantidad
    else:
        lista_compra[producto] = cantidad

    guardar_lista_compra(lista_compra)
    print("Producto añadido a la lista de la compra.")




def ver_lista_compra(lista_compra):
    print("\n--- LISTA DE LA COMPRA ---")

    if not lista_compra:
        print("La lista de la compra está vacía.")
        return

    for producto, cantidad in lista_compra.items():
        print(f"- {producto}: {cantidad} unidades")





def marcar_comprado(lista_compra, despensa):
    if not lista_compra:
        print("La lista de la compra está vacía.")
        return

    print("\n--- PRODUCTOS PENDIENTES ---")
    for producto, cantidad in lista_compra.items():
        print(f"- {producto}: {cantidad} unidades")

    nombre = input("\n¿Qué producto has comprado? ").strip()
    producto_lista = buscar_producto(lista_compra, nombre)

    if producto_lista is None:
        print("Ese producto no está en la lista.")
        return

    cantidad = lista_compra[producto_lista]
    producto_despensa = buscar_producto(despensa, producto_lista)

    if producto_despensa is not None:
        despensa[producto_despensa] += cantidad
    else:
        despensa[producto_lista] = cantidad

    del lista_compra[producto_lista]

    guardar_despensa(despensa)
    guardar_lista_compra(lista_compra)

    print(f"Has añadido {cantidad} unidades de {producto_lista} a la despensa.")
    print("Producto retirado de la lista de la compra.")





def productos_reponer(despensa, lista_compra):
    print("\n--- PRODUCTOS QUE NECESITO REPONER ---")

    productos_bajos = {
        producto: cantidad
        for producto, cantidad in despensa.items()
        if cantidad <= 2
    }

    if not productos_bajos:
        print("No tienes productos con pocas unidades.")
        return

    for producto, cantidad in productos_bajos.items():
        print(f"- {producto}: quedan {cantidad} unidades")

    respuesta = input(
        "\n¿Quieres añadir productos a la lista de la compra? (s/n): "
    ).strip().lower()

    if respuesta != "s":
        print("No se han añadido productos.")
        return

    cambios = False

    for producto, cantidad_actual in productos_bajos.items():
        print(f"\nProducto: {producto}")
        print(f"Unidades que tienes: {cantidad_actual}")

        try:
            cantidad_compra = int(
                input("¿Cuántas unidades quieres comprar? ")
            )
        except ValueError:
            print("Cantidad no válida. Se omite este producto.")
            continue

        if cantidad_compra <= 0:
            print("La cantidad debe ser mayor que cero. Se omite este producto.")
            continue

        existente = buscar_producto(lista_compra, producto)

        if existente is not None:
            lista_compra[existente] += cantidad_compra
        else:
            lista_compra[producto] = cantidad_compra

        print(f"Añadidas {cantidad_compra} unidades de {producto}.")
        cambios = True

    if cambios:
        guardar_lista_compra(lista_compra)
        print("\nLista de la compra actualizada.")
    else:
        print("\nNo se han añadido productos.")




def ver_productos(despensa):
    print("\n--- MI DESPENSA ---")

    if not despensa:
        print("La despensa está vacía.")
        return

    for producto, cantidad in despensa.items():
        print(f"- {producto}: {cantidad}")



def anadir_producto(despensa):
    producto = input("¿Qué producto has comprado? ").strip()

    if not producto:
        print("Debes escribir un nombre de producto.")
        return

    existente = buscar_producto(despensa, producto)

    if existente:
        producto = existente

    try:
        cantidad = int(input("¿Cuántas unidades has comprado? "))
    except ValueError:
        print("Debes introducir un número entero.")
        return

    if cantidad <= 0:
        print("La cantidad debe ser mayor que cero.")
        return

    if producto in despensa:
        despensa[producto] += cantidad
    else:
        despensa[producto] = cantidad

    guardar_despensa(despensa)
    print("Compra registrada correctamente.")




def consumir_producto(despensa):
    producto = input("¿Qué producto has consumido? ").strip()

    existente = buscar_producto(despensa, producto)

    if existente is None:
        print("Ese producto no está en la despensa.")
        return

    try:
        cantidad = int(input("¿Cuántas unidades has consumido? "))
    except ValueError:
        print("Debes introducir un número entero.")
        return

    if cantidad <= 0:
        print("La cantidad debe ser mayor que cero.")
        return

    if cantidad > despensa[existente]:
        print("No tienes tantas unidades disponibles.")
        return

    despensa[existente] -= cantidad

    if despensa[existente] == 0:
        del despensa[existente]
        print("El producto se ha agotado y se ha retirado de la despensa.")
    else:
        print("Consumo registrado correctamente.")

    guardar_despensa(despensa)




def eliminar_producto(despensa):
    producto = input(
        "¿Qué producto quieres eliminar por completo? "
    ).strip()

    existente = buscar_producto(despensa, producto)

    if existente is not None:
        del despensa[existente]
        guardar_despensa(despensa)
        print("Producto eliminado correctamente.")
    else:
        print("Ese producto no está en la despensa.")



def main():
    despensa = cargar_despensa()
    lista_compra = cargar_lista_compra()

    while True:
        print("\n==============================")
        print("        MI DESPENSA")
        print("==============================")
        print("1. Ver productos")
        print("2. Añadir productos")
        print("3. Consumir productos")
        print("4. Eliminar un producto")
        print("5. Marcar producto como comprado")
        print("6. Ver lista de la compra")
        print("7. Añadir a la lista de la compra")
        print("8. Productos que necesito reponer")
        print("9. Salir")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            ver_productos(despensa)
        elif opcion == "2":
            anadir_producto(despensa)
        elif opcion == "3":
            consumir_producto(despensa)
        elif opcion == "4":
            eliminar_producto(despensa)
        elif opcion == "5":
            marcar_comprado(lista_compra, despensa)
        elif opcion == "6":
            ver_lista_compra(lista_compra)
        elif opcion == "7":
            anadir_lista_compra(lista_compra)
        elif opcion == "8":
            productos_reponer(despensa, lista_compra)
        elif opcion == "9":
            guardar_despensa(despensa)
            guardar_lista_compra(lista_compra)
            print("Despensa y lista de la compra guardadas. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Elige del 1 al 5.")


if __name__ == "__main__":
    main()
