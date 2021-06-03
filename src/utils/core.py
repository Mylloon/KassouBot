import re
import json
import requests
import time
import os
from pytz import timezone
from datetime import datetime, timedelta

myTimezone = os.environ['TIMEZONE']

def goodTimezone(date, type, tz):
    """renvoie une date en fonction d'un timezone"""
    if type == 0:
        return str(timezone(tz).fromutc(date))[:-13].replace('-', '/').split()
    elif type == 1:
        return str(timezone(tz).fromutc(date))[:-13].replace('-', '/').replace(' ', ' à ')

def map_list_among_us(map):
    """Sélecteur de map pour la commande amongus⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
    maps = {}
    maps["skeld"] = ["skeld", "the skeld", "theskeld"]
    maps["mira"] = ["mira", "mira hq", "mirahq"]
    maps["polus"] = ["polus"]
    maps["airship"] = ["airship", "air ship"]
    if map == "all":
        return maps["skeld"] + maps["mira"] + maps["polus"] + maps["airship"]
    return maps[map]

def get_age(date):
    """Recupère un age précisément à la seconde près"""
    joursRestants = datetime.now() - date
    years = joursRestants.total_seconds() / (365.242 * 24 * 3600)
    months = (years - int(years)) * 12
    days = (months - int(months)) * (365.242 / 12)
    hours = (days - int(days)) * 24
    minutes = (hours - int(hours)) * 60
    seconds = (minutes - int(minutes)) * 60
    return (int(years), int(months), int(days),  int(hours), int(minutes), int(seconds))

def ageLayout(tuple):
    """avec la méthode 'get_age', permet de mettre en forme un âge⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
    time = {}
    time[0], time[1], time[2], time[3], time[4], time[5] = "an", "mois", "jour", "heure", "minute", "seconde"
    for i in range(len(tuple)):
        if tuple[i] > 1 and i != 1:
            time[i] = time[i] + "s"
    message = ""
    if tuple[5] > 0: # pour les secondes
        affichage = [5] # on affiche que : seconde
    if tuple[4] > 0:
        affichage = [4, 5] # on affiche : minute + seconde
    if tuple[3] > 0:
        affichage = [3, 4, 5] # on affiche : heure + minute + seconde
    if tuple[2] > 0:
        affichage = [2, 3, 4] # on affiche : jour + heure + minute
    if tuple[1] > 0:
        affichage = [1, 2, 3] # on affiche : mois + jour + heure
    if tuple[0] > 0:
        affichage = [0, 1, 3] # on affiche : an + mois + heure
    for i in affichage:
        message = message + f", {tuple[i]} {time[i]}"
    return message[2:]

def userOrNick(user):
    """Affiche le pseudo et/ou le surnom"""
    if user == None:
        return "Utilisateur inconnu" # Mauvais copié/collé -> changement d'ID
    if user.nick:
        return f"{user.nick} ({user.name}#{user.discriminator})"
    else:
        return f"{user.name}#{user.discriminator}"

def cleanUser(ctx, stringMessage, stringID):
    """récupère l'utilisateur avec son id"""
    stringMessage = stringMessage.replace("<@!", "").replace(">", "").replace("<@", "") # améliorer ça avec du regex
    associatedID = userOrNick(ctx.author.guild.get_member(int(stringID)))
    try:
        stringMessage = stringMessage.replace(stringID, associatedID)
    except:
        pass
    return stringMessage

def cleanCodeStringWithMentionAndURLs(string):
    """formate un string avec des ` tout en gardant les mention et les liens"""
    string = f"`{removeStartEndSpacesString(string)}`"

    findedMention = getMentionInString(string)
    for i in range(0, len(findedMention)):
        string = string.replace(findedMention[i], f"`{findedMention[i]}`") # conserve la mention dans le message

    if string.startswith("``<@"): # conserve le format quand mention au début de la string
        string = string[2:]
    if string.endswith(">``"): # conserve le format quand mention à la fin de la string
        string = string[:-2]
    string = string.replace("``", "") # conserve le format quand deux mentions sont collés
    return string

def getMentionInString(string):
    """récupère les mentions dans un string⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
    findedMention = []
    for findingMention in re.findall(r'<@[!]?\d*>', string): # récupération mention dans le string
        findedMention.append(findingMention)
    findedMention = list(dict.fromkeys(findedMention)) # suppression doublon de mention dans la liste
    return findedMention

def getURLsInString(string):
    """récupère les liens dans un string"""
    findedURLs = []
    for findingMention in re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string): # récupération URLs dans le string
        findedURLs.append(findingMention)
    return findedURLs
        
def removeStartEndSpacesString(string):
    """Retire les espaces en trop au début et à la fin d'un string⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
    while string.startswith(" "):
        string = string[1:]
    while string.endswith(" "):
        string = string[:-1]
    return string

def randomImage(link):
    """Récupération d'une image aléatoirement⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
    temps_requete = int(round(time.time() * 1000))
    try:
        request_data = requests.get(link)
    except Exception as e:
        raise Exception(f"Une erreur s'est produite lors de la tentative de demande de l'API {link} : {e}")

    if not request_data.status_code == 200:
        raise Exception(f"Code HTTP {request_data.status_code} au lieu de HTTP 200 à l'appel de {link} : {request_data.text}")

    try:
        json_data = json.loads(request_data.text)
    except Exception as e:
        raise Exception(f"Erreur lors de la transformation les données de {link} en json : {e}")

    temps_requete = int(round(time.time() * 1000)) - temps_requete
    return (json_data, temps_requete)

def retirerDoublons(liste):
    """Supprime les doublons d'une liste"""
    Newliste = []
    for element in liste:
        if element not in Newliste:
            Newliste.append(element)
    return Newliste

def ligneFormatage(ligne):
    """Traduit en français les balises dans les lyrics d'une chanson"""
    liste_balise = [
        ('[Hook', '[Accroche'), ('[Verse', '[Couplet'), ('[Chorus', '[Chœur'),
        ('[Bridge', '[Pont'),('[Pre-Chorus', '[Pré-chœur'), ('[Post-Chorus', '[Post-chœur')
    ]
    for balises in liste_balise:
        ligne = ligne.replace(balises[0], balises[1])
    return ligne

def stringTempsVersSecondes(time):
    conversionTemps = {
        "86400": ["j", "d"],
        "3600": ["h"],
        "60": ["m"],
        "1": ["s", ""]
    }

    valeursMultiplicateur = ""
    for i in conversionTemps.values():
        for j in i:
            valeursMultiplicateur += f"{j}|"
    match = re.findall(f'([0-9]+)({valeursMultiplicateur[:-1]})?', time)

    if not match:
        return "Veuillez entrer un temps valide."

    remindertime = 0
    for i in match:
        for tempsEnSeconde, nomCommun in conversionTemps.items():
            if i[1] in nomCommun:
                remindertime += int(tempsEnSeconde) * int(i[0])

    return remindertime

def nowTimestampCustom():
    return datetime.now(timezone(myTimezone)).timestamp()

def nowTimestampUTC():
    return datetime.utcnow().timestamp()

def intToTimestamp(int):
    return datetime.fromtimestamp(int)

def timedeltaToString(time):
    age = str(timedelta(seconds = time)).replace('days, ', 'jours, :').split(':')
    if len(age) == 4:
        a = [1, 1, 1, 1] # a pour affichage
    if len(age) == 3:
        a = [0, 1, 1, 1]
        age.insert(0, None)
    for i in range(1, 4):
        if int(age[i]) == 0:
            a[i] = 0
    age[0] = age[0] if a[0] == 1 else ''
    age[1] = f"{age[1]}h " if a[1] == 1 else ''
    age[2] = f"{age[2]}m " if a[2] == 1 else ''
    age[3] = f"{age[3]}s" if a[3] == 1 else ''
    return ''.join(age)
