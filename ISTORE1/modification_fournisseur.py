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

class ModifierFournisseur(QWidget):
    def __init__(self,parent=None):
        super(ModifierFournisseur, self).__init__(parent, Qt.Window)
        loadUi("window_modifier_fournisseur.ui",self)

        self.setWindowModality(Qt.WindowModal)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Modifier un fournisseur")
        self.setWindowIcon(QIcon("./icones/icone_fournisseur.ico"))

        # Signal et Slot pour le bouton d'enregistrement des fournisseurs
        self.bouton_enregistrer_fournisseur.clicked.connect(self.enregistrer_modification_fournisseur)

    def enregistrer_modification_fournisseur(self):
        """Fonction permettant l'enregistrement des modification des fournisseurs"""
        nom_du_fournisseur=self.edit_nom_fournisseur.text()
        num_tel_fournisseur= int(self.edit_num_fournisseur.text())
        email = self.edit_email_fournisseur.text()
        adresse= self.edit_adresse_fournisseur.text()
        type_marchandise= self.edit_type_marchandise.text()

        try:
            self.connexion = sqlite3.connect('idatabase.db')
            self.curseur = self.connexion.cursor()
            query = "SELECT * FROM liste_des_fournisseurs"
            resultat = curseur.execute(query)
            for row in enumerate(resultat):
                if row[0] == self.table_fournisseurs.currentRow():
                    data = row[1]
                    nom_du_fournisseur = data[1]
                    num_tel_fournisseur = data[2]
                    email = data[3]
                    adresse = data[4]
                    type_marchandise = data[5]
                    curseur.execute("UPDATE INTO liste_des_fournisseurs SET fournisseur=? AND num_telephone=? AND email=? AND adresse=? AND type_marchandise=? WHERE fournisseur=? AND num_telephone=? AND email=? AND adresse=? AND type_marchandise=?".format(nom_du_fournisseur,num_tel_fournisseur,email,adresse,type_marchandise))

            #self.curseur.execute("UPDATE INTO liste_des_fournisseurs SET fournisseur ='{}', num_telephone = '{}',email = '{}',adresse = '{}', type_marchandise = '{}'WHERE n°='{}')".format(nom_du_fournisseur,num_tel_fournisseur,email,adresse,type_marchandise))
            self.connexion.commit()
            self.curseur.close()
            self.connexion.close()
            QMessageBox.information(QMessageBox(),"Succès", "Modifié avec succès.")
            self.edit_nom_fournisseur.clear()
            self.edit_num_fournisseur.clear()
            self.edit_fournisseur.clear()
            self.edit_email_fournisseur.clear()
            self.edit_adresse_fournisseur.clear()
            self.edit_type_marchandise.clear()
            self.edit_nom_fournisseur.setFocus()
        except Exception:
            QMessageBox.warning(QMessageBox(), "Erreur", "Ne peut pas modifier le fournisseur dans la base des données.")
            self.edit_nom_fournisseur.clear()
            self.edit_num_fournisseur.clear()
            self.edit_email_fournisseur.clear()
            self.edit_adresse_fournisseur.clear()
            self.edit_type_marchandise.clear()
            self.edit_nom_fournisseur.setFocus()

if __name__ == "__main__":
    app = QApplication([])
    modifier_fournisseur = ModifierFournisseur()
    modifier_fournisseur.show()
    sys.exit(app.exec)
#     pass
