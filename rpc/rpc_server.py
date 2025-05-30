import socket
import threading
from rpc.serializer import serialize, deserialize
from rpc.rpc_binder import RPCBinder

# servidor rpc que registra servico no binder
class RPCServer:
    def __init__(self, service_name, service_instance, host='localhost', port=0, binder_host='localhost', binder_port=8000):
        self.service_name = service_name
        self.service_instance = service_instance
        self.host = host
        self.port = port
        self.binder_host = binder_host
        self.binder_port = binder_port

    # aceita conexoes e trata varios clientes ao mesmo tempo
    # usa threading para atender varios clientes/usuarios
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            self.port = server_socket.getsockname()[1]
            self.register_service()
            server_socket.listen()
            print(f"[SERVER] {self.service_name} escutando em {self.host}:{self.port}")
            while True:
                conn, addr = server_socket.accept()
                threading.Thread(target=self.handle_client, args=(conn,)).start()

    # funcao de registro se conecta ao binder e envia REGISTER
    def register_service(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder_socket:
            binder_socket.connect((self.binder_host, self.binder_port))
            message = f"REGISTER|{self.service_name}|{self.host}|{self.port}"
            binder_socket.sendall(message.encode())
            response = binder_socket.recv(1024)
            print(f"[SERVER] Registro no Binder: {response.decode()}")

    # cada conexxo recebe uma funcao e seus args, executa e retorna o resultado
    def handle_client(self, conn):
        with conn:
            data = conn.recv(4096)
            func_name, args = deserialize(data)
            try:
                result = getattr(self.service_instance, func_name)(*args)
                conn.sendall(serialize(result))
            except Exception as e:
                conn.sendall(serialize(f"ERRO: {e}"))