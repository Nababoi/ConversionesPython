from data.data_helper import Administrador, data_helper

# from os import path
# import json
# import requests as rq
from decimal import Decimal
import decimal
from decimal import getcontext
import sqlobject as SO

class business_helper:
    username=""
    logged=False

    def __init__(self):
        self.logged = True
        # self.data_helper = data_helper()
        self.data_helper = data_helper()
        
    def createAccount(self,curr_code,username):

        curr_code=curr_code.lstrip().rstrip().upper()
        if self.data_helper.isCurrCodeValid(curr_code) == False:
            raise Exception("Codigo de moneda no valido")
        if self.data_helper.AccountExist(curr_code,username) == True:
            raise Exception("Ya Existe la cuenta que desea crear")
        # self.data_helper.createAccount(curr_code,username)
        self.data_helper.createAccount(curr_code,username)
        raise Exception("Se creo la cuenta")


    def addMoney(self,cuenta,moneda,cantidad):
        moneda = moneda.strip().upper()
        # cantidad = Decimal(cantidad)

        try:
            cantidad = Decimal(cantidad)
        except Exception as ex:
            raise Exception("Solo se pueden ingresar numeros")

        if(moneda != "ARS"):
            raise Exception("Solo puede ingresar dinero en la cuenta en pesos Argentinos")
       
        if (cantidad <= 0):
            raise Exception("Ingrese una cantidad valida")
        # if not self.data_helper.maxMoneyAccount(cuenta,moneda,cantidad):
        #     raise Exception("No se puede ingresar mas dinero a la cuenta")
        if not self.data_helper.isCurrCodeValid(moneda):
            raise Exception("Ingrese un codigo de moneda valido")
        if not self.data_helper.AccountExist(moneda,cuenta):
            raise Exception("No tiene una cuenta abierta con esa moneda")

        # self.data_helper.addMoney(cuenta,moneda,cantidad)
        self.data_helper.addMoney(cuenta,moneda,cantidad)
        raise Exception("Se agrego el dinero")

    def buyCurrMoney(self, cuenta,cantidad, moneda):
        moneda = moneda.strip().upper()
        getcontext().prec = 100
        
        try:
            cantidad = Decimal(cantidad)
        except Exception as ex:
            raise Exception("Solo se pueden ingresar numeros")

        self.validaciones(moneda,cuenta,cantidad)

        conexion = self.data_helper.conexionApi(moneda)      
        cot_Moneda_X = self.data_helper.cotizacionMoneda(conexion,moneda)
        cot_Moneda_Peso = self.data_helper.cotizacionMoneda(conexion,"ARS")
        cot_peso_x = cot_Moneda_Peso/cot_Moneda_X

        saldo_peso = self.data_helper.getSaldo("ARS",cuenta)
   
        saldo = self.data_helper.getSaldo(moneda,cuenta)

        cantidad_A_Comprar = Decimal(cot_peso_x).quantize(Decimal('0.00')) * Decimal(cantidad).quantize(Decimal('0.00'))
        
        if cantidad_A_Comprar > saldo_peso:
            raise Exception("No tiene suficiente pesos argentinos para comprar esa moneda")
        # total_moneda_x = Decimal(cantidad_A_Comprar).quantize(Decimal('0.00')) / Decimal(cot_peso_x).quantize(Decimal('0.00'))

        self.data_helper.desacreditar_Dinero(saldo_peso,Decimal(cantidad_A_Comprar),"ARS",cuenta)
        self.data_helper.acreditar_Dinero(saldo,Decimal(cantidad),moneda,cuenta)

        raise Exception("Operacion Realizada")

    def validaciones(self,moneda,cuenta,cantidad):
        if not self.data_helper.isCurrCodeValid(moneda):
            raise Exception("Ingrese un codigo de moneda valido")
        if not self.data_helper.AccountExist(moneda,cuenta):
            raise Exception("No tiene una cuenta abierta en esa moneda")
        if (cantidad <= 0):
            raise Exception("Ingrese una cantidad valida")
        if (moneda == "ARS"):
            raise Exception("No puede comprar pesos argentinos con la misma moneda")

    def sellCurrMoney(self, cuenta,cantidad, moneda):
        moneda = moneda.strip().upper()
        getcontext().prec = 100
    
        try:
            cantidad = Decimal(cantidad)
        except Exception as ex:
            raise Exception("Solo se pueden ingresar numeros")

        self.validaciones(moneda,cuenta,cantidad)
        conexion = self.data_helper.conexionApi(moneda)      
        cot_Moneda_X = self.data_helper.cotizacionMoneda(conexion,moneda)
        cot_Moneda_Peso = self.data_helper.cotizacionMoneda(conexion,"ARS")
        cot_peso_x = cot_Moneda_Peso/cot_Moneda_X

        saldo = self.data_helper.getSaldo(moneda,cuenta)

        saldo_peso = self.data_helper.getSaldo("ARS",cuenta)
        cantidad_A_Comprar = Decimal(cot_peso_x).quantize(Decimal('0.00')) * Decimal(cantidad).quantize(Decimal('0.00'))
        
        if cantidad > saldo:
            raise Exception("No tiene suficiente moneda para comprar")
        
        # total_moneda_x = Decimal(cantidad_A_Comprar).quantize(Decimal('0.00')) / Decimal(cot_peso_x).quantize(Decimal('0.00'))

        self.data_helper.desacreditar_Dinero(saldo,Decimal(cantidad),moneda,cuenta)
        self.data_helper.acreditar_Dinero(saldo_peso,Decimal(cantidad_A_Comprar),"ARS",cuenta)
        raise Exception("Operacion Realizada")


#SECCION DEL LOGIN

class Verificacion:
    
    def __init__(self,contra,nombre):
        self.contra = contra.strip()
        self.nombre = nombre.lower().strip()
        self.data_helper = Administrador()

        
    def Verificador(self):
            try:
                contraV, nombreV = self.data_helper.ContraNombre(self.contra, self.nombre)
                if(contraV == self.contra and nombreV == self.nombre):
                    return True
                else:
                    raise Exception("Datos incorrectos")
            except Exception as ex:
                    raise Exception("Datos incorrectos")

class AgregarAdmin:
    
    def __init__(self,contra,contra2,nombre):
        self.contra = contra.strip()
        self.contra2 = contra2.strip()
        self.nombre = nombre.lower().strip()
        self.data_helper = Administrador()
        
    def Agregar(self):
        # MiAg = Agregador()
        AgrVar = self.data_helper.agregar(self.contra, self.contra2, self.nombre)
        if(AgrVar):
            raise Exception("Se agrego")
        else:
            raise Exception("Las contraseñas no coinciden")
            
class ModificarAdmin:
    def __init__(self,contra,contra2,nombre):
        self.contra = contra.strip()
        self.contra2 = contra2.strip()
        self.nombre = nombre.lower().strip()
        self.data_helper = Administrador()
    
    def modificar(self):

        # MiMod = Modificador()

        ModVar = self.data_helper.modificar(self.contra, self.contra2, self.nombre)
        if(ModVar):
            raise Exception("Se modifico el usuario")
        else:
            raise Exception("No se pudo modificar el usuario")