from django.core.management.base import BaseCommand, CommandError
from fallout.models import Raza

# class Style:
#     def ERROR(self, text: str) -> str: ...
#     def SUCCESS(self, text: str) -> str: ...
#     def WARNING(self, text: str) -> str: ...
#     def NOTICE(self, text: str) -> str: ...
#     def SQL_FIELD(self, text: str) -> str: ...
#     def SQL_COLTYPE(self, text: str) -> str: ...
#     def SQL_KEYWORD(self, text: str) -> str: ...
#     def SQL_TABLE(self, text: str) -> str: ...
#     def HTTP_INFO(self, text: str) -> str: ...
#     def HTTP_SUCCESS(self, text: str) -> str: ...
#     def HTTP_REDIRECT(self, text: str) -> str: ...
#     def HTTP_NOT_MODIFIED(self, text: str) -> str: ...
#     def HTTP_BAD_REQUEST(self, text: str) -> str: ...
#     def HTTP_NOT_FOUND(self, text: str) -> str: ...
#     def HTTP_SERVER_ERROR(self, text: str) -> str: ...
#     def MIGRATE_HEADING(self, text: str) -> str: ...
#     def MIGRATE_LABEL(self, text: str) -> str: ...
#     def ERROR_OUTPUT(self, text: str) -> str: ...

# class Perks:
#     def __init__(self, perkNombre, perkDescripcion, perkRequisitosTX, perkRequisitoNivel, perkNivel, perkCalculo):
#         self.perkNombre = perkNombre
#         self.perkDescripcion = perkDescripcion
#         self.perkRequisitosTX = perkRequisitosTX
#         self.perkRequisitoNivel = perkRequisitoNivel
#         self.perkNivel = perkNivel
#         self.perkCalculo = perkCalculo

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        razas = [
            "Humano",
            "Ghoul",
            "Super Mutante",
            "Robot",
            "Garra Mortal"
        ]
        for raza in razas:
            Raza.objects.create(raza_tipo=raza)
        
        perks = [
            {
                "perkNombre": "Black Widow (Viuda Negra)",
                "perkDescripcion": "Ganas +10% de daño cuando te enfrentas al sexo masculino.",
                "perkRequisitosTX": "Nivel 2, Personaje Femenino",
                "perkRequisitoNivel": 2,
                "perkNivel": 0,
                "perkCalculo": 0
            },
            {
                "perkNombre": "Lady Killer (Asesino de Mujeres)",
                "perkDescripcion": "Ganas +10% de daño cuando te enfrentas al sexo femenino.",
                "perkRequisitosTX": "Nivel 2, Personaje Masculino",
                "perkRequisitoNivel": 2,
                "perkNivel": 0,
                "perkCalculo": 0
            },
            {
                "perkNombre": "Daddy’s Boy/ Girl (Niño/Niña de Papa)",
                "perkDescripcion": "Al igual que tu padre has dedicado tu tiempo a incrementar tus habilidades intelectuales. Ganas +10% a Ciencia; Primeros Auxilios y Doctor.",
                "perkRequisitosTX": "Nivel 2, Inteligencia 4",
                "perkRequisitoNivel": 2,
                "perkNivel": 0,
                "perkCalculo": 0
            },
            {
                "perkNombre": "",
                "perkDescripcion": "",
                "perkRequisitosTX": "",
                "perkRequisitoNivel": 0,
                "perkNivel": 1,
                "perkCalculo": 0
            },
        ]