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
    
    def modificar_valor(self, nom, val):
        self.tabla[nom] = (self.tabla[nom][0], val)

    def mostrar_tabla(self):
        for i in self.tabla:
            print(f"[{i}] -> {self.tabla[i]}")
    
class Error:
    def error_no_declarado(self, linea, nom):
        print(f"Error - Linea {linea}: '{nom}' no esta declarado")

    def error_ya_declarado(self, linea, nom):
        print(f"Error - Linea {linea}: '{nom}' ya fue declarada anteriormente")

    def error_retorno(self, linea, nom):
        print(f"Error - Linea {linea}: valor de retorno no coincide con la declaracion '{nom}'")

    def error_asignacion(self, linea, nom):
         print(f"Error - Linea {linea}: tipo de variable de '{nom}' no coincide con el valor de asignacion")

    def error_comparacion(self, linea, nom):
        print(f"Error - Linea {linea}: el valor de '{nom}' no coincide con el valor de comparacion")

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

    def remplazar_en_linea(self, linea):
        lin = linea.replace('(',' ')
        lin = lin.replace(')',' ')
        lin = lin.replace('{',' ')
        lin = lin.replace('}',' ')
        lin = lin.replace(',',' ')
        lin = lin.replace('+', ' ')
        lin = lin.replace('<', ' ')
        lin = lin.replace('>', ' ')
        lin = lin.replace('=', ' ')
        lin = lin.replace('!', ' ')
        lin = lin.replace('-', ' ')
        lin = lin.replace('*', ' ')
        lin = lin.replace('/', ' ')
        lin = lin.replace('%', ' ')
        return lin
    
    def funciones(self, linea, numLinea):
        palabra = linea.split()
        for i in range (0, len(palabra) - 1, 2):
            if(palabra[i + 1] not in self.tablita.tabla):
                self.tablita.agregar(palabra[i], palabra[i + 1], any)
            else:
                self.error.error_ya_declarado(numLinea, palabra[i + 1])
        
    def funcion_reservadas(self, linea, numLinea):
        palabra = linea.split()
        if(palabra[0] == "if" or "while"):
            pal = palabra[1]
            if(pal in self.tablita.tabla):
                tipo = self.tablita.tabla[pal][0]
                try:
                    if(tipo == "int"):
                        i = int(palabra[2])
                    elif(tipo == "float"):
                        i = float(palabra[2])
                    elif(tipo == "string"):
                        try:
                            if('.' in pal):
                                i = float(palabra[2])
                            else:
                                i = int(palabra[2]) 
                            raise
                        except:
                            return
                    else:
                        raise
                except:
                    self.error.error_comparacion(numLinea, palabra[1])
            else:
                self.error.error_no_declarado(numLinea, palabra[1])
    
    def leer_archivo(self, archivo):
        n = 1
        with open(archivo, "r") as f:
            for linea in f:
                if(n == 1):
                    self.variables(linea, n)
                elif(n==2):
                #self.variables(linea, n)
                #self.funciones(self.remplazar_en_linea(linea), n)
                    self.funcion_reservadas(self.remplazar_en_linea(linea), n)
                else:
                    self.funciones(self.remplazar_en_linea(linea), n)
                n+=1
        self.tablita.mostrar_tabla()

an = Analizador()
an.leer_archivo("codigo.txt")

