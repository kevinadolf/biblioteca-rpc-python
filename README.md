# Biblioteca RPC em Python - Sistemas Distribuídos

## Contexto
Este projeto é uma implementação de uma biblioteca de RPC (Remote Procedure Call) em Python. O foco é permitir que funções de um serviço sejam chamadas remotamente, como se fossem locais. A biblioteca foi feita usando apenas recursos/bibliotecas padrão do Python, organizada de forma modular e usando POO.

## Como Funciona a Arquitetura
O sistema tem alguns componentes principais:

* **`RPCBinder` (`rpc/rpc_binder.py`)**:
    * É tipo um "catálogo" dos serviços.
    * Os servidores se registram nele informando seu nome, IP e porta.
    * Os clientes consultam o binder para descobrir onde um serviço está rodando.
    * Ele tem uma função `start_binder()` para iniciar, como pedido.

* **`RPCServer` (`rpc/rpc_server.py`)**:
    * É o processo que hospeda os objetos de serviço (as classes com os métodos que serão chamados remotamente, tipo `MathService`).
    * Quando ele inicia, ele se registra no `RPCBinder`.
    * Fica escutando por chamadas de clientes, desserializa os dados, invoca a função e devolve o resultado serializado.
    * Ele usa `threading` para conseguir atender vários clientes ao mesmo tempo (servidor concorrente).

* **`RPCClient` (`rpc/rpc_client.py`)**:
    * Usado pelo código do cliente final (através do stub).
    * Primeiro, ele consulta o `RPCBinder` para achar o endereço (IP e porta) do serviço desejado.
    * Depois, ele se conecta diretamente ao `RPCServer` desse serviço para fazer a chamada da função remota, enviando a requisição e recebendo o resultado.

* **`Serializer` (`rpc/serializer.py`)**:
    * Responsável por "empacotar" (serializar) os dados da chamada (nome da função, argumentos) e o resultado para serem enviados pela rede.
    * Também "desempacota" (desserializar) os dados recebidos.
    * Este projeto usa `pickle` para isso, que é uma ferramenta da biblioteca padrão.

* **`Stubs de Serviço` (em `rpc/rpc_stub_generator.py`)**:
    * O "stub" é um objeto no lado do cliente que mascara a complexidade da comunicação remota. Ele tem os mesmos métodos que o serviço remoto, mas quando você chama um método no stub, ele cuida de enviar a mensagem para o servidor e pegar a resposta.
    * No arquivo `rpc_stub_generator.py`, você encontrará as classes de stub (como `MathServiceStub`).
    * Cada stub é escrito manually para um serviço específico.

## Estrutura de Arquivos
O projeto está organizado da seguinte forma:

biblioteca_rpc/
├── rpc/ # logica principal da biblioteca rpc
│   ├── __init__.py # indica que 'rpc' eh um pacote python
│   ├── rpc_binder.py # o binder (localizador de servicos)
│   ├── rpc_client.py # logica do cliente rpc (usado pelo stub)
│   ├── rpc_server.py # logica do servidor rpc
│   ├── rpc_stub_generator.py # contem as classes de stub manuais
│   └── serializer.py # para serializar/desserializar dados
├── interface/ # definicoes das interfaces dos servicos
|   └── echo_service.py # exemplo de novo servico (mensagem ecoada)
│   └── math_service.py # exemplo de interface (calculadora)
├── examples/ # exemplos de como usar a biblioteca
│   ├── client_example.py # exemplo de cliente usando o math_service
│   └── server_example.py # exemplo de servidor registrando o math_service
└── README.md # manual de execucao e organizacao

## como rodar o exemplo da calculadora
Serão necessários 3 terminais diferentes.

1.  **inicie o binder**:
    no primeiro terminal, abra a pasta do projeto (`biblioteca_rpc/`) e rode:
    ```bash
    python -m rpc.rpc_binder
    ```
    voce deve ver algo como: `[BINDER] servidor iniciado em localhost:8000`

2.  **inicie o servidor do servico `math_service`**:
    no segundo terminal, na mesma pasta, rode:
    ```bash
    python examples/server_example.py
    ```
    voce deve ver mensagens indicando que o servico `math_service` foi registrado no binder e esta escutando em alguma porta (ex: `[SERVER] math_service escutando em localhost:xxxx`).

3.  **Execute o cliente**:
    no terceiro terminal, ainda na pasta, rode:
    ```bash
    python examples/client_example.py
    ```

4.  **Saida esperada no cliente**
    ```
    Resultado de 5 + 3: 8
    Resultado de 4 * 2: 8
    Resultado de 5 - 3: 2
    Resultado de 4 / 2: 2.0
    ```

## Como adicionar novos servicos
para adicionar um novo servico (por exemplo, um `EchoService` que devolve a mensagem que recebeu), siga estes passos:

### Passo 1: definir a interface do novo servico

Crie um novo arquivo python em `interface/`. por exemplo, `interface/echo_service.py`:

```python
class EchoService:
    # metodo que retorna a mensagem recebida
    def echo(self, mensagem):
        print(f"[echoservice] mensagem recebida para ecoar: '{mensagem}'")
        return f"servidor diz: eco de '{mensagem}'"

    # outro metodo simples
    def ping(self):
        print("[echoservice] ping recebido")
        return "pong! 3 a 2 ganhei, esquece"
