const client = require('../index')

client.on('ready', () => {
    console.log('Online.')
    require('../handler/commands')()
})