module.exports = {
    name: 'ping',
    description: 'Ping pong',
    type: 1,
    async execute({ interaction, client }) {
        await interaction.deferReply()
        return await interaction.editReply({
            content: `🏓 | Pong: ${client.ws.ping}ms`
        })
    }
}