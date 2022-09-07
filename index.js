/**
 * Este é um bot básico comum no Discloud para consumir a API da DISCLOUD.
 * O código é feito por: Rody#1000 (Membro da Discloud)
 * Autorizado por: PR#4003 (Fundador da Discloud)
 * Analizado por: Serginho#8818 (Manager da Discloud)
 * Construção da API: Gorniaky#2023 (Membro da Discloud) *Api em construção
 */

const { Client, GatewayIntentBits, Collection } = require('discord.js')
require('dotenv/config')

// Recomendo colocar isso dentro de algum arquivo separado pra deixar mais organizado
class Bot extends Client {
    constructor(args) {
        super({
            intents: [
                GatewayIntentBits.Guilds,
                GatewayIntentBits.GuildMembers
            ]
        });
        this.slashCommands = new Collection();
        this._token = process.env.token;
        const eventHandler = require('./handler/events');
        eventHandler();

    }
   
}



const client = new Bot();
client.login(client._token);


module.exports = client
