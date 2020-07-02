# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from lxml import etree

Dimensions = {0: "Evaluation Environment",
              1: "Evaluation Type",
              2: "Type of Component under Evaluation",
              3: "Evaluation Tool",
              4: "Evaluation Stage",
              5: "Logic of the Component"}

class FrameworkXML():
    def __init__(self, dimDict, filename):
        self.root = etree.Element("VVFramework")
        for i in range(6):
            child = etree.SubElement(self.root, Dimensions[i].replace(" ",""), dimension=str(i+1))
            layer = etree.SubElement(child, "Layer")
            dimItem = dimDict[i]
            if isinstance(dimItem, str):
                layer.text = dimDict[i]
            else:
                a, b = dimDict[i]
                sublayer = etree.SubElement(layer, "SubLayer")
                layer.text = b
                sublayer.text = a
        print(etree.tostring(self.root, pretty_print=True,encoding='unicode'))
        tree = etree.ElementTree(self.root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

class VVFramework(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)
        self.buttons = [self.EvaEnvPB, self.EvaTypePB, self.TypeCompPB, self.EvaToolPB, self.EvaStagePB, self.LogicPB]
        self.trees = [self.EvaEnvTW, self.EvaTypeTW, self.TypeCompTW, self.EvaToolTW, self.EvaStageTW, self.LogicTW]
        self.labels = [self.Dim1SelectedLabel, self.Dim2SelectedLabel, self.Dim3SelectedLabel, self.Dim4SelectedLabel, self.Dim5SelectedLabel, self.Dim6SelectedLabel]
        self.SelectedLayers = {0:"", 1:"", 2:"", 3:"", 4:"",5:"", 6:""}
        self.GenerateXMLPB.hide()
        self.FileNameTE.hide()
        self.GenerateXMLPB.clicked.connect(self.xml_generate_callback)
        for obj in self.labels:
            obj.hide()
        for obj in self.trees:
            obj.hide()
        for button, tree in zip(self.buttons, self.trees):
            button.clicked.connect(self.make_callback_button(tree))
        for i, tree in enumerate(self.trees):
            tree.itemSelectionChanged.connect(self.make_callback_selected(tree, i))

    def isAllSelected(self):
        ret = True
        for tree in self.trees:
            idx = tree.selectedIndexes()
            ret = False if len(idx) == 0 else True
        if ret:
            self.GenerateXMLPB.show()
            self.FileNameTE.show()

    def make_callback_selected(self, obj, dim):
        def callback():
            labelObj = self.labels[dim]
            if labelObj.isHidden():
                labelObj.show()
            SelectedObj = obj.selectedItems()[0]
            selectedStr = SelectedObj.data(0,0)
            parentLayer = ''
            if isinstance(SelectedObj.parent(), QtWidgets.QTreeWidgetItem):
                parentLayer = SelectedObj.parent().data(0,0)
                self.SelectedLayers[dim] = (selectedStr, parentLayer)
            else:    
                self.SelectedLayers[dim] = selectedStr
            if not parentLayer:
                labelObj.setText("Dimension-"+str(dim)+" :\n"+selectedStr)
            else:
                labelObj.setText("Dimension-"+str(dim)+" :\n"+parentLayer+"\n"+selectedStr)
            self.isAllSelected()
        return callback

    def make_callback_button(self, obj):
        def callback():
            if obj.isHidden():
                obj.show()
            else:
                obj.hide()
        return callback
    
    def xml_generate_callback(self):
        mFW = FrameworkXML(self.SelectedLayers, filename=self.FileNameTE.toPlainText())

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = VVFramework()
    window.show()
    sys.exit(app.exec_())
