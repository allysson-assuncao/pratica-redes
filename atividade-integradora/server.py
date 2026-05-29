import socket
import threading
import random

HOST = '0.0.0.0'
PORT = 5000

# Estado global compartilhado
clients = set()
lock = threading.Lock()
target_number = random.randint(1, 100)

def broadcast(msg):
    with lock:
        to_remove = set()
        for c in clients:
            try:
                c.sendall(msg.encode('utf-8'))
            except:
                to_remove.add(c)
        for c in to_remove:
            clients.discard(c)

def handle_client(conn, addr):
    global target_number
    
    print(f"[{addr}] Conectado.")
    
    with lock:
        clients.add(conn)
    
    try:
        conn.sendall("BEM-VINDO! Adivinhe o numero (1-100). Envie /quit para sair.\n".encode('utf-8'))
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
                conn.sendall("GOODBYE\n".encode('utf-8'))
                break
                
            try:
                guess = int(msg)
                is_winner = False
                
                with lock:
                    if guess < target_number:
                        conn.sendall("MAIOR\n".encode('utf-8'))
                    elif guess > target_number:
                        conn.sendall("MENOR\n".encode('utf-8'))
                    else:
                        is_winner = True
                        target_number = random.randint(1, 100) # Sorteia um novo numero para a proxima rodada
                
                # Dispara o broadcast fora do lock para nao bloquear outras operacoes
                if is_winner:
                    win_msg = f"WINNER: Cliente {addr} acertou! Novo numero sorteado.\n"
                    print(f"[{addr}] Venceu a rodada.")
                    broadcast(win_msg)
                    
            except ValueError:
                conn.sendall("ERROR: Entrada invalida.\n".encode('utf-8'))
                
        except Exception as e:
            print(f"[{addr}] Erro: {e}")
            break
            
    with lock:
        clients.discard(conn)
    conn.close()
    print(f"[{addr}] Desconectado.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor rodando em {HOST}:{PORT}")
        
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
            
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
