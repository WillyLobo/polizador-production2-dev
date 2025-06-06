from django import forms
from django.utils.safestring import SafeString
from fallout.models import CharFallout

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
    "trueque",
    "juego",
    "vidaAlAireLibre",
    "atletismo"
]

class PlanillaFalloutCreateForm(forms.ModelForm):
    class Meta:
        model = CharFallout
        fields = (
            "nombreJugador",
            "nombrePersonaje",
            # Group 1
            "edadPersonaje",
            "generoPersonaje",
            # Endgroup 1
            "razaPersonaje",
            "alturaPersonaje",
            "pesoPersonaje",
            "faccionPersonaje",
            "nivelPersonaje",
            "experienciaPersonaje",
            "karmaPersonaje",
            "StrBase",
            "PerBase",
            "ResBase",
            "CarBase",
            "IntBase",
            "AgiBase",
            "SueBase",
            "armasPequenasTag",
            "armasGrandesTag",
            "armasEnergiaTag",
            "desarmadoTag",
            "armasMeleeTag",
            "lanzarTag",
            "primerosAuxiliosTag",
            "medicinaTag",
            "sigiloTag",
            "ganzuasTag",
            "robarTag",
            "trampasTag",
            "cienciaTag",
            "repararTag",
            "pilotarTag",
            "conversacionTag",
            "truequeTag",
            "juegoTag",
            "vidaAlAireLibreTag",
            "atletismoTag"
        )
        widgets = {
            "nombreJugador":forms.Select(attrs={
                "class":"fallout-font form-control",
            }),
            "nombrePersonaje":forms.TextInput(attrs={
                "class":"fallout-font form-control"
            }),
            "edadPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"0"
            }),
            "generoPersonaje":forms.TextInput(attrs={
                "class":"fallout-font form-control",
            }),
            "razaPersonaje":forms.Select(attrs={
                "class":"fallout-font form-control",
            }),
            "alturaPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"0"
            }),
            "pesoPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"0"
            }),
            "faccionPersonaje":forms.TextInput(attrs={
                "class":"fallout-font form-control",
                "readonly":"readonly"
            }),
            "nivelPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"1"
            }),
            "experienciaPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"0"
            }),
            "karmaPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"0"
            }),

            # Atributos Primarios
            "StrBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "PerBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "ResBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "CarBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "IntBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "AgiBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "SueBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "armasPequenasTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),


            # "comisionado_sexo":forms.Select(attrs={
            #     "class":"form-control",
            #     }),
            # "comisionado_dni":forms.NumberInput(attrs={
            #     "class":"form-control",
            #     "placeholder":"0"
            #     }),
            # "solicitud_anulada":forms.CheckboxInput(attrs={
            #     "class":"form-check-input",
            #     "style":'width: 2em;height: 2em;'
            #     }),

        }

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='fallout-font form-group'>"))

class PlanillaFalloutUpdateForm(forms.ModelForm):
    class Meta:
        model = CharFallout
        fields = (
            # Datos Generales(Izquierda)
            "nombreJugador", # 1 hidden
            "nombrePersonaje", # 2
            # Group 1
            "edadPersonaje", # 3    
            "generoPersonaje", # 4
            # Endgroup 1
            "razaPersonaje", # 5
            # Group 2
            "alturaPersonaje", # 6
            "pesoPersonaje", # 7
            # Endgroup 2
            "faccionPersonaje", # 8
            # Datos Generales(Derecha)
            "nivelPersonaje", # 9
            "experienciaPersonaje", # 10
            "karmaPersonaje", # 11
            # End Datos Generales
            # Atributos Primarios
            "StrBase", # 12
            "StrMod", # 13
            "PerBase", # 14
            "PerMod", # 15
            "ResBase", # 16
            "ResMod", # 17
            "CarBase", # 18
            "CarMod", # 19
            "IntBase", # 20
            "IntMod", # 21
            "AgiBase", # 22
            "AgiMod", # 23
            "SueBase", # 24
            "SueMod", # 25
            # Atributos Secundarios
            "puntosHabilidadPorNivelMod",
            "puntosGolpePorNivelMod",
            "apMod", # 26
            "secMod", # 27
            "danoMeleeMod", # 28
            "probCriticoMod", # 29
            "ratioCuracionMod", # 30
            "capCargaMod", # 31
            "resVenenoMod", # 32
            "resRadiacionMod", # 33
            "resElectricidadMod", # 34
            "resGasMod", # 35
            "implanteMod", # 36
            # Habilidades
            "armasPequenasTag", # 37
            "armasPequenasMod", # 38
            "armasPequenasPointsSkill", # 39
            "armasGrandesTag", # 40
            "armasGrandesMod", # 41
            "armasGrandesPointsSkill", # 42
            "armasEnergiaTag", # 43
            "armasEnergiaMod", # 44
            "armasEnergiaPointsSkill", # 45
            "desarmadoTag", # 46
            "desarmadoMod", # 47
            "desarmadoPointsSkill", # 48
            "armasMeleeTag", # 49
            "armasMeleeMod", # 50
            "armasMeleePointsSkill", # 51
            "lanzarTag", # 52
            "lanzarMod", # 53
            "lanzarPointsSkill", # 54
            "primerosAuxiliosTag", # 55
            "primerosAuxiliosMod", # 56
            "primerosAuxiliosPointsSkill", # 57
            "medicinaTag", # 58
            "medicinaMod", # 59
            "medicinaPointsSkill", # 60
            "sigiloTag", # 61
            "sigiloMod", # 62
            "sigiloPointsSkill", # 63
            "ganzuasTag", # 64
            "ganzuasMod", # 65
            "ganzuasPointsSkill", # 66
            "robarTag", # 67
            "robarMod", # 68
            "robarPointsSkill", # 69
            "trampasTag", # 70
            "trampasMod", # 71
            "trampasPointsSkill", # 72
            "cienciaTag", # 73
            "cienciaMod", # 74
            "cienciaPointsSkill", # 75
            "repararTag", # 76
            "repararMod", # 77
            "repararPointsSkill", # 78
            "pilotarTag", # 79
            "pilotarMod", # 80
            "pilotarPointsSkill", # 81
            "conversacionTag", # 82
            "conversacionMod", # 83
            "conversacionPointsSkill", # 84
            "truequeTag", # 85
            "truequeMod", # 86
            "truequePointsSkill", # 87
            "juegoTag", # 88
            "juegoMod", # 89
            "juegoPointsSkill", # 90
            "vidaAlAireLibreTag", # 91
            "vidaAlAireLibreMod", # 92
            "vidaAlAireLibrePointsSkill", # 93
            "atletismoTag", # 94
            "atletismoMod", # 95
            "atletismoPointsSkill", # 96
        )

        habilidad_numberinput = {
                    "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                    "placeholder":"0",
                    "step":"1",
                }

        widgets = {
            "nombreJugador":forms.Select(attrs={
                "class":"fallout-font form-control",
                "readonly":"readonly"
            }),
            "nombrePersonaje":forms.TextInput(attrs={
                "class":"fallout-font form-control"
            }),
            "edadPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"0"
            }),
            "generoPersonaje":forms.TextInput(attrs={
                "class":"fallout-font form-control",
            }),
            "razaPersonaje":forms.Select(attrs={
                "class":"fallout-font form-control",
            }),
            "alturaPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"0"
            }),
            "pesoPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"0"
            }),
            "faccionPersonaje":forms.TextInput(attrs={
                "class":"fallout-font form-control",
                "readonly":"readonly"
            }),
            "nivelPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"1"
            }),
            "experienciaPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"0"
            }),
            "karmaPersonaje":forms.NumberInput(attrs={
                "class":"fallout-font form-control",
                "placeholder":"0"
            }),

            # Atributos Primarios
            "StrBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "StrMod":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"0",
                "min":"0",
                "step":"1"
            }),
            "PerBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "PerMod":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"0",
                "min":"0",
                "step":"1"
            }),
            "ResBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "ResMod":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"0",
                "min":"0",
                "step":"1"
            }),
            "CarBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "CarMod":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"0",
                "min":"0",
                "step":"1"
            }),
            "IntBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "IntMod":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"0",
                "min":"0",
                "step":"1"
            }),
            "AgiBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "AgiMod":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"0",
                "min":"0",
                "step":"1"
            }),
            "SueBase":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"1",
                "min":"1",
                "step":"1"
            }),
            "SueMod":forms.NumberInput(attrs={
                "class":"fallout-font-md form-control fs-1",
                "placeholder":"0",
                "min":"0",
                "step":"1"
            }),

            "puntosHabilidadPorNivelMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0",
                "min":"0",
                "step":"1"
            }),
            "puntosGolpePorNivelMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0",
                "min":"0",
                "step":"1"
            }),
            "apMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
            "secMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
            "danoMeleeMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
            "probCriticoMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
            "ratioCuracionMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
            "capCargaMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
            "resVenenoMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
            "resRadiacionMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
            "resElectricidadMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
            "resGasMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
            "implanteMod":forms.NumberInput(attrs={
                "class":"fallout-font p-0 m-0 shadow-none no-border w-100",
                "placeholder":"0"
            }),
                 
            "armasPequenasTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "armasPequenasMod":forms.NumberInput(attrs=habilidad_numberinput),
            "armasPequenasPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "armasGrandesTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "armasGrandesMod":forms.NumberInput(attrs=habilidad_numberinput),
            "armasGrandesPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "armasEnergiaTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "armasEnergiaMod":forms.NumberInput(attrs=habilidad_numberinput),
            "armasEnergiaPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "desarmadoTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "desarmadoMod":forms.NumberInput(attrs=habilidad_numberinput),
            "desarmadoPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "armasMeleeTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "armasMeleeMod":forms.NumberInput(attrs=habilidad_numberinput),
            "armasMeleePointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "lanzarTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "lanzarMod":forms.NumberInput(attrs=habilidad_numberinput),
            "lanzarPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "primerosAuxiliosTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "primerosAuxiliosMod":forms.NumberInput(attrs=habilidad_numberinput),
            "primerosAuxiliosPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "medicinaTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "medicinaMod":forms.NumberInput(attrs=habilidad_numberinput),
            "medicinaPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "sigiloTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "sigiloMod":forms.NumberInput(attrs=habilidad_numberinput),
            "sigiloPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "ganzuasTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "ganzuasMod":forms.NumberInput(attrs=habilidad_numberinput),
            "ganzuasPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "robarTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "robarMod":forms.NumberInput(attrs=habilidad_numberinput),
            "robarPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "trampasTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "trampasMod":forms.NumberInput(attrs=habilidad_numberinput),
            "trampasPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "cienciaTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "cienciaMod":forms.NumberInput(attrs=habilidad_numberinput),
            "cienciaPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "repararTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "repararMod":forms.NumberInput(attrs=habilidad_numberinput),
            "repararPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "pilotarTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "pilotarMod":forms.NumberInput(attrs=habilidad_numberinput),
            "pilotarPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "conversacionTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "conversacionMod":forms.NumberInput(attrs=habilidad_numberinput),
            "conversacionPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "truequeTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "truequeMod":forms.NumberInput(attrs=habilidad_numberinput),
            "truequePointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "juegoTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "juegoMod":forms.NumberInput(attrs=habilidad_numberinput),
            "juegoPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "vidaAlAireLibreTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "vidaAlAireLibreMod":forms.NumberInput(attrs=habilidad_numberinput),
            "vidaAlAireLibrePointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
            "atletismoTag":forms.CheckboxInput(attrs={
                "class":"fallout-font form-check-input",
            }),
            "atletismoMod":forms.NumberInput(attrs=habilidad_numberinput),
            "atletismoPointsSkill":forms.NumberInput(attrs=habilidad_numberinput),
        }

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='fallout-font form-group'>"))

class PlanillaFalloutForm(forms.ModelForm):
    class Meta:
        model = CharFallout
        fields = "__all__"
    
"""
def show_part(form,section=1): 
    display = ''
    for id,field in enumerate(form):  
         if int(section) == 1 and id > 3:
             break
         elif int(section) == 2 and id < 3:
             continue
         display += '<tr><td>'+field.label_tag+'</td>'
         display += '<td>'+field+'</td></tr>'
    return display   
"""