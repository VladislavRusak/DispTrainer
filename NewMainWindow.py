import sys
import os
import PyQt5
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as md
import datetime as dt
# import time


from ClassThread import ReportsThread, ReportThread
from ContentManagement import *

# globals
METEO = []

"""     
        ДЛЯ УДОБНОЙ НАВИГАЦИИ, КОД РАЗБИТ НА БЛОКИ ОБОЗНАЧЕНЫЕ КОММЕНАТРИЯМИ
        
        # ГЛАВНОЕ ОКНО ( НАСТРОЙКИ ГЛАВНОГО ОКНА ПРИРЛОЖЕНИЯ)
        # КЛАССЫ НАВИГАЦИОННЫХ ОКОН ( ОКНА ВЫЗЫВАЕМЫЕ ИЗ ГЛАВНОГО ОКНА )
        # КЛАССЫ ИСПОЛНЯЕМЫХ ОКОН ( ОКНА СОДЕРЖАЩИЕ ДАННЫЕ ВЫЗЫВАЕМЫЕ ИЗ БД )
        # КЛАССЫ ВСПОМОГАЛТЕЛЬНЫХ ФУНКЦИЙ ОКОН ( ДОБАВИТЬ, УДАЛИТЬ, ИЗМЕНИТЬ ЗАПИСИ)

"""


#########################################################
#                                                       #
#                                                       #
#                                                       #
#                    ГЛАВНОЕ ОКНО                       #
#                                                       #
#                                                       #
#                                                       #
#########################################################


class MainWindow(QWidget):
    mainWinSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Логистика")
        self.setMainUi()
        self.setGeometry(300, 300, 300, 350)    # left/top/width/height
        self.parent = parent

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('(не работает)РТК')
        b2 = QPushButton('Инфраструктура')
        b3 = QPushButton('Оборудование')
        b4 = QPushButton('Рабочие')
        b5 = QPushButton('Т/С')
        b6 = QPushButton('Грузы')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        self.layout.addWidget(b3)
        self.layout.addWidget(b4)
        self.layout.addWidget(b5)
        self.layout.addWidget(b6)
        # b1.released.connect(self.openTechnologyCard)
        b2.released.connect(self.openInfrastructureWindow)
        b3.released.connect(self.openEquipment)
        b4.released.connect(self.openWorkers)
        b5.released.connect(self.openVehicle)
        b6.released.connect(self.openCargo)

    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)

    # def openTechnologyCard(self):
    #     self.techF = TechnologyCardForm()
    #     self.techF.show()

    def openInfrastructureWindow(self):
        self.structF = InfrastructureWindow()
        self.structF.show()
        self.hide()


    def openEquipment(self):
        self.equipF = EquipmentWindow()
        self.equipF.show()
        self.hide()

    def openWorkers(self):
        self.workF = WorkersWindow()
        self.workF.show()
        self.hide()

    def openVehicle(self):
        self.vehicleF = VehicleWindow()
        self.vehicleF.show()
        self.hide()

    def openCargo(self):
        self.cargoF = CargoWindow()
        self.cargoF.show()
        self.hide()


#########################################################
#                                                       #
#                                                       #
#                                                       #
#               КЛАССЫ НАВИГАЦИОННЫХ ОКОН               #
#                                                       #
#                                                       #
#                                                       #
#########################################################


# ртк класс


class InfrastructureWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, window=None):
        super().__init__()
        self.setWindowTitle('Инфраструктура')
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)
        self.window = window

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton(' Причалы ')
        b2 = QPushButton(' Склады ')
        b3 = QPushButton(' Ж/Д пути(краш) ')
        back = QPushButton(' << Назад ')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        self.layout.addWidget(b3)
        self.layout.addWidget(back)
        b1.released.connect(self.openDocCharManagementForm)
        b2.released.connect(self.openStorageCapManagmentForm)
        b3.released.connect(self.openRailwaysForm)
        back.released.connect(self.GoBack)

    def openDocCharManagementForm(self):
        self.docF = DocCharManagementForm()
        self.docF.show()

    def openStorageCapManagmentForm(self):
        self.storageF = StorageDefaultValuesForm()
        # self.storageF = StorageCapManagementForm()
        self.storageF.show()

    def openRailwaysForm(self):
        self.trainF = RailwaysForm()
        self.trainF.show()

    def GoBack(self):
        self.Back = MainWindow()
        self.hide()
        self.Back.show()



class EquipmentWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, window=None):
        super().__init__()
        self.setWindowTitle("Оборудование")
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)
        self.window = window

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('Краны')
        b2 = QPushButton('Вспом.Техника')
        back = QPushButton(' << Назад ')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        self.layout.addWidget(back)
        b1.released.connect(self.openCransForm)
        b2.released.connect(self.openOtherEquipForm)
        back.released.connect(self.GoBack)

    def openCransForm(self):
        self.cransF = CranManagementForm()
        self.cransF.show()

    def openOtherEquipForm(self):
        self.equipF = OtherEquipmentForm()
        self.equipF.show()

    def GoBack(self):
        self.Back = MainWindow()
        self.hide()
        self.Back.show()


class WorkersWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, window=None):
        super().__init__()
        self.setWindowTitle('Работники')
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)
        self.window = window

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('Квалификации')
        b2 = QPushButton('Работники')
        back = QPushButton(' << Назад ')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        self.layout.addWidget(back)
        b1.released.connect(self.openQualificationsForm)
        b2.released.connect(self.openWorkersForm)
        back.released.connect(self.GoBack)

    def openQualificationsForm(self):
        self.qualificationF = WorkSkillForm()
        self.qualificationF.show()

    def openWorkersForm(self):
        self.workersF = WorkersForm()
        self.workersF.show()

    def GoBack(self):
        self.Back = MainWindow()
        self.hide()
        self.Back.show()

class VehicleWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, window=None):
        super().__init__()
        self.setWindowTitle('Транспорт')
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)
        self.window = window

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('Суда')
        b2 = QPushButton('ЖД составы')
        back = QPushButton(' << Назад ')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        self.layout.addWidget(back)
        b1.released.connect(self.openShipsForm)
        b2.released.connect(self.openTrainsForm)
        back.released.connect(self.GoBack)

    def openShipsForm(self):
        self.shipsF = ShipsForm()
        self.shipsF.show()

    def openTrainsForm(self):
        self.trainsF = TrainsForm()
        self.trainsF.show()

    def GoBack(self):
        self.Back = MainWindow()
        self.hide()
        self.Back.show()


class CargoWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, window=None):
        super().__init__()
        self.setWindowTitle('Грузы')
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)
        self.window = window

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('Грузовая партия')
        b2 = QPushButton('Типы грузов')
        b3 = QPushButton('Способы хранения')
        back = QPushButton(' << Назад ')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        self.layout.addWidget(b3)
        self.layout.addWidget(back)
        b1.released.connect(self.openCargoParty)
        b2.released.connect(self.openCargoType)
        b3.released.connect(self.openStorageMethods)
        back.released.connect(self.GoBack)

    def openCargoParty(self):
        self.partyF = CargoPartyWindow()
        self.partyF.show()
        self.hide()

    def openCargoType(self):
        self.type = CargoTypeForm()
        self.type.show()

    def openStorageMethods(self):
        self.methodF = StorageMethodsForm()
        self.methodF.show()

    def GoBack(self):
        self.Back = MainWindow()
        self.hide()
        self.Back.show()

class CargoPartyWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, window=None):
        super().__init__()
        self.setWindowTitle('Грузовая партия')
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)
        self.window = window

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('Партия')
        b2 = QPushButton('Экспедиторы')
        back = QPushButton(' << Назад ')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        self.layout.addWidget(back)
        b1.released.connect(self.openParty)
        b2.released.connect(self.openExpeditorsForm)
        back.released.connect(self.GoBack)

    def openParty(self):
       self.type = PartyForm()
       self.type.show()

    def openExpeditorsForm(self):
       self.expeditorF = ExpeditorManagementForm()
       self.expeditorF.show()

    def GoBack(self):
        self.Back = CargoWindow()
        self.hide()
        self.Back.show()



#########################################################
#                                                       #
#                                                       #
#                                                       #
#               КЛАССЫ ИСПОЛНЯЕМЫХ ОКОН                 #
#                                                       #
#                                                       #
#                                                       #
#########################################################


class DocCharManagementForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Характеристики причалов")
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(6)
        doc_char = DocChar()
        # t.save()
        thead = ["Номер причала", "Длина", "Глубина", "Статус"]
        col_num = 0
        for val in thead:
            self.table.setItem(0, col_num, QTableWidgetItem(str(val)))
            col_num += 1
        self.data = doc_char.getAll()
        row_num = 0
        for i in self.data:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            iter = 0
            for j in i:
                if iter == 0:
                    iter += 1
                    continue

                if iter == 4:
                    if j == "" or j == "null" or j == "0" or j == None:
                        self.table.setItem(row_num, col_num, QTableWidgetItem("Свободен"))
                    else:
                        self.table.setItem(row_num, col_num, QTableWidgetItem("Занят"))
                else:
                    self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                col_num += 1

                iter += 1

            w = QWidget()
            s = str(i[0])
            p = SaveRowButton('Сохранить', w, s, str(row_num), 0)
            p.s.connect(self.saveRow)
            self.table.setCellWidget(row_num, col_num, w)
            col_num += 1
            w = QWidget()
            s = str(i[0])
            p = MyButton('Удалить', w, s)
            p.s.connect(self.delDoc)
            self.table.setCellWidget(row_num, col_num, w)

        self.layout.addWidget(self.table)
        w = QWidget()
        l = QGridLayout()
        w.setLayout(l)
        self.layout.addWidget(w)
        add_b = QPushButton('Добавить значение')
        self.num = QLineEdit()
        self.length = QLineEdit()
        self.depth = QLineEdit()
        l.addWidget(self.num, 1, 0)
        l.addWidget(self.length, 1, 1)
        l.addWidget(self.depth, 1, 2)
        l.addWidget(QLabel('Номер причала'), 0, 0)
        l.addWidget(QLabel('Длина'), 0, 1)
        l.addWidget(QLabel('Глубина'), 0, 2)
        l.addWidget(add_b, 1, 3)
        add_b.released.connect(self.addDocChar)

    def saveRow(self, id, row, param):
        row = int(row)
        doc_char = DocChar()
        doc_row = doc_char.find(id)
        if doc_row != []:
            Doc = DocChar(str(doc_row[0][0]), self.table.item(row, 0).text(), self.table.item(row, 1).text(),
                          self.table.item(row, 2).text(), '')
            Doc.save()
        else:
            self.sup = SupportWindow("Не удалось выбрать", 0)
            self.sup.show()

    def addDocChar(self):
        error = False
        error_text = ""
        num = self.num.text()
        length = self.length.text()
        depth = self.depth.text()
        try:
            num = int(num)
        except Exception:
            error = True
            error_text = error_text + "Поле Номер причала должно быть числовым\n"

        try:
            length = int(length)
        except Exception:
            error = True
            error_text = error_text + "Поле Длина должно быть числовым\n"

        try:
            depth = float(depth)
        except Exception:
            error = True
            error_text = error_text + "Поле Глубина должно быть числовым\n"

        if not error:
            doc_char = DocChar(None, str(num), str(length), str(depth), '')
            doc_char.save()
            qw = QWidget()
            qw.setLayout(self.layout)
            self.setMainUi()
        else:
            QMessageBox.about(self, 'Ошибка!', error_text)

    def delDoc(self, val):
        self.sup = SupportWindow('Удалить причал?', 1)
        self.sup.show()
        self.delete_id = val
        self.sup.signal.connect(self.mk)

    def mk(self, val):
        if val == 1:
            doc_char = DocChar()
            doc_char.delete(self.delete_id)
            qw = QWidget()
            qw.setLayout(self.layout)
            self.setMainUi()


class StorageManagementForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Склады")
        self.resize(400, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        storage = Storage()
        # t.save()
        self.data = storage.getAll()
        row_num = -1
        for i in self.data:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            for j in i:
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                col_num += 1
            w = QWidget()
            s = str(i[0])
            p = MyButton('Удалить', w, s)
            p.s.connect(self.mk)
            # p.s.connect(self.mk)
            # p.released.connect()
            self.table.setCellWidget(row_num, col_num, w)

        self.layout.addWidget(self.table)
        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        self.layout.addWidget(w)
        add_b = QPushButton('Добавить значение')
        self.type = QLineEdit()
        l.addWidget(self.type)
        l.addWidget(add_b)
        add_b.released.connect(self.addStorage)

    def addStorage(self):
        if self.type.text() == '':
            self.sup = SupportWindow("Заполните название", 0)
            self.sup.show()
            return False
        storage = Storage(0, self.type.text())
        storage.save()
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def mk(self, val):
        storage = Storage()
        storage.delete(val)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def closeEvent(self, evt):
        QWidget.closeEvent(self, evt)
        self.signal.emit("1")


class StorageDefaultValuesForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setMainUi()
        self.resize(700, 500)
        self.setWindowTitle('Загруженность складов')

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(4)
        storage = Storage()
        # st_def_val = StorageDefVal()
        thead = ["Название склада", "Обслуживаемый груз (UF)", "Процент загруженности склада", "Вместимость склада (W)",
                 "Добавить экспедитора"]
        col_num = 0
        for val in thead:
            self.table.setItem(0, col_num, QTableWidgetItem(str(val)))
            col_num += 1

        # self.data = st_def_val.getAll()
        self.data = storage.getAll()
        row_num = 0
        for i in self.data:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            self.table.setItem(row_num, 0, QTableWidgetItem(str(i[1])))
            wgt = QWidget()
            l = QGridLayout()
            wgt.setLayout(l)
            exps = storage.getExpeditors(i[0])
            pos = 0
            if exps != []:
                for ex in exps:
                    e = Expeditor()
                    expeditor = e.find(ex[1])
                    cargo = Cargo()
                    c = cargo.find(ex[3])

                    s = str(ex[0])
                    p = MyButton('Удалить', None, s)
                    p.s.connect(self.delExpConfirm)

                    l.addWidget(QLabel(str(expeditor[0][1])), pos, 0)
                    l.addWidget(QLabel(str(c[0][1])), pos, 1)
                    l.addWidget(QLabel(str(ex[4])), pos, 2)
                    l.addWidget(p, pos, 3)

                    pos += 1

            self.table.setCellWidget(row_num, 1, wgt)

            wgt = QWidget()
            l = QGridLayout()
            wgt.setLayout(l)

            total_perc = 0

            st_d_v = StorageDefVal()
            default_values = st_d_v.getBy('storage', '=', str(i[0]))
            pos = 0
            if default_values != []:
                for dv in default_values:
                    cargo = Cargo()
                    c = cargo.find(dv[2])

                    l.addWidget(QLabel(str(c[0][1])), pos, 0)
                    l.addWidget(QLabel(str(dv[4])), pos, 1)

                    pos += 1

                for r in exps:
                    capW = 0
                    for p in default_values:
                        if int(r[3]) == int(p[2]):
                            capW = p[4]

                    v = str(capW)
                    capW = float(v.replace(',', '.'))
                    v = str(r[4])
                    cap = float(v.replace(',', '.'))
                    total_perc = total_perc + (cap * 100 / capW)

            self.table.setItem(row_num, 2, QTableWidgetItem(str(total_perc) + "%"))
            self.table.setCellWidget(row_num, 3, wgt)
            self.table.item(row_num, 0).setFlags(Qt.NoItemFlags)

            w = QWidget()
            s = str(i[0])
            p = MyButton('Добавить экспедитора', w, s)
            p.s.connect(self.addExpeditor)
            self.table.setCellWidget(row_num, 3, w)
            col_num += 1

            # w = QWidget()
            # s = str(i[0])
            # p = MyButton('Удалить', w, s)
            # p.s.connect(self.delConfirm)
            # self.table.setCellWidget(row_num, col_num, w)

        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.layout.addWidget(self.table)
        add_b = QPushButton('Редактировать вместимость складов')
        self.layout.addWidget(add_b)
        add_b.released.connect(self.openStorageDefVal)
        # w = QWidget()
        # l = QHBoxLayout()
        # w.setLayout(l)
        # self.layout.addWidget(w)
        # add_b = QPushButton('Добавить значение')
        # self.storage = QComboBox()
        # storage = Storage()
        # c = storage.getAll()
        # for i in c:
        # self.storage.addItem(i[1], i[0])

        # self.cargo = QComboBox()
        # cargo = Cargo()
        # c = cargo.getAll()
        # for i in c:
        # self.cargo.addItem(i[1], i[0])
        # self.cargo.currentIndexChanged.connect(self.getStorageW)
        # self.capW = QLineEdit()
        # self.capW.setReadOnly(True)
        # self.capUF = QLineEdit()
        # l.addWidget(self.storage)
        # l.addWidget(self.cargo)
        # l.addWidget(self.capW)
        # l.addWidget(self.capUF)
        # l.addWidget(add_b)
        # add_b.released.connect(self.addStorageDefVal)

    def addExpeditor(self, val):
        self.storage_id = val
        add_e_w = QWidget()
        l = QFormLayout()
        add_e_w.setLayout(l)
        add_e_w.exp = QComboBox()
        e = Expeditor()
        ex = e.getAll()
        for i in ex:
            add_e_w.exp.addItem(i[1], i[0])

        l.addRow(QLabel("Экспедитор"), add_e_w.exp)
        add_e_w.cargo = QComboBox()
        cargo = Cargo()
        c = cargo.getAll()
        for i in c:
            add_e_w.cargo.addItem(i[1], i[0])
        add_e_w.cargo.currentIndexChanged.connect(self.changeCargoLeft)
        l.addRow(QLabel("Тип груза"), add_e_w.cargo)
        add_e_w.amount = QLineEdit()
        l.addRow(QLabel("Количество"), add_e_w.amount)
        add_e_w.cargoLeft = QLabel()
        l.addRow(QLabel("Данного типа груза можно добавить еще(т)"), add_e_w.cargoLeft)
        do_add = QPushButton("Добавить")
        do_add.released.connect(self.doAddExpeditorStorage)
        l.addWidget(do_add)

        self.addExpeditorStorageForm = add_e_w
        self.addExpeditorStorageForm.show()
        self.changeCargoLeft()

    def changeCargoLeft(self):
        perc_left = 100 - self.getCapUFPerc(self.storage_id)
        cargo = self.addExpeditorStorageForm.cargo.currentData()
        sdv = StorageDefVal()
        storage_params = sdv.getBy('storage', '=', str(self.storage_id))
        capW = 0
        for p in storage_params:
            if int(cargo) == int(p[2]):
                capW = p[4]

        val = capW * perc_left / 100

        self.addExpeditorStorageForm.cargoLeft.setText(str(val))

    def getCapUFPerc(self, storage_id=None):
        cg = Cargo()
        c = cg.getAll()
        s = Storage()
        sdv = StorageDefVal()
        total_perc = 0
        storage_params = sdv.getBy('storage', '=', str(storage_id))
        exps = s.getExpeditors(storage_id)
        if exps != []:
            for r in exps:
                capW = 0
                for p in storage_params:
                    if int(r[3]) == int(p[2]):
                        capW = p[4]

                v = str(capW)
                capW = float(v.replace(',', '.'))
                v = str(r[4])
                cap = float(v.replace(',', '.'))
                total_perc = total_perc + (cap * 100 / capW)

        return total_perc

    def doAddExpeditorStorage(self):
        cg = Cargo()
        c = cg.getAll()
        s = Storage()
        sdv = StorageDefVal()
        total_perc = 0
        storage_params = sdv.getBy('storage', '=', str(self.storage_id))
        exps = s.getExpeditors(self.storage_id)
        if exps != []:
            for r in exps:
                capW = 0
                for p in storage_params:
                    if int(r[3]) == int(p[2]):
                        capW = p[4]

                v = str(capW)
                capW = float(v.replace(',', '.'))
                v = str(r[4])
                cap = float(v.replace(',', '.'))
                total_perc = total_perc + (cap * 100 / capW)

        for p in storage_params:
            if int(self.addExpeditorStorageForm.cargo.currentData()) == int(p[2]):
                capW = p[4]
        v = str(capW)
        capW = float(v.replace(',', '.'))
        total_perc = total_perc + (float(self.addExpeditorStorageForm.amount.text().replace(',', '.')) * 100 / capW)

        if total_perc >= 100:
            QMessageBox.about(self, 'Ошибка!', 'Склад переполнен, данные не внесены')
            return False

        s.addExpeditor(str(self.storage_id), str(self.addExpeditorStorageForm.exp.currentData()),
                       str(self.addExpeditorStorageForm.cargo.currentData()),
                       str(self.addExpeditorStorageForm.amount.text()))
        self.addExpeditorStorageForm.close()
        q = QWidget()
        q.setLayout(self.layout)
        self.setMainUi()

    def delExpConfirm(self, val):
        self.delete_id = val
        self.sup = SupportWindow("Действительно хотите удалить?", 1)
        self.sup.show()
        self.sup.signal.connect(self.deleteExpDo)

    def deleteExpDo(self):
        s = Storage()
        s.deleteExpeditor(self.delete_id)
        q = QWidget()
        q.setLayout(self.layout)
        self.setMainUi()

    def openStorageDefVal(self):
        self.op = StorageCapManagementForm()
        self.op.show()
        self.close()

    def save_W(self, id, row, col):
        row = int(row)
        sdv = StorageDefVal()
        sdv_row = sdv.find(id)
        value = self.table.item(row, col).text()
        if sdv_row != []:
            StorageDef = StorageDefVal(str(sdv_row[0][0]), str(sdv_row[0][1]), str(sdv_row[0][2]), str(sdv_row[0][3]),
                                       self.table.item(row, x).text())
            StorageDef.save()
        else:
            self.sup = SupportWindow("Не удалось выбрать", 0)
            self.sup.show()

    def delConfirm(self, val):
        self.delete_id = val
        self.sup = SupportWindow("Действительно хотите удалить?", 1)
        self.sup.show()
        self.sup.signal.connect(self.mk)

    def getStorageW(self, index):
        cargo = self.cargo.itemData(self.cargo.currentIndex())
        storage = self.storage.itemData(self.storage.currentIndex())
        st = StorageDefVal()
        row = st.findBy({'storage': str(storage), 'cargo': str(cargo)})
        print(row)

    def addStorageDefVal(self):
        st_def_val = StorageDefVal(0, str(self.storage.itemData(self.storage.currentIndex())),
                                   str(self.cargo.itemData(self.cargo.currentIndex())), self.capW.text(),
                                   self.capUF.text())
        st_def_val.save()
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def mk(self, val):
        if val != 0:
            st_def_val = StorageDefVal()
            st_def_val.delete(self.delete_id)
            qw = QWidget()
            qw.setLayout(self.layout)
            self.setMainUi()


class StorageCapManagementForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Управление складами')
        self.setMainUi()
        self.resize(500, 500)
        self.changed = False

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(5)
        storages = Storage()
        cargos = Cargo()
        types = []
        col_num = 1
        for c in cargos.getAll():
            types.append(c[0])
            self.table.setItem(0, col_num, QTableWidgetItem("Вместимость (" + str(c[1]) + ")"))
            col_num += 1

        row_num = 1
        for r in storages.getAll():
            self.table.setRowCount(row_num + 1)
            self.table.setItem(row_num, 0, QTableWidgetItem(str(r[1])))
            sdv = StorageDefVal()
            capW = sdv.findBy({'storage': str(r[0])})
            if capW != []:
                for capW_r in capW:
                    self.table.setItem(row_num, (int(types.index(capW_r[2])) + 1), QTableWidgetItem(str(capW_r[4])))
                    sdf_id = str(capW_r[0])
            else:
                sdf_id = "new"
            w = QWidget()
            p = SaveRowButton('Сохранить', w, sdf_id, str(r[0]), row_num)
            p.s.connect(self.saveStorageCap)
            self.table.setCellWidget(row_num, col_num, w)
            row_num += 1

        self.types = types
        self.layout.addWidget(self.table)
        self.table.itemChanged.connect(self.valueChanged)

        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        self.layout.addWidget(w)
        add_b = QPushButton('Добавить склад')
        l.addWidget(add_b)
        add_b.released.connect(self.openStorageAddWindow)

        return False

    def saveStorageCap(self, id, storage_id, row):
        for x in range(1, 4):
            if self.table.item(row, x) != None:
                sdv = StorageDefVal()
                sdv_row = sdv.findBy({'storage': str(storage_id), 'cargo': str(self.types[(x - 1)])})
                if sdv_row != []:
                    StorageDef = StorageDefVal(str(sdv_row[0][0]), str(sdv_row[0][1]), str(sdv_row[0][2]),
                                               str(sdv_row[0][3]), self.table.item(row, x).text())
                    StorageDef.save()
                else:
                    StorageDef = StorageDefVal(None, str(storage_id), str(self.types[(x - 1)]), '0',
                                               self.table.item(row, x).text())
                    StorageDef.save()

        self.changed = False

    def valueChanged(self, item):
        self.changed = True

    def clos(self):
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def openStorageAddWindow(self):
        self.storage = StorageManagementForm()
        self.storage.show()
        self.storage.signal.connect(self.clos)

    def addStorageCap(self):
        storage_cap = StorageCap(0, str(self.storage.itemData(self.storage.currentIndex())), self.coal.text(),
                                 self.pellet.text(), self.iron.text())
        storage_cap.save()
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def mk(self, val):
        storage_cap = StorageCap()
        storage_cap.delete(val)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def cls(self, val):
        if val == 1:
            self.changed = False
            self.close()

    def closeEvent(self, evt):
        if self.changed:
            self.sup = SupportWindow("Действительно хотите закрыть?", 1)
            self.sup.show()
            self.sup.signal.connect(self.cls)
            evt.ignore()
        else:
            QWidget.closeEvent(self, evt)


class RailwaysForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('ЖД-пути')
        self.resize(400, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(4)
        thead = ['ID', 'Номер', 'Статус', 'Время начала работ']
        col_num = 0
        row_num = 0
        for val in thead:
            self.table.setItem(row_num, col_num, QTableWidgetItem(str(val)))
            col_num += 1

        railway = Railway()
        self.data = railway.getAll()
        row_num = 0
        for i in self.data:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            for j in i:
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                if col_num == 2:
                    if j == "" or j == "null" or j == "0" or j == None:
                        self.table.setItem(row_num, col_num, QTableWidgetItem("Свободен"))
                    else:
                        self.table.setItem(row_num, col_num, QTableWidgetItem("Занят"))

                col_num += 1

            # row_num += 1
            # self.table.setRowCount((row_num + 1))
            # self.table.setItem(row_num, col_num, QTableWidgetItem(str(i)))
            # col_num = 0
            # iter = 0
            # for j in i:
            #     if iter == 2:
            #         if j == "" or j == "null" or j == "0" or j == None:
            #             self.table.setItem(row_num, col_num, QTableWidgetItem("Свободен"))
            #         else:
            #             self.table.setItem(row_num, col_num, QTableWidgetItem("Занят"))
            #     else:
            #         self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
            #     if iter == 3:
            #         j = QDateTime().fromTime_t(j).toString("dd.MM.yyyy h:mm")
            #         self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))

        self.layout.addWidget(self.table)


class TrainsForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('ЖД составы')
        self.resize(600, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(9)
        thead = ["ID", "№ состава", "Экспедитор", "дата и время подхода состава", "Вид груза", "Количество вагонов", "Только прямой вариант (вагон - судно)", "Путь"]
        col_num = 0
        for val in thead:
            self.table.setItem(0, col_num, QTableWidgetItem(str(val)))
            col_num += 1

        trains = Train()
        trains = trains.getAll()
        row_num = 0
        for i in trains:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            iter = 0
            for j in i:
                if iter == 2:
                    e = Expeditor()
                    exp = e.find(j)
                    j = exp[0][1]
                if iter == 3:
                    time = QDateTime().fromTime_t(j).toString("dd.MM.yyyy h:mm")
                    j = time
                if iter == 7:
                    if j != 0 and j != "None" and j != None:
                        rw = "Путь №" + str(j)
                        j = rw
                    else:
                        j = "В ожидании"

                if iter != 6:
                    self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                else:
                    ch_b_w = QWidget()
                    ch = QCheckBox(ch_b_w)
                    if j == 1:
                        ch.setCheckState(Qt.Checked)
                    self.table.setCellWidget(row_num, col_num, ch_b_w)
                col_num += 1
                iter += 1
            w = QWidget()
            s = str(i[0])
            p = MyButton("Удалить", w, s)
            p.s.connect(self.delTrainPrepare)
            self.table.setCellWidget(row_num, col_num, w)

        self.layout.addWidget(self.table)

        butt = QPushButton("Добавить состав")
        butt.released.connect(self.openAddTrainForm)
        self.layout.addWidget(butt)

        self.workers_resource = 75
        self.tech_resource = 30
        resW = QWidget()
        resW_l = QFormLayout()
        resW.setLayout(resW_l)
        resW_l.addWidget(QLabel('Свобоные ресурсы'))
        txt = QLineEdit()
        txt.setText(str(self.workers_resource))
        txt.textChanged.connect(self.changedWorkers)
        resW_l.addRow(QLabel("Люди"), txt)
        txt = QLineEdit()
        txt.setText(str(self.tech_resource))
        txt.textChanged.connect(self.changedTech)
        resW_l.addRow(QLabel("Техника"), txt)
        self.layout.addWidget(resW)

    def changedWorkers(self, text):
        self.workers_resource = int(text)

    def changedTech(self, text):
        self.tech_resource = int(text)

    def addExp(self, val):
        self.ship_id = val
        add_e_w = QWidget()
        l = QFormLayout()
        add_e_w.setLayout(l)
        add_e_w.exp = QComboBox()
        e = Expeditor()
        ex = e.getAll()
        for i in ex:
            add_e_w.exp.addItem(i[1], i[0])

        l.addRow(QLabel("Экспедитор"), add_e_w.exp)
        add_e_w.cargo = QComboBox()
        cargo = Cargo()
        c = cargo.getAll()
        for i in c:
            add_e_w.cargo.addItem(i[1], i[0])
        l.addRow(QLabel("Тип груза"), add_e_w.cargo)
        add_e_w.amount = QLineEdit()
        l.addRow(QLabel("Количество"), add_e_w.amount)
        do_add = QPushButton("Добавить")
        do_add.released.connect(self.doAddExpeditorShip)
        l.addWidget(do_add)
        self.addExpeditorShipForm = add_e_w
        self.addExpeditorShipForm.show()

    def doAddExpeditorShip(self):
        s = Ship()
        ship = s.find(self.ship_id)
        exps = s.getExpeditors(self.ship_id)
        total = 0
        if exps != []:
            for i in exps:
                total += i[4]

        total += int(self.addExpeditorShipForm.amount.text())
        if total > ship[0][9]:
            QMessageBox.about(self, 'Ошибка!', "Вы не можете добавить груз больше, чем дедвейт судна")
            return False
        s.addExpeditor(str(self.ship_id), str(self.addExpeditorShipForm.exp.currentData()),
                       str(self.addExpeditorShipForm.cargo.currentData()), str(self.addExpeditorShipForm.amount.text()))
        self.addExpeditorShipForm.close()
        self.reload()

    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)

    def openAddTrainForm(self):
        self.t = AddTrain(self)
        self.t.show()

    def reload(self):
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def delTrain(self, val):
        if val == 1:
            train = Train()
            train.delete(self.delete_id)
            qw = QWidget()
            qw.setLayout(self.layout)
            self.setMainUi()

    def delTrainPrepare(self, val):
        self.sup = SupportWindow('Удалить запись?', 1)
        self.sup.show()
        self.delete_id = val
        self.sup.signal.connect(self.delTrain)


class ShipsForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Суда")
        self.resize(600, 400)
        self.setMainUi()

    def setMainUi(self):
        global METEO

        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(13)
        thead = ["Название судна", "дата и время подхода судна", "Дата отхода", "Длина", "Осадка", "Максимальный вес",
                 "Экспедитор", "Вид груза", "Причал", "Грузовая партия", "Приоритетное судно", "Удаление судна",
                 "Добавить экспедитора"]
        col_num = 0
        for val in thead:
            self.table.setItem(0, col_num, QTableWidgetItem(str(val)))
            col_num += 1

        ship = Ship()
        # t.save()
        ships = ship.getAll()
        row_num = 0
        for i in ships:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            iter = 0
            for j in i:
                if iter == 0 or iter == 7:
                    iter += 1
                    continue
                if iter == 2:
                    time = QDateTime().fromTime_t(j).toString("dd.MM.yyyy h:mm")
                    j = time

                if iter == 6:
                    doc = ""
                    if str(j) != "" and str(j) != "None":
                        doc = "Причал №" + str(j)
                    else:
                        doc = "В ожидании"
                    self.table.setItem(row_num, 8, QTableWidgetItem(doc))
                else:
                    self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                if iter == 2:
                    col_num += 1
                    self.table.setItem(row_num, col_num, QTableWidgetItem(""))

                col_num += 1
                iter += 1

            s_e = ship.getExpeditors(str(i[0]))
            if s_e != []:
                w1 = QWidget()
                l1 = QBoxLayout(QBoxLayout.TopToBottom)
                w1.setLayout(l1)

                w2 = QWidget()
                l2 = QBoxLayout(QBoxLayout.TopToBottom)
                w2.setLayout(l2)

                w3 = QWidget()
                l3 = QBoxLayout(QBoxLayout.TopToBottom)
                w3.setLayout(l3)
                for line in s_e:
                    e = Expeditor()
                    ex = e.find(line[2])
                    l1.addWidget(QLabel(str(ex[0][1])))

                    c = Cargo()
                    ca = c.find(line[3])
                    l2.addWidget(QLabel(str(ca[0][1])))

                    l3.addWidget(QLabel(str(line[4])))

                self.table.setCellWidget(row_num, 6, w1)
                self.table.setCellWidget(row_num, 7, w2)
                self.table.setCellWidget(row_num, 9, w3)

            w = QWidget()
            с = QCheckBox(w)
            if str(i[7]) == "1":
                c.setCheckState(Qt.Checked)
            self.table.setCellWidget(row_num, 10, w)
            w = QWidget()
            s = str(i[0])
            p = MyButton('Удалить', w, s)
            p.s.connect(self.delShipPrepare)
            self.table.setCellWidget(row_num, 11, w)
            w = QWidget()
            s = str(i[0])
            p = MyButton('Добавить экспедитора', w, s)
            p.s.connect(self.addExp)
            self.table.setCellWidget(row_num, 12, w)

        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.layout.addWidget(self.table)

        but = QPushButton('Добавить судно')
        but.released.connect(self.openAddShipForm)
        self.layout.addWidget(but)

    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)

    def addExp(self, val):
        self.ship_id = val
        add_e_w = QWidget()
        l = QFormLayout()
        add_e_w.setLayout(l)
        add_e_w.exp = QComboBox()
        e = Expeditor()
        ex = e.getAll()
        for i in ex:
            add_e_w.exp.addItem(i[1], i[0])

        l.addRow(QLabel("Экспедитор"), add_e_w.exp)
        add_e_w.cargo = QComboBox()
        cargo = Cargo()
        c = cargo.getAll()
        for i in c:
            add_e_w.cargo.addItem(i[1], i[0])
        l.addRow(QLabel("Тип груза"), add_e_w.cargo)
        add_e_w.amount = QLineEdit()
        l.addRow(QLabel("Количество"), add_e_w.amount)
        do_add = QPushButton("Добавить")
        do_add.released.connect(self.doAddExpeditorShip)
        l.addWidget(do_add)
        self.addExpeditorShipForm = add_e_w
        self.addExpeditorShipForm.show()

    def doAddExpeditorShip(self):
        s = Ship()
        ship = s.find(self.ship_id)
        exps = s.getExpeditors(self.ship_id)
        total = 0
        if exps != []:
            for i in exps:
                total += i[4]

        total += int(self.addExpeditorShipForm.amount.text())
        if total > ship[0][9]:
            QMessageBox.about(self, 'Ошибка!', "Вы не можете добавить груз больше, чем дедвейт судна")
            return False
        s.addExpeditor(str(self.ship_id), str(self.addExpeditorShipForm.exp.currentData()),
                       str(self.addExpeditorShipForm.cargo.currentData()), str(self.addExpeditorShipForm.amount.text()))
        self.addExpeditorShipForm.close()
        self.reload()

    def openAddShipForm(self):
        self.f = AddShip(self)
        self.f.show()

    def reload(self):
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def delShip(self, val):
        if val == 1:
            ship = Ship()
            s = ship.find(self.delete_id)
            d = DocChar()
            d.unuseDoc(s[0][8])
            exps = ship.getExpeditors(self.delete_id)
            if exps != []:
                for i in exps:
                    ship.deleteExpeditor(str(i[0]))
            ship.delete(self.delete_id)
            qw = QWidget()
            qw.setLayout(self.layout)
            self.setMainUi()

    def delShipPrepare(self, val):
        self.sup = SupportWindow('Удалить запись?', 1)
        self.sup.show()
        self.delete_id = val
        self.sup.signal.connect(self.delShip)


class AddShip(QWidget):
    mainWinSignal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.p = parent
        self.setMainUi()

        self.setWindowTitle("Добавление судна")
        self.show()

    def setMainUi(self):
        la = QFormLayout()
        self.l1 = QComboBox()
        cargo = Cargo()
        c = cargo.getAll()
        if c != []:
            for i in c:
                self.l1.addItem(i[1], i[0])

        self.typical = QComboBox()
        ts = TypicalShip()
        ships = ts.getAll()
        self.typical.addItem("Выбрать", None)
        if ships != []:
            for s in ships:
                self.typical.addItem(s[1], s[0])

        self.typical.currentIndexChanged.connect(self.setTypical)
        # l1 = QLineEdit()
        self.l2 = QLineEdit()
        self.l3 = QLineEdit()
        self.l4 = QLineEdit()
        self.max_weight = QLineEdit()
        self.l5 = QDateTimeEdit()
        self.l5.setCalendarPopup(True)
        self.calendL5 = QCalendarWidget()
        self.l5.setCalendarWidget(self.calendL5)
        self.l5.setDate(QDate().currentDate())
        # self.l6 = QComboBox()
        # e = Expeditor()
        # ex = e.getAll()
        # for i in ex:
        # self.l6.addItem(i[1], i[0])
        # la.addRow(QLabel("Вид груза"), self.l1)
        # la.addRow(QLabel("Вид груза"), self.l6)
        # btn_add_exp = QPushButton("Добавить еще экспедитора")
        # btn.released.connect(self.addExp)
        # la.addWidget(btn_add_exp)
        la.addRow(QLabel("Типовое судно"), self.typical)
        la.addRow(QLabel("Название"), self.l2)
        la.addRow(QLabel("длина"), self.l3)
        la.addRow(QLabel("Осадка"), self.l4)
        la.addRow(QLabel("Максимальный вес"), self.max_weight)
        la.addRow(QLabel("Через сколько придет(ч)"), self.l5)

        self.l6 = QCheckBox()
        self.l6.stateChanged.connect(self.showDocs)
        la.addRow(QLabel("Определить причал"), self.l6)
        doc_w = QWidget()
        d_la = QFormLayout()
        doc_w.setLayout(d_la)
        self.l7 = QComboBox()
        self.l7.addItem("Выбор причала", None)
        d = DocChar()
        docs = d.getAll()
        for i in docs:
            self.l7.addItem(str(i[1]), i[0])
        d_la.addRow(QLabel('Причал'), self.l7)
        doc_w.hide()
        la.addRow(doc_w)
        self.d_la = d_la
        self.doc_w = doc_w

        self.l8 = QCheckBox()
        la.addRow(QLabel("Приоритетное судно"), self.l8)
        subm = QPushButton('Добавить')
        subm.released.connect(self.addShip)
        la.addRow(None, subm)
        self.setLayout(la)

    def showDocs(self):
        ch = self.l6.checkState()
        if ch == Qt.Unchecked:
            self.doc_w.hide()
        else:
            self.doc_w.show()

    def setTypical(self):
        typical = TypicalShip()
        ts = typical.find(self.typical.currentData())
        self.l2.setText(str(ts[0][1]))
        self.l3.setText(str(ts[0][3]))
        self.l4.setText(str(ts[0][2]))
        self.max_weight.setText(str(ts[0][4]))

    def addShip(self):
        error = False
        error_text = ""
        name = self.l2.text()
        length = self.l3.text()
        depth = self.l4.text()
        arrival = self.l5
        priority = "0"
        ch_p = self.l8.checkState()
        if ch_p != Qt.Unchecked:
            priority = "1"

        try:
            length = float(length)
        except Exception:
            error = True
            error_text = error_text + "Поле Длина должно быть числовым\n"

        try:
            depth = float(depth)
        except Exception:
            error = True
            error_text = error_text + "Поле Осадка должно быть числовым\n"

        if QDate.currentDate() > arrival.date():
            error = True
            error_text = error_text + "Дата прибытия не должнa быть меньше текущей\n"

        doc_num = 0
        ch = self.l6.checkState()
        if ch != Qt.Unchecked:
            doc_num = self.l7.itemData(self.l7.currentIndex())
        # d = DocChar()
        # docs = d.getAll()
        # docn = ""
        # for doc in docs:
        # if docn != "":
        # break
        # if str(doc[4]) == "" or str(doc[4]) == "0" or str(doc[4]) == "Null" or doc[4] == None:
        # if int(doc[2]) > int(length) and float(doc[3]) > float(depth):
        # docn = doc[0]
        # d.useDoc(str(doc[0]))
        # else:
        # continue
        docn = ""
        if doc_num != 0:
            d = DocChar()
            doc = d.find(doc_num)
            docn = doc[0][1]

        if not error:
            ship = Ship(0, str(length), str(depth), str(self.max_weight.text()), str(arrival.dateTime().toTime_t()),
                        str(name), str(docn), str(priority))
            ship.save()
            self.p.reload()
            self.close()
        else:
            QMessageBox.about(self, 'Ошибка!', error_text)


class CranManagementForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление кранами")
        self.resize(600, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        row_w = QWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(5)
        thead = ["Номер крана", "Тип", "Обслуживаемые объекты", "  Удаление   ", "Добавление объектов"]
        row_w_l = QBoxLayout(QBoxLayout.LeftToRight)
        row_w.setLayout(row_w_l)
        col_num = 0
        for val in thead:
            row_w_l.addWidget(QLabel(val))
            self.table.setItem(0, col_num, QTableWidgetItem(str(val)))
            col_num += 1

        # self.layout.addWidget(row_w)
        row_num = 0
        crans = Cran()
        for i in crans.getAllGroupBy():
            row_w = QWidget()
            row_w_l = QBoxLayout(QBoxLayout.LeftToRight)
            row_w.setLayout(row_w_l)
            row_num += 1
            self.table.setRowCount((row_num + 1))
            self.table.setItem(row_num, 0, QTableWidgetItem(str(i[1])))
            row_w_l.addWidget(QLabel(str(i[1])))
            cran_type = CranType()
            ct = cran_type.find(i[2])
            row_w_l.addWidget(QLabel(str(ct[0][1])))
            self.table.setItem(row_num, 1, QTableWidgetItem(str(ct[0][1])))
            col_num = 0
            # for j in i:
            # self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
            # col_num += 1

            cr = crans.findBy('num', '=', str(i[1]))
            cor_3_wgt = QWidget()
            cor_l = QFormLayout()
            cor_3_wgt.setLayout(cor_l)
            for row in cr:
                if row[3] != '':
                    name = ""
                    if int(row[3]) == 1:
                        s = Storage()
                        tmp = s.find(str(row[3]))
                        name = tmp[0][1]
                    if int(row[3]) == 2:
                        name = "Причал №" + str(row[4])
                    if int(row[3]) == 3:
                        name = "Путь №" + str(i[4])
                    name = str(name)
                    s = str(row[0])
                    p = MyButton('Удалить', None, s)
                    p.s.connect(self.delObjectConfirm)
                    cor_l.addRow(QLabel(name), p)

            # row_w_l.addWidget(cor_3_wgt)
            cor_3_wgt.resize(100, 100)
            self.table.setCellWidget(row_num, 2, cor_3_wgt)

            w = QWidget()
            s = str(i[1])
            p = MyButton('Удалить', w, s)
            p.s.connect(self.delConfirm)
            w.resize(120, 30)
            self.table.setCellWidget(row_num, 3, w)
            w = QWidget()
            s = str(i[1])
            p = MyButton('Добавить объект', w, s)
            p.s.connect(self.addObjectToCran)
            w.resize(130, 30)
            self.table.setCellWidget(row_num, 4, w)
            # row_w_l.addWidget(cor_3_wgt)
            # self.layout.addWidget(row_w)
            # w = QWidget()
            # s = str(i[0])
            # p = SaveRowButton('Сохранить', w, s, str(row_num), (col_num - 2))
            # p.s.connect(self.save_W)
            # self.table.setCellWidget(row_num, col_num, w)

        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.horizontalHeader().setDefaultSectionSize(130)
        self.layout.addWidget(self.table)

        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        self.layout.addWidget(w)
        add_b = QPushButton('Добавить кран')
        l.addWidget(add_b)
        add_b.released.connect(self.addCranFormFunc)

        return False

    def addObjectToCran(self, val):
        self.cran_num = val
        w = QWidget()
        w.setWindowTitle("Добавить объект")
        w.l = QGridLayout()
        w.setLayout(w.l)
        w.type = QComboBox()
        w.type.addItem("Склад", 1)
        w.type.addItem("Причал", 2)
        w.type.addItem("Путь", 3)
        w.type.currentIndexChanged.connect(self.getObjectsByType)

        w.l.addWidget(QLabel("Тип объекта"), 0, 0)
        w.l.addWidget(w.type, 0, 1)

        self.addObjectToCranForm = w
        self.addObjectToCranForm.show()

        objects = QComboBox()

        self.addObjectToCranForm.objects = objects
        self.addObjectToCranForm.l.addWidget(QLabel("Объект"), 1, 0)
        self.addObjectToCranForm.l.addWidget(objects, 1, 1)
        self.addObjectToCranForm.add_b = QPushButton("Добавить")
        self.addObjectToCranForm.add_b.released.connect(self.addObjectToCranDo)
        self.addObjectToCranForm.l.addWidget(self.addObjectToCranForm.add_b)

        self.getObjectsByType(1)

    def addObjectToCranDo(self):
        if not hasattr(self.addObjectToCranForm, 'objects'):
            QMessageBox.about(self, 'Ошибка!', "Добавьте объект")
            return False

        cr = Cran()
        c = cr.findBy('num', '=', str(self.cran_num))
        cran = Cran(None, str(self.cran_num), str(c[0][2]), str(self.addObjectToCranForm.type.currentData()),
                    str(self.addObjectToCranForm.objects.currentData()))
        cran.save()
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()
        self.addObjectToCranForm.close()

    def getObjectsByType(self, type=None):
        type = self.addObjectToCranForm.type.currentData()
        obs = []
        if type == 1:
            s = Storage()
            obs = s.getAll()
        if type == 2:
            d = DocChar()
            tmp = d.getAll()
            for i in tmp:
                obs.append((i[1], "Причал №" + str(i[1])))
        if type == 3:
            r = Railway()
            tmp = r.getAll()
            for i in tmp:
                obs.append((i[0], "Путь №" + str(i[1])))

        self.addObjectToCranForm.objects.clear()
        for ob in obs:
            self.addObjectToCranForm.objects.addItem(str(ob[1]), ob[0])

    def addCranFormFunc(self):
        w = QWidget()
        w.setWindowTitle("Добавление крана")
        w.resize(400, 400)
        w.l = QFormLayout()
        w.setLayout(w.l)
        w.num = QLineEdit()
        w.l.addRow(QLabel('Номер крана'), w.num)
        w.type = QComboBox()
        cranType = CranType()
        c = cranType.getAll()
        for i in c:
            w.type.addItem(i[1], i[0])

        w.l.addRow(QLabel('Тип крана'), w.type)
        btn = QPushButton('Добавить!')
        btn.released.connect(self.doAddCran)
        w.l.addWidget(btn)
        btn = QPushButton('Добавить тип крана')
        btn.released.connect(self.openAddCranTypeForm)
        w.l.addWidget(btn)
        w.l.addWidget(QLabel('Типы кранов'))
        cran_type = CranType()
        ct = cran_type.getAll()
        for i in ct:
            buttons_w = QWidget()
            lay = QBoxLayout(QBoxLayout.LeftToRight)
            buttons_w.setLayout(lay)

            s = str(i[0])
            p = MyButton('Просмотр', None, s)
            p.s.connect(self.editCranType)
            lay.addWidget(p)
            p = MyButton('Удалить', None, s)
            p.s.connect(self.delCranTypeConfirm)
            lay.addWidget(p)
            w.l.addRow(QLabel(i[1]), buttons_w)
        self.addCranForm = w
        self.addCranForm.show()

    def editCranType(self, val):
        cr = CranType()
        c = cr.find(val)
        self.edit_cran_id = val
        w = QWidget()
        w.setWindowTitle("Добавление типа крана")
        w.resize(600, 350)
        w.l = QFormLayout()
        w.setLayout(w.l)
        w.val1 = QLineEdit()
        w.val1.setText(str(c[0][1]))
        w.l.addRow(QLabel('Название'), w.val1)
        w.val2 = QLineEdit()
        w.val2.setText(str(c[0][2]))
        w.l.addRow(QLabel('Производительность при работе с кучи т/смена (уголь)'), w.val2)
        w.val3 = QLineEdit()
        w.val3.setText(str(c[0][3]))
        w.l.addRow(QLabel('Производительность при работе с кучи т/смена (Чугун, брикеты)'), w.val3)
        w.val4 = QLineEdit()
        w.val4.setText(str(c[0][4]))
        w.l.addRow(QLabel('Производительность при работе с подвозом груза т/смена (уголь)'), w.val4)
        # w.val5 = QLineEdit()
        # w.val5.setText(str(c[0][5]))
        # w.l.addRow(QLabel('Производительность при работе с подвозом груза т/смена (Чугун, брикеты)'), w.val5)
        # w.val6 = QLineEdit()
        # w.val6.setText(str(c[0][6]))
        # w.l.addRow(QLabel('Производительность при работе с ж/д составом вагон/смена и т/смена (уголь)'), w.val6)
        # w.val7 = QLineEdit()
        # w.val7.setText(str(c[0][7]))
        # w.l.addRow(QLabel('Производительность при работе с ж/д составом вагон/смена и т/смена (Чугун, брикеты)'),
        #            w.val7)
        btn = QPushButton('Сохранить')
        btn.released.connect(self.editCranTypeDo)
        w.l.addWidget(btn)
        self.editCranTypeForm = w
        self.editCranTypeForm.show()

    def editCranTypeDo(self):
        cran = CranType(self.edit_cran_id, self.editCranTypeForm.val1.text(), self.editCranTypeForm.val2.text(),
                        self.editCranTypeForm.val3.text(), self.editCranTypeForm.val4.text(),
                        self.editCranTypeForm.val5.text(), self.editCranTypeForm.val6.text(),
                        self.editCranTypeForm.val7.text())
        cran.save()
        self.editCranTypeForm.close()

    def delCranTypeConfirm(self, val):
        self.delete_id = val
        self.sup = SupportWindow("Действительно хотите удалить?", 1)
        self.sup.show()
        self.sup.signal.connect(self.delCranType)

    def delCranType(self):
        cran_type = CranType()
        cran_type.delete(self.delete_id)
        self.addCranForm.close()
        self.addCranFormFunc()

    def doAddCran(self):
        crans = Cran(None, self.addCranForm.num.text(), str(self.addCranForm.type.currentData()), "", "")
        crans.save()
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()
        self.addCranForm.close()

    def delObjectConfirm(self, val):
        self.delete_id = val
        self.sup = SupportWindow("Действительно хотите удалить?", 1)
        self.sup.show()
        self.sup.signal.connect(self.deleteObject)

    def deleteObject(self, val):
        cran = Cran()
        cran.delete(self.delete_id)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def delConfirm(self, val):
        self.delete_id = val
        self.sup = SupportWindow("Действительно хотите удалить?", 1)
        self.sup.show()
        self.sup.signal.connect(self.mk)

    def openAddCranTypeForm(self):
        w = QWidget()
        w.setWindowTitle("Добавление типа крана")
        w.resize(600, 350)
        w.l = QFormLayout()
        w.setLayout(w.l)
        w.val1 = QLineEdit()
        w.l.addRow(QLabel('Название'), w.val1)
        w.val2 = QLineEdit()
        w.l.addRow(QLabel('Производительность при работе с кучи т/смена (уголь)'), w.val2)
        w.val3 = QLineEdit()
        w.l.addRow(QLabel('Производительность при работе с кучи т/смена (Чугун, брикеты)'), w.val3)
        w.val4 = QLineEdit()
        w.l.addRow(QLabel('Производительность при работе с подвозом груза т/смена (уголь)'), w.val4)
        w.val5 = QLineEdit()
        w.l.addRow(QLabel('Производительность при работе с подвозом груза т/смена (Чугун, брикеты)'), w.val5)
        w.val6 = QLineEdit()
        w.l.addRow(QLabel('Производительность при работе с ж/д составом вагон/смена и т/смена (уголь)'), w.val6)
        w.val7 = QLineEdit()
        w.l.addRow(QLabel('Производительность при работе с ж/д составом вагон/смена и т/смена (Чугун, брикеты)'),
                   w.val7)
        btn = QPushButton('Добавить')
        btn.released.connect(self.addCranType)
        w.l.addWidget(btn)
        self.addCranTypeForm = w
        self.addCranTypeForm.show()

    def addCranType(self):
        c = CranType(None, self.addCranTypeForm.val1.text(), self.addCranTypeForm.val2.text(),
                     self.addCranTypeForm.val3.text(), self.addCranTypeForm.val4.text(),
                     self.addCranTypeForm.val5.text(), self.addCranTypeForm.val6.text(),
                     self.addCranTypeForm.val7.text())
        c.save()
        self.addCranTypeForm.close()

    def mk(self, val):
        cran = Cran()
        cran.deleteByNum(self.delete_id)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()


class AddTrain(QWidget):
    mainWinSignal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.p = parent
        self.setMainUi()

        self.setWindowTitle("Добавление состава")
        self.show()

    def setMainUi(self):
        la = QFormLayout()
        self.l1 = QComboBox()
        cargo = Cargo()
        c = cargo.getAll()
        for i in c:
            self.l1.addItem(i[1], i[0])

        self.l4 = QComboBox()
        e = Expeditor()
        exp = e.getAll()
        for i in exp:
            self.l4.addItem(i[1], i[0])
        # l1 = QLineEdit()
        self.l3 = QDateTimeEdit()
        self.l3.setCalendarPopup(True)
        self.calendL3 = QCalendarWidget()
        self.l3.setCalendarWidget(self.calendL3)
        self.l3.setDate(QDate().currentDate())
        self.num = QLineEdit()
        la.addRow(QLabel("№ состава"), self.num)
        la.addRow(QLabel("Вид груза"), self.l1)

        la.addRow(QLabel("Через сколько придет"), self.l3)
        la.addRow(QLabel("Экспедитор"), self.l4)
        self.l5 = QLineEdit()
        self.l5.textEdited.connect(self.editCargoValue)
        la.addRow(QLabel("Количество вагонов"), self.l5)
        self.l2 = QLabel()
        la.addRow(QLabel("Грузовая партия"), self.l2)
        self.l6 = QCheckBox()
        self.l6.stateChanged.connect(self.showShips)
        la.addRow(QLabel("Только прямой путь(вагон-судно)"), self.l6)

        ship_w = QWidget()
        sh_la = QFormLayout()
        ship_w.setLayout(sh_la)
        self.l7 = QComboBox()
        s = Ship()
        ships = s.getAll()
        self.l7.addItem("Выбор судна", None)
        for i in ships:
            self.l7.addItem(i[1], i[0])
        sh_la.addRow(QLabel('Привязать судно'), self.l7)
        ship_w.hide()
        la.addRow(ship_w)
        self.sh_la = sh_la
        self.sh_w = ship_w

        self.l8 = QCheckBox()
        self.l8.stateChanged.connect(self.showRailways)
        la.addRow(QLabel("Определить путь"), self.l8)
        rw_w = QWidget()
        rw_la = QFormLayout()
        rw_w.setLayout(rw_la)
        self.l9 = QComboBox()
        self.l9.addItem("Выбор ж/д пути", None)
        self.l9.addItem("Путь №1", 1)
        self.l9.addItem("Путь №2", 2)
        self.l9.addItem("Путь №3", 3)
        self.l9.addItem("Путь №4", 4)
        rw_la.addRow(QLabel('Путь'), self.l9)
        rw_w.hide()
        la.addRow(rw_w)
        self.rw_la = rw_la
        self.rw_w = rw_w

        subm = QPushButton('Добавить')
        subm.released.connect(self.addTrain)
        la.addRow(None, subm)
        self.la = la
        self.setLayout(la)

    def editCargoValue(self, val):
        self.l2.setText(str(int(val) * 70))

    def showShips(self):
        ch = self.l6.checkState()
        if ch == Qt.Unchecked:
            self.sh_w.hide()
        else:
            self.sh_w.show()

    def showRailways(self):
        ch = self.l8.checkState()
        if ch == Qt.Unchecked:
            self.rw_w.hide()
        else:
            self.rw_w.show()

    def getFreeRw(self, time, cargo, expeditor, direct):
        rw = Railway()
        tr_inst = Train()
        ship_instance = Ship()
        tmp_free_rw = 0
        doc_inst = DocChar()
        docs_ids = ''
        docs = doc_inst.getBy('num', 'in', '(2,3,5,6)')
        docs_by_ids = {}
        for doc in docs:
            docs_by_ids[doc[0]] = doc[1]
            docs_ids += str(doc[0])
            docs_ids += ', '

        if direct == '1':
            ship_id = self.l7.itemData(self.l7.currentIndex())
            ship = ship_instance.find(ship_id)
            if (int(time) + 86400) > int(ship[0][5]):
                if int(docs_by_ids[ship[0][8]]) == 2 or int(docs_by_ids[ship[0][8]]) == 3:
                    tmp_free_rw = 4
                    trains = tr_inst.getBy('railway', '=', str(tmp_free_rw))
                    if trains != []:
                        for tr in trains:
                            if int(time) > int(tr[3]) and int(time) < (int(tr[3]) + 5 * 86400):
                                tmp_free_rw = 0

                if int(docs_by_ids[ship[0][8]]) == 5 or int(docs_by_ids[ship[0][8]]) == 6:
                    tmp_free_rw = 1
                    trains = tr_inst.getBy('railway', '=', str(tmp_free_rw))
                    if trains != []:
                        for tr in trains:
                            if int(time) > int(tr[3]) and int(time) < (int(tr[3]) + 5 * 86400):
                                tmp_free_rw = 0

                return tmp_free_rw

        docs_ids = docs_ids[:-2]
        ships = ship_instance.getBy('doc', 'in', ' (' + docs_ids + ') order by arrival_time asc')
        if ships != []:
            for ship in ships:
                if tmp_free_rw != 0:
                    break
                exps = ship_instance.getExpeditors(ship[0])
                if exps != []:
                    for exp in exps:
                        if (int(time) + 86400) > int(ship[5]) and int(exp[3]) == int(cargo) and int(exp[2]) == int(
                                expeditor):
                            if int(docs_by_ids[ship[8]]) == 2 or int(docs_by_ids[ship[8]]) == 3:
                                tmp_free_rw = 4
                                trains = tr_inst.getBy('railway', '=', str(tmp_free_rw))
                                if trains != []:
                                    for tr in trains:
                                        if int(time) > int(tr[3]) and int(time) < (int(tr[3]) + 5 * 86400):
                                            tmp_free_rw = 0

                            if int(docs_by_ids[ship[8]]) == 5 or int(docs_by_ids[ship[8]]) == 6:
                                tmp_free_rw = 1
                                trains = tr_inst.getBy('railway', '=', str(tmp_free_rw))
                                if trains != []:
                                    for tr in trains:
                                        if int(time) > int(tr[3]) and int(time) < (int(tr[3]) + 5 * 86400):
                                            tmp_free_rw = 0
                            break

        if direct == '0':
            if tmp_free_rw == 0:
                tmp_free_rw = 2
                trains = tr_inst.getBy('railway', '=', str(tmp_free_rw))
                if trains != []:
                    for tr in trains:
                        if int(time) > int(tr[3]) and int(time) < (int(tr[3]) + 5 * 86400):
                            tmp_free_rw = 0

            if tmp_free_rw == 0:
                tmp_free_rw = 3
                trains = tr_inst.getBy('railway', '=', str(tmp_free_rw))
                if trains != []:
                    for tr in trains:
                        if int(time) > int(tr[3]) and int(time) < (int(tr[3]) + 5 * 86400):
                            tmp_free_rw = 0

            if tmp_free_rw == 0:
                tmp_free_rw = 4
                trains = tr_inst.getBy('railway', '=', str(tmp_free_rw))
                if trains != []:
                    for tr in trains:
                        if int(time) > int(tr[3]) and int(time) < (int(tr[3]) + 5 * 86400):
                            tmp_free_rw = 0

            if tmp_free_rw == 0:
                tmp_free_rw = 1
                trains = tr_inst.getBy('railway', '=', str(tmp_free_rw))
                if trains != []:
                    for tr in trains:
                        if int(time) > int(tr[3]) and int(time) < (int(tr[3]) + 5 * 86400):
                            tmp_free_rw = 0

        return tmp_free_rw

    def addTrain(self):
        error = False
        error_text = ""
        cargo = self.l1.itemData(self.l1.currentIndex())
        amount = self.l2.text()
        arrival_time = self.l3
        expeditor = self.l4.itemData(self.l4.currentIndex())
        ch = self.l6.checkState()
        ch2 = self.l8.checkState()
        ship_id = ""
        if ch == Qt.Unchecked:
            direct = "0"
        else:
            direct = "1"
            ship_id = self.l7.itemData(self.l7.currentIndex())

        # Для выполнения поиска пути для состава
        railway = ""
        if ch2 != Qt.Unchecked:
            railway = self.l9.itemData(self.l9.currentIndex())
        # free_rw = self.getFreeRw(arrival_time.dateTime().toTime_t(), cargo, expeditor, direct)
        # railway = free_rw

        if self.num.text() == "":
            error = True
            error_text = error_text + "Поле номер поезда не должно быть пустым\n"

        try:
            cargo = int(cargo)
        except Exception:
            error = True
            error_text = error_text + "Ошибка в поле Тип груза\n"

        try:
            amount = int(amount)
        except Exception:
            error = True
            error_text = error_text + "Поле Грузовая партия должно быть числовым\n"

        if QDate.currentDate() > arrival_time.date():
            error = True
            error_text = error_text + "Дата прибытия не должнa быть меньше текущей\n"

        # if railway == 0:
        # QMessageBox.about(self, 'Внимание!',"Состав находится в ожидании")

        if not error:
            train = Train(0, str(cargo), str(amount), str(arrival_time.dateTime().toTime_t()), str(expeditor),
                          self.l5.text(), direct, self.num.text(), str(railway), str(ship_id))

            train.save()
            self.p.reload()
            self.close()
        else:
            QMessageBox.about(self, 'Ошибка!', error_text)


class OtherEquipmentForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вспомогательная техника')
        self.resize(400, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        otherequipment = OtherEquipment()
        self.data = otherequipment.getAll()
        row_num = -1
        for i in self.data:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            for j in i:
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                col_num += 1
            w = QWidget()
            s = str(i[0])
            p = MyButton('Удалить', w, s)
            p.s.connect(self.mk)
            self.table.setCellWidget(row_num, col_num, w)

        self.layout.addWidget(self.table)
        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        self.layout.addWidget(w)
        add_b = QPushButton('Добавить значение')
        self.type = QLineEdit()
        l.addWidget(self.type)
        l.addWidget(add_b)
        add_b.released.connect(self.addCargo)

    def addCargo(self):
        if self.type.text() == '':
            self.sup = SupportWindow('Заполните название', 0)
            self.sup.show()
            return False
        otherequipment = OtherEquipment(0, self.type.text())
        otherequipment.save()
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def mk(self, val):
        otherequipment = OtherEquipment()
        otherequipment.delete(val)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()


class CargoTypeForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Типы груза')
        self.resize(400, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        cargo = Cargo()
        self.data = cargo.getAll()
        row_num = -1
        for i in self.data:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            for j in i:
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                col_num += 1
            w = QWidget()
            s = str(i[0])
            p = MyButton('Удалить', w, s)
            p.s.connect(self.mk)
            self.table.setCellWidget(row_num, col_num, w)

        self.layout.addWidget(self.table)
        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        self.layout.addWidget(w)
        add_b = QPushButton('Добавить значение')
        self.type = QLineEdit()
        l.addWidget(self.type)
        l.addWidget(add_b)
        add_b.released.connect(self.addCargo)

    def addCargo(self):
        if self.type.text() == '':
            self.sup = SupportWindow('Заполните название', 0)
            self.sup.show()
            return False
        cargo = Cargo(0, self.type.text())
        cargo.save()
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def mk(self, val):
        cargo = Cargo()
        cargo.delete(val)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()


class ExpeditorManagementForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Экспедиторы")
        self.resize(400, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        exp = Expeditor()
        expeditors = exp.getAll()
        self.layout.addWidget(QLabel('Экспедиторы'))
        self.LEs = {}
        for i in expeditors:
            w = QWidget()
            w.l = QBoxLayout(QBoxLayout.LeftToRight)
            w.setLayout(w.l)
            s = str(i[0])
            p = MyButton('Сохранить', None, s)
            p.s.connect(self.saveExpeditor)
            self.LEs[str(i[0])] = QLineEdit(i[1])
            w.l.addWidget(self.LEs[str(i[0])])
            w.l.addWidget(p)
            s = str(i[0])
            p = MyButton('Удалить', None, s)
            p.s.connect(self.delExpeditorConfirm)
            w.l.addWidget(p)
            self.layout.addWidget(w)

        self.layout.addWidget(QLabel(''))
        self.exp_name = QLineEdit()
        add_exp_btn = QPushButton('Добавить')
        add_exp_btn.released.connect(self.addExpeditor)
        w = QWidget()
        w.l = QBoxLayout(QBoxLayout.LeftToRight)
        w.setLayout(w.l)
        w.l.addWidget(self.exp_name)
        w.l.addWidget(add_exp_btn)
        self.layout.addWidget(w)

        return False

    def saveExpeditor(self, val):
        exp = Expeditor(val, self.LEs[val].text())
        exp.save()
        w = QWidget()
        w.setLayout(self.layout)
        self.setMainUi()

    def addExpeditor(self):
        exp = Expeditor(None, self.exp_name.text())
        exp.save()
        w = QWidget()
        w.setLayout(self.layout)
        self.setMainUi()

    def delExpeditorConfirm(self, val):
        self.delete_id = val
        self.sup = SupportWindow("Действительно хотите удалить?", 1)
        self.sup.show()
        self.sup.signal.connect(self.delExpeditor)

    def delExpeditor(self):
        exp = Expeditor()
        exp.delete(self.delete_id)
        w = QWidget()
        w.setLayout(self.layout)
        self.setMainUi()


class QualificationsForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Квалификации')
        self.resize(400, 600)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        # qualification = Qualifications()
        # self.data = qualification.getAll()

        self.layout.addWidget(self.table)


class WorkersForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Работники')
        self.resize(400, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(4)
        thead = ['ID', 'Имя', 'Фамилия', 'Профиль']
        col_num = 0
        row_num = 0
        for val in thead:
            self.table.setItem(row_num, col_num, QTableWidgetItem(str(val)))
            col_num += 1

        workers = Workers()
        self.data = workers.getAll()
        row_num = 0
        for i in self.data:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            for j in i:
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                col_num += 1
            w = QWidget()
            s = str(i[0])
            p = MyButton('Удалить', w, s)
            p.s.connect(self.mk)
            self.table.setCellWidget(row_num, col_num, w)

        self.layout.addWidget(self.table)
        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        self.layout.addWidget(w)
        add_b = QPushButton('Добавить значение')
        self.name = QLineEdit()
        self.surname = QLineEdit()
        l.addWidget(self.name)
        l.addWidget(self.surname)
        l.addWidget(add_b)
        add_b.released.connect(self.addWorker)

    def addWorker(self):
        if self.name.text() == '' or self.surname.text() == '':
            self.sup = SupportWindow('Заполните название', 0)
            self.sup.show()
            return False
        workers = Workers(0, self.name.text(), self.surname.text())
        workers.save()
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def mk(self, val):
        workers = Workers()
        workers.delete(val)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()


class WorkSkillForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Квалификации')
        self.resize(400, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(2)
        workskill = WorkSkill()
        thead = ["id квалификации", "Название"]
        col_num = 0
        for val in thead:
            self.table.setItem(0, col_num, QTableWidgetItem(str(val)))
            col_num += 1
        self.data = workskill.getAll()
        row_num = 0
        for i in self.data:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            for j in i:
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                col_num += 1
            w = QWidget()
            s = str(i[0])
            self.table.setCellWidget(row_num, col_num, w)

        self.layout.addWidget(self.table)


    def mk(self, val):
        workskill = WorkSkill()
        workskill.delete(val)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()


class PartyForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Партия')
        self.resize(400, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(8)
        cargoparty = CargoParty()
        thead = ["ID партии", "Тип поставки", "Масса", "Время прибытия", "ID причала", "Время отправки", "Владелец"]
        col_num = 0
        for val in thead:
            self.table.setItem(0, col_num, QTableWidgetItem(str(val)))
            col_num += 1
        self.data = cargoparty.getAll()
        row_num = 0
        for i in self.data:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            for j in i:
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                col_num += 1
            w = QWidget()
            s = str(i[0])
            p = MyButton('Удалить', w, s)
            p.s.connect(self.mk)
            self.table.setCellWidget(row_num, col_num, w)

        self.layout.addWidget(self.table)
        w = QWidget()
        l = QGridLayout()
        w.setLayout(l)
        self.layout.addWidget(w)
        add_b = QPushButton('Добавить')
        self.party_weight = QLineEdit()
        self.party_time_in = QLineEdit()
        self.party_time_in.setInputMask('99.9D.D9 99:99')
        self.warehouse_id = QLineEdit()
        self.party_time_out = QLineEdit()
        self.party_time_out.setInputMask('99.9D.D9 99:99')
        self.owner_name = QLineEdit()
        l.addWidget(self.party_weight, 1, 1)
        l.addWidget(self.party_time_in, 1, 2)
        l.addWidget(self.warehouse_id, 1, 3)
        l.addWidget(self.party_time_out, 1, 4)
        l.addWidget(self.owner_name, 1, 5)
        l.addWidget(QLabel('Масса'), 0, 1)
        l.addWidget(QLabel('Время поставки'), 0, 2)
        l.addWidget(QLabel('id порта'), 0, 3)
        l.addWidget(QLabel('Время отправки'), 0, 4)
        l.addWidget(QLabel('Имя владельца'), 0, 5)
        l.addWidget(add_b, 1, 6)
        add_b.released.connect(self.addCargoParty)

    def addCargoParty(self):
        if self.cargo_type_id.text() == '' or self.party_weight.text() == '' or self.party_time_in.text() == '' or self.warehouse_id.text() == '' or self.party_time_out.text() == '' or self.owner_name.text() == '':
            self.sup = SupportWindow('Заполните все значения', 0)
            self.sup.show()
            return False
        cargoparty = CargoParty(0, self.cargo_type_id.text(), self.party_weight.text(), self.party_time_in.text(),
                                self.warehouse_id.text(), self.party_time_out.text(), self.owner_name.text())
        cargoparty.save()
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def mk(self, val):
        cargoparty = CargoParty()
        cargoparty.delete(val)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()


class StorageMethodsForm(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Способы хранения')
        self.resize(400, 400)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        storagemethods = StorageMethods()
        thead = ["id способа", "Способ хранения"]
        col_num = 0
        for val in thead:
            self.table.setItem(0, col_num, QTableWidgetItem(str(val)))
            col_num += 1
        self.data = storagemethods.getAll()
        row_num = 0
        for i in self.data:
            row_num += 1
            self.table.setRowCount((row_num + 1))
            col_num = 0
            for j in i:
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(j)))
                col_num += 1
            w = QWidget()
            s = str(i[0])
            p = MyButton('Удалить', w, s)
            p.s.connect(self.mk)
            self.table.setCellWidget(row_num, col_num, w)

        self.layout.addWidget(self.table)
        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        self.layout.addWidget(w)
        add_b = QPushButton('Добавить значение')
        self.type = QLineEdit()
        l.addWidget(self.type)
        l.addWidget(add_b)
        add_b.released.connect(self.addStorageMethods)

    def addStorageMethods(self):
        if self.type.text() == '':
            self.sup = SupportWindow('Заполните название', 0)
            self.sup.show()
            return False
        storagemethods = StorageMethods(0, self.type.text())
        storagemethods.save()
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()

    def mk(self, val):
        storagemethods = StorageMethods()
        storagemethods.delete(val)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()


#########################################################
#                                                       #
#                                                       #
#                                                       #
#         КЛАССЫ ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ ОКОН           #
#                                                       #
#                                                       #
#                                                       #
#########################################################


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # pass
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    def __init__(self, parent=None, data=None):
        # pass
        self.data = data
        super().__init__(parent, width=5, height=4, dpi=100)

    def compute_initial_figure(self, data=None):
        # pass
        for row in self.data:

            dates = [dt.datetime.fromtimestamp(ts) for ts in row[0]]
            xfmt = md.DateFormatter('%Y-%m-%d %H:%M')
            self.axes.xaxis.set_major_formatter(xfmt)
            self.axes.plot(dates, row[1], row[2], label=row[3])
            self.axes.legend()
            for label in self.axes.get_xmajorticklabels():
                label.set_rotation(20)
        # self.axes.hist([10,20], 5, normed=1, facecolor='g', alpha=0.75)


class GraphWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.setMainUi()
        self.resize(700, 500)

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        sc = MyStaticMplCanvas(self, self.data)
        self.layout.addWidget(sc)


class MyButton(QPushButton):
    s = pyqtSignal(str)

    def __init__(self, text, parent, val):
        super().__init__(text, parent)
        self.d = val

    def mouseReleaseEvent(self, e):
        QPushButton.mouseReleaseEvent(self, e)
        self.s.emit(self.d)


class SaveRowButton(QPushButton):
    s = pyqtSignal(str, str, int)

    def __init__(self, text, parent, id, st_id, row):
        super().__init__(text, parent)
        self.id = id
        self.st_id = st_id
        self.row = row

    def mouseReleaseEvent(self, e):
        QPushButton.mouseReleaseEvent(self, e)
        self.s.emit(self.id, self.st_id, self.row)


class SupportWindow(QWidget):
    signal = pyqtSignal(int)

    def __init__(self, text, type):
        self.text = text
        self.type = type
        super().__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setMainUi()

    def setMainUi(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        lbl = QLabel(self.text)
        self.layout.addWidget(lbl)
        widg = QWidget()
        self.layout.addWidget(widg)
        ok_b = QPushButton('Ok')
        deny_b = QPushButton('Отмена')
        ok_b.released.connect(self.confirm)
        deny_b.released.connect(self.deny)
        lo = QHBoxLayout()
        widg.setLayout(lo)
        if self.type == 1:
            lo.addWidget(ok_b)
        lo.addWidget(deny_b)

    def confirm(self):
        self.close()
        self.signal.emit(1)

    def deny(self):
        self.close()