import os
import PyQt5
import qgis
import qgis.core

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from qgis.PyQt import QtCore
from qgis.PyQt.QtWidgets import QWidget, QDialogButtonBox, QListWidgetItem, QDialog, QListWidget,  QMainWindow, QScrollArea
from qgis.core import QgsRelation, QgsFeature, QgsVectorLayer, QgsMessageLog, QgsFeatureRequest, QgsProject, QgsExpression, QgsExpressionContext, QgsExpressionContextScope
from qgis.gui import QgsAttributeForm
from functools import partial

#cambiar a un path fijo en el S.O.
from forms.layer_config import  LayerConfig
# from forms.layer_config import find_layer_config
# FORM_CLASS, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'NN.ui'))


# print(lc)
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    QgsProject.instance().absolutePath(), 'forms/NN-nuevo.ui'))

FORM_CLASS_INSPECTOR, _ = uic.loadUiType(os.path.join(
    QgsProject.instance().absolutePath(), 'forms/NN.ui'))
print(FORM_CLASS)
print(FORM_CLASS_INSPECTOR)
# QgsMessageLog.logMessage(__file__, 'MyPlugin')



from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction



def my_form_open(dialog, layer, feature):
    # QgsMessageLog.logMessage(str(type(layer)), 'asdasdadasd')
    print('my_form_open')
    # print ('fields',feature.fields().names())
    config = LayerConfig().find(layer.id())

    # print(config)
    tipo: str = ''
    if dialog.parent() is not None:
        if isinstance(dialog.parent().parent(),QDialog):
            print('identify')
            tipo = 'identify'
        elif isinstance(dialog.parent().parent(),QgsMapCanvas):
            print('nuevo Feature')
            tipo = 'nuevo'
        elif isinstance(dialog.parent().parent(),QScrollArea):
            print('tabla')
            tipo = 'tabla'
        elif isinstance(dialog.parent().parent(),QMainWindow):
            tipo = 'multi'
            print('search o multiedit')
    
    if tipo in ['identify', 'nuevo']:
        dialog.parent().setFixedSize(config['size'][0], config['size'][1])
    # elif tipo == 'multi':
    #     print("multi")
    #     # dialog.parent().setFixedSize(config['size'][0], config['size'][1])
    #     print(dialog.setFixedSize)
    #     dialog.adjustSize()
    #     # dialog.parent().sizeHint(config['size'][0], config['size'][1])

    if 'nn' in config and len(config['nn']) >0:
        form = nnForm(dialog, layer, feature, config)
        pass
   


class nnDialog(QtWidgets.QDialog):
    def __init__(self, parent, layer, displayExpression, search=False):
        super( nnDialog, self).__init__(parent)
        pass

    def setup(self, parent, layer, displayExpression, search):
        '''
        método para setear todas las variables

        '''
        self.displayExpression = displayExpression
        self.layer =  layer
        self.search = search
        self.selectedItem = None

        self.populateList()

        # Add dynamic control when list is changing
        self.SEARCH.textChanged.connect(self.populateList)
        self.LIST.currentItemChanged.connect(self.selectElement)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def getSelected(self):
        return self.selectedItem

    def populateList(self, txtFilter=None):
        '''Fill the QListWidget with values'''
        # Delete everything
        self.LIST.clear()

        # # We need a request
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        if txtFilter is not None:
            # print('Not None')
            filter = u"({0}) LIKE '%{1}%'".format(self.displayExpression.expression(), txtFilter)
            request.setFilterExpression(filter)
            # print(filter)

        # # Grab the results from the layer
        features = self.layer.getFeatures(request)
        # print(features)

        context = QgsExpressionContext()
        scope = QgsExpressionContextScope()
        context.appendScope(scope)

        for feature in features:
            scope.setFeature(feature)
            # print(featureNN.attributes()) 
            
            #evaluo la expresion para obtener el valor a mostrar en el list
            value = self.displayExpression.evaluate(context)

            element = QListWidgetItem(str(value))
            # DESVÍO TEMPORAL PARA EL SPIKE N:N vs WFS-T (ver plan
            # en-lugar-de-geoserver-hashed-cupcake.md): feature.id() es el
            # FID interno de QGIS, no necesariamente el valor real de la
            # columna "id" -- contra Postgres directo siempre coincidían,
            # contra un layer WFS se vio en vivo que no (3 de 3 pruebas
            # guardaban el id inmediatamente anterior al elegido: DELIEL 901
            # quedaba como 900, CIMBARO 884 como 883, NOVELLI 1035 como
            # 1034). Se usa el atributo real en vez del FID.
            element.setData(Qt.UserRole, feature.attribute('id'))

            self.LIST.addItem(element)

    
    #reimplementar segun clase
    def selectElement(self, elementActual, elementAnterior):
        #Habilitar el boton de OK
        # print(self.selectedItem)
        if elementActual:
            self.selectedItem = {'id': elementActual.data(Qt.UserRole)}
            #Habilitar el boton de OK
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.selectedItem = None
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

class nnDialogPM(nnDialog, FORM_CLASS):
    def __init__(self, parent, layer, displayExpression, search=False):
        # print('__init__ nnDialog', initValues)
        """Constructor."""
        super( nnDialogPM, self).__init__( parent, layer, displayExpression, search)
        self.setupUi(self)
        self.setup(parent, layer, displayExpression, search)

    #reimplementado para PM
    def getSelected(self):
        if self.selectedItem:
            item = self.selectedItem.copy()
            item['tipo'] = self.TIPO.currentText()
            return item
        else:
            return None
 

class nnDialogInspector(nnDialog, FORM_CLASS_INSPECTOR):
    def __init__(self, parent, layer, displayExpression, search=False):
        """Constructor."""
        super(nnDialogInspector, self).__init__(parent, layer, displayExpression, search)
        self.setupUi(self)
        self.setup(parent, layer, displayExpression, search)


class nnDialogEjecutor(nnDialog, FORM_CLASS_INSPECTOR):
    def __init__(self, parent, layer, displayExpression, search=False):
        """Constructor."""
        super(nnDialogEjecutor, self).__init__(parent, layer, displayExpression, search)
        self.setupUi(self)
        self.setup(parent, layer, displayExpression, search)




def buscar_feature_por_id(layer, valor_id):
    """DESVÍO TEMPORAL PARA EL SPIKE N:N vs WFS-T (ver plan
    en-lugar-de-geoserver-hashed-cupcake.md): reemplaza layer.getFeature(x),
    que busca por QgsFeatureId (el id interno de QGIS). Contra Postgres
    directo el FID siempre coincidía con el valor real de la columna "id",
    así que layer.getFeature(id_real) siempre traía el feature correcto --
    contra un layer WFS no es así (se vio en vivo: pedir "ZENTRA" por su id
    real terminaba trayendo "ZETA", el feature vecino). Busca por el
    ATRIBUTO "id" en vez del FID."""
    req = QgsFeatureRequest().setFilterExpression('"id" = {}'.format(valor_id))
    for f in layer.getFeatures(req):
        return f
    return None


def id_real(feature):
    """Devuelve el valor del atributo "id" real de un feature, o None si el
    feature no trae ese campo -- feature.attribute('id') tira KeyError en
    vez de devolver None cuando el campo no está en el subconjunto de
    atributos del feature (se vio en vivo: al abrir recién la tabla de
    atributos de Intervención, QGIS arma el primer formulario con un
    feature "parcial" que todavía no tiene todos los campos resueltos).
    Tratarlo como "sin id todavía" en vez de crashear."""
    idx = feature.fields().indexOf('id')
    if idx < 0:
        return None
    valor = feature.attribute(idx)
    return valor if valor not in (None,) else None


class nnConfig:
    
    def __init__(self, dialog: QgsAttributeForm, layer: QgsVectorLayer, feature: QgsFeature, form,  configNN: dict):
        print ('initNNCONFIG')
        self.dialog = dialog
        self.layer = layer
        self.feature = feature
        self.config = configNN
        
        
        self.search: bool = False #????
        self.lista: QListWidget = dialog.findChild(QWidget, self.config['element'])
        self.nnButton: QWidget = dialog.findChild(QWidget, self.config['element'] + 'Add') 
        self.delButton: QWidget = dialog.findChild(QWidget, self.config['element'] + 'Del') 
        self.values: list = []
        self.originalNN: list = []
        self.selectedItem = None

        print('nnButton', self.nnButton)
        print('element', self.config['element'])
        
        self.dirtyField: str = configNN['dirty_field']

        self.layerNN: QgsVectorLayer = None
        self.layerN: QgsVectorLayer = None
        self.relationN1: QgsRelation = None
        self.relation1N: QgsRelation = None
        #Context para la expression        
        self.context = QgsExpressionContext()
        self.scope = QgsExpressionContextScope()
        self.context.appendScope(self.scope)

        ## conectamos el boton a la funcion con el objeto (self) como parametro
        if not isinstance(dialog.parent(),QDialog): #es una tabla, no un dialog
            try:
                self.nnButton.clicked.disconnect()
            except:
                pass
        
        self.nnButton.clicked.connect(partial(form.openNN, self))
        # return 
        self.delButton.clicked.connect(self.remove)
        self.lista.currentItemChanged.connect(self.selectElement)
        
        # Disponible solo si el feature ya existe, y si la capa es editable.
        # DESVÍO TEMPORAL PARA EL SPIKE N:N vs WFS-T (ver plan
        # en-lugar-de-geoserver-hashed-cupcake.md): antes esto se evaluaba
        # una sola vez acá, en el momento en que se arma el formulario -- si
        # activabas "Alternar edición" DESPUÉS de abrir esa fila, el botón
        # quedaba deshabilitado hasta ir a otra fila y volver (recién ahí se
        # reconstruye el formulario y se vuelve a evaluar). Ahora también se
        # reacciona a que la capa entre/salga de edición mientras el
        # formulario ya está abierto.
        self.layer.editingStarted.connect(self._actualizar_estado_nnButton)
        self.layer.editingStopped.connect(self._actualizar_estado_nnButton)
        self._actualizar_estado_nnButton()

        #tabla intermedia 
        id_tabla_intermedia = LayerConfig().get(self.config['tabla_intermedia'])['id']
        
        print(id_tabla_intermedia)
        
        self.layerNN = QgsProject().instance().mapLayers()[id_tabla_intermedia]
        #tabla del otro extremo (final)
        id_tabla_final = LayerConfig().get(self.config['tabla_final'])['id']
        self.layerN = QgsProject().instance().mapLayers()[id_tabla_final]
        # print(self.layerN)

        #Relation entre la tabla local y la intermedia
        self.relation1N = QgsProject.instance().relationManager().relations()[self.config['id']]

        #Relation entre la tabla intermedia intermedia y la extrema
        self.relationN1 = QgsProject.instance().relationManager().relations()[self.config['id_relacion_tabla_final']]
        #Expresion para el display de la tabla final
        self.displayExpression = QgsExpression(self.layerN.displayExpression())

    def _actualizar_estado_nnButton(self):
        try:
            valor_id = id_real(self.feature)
            habilitado = bool(valor_id) and self.layer.isEditable() and isinstance(valor_id, int) and valor_id > 0
            self.nnButton.setEnabled(habilitado)
        except RuntimeError:
            # El widget del formulario ya no existe (se navegó a otra fila
            # y este formulario se destruyó) -- la señal del layer sigue
            # viva más tiempo que el formulario, se ignora.
            pass

    def removeItemFromList(self, item):
        # self.lista.takeItem(item)
        for value in self.values:
            if value == item.data(Qt.UserRole):
                 self.values.remove(value)

        print(item.data(Qt.UserRole))
        r = self.lista.row(item)
        self.lista.takeItem(r)

    def selectElement(self, elementActual, elementAnterior):
        
        # print(self.selectedItem)
        if elementActual:
            #Habilitar el boton de Borrar
            self.selectedItem = elementActual
        else:
            #Deshabilitar el boton de Borrar
            self.selectedItem = None

    def remove(self):
        if self.selectedItem:
            self.removeItemFromList(self.selectedItem)
            self.setFormDirty()

    def isDirty(self) -> bool:
        print(self.values)
        print(self.originalNN)
        #chequear si cada value in originalNN, y viceversa
        for val in self.values:
            if val not in self.originalNN:
                return True
        for val in self.originalNN:
            if val not in self.values:
                return True
        
        return False

    def setFormDirty(self):
        # Con esto me aseguro que el feature quede marcado como "dirty", así es guardado
        # HORRIBLE!!! Buscar otra forma mejor...
        print('dirty',self.dirtyField)
        self.dialog.changeAttribute(self.dirtyField, str(self.feature.attribute(self.dirtyField))+' ', '')
        self.dialog.changeAttribute(self.dirtyField, str(self.feature.attribute(self.dirtyField)).strip(), '')

    #Caso Estandar (solo id), reimplementar segun clase
    def populateList(self):
        self.lista.clear()
        self.values.clear()
            
        #Features asociadas de la Tabla intermedia
        features = self.relation1N.getRelatedFeatures(self.feature)
    
        for feature in features:
            #obtengo la fk
            fk = feature.attribute(self.relationN1.referencingFields()[0])
            # print(fk)
            #busco el feature a partir de la fk
            featureN = buscar_feature_por_id(self.layerN, fk)
            self.addItemToList(featureN)
            self.originalNN.append({'id':feature.id()})

    #Caso Estandar (solo id), reimplementar segun clase
    def add(self,item):
        featureN = buscar_feature_por_id(self.layerN, item['id'])
        self.addItemToList(featureN)
        self.setFormDirty()

    #Caso Estandar (solo id), reimplementar segun clase
    def addItemToList(self, feature):
        self.scope.setFeature(feature)
        value = self.displayExpression.evaluate(self.context)
        element = QListWidgetItem(str(value))
        element.setData(Qt.UserRole, {'id':feature.attribute('id')})
        self.lista.addItem(element)
        self.values.append({'id':feature.attribute('id')})

    #Caso Estandar (solo id), reimplementar segun clase
    def save(self):
        # DESVÍO TEMPORAL PARA EL SPIKE N:N vs WFS-T: mismo bug FID-vs-
        # atributo "id" que en buscar_feature_por_id, pero del lado de la
        # capa referenciante (Intervención) -- se vio en vivo que un guardado
        # con feature.id() terminaba en otra Intervención (id 1001 pedido,
        # id 890 guardado). Se usa el atributo real en vez del FID.
        valor_id = id_real(self.feature)
        print('nnConfig:save | feature id real =', valor_id)

        if valor_id and self.isDirty() and self.layer.isEditable() and isinstance(valor_id, int) and valor_id > 0:
            self.layerNN.startEditing()
            request = self.relation1N.getRelatedFeaturesRequest(self.feature)
            fids = [f.id() for f in self.layerNN.getFeatures(request)]
            # print(fids)
            self.layerNN.dataProvider().deleteFeatures(fids)

            attr_id_1N = self.relation1N.referencingFields()[0]
            attr_id_N1 = self.relationN1.referencingFields()[0]
            features = []
            print('values',self.values)
            for value in self.values:
                feat = QgsFeature(self.layerNN.fields())
                feat.setAttribute(attr_id_1N, valor_id)
                feat.setAttribute(attr_id_N1, value['id'])
                feat.setAttribute('id', None)
                features.append(feat)

            self.layerNN.dataProvider().addFeatures(features)

class nnConfigPM(nnConfig):
    def __init__(self, dialog: QgsAttributeForm, layer: QgsVectorLayer, feature: QgsFeature, form,  configNN: dict):
        super().__init__(dialog, layer, feature, form, configNN)

    #reimplementado para PM
    def populateList(self):
        self.lista.clear()
        self.values.clear()
            
        #Features asociadas de la Tabla intermedia
        features = self.relation1N.getRelatedFeatures(self.feature)
    
        for feature in features:
            #obtengo la fk
            fk = feature.attribute(self.relationN1.referencingFields()[0])
            # print(fk)
            #busco el feature a partir de la fk
            featureN = buscar_feature_por_id(self.layerN, fk)
            self.addItemToList(featureN, feature.attribute('tipo'))
            self.originalNN.append({'id':feature.id(),'tipo':feature.attribute('tipo')})
    #reimplementado para PM
    def addItemToList(self, feature, tipo):
        self.scope.setFeature(feature)
        value = self.displayExpression.evaluate(self.context)
        element = QListWidgetItem(str(value) + '\t- ' + str(tipo).upper())
        element.setData(Qt.UserRole, {'id':feature.attribute('id'),'tipo':tipo})
        self.lista.addItem(element)
        self.values.append({'id':feature.attribute('id'),'tipo':tipo})

    #reimplementado para PM
    def add(self,item):
        featureN = buscar_feature_por_id(self.layerN, item['id'])
        self.addItemToList(featureN,item['tipo'])
        self.setFormDirty()
    #reimplementado para PM
    def save(self):
        # Ver comentario equivalente en nnConfig.save().
        valor_id = id_real(self.feature)
        print('nnConfig:save | feature id real =', valor_id)

        if valor_id and self.isDirty() and self.layer.isEditable() and isinstance(valor_id, int) and valor_id > 0:
            self.layerNN.startEditing()
            request = self.relation1N.getRelatedFeaturesRequest(self.feature)
            fids = [f.id() for f in self.layerNN.getFeatures(request)]
            # print(fids)
            self.layerNN.dataProvider().deleteFeatures(fids)

            attr_id_1N = self.relation1N.referencingFields()[0]
            attr_id_N1 = self.relationN1.referencingFields()[0]
            features = []
            print('values',self.values)
            for value in self.values:
                feat = QgsFeature(self.layerNN.fields())
                feat.setAttribute(attr_id_1N, valor_id)
                feat.setAttribute(attr_id_N1, value['id'])
                feat.setAttribute('tipo', value['tipo'])
                feat.setAttribute('id', None)
                features.append(feat)

            self.layerNN.dataProvider().addFeatures(features)

class nnConfigInspector(nnConfig):

    def __init__(self, dialog: QgsAttributeForm, layer: QgsVectorLayer, feature: QgsFeature, form,  configNN: dict):
        print('init')
        super().__init__(dialog, layer, feature, form,  configNN)

class nnConfigEjecutor(nnConfig):

    def __init__(self, dialog: QgsAttributeForm, layer: QgsVectorLayer, feature: QgsFeature, form,  configNN: dict):
        print('init')
        super().__init__(dialog, layer, feature, form,  configNN)





'''
nuevo Feature:
parent <PyQt5.QtWidgets.QDialog object at 0x7f9d0626faf8>
parent2 <qgis._gui.QgsMapCanvas object at 0x7f9d84c49d38>

identify:
parent: <PyQt5.QtWidgets.QDialog object at 0x7f9d0625c948>
parent2 <PyQt5.QtWidgets.QDialog object at 0x7f9d0625c798>

multiedit:
parent <PyQt5.QtWidgets.QDialog object at 0x7f9d0625cb88>
parent2 <PyQt5.QtWidgets.QMainWindow object at 0x7f9d0625c4c8>

search:
parent <PyQt5.QtWidgets.QDialog object at 0x7f9d2c496678>
parent2 <PyQt5.QtWidgets.QMainWindow object at 0x7f9d2c496288>


Tabla:
parent None // la primera vez que se abre, no se para que
    //el form propiamente dicho
parent <PyQt5.QtWidgets.QWidget object at 0x7f884268c9d8>
parent2 <PyQt5.QtWidgets.QScrollArea object at 0x7f884268c0d8>

'''

class nnForm:
    '''Class to handle forms to type data'''
    def __init__(self, dialog: QgsAttributeForm, layer, feature, config):
        # print ('parent', dialog.parent())
        # print ('parent2', dialog.parent().parent())
        # return

        self.dialog = dialog
        self.layer = layer
        self.feature = feature
        self.config = config
        self.nullValue = QSettings().value("qgis/nullValue" , u"NULL")
        self.nnConfigs:dict = {}
        
        # print('mode:',dir(dialog))
        
        # print(self.nnConfigs)
        tipo = ''
        if dialog.parent() is not None:
            if isinstance(dialog.parent().parent(),QDialog):
                print('identify')
                tipo = 'identify'
            elif isinstance(dialog.parent().parent(),QgsMapCanvas):
                print('nuevo Feature')
                tipo = 'nuevo'
            elif isinstance(dialog.parent().parent(),QScrollArea):
                print('tabla')
                tipo = 'tabla'
            elif isinstance(dialog.parent().parent(),QMainWindow):
                tipo = 'multi'
                print('search o multiedit')

        if tipo != 'multi': #conectamos todo solo si no es un form de search o multiedit
            if tipo != 'identify': #si no es un identify
                try:
                    self.dialog.featureSaved.disconnect()
                except:
                    pass
            self.dialog.featureSaved.connect(partial(self.saveNN))
            
            for conf in self.config['nn']:
                # print(conf)
                if conf['tabla_final'] == 'plano_mensura':
                    clase = nnConfigPM
                elif conf['tabla_final'] == 'inspector':
                    clase = nnConfigInspector
                elif conf['tabla_final'] == 'ejecutor':
                    clase = nnConfigEjecutor
                
                print('clase',clase)


                self.nnConfigs[conf['tabla_final']] = clase(dialog, layer, feature, self, conf)
                # print(self.nnConfigs[conf['tabla_final']])
                self.nnConfigs[conf['tabla_final']].populateList()
        # return

    def saveNN(self):
        if self.feature.id():
            print('saveNN self.feature.id()' ,self.feature.id())
            conf: nnConfig = None
            for name, conf in self.nnConfigs.items():
                # print('for conf in self.nnConfigs: ',name, conf)
                if conf.isDirty():
                    # print('conf.isDirty():')
                    conf.save()

    
    def openNN(self, configNN: nnConfig):
        # print('openNN')
        if isinstance(configNN,nnConfigInspector):
            print('INNNNNNNNNNSSSSSSSPPPPPPEEEEEEE')
            clase = nnDialogInspector
        elif isinstance(configNN,nnConfigPM):
            print('PPPPPPPPPPPMMMMMMMMMMMMMMMMMMM')
            clase = nnDialogPM
        elif isinstance(configNN,nnConfigEjecutor):
            print('PPPPPPPPPPPMMMMMMMMMMMMMMMMMMM')
            clase = nnDialogEjecutor

        dialog = clase(self.dialog, configNN.layerN, configNN.displayExpression,False)
        
        # dialog.show()
        if dialog.exec_():
            # Get the results:
            item = dialog.getSelected()
            # print(thevalues, dialog)
            configNN.add(item)


