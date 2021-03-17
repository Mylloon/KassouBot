# Bot developed with [discord.py](https://github.com/Rapptz/discord.py) (rewrite) - FRENCH

## __Setting up__

You have to replace `TOKEN_DISCORD`, `TOKEN_GENIUS`, `TOKEN_REDDIT_CLIENT_ID`, `TOKEN_REDDIT_CLIENT_SECRET` and `TOKEN_REDDIT_USER_AGENT` with your desired values.
With a [docker-compose](docker-compose.yml) or in command line:

```
docker run -d \
    --name="kassoubot" \
    mylloon/kassoubot \
    --TOKEN_DISCORD="yourValue" \
    --TOKEN_GENIUS="yourValue" \
    --TOKEN_REDDIT_CLIENT_ID="yourValue" \
    --TOKEN_REDDIT_CLIENT_SECRET="yourValue" \
    --TOKEN_REDDIT_USER_AGENT="yourValue"
```

To find reddit tokens, go to [this site](https://www.reddit.com/prefs/apps) and here are the instructions: ![instructions](https://i.imgur.com/tEzYKDA.png)

*redirection uri (for copy/paste) : http://localhost:8080*

## __Add the bot to your server__

- [This site](https://discordapi.com/permissions.html) allows you to choose which permissions to add by default to the bot.
    - Choose *Administrator* so you don't get in over your head.
    - Copy and paste the ID of your bot in *Client ID* found [here](https://discord.com/developers/applications) and go to the link at the bottom of the page.

## __Features__

Everything is explained by doing `.help`
