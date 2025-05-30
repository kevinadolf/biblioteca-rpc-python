import socket
import threading

# classe que registra e localiza servicos
class RPCBinder:
    # dicionario q guarda os servicos registrados
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.services = {}  # service_name -> (ip, port)

    # inicia o binder e escuta conexoes
    def start_binder(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"[BINDER] servidor iniciado em {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn,)).start()

    # processamento
    # cada cliente eh tratado em uma thread
    def handle_client(self, conn):
        with conn: # "loop"
            data = conn.recv(1024).decode()
            if not data: #tratamento
                return
            parts = data.strip().split('|') # separacao de msgs
            command = parts[0]
            # comando REGISTER add um servico
            if command == 'REGISTER' and len(parts) == 4:
                service_name, ip, port = parts[1], parts[2], parts[3]
                self.services[service_name] = (ip, port)
                conn.sendall(b'OK')
                # comando LOOKUP procura um servico
            elif command == 'LOOKUP' and len(parts) == 2:
                service_name = parts[1]
                if service_name in self.services:
                    ip, port = self.services[service_name]
                    conn.sendall(f"{ip}|{port}".encode())
                else:
                    conn.sendall(b'NOT_FOUND')