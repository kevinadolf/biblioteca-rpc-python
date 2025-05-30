# rpc/rpc_stub_generator.py
from rpc.rpc_client import RPCClient

# stub para o servico de math
class MathServiceStub:
    # conecta ao binder e descobre ip e porta do servidor
    def __init__(self):
        self.client = RPCClient() # usa o cliente rpc padrao
        # o nome 'math_service' deve ser o mesmo usado pelo servidor ao se registrar no binder
        self.ip, self.port = self.client.lookup('math_service')

    # cada funcao abaixo eh um metodo do servico math que queremos chamar remotamente.
    # elas basicamente empacotam a chamada para o self.client.call.

    def add(self, a, b):
        return self.client.call(self.ip, self.port, 'add', (a, b))

    def multiply(self, a, b):
        return self.client.call(self.ip, self.port, 'multiply', (a, b))

    def sub(self, a, b):
        return self.client.call(self.ip, self.port, 'sub', (a, b))

    def divide(self, a, b):
        return self.client.call(self.ip, self.port, 'divide', (a, b))

# ---------------------------------------------------------------------------

# pra adicionar um stub para um novo servico (ex: EchoService):
# 1. copie a estrutura do MathServiceStub acima.
# 2. renomeie a classe para EchoServiceStub (ou o nome do seu servico + Stub).
# 3. no metodo __init__, mude 'math_service' para o nome do seu novo servico
#    (ex: self.ip, self.port = self.client.lookup('echo_service')).
# 4. para cada metodo do seu novo servico, crie um metodo correspondente no stub
#    que chama self.client.call, passando o nome do metodo e os argumentos.

# exemplo de como seria um EchoServiceStub:


# stub para o servico de echo
class EchoServiceStub:
    # conecta ao binder e descobre ip e porta do servidor de echo
    def __init__(self):
        self.client = RPCClient()
        # 'echo_service' eh o nome que o servidor do EchoService usara para se registrar no binder
        self.ip, self.port = self.client.lookup('echo_service')

    # metodo para chamar o 'echo' remoto
    def echo(self, mensagem):
        # o ultimo argumento eh uma tupla com os parametros da funcao remota
        return self.client.call(self.ip, self.port, 'echo', (mensagem,)) # (mensagem,) cria uma tupla com um elemento

    # metodo para chamar o 'ping' remoto
    def ping(self):
        return self.client.call(self.ip, self.port, 'ping', ()) # () para metodos sem argumentos