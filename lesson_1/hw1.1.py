from abc import abstractclassmethod, ABCMeta
import json
import pickle
import math


class SerializationInterfece(metaclass=ABCMeta):
    
    @abstractclassmethod
    def serialize(self):
        pass
    
    @abstractclassmethod
    def deserialize(self):
        pass

class SerializationToJsonList(SerializationInterfece):
    def serialize(self, data):
        return json.dumps(data)

    def deserialize(self, pack_data):
        return json.loads(pack_data)


class SerializationToJsonDict(SerializationInterfece):
    def serialize(self, data):
        return json.dumps(data)

    def deserialize(self, pack_data):
        return json.loads(pack_data)


class SerializationToJsonSet(SerializationInterfece):
    def serialize(self, data):
        return json.dumps(list(data))

    def deserialize(self, pack_data):
        deserialize_date = json.loads(pack_data)
        for i, el in enumerate(deserialize_date):
            if type(el) == list:
                deserialize_date[i] = tuple(el)
        return set(deserialize_date)


class SerializationToJsonTuple(SerializationInterfece):
    def serialize(self, data):
        return json.dumps(list(data))

    def deserialize(self, pack_data):
        return tuple(json.loads(pack_data))


class SerializationToBinList(SerializationInterfece):
    def serialize(self, data):
        return pickle.dumps(data)

    def deserialize(self, pack_data):
        return pickle.loads(pack_data)


class SerializationToBinDict(SerializationInterfece):
    def serialize(self, data):
        return pickle.dumps(data)

    def deserialize(self, pack_data):
        return pickle.loads(pack_data)


class SerializationToBinSet(SerializationInterfece):
    def serialize(self, data):
        return pickle.dumps(data)

    def deserialize(self, pack_data):
        return pickle.loads(pack_data)


class SerializationToBinTuple(SerializationInterfece):
    def serialize(self, data):
        return pickle.dumps(data)

    def deserialize(self, pack_data):
        return pickle.loads(pack_data)


data_list = [1, '2', math.pi, (1,2,3), False]
data_list = [1,2,3,"4",{100:"100"},(1,2,3)]
data_dict_bin = {1: 2, '2': '3', (1,2,3): True, '3': math.pi, '4': [1,2,3], '5': set('bin'), '6' :tuple('set'), '7': {1:2, 3:4}}
data_dict_json = {'1': 2, '2': '3', '0': True, '3': math.pi, '4': [1,2,3], '5': 'json', '6' :'json', '7': 0}
data_set = {'r', (3,4,5), 2, math.pi}
data_tuple = (1,'2', math.pi, [1,2,3], False)

print(f'serialize  - deserialize json list \n{data_list}:')
packed_data = SerializationToJsonList().serialize(data_list)
print(f'serialize data - \n{packed_data}')
data_after = SerializationToJsonList().deserialize(packed_data)
print(f'deserialize data \n{data_after}')
try:
    assert data_list == data_after, 'No correct deserialize json list'
    print("\njson list serialization and deserialization was successful\n")
except AssertionError as error:
    print(f'\n{error}\n')

print(f'serialize  - deserialize json dict \n{data_dict_json}:')
packed_data = SerializationToJsonDict().serialize(data_dict_json)
print(f'serialize data - \n{packed_data}')
data_after = SerializationToJsonDict().deserialize(packed_data)
print(f'deserialize data \n{data_after}')
try:
    assert data_dict_json == data_after, 'No correct deserialize json dict'
    print("\njson dict serialization and deserialization was successful\n")
except AssertionError as error:
    print(f'\n{error}\n')

print(f'serialize  - deserialize json set \n{data_set}:')
packed_data = SerializationToJsonSet().serialize(data_set)
print(f'serialize data - \n{packed_data}')
data_after = SerializationToJsonSet().deserialize(packed_data)
print(f'deserialize data \n{data_after}')
try:
    assert data_set == data_after, 'No correct deserialize json set'
    print("\njson set serialization and deserialization was successful\n")
except AssertionError as error:
    print(f'\n{error}\n')
    

print(f'serialize  - deserialize json tuple \n{data_tuple}:')
packed_data = SerializationToJsonTuple().serialize(data_tuple)
print(f'serialize data - \n{packed_data}')
data_after = SerializationToJsonTuple().deserialize(packed_data)
print(f'deserialize data \n{data_after}')
try:
    assert data_tuple == data_after, 'No correct deserialize json tuple'
    print("\njson tuple serialization and deserialization was successful\n")
except AssertionError as error:
    print(f'\n{error}\n')

print(f'serialize  - deserialize bin list \n{data_list}:')
packed_data = SerializationToBinList().serialize(data_list)
print(f'serialize data - \n{packed_data}')
data_after = SerializationToBinList().deserialize(packed_data)
print(f'deserialize data \n{data_after}')
try:
    assert data_list == data_after, 'No correct deserialize bin list'
    print("\nbin list serialization and deserialization was successful\n")
except AssertionError as error:
    print(f'\n{error}\n')

print(f'serialize  - deserialize bin dict \n{data_dict_bin}:')
packed_data = SerializationToBinDict().serialize(data_dict_bin)
print(f'serialize data - \n{packed_data}')
data_after = SerializationToBinDict().deserialize(packed_data)
print(f'deserialize data \n{data_after}')
try:
    assert data_dict_bin == data_after, 'No correct deserialize bin dict'
    print("\nbin dict serialization and deserialization was successful\n")
except AssertionError as error:
    print(f'\n{error}\n')

print(f'serialize  - deserialize bin set \n{data_set}:')
packed_data = SerializationToBinSet().serialize(data_set)
print(f'serialize data - \n{packed_data}')
data_after = SerializationToBinSet().deserialize(packed_data)
print(f'deserialize data \n{data_after}')
try:
    assert data_set == data_after, 'No correct deserialize bin set'
    print("\nbin set serialization and deserialization was successful\n")
except AssertionError as error:
    print(f'\n{error}\n')

print(f'serialize  - deserialize bin tuple v{data_tuple}:')
packed_data = SerializationToBinTuple().serialize(data_tuple)
print(f'serialize data - \n{packed_data}')
data_after = SerializationToBinTuple().deserialize(packed_data)
print(f'deserialize data \n{data_after}')
try:
    assert data_tuple == data_after, 'No correct deserialize bin tuple'
    print("\nbin tuple serialization and deserialization was successful\n")
except AssertionError as error:
    print(f'\n{error}\n')
