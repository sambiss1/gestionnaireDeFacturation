# This Python file uses the following encoding: utf-8
import sys
import os


from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QPushButton, QMessageBox, QTableWidgetItem, QTableWidget, QHeaderView
from PyQt5.QtCore import Qt, QFile, QRect, QSize, QDateTime, QDate, QTime
from PyQt5.QtGui import QIcon, QKeySequence, QColor, QBrush, QFont
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalDelegate, QSqlRelationalTableModel, QSqlTableModel
import sqlite3

from ajout_fournisseur import EnregistrerFournisseur
from nouvelle_livraison import NouvelleLivraison


# Connexion à la base des données
connexion = sqlite3.connect('idatabase.db')
curseur = connexion.cursor()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi("window.ui", self)

        # Configuration de la fenêtre principale
        self.setWindowTitle("IStore")
        self.resize(1200,680)
        self.setMaximumSize(1200,680)
        self.setMinimumSize(1200,680)
        #self.setGeometry(QRect(50,50,1200,700))
        self.center()

        # Page d'ouverture par défaut
        self.stackedWidget.setCurrentWidget(self.dashboard)

        # Signaux et Slots de changement des pages
        self.bouton_dashboard.clicked.connect(self.show_dashboard)
        self.bouton_factures.clicked.connect(self.show_factures)
        self.bouton_commandes.clicked.connect(self.show_commandes)
        self.bouton_clients.clicked.connect(self.show_clients)
        self.bouton_stock.clicked.connect(self.show_stock)
        self.bouton_statistiques.clicked.connect(self.show_statistiques)
        self.bouton_utilisateurs.clicked.connect(self.show_utilisateurs)

        # Style du bouton de la page d'accueil à l'ouverture
        self.bouton_dashboard.setStyleSheet("QPushButton{background-color: rgb(85, 170, 255);color: rgb(255, 255, 255);border: 0px solid #052F61;}")


    def center(self):
        """Fonction permettant de centrer la fenêtre à l'ouverture de l'application"""
        centerscreen =self.frameGeometry()
        centerposition = QDesktopWidget().availableGeometry().center()
        centerscreen.moveCenter(centerposition)
        self.move(centerscreen.topLeft())

    def show_dashboard(self):
        """Fonction d'ouverture de la page d'accueil"""
        self.stackedWidget.setCurrentWidget(self.dashboard)
        self.bouton_dashboard.setStyleSheet("QPushButton{background-color: rgb(85, 170, 255);color: rgb(255, 255, 255);border: 0px solid #052F61;}")
        self.bouton_factures.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_commandes.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_clients.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_stock.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_statistiques.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_utilisateurs.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_deconnexion.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")

    def show_factures(self):
        """Fonction d'ouverture de la page des factures"""
        self.stackedWidget.setCurrentWidget(self.page_factures)
        self.bouton_factures.setStyleSheet("QPushButton{background-color: rgb(85, 170, 255);color: rgb(255, 255, 255);border: 0px solid;}")
        self.bouton_dashboard.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_commandes.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_clients.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_stock.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_statistiques.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_utilisateurs.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_deconnexion.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")

    def show_commandes(self):
        """Fonction d'ouverture de la page des commandes"""
        self.stackedWidget.setCurrentWidget(self.page_commandes)
        self.bouton_commandes.setStyleSheet("QPushButton{background-color: rgb(85, 170, 255);color: rgb(255, 255, 255);border: 0px solid;}")
        self.bouton_dashboard.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_factures.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_clients.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_stock.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_statistiques.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_utilisateurs.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_deconnexion.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")

        #self.bouton_effectuer_commande.clicked.connect(self.passercommande)
    def show_clients(self):
        """Fonction d'ouverture de la page des clients"""
        self.stackedWidget.setCurrentWidget(self.page_clients)
        self.bouton_clients.setStyleSheet("QPushButton{background-color: rgb(85, 170, 255);color: rgb(255, 255, 255);border: 0px solid;}")
        self.bouton_dashboard.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_factures.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_commandes.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_stock.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_statistiques.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_utilisateurs.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_deconnexion.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")

        self.listes_clients()

    def listes_clients(self):
        # Configuration du QTableWidget
        #self.table_liste_clients = QTableWidget(self)
        self.table_liste_clients.setRowCount(5) # Nombre des lignes
        self.table_liste_clients.setColumnCount(3) # Nombre des colonnes
        self.table_liste_clients.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_liste_clients.horizontalHeader().setVisible(False) # Visibilité de la ligne par défaut
        self.table_liste_clients.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_passer_clients.setGeometry(QRect(30,130,650,201)) # Position
        self.table_liste_clients.setFont(QFont('Century Gothic', 14)) # Police
        header = self.table_liste_clients.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        #header.setStretchLastSection(True)

        # Creation de colonnes
        # Colonne 1
        self.table_liste_clients.setItem(0,0, QTableWidgetItem("N°"))
        # Couleur du texte et de l'arrière plan
        self.table_liste_clients.item(0,0).setBackground(QColor(5,47,97))
        self.table_liste_clients.item(0,0).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 2
        self.table_liste_clients.setItem(0,1, QTableWidgetItem("Nom du client"))
        # Couleur du texte et de l'arrière plan
        self.table_liste_clients.item(0,1).setBackground(QColor(5,47,97))
        self.table_liste_clients.item(0,1).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 3
        self.table_liste_clients.setItem(0,2, QTableWidgetItem("N° Téléphone"))
        # Couleur du texte et de l'arrière plan
        self.table_liste_clients.item(0,2).setBackground(QColor(5,47,97))
        self.table_liste_clients.item(0,2).setForeground(QBrush(QColor(255,255,255)))

    def show_stock(self):
        """Fopassern d'ouverture de la page de stock"""
        ## Gestion de la page de stock

        self.stackedWidget.setCurrentWidget(self.page_stock)
        self.tabWidget_stock.setCurrentIndex(0)
        self.bouton_stock.setStyleSheet("QPushButton{background-color: rgb(85, 170, 255);color: rgb(255, 255, 255);border: 0px solid;}")
        self.bouton_dashboard.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_factures.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_commandes.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_clients.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_statistiques.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_utilisateurs.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_deconnexion.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")


        ## Onglet de l'état du stock
        self.onglet_etat_du_stock()

        ## Onglet des fournisseurs
        self.onglet_des_fournisseurs()

        ## Onglet des livraisons
        self.onglet_des_livraisons()

    def onglet_etat_du_stock(self):
        ## Configupapasser du QTableWidget
        ##  TableWidget Etat du Stock
        self.table_stock.setRowCount(5) # Nombre des lignes
        self.table_stock.setColumnCount(6) # Nombre des colonnes
        self.table_stock.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_stock.horizontalHeader().setVisible(False) # Visibilité de la ligne par défaut
        self.table_stock.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_stock.setGeometry(QRect(30,150,740,250)) # Position
        self.table_stock.setFont(QFont('Century Gothic', 14)) # Police
        header = self.table_stock.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        #header.setpasserchLastSection(True)

        # Creation 1
        self.table_stock.setItem(0,0, QTableWidgetItem("N°"))
        # Couleur du texte et de l'arrière plan
        self.table_stock.item(0,0).setBackground(QColor(5,47,97))
        self.table_stock.item(0,0).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 2
        self.table_stock.setItem(0,1, QTableWidgetItem("Article"))
        # Couleur du texte et de l'arrière plan
        self.table_stock.item(0,1).setBackground(QColor(5,47,97))
        self.table_stock.item(0,1).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 3
        self.table_stock.setItem(0,2, QTableWidgetItem("Types"))
        # Couleur du texte et de l'arrière plan
        self.table_stock.item(0,2).setBackground(QColor(5,47,97))
        self.table_stock.item(0,2).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 4
        self.table_stock.setItem(0,3, QTableWidgetItem("Quantité Disponible"))
        # Couleur du texte et de l'arrière plan
        self.table_stock.item(0,3).setBackground(QColor(5,47,97))
        self.table_stock.item(0,3).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 5
        self.table_stock.setItem(0,4, QTableWidgetItem("prix Unitaire"))
        # Couleur du texte et de l'arrière plan
        self.table_stock.item(0,4).setBackground(QColor(5,47,97))
        self.table_stock.item(0,4).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 6
        self.table_stock.setItem(0,5, QTableWidgetItem("Date de livraison"))
        # Couleur du texte et de l'arrière plan
        self.table_stock.item(0,5).setBackground(QColor(5,47,97))
        self.table_stock.item(0,5).setForeground(QBrush(QColor(255,255,255)))

    def onglet_des_fournisseurs(self):
        ## Fournisseurs

        ## Configuration du QTableWidget

        self.table_fournisseurs.setRowCount(2) # Nombre des lignes
        self.table_fournisseurs.setColumnCount(6) # Nombre des colonnes
        self.table_fournisseurs.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_fournisseurs.horizontalHeader().setVisible(False) # Visibilité de la ligne par défaut
        self.table_fournisseurs.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_stock.setGeometry(QRect(30,150,740,250)) # Position
        self.table_fournisseurs.setFont(QFont('Century Gothic', 14)) # Police
        header = self.table_fournisseurs.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        #header.setStretchLastSection(True)

        ## Actualisation de la table à l'ouverture
        query = "SELECT * FROM liste_des_fournisseurs"
        resultat = connexion.execute(query)
        self.table_fournisseurs.setRowCount(-1)
        for row_number, row_data in enumerate(resultat):
            self.table_fournisseurs.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_fournisseurs.setItem(row_number+1, column_number, QTableWidgetItem(str(data)))
        connexion.close

        # Creation de colonnes
        # Colonne 1
        self.table_fournisseurs.setItem(0,0, QTableWidgetItem("N°"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,0).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,0).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 2
        self.table_fournisseurs.setItem(0,1, QTableWidgetItem("Nom"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,1).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,1).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 3
        self.table_fournisseurs.setItem(0,2, QTableWidgetItem("N° Téléphone"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,2).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,2).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 4
        self.table_fournisseurs.setItem(0,3, QTableWidgetItem("Email"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,3).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,3).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 5
        self.table_fournisseurs.setItem(0,4, QTableWidgetItem("Adresse"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,4).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,4).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 6
        self.table_fournisseurs.setItem(0,5, QTableWidgetItem("Type des marchandises"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,5).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,5).setForeground(QBrush(QColor(255,255,255)))

        ## Signaux et Slots
        ## Actulisation de la liste des fournisseurs
        self.bouton_actualiser_fournisseurs.clicked.connect(self.actualiser_liste_fournisseur)

        ## Ajout d'un nouveau fournisseur
        self.bouton_ajouter_fournisseurs.clicked.connect(self.show_page_enregistrer_fournisseur)

    def actualiser_liste_fournisseur(self):
        query = "SELECT * FROM liste_des_fournisseurs"
        resultat = connexion.execute(query)
        self.table_fournisseurs.setRowCount(1)
        for row_number, row_data in enumerate(resultat):
            self.table_fournisseurs.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_fournisseurs.setItem(row_number+1, column_number, QTableWidgetItem(str(data)))
        connexion.close

        # Initialisation des colonnes
        # Colonne 1
        self.table_fournisseurs.setItem(0,0, QTableWidgetItem("N°"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,0).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,0).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 2
        self.table_fournisseurs.setItem(0,1, QTableWidgetItem("Nom"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,1).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,1).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 3
        self.table_fournisseurs.setItem(0,2, QTableWidgetItem("N° Téléphone"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,2).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,2).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 4
        self.table_fournisseurs.setItem(0,3, QTableWidgetItem("Email"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,3).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,3).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 5
        self.table_fournisseurs.setItem(0,4, QTableWidgetItem("Adresse"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,4).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,4).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 6
        self.table_fournisseurs.setItem(0,5, QTableWidgetItem("Type des marchandises"))
        # Couleur du texte et de l'arrière plan
        self.table_fournisseurs.item(0,5).setBackground(QColor(5,47,97))
        self.table_fournisseurs.item(0,5).setForeground(QBrush(QColor(255,255,255)))

    def show_page_enregistrer_fournisseur(self):
        enregistrer_fournisseur = EnregistrerFournisseur(self)
        enregistrer_fournisseur.show()

    def onglet_des_livraisons(self):

        # Configuration du QTableWidget
        # TableWidget livraisons
        self.table_livraisons.setRowCount(5) # Nombre des lignes
        self.table_livraisons.setColumnCount(10) # Nombre des colonnes
        self.table_livraisons.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_livraisons.horizontalHeader().setVisible(False) # Visibilité de la ligne par défaut
        self.table_livraisons.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_livraisons.setGeometry(QRect(30,150,740,250)) # Position
        self.table_livraisons.setFont(QFont('Century Gothic', 14)) # Police
        header = self.table_livraisons.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)
        #header.setStretchLastSection(True)

        # Creation des colonnes
        # Colonne 1
        self.table_livraisons.setItem(0,0, QTableWidgetItem("N°"))
        # Couleur du texte et de l'arrière plan
        self.table_livraisons.item(0,0).setBackground(QColor(5,47,97))
        self.table_livraisons.item(0,0).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 2
        self.table_livraisons.setItem(0,1, QTableWidgetItem("Article"))
        # Couleur du texte et de l'arrière plan
        self.table_livraisons.item(0,1).setBackground(QColor(5,47,97))
        self.table_livraisons.item(0,1).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 3
        self.table_livraisons.setItem(0,2, QTableWidgetItem("Type"))
        # Couleur du texte et de l'arrière plan
        self.table_livraisons.item(0,2).setBackground(QColor(5,47,97))
        self.table_livraisons.item(0,2).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 4
        self.table_livraisons.setItem(0,3, QTableWidgetItem("Bon de Livraison"))
        # Couleur du texte et de l'arrière plan
        self.table_livraisons.item(0,3).setBackground(QColor(5,47,97))
        self.table_livraisons.item(0,3).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 5
        self.table_livraisons.setItem(0,4, QTableWidgetItem("Fournisseur"))
        # Couleur du texte et de l'arrière plan
        self.table_livraisons.item(0,4).setBackground(QColor(5,47,97))
        self.table_livraisons.item(0,4).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 6
        self.table_livraisons.setItem(0,5, QTableWidgetItem("Fabricant"))
        # Couleur du texte et de l'arrière plan
        self.table_livraisons.item(0,5).setBackground(QColor(5,47,97))
        self.table_livraisons.item(0,5).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 7
        self.table_livraisons.setItem(0,6, QTableWidgetItem("Date de Livraison"))
        # Couleur du texte et de l'arrière plan
        self.table_livraisons.item(0,6).setBackground(QColor(5,47,97))
        self.table_livraisons.item(0,6).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 8
        self.table_livraisons.setItem(0,7, QTableWidgetItem("Quantité Livrée"))
        # Couleur du texte et de l'arrière plan
        self.table_livraisons.item(0,7).setBackground(QColor(5,47,97))
        self.table_livraisons.item(0,7).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 9
        self.table_livraisons.setItem(0,8, QTableWidgetItem("Prix Unitaire"))
        # Couleur du texte et de l'arrière plan
        self.table_livraisons.item(0,8).setBackground(QColor(5,47,97))
        self.table_livraisons.item(0,8).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 10
        self.table_livraisons.setItem(0,9, QTableWidgetItem("Prix Total"))
        # Couleur du texte et de l'arrière plan
        self.table_livraisons.item(0,9).setBackground(QColor(5,47,97))
        self.table_livraisons.item(0,9).setForeground(QBrush(QColor(255,255,255)))

        self.bouton_nouvelle_livraison.clicked.connect(self.nouvellelivraison)

    def nouvellelivraison(self):
        nouvelle_livraison = NouvelleLivraison(self)
        nouvelle_livraison.show()

    def show_statistiques(self):
        """Fonctions d'ouverture de la page des statistiques"""
        self.stackedWidget.setCurrentWidget(self.page_statistiques)
        self.tabWidget_statistiques.setCurrentIndex(0)
        self.bouton_statistiques.setStyleSheet("QPushButton{background-color: rgb(85, 170, 255);color: rgb(255, 255, 255);border: 0px solid;}")
        self.bouton_dashboard.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_factures.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_commandes.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_clients.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_stock.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_utilisateurs.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_deconnexion.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")

        ## Onglet des ventes
        self.onglet_des_ventes()

        ## Onglet des recettes
        self.onglet_des_recettes()

    def onglet_des_ventes(self):
        ## Onglet des ventes

        # Configuration du QTableWidget
        self.table_ventes.setRowCount(5) # Nombre des lignes
        self.table_ventes.setColumnCount(6) # Nombre des colonnes
        self.table_ventes.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_ventes.horizontalHeader().setVisible(False) # Visibilité de la ligne par défaut
        self.table_ventes.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_liste_utilisateurs.setGeometry(QRect(30,100,650,201)) # Position
        self.table_ventes.setFont(QFont('Century Gothic', 14)) # Police
        header = self.table_ventes.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        # Creation de colonnes
        # Colonne 1
        self.table_ventes.setItem(0,0, QTableWidgetItem("N°"))
        # Couleur du texte et de l'arrière plan
        self.table_ventes.item(0,0).setBackground(QColor(5,47,97))
        self.table_ventes.item(0,0).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 2
        self.table_ventes.setItem(0,1, QTableWidgetItem("Article"))
        # Couleur du texte et de l'arrière plan
        self.table_ventes.item(0,1).setBackground(QColor(5,47,97))
        self.table_ventes.item(0,1).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 3
        self.table_ventes.setItem(0,2, QTableWidgetItem("Quantité Vendue "))
        # Couleur du texte et de l'arrière plan
        self.table_ventes.item(0,2).setBackground(QColor(5,47,97))
        self.table_ventes.item(0,2).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 4
        self.table_ventes.setItem(0,3, QTableWidgetItem("Prix Unitaire"))
        # Couleur du texte et de l'arrière plan
        self.table_ventes.item(0,3).setBackground(QColor(5,47,97))
        self.table_ventes.item(0,3).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 5
        self.table_ventes.setItem(0,4, QTableWidgetItem("Prix Total"))
        # Couleur du texte et de l'arrière plan
        self.table_ventes.item(0,4).setBackground(QColor(5,47,97))
        self.table_ventes.item(0,4).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 6
        self.table_ventes.setItem(0,5, QTableWidgetItem("Date de vente"))
        # Couleur du texte et de l'arrière plan
        self.table_ventes.item(0,5).setBackground(QColor(5,47,97))
        self.table_ventes.item(0,5).setForeground(QBrush(QColor(255,255,255)))

    def onglet_des_recettes(self):
        # Configuration du QTableWidget

        self.table_recettes.setRowCount(5) # Nombre des lignes
        self.table_recettes.setColumnCount(6) # Nombre des colonnes
        self.table_recettes.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_recettes.horizontalHeader().setVisible(False) # Visibilité de la ligne par défaut
        self.table_recettes.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_liste_utilisateurs.setGeometry(QRect(30,100,650,201)) # Position
        self.table_recettes.setFont(QFont('Century Gothic', 14)) # Police
        header = self.table_recettes.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        # Creation de colonnes
        # Colonne 1
        self.table_recettes.setItem(0,0, QTableWidgetItem("N°"))
        # Couleur du texte et de l'arrière plan
        self.table_recettes.item(0,0).setBackground(QColor(5,47,97))
        self.table_recettes.item(0,0).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 2
        self.table_recettes.setItem(0,1, QTableWidgetItem("Article"))
        # Couleur du texte et de l'arrière plan
        self.table_recettes.item(0,1).setBackground(QColor(5,47,97))
        self.table_recettes.item(0,1).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 3
        self.table_recettes.setItem(0,2, QTableWidgetItem("Quantité Vendue"))
        # Couleur du texte et de l'arrière plan
        self.table_recettes.item(0,2).setBackground(QColor(5,47,97))
        self.table_recettes.item(0,2).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 4
        self.table_recettes.setItem(0,3, QTableWidgetItem("Prix d'Achat"))
        # Couleur du texte et de l'arrière plan
        self.table_recettes.item(0,3).setBackground(QColor(5,47,97))
        self.table_recettes.item(0,3).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 5
        self.table_recettes.setItem(0,4, QTableWidgetItem("Prix de Vente"))
        # Couleur du texte et de l'arrière plan
        self.table_recettes.item(0,4).setBackground(QColor(5,47,97))
        self.table_recettes.item(0,4).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 6
        self.table_recettes.setItem(0,5, QTableWidgetItem("Bénéfice"))
        # Couleur du texte et de l'arrière plan
        self.table_recettes.item(0,5).setBackground(QColor(5,47,97))
        self.table_recettes.item(0,5).setForeground(QBrush(QColor(255,255,255)))


    def show_utilisateurs(self):
        """Fonction d'ouverture de la page d'utilisateurs"""
        self.stackedWidget.setCurrentWidget(self.page_utilisateurs)
        self.bouton_utilisateurs.setStyleSheet("QPushButton{background-color: rgb(85, 170, 255);color: rgb(255, 255, 255);border: 0px solid;}")
        self.bouton_dashboard.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_factures.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_commandes.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_clients.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_stock.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_statistiques.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")
        self.bouton_deconnexion.setStyleSheet("QPushButton{background-color: rgb(5, 47, 97);color: rgb(255, 255, 255);border: 0px solid;} QPushButton:hover {background-color: rgb(85, 170, 255);}")

        ## Table des utilisateurs
        self.liste_des_utilisateurs()

    def liste_des_utilisateurs(self):
        # Configuration du QTableWidget
        #self.table_liste_utilisateurs = QTableWidget(self)
        self.table_liste_utilisateurs.setRowCount(5) # Nombre des lignes
        self.table_liste_utilisateurs.setColumnCount(5) # Nombre des colonnes
        self.table_liste_utilisateurs.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_liste_utilisateurs.horizontalHeader().setVisible(False) # Visibilité de la ligne par défaut
        self.table_liste_utilisateurs.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_liste_utilisateurs.setGeometry(QRect(30,100,650,201)) # Position
        self.table_liste_utilisateurs.setFont(QFont('Century Gothic', 14)) # Police
        header = self.table_liste_utilisateurs.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        #header.setStretchLastSection(True)

        # Creation de colonnes
        # Colonne 1
        self.table_liste_utilisateurs.setItem(0,0, QTableWidgetItem("N°"))
        # Couleur du texte et de l'arrière plan
        self.table_liste_utilisateurs.item(0,0).setBackground(QColor(5,47,97))
        self.table_liste_utilisateurs.item(0,0).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 2
        self.table_liste_utilisateurs.setItem(0,1, QTableWidgetItem("Nom d'utilisateur"))
        # Couleur du texte et de l'arrière plan
        self.table_liste_utilisateurs.item(0,1).setBackground(QColor(5,47,97))
        self.table_liste_utilisateurs.item(0,1).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 3
        self.table_liste_utilisateurs.setItem(0,2, QTableWidgetItem("Type de Compte"))
        # Couleur du texte et de l'arrière plan
        self.table_liste_utilisateurs.item(0,2).setBackground(QColor(5,47,97))
        self.table_liste_utilisateurs.item(0,2).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 4
        self.table_liste_utilisateurs.setItem(0,3, QTableWidgetItem("ID Agent"))
        # Couleur du texte et de l'arrière plan
        self.table_liste_utilisateurs.item(0,3).setBackground(QColor(5,47,97))
        self.table_liste_utilisateurs.item(0,3).setForeground(QBrush(QColor(255,255,255)))

        # Colonne 5
        self.table_liste_utilisateurs.setItem(0,4, QTableWidgetItem("ID Administrateur"))
        # Couleur du texte et de l'arrière plan
        self.table_liste_utilisateurs.item(0,4).setBackground(QColor(5,47,97))
        self.table_liste_utilisateurs.item(0,4).setForeground(QBrush(QColor(255,255,255)))

    def closeEvent(self, event=None):
        messageConfirmation="Êtes-vous sûr de vouloir quitter ?"
        self.reponse = QMessageBox.question(self ,"Confirmation",
        messageConfirmation,QMessageBox.Yes,QMessageBox.No)
        if self.reponse == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
