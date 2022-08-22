const { readdirSync } = require('fs')

module.exports = () => {
    const events = readdirSync('./events/')
    for (const event of events)
        require(`../events/${event}`)
    return console.log('events loaded')
}