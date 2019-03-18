#from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
#from PyQt4.QtGui import QAction, QIcon, QFileDialog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from save_attributes_dialog import SaveAttributesDialog



class Carto:
    
  def __init__():
        pass

  def select_option(self):
      for i in layer.getFeatures():
          l = []
          l.append(i.attributes())
          print(l)    