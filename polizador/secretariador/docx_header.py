"""
Reemplazo del encabezado (header/footer OOXML de primera página, par e
impar) de un .docx "cuerpo" (con tags Jinja de docxtpl) por el de otro .docx
"encabezado", sin tocar el resto del documento.

En OOXML el header/footer de un docx es una parte separada del cuerpo
(word/header*.xml, word/footer*.xml), referenciada desde el <w:sectPr> de
word/document.xml. Los tags Jinja de docxtpl viven exclusivamente en
word/document.xml, así que esta cirugía nunca los toca.
"""
import io
import posixpath
import zipfile
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

ET.register_namespace("", PKG_REL_NS)
ET.register_namespace("", CT_NS)

DOCUMENT_XML = "word/document.xml"
DOCUMENT_RELS = "word/_rels/document.xml.rels"
CONTENT_TYPES = "[Content_Types].xml"

_EXT_CONTENT_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "emf": "image/x-emf",
    "wmf": "image/x-wmf",
    "tif": "image/tiff",
    "tiff": "image/tiff",
}


def _section_refs(document_xml_bytes):
    """{'header'|'footer': {'first'|'default'|'even': rId}} de la última sectPr (la del cuerpo)."""
    root = ET.fromstring(document_xml_bytes)
    sect_prs = root.findall(f".//{{{W_NS}}}sectPr")
    refs = {"header": {}, "footer": {}}
    if not sect_prs:
        return refs
    sect_pr = sect_prs[-1]
    for tag, key in ((f"{{{W_NS}}}headerReference", "header"), (f"{{{W_NS}}}footerReference", "footer")):
        for el in sect_pr.findall(tag):
            tipo = el.get(f"{{{W_NS}}}type")
            rid = el.get(f"{{{R_NS}}}id")
            if tipo and rid:
                refs[key][tipo] = rid
    return refs


def _rels_map(rels_xml_bytes):
    """rId -> Target de un archivo _rels/*.rels."""
    root = ET.fromstring(rels_xml_bytes)
    return {rel.get("Id"): rel.get("Target") for rel in root.findall(f"{{{PKG_REL_NS}}}Relationship")}


def _rels_path_for(part_path):
    directory, name = posixpath.split(part_path)
    return posixpath.join(directory, "_rels", f"{name}.rels")


def _type_to_part(zf):
    """{'header'|'footer': {'first'|'default'|'even': 'word/headerN.xml'}} de un docx abierto."""
    refs = _section_refs(zf.read(DOCUMENT_XML))
    try:
        rels = _rels_map(zf.read(DOCUMENT_RELS))
    except KeyError:
        rels = {}
    result = {"header": {}, "footer": {}}
    for kind in ("header", "footer"):
        for tipo, rid in refs[kind].items():
            target = rels.get(rid)
            if target:
                result[kind][tipo] = posixpath.normpath(posixpath.join("word", target))
    return result


def tiene_encabezado_valido(fileobj):
    """True si fileobj es un .docx con al menos un header referenciado en su sectPr."""
    pos = fileobj.tell()
    fileobj.seek(0)
    try:
        with zipfile.ZipFile(fileobj) as zf:
            mapping = _type_to_part(zf)
    except (zipfile.BadZipFile, KeyError, ET.ParseError):
        return False
    finally:
        fileobj.seek(pos)
    return bool(mapping["header"])


def inject_header(body_docx, header_docx):
    """
    Devuelve un BytesIO con el docx `body_docx` (path o file-like), pero con
    sus partes de header/footer (first/default/even) reemplazadas por las de
    `header_docx` (path o file-like) para cada slot presente en ambos.
    Slots que el header fuente no trae se dejan sin cambios en el cuerpo.
    """
    with zipfile.ZipFile(body_docx) as body_zf:
        body_infos = body_zf.infolist()
        body_bytes = {info.filename: body_zf.read(info.filename) for info in body_infos}
        body_mapping = _type_to_part(body_zf)

    with zipfile.ZipFile(header_docx) as header_zf:
        header_mapping = _type_to_part(header_zf)

        ct_root = ET.fromstring(body_bytes[CONTENT_TYPES])
        existing_extensions = {d.get("Extension", "").lower() for d in ct_root.findall(f"{{{CT_NS}}}Default")}
        ct_changed = False
        media_counter = 0

        for kind in ("header", "footer"):
            for tipo, target_part in body_mapping[kind].items():
                source_part = header_mapping[kind].get(tipo)
                if not source_part:
                    continue
                try:
                    new_xml = header_zf.read(source_part)
                except KeyError:
                    continue

                target_rels_path = _rels_path_for(target_part)
                try:
                    source_rels_bytes = header_zf.read(_rels_path_for(source_part))
                except KeyError:
                    source_rels_bytes = None

                if source_rels_bytes is not None:
                    rels_root = ET.fromstring(source_rels_bytes)
                    for rel in rels_root.findall(f"{{{PKG_REL_NS}}}Relationship"):
                        rel_target = rel.get("Target")
                        if not rel_target or rel.get("TargetMode") == "External":
                            continue
                        media_part = posixpath.normpath(posixpath.join("word", rel_target))
                        try:
                            media_bytes = header_zf.read(media_part)
                        except KeyError:
                            continue
                        ext = media_part.rsplit(".", 1)[-1].lower()
                        media_counter += 1
                        new_name = f"image_encabezado_{media_counter}.{ext}"
                        new_media_part = f"word/media/{new_name}"
                        while new_media_part in body_bytes:
                            media_counter += 1
                            new_name = f"image_encabezado_{media_counter}.{ext}"
                            new_media_part = f"word/media/{new_name}"
                        body_bytes[new_media_part] = media_bytes
                        rel.set("Target", f"media/{new_name}")
                        if ext not in existing_extensions:
                            default_el = ET.SubElement(ct_root, f"{{{CT_NS}}}Default")
                            default_el.set("Extension", ext)
                            default_el.set("ContentType", _EXT_CONTENT_TYPES.get(ext, "application/octet-stream"))
                            existing_extensions.add(ext)
                            ct_changed = True
                    body_bytes[target_rels_path] = ET.tostring(rels_root, xml_declaration=True, encoding="UTF-8")

                body_bytes[target_part] = new_xml

        if ct_changed:
            body_bytes[CONTENT_TYPES] = ET.tostring(ct_root, xml_declaration=True, encoding="UTF-8")

    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as out_zf:
        written = set()
        for info in body_infos:
            out_zf.writestr(info, body_bytes[info.filename])
            written.add(info.filename)
        for name, data in body_bytes.items():
            if name not in written:
                out_zf.writestr(name, data)
    out.seek(0)
    return out


def con_encabezado_vigente(template_path):
    """
    Devuelve `template_path` con el header/footer actualizado al último
    EncabezadoDocumento subido, o el `template_path` sin cambios si nunca se
    subió ninguno (comportamiento actual, sin romper nada).
    """
    from secretariador.models import EncabezadoDocumento

    actual = EncabezadoDocumento.vigente()
    if actual is None:
        return template_path
    with actual.encabezadodocumento_archivo.open("rb") as f:
        header_bytes = f.read()
    return inject_header(template_path, io.BytesIO(header_bytes))
