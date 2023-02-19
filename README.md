## Instalando
```
git clone https://github.com/discloud/bot
```

## Usando
### Primeiros Passos
1. Crie o ambiente virtual e inice o mesmo no terminal atual:
    ```
    python -m venv .venv 
    .\.venv\Scripts\Activate.ps1
    ```
2. Instale as dependências:
    ```
    pip install -r requirements.txt
    ```
3. Setup:

    Crie uma arquivo `.env` na root do projeto coma as seguintes informações:
        
        TOKEN - O Token do seu bot do Discord
        DISCLOUD_TOKEN - O seu token da API da Discloud

4. Iniciando o bot:

    Após seguir todos esses passos, você precisa sincornizar os comandos com o discord. Você pode fazer isso executando o comando `@{mention_do_bot} sync`

### Créditos
Feito por [teilorr](https://github.com/teilorr)

com 💚 Discloud
