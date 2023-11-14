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
        self.tabla = {}

    def funcion_hash(self, val):
        return ((val%10+1)%10)
    
    def valor_str(self, str):
        suma = 0
        for i in str:
            suma += ord(i)
        return suma
    
    def agregar(self, tipo, nom, val):
        #x = self.valor_str(nom)
        #indice = self.funcion_hash(x)
        self.tabla[nom] = (tipo, val)
        
    def mostrar_tabla(self):
        for i in self.tabla:
            print(f"[{i}] -> {self.tabla[i]}")
    
class Error:
    def error_no_declarado(self, linea, nom):
        print(f"Error - Linea {linea} '{nom}' no esta declarado")

    def error_retorno(self, linea, nom):
        print(f"Error - Linea {linea} valor de retorno no coincide con la declaracion '{nom}'")

class Analizador:
    def __int__(self):
        self.tabla = Tabla_Hash()
        self.error = Error()

    def analisis(self, linea, numLinea):
        vec = []
        i = 0
        for palabra in linea.split():
            if (palabra is "int" or "string" or "float" or "void"):
                vec[i] = palabra
                palabra in linea.split()
                if(palabra is not tabla and palabra is not "int" or "string" or "float" or "void" or "{" or "}" or "(" or ")"):
                    i+=1
                    vec[i] = palabra
                    palabra in linea.split()
                    if(palabra is "="):
                        
            elif ():


    def leer_archivo(self, archivo):
        n = 1
        with open(archivo, "r") as f:
            for linea in f:
                return
                


                


tabla = Tabla_Hash()
tabla.agregar("int", "x", 20)
tabla.agregar("int", "A7", 40)
tabla.agregar("string", "cadena", "Hola")
tabla.mostrar_tabla()

