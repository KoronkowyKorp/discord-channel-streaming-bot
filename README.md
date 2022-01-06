# discord-channel-streaming-bot
Discord bot for streaming data from an authorized channel within a server

## Database
Write now the system relies on a sqlite3 database to store data produced by the bot.

As of now, servers need to be MANUALLY ADDED via connection to the database.


## Python dev setup
Set up a virtual environment by running
```
python3 -m virtualenv .
```
This will initalize a virtual environment in this directory.

To enter the virtual environment, run
```
source bin/activate
```

To install library dependencies, run
```
pip install -r requirements.txt
```

## Bot tokens
A token for the bot can be retrieved from the [Discord Developer Applications panel](https://discord.com/developers/applications/). You may save it to a file named `config.json`, styled like so:
```
{
    "token":"<bot token>",
    "client_id":"<client id>",
    "client_secret":"<client secret>"
}
```
This page has more info on how to add the bot to the server: [https://discordpy.readthedocs.io/en/stable/discord.html](https://discordpy.readthedocs.io/en/stable/discord.html).

Adding the bot to your server will depend on authorizing it via the Discord OAuth2 url generated here:
`https://discord.com/api/oauth2/authorize?client_id=928752486817341460&permissions=1374389738496&scope=bot`

