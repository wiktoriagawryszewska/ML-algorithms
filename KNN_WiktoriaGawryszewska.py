from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import numpy as np

#  Wczytanie danych ze zbioru iris
iris = load_iris()
X = iris.data       # cechy
y = iris.target     # klasy

# Podział na zbiór treningowy (70%) i testowy (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=15)

# Funkcja licząca odległość euklidesową między dwoma punktami
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

# Implementacja klasyfikatora KNN
def knn_classifier(X_train, y_train, X_test, k):
    predicted_classes = []  # lista na przewidywane klasy
    for test_point in X_test:
        # Oblicza dystanse od punktu testowego do wszystkich treningowych
        distances = [euclidean_distance(test_point, train_point) for train_point in X_train]

        # Znajduje indeksy k najbliższych sąsiadów
        nearest_indices = np.argsort(distances)[:k]

        # Odczytuje klasy tych k najbliższych sąsiadów
        nearest_labels = y_train[nearest_indices]

        # Zlicza ile razy pojawiła się każda klasa
        values, counts = np.unique(nearest_labels, return_counts=True)
        max_count = np.max(counts)

        # Jeśli więcej niż jedna klasa ma tyle samo głosów — remis
        if list(counts).count(max_count) > 1:
            predicted_classes.append(None)  # wpisz None w przypadku remisu
        else:
            # Wybiera klasę z największą liczbą głosów
            predicted_classes.append(values[np.argmax(counts)])

    return predicted_classes

# Używa klasyfikatora KNN z wybranym k
k = 3
y_pred = knn_classifier(X_train, y_train, X_test, k)

# Oblicza liczbę trafień
correct = sum(1 for pred, true in zip(y_pred, y_test) if pred == true)
total = len(y_test)
accuracy = correct / total * 100

# Sprawdza czy pojawił się jakikolwiek remis
if None in y_pred:
    print("None")  # wypisze None, jeśli jakikolwiek wynik to remis

# Wypisuje dokładność klasyfikacji
print(f"Dokładność (k={k}): {accuracy:.2f}%")
