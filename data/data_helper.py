from currencies import curr
from os import path
import json
import requests as rq
import bcrypt
from decimal import Decimal
# from decimal import getcontext
import os

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

    def getJson(self,cuenta):
        archivo = cuenta + ".json"
        return archivo

    def getUsuario(self, user):
        archivo = user + ".json"
        if os.path.exists(archivo):
            with open(archivo, "r") as f:
                datos_usuario = json.load(f)
            return datos_usuario.get("usuario")

    def getSaldo(self,moneda,user):
        archivo = self.getJson(user)
        with open(archivo, "r") as f:
            cuenta = json.load(f)
        saldo_X = Decimal(cuenta[moneda])
        return saldo_X

    def addMoney(self,cuenta,moneda,cantidad):
        archivo = self.getJson(cuenta)

        with open(archivo, "r") as f:
            cuentas = json.load(f)

        cantidad_decimal = Decimal(str(cantidad))
        cuentas[moneda] = str(Decimal(cuentas[moneda]) + cantidad_decimal)
        
        with open(archivo, "w") as f:
            json.dump(cuentas, f, indent=4)

    def maxMoneyAccount(self, cuenta, moneda, cantidad):
        archivo = self.getJson(cuenta)
        with open(archivo, "r") as f:
            cuentas = json.load(f)

        if moneda in cuentas:
            saldo = Decimal(cuentas[moneda]) 
            if saldo + Decimal(cantidad) > Decimal("20000.00"): 
                return False
        return True

    def getSaldo(self,moneda,user):
        archivo = self.getJson(user)
        with open(archivo, "r") as f:
            cuenta = json.load(f)
        saldo_X = Decimal(cuenta[moneda])
        return saldo_X

    def desacreditar_Dinero(self, saldo, monto, moneda, usuario):
        saldo = self.getSaldo(moneda, usuario)        
        archivo = usuario + ".json"
        with open(archivo, "r") as f:
            cuentas = json.load(f)

        saldoTotal = Decimal(saldo) - Decimal(monto)
        cuentas[moneda] = "{:.2f}".format(saldoTotal)  # Actualiza el saldo de la moneda con 2 decimales

        with open(archivo, "w") as f:
            json.dump(cuentas, f, indent=4)

    def acreditar_Dinero(self, saldo, monto, moneda, usuario):
        saldo = self.getSaldo(moneda, usuario)        
        archivo = usuario + ".json"
        with open(archivo, "r") as f:
            cuentas = json.load(f)

        saldoTotal = Decimal(saldo) + Decimal(monto)
        cuentas[moneda] = "{:.2f}".format(saldoTotal)  # Actualiza el saldo de la moneda con 2 decimales

        with open(archivo, "w") as f:
            json.dump(cuentas, f, indent=4)


    def conexionApi(self,moneda):
        
        # url = f"http://data.fixer.io/api/latest?access_key=27bc953cfda45f1f9fa6131efa757947&symbols=ARS,{moneda}"
        url = f"http://data.fixer.io/api/latest?access_key=17d5c13ee70b7ca3cf18d12c8be1b96f&symbols=ARS,{moneda}"
        response = rq.get(url)
        res_json = response.json()
        return res_json

    def cotizacionMoneda(self,datos,moneda):
        return Decimal(datos['rates'][moneda])

#SECCION DEL LOGIN
class Administrador:
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

