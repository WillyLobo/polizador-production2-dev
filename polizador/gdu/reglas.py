"""
Reglas de visibilidad/validez de las encuestas en formato JsonLogic (jsonlogic.com):
un subconjunto declarativo que se puede evaluar igual en el servidor y en el navegador,
en lugar de las funciones JS guardadas como texto en la base heredada.

Operadores soportados: "and", "or", "!", "==", "!=", ">", ">=", "<", "<=", "in" y {"var": "a.b"}.
"""
import re

OPERADORES_COMPARACION = {"==", "!=", ">", ">=", "<", "<="}


class ReglaInvalida(ValueError):
    pass


def _obtener(datos, ruta):
    valor = datos
    for parte in ruta.split("."):
        if not isinstance(valor, dict):
            return None
        valor = valor.get(parte)
    return valor


def evaluar(regla, datos):
    """Evalúa una regla JsonLogic contra las respuestas de la encuesta (dict variable -> valor)."""
    if not isinstance(regla, dict):
        return regla
    if len(regla) != 1:
        raise ReglaInvalida(f"Regla con más de un operador: {regla!r}")
    operador, args = next(iter(regla.items()))
    if operador == "var":
        return _obtener(datos, args)
    if not isinstance(args, list):
        args = [args]
    if operador == "and":
        resultado = True
        for arg in args:
            resultado = evaluar(arg, datos)
            if not resultado:
                return resultado
        return resultado
    if operador == "or":
        resultado = False
        for arg in args:
            resultado = evaluar(arg, datos)
            if resultado:
                return resultado
        return resultado
    if operador == "!":
        return not evaluar(args[0], datos)
    if operador == "in":
        # opción marcada en una pregunta de respuesta múltiple (o substring en un texto)
        valor, contenedor = (evaluar(arg, datos) for arg in args)
        return contenedor is not None and valor in contenedor
    if operador in OPERADORES_COMPARACION:
        a, b = (evaluar(arg, datos) for arg in args)
        if operador == "==":
            return a == b
        if operador == "!=":
            return a != b
        if a is None or b is None:
            return False
        return {">": a > b, ">=": a >= b, "<": a < b, "<=": a <= b}[operador]
    raise ReglaInvalida(f"Operador no soportado: {operador!r}")


# --- traducción desde las reglas JS heredadas: "(e) =>{ return <expresión> }" o "(e) => <expresión>" ---

_ENVOLTORIO_JS = re.compile(
    r"^\s*\(\s*e\s*\)\s*=>\s*(?:\{\s*return\s+(?P<expr>.*?);?\s*\}|(?P<expr_corta>[^{].*?))\s*$", re.S,
)
_TOKEN = re.compile(
    r"\s*(?:(?P<num>-?\d+(?:\.\d+)?)|(?P<str>'[^']*'|\"[^\"]*\")|(?P<op>===|!==|==|!=|>=|<=|&&|\|\||[()!<>,])"
    r"|(?P<id>[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*))"
)
_COMPARACIONES_JS = {"===": "==", "==": "==", "!==": "!=", "!=": "!=", ">": ">", ">=": ">=", "<": "<", "<=": "<="}


def _tokenizar(expr):
    tokens, pos = [], 0
    expr = expr.strip()
    while pos < len(expr):
        m = _TOKEN.match(expr, pos)
        if not m or m.end() == pos:
            raise ReglaInvalida(f"No se puede interpretar cerca de: {expr[pos:pos + 20]!r}")
        tipo = m.lastgroup
        tokens.append((tipo, m.group(tipo)))
        pos = m.end()
        while pos < len(expr) and expr[pos].isspace():
            pos += 1
    return tokens


class _Parser:
    # precedencia JS: || < && < comparación < ! < primario
    def __init__(self, tokens):
        self.tokens, self.i = tokens, 0

    def _ver(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else (None, None)

    def _tomar(self, valor=None):
        tipo, token = self._ver()
        if token is None or (valor is not None and token != valor):
            raise ReglaInvalida(f"Se esperaba {valor or 'una expresión'} y se encontró {token!r}")
        self.i += 1
        return tipo, token

    def parsear(self):
        regla = self._or()
        if self.i != len(self.tokens):
            raise ReglaInvalida(f"Sobra texto desde {self._ver()[1]!r}")
        return regla

    def _or(self):
        partes = [self._and()]
        while self._ver()[1] == "||":
            self._tomar()
            partes.append(self._and())
        return partes[0] if len(partes) == 1 else {"or": partes}

    def _and(self):
        partes = [self._comparacion()]
        while self._ver()[1] == "&&":
            self._tomar()
            partes.append(self._comparacion())
        return partes[0] if len(partes) == 1 else {"and": partes}

    def _comparacion(self):
        izquierda = self._unario()
        if self._ver()[1] in _COMPARACIONES_JS:
            _, op = self._tomar()
            return {_COMPARACIONES_JS[op]: [izquierda, self._unario()]}
        return izquierda

    def _unario(self):
        if self._ver()[1] == "!":
            self._tomar()
            return {"!": [self._unario()]}
        return self._primario()

    def _primario(self):
        tipo, token = self._tomar()
        if token == "(":
            regla = self._or()
            self._tomar(")")
            return regla
        if tipo == "num":
            return float(token) if "." in token else int(token)
        if tipo == "str":
            return token[1:-1]
        if tipo == "id":
            if token in ("true", "false"):
                return token == "true"
            if token == "null":
                return None
            if token.startswith("e."):
                return {"var": token[2:]}
            if token == "v" and self._ver()[1] == "(":
                return self._opcion_marcada()
        raise ReglaInvalida(f"Elemento no soportado: {token!r}")

    def _opcion_marcada(self):
        # helper v(e, 'variable', opcion) de la app de encuestas heredada: la opción está
        # marcada en una pregunta de respuesta múltiple
        self._tomar("(")
        self._tomar("e")
        self._tomar(",")
        tipo, variable = self._tomar()
        self._tomar(",")
        opcion = self._primario()
        self._tomar(")")
        if tipo != "str" or isinstance(opcion, dict):
            raise ReglaInvalida("v() espera v(e, 'variable', valor)")
        return {"in": [opcion, {"var": variable[1:-1]}]}


def traducir_js(texto):
    """Traduce una regla JS heredada a JsonLogic. Devuelve None si la regla está vacía y
    lanza ReglaInvalida si usa algo fuera del subconjunto soportado."""
    texto = (texto or "").strip().strip("|").strip()
    if not texto:
        return None
    m = _ENVOLTORIO_JS.match(texto)
    if not m:
        raise ReglaInvalida(f"No tiene la forma (e) => {{ return ... }}: {texto[:60]!r}")
    return _Parser(_tokenizar(m.group("expr") or m.group("expr_corta"))).parsear()
