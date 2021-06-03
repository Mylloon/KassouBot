import sqlite3

class Database:

    def __init__(self):
        path = "src/db/bot.sqlite3"
        if not self.isDatabaseExists(path):
            self.createDB(path)
        self.con = sqlite3.connect(path)
        print("DB Open")

    def isDatabaseExists(self, path):
        try:
            open(path, "r")
        except FileNotFoundError:
            return False
        else:
            return True

    def createDB(self, path):
        print("Creating DB...")
        open(path, "x")
