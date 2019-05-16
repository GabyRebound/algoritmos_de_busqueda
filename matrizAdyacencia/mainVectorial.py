#!/usr/bin/python3
# coding: utf-8

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5.QtCore import pyqtSlot
import  sys

from controller.helpersVectProb import generateMatrixGeneral, generateMatrixVectorial, calculateSim, readDict, readQueryDefault, readWordEmpty, convertMatrizGeneralFrecu

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'METODO VECTORIAL'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 700

        css = """
        QWidget{
            Background: #AA00AA;
            color:white;
            font:12px bold;
            font-weight:bold;
            border-radius: 1px;
            height: 11px;
        }
        QDialog{
            Background-image:url('img/titlebar bg.png');
            font-size:12px;
            color: black;

        }
        QToolButton{
            Background:#AA00AA;
            font-size:11px;
        }
        QToolButton:hover{
            Background: #FF00FF;
            font-size:11px;
        }
        """

    
        self.setStyleSheet(css)

        self.dict = readDict('data/dict')
        self.dict['Q'] = readQueryDefault('data/queryDefaultVectProb')
        self.words_empty = readWordEmpty('data/words_empty')

        self.matrixGeneral = generateMatrixGeneral(self.dict, self.words_empty)
        self.matrixVectorial = generateMatrixVectorial(self.matrixGeneral)
        self.simility = calculateSim(self.matrixVectorial)

        self.labelSim = QLabel('')

        # creacion del grid
        self.grid = QGridLayout()
        self.grid.setSpacing(15)


        # cabezera del widget
        a = QLabel('                                                  ')
        self.grid.addWidget(a, 0, 0)
        self.grid.addWidget(a, 0, 1)
        title = QLabel('METODO VECTORIAL')
        self.grid.addWidget(title, 0, 2)
        self.grid.addWidget(a, 0, 3)
        self.grid.addWidget(a, 0, 4)

        # botones de consultas
        c = 3
        stl = """QPushButton {
                        background-color: palegoldenrod;
                        border-width: 2px;
                        border-color: darkkhaki;
                        border-style: solid;
                        border-radius: 5;
                        padding: 3px;
                        min-width: 9ex;
                        min-height: 2.5ex;
                    }"""
        self.line = QLineEdit(self)

        self.line.setText(self.dict['Q'])
        self.grid.addWidget(self.line, c, 0, 1,2)
        # self.grid.addWidget(QLabel(v), c, 0)
        button = QPushButton('Calcular')
        button.setStyleSheet(stl)
        button.clicked.connect(self.on_click_button( self.initUI, self.changeVarible))
        self.grid.addWidget(button, c, 3)
        c += 1


        self.initUI()

    # metodo auxiliar que modifica nuestra matriz general, vectorial y similitud, cada vez que hacemos una consulta
    def changeVarible(self, query):
        self.dict['Q'] = query

        self.matrixGeneral = generateMatrixGeneral(self.dict, self.words_empty)
        self.matrixVectorial = generateMatrixVectorial(self.matrixGeneral)
        self.simility = calculateSim(self.matrixVectorial)

    # metodo que diguba toda la  interfaz grafica
    def initUI(self):

        self.createTable(self.matrixGeneral, self.matrixVectorial, self.simility)

        self.grid.addWidget(self.tableWidget, 4, 0, 3, 4)
        self.grid.addWidget(self.tableWidget2, 9, 0, 3 ,4)

        cadSim = ""
        for key, value in self.simility.items():
            cadSim += str(key)+": "+str(value)+"\n"

        self.labelSim.setText(cadSim)

        self.grid.addWidget(self.labelSim, 4, 4)
        # seteamos el layout del widget
        self.setLayout(self.grid)
        self.show()

    # metodo que pinta las tablas
    def createTable(self, matrixGeneral, matrixVectorial, simility):

        matrixGeneral = convertMatrizGeneralFrecu(matrixGeneral)
        # create table's head
        head = []
        for value in matrixGeneral.values():
            for key in value.keys():
                head.append(key)
            break

        # create table's body
        body = {}
        for key, value in matrixGeneral.items():
            body[key] = []
            for key2, value2 in value.items():
                body[key].append(value2)


        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(body))
        self.tableWidget.setColumnCount(len(head))
        self.tableWidget.setHorizontalHeaderLabels(head)
        self.tableWidget.setVerticalHeaderLabels(body.keys())
        self.tableWidget.setStyleSheet("""*{
                                        background-color: qlineargradient(spreadad, x1:1, y1:0.813, x2:1, y2:0, stop:0 rgba(87, 87, 87, 255), stop:1 rgba(135,135, 135, 255));
                                        border: 2px solid gray;
                                        border-radius: 10px;
                                        padding: 0 8px;
                                        color: rgb(0, 0, 0);
                                        }""")

        # insert body and head to the table
        cont = 0
        for value in body.values():
            for i in range(len(value)):
                self.tableWidget.setItem(cont, i, QTableWidgetItem(str(value[i])))
            cont +=1

        self.tableWidget.move(100, 100)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

        # ================================================
        # create table's head
        head = []
        for value in matrixVectorial.values():
            for key in value.keys():
                head.append(key)
            break

        # create table's body
        body = {}
        for key, value in matrixVectorial.items():
            body[key] = []
            for key2, value2 in value.items():
                body[key].append("{0:.4f}".format(value2))

        # Create table
        self.tableWidget2 = QTableWidget()
        self.tableWidget2.setRowCount(len(body))
        self.tableWidget2.setColumnCount(len(head))
        self.tableWidget2.setHorizontalHeaderLabels(head)
        self.tableWidget2.setVerticalHeaderLabels(body.keys())

        self.tableWidget2.setStyleSheet("""*{
                                            background-color: qlineargradient(spreadad, x1:1, y1:0.813, x2:1, y2:0, stop:0 rgba(87, 87, 87, 255), stop:1 rgba(135,135, 135, 255));
                                            border: 2px solid gray;
                                            border-radius: 10px;
                                            padding: 0 8px;
                                            color: rgb(0, 0, 0);
                                            }""")
        # insert body and head to the table
        cont = 0
        for value in body.values():
            for i in range(len(value)):
                self.tableWidget2.setItem(cont, i, QTableWidgetItem(str(value[i])))
            cont += 1

        self.tableWidget2.move(400, 400)

        # table selection change
        self.tableWidget2.doubleClicked.connect(self.on_click)

    # evento de los campos de la tabla
    @pyqtSlot()
    def on_click_button(self,  initUI, changeVariable):

        def click_button():
            changeVariable(self.line.text())
            initUI()
        return click_button

    # evento para cada button de la interfaz
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text(), )


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())