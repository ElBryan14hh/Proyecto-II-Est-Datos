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

    def agregar(self, tipo, nom, val):
        self.tabla[nom] = (tipo, val)
        
    def mostrar_tabla(self):
        for i in self.tabla:
            print(f"[{i}] -> {self.tabla[i]}")
    
class Error:
    def error_no_declarado(self, linea, nom):
        print(f"Error - Linea {linea} '{nom}' no esta declarado")

    def error_retorno(self, linea, nom):
        print(f"Error - Linea {linea} valor de retorno no coincide con la declaracion '{nom}'")

    def error_asignacion(self, linea, nom):
         print(f"Error - Linea {linea} tipo de variable de '{nom}' no coincide con el valor de asignacion")

class Analizador:

    def __init__(self):
        self.tablita = Tabla_Hash()
        self.error = Error()

    def variables(self, linea, numLinea):
        palabra = linea.split()
        salir = False
        try:
            pal = palabra[3]
            if(palabra[0] == "int"):
                i = int(pal)
            elif(palabra[0] == "float"):
                i = float(pal)
            elif(palabra[0] == "string"):
                try:
                    if('.' in pal):
                        i = float(pal)
                    else:
                        i = int(pal) 
                    salir = True
                except:
                    i = pal[1:(len(pal)-1)]
            else:
                raise
            if(salir):
                raise
            self.tablita.agregar(palabra[0], palabra[1], i)
        except:
            self.error.error_asignacion(numLinea, palabra[1])

    def leer_archivo(self, archivo):
        n = 1
        with open(archivo, "r") as f:
            for linea in f:
                self.variables(linea, n)
                n+=1
        self.tablita.mostrar_tabla()

an = Analizador()
an.leer_archivo("codigo.txt")

