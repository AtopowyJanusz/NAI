"""
Autorzy: Patrycja Bednarska i Maciej Dzieciuch
Wymagania:
    python 3.8
    pip install scikit-learn
Start programu:
    python recommend_movie_engine.py
"""
import numpy as np
from numpy import random
from sklearn import svm


"""
Załadowanie pliku z danymi do nauczenia algorytmu oraz wykonanie funkcji loadtxt 
która zczytuje wszystkie dane z pliku wejściowego
"""
input_file = 'pima-indians-diabetes.txt'
data = np.loadtxt(input_file, delimiter=',')

"""
Dla zmiennej X przypisanie wszystkich wartości dla kolumn od 0 do 7
Dla zmiennej y przypisanie ostatniej kolumny
"""
X = data[:, :8]
y = data[:, 8]

"""
Wykonujemy funkcję SVC z biblioteki scikit-learn do której podajemy w argumentach
jądro które ma zostać użyte przez algorytm, parametr regularności C oraz współczynnik gamma 
"""
svc = svm.SVC(kernel='linear', C=1, gamma=100).fit(X, y)

"""
Deklarujemy tablicę XX.
Wykonujemy pętle for określoną do ilości kolumn od 0 do 7 gdzie pobieramy kolejno minimalne i maksymalne wartości
z każdej z kolumn następnie wykonujemy funkcję randint która generuje 100 pseudolosowych liczb określonych przedziałem
zmiennych tmp_min oraz tmp_max.
Na końcu przypisujemy do tablicy XX każde wygenerowane pseudolosowe liczby
w określonych przedziałach dla wszystkich kolumn.
"""
XX = []
for i in range(8):
    tmp_min, tmp_max = X[:, i].min(), X[:, i].max()
    XX.append(random.randint(tmp_min, tmp_max, size=100))

"""
Wykonujemy funkcję asarray z biblioteki numpy która generuje macierz z danymi o typie zmiennoprzecinkowym float.
Następnie wykonywana jest funkcja predict z biblioteki scikit-learn która wykonuje transpozycję macierzy danych.
"""
XX = np.asarray(XX, dtype=np.float32)
Z = svc.predict(np.c_[XX.transpose()])
print("Pima indians diabetes ", Z)


input_file = 'magic-gamma-telescope.txt'
data = np.loadtxt(input_file, delimiter=',')

X = data[:, :10]
y = data[:, 10]

svc = svm.SVC(kernel='linear', C=1, gamma=100).fit(X, y)

XX = []

for i in range(10):
    tmp_min, tmp_max = X[:, i].min(), X[:, i].max()
    XX.append(np.arange(tmp_min, tmp_max, (tmp_max - tmp_min) / 101)[:100])

XX = np.asarray(XX, dtype=np.float32)
Z = svc.predict(np.c_[XX.transpose()])
print("Magic gamma telescope", Z)
