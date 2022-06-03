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
        # КЛАССЫ ВСПОМОГАТЕЛЬНЫХ ОКОН ( ОКНА ВЫЗЫВАЕМЫЕ ИЗ ГЛАВНОГО ОКНА )
        # КЛАССЫ ИСПОЛНЯЕМЫХ ОКОН ( ОКНА СОДЕРЖАЩИЕ ДАННЫЕ ВЫЗЫВАЕМЫЕ ИЗ БД )
        # КЛАССЫ ВСПОМОГАЛТЕЛЬНЫХ ФУНКЦИЙ ОКОН ( ДОБАВИТЬ, УДАЛИТЬ, ИЗМЕНИТЬ ЗАПИСИ)

"""
# ГЛАВНОЕ ОКНО

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
        b3 = QPushButton('(не работает)Оборудование')
        b4 = QPushButton('(не работает)Рабочие')
        b5 = QPushButton('(не работает)Т/С')
        b6 = QPushButton('(не работает)Грузы')
        self.layout.addWidget(b1)
        self.layout.addWidget(b2)
        self.layout.addWidget(b3)
        self.layout.addWidget(b4)
        self.layout.addWidget(b5)
        self.layout.addWidget(b6)
        # b1.released.connect(self.openTechnologyCard)
        b2.released.connect(self.openInfrastructureWindow)
        # b3.released.connect(self.openEquipment)
        # b4.released.connect(self.openWorkers)
        # b5.released.connect(self.openVehicle)
        b6.released.connect(self.openCargo)

    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)

    # def openTechnologyCard(self):
    #     self.techF = TechnologyCardForm()
    #     self.techF.show()

    def openInfrastructureWindow(self):
        self.structF = InfrastructureWindow()
        self.structF.show()

    # def openEquipment(self):
    #     self.equipF = EquipmentForm()
    #     self.techF.show()
    #
    # def openWorkers(self):
    #     self.workF = WorkersForm()
    #     self.workF.show()
    #
    # def openVehicle(self):
    #     self.vehicleF = VehicleForm()
    #     self.vehicleF.show()
    #
    def openCargo(self):
        self.cargoF = CargoTypeForm()
        self.cargoF.show()


# class TechnologyCardForm(QWidget):
#     signal = pyqtSignal(str)
#
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('РТК')

# КЛАССЫ ВСПОМОГАТЕЛЬНЫХ ОКОН

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


# class EquipmentForm(QWidget):
#     signal = pyqtSignal(str)
#
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('РТК')
#
#
# class WorkersForm(QWidget):
#     signal = pyqtSignal(str)
#
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('РТК')
#
#
# class VehicleForm(QWidget):
#     signal = pyqtSignal(str)
#
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('РТК')
#
#
# class CargoForm(QWidget):
#     signal = pyqtSignal(str)
#
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('РТК')


# КЛАССЫ ИСПОЛНЯЕМЫХ ОКОН
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


# КЛАССЫ ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ ОКОН
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