import ipaddress


def client_ip(request):
    """IP del cliente, o None si no hay ninguna válida. Para guardar en un
    GenericIPAddressField junto a un registro de actividad (LoginEvent, EventoVisor de gdu).

    Se confía en la primera entrada de X-Forwarded-For porque en el servidor nginx la
    pisa con la dirección real del cliente (que a su vez saca de CF-Connecting-IP solo
    cuando el pedido viene del túnel de Cloudflare). No leer CF-Connecting-IP acá: un
    cliente que entra por la LAN, sin pasar por Cloudflare, puede mandar ese header.
    El valor se valida porque fuera de ese nginx (desarrollo, otro proxy) el header lo
    escribe el cliente, y uno que no sea una IP hace fallar el INSERT y, con él, el pedido
    que se quería registrar.
    """
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR") or ""
    for candidato in (forwarded_for.split(",")[0].strip(), request.META.get("REMOTE_ADDR")):
        try:
            return str(ipaddress.ip_address(candidato))
        except ValueError:
            continue
    return None
