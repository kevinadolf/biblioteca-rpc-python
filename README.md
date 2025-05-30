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


## Como rodar o exemplo da calculadora
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
```

# ENGLISH

## Introduction
This project is an implementation of an RPC (Remote Procedure Call) library in Python. The idea is to allow functions of a service to be called remotely, as if they were local. The library was built using only standard Python features (no `pip install` of external libraries) and organized модульнаяly using Object-Oriented Programming (OOP).

## How the Architecture Works
The system has a few main components:

* **`RPCBinder` (`rpc/rpc_binder.py`)**:
    * It's like a "catalog" for services.
    * Servers register with it, providing their name, IP, and port.
    * Clients query the binder to find out where a service is running.
    * It has a `start_binder()` function to initialize it, as requested.

* **`RPCServer` (`rpc/rpc_server.py`)**:
    * It's the process that hosts the service objects (the classes with methods that will be called remotely, like `MathService`).
    * When it starts, it registers with the `RPCBinder`.
    * It listens for client calls, deserializes the data, invokes the function, and returns the serialized result.
    * It uses `threading` to handle multiple clients simultaneously (concurrent server).

* **`RPCClient` (`rpc/rpc_client.py`)**:
    * Used by the end-user client code (via the stub).
    * First, it queries the `RPCBinder` to find the address (IP and port) of the desired service.
    * Then, it connects directly to the `RPCServer` of that service to make the remote function call, sending the request and receiving the result.

* **`Serializer` (`rpc/serializer.py`)**:
    * Responsible for "packing" (serializing) the call data (function name, arguments) and the result to be sent over the network.
    * It also "unpacks" (deserializes) the received data.
    * This project uses `pickle` for this, which is a standard library tool.

* **`Service Stubs` (in `rpc/rpc_stub_generator.py`)**:
    * The "stub" is an object on the client-side that masks the complexity of remote communication. It has the same methods as the remote service, but when you call a method on the stub, it handles sending the message to the server and getting the response.
    * In the `rpc_stub_generator.py` file, you'll find the stub classes (like `MathServiceStub`).
    * Each stub is written manually for a specific service.


## File Structure
The project is organized exactly as requested:

biblioteca_rpc/
├── rpc/ # Main logic of the RPC library

│   ├── init.py # Indicates that 'rpc' is a Python package

│   ├── rpc_binder.py # The binder (service locator)

│   ├── rpc_client.py # RPC client logic (used by the stub)

│   ├── rpc_server.py # RPC server logic

│   ├── rpc_stub_generator.py # Contains the manual stub classes

│   └── serializer.py # For serializing/deserializing data

├── interface/ # Definitions of service interfaces

│   └── math_service.py # Example interface (calculator)

├── examples/ # Examples of how to use the library

│   ├── client_example.py # Example client using math_service

│   └── server_example.py # Example server registering math_service

└── README.md # This file (execution and organization manual)

## How to Run the Calculator Example
You will need 3 open terminals.

1.  **Start the Binder**:
    In the first terminal, navigate to the project's root folder (`biblioteca_rpc/`) and run:
    ```bash
    python -m rpc.rpc_binder
    ```
    You should see something like: `[BINDER] server started at localhost:8000`

2.  **Start the `math_service` Server**:
    In the second terminal, in the same root folder, run:
    ```bash
    python examples/server_example.py
    ```
    You should see messages indicating that the `math_service` has been registered with the binder and is listening on some port (e.g., `[SERVER] math_service listening on localhost:xxxx`).

3.  **Execute the Client**:
    In the third terminal, in the root folder, run:
    ```bash
    python examples/client_example.py
    ```

4.  **Expected output in the Client** (exactly as in the assignment PDF):
    ```
    Result of 5 + 3: 8
    Result of 4 * 2: 8
    Result of 5 - 3: 2
    Result of 4 / 2: 2.0
    ```

## How to Add New Services (Manually)
To add a new service (for example, an `EchoService` that returns the message it received), follow these steps:

### Step 1: Define the New Service Interface

Create a new Python file in `interface/`. For example, `interface/echo_service.py`:

```python
# interface/echo_service.py
# Service with echo operations
class EchoService:
    # Method that returns the received message
    def echo(self, message):
        print(f"[EchoService] Message received to echo: '{message}'")
        return f"Server says: echo of '{message}'"

    # Another simple method
    def ping(self):
        print("[EchoService] Ping received")
        return "pong! 3 to 2 I won, forget it"
```

Okay, I'll translate the entire README.md into English for you, maintaining the structure and informal tone, and translating comments within the code examples.

Here's the translated README.md:
Markdown

# RPC Library in Python - Distributed Systems Practical Assignment
Student: Kevin Adolfo Carvalho Koberstain de Araujo - 202110036511

## Introduction
This project is an implementation of an RPC (Remote Procedure Call) library in Python. The idea is to allow functions of a service to be called remotely, as if they were local. The library was built using only standard Python features (no `pip install` of external libraries) and organized модульнаяly using Object-Oriented Programming (OOP).

## How the Architecture Works
The system has a few main components:

* **`RPCBinder` (`rpc/rpc_binder.py`)**:
    * It's like a "catalog" for services.
    * Servers register with it, providing their name, IP, and port.
    * Clients query the binder to find out where a service is running.
    * It has a `start_binder()` function to initialize it, as requested.

* **`RPCServer` (`rpc/rpc_server.py`)**:
    * It's the process that hosts the service objects (the classes with methods that will be called remotely, like `MathService`).
    * When it starts, it registers with the `RPCBinder`.
    * It listens for client calls, deserializes the data, invokes the function, and returns the serialized result.
    * It uses `threading` to handle multiple clients simultaneously (concurrent server).

* **`RPCClient` (`rpc/rpc_client.py`)**:
    * Used by the end-user client code (via the stub).
    * First, it queries the `RPCBinder` to find the address (IP and port) of the desired service.
    * Then, it connects directly to the `RPCServer` of that service to make the remote function call, sending the request and receiving the result.

* **`Serializer` (`rpc/serializer.py`)**:
    * Responsible for "packing" (serializing) the call data (function name, arguments) and the result to be sent over the network.
    * It also "unpacks" (deserializes) the received data.
    * This project uses `pickle` for this, which is a standard library tool.

* **`Service Stubs` (in `rpc/rpc_stub_generator.py`)**:
    * The "stub" is an object on the client-side that masks the complexity of remote communication. It has the same methods as the remote service, but when you call a method on the stub, it handles sending the message to the server and getting the response.
    * In the `rpc_stub_generator.py` file, you'll find the stub classes (like `MathServiceStub`).
    * Each stub is written manually for a specific service.

## File Structure
The project is organized exactly as requested:

biblioteca_rpc/
├── rpc/ # Main logic of the RPC library
│   ├── init.py # Indicates that 'rpc' is a Python package
│   ├── rpc_binder.py # The binder (service locator)
│   ├── rpc_client.py # RPC client logic (used by the stub)
│   ├── rpc_server.py # RPC server logic
│   ├── rpc_stub_generator.py # Contains the manual stub classes
│   └── serializer.py # For serializing/deserializing data
├── interface/ # Definitions of service interfaces
│   └── math_service.py # Example interface (calculator)
├── examples/ # Examples of how to use the library
│   ├── client_example.py # Example client using math_service
│   └── server_example.py # Example server registering math_service
└── README.md # This file (execution and organization manual)


## How to Run the Calculator Example
You will need 3 open terminals.

1.  **Start the Binder**:
    In the first terminal, navigate to the project's root folder (`biblioteca_rpc/`) and run:
    ```bash
    python -m rpc.rpc_binder
    ```
    You should see something like: `[BINDER] server started at localhost:8000`

2.  **Start the `math_service` Server**:
    In the second terminal, in the same root folder, run:
    ```bash
    python examples/server_example.py
    ```
    You should see messages indicating that the `math_service` has been registered with the binder and is listening on some port (e.g., `[SERVER] math_service listening on localhost:xxxx`).

3.  **Execute the Client**:
    In the third terminal, in the root folder, run:
    ```bash
    python examples/client_example.py
    ```

4.  **Expected output in the Client** (exactly as in the assignment PDF):
    ```
    Result of 5 + 3: 8
    Result of 4 * 2: 8
    Result of 5 - 3: 2
    Result of 4 / 2: 2.0
    ```

## How to Add New Services (Manually)
To add a new service (for example, an `EchoService` that returns the message it received), follow these steps:

### Step 1: Define the New Service Interface

Create a new Python file in `interface/`. For example, `interface/echo_service.py`:

```python
# interface/echo_service.py
# Service with echo operations
class EchoService:
    # Method that returns the received message
    def echo(self, message):
        print(f"[EchoService] Message received to echo: '{message}'")
        return f"Server says: echo of '{message}'"

    # Another simple method
    def ping(self):
        print("[EchoService] Ping received")
        return "pong! 3 to 2 I won, forget it"
```
