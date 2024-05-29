import magic
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError

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

@deconstructible
class CuitValidator(object):
    error_messages = {
    'cuit': ("CUIT incorrecto."),
}
    def __init__(self, cuit=None):
        self.cuit = cuit

    def __call__(self, cuit):
        if validar_cuit(cuit):
            return cuit

        raise ValidationError(self.error_messages['cuit'])

# Genera CUIL en base a número de DNI y Sexo.
# Uso:
#   get_cuil(DNI, M/F/S)

def get_cuil(document_number, gender):
    MALE = ('M', 'MALE', 'HOMBRE')
    FEMALE = ('F', 'FEMALE', 'MUJER')
    SOCIETY = ('S', 'SOCIETY', 'SOCIEDAD')

    if len(document_number) != 8 and document_number.isdigit():
        if len(document_number) == 7:
            document_number = ''.join(['0', document_number])
        else:
            raise ValidationError("DNI incorrecto.")

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

@deconstructible
class FileValidator(object):
    error_messages = {
     'max_size': ("Ensure this file size is not greater than %(max_size)s."
                  " Your file size is %(size)s."),
     'min_size': ("Ensure this file size is not less than %(min_size)s. "
                  "Your file size is %(size)s."),
     'content_type': "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size), 
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                   'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'], 
                                   'min_size', params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = { 'content_type': content_type }
                raise ValidationError(self.error_messages['content_type'],
                                   'content_type', params)
        return data

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator) and
            self.max_size == other.max_size and
            self.min_size == other.min_size and
            self.content_types == other.content_types
        )
