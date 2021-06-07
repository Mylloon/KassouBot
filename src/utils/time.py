from os import environ
from pytz import timezone
from datetime import datetime, timedelta
from re import findall

myTimezone = environ['TIMEZONE']

def stringTempsVersSecondes(time):
    """Convertis une durée rentrée par un utilisateur en string vers des secondes en int"""
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
    match = findall(f'([0-9]+)({valeursMultiplicateur[:-1]})?', time)

    if not match:
        return "Veuillez entrer un temps valide."

    remindertime = 0
    for i in match:
        for tempsEnSeconde, nomCommun in conversionTemps.items():
            if i[1] in nomCommun:
                remindertime += int(tempsEnSeconde) * int(i[0])

    return remindertime

def nowCustom():
    """Heure de maintenant avec fuseau horaire local en float"""
    return datetime.now(timezone(myTimezone)).timestamp()

def nowUTC():
    """Heure de maintenant en UTC en float"""
    return datetime.utcnow().timestamp()

def UTCDatetimeToCustomDatetime(datetime):
    """Conversion d'une timestamp UTC en timestamp local en datetime"""
    return timezone(myTimezone).fromutc(datetime)

def intToDatetime(intOrFloat):
    """Convertis un int ou float en Datetime"""
    return datetime.fromtimestamp(intOrFloat)

def timestampScreen(timestamp):
    """Affichage d'une timestamp"""
    date_edit = str(UTCDatetimeToCustomDatetime(timestamp)).replace('-', '/').split(' ')
    date = date_edit[0]
    heure = date_edit[1].split('+')[0]
    return f"{date[8:]}/{date[5:-3]}/{date[:4]} à {heure.split('.')[0]}"

def timedeltaToString(time):
    """Différence entre une heure en seconde et maintenant"""
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

def getAge(date):
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
    """avec la méthode 'getAge', permet de mettre en forme un âge⁢⁢⁢⁢⁢⁢⁢⁢⁢⁢"""
    time = {}
    time[0], time[1], time[2], time[3], time[4], time[5] = "an", "mois", "jour", "heure", "minute", "seconde"
    for i in range(len(tuple)):
        if tuple[i] > 1 and i != 1:
            time[i] = time[i] + "s"
    message = ""
    if tuple[5] > 0:
        affichage = [5]
    if tuple[4] > 0:
        affichage = [4, 5]
    for i in [3, 0]:
        if tuple[i] > 0:
            affichage = [i, i + 1, i + 2]
    for i in affichage:
        message = message + f", {tuple[i]} {time[i]}"
    return message[2:]
