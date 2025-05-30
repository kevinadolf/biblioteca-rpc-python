from rpc.rpc_server import RPCServer
from interface.math_service import MathService
from interface.echo_service import EchoService # <--- importe a classe do novo servico
import threading

if __name__ == '__main__':
    # configurando e iniciando o math_service
    math_server = RPCServer(service_name='math_service', service_instance=MathService())
    thread_math = threading.Thread(target=math_server.start)
    thread_math.start()
    print("[main server] math_service iniciado em background...")

    # --- configurando e iniciando o echo_service ---
    # crie uma instancia do seu novo servico
    echo_service_instance = EchoService()
    
    # crie uma instancia do RPCServer para o novo servico
    #    use um 'service_name' unico para o binder
    echo_server = RPCServer(service_name='echo_service', service_instance=echo_service_instance)
    
    # inicie o servidor do echo_service em uma nova thread para nao bloquear
    thread_echo = threading.Thread(target=echo_server.start)
    thread_echo.start()
    print("[main server] echo_service iniciado em background...")

    # espera as threads dos servidores terminarem 
    thread_math.join()
    thread_echo.join()
    print("[main server] todos os servicos foram finalizados.")