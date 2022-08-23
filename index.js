const { Client, GatewayIntentBits, Collection } = require('discord.js')
require('dotenv').config()

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMembers
    ]
})

module.exports = client
client.slashCommands = new Collection()
require('./handler/events')()
client.login(process.env.token)