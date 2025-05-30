import pickle

# serializa objetos usando pickle
def serialize(data):
    return pickle.dumps(data)

# desserializa os dados recebidos
def deserialize(data_bytes):
    return pickle.loads(data_bytes)