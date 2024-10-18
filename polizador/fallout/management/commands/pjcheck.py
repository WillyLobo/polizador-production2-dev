from django.core.management.base import BaseCommand, CommandError
from fallout.models import CharFallout, Raza
from django.contrib.auth.models import User


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

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """
        Checks if solicitud.solicitud_actuacion is correct.
        """
        atributos_primarios = [
        "Str",
        "Per",
        "Res",
        "Car",
        "Int",
        "Agi",
        "Sue"
        ]
        atributos_secundarios = [
        "ap",
        "sec",
        "danoMelee",
        "probCritico",
        "ratioCuracion",
        "capCarga",
        "resVeneno",
        "resRadiacion",
        "resElectricidad",
        "resGas",
        "implante"
        ]
        skill_list = [
        "armasPequenas",
        "armasGrandes",
        "armasEnergia",
        "desarmado",
        "armasMelee",
        "lanzar",
        "primerosAuxilios",
        "medicina",
        "sigilo",
        "ganzuas",
        "robar",
        "trampas",
        "ciencia",
        "reparar",
        "pilotar",
        "conversacion",
        "Trueque",
        "juego",
        "vidaAlAireLibre",
        "atletismo"
        ]

        # char = CharFallout.objects.get(id=1)
        # print(f"S: {char.StrTotal} - P: {char.PerTotal} - E: {char.ResTotal} - C: {char.CarTotal} - I: {char.IntTotal} - A: {char.AgiTotal} - L: {char.SueTotal}")
        # for skill in skill_list:
        #     base_skill = getattr(char, f"{skill}BaseSkill")
        #     points_skill = getattr(char, f"{skill}PointsSkill")
        #     total_skill = getattr(char, f"{skill}TotalSkill")
        #     mod = getattr(char, f"{skill}Mod")
        #     tag = getattr(char, f"{skill}Tag")

        #     print(f"{skill}: {base_skill} - {skill}PointsSkill: {points_skill} - {skill}TotalSkill: {total_skill} - {skill}Mod: {mod} - {skill}Tag: {tag}")
        jugador = User.objects.get(pk=1)
        raza = Raza.objects.get(pk=2)
        corcky = {"nombrePersonaje": "AutoCorcky", "nombreJugador": jugador,
                  "edadPersonaje": 218, "generoPersonaje": "Masculino", "razaPersonaje": raza, "alturaPersonaje": "1.73", "pesoPersonaje": 75, "faccionPersonaje": "Ninguna",
                  "nivelPersonaje": 1, "experienciaPersonaje": 0,
                  "karmaPersonaje": 0,
                #   "puntosGolpePorNivelBase": 1, "puntosGolpePorNivelMod": 1, "puntosGolpePorNivelTotal": 1,
                #   "puntosHabilidadPorNivelBase": 1, "puntosHabilidadPorNivelMod": 0, "puntosHabilidadPorNivelTotal": 0,
                #   "perksPorNivelBase": 1, "perksPorNivelMod": 0, "perksPorNivelTotal": 0,
                  "StrBase": 5,# "StrMod": 0, "StrTotal": 5,
                  "PerBase": 5,# "PerMod": 0, "PerTotal": 5,
                  "ResBase": 10,# "ResMod": 0, "ResTotal": 10,
                  "CarBase": 1,# "CarMod": 0, "CarTotal": 1,
                  "IntBase": 2,# "IntMod": 0, "IntTotal": 2,
                  "AgiBase": 6,# "AgiMod": 0, "AgiTotal": 6,
                  "SueBase": 12,# "SueMod": 0, "SueTotal": 12,
                #   "apBase": 8.0, "apMod": 0, "apTotal": 8.0,
                #   "secBase": 10, "secMod": 0, "secTotal": 10.0,
                #   "danoMeleeBase": 1, "danoMeleeMod": 0, "danoMeleeTotal": 1.0,
                #   "probCriticoBase": 12, "probCriticoMod": 0, "probCriticoTotal": 12.0,
                #   "ratioCuracionBase": 3.3333333333333335, "ratioCuracionMod": 0, "ratioCuracionTotal": 3.3333333333333335,
                #   "capCargaBase": 68.1, "capCargaMod": 0, "capCargaTotal": 68.1, 
                #   "resVenenoBase": 50, "resVenenoMod": 0, "resVenenoTotal": 50.0, 
                #   "resRadiacionBase": 20, "resRadiacionMod": 0, "resRadiacionTotal": 20.0, 
                #   "resElectricidadBase": 0, "resElectricidadMod": 0, "resElectricidadTotal": 0.0, 
                #   "resGasBase": 0, "resGasMod": 0, "resGasTotal": 0.0, 
                #   "implanteBase": 120, "implanteMod": 0, "implanteTotal": 120.0, 
                  "armasPequenasTag": False, # "armasPequenasBaseSkill": 29, "armasPequenasPointsSkill": 0, "armasPequenasTotalSkill": 29.0, "armasPequenasMod": 0, 
                  "armasGrandesTag": False, # "armasGrandesBaseSkill": 12, "armasGrandesPointsSkill": 0, "armasGrandesTotalSkill": 12.0, "armasGrandesMod": 0, 
                  "armasEnergiaTag": False, # "armasEnergiaBaseSkill": 12, "armasEnergiaPointsSkill": 0, "armasEnergiaTotalSkill": 12.0, "armasEnergiaMod": 0, 
                  "desarmadoTag": False, # "desarmadoBaseSkill": 52, "desarmadoPointsSkill": 0, "desarmadoTotalSkill": 52.0, "desarmadoMod": 0, 
                  "armasMeleeTag": True, # "armasMeleeBaseSkill": 62, "armasMeleePointsSkill": 0, "armasMeleeTotalSkill": 62.0, "armasMeleeMod": 0, 
                  "lanzarTag": False, # "lanzarBaseSkill": 24, "lanzarPointsSkill": 0, "lanzarTotalSkill": 24.0, "lanzarMod": 0, 
                  "primerosAuxiliosTag": False, # "primerosAuxiliosBaseSkill": 14, "primerosAuxiliosPointsSkill": 0, "primerosAuxiliosTotalSkill": 14.0, "primerosAuxiliosMod": 0, 
                  "medicinaTag": False, # "medicinaBaseSkill": 14, "medicinaPointsSkill": 0, "medicinaTotalSkill": 14.0, "medicinaMod": 0, 
                  "sigiloTag": False, # "sigiloBaseSkill": 23, "sigiloPointsSkill": 0, "sigiloTotalSkill": 23.0, "sigiloMod": 0, 
                  "ganzuasTag": True, # "ganzuasBaseSkill": 41, "ganzuasPointsSkill": 0, "ganzuasTotalSkill": 41.0, "ganzuasMod": 0, 
                  "robarTag": False, # "robarBaseSkill": 18, "robarPointsSkill": 0, "robarTotalSkill": 18.0, "robarMod": 0, 
                  "trampasTag": False, # "trampasBaseSkill": 11, "trampasPointsSkill": 0, "trampasTotalSkill": 11.0, "trampasMod": 0, 
                  "cienciaTag": False, # "cienciaBaseSkill": 8, "cienciaPointsSkill": 0, "cienciaTotalSkill": 8.0, "cienciaMod": 0, 
                  "repararTag": False, # "repararBaseSkill": 6, "repararPointsSkill": 0, "repararTotalSkill": 6.0, "repararMod": 0, 
                  "pilotarTag": False, # "pilotarBaseSkill": 22, "pilotarPointsSkill": 0, "pilotarTotalSkill": 22.0, "pilotarMod": 0, 
                  "conversacionTag": True, # "conversacionBaseSkill": 25, "conversacionPointsSkill": 0, "conversacionTotalSkill": 25.0, "conversacionMod": 0, 
                  "truequeTag": False, # "TruequeBaseSkill": 4, "TruequePointsSkill": 0, "TruequeTotalSkill": 4.0, "TruequeMod": 0, 
                  "juegoTag": False, # "juegoBaseSkill": 60, "juegoPointsSkill": 0, "juegoTotalSkill": 60.0, "juegoMod": 0, 
                  "vidaAlAireLibreTag": False, # "vidaAlAireLibreBaseSkill": 24, "vidaAlAireLibrePointsSkill": 0, "vidaAlAireLibreTotalSkill": 24.0, "vidaAlAireLibreMod": 0, 
                  "atletismoTag": True, #"atletismoBaseSkill": 47, "atletismoPointsSkill": 0, "atletismoTotalSkill": 47.0, "atletismoMod": 0, 
                  }
        char = CharFallout(**corcky)
        char.save()

        # {"model": "fallout.charfallout", "pk": 1, "fields": {"nombrePersonaje": "Corcky", "nombreJugador": 1, "edadPersonaje": 218, "generoPersonaje": "Masculino", "razaPersonaje": 2, "alturaPersonaje": "1.73", "pesoPersonaje": 75, "faccionPersonaje": "Ninguna", "nivelPersonaje": 1, "experienciaPersonaje": 0, "karmaPersonaje": 0, "puntosGolpePorNivelBase": 1, "puntosGolpePorNivelMod": 1, "puntosGolpePorNivelTotal": 1, "puntosHabilidadPorNivelBase": 1, "puntosHabilidadPorNivelMod": 0, "puntosHabilidadPorNivelTotal": 0, "perksPorNivelBase": 1, "perksPorNivelMod": 0, "perksPorNivelTotal": 0, "StrStat": 5, "StrMod": 0, "StrTotal": 5, "PerStat": 5, "PerMod": 0, "PerTotal": 5, "ResStat": 10, "ResMod": 0, "ResTotal": 10, "CarStat": 1, "CarMod": 0, "CarTotal": 1, "IntStat": 2, "IntMod": 0, "IntTotal": 2, "AgiStat": 6, "AgiMod": 0, "AgiTotal": 6, "SueStat": 12, "SueMod": 0, "SueTotal": 12, "apBase": 8.0, "apMod": 0, "apTotal": 8.0, "secBase": 10, "secMod": 0, "secTotal": 10.0, "danoMeleeBase": 1, "danoMeleeMod": 0, "danoMeleeTotal": 1.0, "probCriticoBase": 12, "probCriticoMod": 0, "probCriticoTotal": 12.0, "ratioCuracionBase": 3.3333333333333335, "ratioCuracionMod": 0, "ratioCuracionTotal": 3.3333333333333335, "capCargaBase": 68.1, "capCargaMod": 0, "capCargaTotal": 68.1, "resVenenoBase": 50, "resVenenoMod": 0, "resVenenoTotal": 50.0, "resRadiacionBase": 20, "resRadiacionMod": 0, "resRadiacionTotal": 20.0, "resElectricidadBase": 0, "resElectricidadMod": 0, "resElectricidadTotal": 0.0, "resGasBase": 0, "resGasMod": 0, "resGasTotal": 0.0, "implanteBase": 120, "implanteMod": 0, "implanteTotal": 120.0, "armasPequenasBaseSkill": 29, "armasPequenasPointsSkill": 0, "armasPequenasTotalSkill": 29.0, "armasPequenasMod": 0, "armasPequenasTag": False, "armasGrandesBaseSkill": 12, "armasGrandesPointsSkill": 0, "armasGrandesTotalSkill": 12.0, "armasGrandesMod": 0, "armasGrandesTag": False, "armasEnergiaBaseSkill": 12, "armasEnergiaPointsSkill": 0, "armasEnergiaTotalSkill": 12.0, "armasEnergiaMod": 0, "armasEnergiaTag": False, "desarmadoBaseSkill": 52, "desarmadoPointsSkill": 0, "desarmadoTotalSkill": 52.0, "desarmadoMod": 0, "desarmadoTag": False, "armasMeleeBaseSkill": 62, "armasMeleePointsSkill": 0, "armasMeleeTotalSkill": 62.0, "armasMeleeMod": 0, "armasMeleeTag": True, "lanzarBaseSkill": 24, "lanzarPointsSkill": 0, "lanzarTotalSkill": 24.0, "lanzarMod": 0, "lanzarTag": False, "primerosAuxiliosBaseSkill": 14, "primerosAuxiliosPointsSkill": 0, "primerosAuxiliosTotalSkill": 14.0, "primerosAuxiliosMod": 0, "primerosAuxiliosTag": False, "medicinaBaseSkill": 14, "medicinaPointsSkill": 0, "medicinaTotalSkill": 14.0, "medicinaMod": 0, "medicinaTag": False, "sigiloBaseSkill": 23, "sigiloPointsSkill": 0, "sigiloTotalSkill": 23.0, "sigiloMod": 0, "sigiloTag": False, "ganzuasBaseSkill": 41, "ganzuasPointsSkill": 0, "ganzuasTotalSkill": 41.0, "ganzuasMod": 0, "ganzuasTag": True, "robarBaseSkill": 18, "robarPointsSkill": 0, "robarTotalSkill": 18.0, "robarMod": 0, "robarTag": False, "trampasBaseSkill": 11, "trampasPointsSkill": 0, "trampasTotalSkill": 11.0, "trampasMod": 0, "trampasTag": False, "cienciaBaseSkill": 8, "cienciaPointsSkill": 0, "cienciaTotalSkill": 8.0, "cienciaMod": 0, "cienciaTag": False, "repararBaseSkill": 6, "repararPointsSkill": 0, "repararTotalSkill": 6.0, "repararMod": 0, "repararTag": False, "pilotarBaseSkill": 22, "pilotarPointsSkill": 0, "pilotarTotalSkill": 22.0, "pilotarMod": 0, "pilotarTag": False, "conversacionBaseSkill": 25, "conversacionPointsSkill": 0, "conversacionTotalSkill": 25.0, "conversacionMod": 0, "conversacionTag": True, "TruequeBaseSkill": 4, "TruequePointsSkill": 0, "TruequeTotalSkill": 4.0, "TruequeMod": 0, "TruequeTag": False, "juegoBaseSkill": 60, "juegoPointsSkill": 0, "juegoTotalSkill": 60.0, "juegoMod": 0, "juegoTag": False, "vidaAlAireLibreBaseSkill": 24, "vidaAlAireLibrePointsSkill": 0, "vidaAlAireLibreTotalSkill": 24.0, "vidaAlAireLibreMod": 0, "vidaAlAireLibreTag": False, "atletismoBaseSkill": 47, "atletismoPointsSkill": 0, "atletismoTotalSkill": 47.0, "atletismoMod": 0, "atletismoTag": True}}