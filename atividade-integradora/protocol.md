# Documentação do Protocolo

## Especificações Gerais

| Propriedade         | Detalhe                                        |
| ------------------- | ---------------------------------------------- |
| **Nome**            | *GuessGame Protocol*                           |
| **Transporte**      | TCP (*Transmission Control Protocol*)          |
| **Porta Padrão**    | `5000`                                         |
| **Formato**         | Texto Puro / *Plain Text*                      |
| **Codificação**     | UTF-8                                          |
| **Delimitadores**   | `\n` (Quebra de linha / *Newline*)             |

## Mensagens e Comandos

O protocolo de aplicação estabelece a seguinte relação de comandos enviados pelo cliente e respostas recebidas do servidor:

### Comandos do Cliente
Qualquer envio do cliente para o servidor deve ser uma string UTF-8 encerrada em `\n`. 
Os comandos válidos são:

| Comando | Descrição |
| :--- | :--- |
| `{Inteiro}` | O palpite do jogador (ex: `45`, `10`, `99`). O servidor tentará fazer o parse para `int`. |
| `/quit` | Comando de término voluntário de sessão. |
| *(Qualquer outro)* | Será interpretado pelo servidor como formato inválido e retornará uma mensagem de erro. |

### Respostas do Servidor
As respostas enviadas do servidor também serão em texto UTF-8 encerradas em `\n`.

| Resposta | Descrição | Ação Esperada |
| :--- | :--- | :--- |
| `BEM-VINDO! ...` | Enviado automaticamente ao estabelecer a conexão. | Cliente deve exibir ao usuário. |
| `MAIOR` | O palpite enviado é menor que o número correto. O jogador precisa chutar mais alto. | Cliente continua jogando. |
| `MENOR` | O palpite enviado é maior que o número correto. O jogador precisa chutar mais baixo. | Cliente continua jogando. |
| `WINNER: ...` | Mensagem de *broadcast* indicando que algum cliente acertou o número. O sorteio recomeça automaticamente. | Cliente exibe a mensagem e a partida continua. |
| `ERROR: ...` | Enviado caso o servidor não compreenda o formato (ex: letras ao invés de números). | Cliente deve exibir erro e pedir nova entrada. |
| `GOODBYE` | Enviado confirmando o recebimento de um `/quit`. | Cliente encerra o socket. |

## Tratamento de Erros e Encerramento (Exceptions)

- **Desconexão por Exceção (Crash/Close):** Se o cliente perder conectividade forçadamente (ex: fechou o terminal) e enviar um evento *ConnectionResetError*, ou sinal EOF, a *thread* correspondente tratará a exceção e fechará o *socket* no lado do servidor sem interromper a execução para os demais jogadores.
- **Término Gratuito (Graceful Exit):** O término padrão ocorre com o cliente enviando `/quit`. O servidor responde `GOODBYE` e então o laço se encerra de forma mutuamente acordada (`conn.close()` de ambos os lados).
- **Validação de Entrada:** Se o usuário enviar letras ao invés de números (ex: `dez`), o servidor engolirá o `ValueError` emitindo em seguida a mensagem `ERROR: Entrada invalida. Envie um numero ou /quit.`, sem encerrar a conexão.
