import socket
import threading
import os

def receive_messages(client):
    """
    Thread dedicada para receber mensagens do servidor sem bloquear o input do usuario.
    """
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print("\n[Desconectado pelo servidor]")
                os._exit(0)
            
            msg = data.decode('utf-8').strip()
            if msg == 'GOODBYE':
                print("\nSaindo...")
                os._exit(0)
                
            # Exibe a mensagem do servidor e reimprime o prompt de input
            print(f"\nServidor: {msg}")
            print("Seu chute: ", end="", flush=True)
            
        except Exception:
            print("\n[Erro de conexao]")
            os._exit(1)

def start_client():
    server_ip = input("IP do servidor (ex: 127.0.0.1): ").strip()
    if server_ip == '':
        server_ip = '127.0.0.1'
    port = 5000
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, port))
        print(f"Conectado a {server_ip}:{port}")
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return
        
    # Inicia a thread de recebimento
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    # Loop principal focado apenas no envio
    while True:
        try:
            msg = input("Seu chute: ").strip()
            if msg:
                client.sendall((msg + "\n").encode('utf-8'))
        except (KeyboardInterrupt, EOFError):
            client.sendall("/quit\n".encode('utf-8'))
            break
        except Exception:
            break

if __name__ == "__main__":
    start_client()
