# importe o stub do novo servico alem do MathServiceStub
from rpc.rpc_stub_generator import MathServiceStub, EchoServiceStub

if __name__ == '__main__':
    print("--- testando mathservice ---")
    math_stub = MathServiceStub()
    print("resultado de 5 + 3:", math_stub.add(5, 3))
    print("resultado de 4 * 2:", math_stub.multiply(4, 2))
    print("resultado de 5 - 3:", math_stub.sub(5, 3))
    print("resultado de 4 / 2:", math_stub.divide(4, 2))
    print("-" * 30)

    print("--- testando echoservice ---")
    # instancie o stub do novo servico
    echo_stub = EchoServiceStub()

    # chame os metodos do novo servico
    mensagem_original = "ola mundo distribuido!"
    mensagem_ecoada = echo_stub.echo(mensagem_original)
    print(f"enviado para eco: '{mensagem_original}'")
    print(f"recebido do eco: '{mensagem_ecoada}'")

    resposta_ping = echo_stub.ping()
    print(f"resposta do ping: '{resposta_ping}'")