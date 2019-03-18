from PyQt4.QtCore import *

from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
import carto
# Import the code for the dialog
from save_attributes_dialog import SaveAttributesDialog
import os.path
import pkg_resources
#from qgis.core import *
import qgis.utils
import os
from qgis.core import *




class SaveAttributes:
    """QGIS Plugin Implementation."""
    
    

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SaveAttributes_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = SaveAttributesDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Save Attributes')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SaveAttributes')
        self.toolbar.setObjectName(u'SaveAttributes')
        
     #############################################################  
       
        self.dlg.tester.clicked.connect(self.symbologie)    
      ############################################################ 
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SaveAttributes', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
     
     

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/SaveAttributes/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Save Attributes as CSV'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Save Attributes'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
 
    
    
    
    
    def run(self):
       """Run method that performs all the real work""" 
       self.dlg.show()
       layers = self.iface.legendInterface().layers()
       layer_list = ['']      
       for layer in layers:
           layer_list.append(layer.name())                  
       self.dlg.comboBox.clear()
       self.dlg.comboBox.addItems(layer_list) 
       self.dlg.comboBox.currentIndexChanged.connect(self.attribut_value)  
       self.dlg.combow_color.currentIndexChanged.connect(self.textEdit_color)
       
       
       self.symbologie_value()
       
       #style     
       self.symbologie_color() 
       
       self.dlg.color_symb.setStyleSheet("background-color: '#FFF';")
       self.dlg.comboBox.setStyleSheet("background-color: '#DFE6EB';")
      
       
    
       
       
    #liste des attrubut par couche
    def field_layer(self):
       attr_list = [''] 
       layers = self.iface.legendInterface().layers()
       for layer in layers:
            fields = layer.pendingFields()
            field_names = [field.name() for field in fields]            
            attr_list.append(field_names)               
       return attr_list
   
    
    #type des attribut
    def attr_type(self):
        attr_types = ['']
        layers = self.iface.legendInterface().layers()
        for layer in layers:
            fields = layer.pendingFields()
            type_field = [field.typeName() for field in fields]            
            attr_types.append(type_field)       
        return attr_types
    
    #liste valeur attribut    
    def field_value_array(self):
        attr = []
        layers = self.iface.legendInterface().layers()
        if self.dlg.comboBox.currentText() != '':
            index_combow = self.layer_list().index(self.dlg.comboBox.currentText())
            att_selected = self.dlg.attribut.currentText()
            field_array = ['']        
            feature = layers[index_combow-1]
            for feat in feature.getFeatures():
                attr.append(feat.attribute(att_selected))
        else:
            self.dlg.comboBox.setStyleSheet("background-color: '#BABABA';")
        return attr       
    #coordonate 
    def coordonate_suiv(self,var):
        layers = self.iface.legendInterface().layers()
        vars = []
        if self.dlg.comboBox.currentText() != '':
            index_combow = self.layer_list().index(self.dlg.comboBox.currentText())
            feature = layers[index_combow-1]
            for feat in feature.getFeatures():
                vars.append(feat.attribute(var))
        return vars        
                
            
    #liste des couche
    def layer_list (self):
        layers = self.iface.legendInterface().layers()
        layer_list = ['']      
        for layer in layers:
               layer_list.append(layer.name())  
        #print(layer_list)                       
        return layer_list 
    #types des couche
    def layer_type(self):
        layers = self.iface.legendInterface().layers()
        layer_type = ['']
        for layer in layers:
               layer_type.append(layer.wkbType())                         
        return layer_type 
    
    #liste des attribut qui correspond au couche selectionner       
    def attribut_value(self):
        self.dlg.comboBox.setStyleSheet("background-color: '#DFE6EB';")        
        index_combow = self.layer_list().index(self.dlg.comboBox.currentText())
        self.dlg.attribut.clear()
        self.dlg.attribut.addItems(self.field_layer()[index_combow]) 
             
    #symbologie
    def symbologie(self):
        layers = self.iface.legendInterface().layers()
        #for layer in layers:
         #   if layer.type() == QgsMapLayer.VectorLayer:
          #      print ("")
        index_combow = self.layer_list().index(self.dlg.comboBox.currentText())
       
        index_combow = index_combow
        
        att_selected = self.dlg.attribut.currentText()
        attributs = self.field_layer()[index_combow]
        lst_attr_type = self.attr_type()[index_combow]
        lst_attr_name_index = self.field_layer()[index_combow].index(att_selected) 
        attr_type = lst_attr_type[lst_attr_name_index] 
        if attr_type == "integer" or attr_type == "double" or attr_type == "real":
            attr_value_tri = self.tri_insertion(self.field_value_array())
            class4 = (max(attr_value_tri) - min(attr_value_tri))/4
                     
            #print(class4) 
            
                
        print(self.coordonate_suiv('y')) 
          
        #print(attributs)
        
    def symbologie_color(self):
        colors = [u'bleu',u'maron',u'vert',u'jaune',u'rouge'] 
        self.dlg.combow_color.clear()
        self.dlg.combow_color.addItems(colors)
    
    def symbologie_value(self):
        val_symb = [u'categoriser',u'graduer']
        self.dlg.symbole_combow.clear()
        self.dlg.symbole_combow.addItems(val_symb)    

    def textEdit_color(self):
        colors = [u'bleu',u'maron',u'vert',u'jaune',u'rouge']
        colors_= [u'#0000FF',u'#A52A2A',u'#006400',u'#FFD700',u'#FF0000']
        index_color = colors.index(self.dlg.combow_color.currentText()) 
        self.dlg.color_symb.setStyleSheet("background-color:"+colors_[index_color]+";")
        return colors_[index_color]
        
    #triage d'un tableau 
    def tri_insertion(self,B):
        A = list(B) 
        N = len(A)
        for i in range(1,N):
            cle = A[i]
            j = i-1
            while j>=0 and A[j] > cle:
                A[j+1] = A[j] 
                j = j-1
            A[j+1] = cle
        return A
        
    
    def generate_carte(self):
        a = 1
        myLabel = self.dlg.attribut.currentText() 
        layers = self.iface.legendInterface().layers()
        layer_list = ['']
        classe = 4      
        
        myRangeList = []
        
        
        
        
        index_combow = self.layer_list().index(self.dlg.comboBox.currentText())
       
        index_combow = index_combow
        
        att_selected = self.dlg.attribut.currentText()
        attributs = self.field_layer()[index_combow]
        lst_attr_type = self.attr_type()[index_combow]
        lst_attr_name_index = self.field_layer()[index_combow].index(att_selected) 
        attr_type = lst_attr_type[lst_attr_name_index] 
        if attr_type == "integer" or attr_type == "double" or attr_type == "real":
            attr_value_tri = self.tri_insertion(self.field_value_array())
            class4 = (max(attr_value_tri) - min(attr_value_tri))/4
            
        for layer in layers:       
            if layer.wkbType()==QGis.WKBPolygon:
                #print(layer.name()+" ok") 
                layer_list.append(layer.name())     
                layer.rendererV2().symbol().setColor(QColor(self.textEdit_color()))                                    
                #self.mapCanvas().refresh()      
            if layer.wkbType()==QGis.WKBPoint:
                if a==2:                   
                                     
                    symbol = QgsMarkerSymbolV2.createSimple({'size': '4','name': 'circle'})                                         
                    colorRamp = QgsVectorGradientColorRampV2.create({'color1':'255,0,0,255', 'color2':'0,0,255,255','stops':'0.25;255,255,0,255:0.50;0,255,0,255:0.75;0,255,255,255'})
                    renderer = QgsGraduatedSymbolRendererV2.legendSymbologyItems(layer,myLabel,classe,QgsGraduatedSymbolRendererV2.Jenks,symbol,colorRamp)
                    layer.setRendererV2(renderer)
                else:
                    
                    y_ = self.coordonate_suiv('y')
                    x_ = self.coordonate_suiv('x')
                    #atao anaty tableau, QGsPoint(x,y) ; 
                    my_classes = {1: ('yellow', 'First',2),
                                  2: ('yellow', 'Second',3),
                                  3: ('yellow', 'Third',4),
                                  4: ('yellow', 'Fourth',5)}
                    categories = []
                    
                    for class_value, (symbol_property, label_text,size) in my_classes.items():
                        
                        symbol = QgsMarkerSymbolV2.createSimple({'name': 'circle'})          
                        symbol.setColor(QColor(symbol_property))
                        symbol.setSize(size)                    
                        # create a category with these properties
                        category = QgsRendererCategoryV2(class_value, symbol, label_text)                    
                        categories.append(category)
                        
                    field = myLabel
                    renderer = QgsCategorizedSymbolRendererV2(field,categories)                                              
                    layer.setRendererV2(renderer)
                    
                    
                    
                                   
                        
                    #symbol = QgsMarkerSymbolV2.createSimple({'name': 'square', 'color': 'red','size' : '4'})
                    #layer.rendererV2().setSymbol(symbol)
                    
                                                            
                    
                    
                                        
        layer.triggerRepaint()
        self.iface.mapCanvas().refresh()
        self.iface.legendInterface().refreshLayerSymbology(layer)
       
 
   
         