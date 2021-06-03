import sqlite3

class Database:
    def __init__(self):
        self.connexion = self.createConnection(r"src/db/bot.sqlite3")
        self.curseur = self.connexion.cursor()

    def createConnection(self, path):
        """Connexion à une base de donnée SQLite"""
        if not self.isFileExists(path):
            open(path, "x")
        connnexion = None
        try:
            connnexion = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(e)
        return connnexion

    def isFileExists(self, path):
        """Vérifie qu'un fichier existe"""
        try:
            open(path, "r")
        except FileNotFoundError:
            return False
        else:
            return True

    def requete(self, requete, valeurs = None):
        """Envois une requête vers la base de données"""
        try:
            if valeurs:
               self.curseur.execute(requete, valeurs) 
            else:
                self.curseur.execute(requete)
            self.connexion.commit()
            return self.curseur.lastrowid
        except sqlite3.Error as e:
            print(e)
