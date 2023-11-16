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

class VariablesPila:
    def __init__(self, c, u):
        self.clave = c
        self.ubicacion = u

class Pila:
    def __init__(self):
        self.stack = []
        self.cont = 0
    
    def agregar(self, c):
        elemento = VariablesPila(c, self.cont)
        self.stack.append(elemento)

    def aumentar(self):
        self.cont+=1

    def eliminar(self):
        vec = []
        for var in reversed(self.stack):
            if(var.ubicacion == self.cont):
                vec.append(var.clave)
                self.stack.pop()
            else:
                break
        self.cont-=1
        return vec

            
class Error:
    def __init__(self):
        self.cant = 0
    
    def error_no_declarado(self, linea, nom):
        print(f"Error - Linea {linea}: '{nom}' no esta declarado")
        self.cant += 1

    def error_ya_declarado(self, linea, nom):
        print(f"Error - Linea {linea}: '{nom}' ya fue declarada anteriormente")
        self.cant += 1

    def error_retorno(self, linea, nom):
        print(f"Error - Linea {linea}: valor de retorno no coincide con la declaracion '{nom}'")
        self.cant += 1

    def error_asignacion(self, linea, nom):
        print(f"Error - Linea {linea}: tipo de variable de '{nom}' no coincide con el valor de asignacion")
        self.cant += 1

    def error_comparacion(self, linea, nom):
        print(f"Error - Linea {linea}: el valor de '{nom}' no coincide con el valor de comparacion")
        self.cant += 1

    def error_operacion(self, linea, nom):
        print(f"Error - Linea {linea}: el valor de '{nom}' no coincide con el valor de algun dato en la operacion")
        self.cant += 1
    
    def error_retorno_void(self, linea, nom):
        print(f"Error - Linea {linea}: '{nom}' no puede retornar ningun valor")
        self.cant += 1

class Analizador:
    def __init__(self):
        self.tablita = Tabla_Hash()
        self.error = Error()
        self.pila = Pila()
        self.funcion = ""

    def variables(self, linea, numLinea):
        palabra = linea.split()
        salir = False
        try:
            if(palabra[1] in self.tablita.tabla):
                self.error.error_ya_declarado(numLinea, palabra[1])
                return
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
            self.pila.agregar(palabra[1])
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
                if(i == 0):
                    self.pila.aumentar()
                    self.funcion = palabra[1]
                self.tablita.agregar(palabra[i], palabra[i + 1], any)
                self.pila.agregar(palabra[i + 1])
            else:
                self.error.error_ya_declarado(numLinea, palabra[i + 1])
        
    def funcion_reservadas(self, linea, numLinea):
        palabra = linea.split()
        if(palabra[0] == "if" or "while"):
            self.pila.aumentar()
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
                    self.error.error_comparacion(numLinea, pal)
            else:
                self.error.error_no_declarado(numLinea, palabra[1])
    
    def operaciones(self, linea, numLinea):
        palabra = linea.split()
        pal = palabra[0]
        if(pal in self.tablita.tabla):
            tipo = self.tablita.tabla[pal][0]
            if(tipo == "int" or "float"):
                try:
                    for i in range (1, len(palabra)):
                        if(palabra[i] in self.tablita.tabla):
                            tipo2 = self.tablita.tabla[palabra[i]][0]
                            if(tipo2 != "int" and tipo2 != "float"):
                                raise
                        elif(tipo == "int"):
                            p = int(palabra[i])
                        else:
                            p = float(palabra[i])
                except:
                    self.error.error_operacion(numLinea, pal)
        else:
            self.error.error_no_declarado(numLinea, pal)
    
    def asignaciones(self, linea, numLinea):
        palabra = linea.split()
        pal = palabra[0]
        if(pal in self.tablita.tabla):
            tipo = self.tablita.tabla[pal][0]
            if(tipo == "int" or "float" or "string"):
                try:
                    if(palabra[1] in self.tablita.tabla):
                        tipo2 = self.tablita.tabla[palabra[1]][0]
                        if(tipo2 != "int" and tipo2 != "float" and tipo2 != "string"):
                            raise
                    elif(tipo == "string"):
                        if(palabra[1].count('"') != 2):
                            raise
                    elif(tipo == "int"):
                        p = int(palabra[1])
                    else:
                        p = float(palabra[1])
                except:
                    self.error.error_asignacion(numLinea, pal)
        else:
            self.error.error_no_declarado(numLinea, pal)

    def valor_retorno(self, linea, numLinea):
        palabra = linea.split()
        tipo = self.tablita.tabla[self.funcion][0]
        if(tipo == "void"):
            if(len(palabra) == 1):
                return
            else:
                self.error.error_retorno_void(numLinea, self.funcion)
        else:
            val = palabra[1]
            try:
                if(val in self.tablita.tabla):
                    
                    if(self.tablita.tabla[val][0] == tipo):
                        return
                    else:
                        raise
                else:
                    try:
                        f = float(val)
                    except:
                        if(val.count('"') != 2):
                            self.error.error_no_declarado(numLinea, self.funcion)
                        else:
                            raise
                    if(tipo == "int"):
                        i = int(val)
            except:
                self.error.error_retorno(numLinea, self.funcion)

    def fin_funcion(self, linea, numLinea):
        vec = self.pila.eliminar()
        for i in vec:
            del self.tablita.tabla[i]

    def leer_archivo(self, archivo):
        n = 1
        with open(archivo, "r") as f:
            for linea in f:
                lin = self.remplazar_en_linea(linea)
                lin2 = lin.split()
                lin3 = linea.split()
                if('=' in linea and lin2[0] != "if" and lin2[0] != "while"):
                    if(lin2[0] != "int" and "string" and "float"):
                        if('+' in linea or '/' in linea or '-' in linea or '*' in linea or '%' in linea):
                            self.operaciones(lin, n)
                        else:
                            self.asignaciones(lin, n)
                    else:
                        self.variables(linea, n)
                elif('(' in linea and ')' in linea):
                    if(lin2[0] == "if" or lin2[0] == "while"):
                        self.funcion_reservadas(lin, n)
                    else:
                        self.funciones(lin, n)
                elif('=' in linea):
                    self.asignaciones(lin, n)
                elif(lin3 != []):
                    if(lin3[0] == "return"):
                        self.valor_retorno(linea, n)
                elif(linea[0] == "}"):
                    self.fin_funcion(linea, n)
                n+=1
        print(f"Errores -> [{self.error.cant}]")
        if(self.error.cant == 0):
            print("El codigo se ha compilado correctamente!")
        self.tablita.mostrar_tabla()

an = Analizador()
an.leer_archivo("codigo.txt")