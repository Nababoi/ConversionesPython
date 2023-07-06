from currencies import curr
from os import path
import json
import requests as rq
import bcrypt
from decimal import Decimal
from decimal import getcontext

class data_helper:

    def checkAccounts(self,username):
        filename = username + ".json"
        if path.exists(filename):
            if self.AccountExist("ARS",username)==True:
                return True
            else:
                return False
        with open(filename,"w") as f:
            account_des = {"ARS":"0.00"}
            account_ser = json.dumps(account_des,indent=4)
            f.write(account_ser)
            return True

    def isCurrCodeValid(self,currCode):
        if currCode in curr.keys():
            return True
        return False

    def AccountExist(self,currCode,username):
        filename = username + ".json"
        with open(filename,"r") as f:
            file_content = f.read()
            file_des=json.loads(file_content)
            if currCode in file_des.keys():
                return True
            else:
                return False

    def createAccount(self,curr_code,username):
        filename = username + ".json"
        accounts_des = {}
        with open(filename,"r") as f:
            file_content = f.read()
            accounts_des=json.loads(file_content)
        accounts_des.update({curr_code:"0.00"})
        with open(filename,"w") as f:
            accounts_ser = json.dumps(accounts_des,indent=4)
            f.write(accounts_ser)
            
    def maxMoneyAccount(self, cuenta, moneda, cantidad):
        archivo = cuenta + ".json"
        with open(archivo, "r") as f:
            cuentas = json.load(f)

        if moneda in cuentas:
            saldo = Decimal(cuentas[moneda])  # Convertir a Decimal
            if saldo + Decimal(cantidad) > Decimal("20000.00"):  # Convertir a Decimal
                return False
        return True



    def addMoney(self, cuenta, moneda, cantidad):
        archivo = cuenta + ".json"
        with open(archivo, "r") as f:
            cuentas = json.load(f)

        # if self.maxMoneyAccount(cuenta, moneda, cantidad) == False:
        #     return False
        # if self.isCurrCodeValid(moneda) == False:
        #     return False
        # if self.AccountExist(moneda, cuenta) == False:
        #     return False

        cantidad_decimal = Decimal(str(cantidad))
        cuentas[moneda] = str(Decimal(cuentas[moneda]) + cantidad_decimal)

        with open(archivo, "w") as f:
            json.dump(cuentas, f, indent=4)

    
    def buyCurrMoney(self, cuenta, cantidad, moneda):
        url = f"http://data.fixer.io/api/latest?access_key=74669fd726cfe6800dc093693542d376&symbols=ARS,{moneda}"
        response = rq.get(url)
        res_json = response.json()

        cot_peso_x = Decimal(res_json['rates']['ARS']) / Decimal(res_json['rates'][moneda])
        archivo = str(cuenta) + ".json"

        with open(archivo, "r") as f:
            cuentas = json.load(f)

        if not self.isCurrCodeValid(moneda):
            return False

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

    # def leerArchivo(self,cuenta, archivo):
    #     # archivo = f"{cuenta}.json"
    #     with open(archivo, "r") as f:
    #         cuenta = json.load(f)
    #     return cuenta

    def conexionApi(self,moneda):
        url = f"http://data.fixer.io/api/latest?access_key=74669fd726cfe6800dc093693542d376&symbols=ARS,{moneda}"
        response = rq.get(url)
        res_json = response.json()
        return res_json

    def cotizacionMoneda(self,datos,moneda):
        return Decimal(datos['rates'][moneda])
        

    # def sellCurrMoney(self, cuenta, cantidad, moneda):
    #     getcontext().prec = 100
    #     url = f"http://data.fixer.io/api/latest?access_key=74669fd726cfe6800dc093693542d376&symbols=ARS,{moneda}"
    #     response = rq.get(url)
    #     res_json = response.json()

       
    #     a=Decimal(res_json['rates'][moneda])
    #     b=Decimal(res_json['rates']['ARS'])  
    #     cot_peso_x = b/a
    #     print(cot_peso_x)
    #     archivo = f"{cuenta}.json"
        
    #     with open(archivo, "r") as f:
    #         cuenta = json.load(f)

    #     if moneda not in cuenta:
    #         raise Exception("No posee la cuenta origen")

    #     saldo_X = Decimal(cuenta[moneda])

    #     cantidad_A_acreditar = cot_peso_x * Decimal(cantidad)

    #     if Decimal(cantidad) > saldo_X:
    #         raise Exception("El saldo no es suficiente")

    #     saldo_restante = saldo_X - Decimal(cantidad)
    #     cuenta[moneda] = "{:.2f}".format(saldo_restante)

    #     saldo_restante = (Decimal(cuenta['ARS']) + cantidad_A_acreditar)
    #     cuenta['ARS'] = "{:.2f}".format(saldo_restante)

    #     with open(archivo, "w") as f:
    #         json.dump(cuenta, f, indent=4)
        
    #     raise Exception("Operacion exitosa")

#SECCION DEL LOGIN
class Login:
    def __init__(self):
        self.filepath="usuarios.json" 
        
    def ContraNombre(self,contra,nombre):
        with open(self.filepath, "r") as f:
            serObj = f.read()
            data = json.loads(serObj)
            for dato in data:
                contraV = dato["contra"]
                nombreV = dato["nombre"]
                if bcrypt.checkpw(contra.encode("utf-8"), contraV.encode("utf-8")):
                    if nombre == nombreV:
                        return contra, nombre
        return None, None


class Agregador:
    def __init__(self):
        self.filepath = "usuarios.json"
        
    def agregar(self,contra,contra2,nombre):
        if contra == contra2:
                with open(self.filepath, 'r') as f:  
                    serObj = f.read()
                    data = json.loads(serObj)
                nombreJson= set(usuario["nombre"] for usuario in data)
                if nombre in nombreJson:
                    raise Exception("El usuario ya existe")
                     
                contra_hash = bcrypt.hashpw(contra.encode("utf-8"), bcrypt.gensalt())
                data.append({"contra": contra_hash.decode("utf-8"), "nombre": nombre})

                with open(self.filepath, 'w') as f:
                    json.dump(data, f, indent=4)

                cuenta = f"{nombre}.json"

                datosCuenta = {
                    "ARS":"0.00"
                }

                with open(cuenta, 'w') as f:
                    json.dump(datosCuenta, f, indent=4)

                return True
        else:
                return False

class Modificador():
    
    def __init__(self):
        self.filepath = 'usuarios.json'

    def modificar(self,contra,contra2,nombre):
        with open(self.filepath, 'r') as f:
            serObj = f.read()
            data = json.loads(serObj)

        ok = False
        for item in data:
            contraM = item["contra"]
            nombreM = item["nombre"]
            if contra == contra2:
                if nombreM == nombre:
                    contra_hash = bcrypt.hashpw(contra.encode("utf-8"), bcrypt.gensalt())
                    item["contra"] = contra_hash.decode("utf-8")
                    ok = True

        if ok:
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=4)
                return True
        return False

