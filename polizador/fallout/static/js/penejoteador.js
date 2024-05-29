function generar(raza, nivel) {
    // Habilidades principales arrancarian en 5 para PJs, pero siendo pnjs arrancan en 1, sumando un pool de 28
    // puntos para distribuir más 5 de creación = 33, mas 7 del minimo 1 = 40.
    var initialPool;
    var endPool;
    var nameList = [
        'Time', 'Past', 'Future', 'Dev',
        'Fly', 'Flying', 'Soar', 'Soaring', 'Power', 'Falling',
        'Fall', 'Jump', 'Cliff', 'Mountain', 'Rend', 'Red', 'Blue',
        'Green', 'Yellow', 'Gold', 'Demon', 'Demonic', 'Panda', 'Cat',
        'Kitty', 'Kitten', 'Zero', 'Memory', 'Trooper', 'XX', 'Bandit',
        'Fear', 'Light', 'Glow', 'Tread', 'Deep', 'Deeper', 'Deepest',
        'Mine', 'Your', 'Worst', 'Enemy', 'Hostile', 'Force', 'Video',
        'Game', 'Donkey', 'Mule', 'Colt', 'Cult', 'Cultist', 'Magnum',
        'Gun', 'Assault', 'Recon', 'Trap', 'Trapper', 'Redeem', 'Code',
        'Script', 'Writer', 'Near', 'Close', 'Open', 'Cube', 'Circle',
        'Geo', 'Genome', 'Germ', 'Spaz', 'Shot', 'Echo', 'Beta', 'Alpha',
        'Gamma', 'Omega', 'Seal', 'Squid', 'Money', 'Cash', 'Lord', 'King',
        'Duke', 'Rest', 'Fire', 'Flame', 'Morrow', 'Break', 'Breaker', 'Numb',
        'Ice', 'Cold', 'Rotten', 'Sick', 'Sickly', 'Janitor', 'Camel', 'Rooster',
        'Sand', 'Desert', 'Dessert', 'Hurdle', 'Racer', 'Eraser', 'Erase', 'Big',
        'Small', 'Short', 'Tall', 'Sith', 'Bounty', 'Hunter', 'Cracked', 'Broken',
        'Sad', 'Happy', 'Joy', 'Joyful', 'Crimson', 'Destiny', 'Deceit', 'Lies',
        'Lie', 'Honest', 'Destined', 'Bloxxer', 'Hawk', 'Eagle', 'Hawker', 'Walker',
        'Zombie', 'Sarge', 'Capt', 'Captain', 'Punch', 'One', 'Two', 'Uno', 'Slice',
        'Slash', 'Melt', 'Melted', 'Melting', 'Fell', 'Wolf', 'Hound',
        'Legacy', 'Sharp', 'Dead', 'Mew', 'Chuckle', 'Bubba', 'Bubble', 'Sandwich', 'Smasher', 'Extreme', 'Multi', 'Universe', 'Ultimate', 'Death', 'Ready', 'Monkey', 'Elevator', 'Wrench', 'Grease', 'Head', 'Theme', 'Grand', 'Cool', 'Kid', 'Boy', 'Girl', 'Vortex', 'Paradox'
      ];
    function getName() {
    var finalName = nameList[Math.floor(Math.random() * nameList.length)];
        return finalName;
        };
    const human = {
        tipo: "Humano",
        tipo_c: "H",
        initialFue:1,
        minFue:1,
        maxFue:10,
        initialPer:1,
        minPer:1,
        maxPer:10,
        initialRes:1,
        minRes:1,
        maxRes:10,
        initialCar:1,
        minCar:1,
        maxCar:10,
        initialInt:1,
        minInt:1,
        maxInt:10,
        initialAgi:1,
        minAgi:1,
        maxAgi:10,
        initialSue:1,
        minSue:1,
        maxSue:10,
        bonusPgPorNivel:0,
        bonusHabilidadPorNivel:0,
        bonusPuntosdeAccion:0,
        bonusSecuencia:0,
        bonusBonusDanoMelee:0,
        bonusCritChance:0,
        bonusHealRate:0,
        bonusCapCarga:0,
        bonusResVeneno:0,
        bonusResRadiacion:0,
        bonusResElectricidad:0,
        bonusResGas:0,
        bonusImplante:0
    };
    const ghoul = {
        tipo: "Ghoul",
        tipo_c:"G",
        initialFue:1,
        minFue:1,
        maxFue:6,
        initialPer:4,
        minPer:4,
        maxPer:14,
        initialRes:1,
        minRes:1,
        maxRes:10,
        initialCar:1,
        minCar:1,
        maxCar:9,
        initialInt:2,
        minInt:2,
        maxInt:13,
        initialAgi:1,
        minAgi:1,
        maxAgi:8,
        initialSue:5,
        minSue:1,
        maxSue:13
    };
    const superMutant = {
        tipo: "Super-Mutante",
        tipo_c:"S",
        initialFue:5,
        minFue:5,
        maxFue:13,
        initialPer:1,
        minPer:1,
        maxPer:10,
        initialRes:4,
        minRes:4,
        maxRes:12,
        initialCar:1,
        minCar:1,
        maxCar:8,
        initialInt:1,
        minInt:1,
        maxInt:8,
        initialAgi:1,
        minAgi:1,
        maxAgi:8,
        initialSue:1,
        minSue:1,
        maxSue:10
    };
    const deathClaw = {
        tipo: "Garra Mortal",
        tipo_c:"D",
        initialFue:6,
        minFue:6,
        maxFue:14,
        initialPer:4,
        minPer:4,
        maxPer:12,
        initialRes:1,
        minRes:1,
        maxRes:13,
        initialCar:1,
        minCar:1,
        maxCar:3,
        initialInt:1,
        minInt:1,
        maxInt:4,
        initialAgi:6,
        minAgi:6,
        maxAgi:16,
        initialSue:1,
        minSue:1,
        maxSue:10
    };   
    // Debug vars
    var iterations = 0;
    var totalStats = 0;
    // Devuelve random entre minStat y maxStat, chequeando que no sea superior al maximo en creacion.
    function get_random(stat, maxStat, minStat) {
        if (stat == maxStat){
            return stat;
        } else {
            var rng = Math.floor(Math.random() * (maxStat - minStat) + minStat);
            return rng;
        };
    };
    // Recolector de Argumentos
    if (raza == "H") {
        raza = human;
        initialPool = 5 + 7 + (5 - raza.initialFue) + (5 - raza.initialPer) + (5 - raza.initialRes) + (5 - raza.initialCar) + (5 - raza.initialInt) + (5 - raza.initialAgi) + (5 - raza.initialSue);
        endPool = initialPool;
    } else if (raza == "G") {
        raza = ghoul;
        initialPool = 5 + 7 + (5 - raza.initialFue) + (5 - raza.initialPer) + (5 - raza.initialRes) + (5 - raza.initialCar) + (5 - raza.initialInt) + (5 - raza.initialAgi) + (5 - raza.initialSue);
        endPool = initialPool;
    } else if (raza == "S") {
        raza = superMutant;
        initialPool = 5 + 7 + (5 - raza.initialFue) + (5 - raza.initialPer) + (5 - raza.initialRes) + (5 - raza.initialCar) + (5 - raza.initialInt) + (5 - raza.initialAgi) + (5 - raza.initialSue);
        endPool = initialPool;
    } else if (raza == "D") {
        raza = deathClaw;
        initialPool = 5 + 7 + (5 - raza.initialFue) + (5 - raza.initialPer) + (5 - raza.initialRes) + (5 - raza.initialCar) + (5 - raza.initialInt) + (5 - raza.initialAgi) + (5 - raza.initialSue);
        endPool = initialPool;
    } else if (typeof raza === "undefined") {
        console.log("########################################################");
        console.log("Uso:");
        console.log("   generar(\"raza\",nivel)");
        console.log("Raza: Corresponde a la raza del personaje a crear. Opciones: Humano, Ghoul, Super Mutante, Death Claw");
        console.log(" ");
        console.log("Nivel: Nivel del personaje a crear.");
        console.log("########################################################");
    } else {
        raza = human;
        initialPool = 5 + 7 + (5 - raza.initialFue) + (5 - raza.initialPer) + (5 - raza.initialRes) + (5 - raza.initialCar) + (5 - raza.initialInt) + (5 - raza.initialAgi) + (5 - raza.initialSue);
        endPool = initialPool;
    }
    ;
    nivel = nivel;

    // Distribuidor de puntos de habilidad. Loop volcando puntos hasta alcanzar el pool total de puntos.
    while (endPool != 0) {
        raza.initialFue = get_random(raza.initialFue, raza.maxFue, raza.minFue);
        raza.initialPer = get_random(raza.initialPer, raza.maxPer, raza.minPer);
        raza.initialRes = get_random(raza.initialRes, raza.maxRes, raza.minRes);
        raza.initialCar = get_random(raza.initialCar, raza.maxCar, raza.minCar);
        raza.initialInt = get_random(raza.initialInt, raza.maxInt, raza.minInt);
        raza.initialAgi = get_random(raza.initialAgi, raza.maxAgi, raza.minAgi);
        raza.initialSue = get_random(raza.initialSue, raza.maxSue, raza.minSue);
        iterations++; 
        endPool = initialPool - raza.initialFue - raza.initialPer - raza.initialRes - raza.initialCar - raza.initialInt - raza.initialAgi - raza.initialSue;
    };
    totalStats = raza.initialFue+raza.initialPer+raza.initialRes+raza.initialCar+raza.initialInt+raza.initialAgi+raza.initialSue;

    // Stats Secundarios
    pgPorNivel = Math.floor(3 + (raza.initialRes /2)) + raza.bonusPgPorNivel;
    habilidadPorNivel = Math.floor(5 + (2 + raza.initialInt)) + raza.bonusHabilidadPorNivel;
    puntosDeAccion = Math.floor(5 + raza.initialAgi / 2) + raza.bonusPuntosdeAccion;
    secuencia = Math.floor(2* raza.initialPer) + raza.bonusSecuencia;
    bonusDanoMelee = (Math.floor(raza.initialFue-5) < 1) ? (1) : (raza.initialFue - 5);
    critChance = (raza.initialSue) + raza.bonusCritChance;
    healRate = Math.floor(raza.initialRes / 3) + raza.bonusHealRate;
    capCarga = Math.floor(25 + 25 * raza.initialFue) + raza.bonusCapCarga;
    resVeneno = Math.floor(5 * raza.initialRes) + raza.bonusResVeneno;
    resRadiacion = Math.floor(2* raza.initialRes) + raza.bonusResRadiacion;
    resElectricidad = 0 + raza.bonusResElectricidad;
    resGas = 0 + raza.bonusResGas;
    implante = Math.floor(10 *(raza.initialInt+raza.initialRes)) + raza.bonusImplante;
    // Stats para Calculo
    habilidadPorNivelFinal = habilidadPorNivel * nivel
    

    // Habilidades
    armasPequenas = (5 + (4 * raza.initialAgi));
    armasGrandes = (0 + 2 * raza.initialAgi);
    armasEnergia = (0 + 2 * raza.initialAgi);
    desarmado = (30 + 2 * (raza.initialAgi + raza.initialFue));
    armasMelee = (20 + 2 * (raza.initialAgi + raza.initialFue));
    lanzar = (0 + (4 * raza.initialAgi));
    primerosAuxilios = (2*(raza.initialPer + raza.initialInt));
    medicina = (5 + raza.initialPer + raza.initialInt);
    sigilo = (5 + (3 * raza.initialAgi)),
    ganzuas = (10 + raza.initialPer + raza.initialAgi);
    robar = (0 + (3 * raza.initialAgi));
    trampas = (0 + raza.initialPer + raza.initialAgi);
    ciencia = (0 + (4 * raza.initialInt));
    reparar = (0 + (3 * raza.initialInt));
    pilotar = (2 * (raza.initialAgi + raza.initialPer));
    conversacion = (0 + (5 * raza.initialCar));
    trueque = (0 + (4 * raza.initialCar));
    juego = (0 + (5 * raza.initialSue));
    vidaAlAireLibre = (2 * (raza.initialRes + raza.initialInt));
    atletismo = (5 + (2 * (raza.initialFue + raza.initialAgi)));

    // Funciones Leveleadoras
    function calcSkillUp(skill) {
        habBase = skill
        habSkill = 0
        invHabAvail = habilidadPorNivelFinal
        habTotal = habBase + 20
        for (let step = 1; step < habilidadPorNivelFinal + 1; step++) {
            // Runs habilidadPorNivelFinal times, with values of step 1 through habilidadPorNivelFinal.
            if (habTotal > 200) {
                habTotal = habTotal + (1/6 * 2)
            } else if (habTotal > 175) {
                habTotal = habTotal + ((1/5 * 2))
            } else if (habTotal > 150) {
                habTotal = habTotal + ((1/4 * 2))
            } else if (habTotal > 125) {
                habTotal = habTotal + ((1/3 * 2))
            } else if (habTotal > 100 && habTotal <= 125) {
                habTotal = habTotal + (1/2 * 2)
            } else if (habTotal <= 100) {
                habTotal = habTotal + (1 * 2) 
            } else if (habTotal <= 0) {
                habTotal = 0
            }// endif
    } // endfor
    return habTotal
    } // exit function

    function lvlUp(lvl) {
    tageador = Math.floor(Math.random() * (7 - 1) + 1);
    switch(tageador) {
        case 1: tag = calcSkillUp(armasPequenas); break;
        case 2: tag = calcSkillUp(armasGrandes); break;
        case 3: tag = calcSkillUp(armasEnergia); break;
        case 4: tag = calcSkillUp(desarmado); break;
        case 5: tag = calcSkillUp(armasMelee); break;
        case 6: tag = calcSkillUp(lanzar); break;
        }
        return tag
    }
    lvlUp(nivel)

    //Nombre
    var nameChar = getName()
    document.getElementById("id_nombrePersonaje").value = nameChar
    console.log("Name: "+ nameChar);
    //Edad
    //Género
    //Raza
    document.getElementById("id_razaPersonaje").value = raza.tipo_c
    console.log("Race: "+ raza.tipo+"("+raza.tipo_c+")");
    //Altura
    //Peso
    //Facción
    //Nivel
    document.getElementById("id_nivelPersonaje").value = nivel
    console.log("Nivel: "+nivel)
    //Experiencia
    //Karma
    console.log("Starting Pool: " + initialPool);
    console.log("Iterations: " + iterations);
    console.log("End pool: " + endPool);
    //Stats
    document.getElementById("id_StrStat").value = raza.initialFue
    document.getElementById("id_PerStat").value = raza.initialPer
    document.getElementById("id_ResStat").value = raza.initialRes
    document.getElementById("id_CarStat").value = raza.initialCar
    document.getElementById("id_IntStat").value = raza.initialInt
    document.getElementById("id_AgiStat").value = raza.initialAgi
    document.getElementById("id_SueStat").value = raza.initialSue
    console.log("Stats in parentheses are Min-Max");
    console.log(
         "F:"+raza.initialFue+"("+raza.minFue+"-"+raza.maxFue+")"
        +"P:"+raza.initialPer+"("+raza.minPer+"-"+raza.maxPer+")"
        +"E:"+raza.initialRes+"("+raza.minRes+"-"+raza.maxRes+")"
        +"C:"+raza.initialCar+"("+raza.minCar+"-"+raza.maxCar+")"
        +"I:"+raza.initialInt+"("+raza.minInt+"-"+raza.maxInt+")"
        +"A:"+raza.initialAgi+"("+raza.minAgi+"-"+raza.maxAgi+")"
        +"L:"+raza.initialSue+"("+raza.minSue+"-"+raza.maxSue+")"
        );
    console.log("Total Stats: " + totalStats);
    console.log("#######################################");
    //PG por Nivel
    document.getElementById("pgPorNivelPersonaje").value = pgPorNivel
    console.log("Puntos de golpe p/nivel: "+ pgPorNivel);
    //Puntos de Habilidad por nivel
    document.getElementById("habilidadPorNivelPersonaje").value = habilidadPorNivel
    console.log("Puntos habilidad p/nivel: "+ habilidadPorNivel);
    console.log("Puntos de Habilidad para Distribuir: "+ habilidadPorNivel * nivel)
    //Persks por nivel
    document.getElementById("perksPorNivelPersonaje").value = 0
    //AP
    document.getElementById("apBase").innerHTML = document.getElementById("apTotal").innerHTML = puntosDeAccion
    document.getElementById("id_apMod").value = 0
    console.log("Puntos de acción: "+ puntosDeAccion);
    //Secuencia
    document.getElementById("secBase").innerHTML = document.getElementById("secTotal").innerHTML = secuencia
    document.getElementById("id_secMod").value = 0
    console.log("Secuencia: "+ secuencia);
    //Bonus Daño Melee
    document.getElementById("danoMeleeBase").innerHTML = document.getElementById("danoMeleeTotal").innerHTML = bonusDanoMelee
    document.getElementById("id_danoMeleeMod").value = 0
    console.log("Bonus Daño Melee: "+ bonusDanoMelee);
    //Probabilidad de Critico
    document.getElementById("probCriticoBase").innerHTML = document.getElementById("probCriticoTotal").innerHTML = critChance
    document.getElementById("id_probCriticoMod").value = 0
    console.log("Probabilidad de Crítico: "+ critChance);
    //Ratio Curacion
    document.getElementById("ratioCuracionBase").innerHTML = document.getElementById("ratioCuracionTotal").innerHTML = healRate
    document.getElementById("id_ratioCuracionMod").value = 0
    console.log("Ratio curación: "+ healRate);
    //Capacidad de Carga
    document.getElementById("capCargaBase").innerHTML = document.getElementById("capCargaTotal").innerHTML = capCarga
    document.getElementById("id_capCargaMod").valeue = 0
    console.log("Capacidad de Carga: "+ capCarga+"lbs"+"("+Math.floor(capCarga/2.205)+"Kg)");
    //Resistencia a Veneno
    document.getElementById("resVenenoBase").innerHTML = document.getElementById("resVenenoTotal").innerHTML = resVeneno
    document.getElementById("id_resVenenoMod").value = 0
    console.log("Resistencia al Veneno: "+ resVeneno);
    //Resistencia a Radiacion
    document.getElementById("resRadiacionBase").innerHTML = document.getElementById("resRadiacionTotal").innerHTML = resRadiacion
    document.getElementById("id_resRadiacionMod").value = 0
    console.log("Resistencia a la Radiación: "+ resRadiacion);
    //Resistencia a Electricidad
    document.getElementById("resElectricidadBase").innerHTML = document.getElementById("resElectricidadTotal").innerHTML = resElectricidad
    document.getElementById("id_resElectricidadMod").value = 0
    console.log("Resistencia a la Electricidad: "+ resElectricidad);
    //Resistencia a Gas
    document.getElementById("resGasBase").innerHTML = document.getElementById("resGasTotal").innerHTML = resGas
    document.getElementById("id_resGasMod").value = 0
    console.log("Resistencia a Gases: "+ resGas);
    //Implante
    document.getElementById("implanteBase").innerHTML = document.getElementById("implanteTotal").innerHTML = implante
    document.getElementById("id_implanteMod").value = 0
    console.log("Implante: "+ implante);
    //Habilidades
    console.log("#######################################");
    if (tageador == 1) {
        document.getElementById("id_armasPequenasTag").checked = true
        document.getElementById("id_armasPequenasMod").value = 0
        document.getElementById("armasPequenasTotal").innerHTML = Math.floor(tag)
        console.log("* - Armas Pequeñas: (Base "+armasPequenas+") - Total "+Math.floor(tag));
    } else {
        document.getElementById("id_armasPequenasTag").checked = false
        console.log("Armas Pequeñas: "+armasPequenas);
    }
    if (tageador == 2) {
        document.getElementById("id_armasGrandesTag").checked = true
        document.getElementById("id_armasGrandesMod").value = 0
        document.getElementById("armasGrandesTotal").innerHTML = Math.floor(tag)
        console.log("* - Armas Grandes: (Base "+armasGrandes+") - Total "+Math.floor(tag));
    } else {
        document.getElementById("id_armasGrandesTag").checked = false
        console.log("Armas Grandes: "+armasGrandes);
    }
    if (tageador == 3) {
        document.getElementById("id_armasEnergiaTag").checked = true
        document.getElementById("id_armasEnergiaMod").value = 0
        document.getElementById("armasEnergiaTotal").innerHTML = Math.floor(tag)
        console.log("* - Armas Energía: (Base "+armasEnergia+") - Total "+Math.floor(tag));
    } else {
        document.getElementById("id_armasEnergiaTag").checked = false
        console.log("Armas Energía: "+armasEnergia);
    }
    if (tageador == 4) {
        document.getElementById("id_desarmadoTag").checked = true
        document.getElementById("id_desarmadoMod").value = 0
        document.getElementById("desarmadoTotal").innerHTML = Math.floor(tag)
        console.log("* - Desarmado: (Base "+desarmado+") - Total "+Math.floor(tag));
    } else {
        document.getElementById("id_desarmadoTag").checked = false
        console.log("Desarmado: "+desarmado);
    }
    if (tageador == 5) {
        document.getElementById("id_armasMeleeTag").checked = true
        document.getElementById("id_armasMeleeMod").value = 0
        document.getElementById("armasMeleeTotal").innerHTML = Math.floor(tag)
        console.log("* - Armas Meleé: (Base "+armasMelee+") - Total "+Math.floor(tag));
    } else {
        document.getElementById("id_armasMeleeTag").checked = false
        console.log("Armas Meleé: "+armasMelee);
    }
    if (tageador == 6) {
        document.getElementById("id_lanzarTag").checked = true
        document.getElementById("id_lanzarMod").value = 0
        document.getElementById("lanzarTotal").innerHTML = Math.floor(tag)
        console.log("* - Lanzar: (Base "+lanzar+") - Total "+Math.floor(tag));
    } else {
        document.getElementById("id_lanzarTag").checked = false
        console.log("Lanzar: "+lanzar);
    }
    console.log("Primeros Auxilios: "+primerosAuxilios);
    console.log("Medicina: "+medicina+") - Total ");
    console.log("Sigilo: "+sigilo+") - Total ");
    console.log("Ganzúas: "+ganzuas+") - Total ");
    console.log("Robar: "+robar+") - Total ");
    console.log("Trampas: "+trampas);
    console.log("Ciencia: "+ciencia);
    console.log("Reparar: "+reparar);
    console.log("Pilotar: "+pilotar);
    console.log("Conversación: "+conversacion);
    console.log("Trueque: "+trueque);
    console.log("Juego: "+juego);
    console.log("Vida al Aire Libre: "+vidaAlAireLibre);
    console.log("Atletismo: "+atletismo);
    lvlUp(nivel)
}