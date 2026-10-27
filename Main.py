import json
import os

print("ESTOY EJECUTANDO EL MAIN CORRECTO")

ARCHIVO = "despensa.json"


def cargar_despensa():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return {}


def guardar_despensa(despensa):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(despensa, archivo, ensure_ascii=False, indent=4)


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

    if producto not in despensa:
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

    if cantidad > despensa[producto]:
        print("No tienes tantas unidades disponibles.")
        return

    despensa[producto] -= cantidad

    if despensa[producto] == 0:
        del despensa[producto]
        print("El producto se ha agotado y se ha retirado de la despensa.")
    else:
        print("Consumo registrado correctamente.")

    guardar_despensa(despensa)


def eliminar_producto(despensa):
    producto = input("¿Qué producto quieres eliminar por completo? ").strip()

    if producto in despensa:
        del despensa[producto]
        guardar_despensa(despensa)
        print("Producto eliminado correctamente.")
    else:
        print("Ese producto no está en la despensa.")


def main():
    despensa = cargar_despensa()

    while True:
        print("\n==============================")
        print("        MI DESPENSA")
        print("==============================")
        print("1. Ver productos")
        print("2. Añadir productos")
        print("3. Consumir productos")
        print("4. Eliminar un producto")
        print("5. Salir")

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
            guardar_despensa(despensa)
            print("Despensa guardada. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Elige del 1 al 5.")


if __name__ == "__main__":
    main()
