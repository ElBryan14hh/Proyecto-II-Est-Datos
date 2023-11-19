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

    def agregar(self, tipo, nom):
        self.tabla[nom] = tipo

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
            if(var.ubicacion == self.cont and self.cont != 0):
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

    def error_argumentos(self, linea, nom):
        print(f"Error - Linea {linea}: cantidad de argumentos no coincide con '{nom}'")
        self.cant += 1
    
    def error_parametro(self, linea, nom):
        print(f"Error - Linea {linea}: el valor de algun parametro no coincide con '{nom}'")
        self.cant += 1

class Analizador:
    def __init__(self):
        self.tablita = Tabla_Hash()
        self.error = Error()
        self.pila = Pila()
        self.funcion = ""
        self.tabla_funciones = Tabla_Hash()

    def tipo_dato(self, tipo, val):
        try:
            if(val in self.tablita.tabla):
                tipo2 = self.tablita.tabla[val]
                if(tipo2 != tipo):
                    raise
            elif(tipo == "string"):
                if(val.count('"') != 2):
                    raise
            elif(tipo == "int"):
                p = int(val)
            else:
                p = float(val)
        except:
            return False
        return True

    def variables(self, linea, numLinea):
        palabra = linea.split()
        salir = False
        try:
            if(palabra[1] in self.tablita.tabla):
                self.error.error_ya_declarado(numLinea, palabra[1])
                return
            pal = palabra[3]
            pal2 = palabra[3:]
            p = "".join(pal2)
            p = self.remplazar_en_linea(p).split()
            if(p[0] in self.tabla_funciones.tabla):
                params = self.tabla_funciones.tabla[p[0]]
                vals = p[1:]
                if(len(params) != len(vals)):
                    self.error.error_argumentos(numLinea, p[0])
                else:
                    for i in range (0, len(params)):
                        if(self.tipo_dato(params[i], vals[i]) == False):
                            self.error.error_parametro(numLinea, p[0])
                            break
                if(palabra[0] != self.tablita.tabla[p[0]]):
                    raise
            else:
                if(palabra[0] == "int"):
                    i = int(pal)
                elif(palabra[0] == "float"):
                    i = float(pal)
                elif(palabra[0] == "string"):
                    try:
                        i = float(pal)
                        salir = True
                    except:
                        salir = False
                else:
                    raise
                if(salir):
                    raise
            self.tablita.agregar(palabra[0], palabra[1])
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
        vec = []
        pal = ""
        for i in range (0, len(palabra) - 1, 2):
            if(palabra[i + 1] not in self.tablita.tabla):
                if(i == 0):
                    pal = palabra[i + 1]
                    self.funcion = palabra[1]
                else:
                    vec.append(palabra[i])
                if(i == 2):
                    self.pila.aumentar()
                self.tablita.agregar(palabra[i], palabra[i + 1])
                self.pila.agregar(palabra[i + 1])
            else:
                self.error.error_ya_declarado(numLinea, palabra[i + 1])
        if(pal != ""):
            self.tabla_funciones.agregar(vec, pal)
        
    def funcion_reservadas(self, linea, numLinea):
        palabra = linea.split()
        if(palabra[0] == "if" or "while"):
            self.pila.aumentar()
            pal = palabra[1]
            if(pal in self.tablita.tabla):
                tipo = self.tablita.tabla[pal]
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
            tipo = self.tablita.tabla[pal]
            if(tipo == "int" or "float" or "string"):
                try:
                    if(palabra[1] in self.tablita.tabla):
                        tipo2 = self.tablita.tabla[palabra[1]]
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
        tipo = self.tablita.tabla[self.funcion]
        if(tipo == "void"):
            if(len(palabra) == 1):
                return
            else:
                self.error.error_retorno_void(numLinea, self.funcion)
        else:
            val = palabra[1]
            try:
                if(val in self.tablita.tabla):
                    
                    if(self.tablita.tabla[val] == tipo):
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

    def fin_funcion(self):
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
                    if(lin2[0] != "int" and lin2[0] != "string" and lin2[0] != "float"):
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
                    elif(lin3[0] == "}"):
                        self.fin_funcion()
                n+=1
        print(f"\nErrores -> [{self.error.cant}]")
        if(self.error.cant == 0):
            print("El codigo se ha compilado correctamente!")
        self.tablita.mostrar_tabla()

an = Analizador()
an.leer_archivo("codigo.txt")