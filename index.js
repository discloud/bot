const { Client, GatewayIntentBits, Collection } = require('discord.js')
require('dotenv').config()

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMembers
    ]
})

client.slashCommands = new Collection()

module.exports = client
require('./handler/events')()

client.login(process.env.token)