/**
 * Este é um bot básico comum no Discloud para consumir a API da DISCLOUD.
 * O código é feito por: Rody#1000 (Membro da Discloud)
 * Autorizado por: PR#4003 (Fundador da Discloud)
 * Analizado por: Serginho#8818 (Manager da Discloud)
 * Construção da API: Gorniaky#2023 (Membro da Discloud) *Api em construção
 */

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
