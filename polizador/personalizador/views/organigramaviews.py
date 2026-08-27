from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from personalizador.models import Directorio, Gerencia, Direccion, Departamento


def _mermaid_label(nombre, cuof=None, ungi=None):
	label = nombre.strip().replace('"', "'")
	if cuof:
		label += f"<br/>CUOF: {cuof.strip()}"
	if ungi:
		label += f"<br/>UNGI: {ungi.strip()}"
	return label


def _build_organigrama_mermaid():
	directorios = {d.id: d for d in Directorio.objects.all()}
	gerencias = {g.id: g for g in Gerencia.objects.all()}
	direcciones = {r.id: r for r in Direccion.objects.select_related("direccion_gerencia", "direccion_directorio")}
	departamentos = {
		p.id: p for p in Departamento.objects.select_related(
			"departamento_direccion", "departamento_gerencia", "departamento_directorio",
		)
	}

	gerencias_by_directorio = {}
	for g in gerencias.values():
		gerencias_by_directorio.setdefault(g.gerencia_directorio_id, []).append(g)

	direcciones_by_gerencia = {}
	direcciones_directas_by_directorio = {}
	for r in direcciones.values():
		if r.direccion_gerencia_id:
			direcciones_by_gerencia.setdefault(r.direccion_gerencia_id, []).append(r)
		elif r.direccion_directorio_id:
			direcciones_directas_by_directorio.setdefault(r.direccion_directorio_id, []).append(r)

	departamentos_by_direccion = {}
	departamentos_by_gerencia = {}
	departamentos_by_directorio = {}
	for p in departamentos.values():
		if p.departamento_direccion_id:
			departamentos_by_direccion.setdefault(p.departamento_direccion_id, []).append(p)
		elif p.departamento_gerencia_id:
			departamentos_by_gerencia.setdefault(p.departamento_gerencia_id, []).append(p)
		elif p.departamento_directorio_id:
			departamentos_by_directorio.setdefault(p.departamento_directorio_id, []).append(p)

	lines = ["flowchart LR"]

	def departamento_lines(indent, p):
		lines.append(
			f'{indent}P{p.id}["{_mermaid_label(p.departamento_nombre, p.departamento_cuof, p.departamento_ungi)}"]'
		)

	# "Vocal 1" y "Vocal 2" quedan arriba y abajo de IPDUV (en vez de a la
	# misma altura que Presidencia) para no cruzarse con las flechas que
	# salen de Presidencia hacia sus gerencias/direcciones. Para lograrlo se
	# los ubica un rango antes que IPDUV (ambos con línea, sin flecha, hacia
	# ROOT); al ser las dos únicas fuentes de esa columna, mermaid las apila
	# verticalmente y centra IPDUV entre ellas.
	vocales = sorted(
		(did for did, d in directorios.items() if d.directorio_nombre.strip().lower() in ("vocal 1", "vocal 2")),
		key=lambda did: directorios[did].directorio_nombre.strip().lower(),
	)

	if len(vocales) == 2:
		vocal1_id, vocal2_id = vocales
		d1, d2 = directorios[vocal1_id], directorios[vocal2_id]
		lines.append(f'    D{vocal1_id}["{_mermaid_label(d1.directorio_nombre, d1.directorio_cuof, d1.directorio_ungi)}"]')
		lines.append('    ROOT(["IPDUV"])')
		lines.append(f'    D{vocal2_id}["{_mermaid_label(d2.directorio_nombre, d2.directorio_cuof, d2.directorio_ungi)}"]')
		lines.append(f"    D{vocal1_id} --- ROOT")
		lines.append(f"    D{vocal2_id} --- ROOT")
	else:
		lines.append('    ROOT(["IPDUV"])')
		vocales = []

	for did, d in directorios.items():
		if did in vocales:
			continue
		lines.append(f'    D{did}["{_mermaid_label(d.directorio_nombre, d.directorio_cuof, d.directorio_ungi)}"]')
		lines.append(f"    ROOT --> D{did}")

	for did in directorios:
		for g in gerencias_by_directorio.get(did, []):
			lines.append(f'    subgraph SG{g.id}[" "]')
			lines.append(f'        G{g.id}["{_mermaid_label(g.gerencia_nombre, g.gerencia_cuof, g.gerencia_ungi)}"]')
			for r in direcciones_by_gerencia.get(g.id, []):
				lines.append(
					f'        R{r.id}("{_mermaid_label(r.direccion_nombre, r.direccion_cuof, r.direccion_ungi)}")'
				)
				lines.append(f"        G{g.id} --> R{r.id}")
				for p in departamentos_by_direccion.get(r.id, []):
					departamento_lines("        ", p)
					lines.append(f"        R{r.id} --> P{p.id}")
			for p in departamentos_by_gerencia.get(g.id, []):
				departamento_lines("        ", p)
				lines.append(f"        G{g.id} --> P{p.id}")
			lines.append("    end")
			lines.append(f"    D{did} --> G{g.id}")

		directas = direcciones_directas_by_directorio.get(did, [])
		if directas:
			lines.append(f'    subgraph SGD{did}["Dependencia directa"]')
			for r in directas:
				lines.append(
					f'        R{r.id}("{_mermaid_label(r.direccion_nombre, r.direccion_cuof, r.direccion_ungi)}")'
				)
				for p in departamentos_by_direccion.get(r.id, []):
					departamento_lines("        ", p)
					lines.append(f"        R{r.id} --> P{p.id}")
			lines.append("    end")
			for r in directas:
				lines.append(f"    D{did} --> R{r.id}")

		for p in departamentos_by_directorio.get(did, []):
			departamento_lines("    ", p)
			lines.append(f"    D{did} --> P{p.id}")

	lines += [
		"    classDef directorio fill:#C98A2D,stroke:#7A5416,color:#1A1005,font-weight:bold;",
		"    classDef gerencia fill:#2F6FB0,stroke:#173A5E,color:#F5F8FA,font-weight:bold;",
		"    classDef direccion fill:#2F8F72,stroke:#175A44,color:#F5FBF8;",
		"    classDef departamento fill:#EDEAE2,stroke:#9C9587,color:#2A2620;",
		"    classDef root fill:#16232E,stroke:#0A1319,color:#EEF3F7,font-weight:bold;",
		"    classDef sg fill:#E4ECF3,stroke:#B9CBDB,color:#16232E,font-weight:bold;",
		"    class ROOT root;",
	]
	if directorios:
		lines.append("    class " + ",".join(f"D{d}" for d in directorios) + " directorio;")
	if gerencias:
		lines.append("    class " + ",".join(f"G{g}" for g in gerencias) + " gerencia;")
	if direcciones:
		lines.append("    class " + ",".join(f"R{r}" for r in direcciones) + " direccion;")
	if departamentos:
		lines.append("    class " + ",".join(f"P{p}" for p in departamentos) + " departamento;")
	if gerencias:
		lines.append("    class " + ",".join(f"SG{g}" for g in gerencias) + " sg;")

	return "\n".join(lines), {
		"directorios": len(directorios),
		"gerencias": len(gerencias),
		"direcciones": len(direcciones),
		"departamentos": len(departamentos),
	}


@login_required
@permission_required("personalizador.view_directorio", raise_exception=True)
def OrganigramaView(request):
	mermaid_source, counts = _build_organigrama_mermaid()
	return render(request, "organigrama.html", {
		"mermaid_source": mermaid_source,
		"counts": counts,
	})
