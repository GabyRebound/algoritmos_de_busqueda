#!/usr/bin/python3
# coding: utf-8

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5.QtCore import pyqtSlot
import  sys

from controller.helpersVectProb import generateMatrixGeneral, generateMatrixVectorial, calculateSim, readDict, readWordEmpty, readQueryDefault, convertMatrizGeneralFrecu

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'METODO PROBABILISTICO'
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

        self.labelSim = QLabel('')


        self.dict = readDict('data/dict')
        self.dict['Q'] = readQueryDefault('data/queryDefaultVectProb')
        self.words_empty = readWordEmpty('data/words_empty')

        self.matrixGeneral = generateMatrixGeneral(self.dict, self.words_empty)
        self.matrixVectorial = generateMatrixVectorial(self.matrixGeneral)
        self.simility = calculateSim(self.matrixVectorial)

        self.setWindowTitle(self.title)

        # Add box layout, add table to box layout and add box layout to widget
        self.grid = QGridLayout()
        self.grid.setSpacing(15)
        a = QLabel('')
        self.grid.addWidget(a, 0, 0)
        self.grid.addWidget(a, 0, 1)
        title = QLabel('METODO PROBABILISTICO')
        self.grid.addWidget(title, 0, 2)
        self.grid.addWidget(a, 0, 3)
        self.grid.addWidget(a, 0, 4)

        self.c = 2
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
        self.grid.addWidget(self.line, self.c, 0, 1, 3)

        button = QPushButton('Calcular')
        button.setStyleSheet(stl)
        button.clicked.connect(self.on_click_button( self.initUI, self.changeVariable))

        self.grid.addWidget(button, self.c, 3)

        self.c += 1

        self.initUI()


    # metodo auxiliar que modifica nuestra matriz general, vectorial y similitud, cada vez que hacemos una consulta
    def changeVariable(self, query):
        self.dict['Q'] = query
        self.matrixGeneral = generateMatrixGeneral(self.dict, self.words_empty)
        self.matrixVectorial = generateMatrixVectorial(self.matrixGeneral)
        self.simility = calculateSim(self.matrixVectorial)

    # metodo que diguba toda la  interfaz grafica
    def initUI(self):

        self.createTable()
        # Show widget
        self.grid.addWidget(self.tableWidget, self.c,0, self.c , 4)


        auxSimility = ""
        for key, value in self.simility.items():
            auxSimility += key + ':' + str(value) + "\n"

        self.labelSim.setText(auxSimility)

        self.grid.addWidget(self.labelSim, self.c-1, 4, 2, 1)

        self.setLayout(self.grid)

        self.show()

    # metodo que pinta la tabla
    def createTable(self):

        matrixGeneral = convertMatrizGeneralFrecu(self.matrixGeneral)
        # create table's head
        print(matrixGeneral)
        head = []
        head.append('termino')
        for value in matrixGeneral.values():
            for key in value.keys():
                if key == 'Q':
                    head.append('Q=peso de la consulta')
                else:
                    head.append(f'{key}/peso binario')
            break
        head.append('Frecuencia')

        # create table's body
        body = {}
        for key, value in matrixGeneral.items():
            body[key] = []
            body[key].append(key)

            sum = 0
            for key2, value2 in value.items():
                if key2 == 'Q':
                    body[key].append("{0:.4f}".format(self.matrixVectorial[key][key2]))

                else:
                    sum += value2
                    #valor = 1 if value2 >= 1 else 0
                    #body[key].append(valor)
                    body[key].append(value2)
            body[key].append(sum)

        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(body))
        self.tableWidget.setColumnCount(len(head))
        self.tableWidget.setHorizontalHeaderLabels(head)
        self.tableWidget.setVerticalHeaderLabels(map(str, range(len(body.keys()))))
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
            cont += 1

        self.tableWidget.move(100, 100)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    # evento de los campos de la tabla
    @pyqtSlot()
    def on_click(self):
        pass

        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    # evento para cada button de la interfaz
    @pyqtSlot()
    def on_click_button(self, initUI, changeVariable):

        def click_button():
            changeVariable(self.line.text())
            initUI()

        return click_button

# metodo main
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())