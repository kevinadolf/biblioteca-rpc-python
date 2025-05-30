import socket
from rpc.serializer import serialize, deserialize

# cliente rpc que descobre servicos no binder
class RPCClient:
    def __init__(self, binder_host='localhost', binder_port=8000):
        self.binder_host = binder_host
        self.binder_port = binder_port

    # funcao lookup se conecta ao binder e envia LOOKUP
    def lookup(self, service_name):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.binder_host, self.binder_port))
            s.sendall(f"LOOKUP|{service_name}".encode())
            data = s.recv(1024).decode()
            if data == 'NOT_FOUND':
                raise Exception("nenhum serviço encontrado!!!")
            ip, port = data.split('|') #separacao de msgs
            return ip, int(port)
    # funcao call envia chamada serializada para o servidor e espera resposta
    def call(self, ip, port, func_name, args):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(serialize((func_name, args)))
            return deserialize(s.recv(4096))