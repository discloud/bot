const client = require('../index')

client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return

    const command = client.slashCommands.get(interaction.commandName)
    if (!command) return

    return await command.execute({ interaction, client }).catch(console.log)
})