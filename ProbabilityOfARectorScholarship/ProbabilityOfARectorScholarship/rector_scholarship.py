# Autorzy: Patrycja Bednarska i Maciej Dzieciuch
# Uruchamiamy plik rector_scholarship.py

"""
=====================================================
Prawdopodobieństwo otrzymania stypendium rektorskiego
=====================================================

Program oblicza prawdopodobieństwo otrzymania stypendium rektorskiego na podstawie 3 parametrów wejściowych.

* Parametry wejściowe:
    - `average of ratings`
        * Jest to parametr określający średnią jaką otrzymaliśmy z ostatniego roku studiów,
          podajemy go w skali od 2.0 do 5.0.
    - `scientific achievements`
        * Jest to parametr określający ilość osiągnięć naukowych z ostatniego roku studiów,
          podajemy go w skali od 0 do 10.
    - `material situation`
        * Jest to parametr określający jaka sytuacja materialna jest u danego studenta,
          uzupełniamy go w skali od 0 do 1200. (Jednostką są PLN)
* Parametry wyjściowe:
    - `scholarship`
        * Jest to parametr określający w jakim zakresie od 0 do 100% mamy szanse na otrzymanie stypendium rektorskiego.
          (Następnie uczelnia może założyć sobie, że jeżeli wynik będzie 50-75% to student otrzymuje np. 4 pkt
          i przypisaną do tych pkt wysokość stypendium itd.)
* Role:
    (do uzupełnienia)
* Zastosowanie
    (do uzupełnienia)
"""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

"""
    Poniżej określamy nasze parametry wejściowe oraz wyjściowe
"""
average_of_ratings = ctrl.Antecedent(np.arange(2, 5.01, 1), 'average of ratings')
scientific_achievements = ctrl.Antecedent(np.arange(0, 11, 1), 'scientific achievements')
material_situation = ctrl.Antecedent(np.arange(0, 1201, 1), 'material situation')
scholarship = ctrl.Consequent(np.arange(0, 101, 1), 'scholarship')

"""
Definiujemy automatyczny podział "członkostwa" dla parametrów wejściowych
"""
average_of_ratings.automf(3)
scientific_achievements.automf(3)
material_situation.automf(3)

"""
Definiujemy niestandardowy podział "członkostwa" dla parametru wyjściowego 
i granice określające prawdopodobieństwo uzyskania stypendium
"""
scholarship['low'] = fuzz.trimf(scholarship.universe, [0, 0, 25])
scholarship['medium'] = fuzz.trimf(scholarship.universe, [25, 75, 100])
scholarship['high'] = fuzz.trimf(scholarship.universe, [76, 100, 100])

"""
Role
-----------

Poniżej znajduje się lista metod które są odzwierciedleniem poniżej przygotownych ról dla określania prawdopodobieństwa 
otrzymania stypendium rektorskiego.

1. Jeżeli średnia z ocen jest słaba i liczba osiągnięć naukowych jest niska 
   to szansa na stypendium rektorskie jest niska.
   
2. Jeżeli średnia z ocen jest wysoka i liczba osiągnięć naukowych jest wysoka i dochód na osobę 
   w gospodarstwie domowym jest niski to szansa na otrzymanie stypendium rektorskiego jest wysoka.
   
3. Jeżeli średnia z ocen jest wysoka to szansa na otrzymanie stypendium rektorskiego jest średnia.

4. Jeżeli średnia z ocen jest średnia i liczba osiągnięć naukowych jest średnia to szansa 
   na otrzymanie stypendium rektorskiego jest wysoka.
   
5. Jeżeli średnia z ocen jest wysoka i dochód na osobę w gospodarstwie domowym jest niski to szansa 
   na otrzymanie stypendium rektorskiego jest wysoka.
   
6. Jeżeli średnia z ocen jest średnia i liczba osiągnięć naukowych jest niska lub dochód na osobę w gospodarstwie 
   domowym jest średnia to szansa na otrzymanie stypendium rektorskiego jest średnia.
"""

rule1 = ctrl.Rule(average_of_ratings['poor'] & scientific_achievements['poor'], scholarship['low'])
rule2 = ctrl.Rule(average_of_ratings['good'] & scientific_achievements['good'] & material_situation['poor'],
                  scholarship['high'])
rule3 = ctrl.Rule(average_of_ratings['good'], scholarship['medium'])
rule4 = ctrl.Rule(average_of_ratings['average'] & scientific_achievements['average'], scholarship['high'])
rule5 = ctrl.Rule(average_of_ratings['good'] & material_situation['poor'], scholarship['high'])
rule6 = ctrl.Rule(average_of_ratings['average'] & scientific_achievements['poor'] | material_situation['average'],
                  scholarship['medium'])
rule7 = ctrl.Rule(average_of_ratings['good'] & scientific_achievements['good'], scholarship['high'])

"""
Określamy system kontroli według listy ról które podajemy jako listę w argumencie klasy
"""

# scholarship_ctrl = ctrl.ControlSystem([rule1, rule2, rule4, rule5, rule6, rule7])
# scholarship_ctrl = ctrl.ControlSystem([rule7])
scholarship_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
# scholarship_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

"""
Określamy system kontroli symulacji który będzie generował symulację
"""

scholarship_sim = ctrl.ControlSystemSimulation(scholarship_ctrl)

"""
Przekazujemy wartości dla parametrów wejściowych z których ma być określone prawdopodobieństwo
"""
scholarship_sim.input['average of ratings'] = 2
scholarship_sim.input['scientific achievements'] = 10
scholarship_sim.input['material situation'] = 1

"""
Wykonujemy obliczanie na podstawie zadanych wartości parametrów i określonych wcześniej ról
"""
scholarship_sim.compute()

"""
Wyświetlamy wynik w konsoli oraz rysujemy wykres który pokazuje w jakim przedziale jesteśmy 
i jakie mamy prawdopodobieństwo na otrzymanie stypendium rektorskiego
"""
print(scholarship_sim.output['scholarship'])
scholarship.view(sim=scholarship_sim)
