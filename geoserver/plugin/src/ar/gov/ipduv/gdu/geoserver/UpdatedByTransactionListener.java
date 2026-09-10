package ar.gov.ipduv.gdu.geoserver;

import java.sql.Timestamp;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.xml.namespace.QName;

import net.opengis.wfs.InsertElementType;
import net.opengis.wfs.PropertyType;
import net.opengis.wfs.TransactionType;
import net.opengis.wfs.UpdateElementType;
import net.opengis.wfs.WfsFactory;
import org.eclipse.emf.common.util.EList;
import org.geoserver.catalog.Catalog;
import org.geoserver.catalog.FeatureTypeInfo;
import org.geoserver.ows.AbstractDispatcherCallback;
import org.geoserver.ows.Request;
import org.geoserver.platform.GeoServerExtensions;
import org.geoserver.platform.Operation;
import org.geotools.api.feature.simple.SimpleFeature;
import org.geotools.api.feature.simple.SimpleFeatureType;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

/**
 * Completa updated_by/updated_at con el usuario realmente autenticado en GeoServer
 * (LDAP o local) en cada Insert/Update de un WFS-T Transaction, antes de que
 * GeoServer arme los datos que efectivamente escribe -- en vez de confiar en lo
 * que el cliente WFS-T mande (cualquiera puede falsificarlo) o en el rol de
 * conexión del datastore (el mismo para todos los usuarios).
 *
 * Engancha en DispatcherCallback.operationDispatched(), NO en TransactionListener:
 * se probó primero con TransactionListener.dataStoreChange(PRE_UPDATE) mutando
 * TransactionEvent.getAffectedFeatures(), y no tuvo ningún efecto -- confirmado
 * contra el código real de GeoServer (UpdateElementHandler.execute(), rama
 * 2.26.x) que arma el array `values[]` que se le pasa a
 * FeatureStore.modifyFeatures(names, values, filter) ANTES de disparar el
 * evento PRE_UPDATE, así que para cuando el listener corre ya es tarde. Acá en
 * cambio se edita directamente el TransactionType (el request WFS-T ya
 * parseado) antes de que el Dispatcher invoque la operación, que sí alcanza a
 * los handlers de Insert y de Update por igual.
 *
 * Requiere que catastro.set_updated() haga
 * "NEW.updated_by = COALESCE(NEW.updated_by, current_user)" en vez de pisar
 * incondicionalmente -- si no, el trigger lo sobreescribe igual. Ver
 * geoserver/README.md.
 *
 * El camino de Update chequea, vía el Catalog, que la tabla destino tenga
 * updated_by/updated_at antes de agregarlos (mismo chequeo que ya hacía el
 * camino de Insert con SimpleFeature.getFeatureType().getDescriptor()) --
 * antes no lo hacía y agregaba updated_by a CUALQUIER Update sin verificar,
 * lo que rompía con "No such property: updated_by" al editar directo una
 * tabla intermedia sin esa columna (ej. plano_mensura_intervencion, vista en
 * vivo al generalizar a plano_mensura/tierra, 2026-09-10).
 */
public class UpdatedByTransactionListener extends AbstractDispatcherCallback {

    private static final Logger LOGGER = Logger.getLogger("ar.gov.ipduv.gdu.geoserver");
    private static final String UPDATED_BY = "updated_by";
    private static final String UPDATED_AT = "updated_at";

    @Override
    public Operation operationDispatched(Request request, Operation operation) {
        Object[] params = operation.getParameters();
        if (params == null || params.length == 0 || !(params[0] instanceof TransactionType)) {
            return operation;
        }
        String username = currentUsername();
        if (username == null) {
            // Sin usuario autenticado real -- no tocar nada, el trigger cae a
            // current_user (rol del datastore) como antes.
            return operation;
        }

        TransactionType tx = (TransactionType) params[0];
        Timestamp now = new Timestamp(System.currentTimeMillis());

        try {
            for (Object o : (EList) tx.getInsert()) {
                InsertElementType insert = (InsertElementType) o;
                for (Object fo : (EList) insert.getFeature()) {
                    if (fo instanceof SimpleFeature) {
                        setFeatureAttributeIfPresent((SimpleFeature) fo, UPDATED_BY, username);
                        setFeatureAttributeIfPresent((SimpleFeature) fo, UPDATED_AT, now);
                    }
                }
            }
            for (Object o : (EList) tx.getUpdate()) {
                UpdateElementType update = (UpdateElementType) o;
                if (tieneAtributo(update.getTypeName(), UPDATED_BY)) {
                    setOrReplaceProperty(update, UPDATED_BY, username);
                }
                if (tieneAtributo(update.getTypeName(), UPDATED_AT)) {
                    setOrReplaceProperty(update, UPDATED_AT, now);
                }
            }
        } catch (Exception e) {
            // No abortar la transacción por esto -- ver comentario equivalente
            // más abajo. El trigger de Postgres sigue siendo la red de seguridad.
            LOGGER.log(Level.WARNING, "No se pudo completar updated_by/updated_at: " + e.getMessage(), e);
        }

        return operation;
    }

    private void setFeatureAttributeIfPresent(SimpleFeature f, String name, Object value) {
        if (f.getFeatureType().getDescriptor(name) != null) {
            f.setAttribute(name, value);
        }
    }

    private boolean tieneAtributo(QName typeName, String attr) {
        if (typeName == null) {
            return false;
        }
        try {
            // GeoServerExtensions.bean(Catalog.class) tira
            // MultipleBeansException: el contexto tiene más de un bean de
            // tipo Catalog (el crudo y el envuelto con seguridad) -- hay que
            // pedirlo por nombre. "catalog" es el bean convencional de
            // GeoServer para el catalog ya envuelto (con seguridad
            // aplicada), visto en vivo al agregar este chequeo (rompió
            // updated_by en TODAS las tablas hasta corregir esto).
            Catalog catalog = (Catalog) GeoServerExtensions.bean("catalog");
            if (catalog == null) {
                return false;
            }
            FeatureTypeInfo fti = catalog.getFeatureTypeByName(typeName.getNamespaceURI(), typeName.getLocalPart());
            if (fti == null) {
                return false;
            }
            SimpleFeatureType sft = (SimpleFeatureType) fti.getFeatureType();
            return sft.getDescriptor(attr) != null;
        } catch (Exception e) {
            LOGGER.log(Level.WARNING, "No se pudo resolver el esquema de " + typeName + ": " + e.getMessage(), e);
            return false;
        }
    }

    private void setOrReplaceProperty(UpdateElementType update, String name, Object value) {
        EList properties = update.getProperty();
        for (Object po : properties) {
            PropertyType p = (PropertyType) po;
            if (p.getName() != null && name.equals(p.getName().getLocalPart())) {
                p.setValue(value);
                return;
            }
        }
        PropertyType p = WfsFactory.eINSTANCE.createPropertyType();
        p.setName(new QName(name));
        p.setValue(value);
        properties.add(p);
    }

    private String currentUsername() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return null;
        }
        String name = auth.getName();
        if (name == null || "anonymousUser".equals(name)) {
            return null;
        }
        return name;
    }
}
