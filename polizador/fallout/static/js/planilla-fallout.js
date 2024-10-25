
function calculadorHabilidad(nodo, operacion) {

    // Parametros:
    //  nodo = id del nodo de la tabla
    var nodo = document.getElementById(nodo)

    // Surfear el parentazgo
    var habilidadTag = nodo.childNodes[1].childNodes[1].childNodes[1].checked // Nodo Habilidad Tag
    var habilidadBase = parseInt(nodo.children[2].innerText) // Nodo habilidadBase
    var habilidadMod = parseInt(nodo.children[3].childNodes[1].value) // Nodo habilidadMod
    var habilidadSkill = nodo.children[4].childNodes[1] // Nodo Puntos de habilidad.
    var habilidadTotal = nodo.childNodes[11] // Nodo habilidadTotal

    if (operacion == 'plus') {
        habilidadSkill.value = parseInt(habilidadSkill.value) + 1
    } else if (operacion == 'minus') {
        habilidadSkill.value = parseInt(habilidadSkill.value) - 1
    }
    habCalculada = habilidadBase
    habilidadTotal.innerText = Math.round(skillUp(habCalculada, parseInt(habilidadSkill.value)+habilidadMod, habilidadTag) * 100) / 100
}

function skillUp(habilidadTotal, habilidadPuntos, tagged) {
    habilidadTotal = parseFloat(habilidadTotal);
    habilidadPuntos = parseInt(habilidadPuntos);
    /*
    Corcky:
        Melee = 46 base * 2 tageado (92)
        Puntos por nivel = 11
        Nivel = 18
        Puntos de Habilidad = 11 * 18 = 198
    */
    for (let i = 0; i < habilidadPuntos; i++) {
        if (habilidadTotal <= 0) {
            return 0;
        }
        
        const incrementos = [
            [200, 1/6],
            [175, 1/5],
            [150, 1/4],
            [125, 1/3],
            [100, 1/2],
            [0, 1]
        ];
        
        for (const [limite, incremento] of incrementos) {
            if (habilidadTotal > limite) {
                if (tagged === true) {
                    habilidadTotal += incremento * 2;
                } else {
                    habilidadTotal += incremento;
                }
                break;
            }
        }
    }
    
    return habilidadTotal;
}
// //Calculos de Habilidad Base
// armasPequenasBase.innerHTML = (5 + (4 * agi))
// armasGrandesBase.innerHTML = (0 + 2 * agi)
// armasEnergiaBase.innerHTML = (0 + 2 * agi)
// desarmadoBase.innerHTML = (30 + 2 * (agi + fue))
// armasMeleeBase.innerHTML = (20 + 2 * (agi + fue))
// lanzarBase.innerHTML = (0 + (4 * agi))
// primerosAuxiliosBase.innerHTML = (2*(per + int))
// medicinaBase.innerHTML = (5 + per + int)
// sigiloBase.innerHTML = (5 + (3 * agi))
// ganzuasBase.innerHTML = (10 + per + agi)
// robarBase.innerHTML = (0 + (3 * agi))
// trampasBase.innerHTML = (0 + per + agi)
// cienciaBase.innerHTML = (0 + (4 * int))
// repararBase.innerHTML = (0 + (3 * int))
// pilotarBase.innerHTML = (2 * (agi + per))
// conversacionBase.innerHTML = (0 + (5 * car))
// truequeBase.innerHTML = (0 + (4 * car))
// juegoBase.innerHTML = (0 + (5 * sue))
// vidaAlAireLibreBase.innerHTML = (2 * (res + int))
// atletismoBase.innerHTML = (5 + (2 * (fue + agi)))