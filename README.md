# Bot developed with [discord.py](https://github.com/Rapptz/discord.py) (rewrite) - FRENCH

#### __Prerequisites__

- Python 3.7.9
- [requirements.txt](requirements.txt)

#### __Setting up__

- A `tokens.py` file that contains:

```py
token_discord = "your discord token"
token_genius = "your genius token"
token_reddit = {"client_id": "your client id", "client_secret": "your secret pass", "user_agent": "your reddit's username"}
```

To find reddit tokens, go to [this site](https://www.reddit.com/prefs/apps) and here are the instructions: ![instructions](https://i.imgur.com/tEzYKDA.png)

*redirection uri (for copy/paste) : http://localhost:8080*

#### __Starting up__

- Run [main.py](main.py)

#### __Add the bot to your server__

- [This site](https://discordapi.com/permissions.html) allows you to choose which permissions to add by default to the bot.
    - Choose *Administrator* so you don't get in over your head.
    - Copy and paste the ID of your bot in *Client ID* found [here](https://discord.com/developers/applications) and go to the link at the bottom of the page.

## __Features__

Everything is explained by doing `.help`
