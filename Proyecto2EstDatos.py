#########################################
#                                       #
#   Universidad Nacional de Costa Rica  #
#   Estructuras de Datos - CII 2023     #
#   Bryan Hernandez - 8 pm              #
#   Santiago Solis - 6 pm               #
#   Felipe Herrrera - 8 pm              #
#   Proyecto #2 - Analizador Semantico  #
#                                       #
#########################################

class Tabla_Hash:

    def __init__(self):
        self.tabla = [None] * 10

    def funcion_hash(self, val):
        return ((val%10+1)%10)
    
    def valor_str(self, str):
        suma = 0
        for i in str:
            suma += ord(i)
        return suma
    
    def agregar(self, tipo, nom, val):
        x = self.valor_str(nom)
        indice = self.funcion_hash(x)
        tupla = (tipo, nom, val)
        if (self.tabla[indice] is None):
            self.tabla[indice] = [tupla]
        else:
            self.tabla[indice].append(tupla)
    
    def mostrar_tabla(self):
        n = 0
        for i in self.tabla:
            print(f"[{n}] -> {i}")
            n += 1

tabla = Tabla_Hash()
tabla.agregar("int", "x", 20)
tabla.agregar("int", "A7", 40)
tabla.agregar("string", "cadena", "Hola")
tabla.mostrar_tabla()

