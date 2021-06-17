# This Python file uses the following encoding: utf-8
import sys
import os


from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QPushButton, QMessageBox, QTableWidgetItem, QTableWidget, QHeaderView
from PyQt5.QtCore import Qt, QFile, QRect, QSize, QDateTime, QDate, QTime
from PyQt5.QtGui import QIcon, QKeySequence, QColor, QBrush, QFont
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalDelegate, QSqlRelationalTableModel, QSqlTableModel
import sqlite3


# Connexion à la base des données
connexion = sqlite3.connect('idatabase.db')
curseur = connexion.cursor()

class ModifierUtilisateur(QWidget):
    def __init__(self,parent=None):
        super(ModifierUtilisateur, self).__init__(parent, Qt.Window)
        loadUi("window_modification_client.ui",self)

        self.setWindowModality(Qt.WindowModal)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)


        # Signal et Slot pour le bouton d'enregistrement des fournisseurs
        #self.bouton_enregistrer_livraison.clicked.connect(self.enregistrer_modification_livraison)

    #def enregistrer_modification_livraison(self):
        #"""Fonction permettant l'enregistrement des modification des fournisseurs"""

if __name__ == "__main__":
    app = QApplication([])
    modifier_utilisateur = ModifierUtilisateur()
    modifier_utilisateur.show()
    sys.exit(app.exec)
#     pass


