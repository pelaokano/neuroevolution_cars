import numpy as np
import pickle

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

class NeuralNetwork:
    def __init__(self, architecture=[6, 6, 4]):
        self.sizes = architecture
        self.num_layers = len(self.sizes)
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def feedforward(self, input_vector):
        """input_vector: list o array de forma (6,) con [d1, d2, d3, d4, d5, velocity]"""
        a = np.array(input_vector).reshape(-1, 1)
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a.flatten()  # devuelve array 1D con 4 salidas

    def decide_action(self, input_vector, threshold=0.5):
        """Devuelve acciones booleanas [acelerar, frenar, derecha, izquierda]"""
        output = self.feedforward(input_vector)
        return [o > threshold for o in output]

    def clone(self):
        """Devuelve una copia (útil para evolución genética)"""
        clone = NeuralNetwork(self.sizes)
        clone.weights = [np.copy(w) for w in self.weights]
        clone.biases = [np.copy(b) for b in self.biases]
        return clone

def save_top_networks(networks, cars, top_n=10, filename="top_networks.pkl"):
    top_indices = sorted(range(len(cars)), key=lambda i: cars[i].score, reverse=True)[:top_n]
    top_nets = [networks[i] for i in top_indices]
    with open(filename, "wb") as f:
        pickle.dump(top_nets, f)
    print(f"Top {top_n} redes guardadas en {filename}")

def mutate_weights(network, mutation_rate=0.1, mutation_strength=0.5):
    for i in range(len(network.weights)):
        noise = np.random.randn(*network.weights[i].shape) * mutation_strength
        mask = np.random.rand(*network.weights[i].shape) < mutation_rate
        network.weights[i] += noise * mask

def mutate_biases(network, mutation_rate=0.1, mutation_strength=0.5):
    for i in range(len(network.biases)):
        noise = np.random.randn(*network.biases[i].shape) * mutation_strength
        mask = np.random.rand(*network.biases[i].shape) < mutation_rate
        network.biases[i] += noise * mask

def crossover_weights(parent1, parent2, child):
    for i in range(len(child.weights)):
        mask = np.random.rand(*child.weights[i].shape) < 0.5
        child.weights[i] = np.where(mask, parent1.weights[i], parent2.weights[i])

def crossover_biases(parent1, parent2, child):
    for i in range(len(child.biases)):
        mask = np.random.rand(*child.biases[i].shape) < 0.5
        child.biases[i] = np.where(mask, parent1.biases[i], parent2.biases[i])