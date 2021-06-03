from utils.db import Database

class Reminder(Database):
    def creationTable(self):
        """Créer la table qui stocker les reminders"""
        requete = """
                  CREATE TABLE IF NOT EXISTS reminder (
                      id INTEGER PRIMARY KEY,
                      guild_id INTEGER,
                      channel_id INTEGER,
                      mention_bool INTEGER,
                      reminder_str TEXT,
                      creation_int INTEGER,
                      expiration_int INTEGER,
                      user_id INTEGER
                  );
                  """
        self.requete(requete)
    
    def ajoutReminder(self, guildID, channelID, mention, reminder, creation, expiration, userID):
        """Ajoute un reminder"""
        requete = """
                  INSERT INTO reminder (
                      guild_id, channel_id, mention_bool, reminder_str, creation_int, expiration_int, user_id
                  ) VALUES (
                      ?, ?, ?, ?, ?, ?, ?
                  );
                  """
        self.requete(requete, (guildID, channelID, mention, reminder, creation, expiration, userID))
    
    def suppressionReminder(self, id):
        """Supprime un reminder"""
        requete = """
                  DELETE FROM reminder
                  WHERE id = ?
                  """
        self.requete(requete, id)

    def listeReminder(self, userID = None):
        """Retourne la liste des reminders, si un userID est mentionné, retourne la liste de cet utilisateur"""
        return

    def recuperationReminder(self, id):
        """Récupère les informations d'un reminder"""
        return
