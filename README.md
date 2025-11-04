## Como Executar o Sistema de Chat

**1. Iniciar o Broker**

O broker é o servidor central e deve ser executado primeiro. Ele precisa permanecer ativo para que o chat funcione.
```bash
python3 broker.py
```

**2. Iniciar um Cliente**

Para cada usuário, abra um novo terminal e execute o cliente.
```bash
python3 chat_client.py
```
O programa solicitará:
1.  Seu **nome de usuário** (ex: `Alice`).
2.  O **canal inicial** que deseja entrar (ex: `#geral`).

**3. Usando o Chat**

Uma vez conectado, você verá um prompt como `[Alice @ #geral]>`.

*   **Para enviar uma mensagem:** Simplesmente digite sua mensagem e pressione Enter. Ela será enviada para o seu canal ativo.
*   **Para usar comandos:** Digite um dos seguintes comandos:

| Comando           | Descrição                                         |
|-------------------|---------------------------------------------------|
| `/help`           | Mostra a lista de comandos disponíveis.           |
| `/join <#topico>`   | Entra em um novo canal para receber mensagens.    |
| `/leave <#topico>`  | Sai de um canal e para de receber suas mensagens. |
| `/switch <#topico>` | Muda o seu canal ativo (para onde você envia).    |
| `/quit`           | Sai do chat de forma limpa.                       |


**Exemplo de Sessão:**

1.  **Alice** entra no canal `#geral`.
2.  **Bob** entra no canal `#geral` em outro terminal.
3.  Alice digita `Oi Bob!` e a mensagem aparece para ambos.
4.  Alice digita `/join #dev`. Ela agora recebe mensagens do `#geral` e do `#dev`.
5.  Alice digita `/switch #dev`. Seu prompt muda para `[Alice @ #dev]>`.
6.  Alice digita `Alguém sabe Python?`. Apenas outros usuários que entraram no canal `#dev` verão esta mensagem. Bob não a verá.