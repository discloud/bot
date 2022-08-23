const axios = require('axios')
const { EmbedBuilder } = require('discord.js')
const config = require('../../config.json')
require('dotenv').config()

module.exports = {
    name: 'backup',
    description: 'Link de backup da aplicação',
    type: 1,
    async execute({ interaction, client }) {

        // Mensagem de carregamento pra ficar bonitinho
        await interaction.reply({
            content: '🔄 | Solicitando o backup da aplicação a Discloud Host.',
            fetchReply: true
        })

        /**
         * ID_DO_BOT_OU_SUBDOMINIO_DO_SEU_SITE
         * Literalmente, use o ID do seu bot ou o Sub-Dominio do seu site.
         * config.botId ou config.subDomain
         */
        return axios.get(`https://api.discloud.app/v2/app/${config.subDomain}/backup`, {
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
                    content: '❌ Não foi possível obter o backup, confira o console.log'
                })
            })

        async function response(data) {

            // Se tudo der certo, você irá receber este objeto abaixo.
            // {
            //     status: 'ok',
            //     message: 'The backup of your application will be generated successfully',
            //     backups: {
            //         id: 'SUB_DOMAIN',
            //         url: 'LINK_PRA_DOWNLOAD'
            //     }
            // }

            // "small" é o conteúdo do terminal limitado para caber dentro da Descrição da embed.
            // Se o seu terminal exceder o tamanho limite da embed, irá ocasionar um erro.
            // Então, de prefêrencia, use o small.

            const downloadLink = data.backups.url

            const embed = new EmbedBuilder()
                .setColor('Green')
                .setTitle('Backup da aplicação')
                .setDescription(`Tudo certo! Só fazer o [download](${downloadLink}).`)

            return await interaction.editReply({
                content: null,
                embeds: [embed]
            })

        }
    }
}