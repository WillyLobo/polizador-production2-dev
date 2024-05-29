# Generated by Django 5.0.3 on 2024-05-28 12:50

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Raza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raza_tipo', models.CharField(max_length=30, verbose_name='Raza')),
            ],
        ),
        migrations.CreateModel(
            name='CharFallout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrePersonaje', models.CharField(max_length=60, verbose_name='Nombre del Personaje')),
                ('edadPersonaje', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Edad')),
                ('generoPersonaje', models.CharField(max_length=15, verbose_name='Género')),
                ('alturaPersonaje', models.DecimalField(decimal_places=2, default=1, max_digits=3, verbose_name='Altura')),
                ('pesoPersonaje', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Peso')),
                ('faccionPersonaje', models.CharField(blank=True, default='Ninguna', max_length=60, verbose_name='Faccion/Alianza')),
                ('nivelPersonaje', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Nivel')),
                ('experienciaPersonaje', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Experiencia')),
                ('karmaPersonaje', models.IntegerField(verbose_name='Karma')),
                ('StrStat', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Fuerza')),
                ('PerStat', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Percepción')),
                ('ResStat', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Resistencia')),
                ('CarStat', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Carisma')),
                ('IntStat', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Inteligencia')),
                ('AgiStat', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Agilidad')),
                ('SueStat', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Suerte')),
                ('apMod', models.IntegerField(default=0, verbose_name='Puntos de Acción Mod')),
                ('secMod', models.IntegerField(default=0, verbose_name='Secuencia Mod')),
                ('danoMeleeMod', models.IntegerField(default=0, verbose_name='Daño Melee Mod')),
                ('probCriticoMod', models.IntegerField(default=0, verbose_name='Probabilidad de Crítico Mod')),
                ('ratioCuracionMod', models.IntegerField(default=0, verbose_name='Ratio de Curación Mod')),
                ('capCargaMod', models.IntegerField(default=0, verbose_name='Capacidad de Carga Mod')),
                ('resVenenoMod', models.IntegerField(default=0, verbose_name='Resistencia Veneno Mod')),
                ('resRadiacionMod', models.IntegerField(default=0, verbose_name='Resistencia Radiació Mod')),
                ('resElectricidadMod', models.IntegerField(default=0, verbose_name='Resistencia a Electricidad')),
                ('resGasMod', models.IntegerField(default=0, verbose_name='Resistencia Gas Mod')),
                ('implanteMod', models.IntegerField(default=0, verbose_name='Implante Mod')),
                ('armasPequenasSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Armas Pequeñas')),
                ('armasPequenasMod', models.IntegerField(default=0, verbose_name='Armas Pequeñas Mod')),
                ('armasPequenasTag', models.BooleanField(default=False, verbose_name='Armas Pequeñas Tag')),
                ('armasGrandesSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Armas Grandes')),
                ('armasGrandesMod', models.IntegerField(default=0, verbose_name='Armas Grandes Mod')),
                ('armasGrandesTag', models.BooleanField(default=False, verbose_name='Armas Grandes Tag')),
                ('armasEnergiaSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Armas de Energía')),
                ('armasEnergiaMod', models.IntegerField(default=0, verbose_name='Armas de Energía Mod')),
                ('armasEnergiaTag', models.BooleanField(default=False, verbose_name='Armas de Energía Tag')),
                ('desarmadoSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Desarmado')),
                ('desarmadoMod', models.IntegerField(default=0, verbose_name='Desarmado Mod')),
                ('desarmadoTag', models.BooleanField(default=False, verbose_name='Desarmado Tag')),
                ('armasMeleeSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Armas Melee')),
                ('armasMeleeMod', models.IntegerField(default=0, verbose_name='Armas Melee Mod')),
                ('armasMeleeTag', models.BooleanField(default=False, verbose_name='Armas Melee Tag')),
                ('lanzarSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Lanzar')),
                ('lanzarMod', models.IntegerField(default=0, verbose_name='Lanzar Mod')),
                ('lanzarTag', models.BooleanField(default=False, verbose_name='Lanzar Tag')),
                ('primerosAuxiliosSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Primeros Auxilios')),
                ('primerosAuxiliosMod', models.IntegerField(default=0, verbose_name='Primeros Auxilios Mod')),
                ('primerosAuxiliosTag', models.BooleanField(default=False, verbose_name='Primeros Auxilios Tag')),
                ('medicinaSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Medicina')),
                ('medicinaMod', models.IntegerField(default=0, verbose_name='Medicina Mod')),
                ('medicinaTag', models.BooleanField(default=False, verbose_name='Medicina Tag')),
                ('sigiloSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Sigilo')),
                ('sigiloMod', models.IntegerField(default=0, verbose_name='Sigilo Mod')),
                ('sigiloTag', models.BooleanField(default=False, verbose_name='Sigilo Tag')),
                ('ganzuasSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Ganzuas')),
                ('ganzuasMod', models.IntegerField(default=0, verbose_name='Ganzuas Mod')),
                ('ganzuasTag', models.BooleanField(default=False, verbose_name='Ganzuas Tag')),
                ('robarSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Robar')),
                ('robarMod', models.IntegerField(default=0, verbose_name='Robar Mod')),
                ('robarTag', models.BooleanField(default=False, verbose_name='Robar Tag')),
                ('trampasSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Trampas')),
                ('trampasMod', models.IntegerField(default=0, verbose_name='Trampas Mod')),
                ('trampasTag', models.BooleanField(default=False, verbose_name='Trampas Tag')),
                ('cienciaSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Ciencia')),
                ('cienciaMod', models.IntegerField(default=0, verbose_name='Ciencia Mod')),
                ('cienciaTag', models.BooleanField(default=False, verbose_name='Ciencia Tag')),
                ('repararSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Reparar')),
                ('repararMod', models.IntegerField(default=0, verbose_name='Reparar Mod')),
                ('repararTag', models.BooleanField(default=False, verbose_name='Reparar Tag')),
                ('pilotarSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Pilotar')),
                ('pilotarMod', models.IntegerField(default=0, verbose_name='Pilotar Mod')),
                ('pilotarTag', models.BooleanField(default=False, verbose_name='Pilotar Tag')),
                ('conversacionSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Conversación')),
                ('conversacionMod', models.IntegerField(default=0, verbose_name='Conversación Mod')),
                ('conversacionTag', models.BooleanField(default=False, verbose_name='Conversación Tag')),
                ('truequeSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Trueque')),
                ('truequeMod', models.IntegerField(default=0, verbose_name='Trueque Mod')),
                ('truequeTag', models.BooleanField(default=False, verbose_name='Trueque Tag')),
                ('juegoSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Juego')),
                ('juegoMod', models.IntegerField(default=0, verbose_name='Juego Mod')),
                ('juegoTag', models.BooleanField(default=False, verbose_name='Juego Tag')),
                ('vidaAlAireLibreSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Vida al Aire Libre')),
                ('vidaAlAireLibreMod', models.IntegerField(default=0, verbose_name='Vida al Aire Libre Mod')),
                ('vidaAlAireLibreTag', models.BooleanField(default=False, verbose_name='Vida al Aire Libre Tag')),
                ('atletismoSkill', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Atletismo')),
                ('atletismoMod', models.IntegerField(default=0, verbose_name='Atletismo Mod')),
                ('atletismoTag', models.BooleanField(default=False, verbose_name='Atletismo Tag')),
                ('nombreJugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('razaPersonaje', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fallout.raza')),
            ],
        ),
    ]