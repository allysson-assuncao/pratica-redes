# Relatório do Projeto: Jogo de Adivinhação

## 1. Evidências de Teste (Concorrência e Rede Local)

> **Instrução para o Aluno:** Para preencher esta seção, abra o servidor em uma máquina. Em seguida, conecte dois clientes simultaneamente (pode ser abrindo dois terminais diferentes na sua máquina apontando para `127.0.0.1`, ou usando um outro computador na mesma rede Wi-Fi apontando para o IP local do servidor, ex: `192.168.1.10`).
> 
> **Cole os prints/screenshots do terminal abaixo demonstrando:**
> 1. O servidor recebendo conexões múltiplas.
> 2. Os dois clientes jogando ao mesmo tempo sem que um trave o outro.

*(Cole suas imagens aqui)*
- `[Screenshot do Servidor]`
- `[Screenshot do Cliente 1]`
- `[Screenshot do Cliente 2]`

---

## 2. Limitações da Arquitetura Atual

Embora o sistema cumpra todos os requisitos e funcione de forma assíncrona para múltiplos clientes via *Threads*, ele possui algumas limitações inerentes ao design escolhido:

1. **Falta de Estado Persistente (Banco de Dados):** O servidor não armazena o histórico dos jogadores. Se o servidor for reiniciado, o número alvo de todos os jogadores em andamento é perdido.
2. **Custo de Escalabilidade (Thread-per-connection):** A abordagem de criar uma nova `Thread` do SO para cada cliente conectado (`threading.Thread`) funciona bem para dezenas de usuários, mas pode esgotar os recursos de memória e CPU do servidor se milhares de clientes se conectarem simultaneamente.
3. **Ausência de Autenticação/Identificação:** Os jogadores são identificados internamente pelo servidor apenas pela tupla `(IP, Porta)` do socket. Não existe um sistema de "Nicknames" ou login.
4. **Segurança (Texto em Claro):** O protocolo trafega os dados em texto puro (UTF-8) sobre TCP. Em uma rede local pública, os palpites poderiam ser facilmente interceptados via *sniffing* (ex: Wireshark).

## 3. Possíveis Melhorias Futuras

Para evoluir a aplicação, as seguintes melhorias poderiam ser implementadas:

1. **Migrar para I/O Assíncrono (`asyncio` ou `select`):** Para resolver o problema de escalabilidade das *Threads*, o servidor poderia usar a biblioteca `select` nativa ou o módulo `asyncio` para lidar com milhares de conexões em uma única thread usando multiplexação de I/O.
2. **Placar Global (Leaderboard):** Adicionar suporte para o cliente informar seu "Nome" ao conectar e, ao acertar o número, registrar a quantidade de tentativas no servidor, retornando um ranking geral.
3. **Modos de Dificuldade:** O cliente poderia escolher se quer adivinhar um número entre 1-100, 1-1000, etc., enviando um comando inicial (ex: `/diff hard`).
4. **Criptografia TLS/SSL:** Envolver o socket TCP nativo na biblioteca `ssl` do Python para garantir a confidencialidade das mensagens na rede.
