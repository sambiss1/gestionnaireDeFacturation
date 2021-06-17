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

class EnregistrerFournisseur(QWidget):
    def __init__(self,parent=None):
        super(EnregistrerFournisseur, self).__init__(parent, Qt.Window)
        loadUi("fournisseur_window.ui",self)

        #self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon("./icones/icone_fournisseur.ico"))
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)


        # Signal et Slot pour le bouton d'enregistrement des fournisseurs
        self.bouton_enregistrer_fournisseur.clicked.connect(self.enregistrer_fournisseur)

        # Signal et Slot pour le bouton d'annulation
        self.bouton_annuler_fournisseur.clicked.connect(self.annuler_ajout)

    def enregistrer_fournisseur(self):
        """Fonction permettant l'enregistrement des fournisseurs"""
        nom_du_fournisseur=self.edit_nom_fournisseur.text()
        email = self.edit_email_fournisseur.text()
        adresse= self.edit_adresse_fournisseur.text()
        type_marchandise= self.edit_type_marchandise.text()
        try:
            num_tel_fournisseur= int(self.edit_num_fournisseur.text())
        except ValueError:
            QMessageBox.warning(QMessageBox(), "Attention", "Veuillez introduire une valeur numérique dans la zone de texte du numéro de téléphone")
        try:
            connexion = sqlite3.connect('idatabase.db')
            curseur = connexion.cursor()
            curseur.execute("INSERT INTO liste_des_fournisseurs (fournisseur, num_telephone, email, adresse, type_marchandise) VALUES (?,?,?,?,?)",(nom_du_fournisseur,num_tel_fournisseur,email,adresse,type_marchandise))

            connexion.commit()
            curseur.close()
            connexion.close()
            QMessageBox.information(QMessageBox(),"Succès", "Ajouté avec succès.")
            self.edit_nom_fournisseur.clear()
            self.edit_num_fournisseur.clear()
            self.edit_fournisseur.clear()
            self.edit_email_fournisseur.clear()
            self.edit_adresse_fournisseur.clear()
            self.edit_type_marchandise.clear()
            self.edit_nom_fournisseur.setFocus()
        except Exception:
            QMessageBox.warning(QMessageBox(), "Erreur", "Ne peut pas ajouter le fournisseur dans la base des données.")
            self.edit_nom_fournisseur.clear()
            self.edit_num_fournisseur.clear()
            self.edit_email_fournisseur.clear()
            self.edit_adresse_fournisseur.clear()
            self.edit_type_marchandise.clear()
            self.edit_nom_fournisseur.setFocus()

    def annuler_ajout(self):
        if self.edit_nom_fournisseur.text()=="" and self.edit_num_fournisseur.text()=="" and self.edit_email_fournisseur.text()=="" and self.edit_adresse_fournisseur.text() and self.edit_type_marchandise.text()=="":
            self.close()
        else:
            messageConfirmation="Êtes-vous sûr de vouloir annuler l'enregistrement ?"
            self.reponse = QMessageBox()
            self.reponse.setIcon(QMessageBox.Question)
            self.reponse.setWindowIcon(QIcon("./icones/icone_question.ico"))
            self.reponse.setWindowTitle("Confirmation")
            self.reponse.setText(messageConfirmation)
            self.reponse.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            bouton_oui = self.reponse.button(QMessageBox.Yes)
            bouton_oui.setText("Oui")
            bouton_non = self.reponse.button(QMessageBox.No)
            bouton_non.setText("Non")
            self.reponse.exec_()
            if self.reponse.clickedButton() == bouton_oui:
                self.close()
            else:
                self.edit_nom_fournisseur.setFocus()
                return False


if __name__ == "__main__":
    app = QApplication([])
    enregistrer_fournisseur = EnregistrerFournisseur()
    enregistrer_fournisseur.show()
    sys.exit(app.exec)
#     pass
