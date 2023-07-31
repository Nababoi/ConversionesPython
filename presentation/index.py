from business.admin import business_helper, Verificacion, ModificarAdmin, AgregarAdmin
import getpass
# from decimal import Decimal


def App():

    myadmin = business_helper()
    opcion = input("1-Crear usuario\n2-Iniciar sesion\n")
    if(opcion == "1"):
        try:
            nombre = input("Ingrese su nuevo usuario: ")
            contra = getpass.getpass("Ingrese su nueva contraseña: ")
            contra2 = getpass.getpass("Ingrese de nuevo su contraseña: ")
                                        
            agr = AgregarAdmin(contra, contra2, nombre)
            agr.Agregar()
        except Exception as e:
            print(e.args[0])
    elif(opcion == "2"):
        try:
            usuario = input("Ingrese el usuario\n")
            contra = getpass.getpass("Ingrese la contraseña\n")
            myVery = Verificacion(contra,usuario)
            if (myVery.Verificador()):
                print("Correcto")
            else:
                print("Datos incorrectos")
            print("Bienvenido")
            operacion = 0
            while(operacion != "3"):
                operacion = input("Ingrese el tipo de operacion que desea realizar:\n 1-Operaciones con la cuenta de bancaria\n 2-Operaciones con la cuenta de usuario\n 3-Salir\n")
                if(operacion == "1"):
                    addQuestion = 0
                    while(addQuestion != "5"):
                        addQuestion = input("Elija la accion a realizar\n 1-Depositar\n 2-Comprar\n 3-Vender\n 4-Abrir una cuenta\n 5-Salir\n")
                        if (addQuestion == "1"):
                            try:
                                moneda = input("En que cuenta desea depositar?\n")
                                cantidad = input("Ingrese la cantidad a depositar\n")
                                myadmin.addMoney(usuario,moneda,cantidad)
                            except Exception as e:
                                print(e.args[0])
                        if (addQuestion == "2"):
                            try:
                                moneda = input("Que moneda desea comprar?\n")
                                cantidad = input("Ingrese la cantidad de dinero\n")       
                                myadmin.buyCurrMoney(usuario,cantidad,moneda)
                            except Exception as e:
                                print(e.args[0])
                        if (addQuestion == "3"):
                            try:
                                moneda = input("Con que moneda comprar desea comprar pesos?\n")   
                                cantidad = input("Ingrese la cantidad a comprar\n")    
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
                    operacionUsuario = 1
                    while(operacionUsuario != "3"):
                        operacionUsuario = input("Que accion desea realizar:\n1-Agregar Usuario\n2-Modificar usuario\n3-Salir\n")       
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

            