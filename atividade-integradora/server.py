import socket
import threading
import random

HOST = '0.0.0.0'
PORT = 5000

# Estado global compartilhado
clients = set()
lock = threading.Lock()
target_number = random.randint(1, 100)

# Função que envia mensagem para todos os clientes, com tratamento de erro e remoção de clientes desconectados
def broadcast(msg):
    with lock:
        clientes_a_remover = set()
        for c in clients:
            try:
                c.sendall(msg.encode('utf-8'))
            except:
                clientes_a_remover.add(c)
        for c in clientes_a_remover:
            clients.discard(c)

# Função que lida com cada cliente, aceitando palpites, verificando acertos e enviando feedback
def handle_client(conn, addr):
    global target_number
    
    print(f"[{addr}] Conectado.")
    
    with lock:
        clients.add(conn)
    
    try:
        conn.sendall("BEM-VINDO! Adivinhe o numero (1-100). Envie '/quit' para sair.\n".encode('utf-8'))
    except:
        with lock:
            clients.discard(conn)
        return

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            
            msg = data.decode('utf-8').strip()
            
            if msg == '/quit':
                conn.sendall("ATÉ LOGO!\n".encode('utf-8'))
                break
                
            try:
                guess = int(msg)
                eh_vencedor = False
                
                with lock:
                    if guess < target_number:
                        conn.sendall("MAIOR\n".encode('utf-8'))
                    elif guess > target_number:
                        conn.sendall("MENOR\n".encode('utf-8'))
                    else:
                        eh_vencedor = True
                        target_number = random.randint(1, 100) # Sorteia um novo numero para a proxima rodada
                
                # Dispara o broadcast fora do lock para nao bloquear outras operacoes
                if eh_vencedor:
                    win_msg = f"VENCEDOR: Cliente {addr} acertou! Novo numero sorteado.\n"
                    print(f"[{addr}] Venceu a rodada.")
                    broadcast(win_msg)
                    
            except ValueError:
                conn.sendall("ERRO: Entrada invalida.\n".encode('utf-8'))
                
        except Exception as e:
            print(f"[{addr}] Erro: {e}")
            break
            
    with lock:
        clients.discard(conn)
    conn.close()
    print(f"[{addr}] Desconectado.")

# Função principal que inicia o servidor e aguarda a conexão dos clientes, que é iniciada em threads separadas
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen()
        # Define um timeout no socket do servidor para que accept() não bloqueie indefinidamente.
        # Isso permite que o interpretador Python processe o sinal de Ctrl+C (KeyboardInterrupt) no Windows.
        server.settimeout(1.0)
        print(f"Servidor rodando em {HOST}:{PORT}")
        
        while True:
            try:
                conn, addr = server.accept()
                conn.settimeout(None) # Restaura o socket do cliente para o modo bloqueante padrão
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except socket.timeout:
                continue
            
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
