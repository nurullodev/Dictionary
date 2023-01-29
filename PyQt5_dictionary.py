from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import sys
import json

class MyDictionary(QMainWindow):
     count = 0
     uzbek_angliz =[]
     uzbList = []
     angList = []
     def __init__(self):
          super().__init__()
          self.mainWindow()
          self.openJson()
          self.changeLanguage()
          self.wordTranslation('')
          self.showWords(self.uzbList)

     def openJson(self):
          with open("uzb_ang.json") as file:
               data1 = json.load(file)
               for item in data1:
                    self.uzbek_angliz.append(item)
                    for value in item.values():
                         self.angList.append(value)
                    for key in item.keys():
                         self.uzbList.append(key)
               self.angList.sort() 
               self.uzbList.sort() 
               
     def mainWindow(self):
          self.setFixedSize(500,600)
          self.setStyleSheet("background-color:purple;")
          
          self.radio1 = QRadioButton(self)
          self.radio1.move(115,50)
          self.radio1.clicked.connect(self.checkRadioButton)

          self.btnInRadio1 = QLabel("add 📝",self)
          self.btnInRadio1.setGeometry(20,50,90,30)
          self.btnInRadio1.setStyleSheet("background-color:green;")
          self.btnInRadio1.setFont(QFont('Arial',14))

          self.btnOnAdd = QPushButton("Add the new world",self)
          self.btnOnAdd.setGeometry(175,230,160,55)
          self.btnOnAdd.setFont(QFont('Arial',14))
          self.btnOnAdd.setStyleSheet("background-color:green;")
          self.btnOnAdd.setEnabled(False)
          self.btnOnAdd.clicked.connect(self.addNewWord)
          
          self.radio2 = QRadioButton(self)
          self.radio2.move(360,50)
          self.radio2.clicked.connect(self.checkRadioButton)

          self.bntInRadio2 = QLabel("🔍search",self)
          self.bntInRadio2.setGeometry(380,50,90,30)
          self.bntInRadio2.setFont(QFont('Arial',14))
          self.bntInRadio2.setStyleSheet("background-color:blue;")

          self.input1 = QLineEdit(self)
          self.input1.setGeometry(20,140,150,60)
          self.input1.setFont(QFont('Arial',14))
          self.input1.setStyleSheet("background-color:white;")
          self.input1.textChanged.connect(self.findWords) 

          self.buttonChange = QPushButton("⏪⏩",self)
          self.buttonChange.setGeometry(200,135,100,75)
          self.buttonChange.setFont(QFont('Arial',24))
          self.buttonChange.clicked.connect(self.changeLanguage)

          self.input2 = QLineEdit(self)
          self.input2.setGeometry(330,140,150,60)
          self.input2.setFont(QFont('Arial',14))
          self.input2.setStyleSheet("background-color:white;")

          self.ListVue = QListWidget(self)
          self.ListVue.setGeometry(20,300,150,290)
          self.ListVue.setFont(QFont('Arial',14))
          self.ListVue.setStyleSheet("background-color:white;")
          self.ListVue.itemClicked.connect(self.setMainText)
          self.ListVue.itemClicked.connect(self.wordTranslation)
     
     def showWords(self,uzb_ang):
          self.ListVue.clear()
          for item in uzb_ang:
               self.ListVue.addItem(item)

     def changeLanguage(self):
          self.input1.clear()
          self.input2.clear()
          if self.count%2==0:
               self.input1.setPlaceholderText('Uzbek')
               self.input2.setPlaceholderText('English')
               self.showWords(self.uzbList)
          else:
               self.input2.setPlaceholderText('Uzbek')
               self.input1.setPlaceholderText('English')
               self.showWords(self.angList)
          self.count+=1
          
     def checkRadioButton(self):
          if self.radio1.isChecked():
               self.btnOnAdd.setEnabled(True)
          elif self.radio2.isChecked():
               self.btnOnAdd.setEnabled(False) 

     def findWords(self):
          newListWords = []
          if self.count%2==0:
               for item in self.angList:
                    if self.input1.text().lower() in item.lower():
                         newListWords.append(item)
          else:
               for item in self.uzbList:
                    if self.input1.text().lower() in item.lower():
                         newListWords.append(item)
          self.showWords(newListWords)

     def setMainText(self):
          word =""
          word = self.ListVue.currentItem().text()
          self.input1.setText(self.ListVue.currentItem().text())
          self.wordTranslation(word)

     def wordTranslation(self,word):
          for item in self.uzbek_angliz:
               if self.count%2!=0:
                    for key in item.keys():
                         if key==word:
                              self.input2.setText(item[key])
               else:
                    for key,value in item.items():
                         if word == value:
                              self.input2.setText(key)

     def addNewWord(self):
          if len(self.input1.text())!=0 and len(self.input2.text())!=0:
               if self.count%2!=0:
                    if {self.input1.text():self.input2.text()} not in self.uzbek_angliz:
                         self.uzbek_angliz.append({self.input1.text():self.input2.text()})
                         self.input1.clear()
                         self.input2.clear()
                    else:
                         thereWordMsg = QMessageBox()
                         thereWordMsg.setIcon(QMessageBox.Information)
                         thereWordMsg.setText('Error')
                         thereWordMsg.setInformativeText("There is such a word\nin the dictionary")
                         thereWordMsg.setFont(QFont('Arial',10))
                         thereWordMsg.exec_()
               else:
                    if {self.input2.text():self.input1.text()} not in self.uzbek_angliz:
                         self.uzbek_angliz.append({self.input2.text():self.input1.text()})
                    else:
                         thereWordMsg = QMessageBox()
                         thereWordMsg.setIcon(QMessageBox.Information)
                         thereWordMsg.setText('Error')
                         thereWordMsg.setInformativeText("There is such a word\nin the dictionary")
                         thereWordMsg.setFont(QFont('Arial',10))
                         thereWordMsg.exec_()
                         self.input1.clear()
                         self.input2.clear()
               with open("uzb_ang.json","w") as file:
                    json.dump(self.uzbek_angliz,file,indent='\t')
                    self.input1.clear()
                    self.input2.clear()
          else:
               lenMsg = QMessageBox()
               lenMsg.setIcon(QMessageBox.Critical)
               lenMsg.setInformativeText("Please enter \na word to input")
               lenMsg.setFont(QFont('Arial',10))
               lenMsg.exec_()
                                 
app = QApplication(sys.argv)
word = MyDictionary()
word.show()
sys.exit(app.exec_())
