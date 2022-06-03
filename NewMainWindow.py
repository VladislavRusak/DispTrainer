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

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Логистика")
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)

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

    def openEquipment(self):
        self.equipF = EquipmentWindow()
        self.equipF.show()

    def openWorkers(self):
        self.workF = WorkersWindow()
        self.workF.show()

    def openVehicle(self):
        self.vehicleF = VehicleWindow()
        self.vehicleF.show()

    def openCargo(self):
        self.cargoF = CargoWindow()
        self.cargoF.show()


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

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Инфраструктура')
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('Причалы')
        b2 = QPushButton('Склады')
        b3 = QPushButton('---Ж/Д пути---')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        self.layout.addWidget(b3)
        b1.released.connect(self.openDocCharManagementForm)
        b2.released.connect(self.openStorageCapManagmentForm)
        # b3.released.connect(self.DocCharManagementForm)

    def openDocCharManagementForm(self):
        self.docF = DocCharManagementForm()
        self.docF.show()

    def openStorageCapManagmentForm(self):
        self.storageF = StorageCapManagementForm()
        self.storageF.show()


class EquipmentWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оборудование")
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('Краны')
        b2 = QPushButton('Вспом.Техника')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        b1.released.connect(self.openCransForm)
        # b2.released.connect(self.openOtherEquipForm)

    def openCransForm(self):
        self.cransF = CranManagementForm()
        self.cransF.show()

    # def openOtherEquipForm(self):
    #     self.equipF = OtherEquipmqntForm()
    #     self.equipF.show()





class WorkersWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Работники')
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('Квалификации')
        b2 = QPushButton('Работники')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
    #     b1.released.connect(self.openQualificationsForm)
    #     b2.released.connect(self.openWorkersForm)

    # def openQualificationsForm(self):
    #     # self.qualificationF = QualificationsForm()
    #     # self.qualificationF.show()

    # def openWorkersForm(self):
    #     # self.workersF = WorkersForm()
    #     # self.workersF.show()


class VehicleWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Транспорт')
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('Суда')
        b2 = QPushButton('ЖД составы')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        # b1.released.connect(openShipsForm)
        # b2.released.connect(openTrainsForm)

    # def openShipsForm(self):
    #     self.shipsF = ShipsForm()
    #     self.shipsF.show()

    # def openTrainsForm(self):
    #     self.trainsF = TrainsForm()
    #     self.trainsF.show()

class CargoWindow(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('РТК')
        self.setMainUi()
        self.setGeometry(300, 300, 200, 300)

    def setMainUi(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(self.layout)
        b1 = QPushButton('Грузовая партия')
        b2 = QPushButton('Типы грузов')
        b3 = QPushButton('Способы хранения')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        self.layout.addWidget(b3)
        # b1.released.connect()
        # b2.released.connect()
        # b3.released.connect()


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
            w = QWidget
            s = str(i[0])
            p = MyButton('Удалить', w, s)
            p.s.connect(self.mk)
            self.table.setCellWidget(row_num, col_num, w)

        self.layout.addWidget(self.table)
        w = QWidget()
        l = QHBoxLayout()
        w.layout(l)
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
        qw = QWidget
        qw.setLayout(self.layout)
        self.setMainUi()

    def mk(self, value):
        cargo = Cargo()
        cargo.delete(value)
        qw = QWidget()
        qw.setLayout(self.layout)
        self.setMainUi()


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
                        tmp = s.find(str(row[4]))
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
        w.val5 = QLineEdit()
        w.val5.setText(str(c[0][5]))
        w.l.addRow(QLabel('Производительность при работе с подвозом груза т/смена (Чугун, брикеты)'), w.val5)
        w.val6 = QLineEdit()
        w.val6.setText(str(c[0][6]))
        w.l.addRow(QLabel('Производительность при работе с ж/д составом вагон/смена и т/смена (уголь)'), w.val6)
        w.val7 = QLineEdit()
        w.val7.setText(str(c[0][7]))
        w.l.addRow(QLabel('Производительность при работе с ж/д составом вагон/смена и т/смена (Чугун, брикеты)'),
                   w.val7)
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