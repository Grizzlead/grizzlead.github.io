from PyQt6 import QtWidgets
import sys, datetime

def on_clicked():
    print(calendar.selectedDate().toPyDate())

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Класс QCalendarWidget")
window.resize(300, 400)
calendar = QtWidgets.QCalendarWidget()
calendar.setSelectedDate(datetime.date.today())
button = QtWidgets.QPushButton("Вывести значение")
button.clicked.connect(on_clicked)
button1 = QtWidgets.QPushButton("К выбранной дате")
button1.clicked.connect(calendar.showSelectedDate)
button2 = QtWidgets.QPushButton("К текущей дате")
button2.clicked.connect(calendar.showToday)
button3 = QtWidgets.QPushButton("Предыдущий месяц")
button3.clicked.connect(calendar.showPreviousMonth)
button4 = QtWidgets.QPushButton("Следующий месяц")
button4.clicked.connect(calendar.showNextMonth)
button5 = QtWidgets.QPushButton("Предыдущий год")
button5.clicked.connect(calendar.showPreviousYear)
button6 = QtWidgets.QPushButton("Следующий год")
button6.clicked.connect(calendar.showNextYear)
box = QtWidgets.QVBoxLayout()
box.addWidget(calendar)
box.addWidget(button)
box.addWidget(button1)
box.addWidget(button2)
box.addWidget(button3)
box.addWidget(button4)
box.addWidget(button5)
box.addWidget(button6)
window.setLayout(box)
window.show()
sys.exit(app.exec())
