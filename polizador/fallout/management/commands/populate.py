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
        
        # perkCalculo = (stat, valor, condicionboleanaVerdadera)
        perks = [
            {
                "perkNombre": "Black Widow (Viuda Negra)",
                "perkDescripcion": """Ganas +10% de daño cuando te enfrentas al sexo masculino.""",
                "perkRequisitosTX": "Nivel 2, Personaje Femenino",
                "perkRequisitoNivel": 2,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": 0
            },
            {
                "perkNombre": "Lady Killer (Asesino de Mujeres)",
                "perkDescripcion": """Ganas +10% de daño cuando te enfrentas al sexo femenino.""",
                "perkRequisitosTX": "Nivel 2, Personaje Masculino",
                "perkRequisitoNivel": 2,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": 0
            },
            {
                "perkNombre": "Daddy’s Boy/ Girl (Niño/Niña de Papa)",
                "perkDescripcion": """Al igual que tu padre has dedicado tu tiempo a incrementar tus habilidades 
                                    intelectuales. Ganas +10% a Ciencia; Primeros Auxilios y Doctor.""",
                "perkRequisitosTX": "Nivel 2, Inteligencia 4",
                "perkRequisitoNivel": 2,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("ciencia", 10, True), ("primerosAuxilios", 10, True), ("doctor", 10, True)]
            },
            {
                "perkNombre": "Gun Nut (Experto en Armas)",
                "perkDescripcion": """Estas obsesionado con el uso y mantenimiento de todo tipo de armas de fuego 
                                    convencionales. Por cada rango de Gun Nut ganas +10% a Armas Pequeñas y Reparar""",
                "perkRequisitosTX": "Nivel 2, Inteligencia 4, Agilidad 4",
                "perkRequisitoNivel": 2,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("armasPequeñas", 10, True), ("reparar", 10, True)]
            },
            {
                "perkNombre": "Intense Training (Entrenamiento Intenso)",
                "perkDescripcion": """Con entrenamiento intenso puedes añadir un punto a cualquiera de tus atributos SPECIAL.
                                    Lo puedes combinar con 'Gain Atribute'.""",
                "perkRequisitosTX": "Nivel 2",
                "perkRequisitoNivel": 2,
                "perkNivelMaximo": 7,
                "perkNivel": 0,
                "perkCalculo": [("statPool", 1, True)]
            },
            {
                "perkNombre": "Little Leaguer (Pitcher)",
                "perkDescripcion": """Años en el Vault jugando al baseball incrementaron tus habilidades de arrojar y acertar.
                                    Por cada rango obtienes +10% en Armas Melee y Lanzar.""",
                "perkRequisitosTX": "Nivel 2, Fuerza 4",
                "perkRequisitoNivel": 2,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("armasMelee", 10, True), ("lanzar", 10, True)]
            },
            {
                "perkNombre": "Brown Noser (Lameculos)",
                "perkDescripcion": """Has aprendido el valor de adular a tus superiores, ganas una promoción extra por cada nivel de
                                    este Perk. Este Perk es solo válido para rangos dentro de la Hermandad del Acero.""",
                "perkRequisitosTX": "Nivel 2, Carisma 5, Inteligencia 6",
                "perkRequisitoNivel": 2,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)]
            },
            {
                "perkNombre": "Die Hard (Duro de Matar)",
                "perkDescripcion": """No te rindes fácilmente. Cuando tus Hit Points están por debajo del 20% obtienes un bonificador
                                    de 10% a todas las resistencias.""",
                "perkRequisitosTX": "Nivel 2, Primeros Auxilios 40%, Resistencia 6",
                "perkRequisitoNivel": 2,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("resVeneno", 10, "condHeridoCritico"),
                                ("resRadiacion", 10, "condHeridoCritico"),
                                ("resElectricidad", 10, "condHeridoCritico"),
                                ("resGas", 10, "condHeridoCritico"),
                                ("resDanoNormal", 10, "condHeridoCritico"),
                                ("resDanoLaser", 10, "condHeridoCritico"),
                                ("resDanoFuego", 10, "condHeridoCritico"),
                                ("resDanoPlasma", 10, "condHeridoCritico"),
                                ("resDanoExplosivo", 10, "condHeridoCritico")
                            ]
            },
            # Nivel 3
            {
                "perkNombre": "Awareness (Conocimiento)",
                "perkDescripcion": """Con este Perk recibes la información exacta de cualquier criatura que examines. Esto quiere
                                    decir que sabrás exactamente sus Hit Points, el arma que posea y cuanta munición posee.""",
                "perkRequisitosTX": "Nivel 3, Percepción 5",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)]
            },
            {
                "perkNombre": "Bonus Hand to Hand (Bonus Cuerpo a Cuerpo)",
                "perkDescripcion": """Experiencia en el combate cuerpo a cuerpo te ha dado la habilidad de hacer mas daño.
                                    Obtienes un +15% de daño a tus ataques Desarmado y Armas Melee.""",
                "perkRequisitosTX": "Nivel 3, Agilidad 6, Fuerza 6",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 3,
                "perkNivel": 0,
                "perkCalculo": [("danoDesarmado", 15, True), ("danoMelee", 15, True)]
            },
            {
                "perkNombre": "Comprehension (Comprensión)",
                "perkDescripcion": """Prestas mucha mas atención a los pequeños detalles cuando lees. Ganas un 50% más de 
                                    puntos cuando lees libros.""",
                "perkRequisitosTX": "Nivel 3, Inteligencia 6",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)]
            },
            {
                "perkNombre": "Cautious Nature (Cauteloso)",
                "perkDescripcion": """Algunos pensarían que eres un miedoso, pero en realidad eres muy precavido. Obtienes
                                    un +3 a Percepción en cualquier Random Encounter.""",
                "perkRequisitosTX": "Nivel 3, Percepción 6",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)]
            },
            {
                "perkNombre": "Precence (Presencia)",
                "perkDescripcion": """Tu presencia s eimpone. Obtienes un +15% a la reacción de la gente cuando apareces en 
                                    escena.""",
                "perkRequisitosTX": "Nivel 3, Carisma 6",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Smooth Talker (Buen Conversador)",
                "perkDescripcion": """Obtienes un +1 de Inteligencia para propósitos de dialogo. Esto
                                    podría traducirse en que el Master te de alguna pista en una
                                    conversación.""",
                "perkRequisitosTX": "Nivel 3, Inteligencia 4",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Kamasutra Master",
                "perkDescripcion": """En la cama eres el mejor. Con este fabuloso Perk consigues
                                    que la gente desee tener sexo contigo. Solo los Humanos
                                    pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 3, Resistencia 5, Agilidad 5",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Earlier secuence (Iniciativa Mejorada)",
                "perkDescripcion": """Por cada rango que inviertas en este Perk obtienes un
                                    bonus a tu secuencia de +3.""",
                "perkRequisitosTX": "Nivel 3, Percepción 6",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("secMod", 3)] 
            },
            {
                "perkNombre": "Druken Master (Borracho)",
                "perkDescripcion": """Peleas mejor cuando estas borracho. Recibes un +20% a
                                    Unarmed cuando estas bajo la influencia del alcohol. Los
                                    Robots no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 3, Desarmado 60%",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("danoDesarmado", 20, "condBorracho")] 
            },
            {
                "perkNombre": "Faster Healing (Cura Rapida)",
                "perkDescripcion": """Por cada rango de este Perk incrementas en +5 tu Healing
                                    Rate. Este bonus se añade a tu Healing Rate normal provocando
                                    que te regeneres mas rápido.""",
                "perkRequisitosTX": "Nivel 3, Resistencia 6",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("ratioCuracionMod", 5, True)] 
            },
            {
                "perkNombre": "Flower Child (Abstinencia)",
                "perkDescripcion": """Con este Perk eres menos propenso a caer adicto a las drogas. 
                                    Cualquier tirada de adicción se reduce un - 50%. Además sufres
                                    solo la mitad del tiempo del síndrome de abstinencia.""",
                "perkRequisitosTX": "Nivel 3, Resistencia 5",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Gunner (Tirador)",
                "perkDescripcion": """Eres un experto tirador desde un vehículo. Obtienes una
                                    bonificación de +10% a la chance de acertar cuando ataques
                                    desde un vehículo en movimiento.""",
                "perkRequisitosTX": "Nivel 3, Agilidad 6, Armas Pequeñas 40%",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Healer (Curandero)",
                "perkDescripcion": """La curación de los cuerpos se vuelve mucho más fácil con
                                    este Perk. Por cada rango incrementas tu índice de curación
                                    en 1d6+4 cuando uses Primeros Auxilios o Doctor.""",
                "perkRequisitosTX": "Nivel 3, Percepción 7, Inteligencia 5, Agilidad 6, Primeros Auxilios 40%",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Here and Now (Aquí y Ahora)",
                "perkDescripcion": """Con este Perk ganas inmediatamente un nivel.""",
                "perkRequisitosTX": "Nivel 3",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Lead Foot (Conductor)",
                "perkDescripcion": """Tus reflejos y habilidad de conducir combinados te convierten en un
                                    conductor mucho más veloz. Obtienes un +25% a la velocidad cuando
                                    conduces. Los animales no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 3, Percepción 6, Agilidad 6, Pilotar 60%",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Night Visión (Visión Nocturna)",
                "perkDescripcion": """Con el Perk Night Visión, puedes ver en la oscuridad. Esto reduce
                                    cualquier penalización por oscuridad en 20%.""",
                "perkRequisitosTX": "Nivel 3, Percepción 6",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Quick Pockets (Bolsillo Rapidos)",
                "perkDescripcion": """Has aprendido a usar mejor tu inventario. Los costes de
                                    acceder al inventario se reducen a la mitad. Esto quiere
                                    decir que revisar entre tus objetos solo te cuesta 2 AP.""",
                "perkRequisitosTX": "Nivel 3, Agilidad 5",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Rad Child (Retraso de Radiación)",
                "perkDescripcion": """No recibes daño inmediato por la radiación. De hecho te
                                    regeneras cuando te encuentras expuesto! Sin embargo la
                                    radiación continua sigue en tu sistema como siempre. Solo
                                    los Ghouls pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 3, Resistencia 4",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Scout (Encuentros Mejorados)",
                "perkDescripcion": """Has mejorado tu habilidad para distinguir lugares distantes.
                                    Tienes una mejor chance de toparte con Random Encounters.""",
                "perkRequisitosTX": "Nivel 3, Percepción 7",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Stat! (Cura Mejorada)",
                "perkDescripcion": """Puedes curar a la gente mucho mas rapido que un medico
                                    normal. Reduces el coste de Action Points para Firts Aid
                                    y Doctor en 2 AP por cada rango de este Perk.""",
                "perkRequisitosTX": "Nivel 3, Agilidad 6, Primeros Auxilios 75%, Doctor 50%",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Stonewall (Pies de Piedra)",
                "perkDescripcion": """Eres duro, es realmente difícil conseguir tirarte al suelo.
                                    Reducen en un 75% la chance de Knock Down (tirarte al suelo).""",
                "perkRequisitosTX": "Nivel 3, Fuerza 6",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Strong Back (Mula)",
                "perkDescripcion": """Puedes cargar unas 50 lbs adicionales por cada rango de este Perk.""",
                "perkRequisitosTX": "Nivel 3, Fuerza 6, Resistencia 6",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 3,
                "perkNivel": 0,
                "perkCalculo": [("capCargaMod", 50, True)] 
            },
            {
                "perkNombre": "Survivalist (Supervivencia Mejorada)",
                "perkDescripcion": """Eres el maestro de la supervivencia. Este Perk te confiere
                                    la habilidad de sobrevivir en ambientes hostiles, Obtienes
                                    un +25% a tu Skill de Outdoorsman para propósitos de supervivencia.""",
                "perkRequisitosTX": "Nivel 3, Resistencia 6, Inteligencia 6, Vida al Aire Libre 40%",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("vidaAlAireLibreMod", 25, True)] 
            },
            {
                "perkNombre": "Swift Learner (Alumno Aventajado)",
                "perkDescripcion": """Eres realmente precoz a la hora de aprender cosas nuevas.
                                    Por cada rango en este Perk recibes un 15% adicional de
                                    experiencia.
                                    Es mejor elegir este Perk al principio.""",
                "perkRequisitosTX": "Nivel 3, Inteligencia 4",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Team Player (Jugador de Equipo)",
                "perkDescripcion": """Te criaste en una familia grande y en consecuencia funcionas
                                    mucho mejor en equipo. Obtienes un +10% a todos tus Skills
                                    siempre que te encuentres cercano a un compañero de equipo.""",
                "perkRequisitosTX": "Nivel 3, Carisma 4",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Thief (Ladrón)",
                "perkDescripcion": """La sangre del ladrón corre por tus venas. Con este Perk
                                    obtienes de una vez +10% a Robar, Ganzuas, Sigilo y Trampas.
                                    Un muy buen ladrón es un ladrón vivo.""",
                "perkRequisitosTX": "Nivel 3",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("robarMod", 10, True),
                                ("ganzuasMod", 10, True),
                                ("sigiloMod", 10, True),
                                ("trampasMod", 10, True)
                            ] 
            },
            {
                "perkNombre": "Thoughness (Dureza)",
                "perkDescripcion": """Eres realmente resistente, posees la mítica Iron Skin (piel
                                    de hierro). Por cada nivel de este Perk obtienes un +10% a tu
                                    resistencia al daño Normal.""",
                "perkRequisitosTX": "Nivel 3, Suerte 6, Resistencia 6",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 3,
                "perkNivel": 0,
                "perkCalculo": [("resistenciaDanoNormal", 10, True)] 
            },
            {
                "perkNombre": "Looking for Trouble (Buscando Follón)",
                "perkDescripcion": """Siempre estas buscando pleito. Cuando viajas a través del
                                    mapa puedes “llamar” a un random encounter a voluntad.""",
                "perkRequisitosTX": "Nivel 3, Suerte 4",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Feign Death (Fingir Muerte)",
                "perkDescripcion": """Cuando recibes un golpe puedes fingir tu propia muerte
                                    para engañar a un enemigo. Realizas una tirada de Outdoorsman y si
                                    lo consigues tu enemigo se alejara con una sonrisa de satisfacción.""",
                "perkRequisitosTX": "Nivel 3, Vida al Aire Libre 75%",
                "perkRequisitoNivel": 3,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 4
            {
                "perkNombre": "Bracing (Vigor)",
                "perkDescripcion": """Has aprendido como utilizar armas grandes cuando estas
                                    de pie. Recibes un +2 STR para el propósito de disparar
                                    armas grandes cuando te encuentres en de pie.""",
                "perkRequisitosTX": "Nivel 4, Resistencia 5, Armas Grandes 60%",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Death Sense (Sentido del Peligro)",
                "perkDescripcion": """Has desarrollado sentidos superiores. Este Perk te otorga
                                    un +20% de bonus a Percepción en la oscuridad y un +25% de
                                    bonus para detectar enemigos que usen Sigilo.""",
                "perkRequisitosTX": "Nivel 4, Inteligencia 5",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Flexible",
                "perkDescripcion": """Años de ejercicios te han hecho increíblemente flexible.
                                    Puedes cambiar de estado (de pie, de rodillas, o tumbado)
                                    el doble de rápido que una persona normal. Esto quiere
                                    decir que te cuesta la mitad de AP cambiar de estado.""",
                "perkRequisitosTX": "Nivel 4, Inteligencia 6",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Hit the Deck (Cuerpo a Tierra!)",
                "perkDescripcion": """Reaccionas realmente rapido con la palabra “incoming!”.
                                    Obtienes un +50% a la Explosion Resistance.""",
                "perkRequisitosTX": "Nivel 4, Agilidad 6",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("resDanoExplosivo", 50, True)] 
            },
            {
                "perkNombre": "Leader (Liderazgo)",
                "perkDescripcion": """Eres un líder natural. Cualquier miembro de tu escuadrón
                                    dentro de tu área de influencia obtiene un +1 AG y un +5 AC.
                                    Los animales no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 4, Carisma 6",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Loner (Solitario)",
                "perkDescripcion": """Tu solitaria opresión e infancia significan que funcionas
                                    mucho mejor solo. Obtienes un +20% a todas tus tiradas
                                    cuando no te encuentres bajo la influencia de otro miembro 
                                    del escuadrón.""",
                "perkRequisitosTX": "Nivel 4, Carisma < 5, Vida al Aire Libre 40%",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Steady Arm (Brazo Firme)",
                "perkDescripcion": """Tu increíble tamaño significa que cualquier ataque Burts te
                                    cuesta un AP menos cuando estas de pie. Solo los mutantes pueden 
                                    elegir este Perk""",
                "perkRequisitosTX": "Nivel 4, Fuerza 6, Resistencia 6",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Child At Heart (Corazón de Niño)",
                "perkDescripcion": """Este Perk mejora mucho tu interacción con niños. Obtienes un 
                                    +50% de Speech cuando hables con un niño.""",
                "perkRequisitosTX": "Nivel 4, Carisma 4",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Entomologist (Entomología)",
                "perkDescripcion": """Como entomológista conoces a los insectos mutantes. Produces 
                                    un 50% más de daño, cada vez que ataques a un insecto mutante.""",
                "perkRequisitosTX": "Nivel 4, Inteligencia 4, Ciencia 40%",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Iron Fist (Puño de Hierro)",
                "perkDescripcion": """Con los puños de acero incrementas tu daño en combate
                                    cuerpo a cuerpo. Por cada rango de este Perk obtienes un
                                    +5 MD solo cuando uses Desarmado.""",
                "perkRequisitosTX": "Nivel 4, Fuerza 4",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 3,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Scoundrel (Manipular)",
                "perkDescripcion": """Elige este Perk y podrás utilizar tu encantadora manipulación
                                    para influenciar a la gente. Cada rango de este Perk incrementa 
                                    tus habilidades Trueque y Conversación en +15%.""",
                "perkRequisitosTX": "Nivel 4, Carisma 4",
                "perkRequisitoNivel": 4,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("truequeMod", 15, True),
                                ("conversacionMod", 15, True)
                            ] 
            },
            # Nivel 6
            {
                "perkNombre": "Adrenaline Rush (Adrenalina)",
                "perkDescripcion": """Con este Perk ganas +1 STR cuando tus Hit Points estén
                                    por debajo del 50%.""",
                "perkRequisitosTX": "Nivel 6, Fuerza < 10",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("strMod", 1, "condHeridoMedio")] 
            },
            {
                "perkNombre": "Bone Head (Cabeza Dura)",
                "perkDescripcion": """Eres un cabeza dura. Las probabilidad de dejarte en el
                                    estado Unconciuoss (inconsciente) se reducen en un 50%.""",
                "perkRequisitosTX": "Nivel 6, Resistencia 4",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Bonus Move (Bonus al Movimiento)",
                "perkDescripcion": """Eres realmente rapido. Por cada rango de este Perk obtienes
                                    una bonificación de 4 Action Points solo para propósitos de movimiento.""",
                "perkRequisitosTX": "Nivel 6, Agilidad 5",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Bonus Ranged Damage (Bonus al Ataque a Bocajarro)",
                "perkDescripcion": """Sabes como provocar mas daño cuando utilizas armas a
                                    distancia. Por cada rango de este Perk obtienes un +15% de Daño.
                                    No se aplica a Lanzar.""",
                "perkRequisitosTX": "Nivel 6, Agilidad 6, Suerte 6",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [
                            ("danoArmasPequenas", 15, True)
                            ("danoArmasGrandes", 15, True)
                            ("danoArmasEnergia", 15, True)
                        ]
            },
            {
                "perkNombre": "Cancerous Growth (Crecimiento Canceroso)",
                "perkDescripcion": """Has mutado de tal manera que obtienes un +5 tu Ratio de Curación
                                    y puedes regenerar miembros rotos y amputados.""",
                "perkRequisitosTX": "Nivel 6, Resistencia 4",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("ratioCuracionMod", 5, True)] 
            },
            {
                "perkNombre": "Empathy (Empatía)",
                "perkDescripcion": """Te das cuenta muy rápido como se encuentra la gente. El
                                    narrador te dará una pista del nivel de reacción ante tus comentarios
                                    y podrás decidir si los efectúas o no.""",
                "perkRequisitosTX": "Nivel 6, Percepción 7, Inteligencia 5",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Educated (Educado)",
                "perkDescripcion": """Por cada nivel de este Perk obtienes un +6 a tus Puntos de Habilidad
                                    por Nivel.
                                    Es mejor elegir este Perk al principio.""",
                "perkRequisitosTX": "Nivel 6, Inteligencia 6",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("puntosHabilidadPorNivelMod", 6, True)] 
            },
            {
                "perkNombre": "Gambler (Jugador)",
                "perkDescripcion": """Puedes jugar como el mejor. Con este Perk obtienes un
                                    +20% a tu habilidad de Juego.""",
                "perkRequisitosTX": "Nivel 6, Juego 50%",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("juegoMod", 20, True)] 
            },
            {
                "perkNombre": "",
                "perkDescripcion": """""",
                "perkRequisitosTX": "",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "",
                "perkDescripcion": """""",
                "perkRequisitosTX": "",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "",
                "perkDescripcion": """""",
                "perkRequisitosTX": "",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "",
                "perkDescripcion": """""",
                "perkRequisitosTX": "",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "",
                "perkDescripcion": """""",
                "perkRequisitosTX": "",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "",
                "perkDescripcion": """""",
                "perkRequisitosTX": "",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "",
                "perkDescripcion": """""",
                "perkRequisitosTX": "",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
        ]