import os
import sys

from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget, QDialog, QMessageBox, QLineEdit, QPushButton, QStackedWidget, QFrame, QCompleter, QMessageBox
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QBrush, QPalette, QImage, QIcon, QFont
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalDelegate, QSqlRelationalTableModel, QSqlTableModel
import sqlite3
from main import *


"""def createConnection():
    dbExist=os.path.exists('idatabase.db')
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('idatabase.db')
    db.open()
    print (db.lastError().text())
    return True
    QSqlQuery('''CREATE TABLE IF NOT EXISTS utilisateurs(id INTEGER PRIMARY KEY AUTOINCREMENT, nom_utilisateur TEXT, mot_de_passe TEXT, confirm_mot_de_passe TEXT, type_compte TEXT, id_admin INTEGER, id_user INTEGER )''')"""
connexion = sqlite3.connect('idatabase.db')
curseur = connexion.cursor()

class LoginUser(QDialog):
    def __init__(self, parent=None):
        super(LoginUser, self).__init__(parent)
        loadUi("login_dialog.ui", self)

        self.resize(640,480) # Taille de la fenetre à l'ouverture
        self.setMaximumSize(640,480) # Taille maximum de la fenetre
        self.setMinimumSize(640,480) # Taille minimun de la fenetre
        self.setWindowTitle("Connexion") # Titre de la fenetre
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon("./icones/icone_workspace.ico"))

        # Page par défaut à l'ouverture
        self.stackedWidget.setCurrentIndex(0)

        # Afficher le mode d'écriture de mot de passe
        self.edit_password.setEchoMode(QLineEdit.Password)

        # Afficher un titre en fond
        self.edit_username.setPlaceholderText("Saisissez votre nom d'utilisateur")
        self.edit_password.setPlaceholderText("Saisissez votre mot de passe")

        # Signal pour le bouton connexion
        self.bouton_connexion.clicked.connect(self.connection)

        # Signal pour le bouton de création de compte
        self.bouton_creer_compte.clicked.connect(self.creer_compte)

        #self.widget = MainWindow()



    def connection(self):
        """Fonction permettant de se connecter à la page principale."""
        username = self.edit_username.text()# Affectation de la variable du nom d'utilisateur par défaut
        password = self.edit_password.text() # Affectation de la variable de Mot de passe

        ## Condition de vérification d'existence de l'utilisateur et du mot de passe pour se connecter
        resultat =  curseur.execute("""SELECT * FROM utilisateurs WHERE nom_utilisateur = ? AND mot_de_passe = ?""",(username,password))
        if (len(resultat.fetchall())>0):
            self.message = QMessageBox()
            self.message.setText("Connecté")
            self.message.setWindowTitle("Info")
            self.message.setIcon(QMessageBox.Information)
            #self.message.setStyleSheet("background-color: rgb(255,255,255);")
            #self.message.setStyleSheet("QPushButton {background:gray;}")
            self.message.setWindowIcon(QIcon("icone_info.ico"))
            self.message.setIcon(QMessageBox.Information)
            self.message.exec_()
            self.widget = MainWindow()
            self.widget.show()
            self.widget.showNormal()
            self.lower()
            #self.close()
            #self.destroy()

            # Effacer les textes après traitement
            self.edit_username.clear()
            self.edit_password.clear()
            # Focus
            self.edit_username.setFocus()

        else:
            QMessageBox.warning(self,"Attention", "Nom d'utilisateur ou Mot de passe incorrect.")
            # Effacer les textes après traitement
            self.edit_username.clear()
            self.edit_password.clear()
            # Focus
            self.edit_username.setFocus()




        """
        # Signal pour le bouton de mot de passe oublié
        self.passwordforgot.clicked.connect(self.oublie)
        # Forme du curseur
        self.passwordforgot.setCursor(Qt.PointingHandCursor)
        self.passwordforgot.setStyleSheet("QPushButton {background:transparent}")

        # Signal pour le bouton de création de compte
        self.boutoncreatecount.clicked.connect(self.creer_compte)

        # Forme du curseur
        self.boutoncreatecount.setCursor(Qt.PointingHandCursor)

    def oublie(self):
        QMessageBox.information(self, "Info", "Mot de passe oublié.")"""

    def creer_compte(self):
        """Fonction permettant l'accès à la page de choix de création de type de compte."""

        # Page par défaut à l'ouverture
        self.stackedWidget.setCurrentIndex(1)
        # Changement du titre de la fenetre
        self.setWindowTitle("Créer un compte")
        self.setWindowIcon(QIcon("./icones/icone_creer_compte.ico"))

        self.bouton_suivant_creation.clicked.connect(self.show_type_compte_admin)
        self.bouton_suivant_creation.clicked.connect(self.show_type_compte_agent)
        self.bouton_annuler_choix.clicked.connect(self.annuler_choix)


    def annuler_choix(self, event=None):
        """Fonction permettant l'annulation d'un choix de compte et ramenant à la page principale de connexion."""
        messageConfirmation="Êtes-vous sûr de vouloir annuler ?"
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
            #event.accept()
            self.stackedWidget.setCurrentIndex(0)
            self.setWindowTitle("Connexion")
            self.setWindowIcon(QIcon("./icones/icone_workspace.ico"))
        else:
            #event.ignore()
            return False

    def show_type_compte_admin(self):
        """Fonction affichant la page de création du compte administrateur."""
        if self.radio_butoon_choix_admin.isChecked():
            self.stackedWidget.setCurrentIndex(2)
            self.setWindowTitle("Créer un compte Administrateur")
            self.setWindowIcon(QIcon("./icones/icone_add_admin.ico"))


        #self.bouton_annuler_admin.clicked.connect(self.annulation_creation_compte_admin)
        self.bouton_creer_admin.clicked.connect(self.creer_compte_admin)


    def creer_compte_admin(self):
        """Fonction permettant la création d'un compte administrateur."""
        ## Affectation des variables aux zones de texte
        username_admin = self.edit_username_admin.text()
        id_admin = int(self.edit_id_admin.text())
        tel_admin = int(self.edit_tel_admin.text())
        password1 = self.edit_password_admin.text()
        password_confirm = self.edit_password_admin1.text()
        found = 0
        while found==0:
            ## Connexion à la base de données pour vérifier l'existence d'un enregistrement avant d'ajouter un nouveau compte administrateur, cette fonction vérifie si l'enregistrement existe dans le champ 'nom_utilisateur"
            connexion = sqlite3.connect('idatabase.db') ## Connexion à la base des données
            curseur = connexion.cursor()
            ## Sélection du champ 'nom_utilisateur.
            findUser = ("""SELECT * FROM utilisateurs WHERE nom_utilisateur=?""")
            curseur.execute(findUser,[username_admin])
            if (len(curseur.fetchall())!=0):
                ## Parcours de la table
                self.message = QMessageBox()
                self.message.setText("Nom d'utilisateur ou ID Admin déjà utilisés, choisissez un autre.")
                self.message.setWindowTitle("Attention")
                self.message.setIcon(QMessageBox.Warning)
                self.message.setStyleSheet("background-color: rgb(255,255,255);")
                #self.message.setStyleSheet("QPushButton {background:gray;}")
                self.message.setWindowIcon(QIcon("icone_attention.ico"))
                self.message.setIcon(QMessageBox.Warning)
                bouton_ok = self.message.button(QMessageBox.Ok)
                self.message.exec_()
                if self.message.clickedButton()==bouton_ok:
                    self.edit_username_admin.clear()
                    self.edit_id_admin.clear()
                    self.edit_tel_admin.clear()
                    self.edit_password_admin.clear()
                    self.edit_password_admin1.clear()
                    self.edit_username_admin.setFocus()
                else:
                    return False
            else:
                found=1
        if self.edit_password_admin.text()!=self.edit_password_admin1.text():
            ## Vérification de la correspondance entre les duex mots de passe
            self.message = QMessageBox()
            self.message.setText("Les mots de passe ne correspondent pas.")
            self.message.setWindowTitle("Erreur")
            self.message.setIcon(QMessageBox.Warning)
            self.message.setStyleSheet("background-color: rgb(255,255,255);")
            self.message.setStyleSheet("QPushButton {background:gray;}")
            self.message.setWindowIcon(QIcon("icone_attention.ico"))
            self.message.setIcon(QMessageBox.Warning)
            self.message.exec_()
            self.edit_username_admin.clear()
            self.edit_id_admin.clear()
            self.edit_tel_admin.clear()
            self.edit_password_admin.clear()
            self.edit_password_admin1.clear()
            self.edit_username_admin.setFocus()
        try:
            ##  Vérification de la connexion à la base des données
            connexion = sqlite3.connect('idatabase.db')
            curseur = connexion.cursor()
            ## Enregistrement d'un nouvel utilisateur dans la base des données
            curseur.execute("""INSERT INTO utilisateurs (nom_utilisateur,mot_de_passe,confirm_mot_de_passe,type_compte,id_admin,id_user,tel_admin) VALUES(?,?,?,?,?,?,?)""",[username_admin,password1,password_confirm,'Administrateur',id_admin,'--',tel_admin])
            connexion.commit()
            curseur.close()
            connexion.close() ## Fermeture de la connexion à la base des données
            ## Message de  confirmation de création de compte
            self.message = QMessageBox()
            self.message.setText("Compte Crée.")
            self.message.setWindowTitle("Félicitations")
            self.message.setIcon(QMessageBox.Information)
            self.message.setStyleSheet("background-color: rgb(255,255,255);")
            self.message.setStyleSheet("QPushButton {background:gray;}")
            self.message.setWindowIcon(QIcon("icone_info.ico"))
            self.message.setIcon(QMessageBox.Information)
            self.message.exec_()
            self.edit_username_admin.clear()
            self.edit_id_admin.clear()
            self.edit_tel_admin.clear()
            self.edit_password_admin.clear()
            self.edit_password_admin1.clear()
            self.edit_username_admin.setFocus()
        except sqlite3.OperationalError as exception_retournee:
            print("Voici l'erreur :", exception_retournee)
            self.message = QMessageBox()
            self.message.setText("Une erreur est survenue due à "+ str(exception_retournee))
            self.message.setWindowTitle("Erreur")
            self.message.setIcon(QMessageBox.Information)
            self.message.setStyleSheet("background-color: rgb(255,255,255);")
            self.message.setStyleSheet("QPushButton {background:gray;}")
            self.message.setWindowIcon(QIcon("icone_info.ico"))
            self.message.setIcon(QMessageBox.Information)
            self.message.exec_()


    def annulation_creation_compte_admin(self,event=None):
        """Fonction d'annulation de création de compte administrateur."""
        messageConfirmation="Êtes-vous sûr de vouloir annuler ?"
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
            self.stackedWidget.setCurrentIndex(1)
            self.setWindowTitle("Créer un compte")
            self.setWindowIcon(QIcon("./icones/icone_creer_compte.ico"))
        else:
            return False


    def show_type_compte_agent(self):
        """Fonction affichant la page de création de compte agent"""
        if self.radion_bouton_choix_agent.isChecked():
            ## Condition au cas de sélection du radio button

            ## Affichage de la page de création de compte agent
            self.stackedWidget.setCurrentIndex(3)

            ## Modification du titre de la fenêtre
            self.setWindowTitle("Créer un compte Agent")
            self.setWindowIcon(QIcon("./icones/icone_add_agent.ico"))

        ## Signaux et Slots

        ## Signal du clic du bouton de création de compte
        self.bouton_creer_agent.clicked.connect(self.creer_compte_agent)

        ## Signal du clic du bouton d'annulation de création
        self.bouton_annuler_agent.clicked.connect(self.annulation_creation_compte_agent)

    def creer_compte_agent(self):
        """Fonction permettant la création du compte agent"""
        ## Affectation des variables
        username_agent = self.edit_username_agent.text()
        id_agent = self.edit_id_agent.text()
        num_agent = self.edit_tel_agent.text()
        password_agent = self.edit_password_agent.text()
        password_agent1 = self.edit_password_agent1.text()

        found = 0
        while found==0:
            connexion = sqlite3.connect('idatabase.db')
            curseur = connexion.cursor()
            ## Sélection du champ
            findUser = ("""SELECT * FROM utilisateurs WHERE nom_utilisateur=?""")
            curseur.execute(findUser,[username_agent])
            if (len(curseur.fetchall())!=0):
                self.message = QMessageBox()
                self.message.setText("Nom d'utilisateur ou ID Agent déjà utilisés, choisissez un autre.")
                self.message.setWindowTitle("Attention")
                self.message.setIcon(QMessageBox.Warning)
                self.message.setStyleSheet("background-color: rgb(255,255,255);")
                self.message.setStyleSheet("QPushButton {background:gray;}")
                self.message.setWindowIcon(QIcon("icone_attention.ico"))
                self.message.setIcon(QMessageBox.Warning)
                bouton_ok = self.message.button(QMessageBox.Ok)
                self.message.exec_()
                if self.message.clickedButton()==bouton_ok:
                    self.edit_username_agent.clear()
                    self.edit_id_agent.clear()
                    self.edit_tel_agent.clear()
                    self.edit_password_agent.clear()
                    self.edit_password_agent1.clear()
                    self.edit_username_agent.setFocus()
                else:
                    return False
            else:
                found=1
        if password_agent!=password_agent1:
            self.message = QMessageBox()
            self.message.setText("Les mots de passe ne correspondent pas.")
            self.message.setWindowTitle("Erreur")
            self.message.setIcon(QMessageBox.Warning)
            self.message.setStyleSheet("background-color: rgb(255,255,255);")
            self.message.setStyleSheet("QPushButton {background:gray;}")
            self.message.setWindowIcon(QIcon("icone_attention.ico"))
            self.message.setIcon(QMessageBox.Warning)
            self.message.exec_()
            self.edit_username_agent.clear()
            self.edit_id_agent.clear()
            self.edit_tel_agent.clear()
            self.edit_password_agent.clear()
            self.edit_password_agent1.clear()
            self.edit_username_agent.setFocus()
        try:
            connexion = sqlite3.connect('idatabase.db')
            curseur = connexion.cursor()
            ## Enregistrement dans la base des données
            curseur.execute("""INSERT INTO utilisateurs (nom_utilisateur,mot_de_passe,confirm_mot_de_passe,type_compte,id_admin,id_user,tel_admin) VALUES(?,?,?,?,?,?,?)""",[username_agent,password_agent,password_agent1,'Agent','--',id_agent,num_agent])
            connexion.commit()
            curseur.close()
            connexion.close()
            self.message = QMessageBox()
            self.message.setText("Compte Crée.")
            self.message.setWindowTitle("Félicitations")
            self.message.setIcon(QMessageBox.Information)
            self.message.setWindowIcon(QIcon("icone_info.ico"))
            self.message.setIcon(QMessageBox.Information)
            self.message.exec_()
            self.edit_username_agent.clear()
            self.edit_id_agent.clear()
            self.edit_tel_agent.clear()
            self.edit_password_agent.clear()
            self.edit_password_agent1.clear()
            self.edit_username_agent.setFocus()
        except sqlite3.OperationalError as exception_retournee: #
            #print("Voici l'erreur :", exception_retournee)
            self.message = QMessageBox()
            self.message.setText("Une erreur est survenue due à "+str(exception_retournee))
            self.message.setWindowTitle("Erreur")
            self.message.setIcon(QMessageBox.Information)
            self.message.setWindowIcon(QIcon("icone_info.ico"))
            self.message.setIcon(QMessageBox.Information)
            self.message.exec_()
            self.edit_username_agent.clear()
            self.edit_id_agent.clear()
            self.edit_tel_agent.clear()
            self.edit_password_agent.clear()
            self.edit_password_agent1.clear()
            self.edit_username_agent.setFocus()

    def annulation_creation_compte_agent(self,event=None):
        """Fonction de l'annulation de création d'un compte agent."""
        messageConfirmation="Êtes-vous sûr de vouloir annuler ?"
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
            self.stackedWidget.setCurrentIndex(1)
            self.setWindowTitle("Créer un compte")
            self.setWindowIcon(QIcon("./icones/icone_creer_compte.ico"))
        else:
            return False

    def closeEvent(self, event=None):
        """Fonction de récupération de l'événement à la fermeture de la fenêtre."""
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
    widget1 = LoginUser()
    widget1.setWindowTitle("Connexion")
    widget1.show()
    sys.exit(app.exec())

