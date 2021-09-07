from abc import abstractclassmethod, ABCMeta
import json
import pickle


class SerializationInterfece(metaclass=ABCMeta):
    
    @abstractclassmethod
    def serialize(self):
        pass
    
    @abstractclassmethod
    def deserialize(self):
        pass

class SerializationToJson(SerializationInterfece):
    def serialize(self, data):
        return json.dumps(data)

    def deserialize(self, data):
        return json.loads(data)

