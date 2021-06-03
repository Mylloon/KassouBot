from db import Database

class Reminder(Database):
    def creationTable(self):
        requete = """
                  CREATE TABLE IF NOT EXISTS reminder (
                      id INTEGER PRIMARY KEY,
                      guild_id INTEGER,
                      channel_id INTEGER,
                      mention_bool INTEGER,
                      reminder_str TEXT,
                      creation_str INTEGER,
                      expiration_int INTEGER,
                      user_id INTEGER
                  );
                  """
        self.requete(requete)
    
    def ajoutReminder(self, guildID, channelID, mention, reminder, creation, expiration, userID):
        requete = """
                  INSERT INTO reminder (
                      guild_id, channel_id, mention_bool, reminder_str, creation_str, expiration_int, user_id
                  ) VALUES (
                      ?, ?, ?, ?, ?, ?, ?
                  );
                  """
        self.requete(requete, (guildID, channelID, mention, reminder, creation, expiration, userID))
    
    def suppressionReminder(self, id):
        requete = """
                  DELETE FROM reminder
                  WHERE id = ?
                  """
        self.requete(requete, id)
