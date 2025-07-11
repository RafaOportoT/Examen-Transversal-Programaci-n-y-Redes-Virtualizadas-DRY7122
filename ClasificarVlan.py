# clasificar_vlan.py

# Solicita al usuario el número de VLAN
try:
    vlan = int(input("Ingrese el número de VLAN: "))

    if 1 <= vlan <= 1005:
        print("La VLAN ingresada pertenece al rango NORMAL.")
    elif 1006 <= vlan <= 4094:
        print("La VLAN ingresada pertenece al rango EXTENDIDO.")
    else:
        print("Número de VLAN fuera de rango. Debe estar entre 1 y 4094.")
except ValueError:
    print("Entrada inválida. Debe ingresar un número entero.")
