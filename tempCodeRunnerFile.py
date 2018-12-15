
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