from django.db import models
from django.db.models.lookups import GreaterThan, LessThan
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.dispatch import receiver

def skill_up(habilidad_total, habilidad_puntos, tagged):
    habilidad_total = float(habilidad_total)
    habilidad_puntos = int(habilidad_puntos)
    """
    Corcky:
        Melee = 46 base * 2 tageado (92)
        Puntos por nivel = 11
        Nivel = 18
        Puntos de Habilidad = 11 * 18 = 198
    """
    for _ in range(habilidad_puntos):
        if habilidad_total <= 0:
            return 0, 0
        
        incrementos = [
            (200, 1/6),
            (175, 1/5),
            (150, 1/4),
            (125, 1/3),
            (100, 1/2),
            (0, 1)
        ]
        
        for limite, incremento in incrementos:
            if habilidad_total > limite:
                if tagged == True:
                    habilidad_total += incremento*2
                else:
                    habilidad_total += incremento
                break
        
    return habilidad_total


class Raza(models.Model):
    raza_tipo = models.CharField("Raza", max_length=30)

    def __str__(self):
        return self.raza_tipo

# class Perks(models.Model):
#     perkNombre = models.CharField("Perk", max_length=100)
#     perkDescripcion = models.TextField("Descripción")
#     perkRequisitosTX = models.CharField("Requisitos", max_length=250, default="")
#     perkRequisitoNivel = models.IntegerField("Nivel", default=1, validators=[MinValueValidator(1)])
#     perkNivel = models.IntegerField("Nivel", default=0, validators=[MinValueValidator(0)])
#     perkCalculo = models.CharField("Cálculo", max_length=100)

#     def __str__(self):
#         return self.perkNombre

class CharFallout(models.Model):
    """
    Campos a agregar:
        - resVeneno
        - resRadiacion
        - resElectricidad
        - resGas
        - resDanoNormal
        - resDanoLaser
        - resDanoFuego
        - resDanoPlasma
        - resDanoExplosivo
        - danoArmasPequenas
        - danoArmasGrandes
        - danoArmasEnergia
        - danoLanzar
        - danoDesarmado
        - danoMelee
        - condHeridoCritico (menos de 20% de HP)
        - condHeridoMedio (menos de 50% de HP)
        - condBorracho
        - statPool = models.IntegerField("Puntos S.P.E.C.I.A.L.", default=0, validators=[MinValueValidator(0)])

    """
    # Datos Generales
    nombrePersonaje = models.CharField("Nombre del Personaje", max_length=60)
    nombreJugador = models.ForeignKey(User, on_delete=models.CASCADE)
    edadPersonaje = models.IntegerField(
        "Edad", validators=[MinValueValidator(1)])
    generoPersonaje = models.CharField("Género", max_length=15)
    razaPersonaje = models.ForeignKey("Raza", verbose_name="Raza", on_delete=models.CASCADE)
    alturaPersonaje = models.DecimalField(
        "Altura", max_digits=3, decimal_places=2, default=1)
    pesoPersonaje = models.IntegerField(
        "Peso", validators=[MinValueValidator(1)])

    # Status
    faccionPersonaje = models.CharField(
        "Faccion/Alianza", max_length=60, blank=True, default="Ninguna")
    nivelPersonaje = models.IntegerField(
        "Nivel", default=1, validators=[MinValueValidator(1)])
    experienciaPersonaje = models.IntegerField(
        "Experiencia", default=0, validators=[MinValueValidator(0)])
    karmaPersonaje = models.IntegerField("Karma", default=0)
    puntosGolpePorNivelBase = models.DecimalField("PG/Nivel (3+(RE/2)) »",
                                         max_digits=5, decimal_places=1, default=1, validators=[MinValueValidator(1)])
    puntosGolpePorNivelMod = models.DecimalField("PG/Nivel Mod »",
                                         max_digits=5, decimal_places=1, default=0, validators=[MinValueValidator(0)])
    puntosGolpePorNivelTotal = models.DecimalField("PG/Nivel Total »",
                                         max_digits=5, decimal_places=1, default=0, validators=[MinValueValidator(0)])
    puntosHabilidadPorNivelBase = models.DecimalField(verbose_name="PH/Nivel (5+(2*IN)) »",
                                         max_digits=5, decimal_places=1, default=1, validators=[MinValueValidator(1)])
    puntosHabilidadPorNivelMod = models.DecimalField(verbose_name="PH Mod »",
                                         max_digits=5, decimal_places=1, default=0, validators=[MinValueValidator(0)])
    puntosHabilidadPorNivelTotal = models.DecimalField(verbose_name="PH Total »",
                                         max_digits=5, decimal_places=1, default=0, validators=[MinValueValidator(0)])
    perksPorNivelBase = models.DecimalField(
        "Perks/Nivel »", max_digits=3, decimal_places=1, default=1, validators=[MinValueValidator(0)]
    )
    perksPorNivelMod = models.DecimalField(
        "Perks Mod »", max_digits=3, decimal_places=1, default=0, validators=[MinValueValidator(0)]
    )
    perksPorNivelTotal = models.DecimalField(
        "Perks Total »", max_digits=3, decimal_places=1, default=0, validators=[MinValueValidator(0)]
    )

    # Stats Primarios
    StrBase = models.IntegerField("FU-", validators=[
                                  MinValueValidator(0)], default=1)
    StrMod = models.IntegerField("Fuerza Mod", validators=[
                                 MinValueValidator(0)], default=0)
    StrTotal = models.IntegerField("Fuerza Total", validators=[
                                   MinValueValidator(0)], default=1)

    PerBase = models.IntegerField("PE-", validators=[
                                  MinValueValidator(0)], default=1)
    PerMod = models.IntegerField("Percepción Mod", validators=[
                                 MinValueValidator(0)], default=0)
    PerTotal = models.IntegerField("Percepción Total", validators=[
                                   MinValueValidator(0)], default=1)

    ResBase = models.IntegerField("RE-", validators=[
                                  MinValueValidator(0)], default=1)
    ResMod = models.IntegerField("Resistencia Mod", validators=[
                                 MinValueValidator(0)], default=0)
    ResTotal = models.IntegerField("Resistencia Total", validators=[
                                   MinValueValidator(0)], default=1)

    CarBase = models.IntegerField("CA-", validators=[
                                  MinValueValidator(0)], default=1)
    CarMod = models.IntegerField("Carisma Mod", validators=[
                                 MinValueValidator(0)], default=0)
    CarTotal = models.IntegerField("Carisma Total", validators=[
                                   MinValueValidator(0)], default=1)

    IntBase = models.IntegerField("IN-", validators=[
                                  MinValueValidator(0)], default=1)
    IntMod = models.IntegerField("Inteligencia Mod", validators=[
                                 MinValueValidator(0)], default=0)
    IntTotal = models.IntegerField("Inteligencia Total", validators=[
                                   MinValueValidator(0)], default=1)

    AgiBase = models.IntegerField("AG-", validators=[
                                  MinValueValidator(0)], default=1)
    AgiMod = models.IntegerField("Agilidad Mod", validators=[
                                 MinValueValidator(0)], default=0)
    AgiTotal = models.IntegerField("Agilidad Total", validators=[
                                   MinValueValidator(0)], default=1)

    SueBase = models.IntegerField("SU-", validators=[
                                  MinValueValidator(0)], default=1)
    SueMod = models.IntegerField("Suerte Mod", validators=[
                                 MinValueValidator(0)], default=0)
    SueTotal = models.IntegerField("Suerte Total", validators=[
                                   MinValueValidator(0)], default=1)

    # Stats de Acción
    # Puntos de Acción Base = 5 + AgiTotal/2
    apBase = models.DecimalField("PUNTOS DE ACCION » (5+AG/2)", max_digits=3, decimal_places=1, default=0)
    apMod = models.DecimalField("Puntos de Acción Mod", max_digits=3, decimal_places=1, default=0)
    apTotal = models.DecimalField("Puntos de Acción Total", max_digits=3, decimal_places=1, default=0)
    
    # Secuencia Base = 2 * PerTotal
    secBase = models.DecimalField("SECUENCIA » (2xPE)", max_digits=3, decimal_places=1, default=0)
    secMod = models.DecimalField("Secuencia Mod", max_digits=3, decimal_places=1, default=0)
    secTotal = models.DecimalField("Secuencia Total", max_digits=3, decimal_places=1, default=0)

    # Daño Melee Base = StrTotal -5 (Min 1)
    danoMeleeBase = models.DecimalField("DAÑO MELEE » (FU - 5) Minimo 1", max_digits=3, decimal_places=1, default=1, validators=[MinValueValidator(1)])
    danoMeleeMod = models.DecimalField("Daño Melee Mod", max_digits=3, decimal_places=1, default=0)
    danoMeleeTotal = models.DecimalField("Daño Melee Total", max_digits=3, decimal_places=1, default=0)

    # Probabilidad de Crítico Base = SueTotal
    probCriticoBase = models.DecimalField("POSIBILIDAD DE CRITICO » (SU)", max_digits=3, decimal_places=1, default=0)
    probCriticoMod = models.DecimalField("Probabilidad de Crítico Mod", max_digits=3, decimal_places=1, default=0)
    probCriticoTotal = models.DecimalField("Probabilidad de Crítico Total", max_digits=3, decimal_places=1, default=0)

    # Ratio de Curación Base = ResTotal / 3
    ratioCuracionBase = models.DecimalField("RATIO CURACION » (RE / 3)", max_digits=3, decimal_places=1, default=0)
    ratioCuracionMod = models.DecimalField("Ratio de Curación Mod", max_digits=3, decimal_places=1, default=0)
    ratioCuracionTotal = models.DecimalField("Ratio de Curación Total", max_digits=3, decimal_places=1, default=0)

    # Capacidad de Carga Base = 11.34 + (11.34 * StrTotal)
    capCargaBase = models.DecimalField("CAPACIDAD DE CARGA » (11.35 + 11.35xFU) Kg", max_digits=5, decimal_places=1, default=0)
    capCargaMod = models.DecimalField("Capacidad de Carga Mod", max_digits=5, decimal_places=1, default=0)
    capCargaTotal = models.DecimalField("Capacidad de Carga Total", max_digits=5, decimal_places=1, default=0)

    # Resistencias
    # Resistencia al Veneno Base = 5 * ResTotal
    resVenenoBase = models.DecimalField("RESISTENCIA VENENO » (5 x RE)", max_digits=5, decimal_places=1, default=0)
    resVenenoMod = models.DecimalField("Resistencia Veneno Mod", max_digits=5, decimal_places=1, default=0)
    resVenenoTotal = models.DecimalField("Resistencia Veneno Total", max_digits=5, decimal_places=1, default=0)

    # Resistencia a la Radiación Base = 2 * ResTotal
    resRadiacionBase = models.DecimalField("RESISTENCIA RADIACION » (2 x RE)", max_digits=5, decimal_places=1, default=0)
    resRadiacionMod = models.DecimalField("Resistencia Radiación Mod", max_digits=5, decimal_places=1, default=0)
    resRadiacionTotal = models.DecimalField("Resistencia Radiación Total", max_digits=5, decimal_places=1, default=0)

    # Resistencia a la Electricidad Base = 0
    resElectricidadBase = models.DecimalField("RESISTENCIA ELECTRICIDAD »", max_digits=5, decimal_places=1, default=0)
    resElectricidadMod = models.DecimalField("Resistencia a Electricidad Mod", max_digits=5, decimal_places=1, default=0)
    resElectricidadTotal = models.DecimalField("Resistencia a Electricidad Total", max_digits=5, decimal_places=1, default=0)

    # Resistencia a los Gases Base = 0
    resGasBase = models.DecimalField("Resistencia Gas Base", max_digits=5, decimal_places=1, default=0)
    resGasMod = models.DecimalField("Resistencia Gas Mod", max_digits=5, decimal_places=1, default=0)
    resGasTotal = models.DecimalField("Resistencia Gas Total", max_digits=5, decimal_places=1, default=0)
    
    # Implantes = 10 * (IN + RE)
    implanteBase =models.DecimalField("IMPLANTE » (10 x (IN + RE))", max_digits=4, decimal_places=1, default=0)
    implanteMod = models.DecimalField("Implante Mod", max_digits=5, decimal_places=1, default=0)
    implanteTotal = models.DecimalField("Implante Total", max_digits=5, decimal_places=1, default=0)

    # Stats Secundarios
    # Armas Pequeñas Base Skill = 5 + 4 * AgiTotal
    armasPequenasBaseSkill = models.DecimalField("Armas Pequeñas Base Skill", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasPequenasPointsSkill = models.DecimalField(
        "Armas Pequeñas(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasPequenasTotalSkill = models.DecimalField(
        "Armas Pequeñas(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasPequenasMod = models.DecimalField(
        "Armas Pequeñas Mod", max_digits=5, decimal_places=2, default=0)
    armasPequenasTag = models.BooleanField("ARMAS PEQUEÑAS » (5%+4xAG))", default=False)

    # Armas Grandes Base Skill = 0 + 2 * AgiTotal
    armasGrandesBaseSkill = models.DecimalField("Armas Grandes(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasGrandesPointsSkill = models.DecimalField(
        "Armas Grandes(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasGrandesTotalSkill = models.DecimalField(
        "Armas Grandes(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasGrandesMod = models.DecimalField(
        "Armas Grandes Mod", max_digits=5, decimal_places=2, default=0)
    armasGrandesTag = models.BooleanField("ARMAS GRANDES » (0%+2xAG))", default=False)

    # Armas de Energía Base Skill = 0 + 2 * AgiTotal
    armasEnergiaBaseSkill = models.DecimalField("Armas de Energía(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasEnergiaPointsSkill = models.DecimalField(
        "Armas de Energía(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasEnergiaTotalSkill = models.DecimalField(
        "Armas de Energía(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasEnergiaMod = models.DecimalField(
        "Armas de Energía Mod", max_digits=5, decimal_places=2, default=0)
    armasEnergiaTag = models.BooleanField(
        "ARMAS ENERGIA » (0%+2xAG)", default=False)

    # Desarmado Base skill = 30 + 2*(AgiTotal + StrTotal)
    desarmadoBaseSkill = models.DecimalField("Desarmado(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    desarmadoPointsSkill = models.DecimalField(
        "Desarmado(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    desarmadoTotalSkill = models.DecimalField(
        "Desarmado(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    desarmadoMod = models.DecimalField(
        "Desarmado Mod", max_digits=5, decimal_places=2, default=0)
    desarmadoTag = models.BooleanField("DESARMADO » (30%+2x(AG+FU))", default=False)

    # Armas Melee Base Skill = 20 + 2*(AgiTotal + StrTotal)
    armasMeleeBaseSkill = models.DecimalField("Armas Melee(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasMeleePointsSkill = models.DecimalField(
        "Armas Melee(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasMeleeTotalSkill = models.DecimalField(
        "Armas Melee(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    armasMeleeMod = models.DecimalField(
        "Armas Melee Mod", max_digits=5, decimal_places=2, default=0)
    armasMeleeTag = models.BooleanField("ARMAS MELEE » (20%+2x(AG+FU))", default=False)

    # Lanzar Base Skill = 0 + 4 * AgiTotal
    lanzarBaseSkill = models.DecimalField("Lanzar(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    lanzarPointsSkill = models.DecimalField(
        "Lanzar(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    lanzarTotalSkill = models.DecimalField(
        "Lanzar(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    lanzarMod = models.DecimalField(
        "Lanzar Mod", max_digits=5, decimal_places=2, default=0)
    lanzarTag = models.BooleanField("LANZAR » (0%+4x(AG))", default=False)

    # Primeros Auxilios Base Skill = 2 * (PerTotal + IntTotal)
    primerosAuxiliosBaseSkill = models.DecimalField("Primeros Auxilios(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    primerosAuxiliosPointsSkill = models.DecimalField(
        "Primeros Auxilios(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    primerosAuxiliosTotalSkill = models.DecimalField(
        "Primeros Auxilios(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    primerosAuxiliosMod = models.DecimalField(
        "Primeros Auxilios Mod", max_digits=5, decimal_places=2, default=0)
    primerosAuxiliosTag = models.BooleanField(
        "PRIMEROS AUXILIOS » (0%+2x(PE+IN))", default=False)

    # Medicina Base Skill = 5 + PerTotal + IntTotal
    medicinaBaseSkill = models.DecimalField("Medicina(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    medicinaPointsSkill = models.DecimalField(
        "Medicina(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    medicinaTotalSkill = models.DecimalField(
        "Medicina(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    medicinaMod = models.DecimalField(
        "Medicina Mod", max_digits=5, decimal_places=2, default=0)
    medicinaTag = models.BooleanField("MEDICINA » (0%+5+(PE+IN))", default=False)

    # Sigilo Base Skill = 5 + (3 * AgiTotal)
    sigiloBaseSkill = models.DecimalField("Sigilo(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    sigiloPointsSkill = models.DecimalField(
        "Sigilo(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    sigiloTotalSkill = models.DecimalField(
        "Sigilo(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    sigiloMod = models.DecimalField(
        "Sigilo Mod", max_digits=5, decimal_places=2, default=0)
    sigiloTag = models.BooleanField("SIGILO » (5%+(3xAG))", default=False)

    # Ganzuas Base Skill = 10 + PerTotal + AgiTotal
    ganzuasBaseSkill = models.DecimalField("Ganzuas(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    ganzuasPointsSkill = models.DecimalField(
        "Ganzuas(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    ganzuasTotalSkill = models.DecimalField(
        "Ganzuas(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    ganzuasMod = models.DecimalField(
        "Ganzuas Mod", max_digits=5, decimal_places=2, default=0)
    ganzuasTag = models.BooleanField("GANZUAS » (0%+(10%+PE+AG))", default=False)

    # Robar Base Skill = 0 + 3 * AgiTotal
    robarBaseSkill = models.DecimalField("Robar(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    robarPointsSkill = models.DecimalField(
        "Robar(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    robarTotalSkill = models.DecimalField(
        "Robar(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    robarMod = models.DecimalField(
        "Robar Mod", max_digits=5, decimal_places=2, default=0)
    robarTag = models.BooleanField("ROBAR » (0%+(3xAG))", default=False)

    # Trampas Base Skill = 0 + PerTotal + AgiTotal
    trampasBaseSkill = models.DecimalField("Trampas(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    trampasPointsSkill = models.DecimalField(
        "Trampas(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    trampasTotalSkill = models.DecimalField(
        "Trampas(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    trampasMod = models.DecimalField(
        "Trampas Mod", max_digits=5, decimal_places=2, default=0)
    trampasTag = models.BooleanField("TRAMPAS/EXPLOSIVOS » (0%+PE+AG)", default=False)

    # Ciencia Base Skill = 0 + 4 * IntTotal
    cienciaBaseSkill = models.DecimalField("Ciencia(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    cienciaPointsSkill = models.DecimalField(
        "Ciencia(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    cienciaTotalSkill = models.DecimalField(
        "Ciencia(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    cienciaMod = models.DecimalField(
        "Ciencia Mod", max_digits=5, decimal_places=2, default=0)
    cienciaTag = models.BooleanField("CIENCIA » (0%+4xIN)", default=False)

    # Reparar Base Skill = 0 + 3 * IntTotal
    repararBaseSkill = models.DecimalField("Reparar(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    repararPointsSkill = models.DecimalField(
        "Reparar(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    repararTotalSkill = models.DecimalField(
        "Reparar(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    repararMod = models.DecimalField(
        "Reparar Mod", max_digits=5, decimal_places=2, default=0)
    repararTag = models.BooleanField("REPARAR » (0%+3xIN)", default=False)

    # Pilotar Base Skill = 2 * (AgiTotal + PerTotal)
    pilotarBaseSkill = models.DecimalField("Pilotar(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    pilotarPointsSkill = models.DecimalField(
        "Pilotar(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    pilotarTotalSkill = models.DecimalField(
        "Pilotar(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    pilotarMod = models.DecimalField(
        "Pilotar Mod", max_digits=5, decimal_places=2, default=0)
    pilotarTag = models.BooleanField("PILOTAR » (0%+2x(AG+PE))", default=False)

    # Conversación Base Skill = 0 + 5 * CarTotal
    conversacionBaseSkill = models.DecimalField("Conversación(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    conversacionPointsSkill = models.DecimalField(
        "Conversación(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    conversacionTotalSkill = models.DecimalField(
        "Conversación(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    conversacionMod = models.DecimalField(
        "Conversación Mod", max_digits=5, decimal_places=2, default=0)
    conversacionTag = models.BooleanField("CONVERSACION » (0%+(5xCA))", default=False)

    # Trueque Base Skill = 0 + 4 * CarTotal
    truequeBaseSkill = models.DecimalField("Trueque(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    truequePointsSkill = models.DecimalField(
        "Trueque(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    truequeTotalSkill = models.DecimalField(
        "Trueque(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    truequeMod = models.DecimalField(
        "Trueque Mod", max_digits=5, decimal_places=2, default=0)
    truequeTag = models.BooleanField("TRUEQUE » (0%+(4xCA))", default=False)

    # Juego Base Skill = 0 + 5 * SueTotal
    juegoBaseSkill = models.DecimalField("Juego(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    juegoPointsSkill = models.DecimalField(
        "Juego(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    juegoTotalSkill = models.DecimalField(
        "Juego(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    juegoMod = models.DecimalField(
        "Juego Mod", max_digits=5, decimal_places=2, default=0)
    juegoTag = models.BooleanField("JUEGO » (0%+(5xSU))", default=False)

    # Vida al Aire Libre Base Skill = 2 * (ResTotal + IntTotal)
    vidaAlAireLibreBaseSkill = models.DecimalField("Vida al Aire Libre(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    vidaAlAireLibrePointsSkill = models.DecimalField(
        "Vida al Aire Libre(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    vidaAlAireLibreTotalSkill = models.DecimalField(
        "Vida al Aire Libre(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    vidaAlAireLibreMod = models.DecimalField(
        "Vida al Aire Libre Mod", max_digits=5, decimal_places=2, default=0)
    vidaAlAireLibreTag = models.BooleanField(
        "VIDA AL AIRE LIBRE » (0%+2x(RE+IN))", default=False)

    # Atletismo Base Skill = 5 + (2 * StrTotal + AgiTotal)
    atletismoBaseSkill = models.DecimalField("Atletismo(Base)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    atletismoPointsSkill = models.DecimalField(
        "Atletismo(Puntos invertidos)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    atletismoTotalSkill = models.DecimalField(
        "Atletismo(Total)", max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    atletismoMod = models.DecimalField(
        "Atletismo Mod", max_digits=5, decimal_places=2, default=0)
    atletismoTag = models.BooleanField("ATLETISMO » (5%+2x(FU+AG))", default=False)

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
        "puntosGolpePorNivel",
        "puntosHabilidadPorNivel",
        "perksPorNivel",
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
        "trueque",
        "juego",
        "vidaAlAireLibre",
        "atletismo"
    ]


    def save(self, *args, **kwargs):
        atributos_primarios = {}

        for atributo in self.atributos_primarios:
            atr_base = getattr(self, f"{atributo}Base")
            atr_mod = getattr(self, f"{atributo}Mod")
            atr_total = atr_base + atr_mod

            atributos_primarios.update({f"{atributo}_total": atr_total})

            setattr(self, f"{atributo}Total", atr_total)
            # print(f"Save method: {atributo}Stat: {atr_base} - {atributo}Mod: {atr_mod} - {atributo}Total: {atr_total}")
        
        puntosGolpePorNivelCalculo = 3 + (atributos_primarios["Res_total"] / 2)
        puntosHabilidadPorNivelCalculo = 5 + (2 * atributos_primarios["Int_total"])
        perksPorNivelCalculo = 1
        apCalculo = 5 + atributos_primarios["Agi_total"] /2
        secCalculo = 2 * atributos_primarios["Per_total"]
        danoMeleeCalculo = atributos_primarios["Str_total"] - 5 if atributos_primarios["Str_total"] -5 > 0 else 1
        probCriticoCalculo = atributos_primarios["Sue_total"]
        ratioCuracionCalculo = atributos_primarios["Res_total"] /3
        capCargaCalculo = 11.35 + 11.35 * atributos_primarios["Str_total"]
        resVenenoCalculo = 5 * atributos_primarios["Res_total"]
        resRadiacionCalculo = 2 * atributos_primarios["Res_total"]
        resElectricidadCalculo = 0
        resGasCalculo = 0
        implanteCalculo = 10 * (atributos_primarios["Int_total"] + atributos_primarios["Res_total"])   

        for atributo_secundario in self.atributos_secundarios:
            atr_sec_base    = getattr(self, f"{atributo_secundario}Base")
            atr_sec_mod     = getattr(self, f"{atributo_secundario}Mod")
            atr_sec_calculo = locals().get(f"{atributo_secundario}Calculo")
            atr_sec_base = atr_sec_calculo
            
            if atributo_secundario == "puntosGolpePorNivel":
                # 15 + Fue + (Res*2) + PG/Nivel
                atr_sec_total = 15 + atributos_primarios["Str_total"] + (atributos_primarios["Res_total"] * 2) + ((atr_sec_base + float(atr_sec_mod)) * self.nivelPersonaje)
                setattr(self, f"{atributo_secundario}Base", atr_sec_base)
                setattr(self, f"{atributo_secundario}Total", atr_sec_total)
            elif atributo_secundario == "puntosHabilidadPorNivel":
                atr_sec_total = (atr_sec_base + float(atr_sec_mod)) * self.nivelPersonaje
                setattr(self, f"{atributo_secundario}Base", atr_sec_base)
                setattr(self, f"{atributo_secundario}Total", atr_sec_total)
            else:
                atr_sec_total = atr_sec_base + float(atr_sec_mod)
                setattr(self, f"{atributo_secundario}Base", atr_sec_base)
                setattr(self, f"{atributo_secundario}Total", atr_sec_total)
            # print(f"Save method: {atributo_secundario}Base: {atr_sec_base} - {atributo_secundario}Mod: {atr_sec_mod} - {atributo_secundario}Total: {atr_sec_total}")

        armasPequenasCalculo = 5 + (4 * atributos_primarios["Agi_total"])
        armasGrandesCalculo = 0 + (2 * atributos_primarios["Agi_total"])
        armasEnergiaCalculo = 0 + (2 * atributos_primarios["Agi_total"])
        desarmadoCalculo = 30 + 2 * (atributos_primarios["Agi_total"] + atributos_primarios["Str_total"])
        armasMeleeCalculo = 20 + 2 * (atributos_primarios["Agi_total"] + atributos_primarios["Str_total"])
        lanzarCalculo = 0 + 4 * atributos_primarios["Agi_total"]
        primerosAuxiliosCalculo = 0 + 2 * (atributos_primarios["Per_total"] + atributos_primarios["Int_total"])
        medicinaCalculo = 0 + 2 * (atributos_primarios["Per_total"] + atributos_primarios["Int_total"])
        sigiloCalculo = 0 + 5 + (atributos_primarios["Agi_total"] * 3)
        ganzuasCalculo = 0 + 10 + atributos_primarios["Per_total"] + atributos_primarios["Agi_total"]
        robarCalculo = 0 + 3 * atributos_primarios["Agi_total"]
        trampasCalculo = 0 + atributos_primarios["Per_total"] + atributos_primarios["Agi_total"]
        cienciaCalculo = 0 + 4 * atributos_primarios["Int_total"]
        repararCalculo = 0 + 3 * atributos_primarios["Int_total"]
        pilotarCalculo = 0 + 2 * (atributos_primarios["Agi_total"] + atributos_primarios["Per_total"])
        conversacionCalculo = 0 + 5 * atributos_primarios["Car_total"]
        truequeCalculo = 0 + 4 * atributos_primarios["Car_total"]
        juegoCalculo = 0 + 5 * atributos_primarios["Sue_total"]
        vidaAlAireLibreCalculo = 2 * (atributos_primarios["Res_total"] + atributos_primarios["Int_total"])
        atletismoCalculo = 5 + (2 * (atributos_primarios["Str_total"] + atributos_primarios["Agi_total"]))

        for skill in self.skill_list:
            tag = getattr(self, f"{skill}Tag")
            base_skill = getattr(self, f"{skill}BaseSkill")
            mod = getattr(self, f"{skill}Mod")
            points_skill = getattr(self, f"{skill}PointsSkill")
            total_skill = getattr(self, f"{skill}TotalSkill")
            skill_base_calculo = locals().get(f"{skill}Calculo")

            base_skill = skill_base_calculo + 20 if tag else skill_base_calculo
            setattr(self, f"{skill}BaseSkill", base_skill)

            if tag:
                total_skill = skill_up(base_skill, points_skill, tag) + float(mod)
            else:
                total_skill = skill_up(base_skill, points_skill, tag) + float(mod)

            setattr(self, f"{skill}TotalSkill", total_skill)
            # print(f"{skill}BaseSkill: {base_skill} - {skill}PointsSkill: {points_skill} - {skill}TotalSkill: {total_skill} - {skill}Mod: {mod} - {skill}Tag: {tag}")

        super(CharFallout, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombrePersonaje}({self.nombreJugador})"