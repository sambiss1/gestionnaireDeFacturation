# This Python file uses the following encoding: utf-8
import sys
import os


from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QDesktopWidget, QPushButton, QMessageBox, QTableWidgetItem, QTableWidget, QHeaderView, QDateEdit, QDateTimeEdit
from PyQt5.QtCore import Qt, QFile, QRect, QSize, QDateTime, QDate, QTime
from PyQt5.QtGui import QIcon, QKeySequence, QColor, QBrush, QFont
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalDelegate, QSqlRelationalTableModel, QSqlTableModel
import sqlite3


# Connexion à la base des données
connexion = sqlite3.connect('idatabase.db')
curseur = connexion.cursor()

class NouvelleLivraison(QDialog):
    def __init__(self,parent=None):
        super(NouvelleLivraison, self).__init__(parent, Qt.Window)
        loadUi("new_livraison_dialog.ui",self)

        ## Initialisation de la fenêtre
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Nouvelle Livraison")
        self.setWindowIcon(QIcon("./icones/icone_livraisons.ico"))
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)


        ## Initialisation de la date du jour
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        self.dateEdit.setTime(QTime.currentTime())
        self.dateEdit.setMaximumDate(QDate(7999, 12, 28))
        self.dateEdit.setMaximumTime(QTime(23, 59, 59))
        self.dateEdit.setCalendarPopup(False)


        ## Signal et slot pour le bouton d'enregistrement des nouvelles
        self.bouton_enregistrer_livraison.clicked.connect(self.enregistrer_livraison)
        self.bouton_enregistrer_livraison.clicked.connect(self.enregistrer_stock)

    def enregistrer_livraison(self):
        """Enregistrement dans la table des livraisons"""
        nom_produit = self.edit_nom_article.text()
        bon_livraison = self.edit_bon_livraison.text()
        nom_fournisseur = self.edit_nom_fournisseur.text()
        fabricant = self.edit_fabricant.text()
        type_marchandises = self.edit_type.text()
        value = self.dateEdit.date()
        valeurdate = value.toString(self.dateEdit.displayFormat())
        try:
            quantite_livree = self.edit_quantite_livree.text()
            prix_unitaire_achat = self.edit_prix_unitaire.text()
            qte_livree = int(quantite_livree)
            prix_achat = int(prix_unitaire_achat)
            total_general = int((qte_livree)*(prix_achat))
            self.label_total.setText(str(total_general))
            total = self.label_total.text()
        except ValueError:
            QMessageBox.warning(QMessageBox(), "Attention", "Veuillez introduire des valeurs numériques dans les zones de texte de 'Quantité Livrée' et 'Prix Unitaire'")
        try:
            connexion = sqlite3.connect('idatabase.db')
            curseur = connexion.cursor()
            curseur.execute("""INSERT INTO liste_des_livraisons (article, type, bon_livraison, fournisseur, fabricant, date_livraison, quantite_livree, prix_unitaire, prix_total) VALUES (?,?,?,?,?,?,?,?,?)""",(nom_produit,type_marchandises,bon_livraison,nom_fournisseur,fabricant,valeurdate,qte_livree,prix_achat,total))
            #curseur.execute('''SELECT article, type, quantite_livree, prix_unitaire, date_livraison FROM liste_des_livraisons INNER JOIN etat_stock ON liste_des_livraisons.id=etat_stock.id''')
            connexion.commit()
            curseur.close()
            connexion.close()
            QMessageBox.information(QMessageBox(),"Succès", "Ajouté avec succès.")
        except Exception:
            QMessageBox.warning(QMessageBox(), "Erreur", "Ne peut pas enregister la nouvelle livraison dans la base des données.")

    def enregistrer_stock(self):
        """Enregistrement dans la table stock"""
        nom_produit = self.edit_nom_article.text()
        bon_livraison = self.edit_bon_livraison.text()
        nom_fournisseur = self.edit_nom_fournisseur.text()
        fabricant = self.edit_fabricant.text()
        type_marchandises = self.edit_type.text()
        value = self.dateEdit.date()
        valeurdate = value.toString(self.dateEdit.displayFormat())
        try:
            ## Vérification du type des valeurs introduites
            quantite_livree = self.edit_quantite_livree.text()
            prix_unitaire_achat = self.edit_prix_unitaire.text()
            qte_livree = int(quantite_livree)
            prix_achat = int(prix_unitaire_achat)
            total_general = int((qte_livree)*(prix_achat))
            self.label_total.setText(str(total_general))
            total = self.label_total.text()
        except ValueError:
            QMessageBox.warning(QMessageBox(), "Attention", "Veuillez introduire des valeurs numériques dans les zones de texte de 'Quantité Livrée' et 'Prix Unitaire'")
        try:
            ## Vérification de la connexion à la base des données
            connexion = sqlite3.connect('idatabase.db')
            curseur = connexion.cursor()
            #self.curseur.execute('''SELECT * FROM liste_des_livraisons INNER JOIN etat_stock ON liste_des_livraisons.n°=etat_stock.n°''')
            curseur.execute("INSERT INTO etat_stock (article, type,prix_unitaire,quantite_livree,fournisseur,date_livraison) VALUES (?,?,?,?,?,?)",(nom_produit,type_marchandises,prix_achat,qte_livree,nom_fournisseur,valeurdate))
            connexion.commit()
            curseur.close()
            connexion.close()
            QMessageBox.information(QMessageBox(),"Succès", "Ajouté avec succès.")
            self.edit_nom_article.clear()
            self.edit_bon_livraison.clear()
            self.edit_nom_fournisseur.clear()
            self.edit_fabricant.clear()
            self.edit_quantite_livree.clear()
            self.edit_prix_unitaire.clear()
            self.label_total.setText("0")
            self.label_total.hide()
            self.edit_type.clear()
            self.edit_nom_article.setFocus()
        except Exception:
            QMessageBox.warning(QMessageBox(), "Erreur", "Ne peut pas enregister la nouvelle livraison dans la base des données.")
            self.edit_nom_article.clear()
            self.edit_bon_livraison.clear()
            self.edit_nom_fournisseur.clear()
            self.edit_fabricant.clear()
            self.edit_quantite_livree.clear()
            self.edit_prix_unitaire.clear()
            self.label_total.setText("0")
            self.label_total.hide()
            self.edit_type.clear()
            self.edit_nom_article.setFocus()


if __name__ == "__main__":
    app = QApplication([])
    nouvelle_livraison = NouvelleLivraison()
    nouvelle_livraison.show()
    sys.exit(app.exec)
    #     pass
