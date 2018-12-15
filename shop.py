#!/usr/bin/python3

#TODO: QtMessageBox on checking data in adding smth
#TODO: Refreshing QComboBox by self.box_init()
#TODO: tableWidget->setColumnWidth(1,200);

import design, auth
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
from PyQt5.QtWidgets import QMessageBox

#from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QApplication
#from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class Authentification(QtWidgets.QDialog, auth.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ok_button.clicked.connect(self.ok)
        self.exit_button.clicked.connect(self.exit)
        self.log = ''
        self.pword = ''

    def ok(self):
            self.log = self.login.text()
            self.pword = self.password.text()

            self.accept()
            

    def exit(self):
        exit()

class ShopApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        auth = Authentification()
        auth.exec()
        

        self.db = QtSql.QSqlDatabase.addDatabase("QPSQL7")
        self.db.setHostName('127.0.0.1')
        #db.setPort(62534)
        self.db.setDatabaseName('shop')
        self.db.setUserName(auth.log)
        self.db.setPassword(auth.pword)
        
        if not self.db.open():
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль", QMessageBox.Ok)
            raise Exception("Error opening database: {}".format(self.db.lastError().text()))
        
        self.query = QtSql.QSqlQuery()

        self.customers_table()
        self.products_table()
        self.products_list_table()
        self.stocks_table()
        self.purchases_table()
        self.boxes_init()

        self.purchases_by_name_button.clicked.connect(self.button_sort_purchases)
        self.del_purchase_button.clicked.connect(self.button_purchase_del)
        self.add_purchase_button.clicked.connect(self.button_purchase_add)
        self.purchases_grid_refresh_button.clicked.connect(self.button_purchases_list_refresh)
        self.add_customer_button.clicked.connect(self.button_customer_add)
        self.customers_grid_refresh_button.clicked.connect(self.button_customers_refresh)
        self.del_customer_button.clicked.connect(self.button_customer_del)
        self.products_grid_refresh_button.clicked.connect(self.button_product_refresh)
        self.product_line_button.clicked.connect(self.button_product_add)
        self.del_product_button.clicked.connect(self.button_product_del)
        self.stock_grid_refresh_button.clicked.connect(self.button_stock_refresh)
        self.add_stock_button.clicked.connect(self.button_stock_add)
        self.del_stock_button.clicked.connect(self.button_stock_del)
        self.apply_admin_button.clicked.connect(self.button_admin_apply)

    def boxes_init(self):
        model_cc = QtSql.QSqlQueryModel()
        model_cc.setQuery("select name, id from customers order by name")
        customer_combo = self.customer_box
        customer_combo.setModel(model_cc)
        customer_combo.duplicatesEnabled = True

        model_sc = QtSql.QSqlQueryModel()
        model_sc.setQuery("select name, id from stocks order by name")
        stock_combo = self.stock_box
        stock_combo.setModel(model_sc)
        stock_combo.duplicatesEnabled = True

        model_cpc = QtSql.QSqlQueryModel()
        model_cpc.setQuery("select id from purchases order by id")
        choose_purchase_combo = self.choose_purchase_box
        choose_purchase_combo.setModel(model_cpc)
        choose_purchase_combo.duplicatesEnabled = True

        model_ccc = QtSql.QSqlQueryModel()
        model_ccc.setQuery("select name, id from customers order by name")
        choose_customer_combo = self.choose_customer_box
        choose_customer_combo.setModel(model_ccc)
        choose_customer_combo.duplicatesEnabled = True

        model_cprc = QtSql.QSqlQueryModel()
        model_cprc.setQuery("select name, id from products order by name")
        choose_product_combo = self.choose_product_box
        choose_product_combo.setModel(model_cprc)
        choose_product_combo.duplicatesEnabled = True

        model_csc = QtSql.QSqlQueryModel()
        model_csc.setQuery("select name, id from stocks order by name")
        choose_stock_combo = self.choose_stock_button
        choose_stock_combo.setModel(model_csc)
        choose_stock_combo.duplicatesEnabled = True

        model_sort = QtSql.QSqlQueryModel()
        model_sort.setQuery("select name, id from customers order by name")
        choose_sort = self.last_name_box
        choose_sort.setModel(model_sort)
        choose_sort.duplicatesEnabled = True

        self.products_list_table()


    def button_sort_purchases(self):
        name = self.last_name_box.model().record(self.last_name_box.currentIndex()).value(1)
        print(name)
        model = QtSql.QSqlQueryModel()

        model.setQuery("select purchases.id, customers.name, purchases.products, stocks.name, purchases.price from purchases inner join customers on purchases.customer = customers.id inner join stocks on purchases.stock = stocks.id where purchases.customer = {} order by purchases.id".format(name))
        model.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
        model.setHeaderData(1, QtCore.Qt.Horizontal, 'Имя покупателя')
        model.setHeaderData(2, QtCore.Qt.Horizontal, 'ID товаров')
        model.setHeaderData(3, QtCore.Qt.Horizontal, 'Скидка')
        model.setHeaderData(4, QtCore.Qt.Horizontal, 'Стоимость')
        view = self.purchases_grid_name
        view.setModel(model)
        view.resizeColumnsToContents()
        view.show()

    def button_purchases_list_refresh(self):
        #purchases_grid_refresh_button
        self.purchases_table()

    def button_purchase_add(self):
        #add_purchase_button
        name_index = self.customer_box.currentIndex()
        name = self.customer_box.model().record(name_index).value(1)

        stock = self.stock_box.currentText()
        id = 0
        price_reduction = 0
        
        self.query.exec("SELECT reduction, id FROM stocks WHERE name='{}'".format(stock))
        while(self.query.next()):
            stock = self.query.value(0)
            stock_id = self.query.value(1)
        
        products = self.products_indexes.text()
        products_indexes = self.products_indexes.text().split(",")
        cost = 0

        for index in products_indexes:
            self.query.exec("SELECT price FROM products WHERE id='{}'".format(index))
            while(self.query.next()):
                cost += self.query.value(0)
        if stock != 0:
            cost = cost - cost * stock / 100
        
        flag = True
        for id in products_indexes:
            try:
                flag = flag and type(int(id)) == int
            except ValueError:
                flag = False
        msg = 0
        if flag == False:
            msg = QMessageBox.critical(self, "Ошибка", "Неверно введены ID товаров", QMessageBox.Ok)

        if msg == QMessageBox.Ok:
            return -1

        request = "insert into purchases(customer, stock, products, price) values('{0}', '{1}', '{2}', '{3}')".format(name, stock_id, products, cost)
        self.query.exec(request)
        self.boxes_init()

    def button_purchase_del(self):
        #del_purchase_button
        index = self.choose_purchase_box.currentIndex()
        id = self.choose_purchase_box.model().record(index).value(0)
        request = "delete from purchases where id={}".format(id)
        self.query.exec(request)
        self.boxes_init()

    def button_customers_refresh(self):
        #customers_grid_refresh_button
        self.customers_table()

    def button_customer_add(self):
        #add_customer_button
        #query = QtSql.QSqlQuery()

        cnl = self.customer_name_line.text()
        al = self.adress_line.text()
        zl = self.zipcode_line.text()
        pl = self.passport_line.text()
        
        msg = 0

        if len(pl) < 10:
            msg = QMessageBox.critical(self, "Ошибка", "Введены неверные серия и номер паспорта (цифр меньше 10)", QMessageBox.Ok)
        if len(pl) > 10:
            msg = QMessageBox.critical(self, "Ошибка", "Введены неверные серия и номер паспорта (цифр больше 10)", QMessageBox.Ok)

        if len(zl) < 6:
            msg = QMessageBox.critical(self, "Ошибка", "Введен неверный индекс (цифр меньше 6)", QMessageBox.Ok)
        if len(zl) > 6:
            msg = QMessageBox.critical(self, "Ошибка", "Введен неверный индекс (цифр больше 6)", QMessageBox.Ok)

        if msg == QMessageBox.Ok:
            return -1

        request = "insert into customers(name, adress, passport, index) values('{0}', '{1}', '{2}', '{3}')".format(cnl, al, pl, zl)
        self.query.exec(request)
        self.boxes_init()
        

    def button_customer_del(self):
        #del_customer_button
        index = self.choose_customer_box.currentIndex()
        id = self.choose_customer_box.model().record(index).value(1)
        request = "delete from customers where id={}".format(id)
        self.query.exec(request)
        self.boxes_init()

    def button_product_refresh(self):
        #products_grid_refresh_button
        self.products_table()

    def button_product_add(self):
        #product_line_button
        pnl = self.product_name_line.text()
        pl = self.price_line.text()
        request = "insert into products(name, price) values('{0}', {1})".format(pnl, pl)
        self.query.exec(request)
        self.boxes_init()

    def button_product_del(self):
        #del_product_button
        index = self.choose_product_box.currentIndex()
        id = self.choose_product_box.model().record(index).value(1)
        request = "delete from products where id={}".format(id)
        self.query.exec(request)
        self.boxes_init()

    def button_stock_refresh(self):
        #stock_grid_refresh_button
        self.stocks_table()

    def button_stock_add(self):
        #add_stock_button
        prl = self.price_reduction_line.text()
        snl = self.stock_name_line.text()

        msg = 0

        if int(prl) < 0 or int(prl) > 100:
            msg = QMessageBox.critical(self, "Ошибка", "Размер скидки не попадает в диапазон [0; 100]", QMessageBox.Ok)

        if msg == QMessageBox.Ok:
            return -1

        request = "insert into stocks(name, reduction) values('{0}', {1})".format(snl, prl)
        self.query.exec(request)
        self.boxes_init()

    def button_stock_del(self):
        #del_stock_button
        index = self.choose_stock_button.currentIndex()
        id = self.choose_stock_button.model().record(index).value(1)
        request = "delete from stocks where id={}".format(id)
        self.query.exec(request)
        self.boxes_init()

    def button_admin_apply(self):
        #apply_admin_button
        al = self.admin_line.text()
        model = QtSql.QSqlQueryModel()
        model.setQuery("{}".format(al))
        view = self.admin_grid
        view.setModel(model)
        view.resizeColumnsToContents()
        view.show()

    def purchases_table(self):
        model = QtSql.QSqlQueryModel()
        
        model.setQuery("select purchases.id, customers.name, purchases.products, stocks.name, purchases.price from purchases inner join customers on purchases.customer = customers.id inner join stocks on purchases.stock = stocks.id order by purchases.id")
        model.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
        model.setHeaderData(1, QtCore.Qt.Horizontal, 'Имя покупателя')
        model.setHeaderData(2, QtCore.Qt.Horizontal, 'ID товаров')
        model.setHeaderData(3, QtCore.Qt.Horizontal, 'Скидка')
        model.setHeaderData(4, QtCore.Qt.Horizontal, 'Стоимость')
        
        view = self.purchases_grid
        view.setModel(model)
        view.resizeColumnsToContents()
        view.show()

    def products_table(self):
        model = QtSql.QSqlQueryModel()
        
        model.setQuery("select id, name, price from products order by name")
        model.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
        model.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
        model.setHeaderData(2, QtCore.Qt.Horizontal, 'Цена')
        
        view = self.product_grid
        view.setModel(model)
        view.resizeColumnsToContents()
        view.show()

    def products_list_table(self):
        model = QtSql.QSqlQueryModel()
        
        model.setQuery("select id, name from products order by name")
        model.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
        model.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')

        view = self.products_list_grid
        view.setModel(model)
        view.resizeColumnsToContents()
        view.show()

    def stocks_table(self):
        model = QtSql.QSqlQueryModel()
        
        model.setQuery("select id, name, reduction from stocks order by reduction")
        model.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
        model.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
        model.setHeaderData(2, QtCore.Qt.Horizontal, 'Уменьшение стоимости, %')
        
        view = self.stock_grid
        view.setModel(model)
        view.resizeColumnsToContents()
        view.show()

    def customers_table(self):
        model = QtSql.QSqlQueryModel()
        
        model.setQuery("select id, name, passport, index, adress from customers order by name")
        model.setHeaderData(0, QtCore.Qt.Horizontal, 'ID')
        model.setHeaderData(1, QtCore.Qt.Horizontal, 'ФИО')
        model.setHeaderData(2, QtCore.Qt.Horizontal, 'Паспорт')
        model.setHeaderData(3, QtCore.Qt.Horizontal, 'Индекс')
        model.setHeaderData(4, QtCore.Qt.Horizontal, 'Адрес')
        
        view = self.customers_grid
        view.setModel(model)
        view.resizeColumnsToContents()
        view.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ShopApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()