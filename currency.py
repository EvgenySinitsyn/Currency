import numpy as np
import requests
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
from graph import parse_history
from bs4 import BeautifulSoup


class Ui_Currency(object):
    def setupUi(self, Currency):

        # Создание окна
        Currency.setObjectName("Currency")
        Currency.setWindowModality(QtCore.Qt.NonModal)
        Currency.resize(1300, 575)
        Currency.setUnifiedTitleAndToolBarOnMac(False)
        self.curr = 'USD'  # Начальная валюта для графика

        # Настройки окна
        self.centralwidget = QtWidgets.QWidget(Currency)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setFixedSize(1300, 575)
        self.label_white = QtWidgets.QLabel(self.centralwidget)

        # Кнопки USD EUR CNY
        font = QtGui.QFont()
        font.setPointSize(25)

        self.btn_USD = QtWidgets.QPushButton(self.centralwidget)
        self.btn_USD.setGeometry(QtCore.QRect(0, 70, 500, 145))
        self.btn_USD.setFont(font)
        self.btn_USD.setText("")
        self.btn_USD.setIcon(QtGui.QIcon("USDimg.png"))
        self.btn_USD.setIconSize(QtCore.QSize(110, 110))
        self.btn_USD.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_USD.setObjectName("btn_USD")
        self.btn_USD.setStyleSheet("background-color: white")

        self.btn_EUR = QtWidgets.QPushButton(self.centralwidget)
        self.btn_EUR.setGeometry(QtCore.QRect(0, 200, 500, 145))
        self.btn_EUR.setFont(font)
        self.btn_EUR.setText("")
        self.btn_EUR.setIcon(QtGui.QIcon("EURimg.png"))
        self.btn_EUR.setIconSize(QtCore.QSize(110, 110))
        self.btn_EUR.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_EUR.setObjectName("btn_EUR")
        self.btn_EUR.setStyleSheet("background-color: rgb(186, 197, 232);")

        self.btn_CNY = QtWidgets.QPushButton(self.centralwidget)
        self.btn_CNY.setGeometry(QtCore.QRect(0, 340, 500, 145))
        self.btn_CNY.setFont(font)
        self.btn_CNY.setText("")
        self.btn_CNY.setIcon(QtGui.QIcon("CNYimg.png"))
        self.btn_CNY.setIconSize(QtCore.QSize(110, 110))
        self.btn_CNY.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_CNY.setObjectName("btn_CNY")
        self.btn_CNY.setStyleSheet("background-color: rgb(242, 170, 148);")

        # Надпись над графиком
        self.label_graph_description = self.label_graph = QtWidgets.QLabel(self.centralwidget)
        self.label_graph_description.setStyleSheet("background-color: white")
        self.label_graph_description.setGeometry(QtCore.QRect(500, 0, 800, 40))
        self.label_graph_description.setFont(font)
        self.label_graph_description.setObjectName("label_graph_description")
        self.label_graph_description.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)
        self.label_graph_description.setText(f"График изменений курса {self.curr}")

        # Вывод графика
        self.label_graph = QtWidgets.QLabel(self.centralwidget)
        self.label_graph.setEnabled(True)
        self.label_graph.setGeometry(QtCore.QRect(500, 40, 800, 550))
        self.label_graph.setStyleSheet("")
        self.label_graph.setText("")
        self.label_graph.setPixmap(QtGui.QPixmap("graph.png"))
        self.label_graph.setScaledContents(True)
        self.label_graph.setWordWrap(False)
        self.label_graph.setObjectName("label_graph")
        self.label_graph.setFont(font)
        self.label_graph.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter)

        # Кнопка Обновить
        self.btn_update = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update.setGeometry(QtCore.QRect(300, 0, 200, 70))

        self.btn_update.setFont(font)
        self.btn_update.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_update.setObjectName("btn_update")

        # Виджет текущая дата
        font.setPointSize(20)
        self.label_datetime = QtWidgets.QLabel(self.centralwidget)
        self.label_datetime.setGeometry(QtCore.QRect(0, 0, 300, 70))
        self.label_datetime.setFont(font)
        self.label_datetime.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_datetime.setStyleSheet("background-color: rgb(208, 247, 208);")
        self.label_datetime.setAlignment(QtCore.Qt.AlignCenter)
        self.label_datetime.setObjectName("label_datetime")
        Currency.setCentralWidget(self.centralwidget)

        # Надпись около дат
        self.label_period_description = QtWidgets.QLabel(self.centralwidget)
        self.label_period_description.setEnabled(True)
        self.label_period_description.setGeometry(QtCore.QRect(0, 485, 210, 90))
        self.label_period_description.setStyleSheet("background-color: white")
        font.setPointSize(17)
        font.setWeight(60)
        self.label_period_description.setFont(font)
        self.label_period_description.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        self.label_period_description.setText("Выбрать период:  ")

        # Выбор даты начала и конца графика
        self.date_begin = QtWidgets.QDateEdit(self.centralwidget)
        self.date_begin.setGeometry(QtCore.QRect(210, 485, 145, 90))
        self.date_begin.setObjectName("date_begin")
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setWeight(60)
        self.date_begin.setFont(font)
        self.date_end = QtWidgets.QDateEdit(self.centralwidget)
        self.date_end.setGeometry(QtCore.QRect(355, 485, 145, 90))
        self.date_end.setObjectName("date_end")
        self.date_end.setFont(font)
        self.date_end.setDate(datetime.now())

        self.retranslateUi(Currency)
        QtCore.QMetaObject.connectSlotsByName(Currency)

        self.add_functions()

    def retranslateUi(self, Currency):
        parsed_data = self.parse()
        _translate = QtCore.QCoreApplication.translate
        Currency.setWindowTitle(_translate("Currency", "Currency"))
        self.btn_USD.setText(f"     USD = {parsed_data[0]} ₽")
        self.btn_EUR.setText(f"     EUR = {parsed_data[1]} ₽")
        self.btn_CNY.setText(f"     CNY = {parsed_data[2]} ₽")
        self.btn_update.setText(_translate("Currency", "Обновить"))
        self.label_datetime.setText(_translate("Currency", datetime.now().strftime("%d.%m.%Y %H:%M:%S")))

    def add_functions(self):
        """ Функции кнопок окна"""
        self.btn_update.clicked.connect(self.data_update)
        # self.btn_build_graph.clicked.connect(self.build_graph)
        self.btn_USD.clicked.connect(lambda: self.build_graph('USD'))
        self.btn_EUR.clicked.connect(lambda: self.build_graph('EUR'))
        self.btn_CNY.clicked.connect(lambda: self.build_graph('CNY'))

    def build_graph(self, curr):
        """ Построение графика """
        self.curr = curr
        self.label_graph_description.setText(f"График изменений курса {self.curr}")
        if self.date_begin.date() > self.date_end.date():
            return self.label_graph.setText("Введите корректные даты")
        date_begin = self.date_begin.text().replace('.', '/')
        date_end = self.date_end.text().replace('.', '/')
        data = parse_history(self.curr, date_begin, date_end)
        if isinstance(data, str):
            return self.label_graph.setText(data)

        plt.clf()
        plt.plot(data[1], data[0], linewidth=2, color='green')
        div = len(data[1]) // 5
        if div == 0:
            div = 1

        plt.xticks(np.arange(0, len(data[1]), div))
        plt.grid(True)
        plt.savefig('graph.png')
        self.label_graph.setPixmap(QtGui.QPixmap("graph.png"))

    def data_update(self):
        """ Обновление данных валют """
        _translate = QtCore.QCoreApplication.translate
        parsed_data = self.parse()
        self.label_datetime.setText(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        self.btn_USD.setText(f"     USD = {parsed_data[0]} ₽")
        self.btn_EUR.setText(f"     EUR = {parsed_data[1]} ₽")
        self.btn_CNY.setText(f"     CNY = {parsed_data[2]} ₽")

    def parse(self):
        """ Парсинг данных валют """
        try:
            page_usd = requests.get(
                'https://www.google.com/search?channel=fs&client=ubuntu&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB'
                '%D0%BB%D0%B0%D1%80%D0%B0 '
            )

            page_eur = requests.get(
                "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE&client=ubuntu&hs=0ta&channel=fs&sxsrf=ALiCzsbpyRhiymbqYo9OTyYc__WQrWhfnQ%3A1657697824177&ei=IHbOYoK1Co-QrgT2nrOwBA&ved=0ahUKEwiCxdHPrfX4AhUPiIsKHXbPDEYQ4dUDCA0&uact=5&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE&gs_lcp=Cgdnd3Mtd2l6EAMyCQgjECcQRhCCAjILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMggIABCABBDJAzoHCCMQsAMQJzoHCAAQRxCwAzoKCAAQRxCwAxDJAzoICAAQkgMQsAM6EgguEMcBENEDEMgDELADEEMYAToJCAAQgAQQChAqOgoIABCABBCHAhAUOgUIABCABDoHCAAQgAQQCjoMCCMQsQIQJxBGEIICOgoIABCxAxCDARAKOgcIABDJAxAKOgQIIxAnOhAIABCABBCHAhCxAxCDARAUSgQIQRgASgQIRhgAUJEJWIIfYM0naARwAXgAgAFFiAHCBJIBATmYAQCgAQHIAQvAAQHaAQQIARgI&sclient=gws-wiz"
            )

            page_cny = requests.get(
                "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D1%8F&client=ubuntu&channel=fs&sxsrf=ALiCzsZoWiM3dWY7n1zM_3jPWMweb1BC6g%3A1657698137559&ei=WXfOYqPSIeyPrgSw-qr4BA&oq=%D0%BA%D1%83%D1%80%D1%81+%D1%8E%D0%B0%D0%BD%D1%8F&gs_lcp=Cgdnd3Mtd2l6EAEYADILCAAQgAQQsQMQgwEyBQgAEIAEMgUIABCABDIFCAAQgAQyCwgAEIAEELEDEIMBMgoIABCABBCHAhAUMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoHCAAQRxCwAzoHCAAQsAMQQzoECCMQJzoQCAAQgAQQhwIQsQMQgwEQFDoJCCMQJxBGEIICSgQIQRgASgQIRhgAUJgGWJgNYKUZaAFwAXgAgAFIiAGBApIBATSYAQCgAQHIAQrAAQE&sclient=gws-wiz")

            soup_usd = BeautifulSoup(page_usd.text, 'html.parser')
            convert_usd = soup_usd.find_all("div", {"class": "BNeawe iBp4i AP7Wnd"})
            usd_txt = str(convert_usd[1].text[:5])
            usd_txt = usd_txt.replace(',', '.')

            soup_eur = BeautifulSoup(page_eur.text, 'html.parser')
            convert_eur = soup_eur.find_all("div", {"class": "BNeawe iBp4i AP7Wnd"})
            eur_txt = str(convert_eur[1].text[:5])
            eur_txt = eur_txt.replace(',', '.')

            soup_cny = BeautifulSoup(page_cny.text, 'html.parser')
            convert_cny = soup_cny.find_all("div", {"class": "BNeawe iBp4i AP7Wnd"})
            cny_txt = str(convert_cny[1].text[:5])
            cny_txt = cny_txt.replace(',', '.')
        except:
            usd_txt = 'Нет интернета'
            eur_txt = 'Нет интернета'
            cny_txt = 'Нет интернета'

        return usd_txt, eur_txt, cny_txt


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Currency = QtWidgets.QMainWindow()
    ui = Ui_Currency()
    ui.setupUi(Currency)
    Currency.show()
    sys.exit(app.exec_())
