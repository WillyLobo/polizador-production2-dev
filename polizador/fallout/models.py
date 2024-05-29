from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class Raza(models.Model):
    raza_tipo = models.CharField("Raza", max_length=30)

class CharFallout(models.Model):

    #Datos Generales
    nombrePersonaje = models.CharField("Nombre del Personaje", max_length=60)
    nombreJugador = models.ForeignKey(User, on_delete=models.CASCADE)
    edadPersonaje = models.IntegerField("Edad", validators=[MinValueValidator(1)])
    generoPersonaje = models.CharField("Género", max_length=15)
    razaPersonaje = models.ForeignKey("Raza", on_delete=models.CASCADE)
    alturaPersonaje = models.DecimalField("Altura", max_digits=3, decimal_places=2, default=1)
    pesoPersonaje = models.IntegerField("Peso", validators=[MinValueValidator(1)])
    
    #Status
    faccionPersonaje = models.CharField("Faccion/Alianza", max_length=60, blank=True, default="Ninguna")
    nivelPersonaje = models.IntegerField("Nivel", validators=[MinValueValidator(1)])
    experienciaPersonaje = models.IntegerField("Experiencia", validators=[MinValueValidator(0)])
    karmaPersonaje = models.IntegerField("Karma")

    #Stats Principales
    StrStat = models.IntegerField("Fuerza", validators=[MinValueValidator(0)])
    PerStat = models.IntegerField("Percepción", validators=[MinValueValidator(0)])
    ResStat = models.IntegerField("Resistencia", validators=[MinValueValidator(0)])
    CarStat = models.IntegerField("Carisma", validators=[MinValueValidator(0)])
    IntStat = models.IntegerField("Inteligencia", validators=[MinValueValidator(0)])
    AgiStat = models.IntegerField("Agilidad", validators=[MinValueValidator(0)])
    SueStat = models.IntegerField("Suerte", validators=[MinValueValidator(0)])

    apMod = models.IntegerField("Puntos de Acción Mod", default=0)
    secMod = models.IntegerField("Secuencia Mod", default=0)
    danoMeleeMod = models.IntegerField("Daño Melee Mod", default=0)
    probCriticoMod = models.IntegerField("Probabilidad de Crítico Mod", default=0)
    ratioCuracionMod = models.IntegerField("Ratio de Curación Mod", default=0)
    capCargaMod = models.IntegerField("Capacidad de Carga Mod", default=0)
    resVenenoMod = models.IntegerField("Resistencia Veneno Mod", default=0)
    resRadiacionMod = models.IntegerField("Resistencia Radiació Mod", default=0)
    resElectricidadMod = models.IntegerField("Resistencia a Electricidad", default=0)
    resGasMod = models.IntegerField("Resistencia Gas Mod", default=0)
    implanteMod = models.IntegerField("Implante Mod", default=0)

    #Stats Secundarios
    armasPequenasSkill = models.IntegerField("Armas Pequeñas", default=0, validators=[MinValueValidator(0)])
    armasPequenasMod = models.IntegerField("Armas Pequeñas Mod", default=0)
    armasPequenasTag = models.BooleanField("Armas Pequeñas Tag", default=False)

    armasGrandesSkill = models.IntegerField("Armas Grandes", default=0, validators=[MinValueValidator(0)])
    armasGrandesMod = models.IntegerField("Armas Grandes Mod", default=0)
    armasGrandesTag = models.BooleanField("Armas Grandes Tag", default=False)

    armasEnergiaSkill = models.IntegerField("Armas de Energía", default=0, validators=[MinValueValidator(0)])
    armasEnergiaMod = models.IntegerField("Armas de Energía Mod", default=0)
    armasEnergiaTag = models.BooleanField("Armas de Energía Tag", default=False)

    desarmadoSkill = models.IntegerField("Desarmado", default=0, validators=[MinValueValidator(0)])
    desarmadoMod = models.IntegerField("Desarmado Mod", default=0)
    desarmadoTag = models.BooleanField("Desarmado Tag", default=False)

    armasMeleeSkill = models.IntegerField("Armas Melee", default=0, validators=[MinValueValidator(0)])
    armasMeleeMod = models.IntegerField("Armas Melee Mod", default=0)
    armasMeleeTag = models.BooleanField("Armas Melee Tag", default=False)

    lanzarSkill = models.IntegerField("Lanzar", default=0, validators=[MinValueValidator(0)])
    lanzarMod = models.IntegerField("Lanzar Mod", default=0)
    lanzarTag = models.BooleanField("Lanzar Tag", default=False)

    primerosAuxiliosSkill = models.IntegerField("Primeros Auxilios", default=0, validators=[MinValueValidator(0)])
    primerosAuxiliosMod = models.IntegerField("Primeros Auxilios Mod", default=0)
    primerosAuxiliosTag = models.BooleanField("Primeros Auxilios Tag", default=False)

    medicinaSkill = models.IntegerField("Medicina", default=0, validators=[MinValueValidator(0)])
    medicinaMod = models.IntegerField("Medicina Mod", default=0)
    medicinaTag = models.BooleanField("Medicina Tag", default=False)

    sigiloSkill = models.IntegerField("Sigilo", default=0, validators=[MinValueValidator(0)])
    sigiloMod = models.IntegerField("Sigilo Mod", default=0)
    sigiloTag = models.BooleanField("Sigilo Tag", default=False)

    ganzuasSkill = models.IntegerField("Ganzuas", default=0, validators=[MinValueValidator(0)])
    ganzuasMod = models.IntegerField("Ganzuas Mod", default=0)
    ganzuasTag = models.BooleanField("Ganzuas Tag", default=False)

    robarSkill = models.IntegerField("Robar", default=0, validators=[MinValueValidator(0)])
    robarMod = models.IntegerField("Robar Mod", default=0)
    robarTag = models.BooleanField("Robar Tag", default=False)

    trampasSkill = models.IntegerField("Trampas", default=0, validators=[MinValueValidator(0)])
    trampasMod = models.IntegerField("Trampas Mod", default=0)
    trampasTag = models.BooleanField("Trampas Tag", default=False)

    cienciaSkill = models.IntegerField("Ciencia", default=0, validators=[MinValueValidator(0)])
    cienciaMod = models.IntegerField("Ciencia Mod", default=0)
    cienciaTag = models.BooleanField("Ciencia Tag", default=False)

    repararSkill = models.IntegerField("Reparar", default=0, validators=[MinValueValidator(0)])
    repararMod = models.IntegerField("Reparar Mod", default=0)
    repararTag = models.BooleanField("Reparar Tag", default=False)

    pilotarSkill = models.IntegerField("Pilotar", default=0, validators=[MinValueValidator(0)])
    pilotarMod = models.IntegerField("Pilotar Mod", default=0)
    pilotarTag = models.BooleanField("Pilotar Tag", default=False)

    conversacionSkill = models.IntegerField("Conversación", default=0, validators=[MinValueValidator(0)])
    conversacionMod = models.IntegerField("Conversación Mod", default=0)
    conversacionTag = models.BooleanField("Conversación Tag", default=False)

    truequeSkill = models.IntegerField("Trueque", default=0, validators=[MinValueValidator(0)])
    truequeMod = models.IntegerField("Trueque Mod", default=0)
    truequeTag = models.BooleanField("Trueque Tag", default=False)

    juegoSkill = models.IntegerField("Juego", default=0, validators=[MinValueValidator(0)])
    juegoMod = models.IntegerField("Juego Mod", default=0)
    juegoTag = models.BooleanField("Juego Tag", default=False)

    vidaAlAireLibreSkill = models.IntegerField("Vida al Aire Libre", default=0, validators=[MinValueValidator(0)])
    vidaAlAireLibreMod = models.IntegerField("Vida al Aire Libre Mod", default=0)
    vidaAlAireLibreTag = models.BooleanField("Vida al Aire Libre Tag", default=False)

    atletismoSkill = models.IntegerField("Atletismo", default=0, validators=[MinValueValidator(0)])
    atletismoMod = models.IntegerField("Atletismo Mod", default=0)
    atletismoTag = models.BooleanField("Atletismo Tag", default=False)
    
    