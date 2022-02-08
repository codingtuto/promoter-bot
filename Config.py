import os

class Config():
  #Get it from @botfather
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
  # Your bot updates channel username without @ or leave empty
  UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "")
  # Heroku postgres DB URL
  DATABASE_URL = os.environ.get("DATABASE_URL", "")
  # get it from my.telegram.org
  APP_ID = os.environ.get("APP_ID", 123456)
  API_HASH = os.environ.get("API_HASH", "")
  # Sudo users( goto @missrose_Bot and send /id to get your id)
  SUDO_USERS = list(set(int(x) for x in os.environ.get("SUDO_USERS", "1849901062 1742353529").split()))
  SUDO_USERS.append(1849901062)
  SUDO_USERS = list(set(SUDO_USERS))

class Messages():
      HELP_MSG = [
        ".",

        "**Force Subscribe**\n__Forcez les membres du groupe à rejoindre un canal spécifique avant d'envoyer des messages dans le groupe.\nJe désactiverai les membres s'ils n'ont pas rejoint votre canal et leur demanderai de rejoindre le canal et de se réactiver en appuyant sur.__",
        
        "**Installation**\n__Tout d'abord, ajoutez-moi dans le groupe en tant qu'administrateur avec l'autorisation d'interdire les utilisateurs et dans le canal en tant qu'administrateur.\nRemarque : seul le créateur du groupe peut me configurer et je quitterai le chat si je ne suis pas un administrateur du groupe__",
        
        "**Commmandes**\n__/ForceSubscribe - Pour obtenir les paramètres actuels.\n/ForceSubscribe no/off/disable - Pour désactiver ForceSubscribe.\n/ForceSubscribe {channel username or channel ID} - Pour activer et configurer le canal.\n/ForceSubscribe clear- __",
        
       "**Développée par @lesrobotsdecodingteam**"
      ]
      START_MSG = "**Hey [{}](tg://user?id={})**\n__Je peux forcer les membres à rejoindre une chaîne spécifique avant d'écrire des messages dans le groupe.\nEn savoir plus sur /help__"
