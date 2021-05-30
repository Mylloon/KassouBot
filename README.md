# Bot developed with [discord.py](https://github.com/Rapptz/discord.py) (rewrite) - FRENCH

[![Version](https://img.shields.io/badge/version-1.3-green?style=for-the-badge)](https://github.com/Confrerie-du-Kassoulait/KassouBot/releases/latest)
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

- In the [Discord Dev Portal](https://discord.com/developers/applications) create an application, and make sure it's a `Bot` (third tab).
- To invite it, go to the `OAuth2` (second tab) tab, select the scopes `bot` (required) and `applications.commands` (for the slashs commands) and in the bot permissions select `Administrator` (You can select manually at your own risk).
- You have the link above between the two blocks scope and permissions.
- If you need help, you can [join my Discord](https://discord.gg/Z5ePxH4).

## __Features__

Everything is explained by doing the `help` command.
