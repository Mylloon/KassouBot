import re
import json
import requests
from time import time

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
    temps_requete = int(round(time() * 1000))
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

    temps_requete = int(round(time() * 1000)) - temps_requete
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

def mentionToUser(mention: str):
    """Récupère une mention et renvois son ID"""
    return int(mention[2:-1].replace("!",""))

def getChangelogs(version = 'latest'):
    """Récupère les changements d'une version (par défaut, la dernière en date) et renvois dans l'ordre : url, n° version, changements"""
    if version != 'latest':
        version = f'tags/v{version}'
    changements = requests.get(f"https://api.github.com/repos/Confrerie-du-Kassoulait/KassouBot/releases/{version}").json()
    try:
        changements["message"] # renvois None si aucune version correspondante n'a été trouvée
        return None
    except:
        pass
    return (changements["html_url"], changements["tag_name"][1:], changements["body"])
