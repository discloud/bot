/**
 * Este é um bot básico comum no Discloud para consumir a API da DISCLOUD.
 * O código é feito por: Rody#1000 (Membro da Discloud)
 * Autorizado por: PR#4003 (Fundador da Discloud)
 * Analizado por: Serginho#8818 (Manager da Discloud)
 * Construção da API: Gorniaky#2023 (Membro da Discloud) *Api em construção
 */


const Client = require('./structures/Bot.js')

const client = new Client();
client.login(client._token);

module.exports = client
