from business.admin import business_helper, Verificacion, ModificarAdmin, AgregarAdmin
from data.data_helper import data_helper, Login
import getpass
from decimal import Decimal

def App():
    myadmin = business_helper()
    try:
        usuario = input("Ingrese el usuario\n")
        contra = getpass.getpass("Ingrese la contraseña\n")
        myVery = Verificacion(contra,usuario)
        if (myVery.Verificador()):
            print("Correcto")
        else:
            print("Datos incorrectos")
            
        print("Bienvenido")
        operacion = input("Ingrese el tipo de operacion que desea realizar:\n 1-Operaciones con la cuenta de bancaria\n 2-Operaciones con la cuenta de usuario\n")
        if(operacion == "1"):

            addQuestion = input("Elija la accion a realizar\n 1-Depositar\n 2-Comprar\n 3-Vender\n 4-Abrir una cuenta\n")
            if (addQuestion == "1"):
                try:
                    moneda = input("En que cuenta desea depositar?\n")
                    cantidad = Decimal(input("Ingrese la cantidad a depositar\n"))
                    myadmin.addMoney(usuario,moneda,cantidad)
                except Exception as e:
                    print(e.args[0])
            if (addQuestion == "2"):
                try:
                    moneda = input("Que moneda desea comprar?\n")
                    cantidad = Decimal(input("Ingrese la cantidad de dinero\n"))        
                    myadmin.buyCurrMoney(usuario,cantidad,moneda)
                except Exception as e:
                    print(e.args[0])
            if (addQuestion == "3"):
                try:
                    moneda = input("Con que moneda comprar desea comprar pesos?\n")   
                    cantidad = Decimal(input("Ingrese la cantidad de dinero de pesos a comprar\n"))       
                    myadmin.sellCurrMoney(usuario,cantidad,moneda)
                except Exception as e:
                    print(e.args[0])
                    
            if (addQuestion == "4"):
                    try:
                        cuenta = input("Ingrese el codigo de la moneda\n")   
                        myadmin.createAccount(cuenta,usuario)
                    except Exception as e:
                        print(e.args[0])
        elif(operacion == "2"):
            operacionUsuario = input("Que accion desea realizar:\n1-Agregar Usuario\n2-Modificar usuario\nenter-Salir\n")
            if(operacionUsuario == "1"):
                    try:  
                        nombre = input("Ingrese su nuevo usuario: ")
                        contra = getpass.getpass("Ingrese su nueva contraseña: ")
                        contra2 = getpass.getpass("Ingrese de nuevo su contraseña: ")
                        
                        agr = AgregarAdmin(contra, contra2, nombre)
                        agr.Agregar()
                    except Exception as e:
                        print(e.args[0])
                    
            elif(operacionUsuario == "2"):
                    try:
                        nombre = input("Ingrese el usuario a modificar: ")
                        contra = getpass.getpass("Ingrese la nueva contraseña: ")
                        contra2 = getpass.getpass("Ingrese de nuevo la nueva contraseña: ")
                        
                        Mimod = ModificarAdmin(contra, contra2, nombre)
                        Mimod.modificar()
                    except Exception as e:
                        print(e.args[0])
    except Exception as e:
        print(e.args[0])

        