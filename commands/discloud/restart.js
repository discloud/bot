const axios = require('axios')
const config = require('../../config.json')

module.exports = {
    name: 'restart',
    description: 'Reinicie a aplicação',
    type: 1,
    async execute({ interaction, client }) {

        /**
         * ID_DO_BOT_OU_SUBDOMINIO_DO_SEU_SITE
         * Literalmente, use o ID do seu bot ou o Sub-Dominio do seu site.
         * config.botId ou config.subDomain
         */
        return axios.get(`https://api.discloud.app/v2/app/ID_DO_BOT_OU_SUBDOMINIO_DO_SEU_SITE/restart`, {
            headers: {
                /**
                 * O token da API está no arquivo .env por segurança.
                 * Para obter o seu token, use o comando ".api" no canal de comandos no servidor da Discloud
                 */
                "api-token": process.env.discloudToken
            }
        })
            .catch(async err => {
                console.log(err)
                return await interaction.editReply({
                    content: '❌ Não foi possível obter o backup, confira o console.log'
                })
            })

    }
}