const axios = require('axios')
const { EmbedBuilder } = require('discord.js')
const config = require('../../config.json')
require('dotenv').config()

module.exports = {
    name: 'terminal',
    description: 'Terminal da aplicação',
    type: 1,
    async execute({ interaction, client }) {

        // Mensagem de carregamento pra ficar bonitinho
        await interaction.reply({
            content: '🔄 | Solicitando o conteúdo do terminal a Discloud Host.',
            fetchReply: true
        })
        
        /**
         * ID_DO_BOT_OU_SUBDOMINIO_DO_SEU_SITE
         * Literalmente, use o ID do seu bot ou o Sub-Dominio do seu site.
         * config.botId ou config.subDomain
         */
        return axios.get(`https://api.discloud.app/v2/app/ID_DO_BOT_OU_SUBDOMINIO_DO_SEU_SITE/logs`, {
            headers: {
                /**
                 * O token da API está no arquivo .env por segurança.
                 * Para obter o seu token, use o comando ".api" no canal de comandos no servidor da Discloud
                 */
                "api-token": process.env.discloudToken
            }
        })
            .then(terminal => response(terminal.data))
            .catch(async err => {
                console.log(err)
                return await interaction.editReply({
                    content: '❌ Não foi possível obter o terminal, confira o console.log'
                })
            })

        async function response(data) {

            // Se tudo der certo, você irá receber este objeto abaixo.
            // {
            //     status: 'ok',
            //     message: 'The logs of your applications were loaded',
            //     apps: {
            //         id: 'saphire',
            //         terminal: {
            //             big: 'Conteúdo do terminal aqui dentro',
            //             small: 'Conteúdo do terminal aqui dentro'
            //         }
            //     }
            // }

            // "small" é o conteúdo do terminal limitado para caber dentro da Descrição da embed.
            // Se o seu terminal exceder o tamanho limite da embed, irá ocasionar um erro.
            // Então, de prefêrencia, use o small.
            const terminalContent = data.apps.terminal.small

            if (terminalContent.length === 0)
                return await interaction.editReply({
                    content: 'ℹ | Os logs da aplicação está vázia.'
                })

            const embed = new EmbedBuilder()
                .setColor('Green')
                .setTitle('Terminal da aplicação')
                .setDescription(`\`\`\`txt\n${terminalContent}\n\`\`\``)

            return await interaction.editReply({
                content: null,
                embeds: [embed]
            })

        }
    }
}