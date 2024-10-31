import re
import json
from itertools import product
from datetime import datetime

def convertir_a_formula(oracion):
    proposiciones = re.split(r'\s+y\s+|\s+o\s+', oracion)
    formula = oracion.replace(" y ", " ∧ ").replace(" o ", " ∨ ")
    letras = ['A', 'B', 'C', 'D', 'E', 'F']
    mapeo = {proposiciones[i]: letras[i] for i in range(len(proposiciones))}
    
    for proposicion, letra in mapeo.items():
        formula = formula.replace(proposicion, letra)
    
    return formula, mapeo

def generar_tabla_verdad(formula, mapeo):
    proposiciones = list(mapeo.values())
    n = len(proposiciones)
    combinaciones = list(product([True, False], repeat=n))
    tabla = []

    for combinacion in combinaciones:
        valores = dict(zip(proposiciones, combinacion))
        evaluacion = eval(formula.replace("∧", " and ").replace("∨", " or "), {}, valores)
        tabla.append((combinacion, evaluacion))
    
    return tabla

def imprimir_tabla_verdad(tabla, mapeo):
    proposiciones = list(mapeo.values())
    header = " | ".join(proposiciones) + " | Resultado"
    output = header + "\n" + "-" * len(header) + "\n"
    
    for fila in tabla:
        valores = ["V" if v else "F" for v in fila[0]]
        resultado = "V" if fila[1] else "F"
        output += " | ".join(valores) + " | " + resultado + "\n"
    
    return output

def imprimir_arbol_binario(tabla, mapeo):
    proposiciones = list(mapeo.values())
    output = "\nÁrbol de Decisión Binario:\n"
    
    def construir_nodo(nivel, combinacion, resultado):
        if nivel == len(proposiciones):
            return f"{'V' if resultado else 'F'}\n"
        
        prop = proposiciones[nivel]
        estado = "Verdadero" if combinacion[nivel] else "Falso"
        espaciado = "    " * nivel
        nodo_texto = f"{espaciado}{prop} es {estado} -> "
        
        nodo_texto += construir_nodo(nivel + 1, combinacion, resultado)
        return nodo_texto
    
    for fila in tabla:
        combinacion, resultado = fila
        output += construir_nodo(0, combinacion, resultado)
        output += "-" * 30 + "\n"
    
    return output

def guardar_reglas(archivo, reglas):
    with open(archivo, 'w', encoding='utf-8') as file:
        json.dump(reglas, file)
    print(f"Reglas guardadas en {archivo}.")
    
    # Generar nombre único para el archivo de texto
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_txt = f"resultado_{timestamp}.txt"
    
    # Guardar la salida de la consola en el archivo de texto con codificación UTF-8
    with open(archivo_txt, 'w', encoding='utf-8') as file:
        for regla in reglas:
            formula, mapeo = regla["formula"], regla["mapeo"]
            tabla = generar_tabla_verdad(formula, mapeo)
            file.write(f"\nFórmula lógica: {formula}\n")
            file.write("Mapeo de proposiciones: " + str(mapeo) + "\n")
            file.write(imprimir_tabla_verdad(tabla, mapeo))
            file.write(imprimir_arbol_binario(tabla, mapeo))
    
    print(f"Resultados guardados en {archivo_txt}.")

def cargar_reglas(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            reglas = json.load(file)
        print(f"Reglas cargadas desde {archivo}.")
        return reglas
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []

def preguntar_atomica(mapeo):
    respuestas = {}
    for proposicion, letra in mapeo.items():
        respuesta = input(f"¿{proposicion} es Verdadero (V) o Falso (F)? ")
        respuestas[letra] = True if respuesta.lower() == 'v' else False
    return respuestas

def main():
    reglas = []
    archivo = "reglas.json"

    while True:
        print("\n1. Ingresar nueva regla")
        print("2. Mostrar reglas y evaluar tabla de verdad")
        print("3. Guardar reglas")
        print("4. Cargar reglas")
        print("5. Evaluar proposición atomica")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            oracion = input("Ingrese una proposición compuesta: ")
            formula, mapeo = convertir_a_formula(oracion)
            reglas.append({"formula": formula, "mapeo": mapeo})
            print("Regla añadida.")
        
        elif opcion == "2":
            for regla in reglas:
                formula = regla["formula"]
                mapeo = regla["mapeo"]
                print(f"\nFórmula lógica: {formula}")
                print("Mapeo de proposiciones:", mapeo)
                tabla = generar_tabla_verdad(formula, mapeo)
                print(imprimir_tabla_verdad(tabla, mapeo))
                print(imprimir_arbol_binario(tabla, mapeo))
        
        elif opcion == "3":
            guardar_reglas(archivo, reglas)
        
        elif opcion == "4":
            reglas = cargar_reglas(archivo)
        
        elif opcion == "5":
            if reglas:
                formula, mapeo = reglas[0]["formula"], reglas[0]["mapeo"]
                respuestas = preguntar_atomica(mapeo)
                evaluacion = eval(formula.replace("∧", " and ").replace("∨", " or "), {}, respuestas)
                print(f"Evaluación de la proposición: {evaluacion}")
            else:
                print("No hay reglas cargadas para evaluar.")
        
        elif opcion == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
