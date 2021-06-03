import sqlite3
from pathlib import Path

class Database:

    def __init__(self):
        path = Path("src/db/bot.sqlite3").absolute()
        if not self.isDatabaseExists(path):
            self.createDB(path)
        self.con = sqlite3.connect(path)
        print("DB Open")

    def isDatabaseExists(self, path):
        try:
            Path(path).resolve(strict = True)
        except FileNotFoundError:
            return False
        else:
            return True

    def createDB(self, path):
        print("Creating DB...")
        open(path, "x")
