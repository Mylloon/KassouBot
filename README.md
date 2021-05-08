# Bot developed with [discord.py](https://github.com/Rapptz/discord.py) (rewrite) - FRENCH

[![Version](https://img.shields.io/badge/version-1.2-green?style=for-the-badge)](https://github.com/Confrerie-du-Kassoulait/KassouBot/releases/latest)
[![Docker Stars](https://img.shields.io/docker/stars/mylloon/kassoubot?style=for-the-badge)](https://hub.docker.com/r/mylloon/kassoubot)
[![Docker Pulls](https://img.shields.io/docker/pulls/mylloon/kassoubot?style=for-the-badge)](https://hub.docker.com/r/mylloon/kassoubot)
[![Github stars](https://img.shields.io/github/stars/Confrerie-du-Kassoulait/kassoubot?label=Github%20Stars&style=for-the-badge)](https://github.com/Confrerie-du-Kassoulait/KassouBot/stargazers)
[![Github forks](https://img.shields.io/github/forks/Confrerie-du-Kassoulait/KassouBot?label=Github%20Forks&style=for-the-badge)](https://github.com/Confrerie-du-Kassoulait/KassouBot/network)
## __Setting up__

You have to replace `TOKEN_DISCORD`, `PREFIX`, `TOKEN_GENIUS`, `TOKEN_REDDIT_CLIENT_ID`, `TOKEN_REDDIT_CLIENT_SECRET`, `TOKEN_REDDIT_USER_AGENT` and [`TIMEZONE`](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) with your desired values.
With a [docker-compose](https://github.com/Confrerie-du-Kassoulait/KassouBot/blob/master/docker-compose.yml) or in command line:

```
docker run -d \
    --name="KassouBot" \
    mylloon/kassoubot \
    --TOKEN_DISCORD="yourTokenDiscord" \
    --TOKEN_GENIUS="yourTokenGenius" \
    --TOKEN_REDDIT_CLIENT_ID="yourRedditClientID" \
    --TOKEN_REDDIT_CLIENT_SECRET="yourRedditClientSecret" \
    --TOKEN_REDDIT_USER_AGENT="yourRedditUserAgent" \
    --TIMEZONE="yourTimezone" \
    --PREFIX="yourPrefix"
```

To find reddit tokens, go to [this site](https://www.reddit.com/prefs/apps) and here are the instructions: ![instructions](https://i.imgur.com/tEzYKDA.png)

*redirection uri (for copy/paste) : http://localhost:8080*

## __Add the bot to your server__

- [This site](https://discordapi.com/permissions.html) allows you to choose which permissions to add by default to the bot.
    - Choose *Administrator* so you don't get in over your head.
    - Copy and paste the ID of your bot in *Client ID* found [here](https://discord.com/developers/applications) and go to the link at the bottom of the page.

## __Features__

Everything is explained by doing the `help` command.
