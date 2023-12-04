from currencies import curr
# import json
import requests as rq
import bcrypt
from decimal import Decimal
# from decimal import getcontext
import sqlobject as SO

#Creacion de tablas con su respectiva conexion
database = 'mysql://root:root@localhost:3307/pythonorm'
__connection__ = SO.connectionForURI(database)

class Usuario(SO.SQLObject):

    usuario = SO.StringCol(length = 40, varchar = True, unique = True)
    contra = SO.StringCol(length = 120, varchar = True)
    cuentas = SO.MultipleJoin('Cuenta')
Usuario._connection = __connection__
# Usuario.dropTable(ifExists = True)
# Usuario.createTable()

class Currency(SO.SQLObject):
    
    currencyCode = SO.StringCol(length = 3, varchar = True)
    cuentas = SO.MultipleJoin('Cuenta')
Currency._connection = __connection__
    # Currency.dropTable(ifExists = True)
    # Currency.createTable()

# codigos = curr.keys()
# for cod in codigos:
#     Currency(currencyCode = cod)

class Cuenta(SO.SQLObject):

    currency = SO.ForeignKey('Currency', default="None", cascade=True)
    usuario = SO.ForeignKey('Usuario', default="None", cascade=True, dbName='usuario')
    cantidad = SO.DecimalCol(size=8, precision=2, default="0.00")
    
Cuenta._connection = __connection__
# Cuenta.dropTable(ifExists = True)
# Cuenta.createTable()


#SECCION DEL ADMINISTRADOR(AGREGAR,MODIFICAR,VERIFICAR)

class Administrador:
    def ContraNombre(self, pwd, nombre):
        usuario_encontrado = Usuario.selectBy(usuario=nombre).getOne()
        # try:
        contraseña_encriptada = usuario_encontrado.contra.encode('utf-8')

        if usuario_encontrado.usuario == nombre and bcrypt.checkpw(pwd.encode('utf-8'), contraseña_encriptada):
            return pwd, nombre
        else:
            return None, None
        # except SO.SQLObjectNotFound:
        #     return None, None

    def modificar(self,pwd,contra2,nombre):
            usuario_encontrado = Usuario.selectBy(usuario=nombre).getOne()
            try:
                contra_hash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
                nueva_contra = contra_hash.decode("utf-8")

                if(nombre == usuario_encontrado.usuario):
                    if(pwd == contra2):
                        usuario_encontrado.contra = nueva_contra
                        return True
                return False       
            except SO.SQLObjectNotFound:
                return False
            

    def agregar(self,contra,contra2,nombre):
        if contra == contra2:
            contra_hash = bcrypt.hashpw(contra.encode("utf-8"), bcrypt.gensalt())
            contra_hash_str = contra_hash.decode("utf-8")
            nuevo_usuario = Usuario(usuario=nombre, contra=contra_hash_str)
            nuevo_usuario.sync() 
            usuario_id = nuevo_usuario.id
            # print(contra_hash_str)
            # data.append({"contra": contra_hash.decode("utf-8"), "nombre": nombre})
            Cuenta(currency=340, usuario=usuario_id, cantidad="0.00")
            return True
        else:
            return False

class data_helper:

    def isCurrCodeValid(self,currCode):
        if currCode in curr.keys():
            return True
        return False

    def AccountExist(self,curr_code,username):
        
        currency_obj = Currency.selectBy(currencyCode=curr_code).getOne()
        usuario_obj = Usuario.selectBy(usuario=username).getOne()
        nuevaCuenta = Cuenta.selectBy(currency=currency_obj, usuario=usuario_obj).count()
        return nuevaCuenta > 0

    def createAccount(self,curr_code,username):

        currency_obj = Currency.selectBy(currencyCode=curr_code).getOne()
        usuario_obj = Usuario.selectBy(usuario=username).getOne()
        nuevaCuenta = Cuenta(currency=currency_obj, usuario=usuario_obj)

    def getSaldo(self, moneda, user):
        currency_obj = self.objectoMoneda(moneda)
        usuario_obj = self.objectoUsuario(user)

        cuenta_obj_peso = Cuenta.selectBy(currency=currency_obj, usuario=usuario_obj).getOne()
        saldo = cuenta_obj_peso.cantidad
        return saldo


    def addMoney(self, user, moneda, monto):

        currency_obj = Currency.selectBy(currencyCode=moneda).getOne()
        usuario_obj = Usuario.selectBy(usuario=user).getOne()
        cuenta_obj = Cuenta.selectBy(currency=currency_obj, usuario=usuario_obj).getOne()
        cuenta_obj.cantidad += Decimal(monto)
        cuenta_obj.sync()

    def getSaldo(self,moneda,user):
        currency_obj = self.objectoMoneda(moneda)
        usuario_obj = self.objectoUsuario(user)

        cuenta_obj_peso = Cuenta.selectBy(currency=currency_obj, usuario=usuario_obj).getOne()
        saldo = cuenta_obj_peso.cantidad
        return saldo

    def getUsuario(self,user):
        usuario_obj = Usuario.selectBy(usuario=user).getOne()
        usuario_id = usuario_obj.id
        return usuario_id

    def objectoMoneda(self,moneda):
        currency_obj = Currency.selectBy(currencyCode=moneda).getOne()
        return currency_obj

    def objectoUsuario(self,user):
        usuario_obj = Usuario.selectBy(usuario=user).getOne()
        return usuario_obj

    def conexionApi(self,moneda):
        # url = f"http://data.fixer.io/api/latest?access_key=27bc953cfda45f1f9fa6131efa757947&symbols=ARS,{moneda}"

        url = f"http://data.fixer.io/api/latest?access_key=17d5c13ee70b7ca3cf18d12c8be1b96f&symbols=ARS,{moneda}"
        response = rq.get(url)
        res_json = response.json()
        return res_json

    def acreditar_Dinero(self, saldo, monto, moneda, usuario):
        usuario_obj = self.getUsuario(usuario)
        currency_obj = self.objectoMoneda(moneda)

        monto = Decimal(saldo) + Decimal(monto)
        resultado = Cuenta.select(SO.AND((Cuenta.q.currency == currency_obj), (Cuenta.q.usuario == usuario_obj)))
        cuenta = resultado[0]
        cuenta.cantidad = monto 
        return cuenta

    def desacreditar_Dinero(self, saldo, monto, moneda, usuario):
        usuario_obj = self.getUsuario(usuario)
        currency_obj = self.objectoMoneda(moneda)
        monto = Decimal(saldo) - Decimal(monto)
        resultado = Cuenta.select(SO.AND((Cuenta.q.currency == currency_obj), (Cuenta.q.usuario == usuario_obj)))
        cuenta = resultado[0]
        cuenta.cantidad = monto
        return cuenta

    def cotizacionMoneda(self,datos,moneda):
        return Decimal(datos['rates'][moneda])


