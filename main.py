import pickle

objects = []

with open("sparse_encoder.pkl", 'rb') as f:
    while True:
        try:
            objects.append(pickle.load(f))
            print(objects)
        except EOFError:
            break
        
print(objects)