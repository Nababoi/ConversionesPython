from data.data_helper import data_helper, Login, Modificador, Agregador
from currencies import curr
from os import path
import json
import requests as rq
import bcrypt
from decimal import Decimal
from decimal import getcontext

class business_helper:
    username=""
    logged=False

    def __init__(self):
        # self.username = username
        self.logged = True
        self.data_helper = data_helper()
        
    def createAccount(self,curr_code,username):

        curr_code=curr_code.lstrip().rstrip().upper()
        if self.data_helper.isCurrCodeValid(curr_code) == False:
            raise Exception("Codigo de moneda no valido")
        if self.data_helper.checkAccounts(username) == False:
            raise Exception("Formato de Datos inadecuado")
        if self.data_helper.AccountExist(curr_code,username) == True:
            raise Exception("Ya Existe la cuenta que desea crear")
        self.data_helper.createAccount(curr_code,username)

    # def openAccount(self,moneda,usuario):
        
    def addMoney(self,cuenta,moneda,cantidad):
        moneda = moneda.strip().upper()
        if (cantidad <= 0):
            raise Exception("Ingrese una cantidad valida")
        if not self.data_helper.maxMoneyAccount(cuenta,moneda,cantidad):
            raise Exception("No se puede ingresar mas dinero a la cuenta")
        if not self.data_helper.isCurrCodeValid(moneda):
            raise Exception("Ingrese un codigo de moneda valido")
        if not self.data_helper.AccountExist(moneda,cuenta):
            raise Exception("No tiene una cuenta abierta con esa moneda")
        self.data_helper.addMoney(cuenta,moneda,cantidad) 

    def buyCurrMoney(self, cuenta,cantidad, moneda):
        moneda = moneda.strip().upper()
        getcontext().prec = 100

        self.validaciones(moneda,cuenta,cantidad)

        archivo = str(cuenta) + ".json"

        conexion = self.data_helper.conexionApi(moneda)      
        cot_Moneda_X = self.data_helper.cotizacionMoneda(conexion,moneda)
        cot_Moneda_Peso = self.data_helper.cotizacionMoneda(conexion,"ARS")
        cot_peso_x = cot_Moneda_Peso/cot_Moneda_X

        with open(archivo, "r") as f:
            cuentas = json.load(f)

        saldo_ars = Decimal(cuentas["ARS"])
        cantidad_A_Comprar = Decimal(cot_peso_x).quantize(Decimal('0.00')) * Decimal(cantidad).quantize(Decimal('0.00'))

        if cantidad_A_Comprar > saldo_ars:
            raise Exception("No tiene suficiente pesos argentinos para comprar esa moneda")

        total_moneda_x = Decimal(cantidad_A_Comprar).quantize(Decimal('0.00')) / Decimal(cot_peso_x).quantize(Decimal('0.00'))

        if total_moneda_x == 0:
            raise Exception("No tiene suficientes pesos argentinos para comprar esa moneda")

        cuentas["ARS"] = str(Decimal(saldo_ars) - Decimal(cantidad_A_Comprar))

        if moneda in cuentas:
            cuentas[moneda] = str(Decimal(cuentas[moneda]) + Decimal(total_moneda_x))
        else:
            cuentas[moneda] = str(total_moneda_x)

        with open(archivo, "w") as f:
            json.dump(cuentas, f, indent=4)

        # self.data_helper.buyCurrMoney(cuenta,cantidad,moneda)

    def validaciones(self,moneda,cuenta,cantidad):
        if not self.data_helper.isCurrCodeValid(moneda):
            raise Exception("Ingrese un codigo de moneda valido")
        if not self.data_helper.AccountExist(moneda,cuenta):
            raise Exception("No tiene una cuenta abierta en esa moneda")
        if (cantidad <= 0):
            raise Exception("Ingrese una cantidad valida")
        # self.data_helper.buyCurrMoney(cuenta,cantidad,moneda)

    def sellCurrMoney(self, cuenta,cantidad, moneda):
        moneda = moneda.strip().upper()
        getcontext().prec = 100

        self.validaciones(moneda,cuenta,cantidad)

        conexion = self.data_helper.conexionApi(moneda)      
        cot_Moneda_X = self.data_helper.cotizacionMoneda(conexion,moneda)
        cot_Moneda_Peso = self.data_helper.cotizacionMoneda(conexion,"ARS")
        cot_peso_x = cot_Moneda_X/cot_Moneda_Peso

        archivo = f"{cuenta}.json"
        
        with open(archivo, "r") as f:
            cuenta = json.load(f)

        saldo_X = Decimal(cuenta[moneda])

        cantidad_A_acreditar = cot_peso_x * Decimal(cantidad)

        if Decimal(cantidad) > saldo_X:
            raise Exception("El saldo no es suficiente")

        saldo_restante = saldo_X - Decimal(cantidad)
        cuenta[moneda] = "{:.2f}".format(saldo_restante)

        saldo_restante = (Decimal(cuenta['ARS']) + cantidad_A_acreditar)
        cuenta['ARS'] = "{:.2f}".format(saldo_restante)

        with open(archivo, "w") as f:
            json.dump(cuenta, f, indent=4)
        
        raise Exception("Operacion exitosa")
        # self.data_helper.sellCurrMoney(cuenta,cantidad,moneda)

#SECCION DEL LOGIN

class Verificacion:
    
    def __init__(self,contra,nombre):
        self.contra = contra.strip()
        self.nombre = nombre.lower().strip()
        
    def Verificador(self):

            MyVeri = Login() 
            contraV, nombreV = MyVeri.ContraNombre(self.contra, self.nombre)
            if(contraV == self.contra and nombreV == self.nombre):
                # raise Exception("Hubo matchRaise")
                return True
            else:
                raise Exception("Datos incorrectos")
class AgregarAdmin:
    
    def __init__(self,contra,contra2,nombre):
        self.contra = contra.strip()
        self.contra2 = contra2.strip()
        self.nombre = nombre.lower().strip()
        
    def Agregar(self):
        MiAg = Agregador()
        AgrVar = MiAg.agregar(self.contra, self.contra2, self.nombre)
        if(AgrVar):
                # print("Se agrego")
            raise Exception("Se agrego")
        else:
            raise Exception("Las contraseñas no coinciden")
                # print("Las contraseñas no coinciden")
            
class ModificarAdmin:
    def __init__(self,contra,contra2,nombre):
        self.contra = contra.strip()
        self.contra2 = contra2.strip()
        self.nombre = nombre.lower().strip()
    
    def modificar(self):

        MiMod = Modificador()
        ModVar = MiMod.modificar(self.contra, self.contra2, self.nombre)
        if(ModVar):
            raise Exception("Se modifico el usuario")
        else:
            raise Exception("No se pudo modificar el usuario")