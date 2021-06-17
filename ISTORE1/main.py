# This Python file uses the following encoding: utf-8
import sys
import os


from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QPushButton, QMessageBox, QTableWidgetItem, QTableWidget, QHeaderView, QLineEdit, QLabel, QAction, QMenuBar, QMenu
from PyQt5.QtCore import Qt, QFile, QRect, QSize, QDateTime, QDate, QTime, QSortFilterProxyModel
from PyQt5.QtGui import QIcon, QKeySequence, QColor, QBrush, QFont, QStandardItemModel, QStandardItem, QTextDocument, QTextCursor
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalDelegate, QSqlRelationalTableModel, QSqlTableModel
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
import sqlite3

from ajout_fournisseur import EnregistrerFournisseur
from nouvelle_livraison import NouvelleLivraison
from modification_fournisseur import ModifierFournisseur
from modification_livraison import ModifierLivraison
from modification_etat_stock import ModifierEtatStock
from modification_client import ModifierClient
from modification_utilisateur import ModifierUtilisateur
from login_function import * #LoginUser

## Connexion à la base des données
connexion = sqlite3.connect('idatabase.db')
curseur = connexion.cursor()
##Connexion à la base des données
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName('idatabase.db')
db.open()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi("window.ui", self)

        # Configuration de la fenêtre principale
        self.setWindowTitle("IStore") ## Titre de la fenêtre
        self.resize(1200,680) ## Taille de la fenêtre
        self.setWindowModality(Qt.NonModal) ## Modalité de la fenêtre
        self.setMaximumSize(1200,680) ## Taille maximum
        self.setMinimumSize(1200,680) ## Taille minimum
        self.setWindowIcon(QIcon("./icones/icone_panier.ico")) ## Icône de la fenêtre
        #self.setWindowFlags(Qt.CustomizeWindowHint)
        #self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(Qt.WindowCloseButtonHint)
        #self.setFont(QFont("Century Gothic"))#, 14))
        #self.setPointSize(14)

        ## Appel de la fonction de centralisation de la fenêtres
        self.center()

        self.fet()


        ## La barre de menu
        ## Créattion et Ajout des éléments de la barre de menu
        self.menubar = QMenuBar()
        menuFichier = self.menuBar().addMenu('Fichier')
        menuEdition = self.menuBar().addMenu('A Propos')
        menuAide = self.menuBar().addMenu('?')

        ## Actions
        actionQuitter = QAction(QIcon.fromTheme('application-exit'), "Quitter",
                             self, shortcut="Ctrl+Q", triggered = self.close)
        menuFichier.addAction(actionQuitter)


        """def close(self,event=None):
            messageConfirmation="Êtes-vous sûr de vouloir quitter ?"
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
                event.accept()
            else:
                event.ignore()"""
        ## Page d'ouverture par défaut
        self.stackedWidget.setCurrentWidget(self.dashboard)

        ## Signaux et Slots de changement des pages
        self.bouton_dashboard.clicked.connect(self.show_dashboard)
        self.bouton_factures.clicked.connect(self.show_factures)
        self.bouton_commandes.clicked.connect(self.show_commandes)
        self.bouton_clients.clicked.connect(self.show_clients)
        self.bouton_stock.clicked.connect(self.show_stock)
        self.bouton_statistiques.clicked.connect(self.show_statistiques)
        self.bouton_utilisateurs.clicked.connect(self.show_utilisateurs)

        ## Signal de déconnexion
        self.bouton_deconnexion.clicked.connect(self.deconnexion)

        ## Style du bouton de la page d'accueil à l'ouverture
        self.bouton_dashboard.setStyleSheet("""QPushButton {
                                                    background-color: rgb(85, 170, 255);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid #052F61;
                                                    text-align:left;
                                                    padding-left:5px;
                                                    padding-right:2px;}""")

        ## Element furtif
        self.edit_total = QLabel(self)
        self.edit_total.hide()

        ## Les icônes  des boutons da la barre verticale
        self.bouton_dashboard.setIcon(QIcon("./icones/icone_dashboard.ico"))
        self.bouton_dashboard.setIconSize(QSize(40,40))
        self.bouton_factures.setIcon(QIcon("./icones/icone_facture.ico"))
        self.bouton_factures.setIconSize(QSize(40,40))
        self.bouton_commandes.setIcon(QIcon("./icones/icone_cart.ico"))
        self.bouton_commandes.setIconSize(QSize(40,40))
        self.bouton_clients.setIcon(QIcon("./icones/icones_clients.ico"))
        self.bouton_clients.setIconSize(QSize(40,40))
        self.bouton_stock.setIcon(QIcon("./icones/icone_depot.ico"))
        self.bouton_stock.setIconSize(QSize(40,40))
        self.bouton_statistiques.setIcon(QIcon("./icones/icone_chart.ico"))
        self.bouton_statistiques.setIconSize(QSize(40,40))
        self.bouton_utilisateurs.setIcon(QIcon("./icones/icone_user.ico"))
        self.bouton_utilisateurs.setIconSize(QSize(40,40))
        self.bouton_deconnexion.setIcon(QIcon("./icones/icone_deconnexion.ico"))
        self.bouton_deconnexion.setIconSize(QSize(40,40))

        ## Test
        result = curseur.execute("SELECT * FROM etat_stock")
        for data in result:
            #self.comboBox.addItems(str(data[1]))
            #self.lineEdit_2.setText(str(data[1]))
            print("Données 1 : ",data[1])

    def center(self):
        """Fonction permettant de centrer la fenêtre à l'ouverture de l'application"""
        centerscreen =self.frameGeometry()
        centerposition = QDesktopWidget().availableGeometry().center()
        centerscreen.moveCenter(centerposition)
        self.move(centerscreen.topLeft())

    def deconnexion(self, event=None):
        """Fonction pour gerer la déconnexion"""
        ## Déconnexion
        messageConfirmation="Êtes-vous sûr de vouloir vous déconnecter ?"
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
            widget1 = LoginUser()
            #widget1.setModal(True)
            widget1.exec()
            #widget1.raise_()
            #widget1.showMaximized()
            #widget1.show()
            #widget1.setWindowFlags(Qt.WindowStaysOnTopHint)
        else:
            return False

    def fet(self):
        ## Test d'affichage des données dans un combobox
        self.model_produits = QSqlTableModel()
        self.model_produits.setTable("etat_stock")
        self.model_produits.select()
        self.comboBox.setModel(self.model_produits)
        self.comboBox.setModelColumn(self.model_produits.fieldIndex("article"))


    def show_dashboard(self):
        """Fonction d'ouverture de la page d'accueil"""
        self.stackedWidget.setCurrentWidget(self.dashboard)
        ## Feuilles de style des boutons
        self.bouton_dashboard.setStyleSheet("""QPushButton {
                                                    background-color: rgb(85, 170, 255);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid #052F61;
                                                    text-align:left;
                                                    padding-left:5px;}
                                            """)
        self.bouton_factures.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255); }
                                            """)
        self.bouton_commandes.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255); }
                                            """)
        self.bouton_clients.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255); }
                                            """)
        self.bouton_stock.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                            QPushButton:hover {background-color: rgb(85, 170, 255); }
                                            """)
        self.bouton_statistiques.setStyleSheet(""" QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255); }
                                                """)
        self.bouton_utilisateurs.setStyleSheet(""" QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255); }
                                                """)
        self.bouton_deconnexion.setStyleSheet(""" QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255); }
                                                """)


    def show_factures(self):
        """Fonction d'ouverture de la page des factures"""
        ## Changement de page
        self.stackedWidget.setCurrentWidget(self.page_factures)
        ## Les feuilles de style
        self.bouton_factures.setStyleSheet(""" QPushButton {
                                                    background-color: rgb(85, 170, 255);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                            """)
        self.bouton_dashboard.setStyleSheet(""" QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255); }
                                            """)
        self.bouton_commandes.setStyleSheet(""" QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px; }
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255); }
                                            """)
        self.bouton_clients.setStyleSheet(""" QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255); }
                                            """)
        self.bouton_stock.setStyleSheet(""" QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                            QPushButton:hover {
                                                    background-color: rgb(85, 170, 255); }
                                            """)
        self.bouton_statistiques.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}""")
        self.bouton_utilisateurs.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}""")
        self.bouton_deconnexion.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                """)

    def show_commandes(self):
        """Fonction d'ouverture de la page des commandes"""
        ## Changement de page
        self.stackedWidget.setCurrentWidget(self.page_commandes)
        ## Feuilles de style
        self.bouton_commandes.setStyleSheet("""QPushButton {
                                                        background-color: rgb(85, 170, 255);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                """)
        self.bouton_dashboard.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_factures.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                """)
        self.bouton_clients.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                """)
        self.bouton_stock.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                            QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                            """)
        self.bouton_statistiques.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255); }
                                                        """)
        self.bouton_utilisateurs.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255); }
                                                        """)
        self.bouton_deconnexion.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}""")

        ## Connexion à la table 'etat_de_stock'
        self.model_produits = QSqlTableModel()
        self.model_produits.setTable("etat_stock") ## Sélection de la table
        self.model_produits.select()
        self.model_produits.setHeaderData(0, Qt.Horizontal, "N°")
        self.model_produits.setHeaderData(1, Qt.Horizontal, u"Article")
        self.model_produits.setHeaderData(2, Qt.Horizontal, "Type")
        self.model_produits.setHeaderData(3, Qt.Horizontal, u"Prix Unitaire")
        self.model_produits.setHeaderData(4, Qt.Horizontal, u"Quantité Disponible")
        self.model_produits.setHeaderData(5, Qt.Horizontal, u"Fournisseur")
        self.model_produits.setHeaderData(6, Qt.Horizontal, u"Date de livraison")

        ## Filtrage des données pour la recherche instantanée
        self.filter_produit = QSortFilterProxyModel(self)
        self.filter_produit.setSourceModel(self.model_produits)
        self.filter_produit.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_produit.setFilterKeyColumn(1)
        #self.choix_recherche = self.comboBox_choix_recherche.currentText()
        #if self.choix_recherche=="Article":
        #    self.filter_produit.setFilterKeyColumn(2)
        #elif self.comboBox_choix_recherche.currentIndex()==3:
        #     self.filter_produit.setFilterKeyColumn(2)
        #elif self.comboBox_choix_recherche.currentIndex()==4:
        #    self.filter_produit.setFilterKeyColumn(3)
        #else:
        #    self.filter_produit.setFilterKeyColumn(-1)
        text = self.edit_search.text()
        self.edit_search.textChanged.connect(self.filter_produit.setFilterRegExp)
        self.tableView_produits.setModel(self.filter_produit)
        #font = QFont("Century Gothic", 14)
        #self.tableView_produits.setFont(font)
        self.tableView_produits.setColumnHidden(5, True)
        self.tableView_produits.setColumnHidden(6, True)
        self.tableView_produits.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        ## Signal et Slot pour afficher les contenus de la ligne sélectionnée
        self.tableView_produits.clicked.connect(self.seeindex)

        ## Signal et Slot pour ajouter un produit à la commande
        self.bouton_valider_commande.clicked.connect(self.effectuer_commande)

        ## Signal et Slot pour retirer un produit
        self.bouton_retirer_produit.clicked.connect(self.retirer_article)

        ## Signal et Slot pour imprimer
        self.bouton_imprimer.clicked.connect(self.handlePrint)

        ## Signal ppur l'aperçu avant impression
        self.bouton_preview_print.clicked.connect(self.handlePreview)

        ## Tableau
        self.tableWidget_commandes.setRowCount(0) # Nombre des lignes
        self.tableWidget_commandes.setColumnCount(5) # Nombre des colonnes
        self.tableWidget_commandes.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.tableWidget_commandes.horizontalHeader().setVisible(True) # Visibilité de la ligne par défaut
        self.tableWidget_commandes.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        self.tableWidget_commandes.setFont(QFont('Century Gothic', 14)) # Police
        headers = ["N°","Article", "Quantité", "Prix Unitaire", "Prix Total"]
        self.tableWidget_commandes.setHorizontalHeaderLabels(headers)
        header = self.tableWidget_commandes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

    def seeindex(self,index=None):
        """Fonction permettant de récuperer l'index(le contenu) de la ligne sélectionnée"""
        index.column = 5
        row = index.row()
        col1 = self.model_produits.record(row).field(1).value()
        col2 = self.model_produits.record(row).field(2).value()
        col3 = self.model_produits.record(row).field(3).value()
        self.edit_nom_article.setText(str(col1))
        self.edit_type.setText(str(col2))
        self.edit_prix_unitaire.setText(str(col3))

    def retirer_article(self):
        """Fonction pour retiter un produit"""
        self.edit_nom_article.clear()
        self.edit_type.clear()
        self.edit_prix_unitaire.clear()

    def effectuer_commande(self):
        """Fonction pour ajouter au produit au panier"""
        nom_article = self.edit_nom_article.text()
        quantite = self.edit_quantite.text()
        prix_unitaire = self.edit_prix_unitaire.text()
        #try:
        qte = float(quantite)
        prix_unit = float(prix_unitaire)
        quantite = self.edit_quantite.text()
        prix_unitaire = self.edit_prix_unitaire.text()
        prix_total = float((qte)*(prix_unit))
        self.edit_total.setText(str(prix_total))
        total = prix_total
        i = self.tableWidget_commandes.rowCount()
        i = 0
        if i < 1:
            self.label_total_general.setText(str(prix_total))
            i+=1
        else:
            total = prix_total + prix_total
            self.label_total_general.setText(str(total))
        """while total_general>0:
            total_general += float(total)
            #self.label_total_general.setText(str(total_general+prix_total))
            break"""
        rowPosition = self.table_commandes.rowCount()
        self.table_commandes.insertRow(rowPosition)
        numcols = self.table_commandes.columnCount()
        numrows = self.table_commandes.rowCount()
        self.tableWidget_commandes.setRowCount(numrows)
        self.tableWidget_commandes.setColumnCount(numcols)
        self.tableWidget_commandes.setItem(numrows -1,4, QTableWidgetItem(str(prix_total)))
        self.tableWidget_commandes.setItem(numrows -1,1, QTableWidgetItem(nom_article))
        self.tableWidget_commandes.setItem(numrows -1,2, QTableWidgetItem(quantite))
        self.tableWidget_commandes.setItem(numrows -1,3, QTableWidgetItem(prix_unitaire))
        #except ValueError as erreur_de_valeur:
        #    QMessageBox.warning(QMessageBox(), "Attention", "Veuillez introduire une valeur numérique dans la zone de texte de 'Quantité'")
        #    self.table_commandes.setRowCount(1)

        #self.table_commandes.setItem(numrows -1,1, QTableWidgetItem(nom_article))
        #self.table_commandes.setItem(numrows -1,2, QTableWidgetItem(quantite))
        #self.table_commandes.setItem(numrows -1,3, QTableWidgetItem(prix_unitaire))
        #self.table_commandes.setItem(numrows -1,4, QTableWidgetItem(total))

        #res = 0
        #for j in range(0, self.table_commandes.columnCount()-1):
            #x = self.table_commandes.item(numrows, j).text().strip()
            #if x!="":
                #res += float(x)

        #self.table_commandes.item(numrows, self.table_commandes.columnCount()-1).setText(str(res))
        #self.edit_nom_article.clear()
        #self.edit_quantite.clear()
        #self.edit_prix_unitaire.clear()
        #self.edit_total.clear()

        #def imprimer(self):
        """printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            text = self.edit_nom_client.text()
            #self.edit_nom_client.print_(printer)
            #self.edit_tel_client.print_(printer)
            #self.tableWidget.print_(printer)"""

        ## Blocs des fonctions de test d'impression
    def handlePrint(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QPrintDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePreview(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        document = self.makeTableDocument()
        document.print_(printer)

    def makeTableDocument(self):
        document = QTextDocument()
        cursor = QTextCursor(document)
        rows = self.tableWidget_commandes.rowCount()
        columns = self.tableWidget.columnCount()
        self.tableWidget_commandes = cursor.insertTable(rows + 1, columns)
        format = self.tableWidget_commandes.format()
        format.setHeaderRowCount(1)
        self.tableWidget_commandes.setFormat(format)
        format = cursor.blockCharFormat()
        format.setFontWeight(QFont.Bold)
        for column in range(columns):
            cursor.setCharFormat(format)
            cursor.insertText(self.tableWidget_commandes.horizontalHeaderItem(column).text())
            cursor.movePosition(QTextCursor.NextCell)
        for row in range(rows):
            for column in range(columns):
                cursor.insertText(self.tableWidget_commandes.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        return document
        """def print_preview_dialog(self, printer):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_preview)
        previewDialog.exec_()

        def print_preview(self, printer):
        #self.edit_nom_client.print_(printer)
        #self.edit_tel_client.print_(printer)
        #self.tableWidget.print_(printer)
        #text = self.edit_nom_client.text()"""

    def show_clients(self):
        """Fonction d'ouverture de la page des clients"""
        ## Changement de page
        self.stackedWidget.setCurrentWidget(self.page_clients)
        ## Feuilles de style
        self.bouton_clients.setStyleSheet("""QPushButton {
                                                background-color: rgb(85, 170, 255);
                                                color: rgb(255, 255, 255);
                                                border: 0px solid;
                                                text-align:left;
                                                padding-left:5px;}
                                                """)
        self.bouton_dashboard.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                    """)
        self.bouton_factures.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                """)
        self.bouton_commandes.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                """)
        self.bouton_stock.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                            QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                    """)
        self.bouton_statistiques.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_utilisateurs.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_deconnexion.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}""")

        ## Appel de la fonction d'affichage de la table ayant la liste des clients
        self.listes_clients()

        ## Signaux et Slots
        ## Actualiser la liste des clients
        self.bouton_actualiser_clients.clicked.connect(self.actualiser_liste_clients)

        ## Modifier les informations d'un client
        self.bouton_modifier_clients.clicked.connect(self.modifier_client)

        ## Supprimer un client
        self.bouton_supprimer_clients.clicked.connect(self.supprimer_clients)


    def listes_clients(self):
        """ Fonction de gestion de la table de liste des clients."""

        ## Configuration du QTableWidget
        self.table_liste_clients.setRowCount(5) # Nombre des lignes
        self.table_liste_clients.setColumnCount(3) # Nombre des colonnes
        self.table_liste_clients.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_liste_clients.horizontalHeader().setVisible(False) # Visibilité de la ligne par défaut
        self.table_liste_clients.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        self.table_liste_clients.setFont(QFont("Century Gothic", 14)) # Police
        headers = ["N°","Nom du client", "N° Téléphone"]
        self.table_liste_clients.setHorizontalHeaderLabels(headers)
        header = self.table_liste_clients.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        #header.setStretchLastSection(True)

    def modifier_client(self):
        """Fonction d'affichage de la fenetre de modification des informations du client."""
        self.modifier_client = ModifierClient()
        self.modifier_client.show()

    def actualiser_liste_clients(self):
        """Fonction d'actualisation de la liste des clients."""
        pass

    def supprimer_clients(self):
        pass

    def show_stock(self):
        """Fopassern d'ouverture de la page de stock"""
        ## Gestion de la page de stock

        self.stackedWidget.setCurrentWidget(self.page_stock)
        self.tabWidget_stock.setCurrentIndex(0)
        self.bouton_stock.setStyleSheet("""QPushButton {
                                                background-color: rgb(85, 170, 255);
                                                color: rgb(255, 255, 255);
                                                border: 0px solid;
                                                text-align:left;
                                                padding-left:5px;}
                                                """)
        self.bouton_dashboard.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                    """)
        self.bouton_factures.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                    """)
        self.bouton_commandes.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                    """)
        self.bouton_clients.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                    """)
        self.bouton_statistiques.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_utilisateurs.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_deconnexion.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}""")


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
        self.table_stock.horizontalHeader().setVisible(True) # Visibilité de la ligne par défaut
        self.table_stock.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_stock.setGeometry(QRect(30,150,740,250)) # Position
        #self.table_stock.setFont(QFont('Century Gothic', 14)) # Police
        headers = ["N°","Article", "Types", "Quantité Disponible", "Prix Unitaire","Date de Livraison"]
        self.table_stock.setHorizontalHeaderLabels(headers)
        header = self.table_stock.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        #header.setpasserchLastSection(True)

        ## Signaux et Slots
        ## Actualiser le stock
        self.bouton_actualiser_stock.clicked.connect(self.actualiser_stock)

        ## Modifier le stock
        self.bouton_modifier_stock.clicked.connect(self.modifier_stock)

        ## Supprimer article
        self.bouton_supprimer_stock.clicked.connect(self.supprimer_article)

    def actualiser_stock(self):
        pass

    def modifier_stock(self):
        self.modifier_etat_stock = ModifierEtatStock()
        self.modifier_etat_stock.show()


    def supprimer_article(self):
        pass

    def onglet_des_fournisseurs(self):
        ## Fournisseurs

        ## Configuration du QTableWidget

        self.table_fournisseurs.setRowCount(2) # Nombre des lignes
        self.table_fournisseurs.setColumnCount(6) # Nombre des colonnes
        self.table_fournisseurs.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_fournisseurs.horizontalHeader().setVisible(True) # Visibilité de la ligne par défaut
        self.table_fournisseurs.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_stock.setGeometry(QRect(30,150,740,250)) # Position
        self.table_fournisseurs.setFont(QFont('Century Gothic', 14)) # Police
        headers = ["N°","Nom", "N° Téléphone", "Email", "Adresse","Type de Marchandise"]
        self.table_fournisseurs.setHorizontalHeaderLabels(headers)
        header = self.table_fournisseurs.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        #header.setStretchLastSection(True)

        #header.setStyleSheet("QTableWidget {background:rgb(5,47,97)}")
        ## Actualisation de la table à l'ouverture
        query = "SELECT * FROM liste_des_fournisseurs"
        resultat = connexion.execute(query)
        self.table_fournisseurs.setRowCount(0)
        for row_number, row_data in enumerate(resultat):
            self.table_fournisseurs.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_fournisseurs.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connexion.close


        ## Signaux et Slots
        ## Actulisation de la liste des fournisseurs
        self.bouton_actualiser_fournisseurs.clicked.connect(self.actualiser_liste_fournisseur)

        ## Ajout d'un nouveau fournisseur
        self.bouton_ajouter_fournisseurs.clicked.connect(self.show_page_enregistrer_fournisseur)

        ## Mdofier un fournisseur
        self.bouton_modifier_fournisseur.clicked.connect(self.show_page_modifier_fournisseur)

        ## Supprimer un fournisseur
        self.bouton_supprimer_fournisseur.clicked.connect(self.supprimer_fournisseur)

    def actualiser_liste_fournisseur(self):
        query = "SELECT * FROM liste_des_fournisseurs"
        resultat = connexion.execute(query)
        self.table_fournisseurs.setRowCount(0)
        for row_number, row_data in enumerate(resultat):
            self.table_fournisseurs.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_fournisseurs.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connexion.close


    def show_page_enregistrer_fournisseur(self):
        self.enregistrer_fournisseur = EnregistrerFournisseur()
        self.enregistrer_fournisseur.show()

    def show_page_modifier_fournisseur(self):
        self.modifier_fournisseur = ModifierFournisseur()
        self.modifier_fournisseur.show()

    def supprimer_fournisseur(self):
        self.enregistrer_fournisseur = EnregistrerFournisseur()
        nom_du_fournisseur=self.enregistrer_fournisseur.edit_nom_fournisseur.text()
        num_tel_fournisseur= self.enregistrer_fournisseur.edit_num_fournisseur.text()
        email = self.enregistrer_fournisseur.edit_email_fournisseur.text()
        adresse= self.enregistrer_fournisseur.edit_adresse_fournisseur.text()
        type_marchandise= self.enregistrer_fournisseur.edit_type_marchandise.text()
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
                curseur.execute("""DELETE FROM liste_des_fournisseurs WHERE fournisseur=? AND num_telephone=? AND email=? AND adresse=? AND type_marchandise=?""", (nom_du_fournisseur,num_tel_fournisseur,email,adresse,type_marchandise))
                messageConfirmation="Êtes-vous sûr de vouloir supprimer cet article ?"
                self.reponse = QMessageBox.question(self ,"Confirmation",
                messageConfirmation,QMessageBox.Yes,QMessageBox.No)
                if self.reponse == QMessageBox.Yes:
                    self.supprimer_fournisseur()
                    self.actualiser_liste_fournisseur()
                else:
                    return False

    def onglet_des_livraisons(self):

        # Configuration du QTableWidget
        # TableWidget livraisons
        self.table_livraisons.setRowCount(5) # Nombre des lignes
        self.table_livraisons.setColumnCount(10) # Nombre des colonnes
        self.table_livraisons.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_livraisons.horizontalHeader().setVisible(True) # Visibilité de la ligne par défaut
        self.table_livraisons.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_livraisons.setGeometry(QRect(30,150,740,250)) # Position
        self.table_livraisons.setFont(QFont('Century Gothic', 14)) # Police
        headers = ["N°","Article", "Type", "Bon de Livraison", "Fournisseur","Fabricant","Date de Livraison","Quantité Livrée","Prix Unitaire", "Prix Total"]
        self.table_livraisons.setHorizontalHeaderLabels(headers)
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
        query = "SELECT * FROM liste_des_livraisons"
        resultat = connexion.execute(query)
        self.table_livraisons.setRowCount(0)
        for row_number, row_data in enumerate(resultat):
            self.table_livraisons.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_livraisons.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            connexion.close


        # Nouvelle Livraisons
        self.bouton_nouvelle_livraison.clicked.connect(self.nouvellelivraison)

        # Actualiser
        self.bouton_actualiser_livraison.clicked.connect(self.actualiser_livraison)

        # Modifier Livraison
        self.bouton_modifier_livraison.clicked.connect(self.show_page_modifier_livraison)

    def actualiser_livraison(self):
        query = "SELECT * FROM liste_des_livraisons"
        resultat = connexion.execute(query)
        self.table_livraisons.setRowCount(0)
        for row_number, row_data in enumerate(resultat):
            self.table_livraisons.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table_livraisons.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            connexion.close

    def show_page_modifier_livraison(self):
        modifier_livraison = ModifierLivraison()
        modifier_livraison.setModal(True)
        modifier_livraison.exec()

    def nouvellelivraison(self):
        nouvelle_livraison = NouvelleLivraison()
        nouvelle_livraison.setModal(True)
        nouvelle_livraison.exec()

    def show_statistiques(self):
        """Fonctions d'ouverture de la page des statistiques"""
        self.stackedWidget.setCurrentWidget(self.page_statistiques)
        self.tabWidget_statistiques.setCurrentIndex(0)
        self.bouton_statistiques.setStyleSheet("""QPushButton {
                                                        background-color: rgb(85, 170, 255);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                        """)
        self.bouton_dashboard.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_factures.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_commandes.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_clients.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_stock.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                            QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_utilisateurs.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)
        self.bouton_deconnexion.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)

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
        headers = ["N°","Article", "Quantité Vendue", "Prix Unitaire", "Prix Total","Date de Vente"]
        self.table_ventes.setHorizontalHeaderLabels(headers)
        header = self.table_ventes.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

    def onglet_des_recettes(self):
        # Configuration du QTableWidget

        self.table_recettes.setRowCount(5) # Nombre des lignes
        self.table_recettes.setColumnCount(6) # Nombre des colonnes
        self.table_recettes.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_recettes.horizontalHeader().setVisible(True) # Visibilité de la ligne par défaut
        self.table_recettes.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_liste_utilisateurs.setGeometry(QRect(30,100,650,201)) # Position
        self.table_recettes.setFont(QFont('Century Gothic', 14)) # Police
        headers = ["N°","Article", "Quantité Vendue", "Prix d'Achat", "Prix de Vente","Bénéfice"]
        self.table_recettes.setHorizontalHeaderLabels(headers)
        header = self.table_recettes.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

    def show_utilisateurs(self):
        """Fonction d'ouverture de la page d'utilisateurs"""
        self.stackedWidget.setCurrentWidget(self.page_utilisateurs)
        self.bouton_utilisateurs.setStyleSheet("""QPushButton {
                                                        background-color: rgb(85, 170, 255);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                        """)
        self.bouton_dashboard.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                    """)
        self.bouton_factures.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                    """)
        self.bouton_commandes.setStyleSheet("""QPushButton {
                                                    background-color: rgb(35, 35, 35);
                                                    color: rgb(255, 255, 255);
                                                    border: 0px solid;
                                                    text-align:left;
                                                    padding-left:5px;}
                                                QPushButton:hover {
                                                    background-color: rgb(85, 170, 255);}
                                                    """)
        self.bouton_clients.setStyleSheet("""QPushButton {
                                                background-color: rgb(35, 35, 35);
                                                color: rgb(255, 255, 255);
                                                border: 0px solid;
                                                text-align:left;
                                                padding-left:5px;}
                                            QPushButton:hover {
                                                background-color: rgb(85, 170, 255);}
                                                """)
        self.bouton_stock.setStyleSheet("""QPushButton {
                                                background-color: rgb(35, 35, 35);
                                                color: rgb(255, 255, 255);
                                                border: 0px solid;
                                                text-align:left;
                                                padding-left:5px;}
                                            QPushButton:hover {
                                                background-color: rgb(85, 170, 255);}
                                                """)
        self.bouton_statistiques.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}""")
        self.bouton_deconnexion.setStyleSheet("""QPushButton {
                                                        background-color: rgb(35, 35, 35);
                                                        color: rgb(255, 255, 255);
                                                        border: 0px solid;
                                                        text-align:left;
                                                        padding-left:5px;}
                                                    QPushButton:hover {
                                                        background-color: rgb(85, 170, 255);}
                                                        """)

        ## Table des utilisateurs
        self.liste_des_utilisateurs()

        ## Signaux et Slots
        ## Actualiser la liste des utilisateurs
        self.bouton_actualiser_utilisateur.clicked.connect(self.actualiser_liste_utilisateurs)

        ## Modifier les informations d'utilisateur
        self.bouton_modifier_utilisateur.clicked.connect(self.modifier_utilisateur)

        ## Supprimer un utilisateur
        self.bouton_supprimer_utilisateur.clicked.connect(self.supprimer_utilisateur)

        ## Signal et Slot pour afficher les contenus de la ligne sélectionnée
        self.table_liste_utilisateurs.clicked.connect(self.seeindex_user)

        ## Enregistrer les modificactions
        self.save_changes.clicked.connect(self.save)

    def liste_des_utilisateurs(self):

        """# Configuration du QTableWidget
        #self.table_liste_utilisateurs = QTableWidget(self)
        self.table_liste_utilisateurs.setRowCount(5) # Nombre des lignes
        self.table_liste_utilisateurs.setColumnCount(5) # Nombre des colonnes
        self.table_liste_utilisateurs.verticalHeader().setVisible(False) # Visibilité de la colonne par défaut
        self.table_liste_utilisateurs.horizontalHeader().setVisible(True) # Visibilité de la ligne par défaut
        self.table_liste_utilisateurs.setStyleSheet("QTableWidget {background:white}")# Mise en forme de l'arrière-plan
        #self.table_liste_utilisateurs.setGeometry(QRect(30,100,650,201)) # Position
        self.table_liste_utilisateurs.setFont(QFont('Century Gothic', 14)) # Police
        headers = ["N°","Nom D'utilisateur", "Type de Compte", "ID Agent", "ID Administrateur"]
        self.table_liste_utilisateurs.setHorizontalHeaderLabels(headers)
        #self.table_liste_utilisateurs.horizontalHeader.setFont(QFont('Century Gothic', 14))
        header = self.table_liste_utilisateurs.horizontalHeader() # Element pour la configuration de la taille des colonnes
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Avec ResizeToContents, les colonnes seront rédimensionnées selon leurs contenus
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        ## header.setStretchLastSection(True)"""
        ## Connexion à la table 'utilisateurs'
        self.model = QSqlTableModel()
        self.model.setTable("utilisateurs") ## Sélection de la table
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, u"N°")
        self.model.setHeaderData(1, Qt.Horizontal, u"Nom d'utilisateurs")
        self.model.setHeaderData(2, Qt.Horizontal, u"Mot de passe")
        self.model.setHeaderData(3, Qt.Horizontal, u"Mot de passe")
        self.model.setHeaderData(4, Qt.Horizontal, u"Type de compte")
        self.model.setHeaderData(5, Qt.Horizontal, u"ID Admin")
        self.model.setHeaderData(6, Qt.Horizontal, u"ID Agent")
        self.model.setHeaderData(7, Qt.Horizontal, u"N° Téléphone")
        self.model.setEditStrategy(QSqlRelationalTableModel.OnManualSubmit)

        font = QFont("Century Gothic", 14) ## Police
        self.table_liste_utilisateurs.setFont(font)
        self.table_liste_utilisateurs.setModel(self.model) ## Affectation du modèle au tableau
        self.table_liste_utilisateurs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_liste_utilisateurs.horizontalHeader().setStretchLastSection(True )
        self.table_liste_utilisateurs.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_liste_utilisateurs.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table_liste_utilisateurs.setColumnHidden(2, True)
        self.table_liste_utilisateurs.setColumnHidden(3, True)
        #self.table_liste_utilisateurs.setEditStrategy(QSqlRelationalTableModel.OnManualSubmit)


    def actualiser_liste_utilisateurs(self):
        """Fonction d'actualisation de la liste des utilisateurs."""
        ## Connexion à la table 'utilisateurs'
        self.model = QSqlTableModel()
        self.model.setTable("utilisateurs") ## Sélection de la table
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, u"N°")
        self.model.setHeaderData(1, Qt.Horizontal, u"Nom d'utilisateurs")
        self.model.setHeaderData(2, Qt.Horizontal, u"Mot de passe")
        self.model.setHeaderData(3, Qt.Horizontal, u"Mot de passe")
        self.model.setHeaderData(4, Qt.Horizontal, u"Type de compte")
        self.model.setHeaderData(5, Qt.Horizontal, u"ID Admin")
        self.model.setHeaderData(6, Qt.Horizontal, u"ID Agent")
        self.model.setHeaderData(7, Qt.Horizontal, u"N° Téléphone")
        font = QFont("Century Gothic", 14)
        self.table_liste_utilisateurs.setFont(font)
        self.table_liste_utilisateurs.setModel(self.model)
        self.table_liste_utilisateurs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_liste_utilisateurs.horizontalHeader().setStretchLastSection(True )
        self.table_liste_utilisateurs.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_liste_utilisateurs.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table_liste_utilisateurs.setColumnHidden(2, True)
        self.table_liste_utilisateurs.setColumnHidden(3, True)

        #header.setStretchLastSection(True)

    def seeindex_user(self,index=None):
        """Fonction permettant de récuperer l'index(le contenu) de la ligne sélectionnée"""
        index.column = 5
        row = index.row()
        col1 = self.model.record(row).field(1).value()
        col2 = self.model.record(row).field(4).value()
        col3 = self.model.record(row).field(5).value()
        col4 = self.model.record(row).field(6).value()
        self.lineEdit_3.setText(str(col1))
        self.lineEdit_4.setText(str(col2))
        self.lineEdit_5.setText(str(col3))
        self.lineEdit_6.setText(str(col4))

    def save(self, user):
        user = self.lineEdit_3.text()
        type = self.lineEdit_4.text()
        id_admin = self.lineEdit_5.text()
        id_user = self.lineEdit_6.text()
        QSqlQuery("""UPDATE utilisateurs SET nom_utilisateur ='{}'
        WHERE nom_utilisateur ='{}'""".format([user]))#,type,id_admin,id_user))#,type_compte='{}',id_admin='{}',id_user'{}'
        self.actualiser_liste_utilisateurs()

    def modifier_utilisateur(self):
        """Fonction de modification des informations d'utilisateur."""
        self.modifier_utilisateur = ModifierUtilisateur()
        self.modifier_utilisateur.show()

    def supprimer_utilisateur(self):
        """Fonction de suppression d'utilisateur."""
        self.model = QSqlTableModel()
        self.model.setTable("utilisateurs") ## Sélection de la table
        self.model.select()
        index = self.table_liste_utilisateurs.currentIndex() ## Index courant
        indices = self.table_liste_utilisateurs.selectionModel().selectedRows()
        for index in sorted(indices):
            messageConfirmation="Êtes-vous sûr de vouloir supprimer cet utilisateur ?"
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
                self.model.removeRow(index.row())
                self.model.submitAll()
                curseur.execute("""DELETE FROM utilisateurs""")
                curseur.execute("""DELETE FROM sqlite_sequence WHERE NAME='utilisateurs' """)
                curseur.execute("""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='utilisateurs' """)
                self.actualiser_liste_utilisateurs()
            else:
                return False



    def closeEvent(self, event=None):
        messageConfirmation="Êtes-vous sûr de vouloir quitter ?"
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
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
