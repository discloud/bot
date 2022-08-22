const { Routes } = require('discord.js')
const { REST } = require("@discordjs/rest")
const { readdirSync } = require('fs')
const client = require('../index')

module.exports = async () => {

    const commands = []
    const folders = readdirSync('./commands/slashCommands')

    for (let dir of folders) {

        const commandsData = readdirSync(`./commands/slashCommands/${dir}/`).filter(file => file.endsWith('.js'))

        for await (let file of commandsData) {

            const cmd = require(`../commands/slashCommands/${dir}/${file}`)

            if (cmd && cmd.name) {
                client.slashCommands.set(cmd.name, cmd);
                commands.push(cmd);
            }
        }
    }

    const rest = new REST({ version: "10" }).setToken(process.env.token)

    await rest.put(
        Routes.applicationCommands('1011268475844563024'),
        { body: commands },
    );

    return console.log('Slash Commands loaded.')
}