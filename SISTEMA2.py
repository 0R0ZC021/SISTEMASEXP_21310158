import re
import json
from itertools import product

LETRAS = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

def convertir_a_formula(oracion):
    # Manejo de negación usando 'no'
    oracion = re.sub(r'no\s+(\w+)', r'¬\1', oracion)
    
    proposiciones = re.split(r'\s+y\s+|\s+o\s+', oracion)
    formula = oracion.replace(" y ", " ∧ ").replace(" o ", " ∨ ")
    mapeo = {proposiciones[i]: LETRAS[i] for i in range(len(proposiciones))}
    
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
        
        # Evaluar la fórmula con operadores lógicos
        evaluacion = eval(
            formula.replace("∧", " and ").replace("∨", " or ").replace("¬", " not "),
            {}, valores
        )
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

def imprimir_tabla_atomos(mapeo):
    proposiciones = list(mapeo.values())
    n = len(proposiciones)
    combinaciones = list(product([True, False], repeat=n))
    header = " | ".join(proposiciones)
    output = f"Tabla de átomos:\n{header}\n" + "-" * len(header) + "\n"
    
    for combinacion in combinaciones:
        valores = ["V" if v else "F" for v in combinacion]
        output += " | ".join(valores) + "\n"
    
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

def imprimir_clausulas_horn(tabla, mapeo):
    proposiciones = list(mapeo.values())
    output = "\nCláusulas de Horn:\n"

    for fila in tabla:
        combinacion, resultado = fila
        antecedente = []
        
        for i, valor in enumerate(combinacion):
            if not valor:
                antecedente.append(f"¬{proposiciones[i]}")
            else:
                antecedente.append(proposiciones[i])
        
        consecuente = "Verdadero" if resultado else "Falso"
        
        if antecedente:
            output += f"{' ∧ '.join(antecedente)} → {consecuente}\n"
        else:
            output += f"{consecuente}\n"
    
    return output

def guardar_clausulas_horn(reglas):
    archivo_txt = "clausulas_horn.txt"
    with open(archivo_txt, 'w', encoding='utf-8') as file:
        count = 0
        for regla in reglas:
            formula, mapeo = regla["formula"], regla["mapeo"]
            tabla = generar_tabla_verdad(formula, mapeo)
            clausulas = imprimir_clausulas_horn(tabla, mapeo)
            file.write(f"Regla {count + 1}:\n{clausulas}\n")
            count += 1
            if count >= 20:
                break
    print(f"Cláusulas de Horn guardadas en {archivo_txt}.")

def guardar_reglas(archivo, reglas):
    with open(archivo, 'w', encoding='utf-8') as file:
        json.dump(reglas, file)
    print(f"Reglas guardadas en {archivo}.")

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

def cargar_oraciones_desde_txt(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            oraciones = file.readlines()
        
        reglas = []
        for oracion in oraciones:
            oracion = oracion.strip()
            if oracion:
                formula, mapeo = convertir_a_formula(oracion)
                reglas.append({"formula": formula, "mapeo": mapeo})
        
        print(f"Oraciones cargadas desde {archivo}.")
        return reglas
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []

def main():
    reglas = []
    archivo = "reglas.json"

    while True:
        print("\n1. Ingresar nueva regla")
        print("2. Mostrar reglas, evaluar tabla de verdad y árbol de decisión")
        print("3. Guardar reglas")
        print("4. Cargar reglas")
        print("5. Evaluar proposición atómica")
        print("6. Mostrar tabla de átomos")
        print("7. Mostrar cláusulas de Horn")
        print("8. Mostrar tabla de elementos de cláusulas de Horn")
        print("9. Guardar cláusulas de Horn")
        print("10. Cargar oraciones desde archivo .txt")
        print("11. Salir")
        
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
                for idx, regla in enumerate(reglas, 1):
                    print(f"Regla {idx}: {regla['formula']}")
                seleccion = int(input("Seleccione el número de la regla a evaluar: ")) - 1
                if 0 <= seleccion < len(reglas):
                    formula, mapeo = reglas[seleccion]["formula"], reglas[seleccion]["mapeo"]
                    respuestas = preguntar_atomica(mapeo)
                    evaluacion = eval(formula.replace("∧", " and ").replace("∨", " or ").replace("¬", " not "), {}, respuestas)
                    print(f"Evaluación de la proposición: {'V' if evaluacion else 'F'}")
                else:
                    print("Selección inválida.")
            else:
                print("No hay reglas cargadas para evaluar.")
        
        elif opcion == "6":
            if reglas:
                for idx, regla in enumerate(reglas, 1):
                    mapeo = regla["mapeo"]
                    print(f"\nTabla de átomos para Regla {idx}:")
                    print(imprimir_tabla_atomos(mapeo))
            else:
                print("No hay reglas cargadas para mostrar la tabla de átomos.")
        
        elif opcion == "7":
            if reglas:
                for regla in reglas:
                    formula, mapeo = regla["formula"], regla["mapeo"]
                    tabla = generar_tabla_verdad(formula, mapeo)
                    print(imprimir_clausulas_horn(tabla, mapeo))
            else:
                print("No hay reglas cargadas para mostrar cláusulas de Horn.")
        
        elif opcion == "8":
            if reglas:
                for regla in reglas:
                    formula, mapeo = regla["formula"], regla["mapeo"]
                    tabla = generar_tabla_verdad(formula, mapeo)
                    print(imprimir_clausulas_horn(tabla, mapeo))
            else:
                print("No hay reglas cargadas para mostrar la tabla de elementos de cláusulas de Horn.")
        
        elif opcion == "9":
            guardar_clausulas_horn(reglas)
        
        elif opcion == "10":
            archivo_txt = input("Ingrese el nombre del archivo .txt: ")
            reglas = cargar_oraciones_desde_txt(archivo_txt)
        
        elif opcion == "11":
            print("Saliendo del programa.")
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()
