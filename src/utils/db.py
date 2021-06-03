import sqlite3

class Database:
    def __init__(self):
        self.curseur = self.createConnection("src/db/bot.sqlite3").cursor()

    def createConnection(self, path):
        """Connexion à une base de donnée SQLite"""
        if not self.isFileExists(path):
            open(path, "x")
        connnexion = None
        try:
            connnexion = sqlite3.connect(path)
            print(f"Database connected with SQLite v{sqlite3.version}")
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

    def requete(self, requete):
        """Reqête vers la base de données"""
        try:
            self.curseur.execute(requete)
        except sqlite3.Error as e:
            print(e)
