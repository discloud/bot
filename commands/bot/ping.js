module.exports = {
    name: 'ping',
    description: 'See the latency between Discord servers and the bot',
    type: 1,
    async execute({ interaction, client }) {

        return await interaction.reply({
            content: `🏓 | Pong: ${client.ws.ping}ms`
        })
        
    }
}
