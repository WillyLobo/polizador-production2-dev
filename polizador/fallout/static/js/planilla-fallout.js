function actualizar() {
    actualizarHabilidades();
    actualizarModificadoresAtributosSecundarios();
}

function calculadorHabilidad(nodo) {

    // Parametros:
    //  nodo = id del nodo de la tabla
    var nodo = document.getElementById(nodo)

    // Surfear el parentazgo
    var habilidadTag = nodo.childNodes[1].childNodes[0].checked // Nodo Habilidad Tag
    var habilidadBase = parseInt(nodo.childNodes[3].innerHTML) // Nodo habilidadBase
    var habilidadSkill = parseInt(nodo.childNodes[5].childNodes[0].value) // Nodo habilidadSkill
    var habilidadMod = parseInt(nodo.childNodes[7].childNodes[0].value) // Nodo habilidadMod
    var habilidadTotal = nodo.childNodes[11] // Nodo habilidadTotal
    // Logging
    // console.log("######################")
    // console.log("Tag: "+habilidadTag+"("+typeof habilidadTag+")")
    // console.log("Base: "+habilidadBase+"("+typeof habilidadBase+")")
    // console.log("Skill: "+habilidadSkill+"("+typeof habilidadSkill+")")
    // console.log("Mod: "+habilidadMod+"("+typeof habilidadMod+")")
    // console.log("Total: "+habilidadTotal.innerHTML+"("+typeof habilidadTotal.innerHTML+")")
    habilidadTotal.innerHTML = habilidadBase+habilidadSkill+habilidadMod

    // Funcionalizar correctamente el calculo para el Tag de skill, de manera que no sobreescriba con 0 el valod de armasPequenasMod.
    habilidadMod = habilidadTag == true ? parseInt(habilidadMod) + 20 : habilidadMod
    // Escribir Funcion para reemplazar esta asquerosidad
    if (habilidadTag == true) {
        habilidadTotal.innerHTML= parseInt(habilidadBase) + parseInt(habilidadSkill) + parseInt(habilidadSkill) + parseInt(habilidadMod)
    } else {
        habilidadTotal.innerHTML = parseInt(habilidadBase) + parseInt(habilidadSkill) + parseInt(habilidadMod)
    };

    
}

function actualizarHabilidades() {
    // Variables de Habilidad Primaria
    var fue = parseInt(document.getElementById("id_StrStat").value)
    var per = parseInt(document.getElementById("id_PerStat").value)
    var res = parseInt(document.getElementById("id_ResStat").value)
    var car = parseInt(document.getElementById("id_CarStat").value)
    var int = parseInt(document.getElementById("id_IntStat").value)
    var agi = parseInt(document.getElementById("id_AgiStat").value)
    var sue = parseInt(document.getElementById("id_SueStat").value)

    // Escribir Funcion para reemplazar esta asquerosidad
    calculadorHabilidad("armasPequenasNode")
    calculadorHabilidad("armasGrandesNode")
    calculadorHabilidad("armasEnergiaNode")
    calculadorHabilidad("desarmadoNode")
    calculadorHabilidad("armasMeleeNode")
    calculadorHabilidad("lanzarNode")
    calculadorHabilidad("primerosAuxiliosNode")
    calculadorHabilidad("medicinaNode")
    calculadorHabilidad("sigiloNode")
    calculadorHabilidad("ganzuasNode")
    calculadorHabilidad("robarNode")
    calculadorHabilidad("trampasNode")
    calculadorHabilidad("cienciaNode")
    calculadorHabilidad("repararNode")
    calculadorHabilidad("pilotarNode")
    calculadorHabilidad("conversacionNode")
    calculadorHabilidad("truequeNode")
    calculadorHabilidad("juegoNode")
    calculadorHabilidad("vidaAlAireLibreNode")
    calculadorHabilidad("atletismoNode")
}

function habilidadPlus(habBase, habMod, habSkill, habSkillCheck, habTotal) {
    // Params: habilidad base, habilidad Mod, habilidad SkillPoints, habilidad Skill Check, habilidad total
    habBase = document.getElementById(habBase)
    habMod = document.getElementById(habMod)
    habSkill = document.getElementById(habSkill)
    habTotal = document.getElementById(habTotal)
    habSkillCheck = document.getElementById(habSkillCheck)
    
    // Insert gif de vómito
    if (parseFloat(habTotal.innerHTML) > 200) {
        habSkill.value = parseFloat(habSkill.value) + ((1/6))
    } else if (parseFloat(habTotal.innerHTML) > 175) {
        habSkill.value = parseFloat(habSkill.value) + ((1/5))
    } else if (parseFloat(habTotal.innerHTML) > 150) {
        habSkill.value = parseFloat(habSkill.value) + ((1/4))
    } else if (parseFloat(habTotal.innerHTML) > 125) {
        habSkill.value = parseFloat(habSkill.value) + ((1/3))
    } else if (parseFloat(habTotal.innerHTML) > 100) {
        habSkill.value = parseFloat(habSkill.value) + ((1/2))
    } else if (parseFloat(habTotal.innerHTML) <= 100) {
        habSkill.value = parseFloat(habSkill.value) + ((1))
    } else if (parseFloat(habTotal.innerHTML) <= 0) {
        habSkill.value = 0
    }  
    // console.log(habSkill.value)
    actualizar()
}

function habilidadMinus(habBase, habMod, habSkill, habSkillCheck, habTotal) {
    // Params: habilidad base, habilidad Mod, habilidad SkillPoints, habilidad total
    habBase = document.getElementById(habBase)
    habMod = document.getElementById(habMod)
    habSkill = document.getElementById(habSkill)
    habTotal = document.getElementById(habTotal)
    habSkillCheck = document.getElementById(habSkillCheck)

    // Insert gif de vómito
    if (parseFloat(habTotal.innerHTML) > 200) {
        habSkill.value = parseFloat(habSkill.value) - ((1/6))
    } else if (parseFloat(habTotal.innerHTML) > 175) {
        habSkill.value = parseFloat(habSkill.value) - ((1/5))
    } else if (parseFloat(habTotal.innerHTML) > 150) {
        habSkill.value = parseFloat(habSkill.value) - ((1/4))
    } else if (parseFloat(habTotal.innerHTML) > 125) {
        habSkill.value = parseFloat(habSkill.value) - ((1/3))
    } else if (parseFloat(habTotal.innerHTML) > 100) {
        habSkill.value = parseFloat(habSkill.value) - ((1/2))
    } else if (parseFloat(habTotal.innerHTML) <= 100) {
        habSkill.value = parseFloat(habSkill.value) - ((1))
    } else if (parseFloat(habTotal.innerHTML) <= 0) {
        habSkill.value = 0
    }
    // console.log(habSkill.value)
    actualizar()
}

function actualizarModificadoresAtributosSecundarios() {
    var fue = parseInt(document.getElementById("id_StrStat").value)
    var per = parseInt(document.getElementById("id_PerStat").value)
    var res = parseInt(document.getElementById("id_ResStat").value)
    var car = parseInt(document.getElementById("id_CarStat").value)
    var int = parseInt(document.getElementById("id_IntStat").value)
    var agi = parseInt(document.getElementById("id_AgiStat").value)
    var sue = parseInt(document.getElementById("id_SueStat").value)
    // Puntos de Golpe por Nivel
    document.getElementById("pgPorNivelPersonaje").value = Math.floor(3 + (res /2))
    // Puntos de Habilidad por Nivel
    document.getElementById("habilidadPorNivelPersonaje").value = Math.floor(5 + (2 + int))

    // Puntos de Accion
    document.getElementById("apBase").innerHTML = Math.floor(5 + agi / 2)
    document.getElementById("apTotal").innerHTML = parseInt(document.getElementById("apBase").innerHTML) + parseInt(document.getElementById("id_apMod").value)
    // Secuencia
    document.getElementById("secBase").innerHTML = Math.floor(2* per)
    document.getElementById("secTotal").innerHTML = parseInt(document.getElementById("secBase").innerHTML) + parseInt(document.getElementById("id_secMod").value)
    // Bonuns Daño Melee
    if (Math.floor(fue-5) < 1) {
        document.getElementById("danoMeleeBase").innerHTML = 1
    }
    else {
        document.getElementById("danoMeleeBase").innerHTML = Math.floor(fue-5)
    };
    document.getElementById("danoMeleeTotal").innerHTML = parseInt(document.getElementById("danoMeleeBase").innerHTML) + parseInt(document.getElementById("id_danoMeleeMod").value)
    // Probabilidad de Critico
    document.getElementById("probCriticoBase").innerHTML = Math.floor(sue)
    document.getElementById("probCriticoTotal").innerHTML = parseInt(document.getElementById("probCriticoBase").innerHTML) + parseInt(document.getElementById("id_probCriticoMod").value)
    // Ratio de Curacion
    document.getElementById("ratioCuracionBase").innerHTML = Math.floor(res/3)
    document.getElementById("ratioCuracionTotal").innerHTML = parseInt(document.getElementById("ratioCuracionBase").innerHTML) + parseInt(document.getElementById("id_ratioCuracionMod").value)
    // Capacidad de Carga
    document.getElementById("capCargaBase").innerHTML = Math.floor(25 + 25*fue)
    document.getElementById("capCargaTotal").innerHTML = parseInt(document.getElementById("capCargaBase").innerHTML) + parseInt(document.getElementById("id_capCargaMod").value)
    // Resistencia al Veneno
    document.getElementById("resVenenoBase").innerHTML = Math.floor(5 * res)
    document.getElementById("resVenenoTotal").innerHTML = parseInt(document.getElementById("resVenenoBase").innerHTML) + parseInt(document.getElementById("id_resVenenoMod").value)
    // Resistencia a la Radiacion
    document.getElementById("resRadiacionBase").innerHTML = Math.floor(2 * res)
    document.getElementById("resRadiacionTotal").innerHTML = parseInt(document.getElementById("resRadiacionBase").innerHTML) + parseInt(document.getElementById("id_resRadiacionMod").value)
    // Resistencia a la Electricidad
    document.getElementById("resElectricidadBase").innerHTML = 0
    document.getElementById("resElectricidadTotal").innerHTML = parseInt(document.getElementById("resElectricidadBase").innerHTML) + parseInt(document.getElementById("id_resElectricidadMod").value)
    // Resistencia al Gas
    document.getElementById("resGasBase").innerHTML = 0
    document.getElementById("resGasTotal").innerHTML = parseInt(document.getElementById("resGasBase").innerHTML) + parseInt(document.getElementById("id_resGasMod").value)
    // Implante
    document.getElementById("implanteBase").innerHTML = Math.floor(10 * (int + res))
    document.getElementById("implanteTotal").innerHTML = parseInt(document.getElementById("implanteBase").innerHTML) + parseInt(document.getElementById("id_implanteMod").value)

    //Calculos de Habilidad Base
    armasPequenasBase.innerHTML = (5 + (4 * agi))
    armasGrandesBase.innerHTML = (0 + 2 * agi)
    armasEnergiaBase.innerHTML = (0 + 2 * agi)
    desarmadoBase.innerHTML = (30 + 2 * (agi + fue))
    armasMeleeBase.innerHTML = (20 + 2 * (agi + fue))
    lanzarBase.innerHTML = (0 + (4 * agi))
    primerosAuxiliosBase.innerHTML = (2*(per + int))
    medicinaBase.innerHTML = (5 + per + int)
    sigiloBase.innerHTML = (5 + (3 * agi))
    ganzuasBase.innerHTML = (10 + per + agi)
    robarBase.innerHTML = (0 + (3 * agi))
    trampasBase.innerHTML = (0 + per + agi)
    cienciaBase.innerHTML = (0 + (4 * int))
    repararBase.innerHTML = (0 + (3 * int))
    pilotarBase.innerHTML = (2 * (agi + per))
    conversacionBase.innerHTML = (0 + (5 * car))
    truequeBase.innerHTML = (0 + (4 * car))
    juegoBase.innerHTML = (0 + (5 * sue))
    vidaAlAireLibreBase.innerHTML = (2 * (res + int))
    atletismoBase.innerHTML = (5 + (2 * (fue + agi)))

    //Calculo de Habilidades Totales
    actualizarHabilidades()
}
