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
                "perkNombre": "Ghost (Fantasma)",
                "perkDescripcion": """Cuando se pone el sol, o cuando te encuentras en una zona
                                    poco iluminada, te mueves como un fantasma con este Perk.
                                    Obtienes un bonus de +20% a tu habilidad de Sigilo en condiciones
                                    de baja intensidad lumínica.""",
                "perkRequisitosTX": "Nivel 6, Sigilo 60%",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Harmless (Inofensivo)",
                "perkDescripcion": """Tu inocente apariencia hace que robarle a la gente sea un
                                    poco mas facil. Ganas un +20% a Robar. Las Deathclaws
                                    no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 6, Robar 50%, Karma 50+",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Heave Ho! (Allá Va!)",
                "perkDescripcion": """Este Perk añade 2 puntos mas de Strenght para propósitos
                                    de determinar el rango con armas arrojadizas. Este Perk
                                    no excede el máximo del arma.""",
                "perkRequisitosTX": "Nivel 6, Fuerza < 9",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "More Criticals (Critico Mejorado)",
                "perkDescripcion": """Eres más propenso a causar golpes críticos si posees este
                                    Perk. Cada nivel de More Criticals te otorga un +5% adicional a tu
                                    Probabilidad de Golpe Crítico.
                                    Los Super-Mutants no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 6, Suerte 6",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 3,
                "perkNivel": 0,
                "perkCalculo": [("probCriticoMod", 5, True)] 
            },
            {
                "perkNombre": "Negotiator (Negociador)",
                "perkDescripcion": """Eres un negociante muy habilidoso. No solo puedes negociar
                                    como el mejor sino que además puedes hablar como el mejor.
                                    Este Perk otorga una bonificación única de +20% a Trueque y
                                    Conversación.""",
                "perkRequisitosTX": "Nivel 6, Trueque 50%, Conversación 50%",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("truequeMod", 20, True),
                                ("conversacionMod", 20, True)
                            ] 
            },
            {
                "perkNombre": "Pack Rat (Organizado)",
                "perkDescripcion": """Eres muy eficiente a la hora de acomodar tu inventario.
                                    Esto hace que cargues un poco de peso extra que siempre
                                    necesitas. Obtienes un bonus a la Capacidad de Carga de 23kg.""",
                "perkRequisitosTX": "Nivel 6",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("capCargaMod", 23, True)] 
            },
            {
                "perkNombre": "Pathfinder (Viajero)",
                "perkDescripcion": """Eres el mejor encontrando la ruta mas corta. Con este Perk
                                    los viajes a traves del mapamundi se reducen un 25% del
                                    tiempo por cada rango.""",
                "perkRequisitosTX": "Nivel 6, Resistencia 6, Vida al Aire Libre 40%",
                "perkRequisitoNivel": 6,
            },
            {
                "perkNombre": "Quick Recovery (Recuperación Rapida)",
                "perkDescripcion": """Eres muy rapido para recuperarte de las caídas. Solo te
                                    cuesta un Puntos de Acción levantarte.""",
                "perkRequisitosTX": "Nivel 6, Agilidad 5",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Rad Resistance (Resistencia a la Radiación Mejorada)",
                "perkDescripcion": """Eres mejor para esquivar los efectos de la radiación y los
                                    malos efectos que esta conlleva. Cada nivel de este Perk
                                    mejora tu resistencia a la Radiación en un +15%. Los
                                    Ghouls no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 6, Resistencia 6, Inteligencia 4",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("resRaciacionMod", 15, True)] 
            },
            {
                "perkNombre": "Ranger (Viajero Mejorado)",
                "perkDescripcion": """Eres bueno evitando la atención cuando viajas a traves de
                                    los Yermos. Obtienes una bonificación de 15% a Vida al Aire Libre.""",
                "perkRequisitosTX": "Nivel 6, Percepción 6",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("vidaAlAireLibreMod", 15, True)] 
            },
            {
                "perkNombre": "Salesman (Comercial)",
                "perkDescripcion": """Eres el vendedor definitivo. De echo eres tan bueno que
                                    eres capaz de vender gato por liebre. Con este Fabuloso
                                    Perk añades un 20% a Trueque.""",
                "perkRequisitosTX": "Nivel 6, Trueque 50%",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("truequeMod", 20, True)] 
            },
            {
                "perkNombre": "Silent Running (Sigilo)",
                "perkDescripcion": """Con este Perk obtienes la habilidad de moverte rapido pero
                                    mantenerte silencioso. Puedes usar tu habilidad Sneak y correr
                                    al mismo tiempo.
                                    Sin este Perk automáticamente dejas de ser sigiloso al correr.""",
                "perkRequisitosTX": "Nivel 6, Agilidad 6, Sigilo 50%",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Sneakeater (Resistencia al Veneno Mejorada)",
                "perkDescripcion": """Um! Sabe a pollo. Ganas una inmunidad al
                                    veneno resultante en un +25% de Poison Resistance.""",
                "perkRequisitosTX": "Nivel 6, Resistencia 3",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("resVenenoMod", 25, True)] 
            },
            {
                "perkNombre": "StuntMan (Especialista)",
                "perkDescripcion": """Has aprendido a rebotar. Recibes 25% menos de daño por
                                    caídas y explosivos. Ademas obtienes un +10% a Pilotar. Los
                                    animales no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 6, Fuerza 6, Resistencia 6, Agilidad 6",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("pilotarMod", 10, True)] 
            },
            {
                "perkNombre": "Way of the Fruit (El Camino de la Fruta)",
                "perkDescripcion": """Comprendes el antiguo “camino de la fruta”. Disfrutas de
                                    los extraños y maravillosos beneficios que conlleva comer
                                    una fruta. Cuando lo haces obtienes temporalmente un +1
                                    STR. Los animales no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 6, Carisma 6",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Fortune Finder (Afortunado)",
                "perkDescripcion": """Con este fabuloso Perk recibes el doble de chapas cada vez
                                    que revises un container.""",
                "perkRequisitosTX": "Nivel 6, Suerte 5",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Gunslinger (Disparo Preciso)",
                "perkDescripcion": """Cuando uses una pistola (o un arma similar de una mano
                                    como, los revólveres o las SMG) aumenta tu precisión.
                                    Cada disparo Apuntado que realices recibe un +20% de bonus.""",
                "perkRequisitosTX": "Nivel 6",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Lead Belly (Estomago Resistente)",
                "perkDescripcion": """Con este Perk recibes solo un 50% de radiación por beber
                                    agua irradiada u otras bebidas.""",
                "perkRequisitosTX": "Nivel 6, Resistencia 5",
                "perkRequisitoNivel": 6,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 8
            {
                "perkNombre": "Bluff Master (Mentiroso)",
                "perkDescripcion": """Siempre consigues hablar para salir de una situación embarazosa
                                    cuando has usado Robar. Esto quiere decir que cualquiera, por mas
                                    que sea hostil, no te atacara directamente si intentas robarle y 
                                    eres detectado.""",
                "perkRequisitosTX": "Nivel 8, Carisma 3",
                "perkRequisitoNivel": 8,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Brutish Hulk (Crecimiento Brutal)",
                "perkDescripcion": """Con este fabuloso Perk ganas el doble del máximo de Puntos de
                                    Golpe cada vez que ganas un nivel. Esto quiere que si por
                                    nivel ganas 4 HP, con ese Perk, ganas 8. Solo las Deathclaws 
                                    pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 8, Fuerza 7, Resistencia 5",
                "perkRequisitoNivel": 8,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("puntosGolpePorNivelMod", 4, True)] 
            },
            {
                "perkNombre": "Psychotic",
                "perkDescripcion": """Tu cuerpo ha mutado para adaptarte a los estimulantes del
                                    Psycho. Con este Perk los efectos de esta droga son el
                                    doble y los efectos negativos del síndrome de abstinencia
                                    se dividen a la mitad. Solo los mutantes pueden elegir este
                                    Perk.""",
                "perkRequisitosTX": "Nivel 8, Resistencia 5",
                "perkRequisitoNivel": 8,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Tunnel Rat (Gatear)",
                "perkDescripcion": """Puedes gatear como un bebe (como un bebe muy RAPIDO). Eres
                                    capaz de moverte a la misma velocidad en los 3 estados (de pie,
                                    de rodillas y reptando). Consumes la misma cantidad de Puntos
                                    de Acción para moverte como si estuvieras de pie.""",
                "perkRequisitosTX": "Nivel 8",
                "perkRequisitoNivel": 8,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Commando",
                "perkDescripcion": """Cuando usas un rifle (o cualquier arma similar de dos manos,
                                    como una shotgun) recibes un bonus de +20% solo para disparos
                                    Apuntados. Este Perk es similar a Gunslinger.""",
                "perkRequisitosTX": "Nivel 8",
                "perkRequisitoNivel": 8,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Impartial Meditation (Meditación Imparcial)",
                "perkDescripcion": """Con este Perk obtienes un increíble bonus de +30% a Conversación,
                                    siempre y cuando mantengas tu Karma neutral.""",
                "perkRequisitosTX": "Nivel 8, Carisma 5",
                "perkRequisitoNivel": 8,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Scrounger (Gorrón)",
                "perkDescripcion": """Con este Perk recibes el doble de munición que normalmente encontrarías
                                    cada vez que revises un container.""",
                "perkRequisitosTX": "Nivel 8, Suerte 5",
                "perkRequisitoNivel": 8,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Size Matters (Gran Tamaño)",
                "perkDescripcion": """Estas obsesionado con las armas realmente grandes. Por cada rango de este
                                    Perk recibes un bonus de +20% a Armas Grandes.""",
                "perkRequisitosTX": "Nivel 8, Resistencia 5",
                "perkRequisitoNivel": 8,
                "perkNivelMaximo": 2,
                "perkNivel": 0,
                "perkCalculo": [("armasGrandesMod", 20, True)] 
            },
            # Nivel 9
            {
                "perkNombre": "Better Criticals (Critico Mejorado)",
                "perkDescripcion": """Los críticos que causas en combate son más devastadores,
                                    Mejoras tu tabla crítica en 20%. Además te aseguras mas daño.
                                    Este Perk no incrementa tu Probabilidad de Crítico. Los mutantes no pueden
                                    elegir este Perk.""",
                "perkRequisitosTX": "Nivel 9, Percepción 6, Agilidad 4, Suerte 6",
                "perkRequisitoNivel": 9,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Crazy Bomber (Artificiero)",
                "perkDescripcion": """No mas sudor en la frente! Con este Perk si tu personaje
                                    falla una tirada en la que usa explosivos, el dispositivo en cuestión se
                                    desactivara o se reseteará. Los animales no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 9, Trampas 60%, Inteligencia 6",
                "perkRequisitoNivel": 9,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Demolition Expert (Demoliciones)",
                "perkDescripcion": """Eres un experto en el fino arte de manipular explosivos.
                                    Siempre detonan al momento exacto, y además causan daño extra. Este Perk
                                    incrementa el daño de cualquier explosivo en 10.""",
                "perkRequisitosTX": "Nivel 9, Trampas 75%, Agilidad 4",
                "perkRequisitoNivel": 9,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Dodger (Esquiva)",
                "perkDescripcion": """Es muy difícil golpearte en combate si posees este Perk. Obtienes una
                                    bonificación de +5 a tu Clase de Armadura.""",
                "perkRequisitosTX": "Nivel 9, Agilidad 6",
                "perkRequisitoNivel": 9,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Explorer (explorador)",
                "perkDescripcion": """La marca del explorador es buscar nuevos lugares interesantes que investigar.
                                    Con este Perk obtienes una gran chance de encontrar gente y lugares especiales.""",
                "perkRequisitosTX": "Nivel 9",
                "perkRequisitoNivel": 9,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Light Step (Pies Ligeros)",
                "perkDescripcion": """Eres ágil, tienes suerte y siempre andas con cuidado. Este Perk da un 50%
                                    probabilidad de no activar una trampa.""",
                "perkRequisitosTX": "Nivel 9, Agilidad 5, Suerte 5",
                "perkRequisitoNivel": 9,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Mutate! (Mutación)",
                "perkDescripcion": """La radiación de las tierras baldías te ha cambiado! Uno de tus Razgos ha
                                    mutado en algo mas. Este Perk te permite intercambiar uno de tus Razgos a
                                    cambio de otro.""",
                "perkRequisitosTX": "Nivel 9",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Pyromaniac (Pirómano)",
                "perkDescripcion": """Eres un pirómano estas obsesionado con el fuego. Provocas daño extra con
                                    armas basadas en fuego. Y los enemigos siempre mueren de la manera más
                                    dramática y dolorosa posible. Obtienes un +10 de daño a cualquier arma
                                    basada en fuego.""",
                "perkRequisitosTX": "Nivel 9, Armas Grandes 75%",
                "perkRequisitoNivel": 9,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Sharpshooter (Disparo a Larga Distancia)",
                "perkDescripcion": """Tienes el talento de acertar a las cosas a larga distancia. Este Perk
                                    suma +2 de Percepción para propósitos de determinar el modificador de distancia.
                                    Es más fácil que nunca matar a larga distancia.""",
                "perkRequisitosTX": "Nivel 9, Percepción 7, Suerte 4",
                "perkRequisitoNivel": 9,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Mysterious Stranger (Angel de la Guarda)",
                "perkDescripcion": """Tienes un ángel guardián, o simplemente alguien a quien simpatizas lo
                                    suficiente. Con este Perk obtienes una chance de Suerte*5 de obtener un
                                    aliado temporal en los Random Encounters.""",
                "perkRequisitosTX": "Nivel 9, Suerte 4",
                "perkRequisitoNivel": 9,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Karma Beacon (Gran Karma)",
                "perkDescripcion": """Tu reputación te precede. Tu karma se duplica para propósitos de
                                    conversación y reacción de los personajes no jugadores.""",
                "perkRequisitosTX": "Nivel 9, Carisma 6",
                "perkRequisitoNivel": 9,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 10
            {
                "perkNombre": "Hide Of Scars (Resistencia)",
                "perkDescripcion": """Tus peleas te han endurecido la piel dejándote lleno de cicatrices.
                                    Obtienes una increíble bonificación de +15% a todas las resistencias
                                    excepto al fuego. Solo las Deathclaws pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 10, Resistencia 6",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [
                    ("resVeneno", 15, True),
                    ("resRadiacion", 15, True),
                    ("resElectricidad", 15, True),
                    ("resGas", 15, True),
                    ("resDanoNormal", 15, True),
                    ("resDanoLaser", 15, True),
                    ("resDanoFuego", 15, True),
                    ("resDanoPlasma", 15, True),
                    ("resDanoExplosivo", 15, True),
                    ] 
            },
            {
                "perkNombre": "Animal Friend (Amigo de los Animales)",
                "perkDescripcion": """Por alguna extraña razón las criaturas de las tierras baldías no se
                                    muestran hostiles hacia ti, siempre y cuando no las ataques. En el
                                    primer rango, simplemente no te atacaran. Al segundo vendrán a
                                    ayudarte en combate, pero nunca contra otro animal. Solo afecta a Dog,
                                    Yao Guai, Mole Rat, Brahmin, etc""",
                "perkRequisitosTX": "Nivel 10, Carisma 6",
                "perkRequisitoNivel": 10,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Mister Sandman (Hombre de Arena)",
                "perkDescripcion": """Con este Perk tienes la opción, siempre y cuando estes en el modo
                                    Sigiloso, de matar instantáneamente a un humano o ghoul que este durmiendo.
                                    Ademas cada muerte siempre te otorga XP.""",
                "perkRequisitosTX": "Nivel 10, Sigilo 60%",
                "perkRequisitoNivel": 10,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Nerd Rage! (Rabia de los Empollones)",
                "perkDescripcion": """Ya te molestaron lo suficiente! Con la rabia Nerd tu Fuerza aumenta a 10
                                    y obtienes 50% de Resistencia al Daño Normal siempre y cuando tus Puntos
                                    de Golpe estén por debajo del 20%.""",
                "perkRequisitosTX": "Nivel 10, Ciencia 50%, Inteligencia 5",
                "perkRequisitoNivel": 10,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 12
            {
                "perkNombre": "Action Boy (Temerario)",
                "perkDescripcion": """Cada nivel de Action Boy (o Girl si lo prefieres) te otorga un Punto de
                                    Acción adicional en cada turno de combate. Puedes usar estos Puntos de Acción
                                    genéricos en cualquier tarea.""",
                "perkRequisitosTX": "Nivel 12, Agilidad 5",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("apMod", 1, True)] 
            },
            {
                "perkNombre": "Bonsa",
                "perkDescripcion": """Tienes un pequeño árbol frutal creciendo en tu cabeza!. Obtendrás una fruta
                                    de tanto en tanto que cura 1D10+5 Queda a discreción del Master decidir cada
                                    cuanto. Solo los Ghouls pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 12, Vida al Aire Libre 40%",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Cult Of Personality (Personalidad)",
                "perkDescripcion": """La gente siempre te vera favorablemente. No importa el alineamiento y la
                                    reputación que poseas.""",
                "perkRequisitosTX": "Nivel 12, Carisma 10",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Gain statistics (Gana Estadísticas)",
                "perkDescripcion": """Cada rango de este Perk te asigna un punto en un Stat a elección.""",
                "perkRequisitosTX": "12, Stat < 10",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 3,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "HtH evade (Evasión HtH)",
                "perkDescripcion": """Si no llevas ítems en tus manos, obtienes cada Punto de Acción que
                                    inviertas al final del turno para tener mas Clase de Armadura esta se 
                                    duplica, ademas obtienes un plus de 1/12 Desarmado en tu Clase de 
                                    Armadura.""",
                "perkRequisitosTX": "Nivel 12, Desarmado 75%",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Lifegiver (Creador de Vida)",
                "perkDescripcion": """Por cada nivel de este Perk obtienes un adicional de 4 Puntos de
                                    Golpe cada vez que subas de nivel.""",
                "perkRequisitosTX": "Nivel 12, Resistencia 4",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("puntosGolpePorNivelMod", 4, True)] 
            },
            {
                "perkNombre": "Master Thief (Maestro Ladrón)",
                "perkDescripcion": """Las especialidades del Maestro ladrón son robar y abrir cerraduras.
                                    Obtienes un bonus de +15% a Robar y Ganzúas. Robale a los ricos y datelo a ti.""",
                "perkRequisitosTX": "Nivel 12, Robar 50%, Ganzúas 50%",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [
                    ("robarMod", 15, True),
                    ("ganzuasMod", 15, True),
                    ] 
            },
            {
                "perkNombre": "Master Trader (Trueque Mejorado)",
                "perkDescripcion": """Has mejorado uno de los aspectos del comercio. Compras cosas mucho mas barato de
                                    lo normal. Con este Perk obtienes un descuento del 25% cuando compres cosas a un
                                    mercader o en una tienda. Los animales no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 12, Carisma 7, Comercio 75%",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Medic! (Medicina)",
                "perkDescripcion": """Este Perk te da un bonus unico de +20% a Primeros Auxilios y Doctor. Las
                                    habilidades curativas son una cosa buena.""",
                "perkRequisitosTX": "Nivel 12, Primeros Auxilios 40%, Doctor 40%",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [
                    ("primerosAuxiliosMod", 20, True),
                    ("medicinaMod", 20, True),
                    ] 
            },
            {
                "perkNombre": "Mr Fixit (Reparación Mejorada)",
                "perkDescripcion": """Este Perk te otorga un bonus único de +20% a Reparar y Ciencia. Quedarte una
                                    noche trabajando no hiere a nadie, especialmente a ti. Los animales no pueden
                                    elegir este Perk.""",
                "perkRequisitosTX": "Nivel 12, Ciencia 40%, Reparar 40%",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [
                    ("repararMod", 20, True),
                    ("cienciaMod", 20, True),
                    ] 
            },
            {
                "perkNombre": "Road Warrior (Guerrero de Carretera)",
                "perkDescripcion": """Has aprendido a disparar y conducir al mismo tiempo. No sufres penalizaciones 
                                    por disparar pequeñas armas de fuego y pilotar un vehículo en movimiento. Los 
                                    animales no pueden conducir, así que no pueden elegir este Perk""",
                "perkRequisitosTX": "Nivel 12, Pilotar 60%, Inteligencia 6",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Tag! (Especialidad)",
                "perkDescripcion": """Tus habilidades han mejorado hasta el punto de obtener otro Tag. Esta habilidad
                                    aumenta el doble de lo normal.""",
                "perkRequisitosTX": "Nivel 12",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Talon Of Fear (Garra del Miedo)",
                "perkDescripcion": """El veneno chorrea por tus garras. Todos los ataques Unarmed que realices envenenan 
                                    a tus oponentes. Solo las Deathclaws pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 12, Fuerza 6, Desarmado 60%",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Tough Hide (Piel Dura)",
                "perkDescripcion": """La exposición a la radiación te ha endurecido contra los elementos. Obtienes un 
                                    +15% a tu Clase de Armadura y +10% a todas tus resistencias. Solo los mutantes 
                                    pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 12, Resistencia 8",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [
                    ("resVeneno", 10, True),
                    ("resRadiacion", 10, True),
                    ("resElectricidad", 10, True),
                    ("resGas", 10, True),
                    ("resDanoNormal", 10, True),
                    ("resDanoLaser", 10, True),
                    ("resDanoFuego", 10, True),
                    ("resDanoPlasma", 10, True),
                    ("resDanoExplosivo", 10, True),
                    ] 
            },
            {
                "perkNombre": "Weapon Handling (Manejo de Armas)",
                "perkDescripcion": """Puedes levantar armas mucho más grandes que las normalmente permitidas. Ganas 
                                    +3 Fuerza para propósitos de utilizar armas. Este Perk solo se aplica al 
                                    requerimiento de Fuerza en las Armas. Los animales no pueden elegir este Perk.""",
                "perkRequisitosTX": "Nivel 12, Fuerza < 7, Agilidad 5",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Cannibal (Canibal)",
                "perkDescripcion": """Con este extraño Perk ganas la opción de comer cuerpos para recuperar tu salud. 
                                    Pero cada vez que te alimentas pierdes 1 punto de Karma por el hecho de ser 
                                    considerado en contra de la naturaleza. Obtienes 20 Puntos de Golpe por cada 
                                    cadáver que devores.""",
                "perkRequisitosTX": "Nivel 12",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Robotics Expert (Experto en Robótica)",
                "perkDescripcion": """Eres el experto en robots! Con este Perk obtienes un bonus de +25% al daño 
                                    contra Robots. Aun mejor, usar el modo Sigilo contra un robot y ser detectado 
                                    implica que el robot quedara automáticamente desactivado.""",
                "perkRequisitosTX": "Nivel 12, Ciencia 50%",
                "perkRequisitoNivel": 12,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 14
            {
                "perkNombre": "Divine Favor (Favor Divino)",
                "perkDescripcion": """Has agradado a un poder superior. Obtienes un +1 a tu Stat más alto y bajas 
                                    tú Perk Rate en 1. Esto quiere decir que si antes ganabas Perks cada 3 niveles 
                                    ahora los ganas cada 2.""",
                "perkRequisitosTX": "Nivel 14, Carisma 8",
                "perkRequisitoNivel": 14,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("perksPorNivelMod", 1, True)] 
            },
            {
                "perkNombre": "Adamantium Skeleton (Esq. Adamantium)",
                "perkDescripcion": """Con este fabuloso Perk tus extremidades solo sufren un 50% del daño que 
                                    normalmente recibirían. (Solo contra ataques apuntados)""",
                "perkRequisitosTX": "Nivel 14",
                "perkRequisitoNivel": 14,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Chemist (Químico)",
                "perkDescripcion": """Con este Perk cualquier sustancia química que consumas duplica la duración 
                                    normal. Esto quiere decir que los efectos de la droga duran el doble.""",
                "perkRequisitosTX": "Nivel 14, Ciencia 60%",
                "perkRequisitoNivel": 14,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Contract killer (Asesino a Sueldo)",
                "perkDescripcion": """Una vez que elijas este Perk, podrás quitar las orejas de cualquier 
                                    personaje bueno que hayas matado y vendérselo a cierta persona (su 
                                    identidad es descubierta cuando eliges este Perk) por chapas y 
                                    Karma negativo.""",
                "perkRequisitosTX": "Nivel 14",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Cyborg",
                "perkDescripcion": """Has echo cambios permanentes en tu cuerpo! Este Perk te otorga 
                                    instantáneamente +10% a todas tus resistencias y +10% a Armas de 
                                    Energía.""",
                "perkRequisitosTX": "Nivel 14, Medicina 60%, Ciencia 60%",
                "perkRequisitoNivel": 14,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [
                    ("resVeneno", 10, True),
                    ("resRadiacion", 10, True),
                    ("resElectricidad", 10, True),
                    ("resGas", 10, True),
                    ("resDanoNormal", 10, True),
                    ("resDanoLaser", 10, True),
                    ("resDanoFuego", 10, True),
                    ("resDanoPlasma", 10, True),
                    ("resDanoExplosivo", 10, True),
                    ("armasEnergiaMod", 10, True),
                ] 
            },
            {
                "perkNombre": "Lawbringer (Justiciero)",
                "perkDescripcion": """Una vez que elijas este Perk, podrás quitar los dedos de cualquier 
                                    personaje malo que hayas matado y vendérselo a cierta persona (su 
                                    identidad es descubierta cuando eliges este Perk) por chapas y Karma 
                                    positivo.""",
                "perkRequisitosTX": "Nivel 14",
                "perkRequisitoNivel": 14,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 15
            {
                "perkNombre": "Bonus HtH atacks (Bonus al ataque Mano a Mano)",
                "perkDescripcion": """Has aprendido el secreto arte del Este, o simplemente pegas más
                                    rápido. En cualquier caso cualquier ataque cuerpo a cuerpo que realices 
                                    te cuesta un Punto de Acción menos.""",
                "perkRequisitosTX": "Nivel 15, Agilidad 6",
                "perkRequisitoNivel": 15,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Bonus Rate Of Fire (Bonus Cadencia de Fuego)",
                "perkDescripcion": """Este Perk te habilita para apretar el gatillo un poquito más rápido 
                                    y seguir siendo tan diestro como siempre. Atacar con cualquier arma a 
                                    distancia cuesta un Punto de Acción menos.""",
                "perkRequisitosTX": "Nivel 15, Percepción 6, Inteligencia 6, Agilidad 7",
                "perkRequisitoNivel": 15,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Pickpocket (Carterista)",
                "perkDescripcion": """Estas acostumbrado a robar, de echo eres tan bueno que con este Perk 
                                    puedes ignorar los modificadores de tamaño y visión.""",
                "perkRequisitosTX": "Nivel 15, Agilidad 8, Robar 80%",
                "perkRequisitoNivel": 15,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 16
            {
                "perkNombre": "Bend Rules (Dobla las Reglas)",
                "perkDescripcion": """Elige este Perk y el próximo Perk que elijas no tendrá requerimientos, 
                                    excepto por la raza.""",
                "perkRequisitosTX": "Nivel 16",
                "perkRequisitoNivel": 16,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 18
            {
                "perkNombre": "Silent Death (Muerte Silenciosa)",
                "perkDescripcion": """Cuando estés en el modo Sneak y atacas a alguien por la espalda, causas 
                                    el doble de daño usando ataques cuerpo a cuerpo.""",
                "perkRequisitosTX": "Nivel 18, Sigilo 80%, Desarmado 80%, Agilidad 10",
                "perkRequisitoNivel": 18,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Computer Whiz (Genio de los ordenadores)",
                "perkDescripcion": """Has fallado en un intento de Hackear una computadora y esta se bloqueo?
                                    No si tienes este Perk. Puedes intentar Hackear cualquier computadora que 
                                    hayas bloqueado.""",
                "perkRequisitosTX": "Nivel 18, Inteligencia 7, Ciencia 70%",
                "perkRequisitoNivel": 18,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Concentrated Fire (Fuego Concentrado)",
                "perkDescripcion": """Con este impresionante Perk incrementas tus chances de acertar cuando 
                                    apuntes a cualquier parte del cuerpo en +20%.""",
                "perkRequisitosTX": "Nivel 18, Armas Pequeñas 60%, Armas de Energía 60%",
                "perkRequisitoNivel": 18,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Infiltrator (Infiltrado)",
                "perkDescripcion": """El Infiltrator puede intentar abrir cualquier cerradura que este 
                                    bloqueada y que normalmente no hubiera podido. Esto incluye también 
                                    los intentos de forzar las cerraduras.""",
                "perkRequisitosTX": "Nivel 18, Percepción 7, Ganzúas 70%",
                "perkRequisitoNivel": 18,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Paralyzing Palm (Golpe Paralizantes)",
                "perkDescripcion": """Puedes realizar un golpe especial de Unarmed que paraliza a tus 
                                    oponentes durante 30 segundos. Para realizar este increíble ataque 
                                    tienes que estar completamente desarmado. Nota: normalmente 30 
                                    segundos equivaldrían a 3 turnos, el narrador puede decidir cambiar 
                                    esta regla a 30 Puntos de Acción.""",
                "perkRequisitosTX": "Nivel 18, Desarmado 70%",
                "perkRequisitoNivel": 18,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 20
            {
                "perkNombre": "Break the Rules (Rompe las Reglas)",
                "perkDescripcion": """Elige este Perk y el próximo Perk que elijas no tendrá 
                                    requerimientos, ni siquiera por raza.""",
                "perkRequisitosTX": "Nivel 20",
                "perkRequisitoNivel": 20,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Grim Reaper’s Sprint (Hendedura)",
                "perkDescripcion": """Este maravilloso Perk funciona muy parecido al Trait Rabid de 
                                    las Deathclaws. Cada vez que mates a un oponente recuperarás todos 
                                    tus Puntos de Acción ese turno. Te vuelves la máquina de matar 
                                    definitiva.""",
                "perkRequisitosTX": "Nivel 20",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Ninja",
                "perkDescripcion": """Este Perk te garantiza el increíble poder de los infalibles
                                    guerreros sombra. Cualquier ataque Melee o Desarmado que realices 
                                    gana un +15% de Critical Chance, ademas los ataques en modo Sigilo
                                    producen un +25% de daño.""",
                "perkRequisitosTX": "Nivel 20, Melee 80%, Sigilo 80%",
                "perkRequisitoNivel": 20,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Solar Powered (Energía Solar)",
                "perkDescripcion": """El sol es tu fuente de poder al igual que los antiguos superhéroes. 
                                    Obtienes +2 Fuerza y regeneras un Punto de Golpe por turno siempre 
                                    que te encuentres expuesto directamente al sol.""",
                "perkRequisitosTX": "Nivel 20, Resistencia 7",
                "perkRequisitoNivel": 20,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 21
            {
                "perkNombre": "Deep Sleep (Dormir Profundamente)",
                "perkDescripcion": """No importa en que cama duermas siempre duermes bien. Obtienes un 
                                    beneficio de +15% de XP siempre que duermas ocho horas seguidas. Nota: 
                                    el narrador tiene la última palabra sobre como aplicar este Perk.""",
                "perkRequisitosTX": "Nivel 21",
                "perkRequisitoNivel": 21,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Puppies! (Mascotas)",
                "perkDescripcion": """Siempre obtienes un compañero canino. No importa si este muere, otro 
                                    lo reemplazara. Y te lo encontraras en la ciudad más cercana 
                                    esperándote.""",
                "perkRequisitosTX": "Nivel 21",
                "perkRequisitoNivel": 21,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Quantum Chemist (Químico Quantum)",
                "perkDescripcion": """AH QUE REFRESCANTE! Cada 10 Nuka-Colas que adquieras puedes convertirlas 
                                    en una Nuka-Cola Quantum.""",
                "perkRequisitosTX": "Nivel 21, Ciencia 70%",
                "perkRequisitoNivel": 21,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Party Boy",
                "perkDescripcion": """Ya no sufres los efectos negativos de la adicción al Alcohol. Ya puedes 
                                    beber sin preocuparte.""",
                "perkRequisitosTX": "Nivel 21",
                "perkRequisitoNivel": 21,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Rad Tolerance",
                "perkDescripcion": """Ya no sufres los efectos del envenamiento por Radiación. Siempre que 
                                    resultes expuesto a dosis menores de radiación, no sufres las consecuencias.
                                    Nota: Queda a discreción del Máster decidir cuanto es menor. Pero se estima 
                                    unos 400/600 Rads.""",
                "perkRequisitosTX": "Nivel 21, Resistencia 7",
                "perkRequisitoNivel": 21,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Devil’s highway (Carretera del Diablo)",
                "perkDescripcion": """Tu karma es realmente negativo, incluso más de lo que realmente es. Las 
                                    personas reaccionan como si tu Karma fuera un nivel mas bajo del que posee.""",
                "perkRequisitosTX": "Nivel 21, Karma -100",
                "perkRequisitoNivel": 21,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Escalator To Heaven (Escaleras hacía el Cielo)",
                "perkDescripcion": """A la inversa que Devil’s Hayway tu karma es realmente positivo, tanto que 
                                    la gente reacciona como si fuera un nivel mayor del que posees.""",
                "perkRequisitosTX": "Nivel 21, Karma 100",
                "perkRequisitoNivel": 21,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Karmic Rebalance (Restablecer Karma)",
                "perkDescripcion": """Has logrado reestablecer tu Karma. Tu carma vuelve a 0 automáticamente al 
                                    elegir este Perk.""",
                "perkRequisitosTX": "Nivel 21",
                "perkRequisitoNivel": 21,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "No Weaknesses (No hay Puntos Debiles)",
                "perkDescripcion": """De alguna forma te has vuelto mas fuerte ya no posees debilidades. Todos 
                                    tus Stats inferiores a 5 aumentan hasta 5 automáticamente. ( otras razas la 
                                    mitad de su máximo )""",
                "perkRequisitosTX": "Nivel 21",
                "perkRequisitoNivel": 1,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 24
            {
                "perkNombre": "Nerves Of Steel (Nervios de Acero)",
                "perkDescripcion": """Tienes los nervios de acero. Solo gastas la mitad de tus Puntos de Acción.""",
                "perkRequisitosTX": "Nivel 24, Agilidad 7",
                "perkRequisitoNivel": 24,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Rad Tolerance (Tolerancia a la Radiación)",
                "perkDescripcion": """Por algún extraño motivo pierdes niveles de radiación de forma natural. 
                                    Pierdes 30 Rads al día siempre y cuando no te encuentres expuesto a la 
                                    radiación""",
                "perkRequisitosTX": "Nivel 24, Resistencia 7",
                "perkRequisitoNivel": 24,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Warmonger (Belicista)",
                "perkDescripcion": """Todas las armas custom se vuelven disponibles incluso sino posees los 
                                    planos.""",
                "perkRequisitosTX": "Nivel 24, Inteligencia 7, Reparar 125%",
                "perkRequisitoNivel": 24,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 27
            {
                "perkNombre": "Slayer (Asesino)",
                "perkDescripcion": """El Slayer camina por la tierra. En combate cuerpo a cuerpo todos tus 
                                    golpes son mejorados a críticos, causando una destrucción masiva. Cada vez 
                                    que ataques con Melee o Desarmado se vuelve golpe crítico.""",
                "perkRequisitosTX": "Nivel 27, Desarmado 80%, Fuerza 8, Agilidad 8",
                "perkRequisitoNivel": 27,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            {
                "perkNombre": "Sniper (Francotirador)",
                "perkDescripcion": """Has desarrollado el uso de las armas de fuego como una fuente de dolor. 
                                    Todos tus golpes son mejorados a críticos, causando una destrucción 
                                    masiva. Cada vez que ataquas con armas a distancia, tiras Suerte. Si 
                                    obtienes igual o menos que tu suerte, el golpe se vuelve crítico.""",
                "perkRequisitosTX": "Nivel 27, Armas Pequeñas 80%, Percepción 8, Agilidad 8",
                "perkRequisitoNivel": 27,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
            # Nivel 30
            {
                "perkNombre": "Almost Perfect (Casi Perfecto)",
                "perkDescripcion": """Puede que sea por la meditación Zen o simplemente por que te has 
                                    planteado mejorar, pero has conseguido estar a un paso de la perfección. 
                                    Todos tus Stats aumentan a 9 automáticamente.""",
                "perkRequisitosTX": "Nivel 30",
                "perkRequisitoNivel": 30,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [
                    ("FueTotal", 9, True),
                    ("PerTotal", 9, True),
                    ("ResTotal", 9, True),
                    ("CarTotal", 9, True),
                    ("IntTotal", 9, True),
                    ("AgiTotal", 9, True),
                    ("SueTotal", 9, True),    
                ] 
            },
            {
                "perkNombre": "Nuclear Anomaly (Anomalía Nuclear)",
                "perkDescripcion": """Siempre que tu salud se reduzca a 20 o menos provocas una terrible y 
                                    destructiva explosión nuclear. (Daño de Fat-Man) Nota: cualquier aliado 
                                    próximo sufrirá los efectos. Nota: debido a que este Perk es demasiado 
                                    rebuscado queda a discreción del Master aplicarlo o no.""",
                "perkRequisitosTX": "Nivel 30",
                "perkRequisitoNivel": 30,
                "perkNivelMaximo": 1,
                "perkNivel": 0,
                "perkCalculo": [("", 0, True)] 
            },
        ]