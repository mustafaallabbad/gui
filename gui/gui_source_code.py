from PySide2.QtWidgets import *
import sys
from PySide2.QtGui import *
import PySide2.QtCore as QtCore
import pyqtgraph as pg
import numpy as np
def insert (source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]


#equation = input("please enter the function to be plotted : ")
class Window(QWidget):
    def __init__(self):

        super().__init__()
        self.setWindowTitle("Analog Design Tool (ADT) ")
        self.setGeometry(700, 200, 700, 500)
        self.quit_push_btn()
        equation_label = QLabel(self)
        equation_label.setText("Enter the function here : ")
        equation_label.move(10, 200)
        equation_label.setFont(QFont('Times', 10))
        self.equation_text_box = QLineEdit(self)
        self.equation_text_box.move(170, 200)
        self.equation_text_box.setFixedWidth(300)
        #range_label = QLabel(self)
        #range_label.setText("Enter the range")
        #range_label.move(0, 300)
        #range_label.setFont(QFont('Times', 9))
        from_label = QLabel(self)
        from_label.setText("From")
        from_label.move(10, 250)
        from_label.setFont(QFont('Times', 10))
        self.from_text_box = QLineEdit(self)
        self.from_text_box.move(50, 250)
        self.from_text_box.setFixedWidth(50)
        to_label = QLabel(self)
        to_label.setText("To")
        to_label.move(115, 250)
        to_label.setFont(QFont('Times', 10))
        self.to_text_box = QLineEdit(self)
        self.to_text_box.move(150, 250)
        self.to_text_box.setFixedWidth(50)
        self.plot_push_btn()
        self.about_push_btn()
        self.window_icon()
        self.inside_icon()
        self.help_push_btn()
        self.status_suc = QLabel(self)
        self.status_fail = QLabel(self)
        #self.setStyleSheet('background-color: blue;')
    def quit_push_btn(self):
        self.quit_btn = QPushButton("exit", self)
        self.quit_btn.move(500, 400)
        self.quit_btn.clicked.connect(self.quit_App)
    def quit_App(self):
        exit_input = QMessageBox.question(self,"Yes or No", "Are you sure you want to exit",
                                        QMessageBox.Yes | QMessageBox.No)
        if exit_input == QMessageBox.Yes:
            App.quit()
        elif exit_input == QMessageBox.No:
            pass

    def plot_push_btn(self):
        self.enter_btn = QPushButton("plot", self)
        self.enter_btn.setFixedWidth(220)
        self.enter_btn.move(250, 250)
        self.enter_btn.clicked.connect(self.evaluate)

    def about_push_btn(self):
        self.about_btn = QPushButton("About", self)
        self.about_btn.move(300, 400)
        self.about_btn.clicked.connect(self.aboutBox)

    def aboutBox(self):
        about_text = "ADT is a program that uses systematic analog design to provide a tool used in circuit simulation"
        QMessageBox.about(self.about_btn, "About ADT", about_text)
    def help_push_btn(self):
        self.help_btn = QPushButton("Help", self)
        self.help_btn.move(100, 400)
        self.help_btn.clicked.connect(self.helpBox)
    def helpBox(self):
        help_text = "Valid inputs:\n-Enter a function of variable (x) \n-Enter the minimum value of x \n-Enter the maximum value of x\nSupported Functions:\n-Polynomial functions,exponential functions,sinusoidal functions\nFunction formats:\n-Polynomial functions (a1*x^n1+a2*x^n2+--)\n-Sinusoidal Functions: sin(x),cos(x),tan(x)\n-Exponential functions: exp(x)"
        QMessageBox.about(self.help_btn, "Help", help_text)

    def evaluate(self):
        try:
            self.equation = self.equation_text_box.text()
            self.min_val = self.from_text_box.text()
            self.max_val = self.to_text_box.text()
            step = 50*abs(float(self.min_val)-float(self.max_val))
            if step > 0 :
                step_verified = int(step)
            elif step <= 0:
                step_verified = 100
            print(self.min_val)
            x = np.linspace(float(self.min_val), float(self.max_val), step_verified)
            counter = 0
            arr_var = []
            flag = 0
            equation_mod = self.equation + '+'
            equation_mod = equation_mod.replace("sin", "np.sin")
            equation_mod = equation_mod.replace("cos", "np.cos")
            equation_mod = equation_mod.replace("tan", "np.tan")
            equation_mod = equation_mod.replace("exp", "np.exp")
            for index in range(len(equation_mod)):
                if equation_mod[index] == 'x':
                    flag = 1
                if equation_mod[index] == '^':

                    for c in range(index, len(equation_mod)):
                        if equation_mod[c] == '+' or equation_mod[c] == '-' or equation_mod[c] == '*' or equation_mod[
                            c] == '/':
                            equation_mod = insert(equation_mod, ')', c)
                            break
            for index in range(len(equation_mod)):
                new_eq = equation_mod.replace('x^', 'pow(x,')
            final_equation = new_eq[:len(new_eq) - 1]
            if flag == 1:
                y = eval(final_equation)
            elif flag == 0:
                y = np.linspace(eval(final_equation), eval(final_equation), step_verified)

            self.status_fail.clear()
            self.status_suc = QLabel(self)
            self.status_suc.setText("<font color='green'>Successful</font>")
            self.status_suc.move(100, 350)
            self.status_suc.show()
            pg.plot(x, y)
            #pg.show()
        except:
            self.status_suc.clear()
            self.status_fail = QLabel(self)
            self.status_fail.setText("<font color='red'>Invalid input</font>")
            self.status_fail.move(100, 350)
            self.status_fail.show()

    def window_icon(self):
        icon = QIcon(".img//outside_icon .png")
        self.setWindowIcon(icon)

    def inside_icon(self):
        icon1 = QIcon(".img//inside_icon.png")
        label1 = QLabel('Sample', self)
        pixmap1 = icon1.pixmap(100, 100, QIcon.Active, QIcon.On)
        label1.setPixmap(pixmap1)

App = QApplication(sys.argv)
window = Window()
window.show()
App.exec_()
sys.exit(0)
