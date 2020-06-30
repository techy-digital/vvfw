# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic


class VVFramework(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)
        self.buttons = [self.EvaEnvPB, self.EvaTypePB, self.TypeCompPB, self.EvaToolPB, self.EvaStagePB, self.LogicPB]
        self.trees = [self.EvaEnvTW, self.EvaTypeTW, self.TypeCompTW, self.EvaToolTW, self.EvaStageTW, self.LogicTW]
        self.labels = [self.Dim1SelectedLabel, self.Dim2SelectedLabel, self.Dim3SelectedLabel, self.Dim4SelectedLabel, self.Dim5SelectedLabel, self.Dim6SelectedLabel]
        self.GenerateXMLPB.hide()
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

    def make_callback_selected(self, obj, dim):
        def callback():
            labelObj = self.labels[dim]
            if labelObj.isHidden():
                labelObj.show()
            getSelected = obj.selectedItems()[0]
            selectedStr = getSelected.data(0,0)
            labelObj.setText("Dimension-"+str(dim)+" :\n"+selectedStr)
            self.isAllSelected()
        return callback

    def make_callback_button(self, obj):
        def callback():
            if obj.isHidden():
                obj.show()
            else:
                obj.hide()
        return callback

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = VVFramework()
    window.show()
    sys.exit(app.exec_())
