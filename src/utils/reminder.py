from utils.db import Database

class Reminder(Database):
    def __init__(self):
        super().__init__(r"src/db/bot.sqlite3")

    def creationTable(self):
        """Créer la table qui stocker les reminders"""
        requete = """
                  CREATE TABLE IF NOT EXISTS reminder (
                      id INTEGER PRIMARY KEY,
                      message_id INTEGER,
                      channel_id INTEGER,
                      mention_bool INTEGER,
                      reminder_str TEXT,
                      creation_int INTEGER,
                      expiration_int INTEGER,
                      user_id INTEGER,
                      guild_id INTEGER
                  );
                  """
        self.requete(requete)
    
    def ajoutReminder(self, messageID = int, channelID = int, mention = int, reminder = str, creation = int, expiration = int, userID = int, guildID = int):
        """Ajoute un reminder"""
        requete = """
                  INSERT INTO reminder (
                      message_id, channel_id, mention_bool, reminder_str, creation_int, expiration_int, user_id, guild_id
                  ) VALUES (
                      ?, ?, ?, ?, ?, ?, ?, ?
                  );
                  """
        self.requete(requete, [messageID, channelID, mention, reminder, creation, expiration, userID, guildID])
    
    def suppressionReminder(self, id = int):
        """Supprime un reminder"""
        requete = """
                  DELETE FROM reminder
                  WHERE id = ?
                  """
        self.requete(requete, id)

    def listeReminder(self, userID = int, guildID = int):
        """Retourne la liste des reminders d'un utilisateur"""
        requete = """
                  SELECT reminder_str, creation_int, expiration_int FROM reminder
                  WHERE user_id = ? AND guild_id = ?
                  """
        return self.affichageResultat(self.requete(requete, [userID, guildID]))

    def recuperationExpiration(self, time = int):
        """Récupère les reminders qui sont arrivés à expiration et ses infos"""
        requete = """
                  SELECT channel_id, mention_bool, reminder_str, creation_int, user_id, id, message_id FROM reminder
                  WHERE expiration_int < ?
                  """
        return self.affichageResultat(self.requete(requete, time))
