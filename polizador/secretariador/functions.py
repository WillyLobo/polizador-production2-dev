def validar_cuit(cuit):
    cuit = cuit.replace("-", "") # remuevo las barras

    # validaciones minimas
    if len(cuit) != 11:
        return False

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    # calculo el digito verificador:
    aux = 0
    for i in range(10):
        aux += int(cuit[i]) * base[i]

    aux = 11 - (aux - (int(aux / 11) * 11))

    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(cuit[10])

# Genera CUIL en base a número de DNI y Sexo.
# Uso:
#   get_cuil(DNI, M/F/S)

class DNIIncorrecto(Exception):
    pass

def get_cuil(document_number, gender):
    MALE = ('M', 'MALE', 'HOMBRE')
    FEMALE = ('F', 'FEMALE', 'MUJER')
    SOCIETY = ('S', 'SOCIETY', 'SOCIEDAD')

    if len(document_number) != 8 and document_number.isdigit():
        if len(document_number) == 7:
            document_number = ''.join(['0', document_number])
        else:
            raise DNIIncorrecto(u"document_number incorrect")

    gender = gender.upper()
    if gender in MALE:
        AB = '20'
    elif gender in FEMALE:
        AB = '27'
    else:
        AB = '30'

    #############
    # Los numeros (excepto los dos primeros) que le tengo que
    # multiplicar a la cadena formada por el prefijo y por el
    # numero de documento los tengo almacenados en un arreglo.
    #############
    multipliers = [3, 2, 7, 6, 5, 4, 3, 2]

    # Realizo las dos primeras multiplicaciones por separado.
    calculation = (int(AB[0]) * 5) + (int(AB[1]) * 4)
    for i, digit in enumerate(document_number):
        calculation += (int(digit) * multipliers[i])

    # Mod is calculated here
    rest = calculation % 11

    #############
    # Llevo a cabo la evaluacion de las tres condiciones para
    # determinar el valor de C y conocer el valor definitivo de
    # AB.
    #############

    if gender not in SOCIETY and rest == 1:
        if gender in MALE:
            C = '9'
        else:
            C = '4'
        AB = '23'
    elif rest == 0:
        C = '0'
    else:
        C = 11 - rest

    print (f"{AB}-{document_number}-{C}")

    return f"{AB}{document_number}{C}"
