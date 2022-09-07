const { Client, GatewayIntentBits, Collection } = require('discord.js');
require('dotenv/config');


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
        const eventHandler = require('../handler/events');
        eventHandler();

    }
   
}

module.exports = Bot;
