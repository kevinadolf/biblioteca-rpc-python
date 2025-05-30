# arquivo exemplo com servicos com as operacoes de echo

# servico com ops de eco
class EchoService:
    # metodo que retorna a mensagem recebida
    def echo(self, mensagem):
        print(f"[EchoService] Mensagem recebida para ecoar: '{mensagem}'")
        return f"Servidor diz: eco de '{mensagem}'"

    # outro méetodo simples
    def ping(self):
        print("[EchoService] Ping recebido")
        return "pong! 3 a 2 ganhei, esquece"