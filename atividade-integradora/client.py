import socket
import threading
import os

# Função dedicada à receber mensagens do servidor sem bloquear o input do usuario
def receive_messages(client):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print("\n[Desconectado pelo servidor]")
                os._exit(0)
            
            msg = data.decode('utf-8').strip()
            if msg == 'ATÉ LOGO!':
                print("\nSaindo...")
                os._exit(0)
                
            # Limpa a linha atual (onde está o prompt pendente) usando códigos ANSI
            # \r move o cursor para o início da linha, \033[K limpa a linha.
            print(f"\r\033[KServidor: {msg}")
            print("Seu palpite: ", end="", flush=True)
            
        except Exception:
            print("\n[Erro de conexao]")
            os._exit(1)

# Função principal que inicia o cliente, se conecta ao servidor e inicia o fluxo de interação
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

    # Exibe o prompt inicial antes de iniciar o loop de input
    print("Seu palpite: ", end="", flush=True)

    # Loop principal focado apenas no envio
    while True:
        try:
            msg = input().strip()
            if msg:
                client.sendall((msg + "\n").encode('utf-8'))
            else:
                # Se o usuário pressionar Enter vazio, apenas reimprime o prompt
                print("Seu palpite: ", end="", flush=True)
        except (KeyboardInterrupt, EOFError):
            client.sendall("/quit\n".encode('utf-8'))
            break
        except Exception:
            break

if __name__ == "__main__":
    start_client()
