from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qdarktheme
import sys

from login import main_login,toggle_theme

import MySQLdb

from PyQt5.uic import loadUiType

ui, _ = loadUiType("library.ui")
light = True


# TODO Create a global variable to handle user and admin, like is_admin, regler le pb avec les combo box et continuer avec la 1ere page




class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.fill_book_db()
        self.handle_ui_changes()
        self.handle_buttons()
        self.show_category()
        self.show_language()
        self.show_category_and_language_combo_box()

    def fill_book_db(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        insert_query = '''
        INSERT INTO book (title, author, category, available, number_of_pages,description,language)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        book_list = [
            ("To Kill a Mockingbird", "Harper Lee", "Fiction", 1, 336,
             "A classic novel tackling issues of race and morality in the American South.", "English"),
            ("1984", "George Orwell", "Fiction", 1, 328,
             "A dystopian masterpiece exploring surveillance and totalitarianism.", "English"),
            ("Pride and Prejudice", "Jane Austen", "Fiction", 1, 432,
             "A timeless tale of love and social norms in Regency-era England.", "English"),
            ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1, 180,
             "A vivid portrayal of the Jazz Age's excesses and the American Dream.", "English"),
            ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 1, 320,
             "The magical start to a beloved series about a young wizard's adventures.", "English"),
            ("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1, 1178,
             "An epic journey through a world of hobbits, elves, and dark forces.", "English"),
            ("The Catcher in the Rye", "J.D. Salinger", "Fiction", 1, 277,
             "A coming-of-age story capturing the disillusionment of a teenage boy.", "English"),
            ("Animal Farm", "George Orwell", "Fiction", 1, 112,
             "A satirical allegory illustrating the dangers of political power struggles.", "English"),
            ("Brave New World", "Aldous Huxley", "Fiction", 1, 288,
             "A futuristic society explores themes of technology, conformity, and free will.", "English"),
            ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1, 310,
             "A charming adventure featuring a hobbit on a quest for treasure.", "English"),
            ("The Da Vinci Code", "Dan Brown", "Mystery", 1, 592,
             "A gripping thriller unraveling cryptic codes and historical secrets.", "English"),
            ("The Hunger Games", "Suzanne Collins", "Young Adult", 1, 374,
             "In a dystopian world, a fight for survival unfolds in a televised arena.", "English"),
            ("The Alchemist", "Paulo Coelho", "Fiction", 1, 208,
             "A philosophical journey of self-discovery and the pursuit of dreams.", "English"),
            ("Fahrenheit 451", "Ray Bradbury", "Science Fiction", 1, 249,
             "In a future society, firemen burn books to control knowledge and ideas.", "English"),
            ("Gone with the Wind", "Margaret Mitchell", "Fiction", 1, 960,
             "A sweeping historical romance set against the backdrop of the Civil War.", "English"),
        ]

        self.cursor.executemany(insert_query, book_list)
        self.db.commit()
        print("Data insertion successful.")

    def handle_ui_changes(self):
        self.tabWidget.tabBar().setVisible(False)

    def handle_buttons(self):
        self.dayBtn.clicked.connect(self.open_day_to_day_tab)
        self.themeBtn.clicked.connect(toggle_theme)

        self.deleteBook.clicked.connect(self.delete_book)
        self.bookBtn.clicked.connect(self.open_books_tab)
        self.userBtn.clicked.connect(self.open_users_tab)
        self.settingBtn.clicked.connect(self.open_settings_tab)
        # operations
        self.saveBtn.clicked.connect(self.add_new_book)
        self.addUserBtn.clicked.connect(self.add_new_user)
        self.saveChangesUser.clicked.connect(self.update_user)
        self.searchBtn.clicked.connect(self.search_book)
        self.loginBtn.clicked.connect(self.edit_user)
        # self.loginBtn.clicked.connect(self.update_user)
        self.addCategory.clicked.connect(self.add_category)
        self.addLang.clicked.connect(self.add_language)
        self.saveChanges.clicked.connect(self.edit_book)

    #####################################################
    ############### opening tabs ######################

    def open_day_to_day_tab(self):
        # TODO Add the different actions(delete,update,add) to the first window, change the icon and the title of the app, possibility to rent a book
        self.tabWidget.setCurrentIndex(0)

    def open_books_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(3)

    #####################################################
    ############### book operations ######################

    def add_new_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        book_title = self.book_title.text()
        book_author = self.book_author.text()
        category = self.category_combo.currentText()
        available = 0 if self.available_combo.currentText() == 'False' else 1
        pages = int(self.pages.text())
        description = self.description.toPlainText()
        language = self.language_combo.currentText()

        self.cursor.execute('''
            INSERT INTO book (title, author, category, available, number_of_pages, description, language)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (book_title, book_author, category, available, pages, description, language))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage("Book added successfully")

    def search_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        book_title = self.title_search.text()
        self.cursor.execute('''
        SELECT * FROM book WHERE title = (%s)
        ''', (book_title,))

        data = self.cursor.fetchall()
        # print(data)
        self.pagesEdit.setText(str(data[0][5]))
        self.titleEdit.setText(data[0][1])
        self.authorEdit.setText(data[0][2])
        self.descriptionEdit.setPlainText(data[0][6])
        self.categoryEdit.addItem(data[0][3])
        self.categoryEdit.setCurrentText(data[0][3])
        print("--------> : ",data[0][3],data[0][7])
        self.language_combo_2.addItem(data[0][7])
        self.language_combo_2.setCurrentText(data[0][7])
        self.availableEdit.setCurrentText("True" if data[0][4] == 1 else "False")
        self.db.commit()
        self.db.close()

    def edit_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()
        book_title = self.title_search.text()
        self.cursor.execute('''
                SELECT * FROM book WHERE title = (%s)
                ''', (book_title,))

        data = self.cursor.fetchall()

        update_query = '''
                    UPDATE book
                    SET title = %s, author = %s, category = %s,available = %s, number_of_pages = %s, description = %s, language=%s
                    WHERE title = %s'''

        pages = self.pagesEdit.text()

        title = self.titleEdit.text()
        author = self.authorEdit.text()
        description = self.descriptionEdit.toPlainText()
        category = self.categoryEdit.currentText()
        language = self.language_combo_2.currentText()
        print(self.availableEdit.currentText())
        available = 0 if self.availableEdit.currentText() == 'False' else 1

        self.cursor.execute(update_query, (title, author, category, available, int(pages), description, language,
                                           data[0][1],))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage("Book has been updated successfully!")

    def delete_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()
        book_title = self.title_search.text()
        delete_query = "DELETE FROM book WHERE title = %s"
        self.cursor.execute(delete_query, (book_title,))

        self.db.commit()
        self.db.close()
        self.statusBar().showMessage("The book has been deleted successfully!")

    #####################################################
    ############### user operations ######################

    def add_new_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        username = self.username.text()
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirmPassword.text()

        self.cursor.execute('''
                       SELECT * FROM users WHERE username = (%s)
                       ''', (username,))
        user=self.cursor.fetchone()

        if user:
            # open a dialog box to say that the username is already taken
            pass
        else:
            if username and email and password and confirm_password and password == confirm_password:
                self.cursor.execute('''
                            INSERT INTO users (username, password, email)
                            VALUES (%s, %s, %s)
                            ''', (username, password, email))
                self.db.commit()
                self.db.close()
                self.statusBar().showMessage("The user has been added successfully!")
            else:
                # Open the dialog box with the message
                print("Please don't create problem")

    # TODO Finish with the login functionality


    def edit_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        username = self.username2.text()
        password = self.password2.text()

        self.cursor.execute('''
                               SELECT * FROM users WHERE username = (%s) AND password= (%s)
                               ''', (username, password,))
        user = self.cursor.fetchone()
        #print(user)
        if user:
            change_visibility = [self.username3, self.password3, self.email2, self.confirmPassword2,
                                 self.saveChangesUser]

            for obj in change_visibility:
                obj.setEnabled(True)

            self.username3.setText(user[1])
            self.password3.setText(user[2])
            self.email2.setText(user[3])
            self.confirmPassword2.setText(user[2])
        else:
            print("Please don't create problem")

    def update_user(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        new_username = self.username3.text()
        new_email = self.email2.text()
        new_password = self.password3.text()
        new_confirm_password = self.confirmPassword2.text()

        username = self.username2.text()
        email = self.email.text()
        update_query = '''UPDATE users
                          SET username = %s , password= %s, email=%s
                          WHERE username = %s'''

        if new_username and new_email and new_password and new_confirm_password:
            self.cursor.execute(update_query, (new_username, new_password, new_email, username,))
            self.db.commit()
            self.db.close()
            change_visibility = [self.username3, self.password3, self.email2, self.confirmPassword2,
                                 self.saveChangesUser]

            for obj in change_visibility:
                obj.setEnabled(False)
            self.statusBar().showMessage("The user has been updated successfully!")
        else:
            print("Please don't create problem")

    #####################################################
    ############### opening tabs ######################

    def add_category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        category_name = self.categoryName.text()

        self.cursor.execute('''
        INSERT INTO category (category_name) VALUES (%s)
        ''', (category_name,))

        self.db.commit()
        self.show_category()
        self.categoryName.setText("")
        self.statusBar().showMessage("Done adding category!")

    def show_category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        self.cursor.execute('''
        SELECT category_name FROM category
        ''')

        data = self.cursor.fetchall()
        if data:
            self.categoryWidget.setRowCount(0)
            self.categoryWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    # print(column, row, form, item)
                    self.categoryWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.categoryWidget.rowCount()
                self.categoryWidget.insertRow(row_position)
        self.db.commit()
        self.db.close()

    def add_language(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        language = self.langName.text()

        self.cursor.execute('''
                INSERT INTO language (language_name) VALUES (%s)
                ''', (language,))

        self.db.commit()
        self.langName.setText("")
        self.show_language()
        # print("Done adding language!")
        self.statusBar().showMessage("Done adding language!")

    def show_language(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        self.cursor.execute('''
         SELECT language_name FROM language
         ''')

        data = self.cursor.fetchall()
        if data:
            self.langWidget.setRowCount(0)
            self.langWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    # print(column, row, form, item)
                    self.langWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.langWidget.rowCount()
                self.langWidget.insertRow(row_position)
        self.db.commit()
        self.db.close()
    #####################################################
    ########### show settings in all combobox ###########

    def show_category_and_language_combo_box(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456789', db='library')
        self.cursor = self.db.cursor()

        self.cursor.execute('''SELECT category_name FROM category''')

        data = self.cursor.fetchall()

        for category in data:
            self.categoryEdit.addItem(category[0])
            print(category)
        self.cursor.execute('''SELECT language_name FROM language''')
        data = self.cursor.fetchall()
        for language in data:
            self.language_combo_2.addItem(language[0])
        self.db.commit()
        self.db.close()




def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    login_=main_login()
    if login_:
        main()
    else:
        pass
# run this inside the terminal to avoid the error caused by the .qrc file :

# pyrcc5 icons.qrc -o icons_rc.py
