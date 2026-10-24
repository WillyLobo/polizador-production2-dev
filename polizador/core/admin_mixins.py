class StrSelectRelatedAdminMixin:
    """Evita N+1 cuando el __str__ del modelo recorre FKs.

    El admin llama a str(obj) por cada fila del changelist (el checkbox de acciones
    lo usa como aria-label), por cada resultado del autocomplete y por cada inline.
    `str_select_related` declara la cadena de FKs que necesita ese __str__ y se
    aplica en get_queryset, que comparten el changelist, el autocomplete y el borrado.

    El changelist solo aplica list_select_related si el queryset todavia no tiene
    select_related (ChangeList.get_queryset), asi que con este mixin una lista en
    list_select_related se suma aca; si no, se perderia en silencio.

    Los formfields FK que apuntan a un modelo registrado con este mixin reutilizan
    su `str_select_related`, asi los widgets de autocomplete de los inlines (que
    renderizan la opcion seleccionada con una query por fila) no suman mas queries.
    """
    str_select_related = ()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        related = [*self.str_select_related]
        list_select_related = getattr(self, "list_select_related", False)
        if isinstance(list_select_related, (list, tuple)):
            related += list_select_related
        if related:
            qs = qs.select_related(*related)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        remote_admin = self.admin_site._registry.get(db_field.remote_field.model)
        related = getattr(remote_admin, "str_select_related", ())
        if related and "queryset" not in kwargs:
            queryset = self.get_field_queryset(None, db_field, request)
            if queryset is None:
                queryset = db_field.remote_field.model._default_manager.all()
            kwargs["queryset"] = queryset.select_related(*related)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
