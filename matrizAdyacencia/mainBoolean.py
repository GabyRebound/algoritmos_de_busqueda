#!/usr/bin/python3
# coding: utf-8

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QLabel, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSlot
from controller.helpersBoolean import MATRIZ, recursividad
from controller.helpersVectProb import readQueryDefault, convertMatrizGeneralBinaria

class App(QWidget):

    def __init__(self):
        super().__init__()
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

        self.title = 'METODO BOOLEANO'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 700
        self.matriz = convertMatrizGeneralBinaria(MATRIZ)
        self.initUI()

    # metodo que dibuja toda la  interfaz grafica
    def initUI(self ):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createTable(self.matriz)

        # Add box layout, add table to box layout and add box layout to widget

        self.grid = QGridLayout()
        self.grid.setSpacing(15)
        a = QLabel('                                                 ')

        self.grid.addWidget(a, 0, 0)
        self.grid.addWidget(a, 0, 1)
        title = QLabel('METODO BOOLEANO')
        self.grid.addWidget(title, 0, 2)
        self.grid.addWidget(a, 0, 3)
        self.grid.addWidget(a, 0, 4)

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
        query = readQueryDefault('data/queryDefaultBoolean')
        self.line = QLineEdit(query)
        self.grid.addWidget(self.line, c, 0, 1, 3)
        button = QPushButton('Calcular')
        button.setStyleSheet(stl)
        button.clicked.connect(self.on_click_button)
        self.grid.addWidget(button, c, 3)
        c += 1


        self.grid.addWidget(self.tableWidget, c, 0, c , 4)
        self.mensaje = QLabel('')
        self.grid.addWidget(self.mensaje, 4, 4)

        self.setLayout(self.grid)
        self.show()

    # metodo que pinta las tablas
    def createTable(self, matriz):

        # create table's head
        head = []
        for value in matriz.values():
            for key in value.keys():
                head.append(key)
            break

        # create table's body
        body = {}
        for key, value in matriz.items():
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

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    # evento de los campos de la tabla
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    # evento para cada button de la interfaz
    @pyqtSlot()
    def on_click_button(self):
        try:
            message = self.line.text()
            query = recursividad(message.split(' '))
            cad = ''
            for k,v in query.items():
                if v==1:
                    cad += k+', '
            self.mensaje.setText(cad)
        except Exception:
            self.mensaje.setText("no hay coincidencia")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())