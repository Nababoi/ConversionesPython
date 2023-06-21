from data.data_helper import data_helper, Login, Modificador, Agregador

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
        if not self.data_helper.isCurrCodeValid(moneda):
            raise Exception("Ingrese un codigo de moneda valido")
        if (cantidad <= 0):
            raise Exception("Ingrese una cantidad valida")
        self.data_helper.buyCurrMoney(cuenta,cantidad,moneda)

    def sellCurrMoney(self, cuenta,cantidad, moneda):
        moneda = moneda.strip().upper()
        if not self.data_helper.isCurrCodeValid(moneda):
            raise Exception("Ingrese un codigo de moneda valido")
        if (cantidad <= 0):
            raise Exception("Ingrese una cantidad valida")
        self.data_helper.sellCurrMoney(cuenta,cantidad,moneda)

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