from utility import Utility
import time
import sys
import numpy as np
from copy import copy, deepcopy
import operator
from resources import st70_opt, toy_problem, pr76_opt, berlin52_opt, kroA100_opt


class Tsp:
    # problem_name = 'berlin52'
    # problem_name = 'a280'
    # problem_name = 'pr1002'
    # problem_name = 'kroA100'
    # problem_name = 'kroB200'
    # problem_name = 'pr76'
    problem_name = 'st70'

    # problem_name = 'bier127'
    # problem_name = 'ch130'

    def __init__(self):

        # Creo la matrice che rappresenta il problema
        self.matrix = Utility().create_matrix(self.problem_name)

        # Toy problem
        # self.matrix = toy_problem

        # Utility.print_matrix(self.matrix)

        # Costruisco la soluzione iniziale
        route = self.initial_solution(deepcopy(self.matrix))

        # Stampa del Percorso e costo iniziale
        print(route, self.cost(route))

        # Test dell'optimal tour
        print("Ottimo:")
        print(st70_opt, self.cost(st70_opt))
        # print(pr76_opt, self.cost(pr76_opt))
        # print(kroA100_opt, self.cost(kroA100_opt))
        # print(berlin52_opt, self.cost(berlin52_opt))

        # Percorso e costo dopo 2-opt
        # print(self.test_two_opt_neighborhood(route))

        route, cost = self.two_opt_neighborhood(route)
        print(route, cost)

        # Percorso e costo dopo 3-opt
        # print(self.test_three_opt_neighborhood(route))

        route, cost = self.three_opt_neighborhood(route)
        print(route, cost)

        # route, cost = self.two_opt_neighborhood(route)
        # print(route, cost)
        #
        # route, cost = self.three_opt_neighborhood(route)
        # print(route, cost)
        #
        # route, cost = self.two_opt_neighborhood(route)
        # print(route, cost)

    def cost(self, route):
        """
        Somma i valori contenuti negli elementi selezionati nella matrice

        ES. matrix[[0, 1], [2, 3]]
        Restituisce il contenuto della cella [0,1] e il contenuto della cella [2,3] che con .sum() vengono sommati

        In questo modo se ho una route [0,2,3], grazie ad np.roll
        vado a sommare gli elementi nella matrice in [[3,0,2][0,2,3]].sum()

        :param matrix:
        :param route:
        :return:
        """
        # print np.roll(route, 1)
        # print self.matrix[np.roll(route, 1), route]
        # print self.matrix[1][0]
        # return self.matrix[np.roll(route, 1)][route].sum()
        np.set_printoptions(precision=24)
        # print self.matrix[np.roll(route, 1), route]
        return int(self.matrix[np.roll(route, 1), route].sum())

    def two_opt_neighborhood(self, route):
        """
        Intorno 2-opt
        :return:
        """

        best_route = route
        best_cost = self.cost(route)

        # Aggiungo il nodo di start al fondo della lista
        route.append(route[0])

        # Numero di volte in qui e stato calcolato l'intorno
        count = 0
        # https://stackoverflow.com/questions/53275314/2-opt-algorithm-to-solve-the-travelling-salesman-problem-in-python
        improved = True
        while improved:
            count += 1
            improved = False
            for i in range(0, len(route)):
                for j in range(i + 2, len(route) - 1):

                    # print (route[i], route[i + 1]), (route[j], route[j + 1])

                    """
                    In list[first:last], last is not included.
                    The 10th element is ls[9], in ls[0:10] there isn't ls[10]
                    """

                    reverse = route[i + 1:j + 1]
                    # print(reverse)
                    new_route = route[:i + 1] + reverse[::-1] + route[j + 1:]
                    # print new_route

                    # Tolto l'ultimo elemento (duplicato dell start node) cosi da calcolare il costo
                    new_route_cost = self.cost(new_route[:len(new_route) - 1])
                    # new_route_cost = self.cost(new_route)

                    if new_route_cost < best_cost:
                        best_route = new_route
                        best_cost = new_route_cost
                        improved = True

            route = best_route

        print("Numero di intorni 2-opt visitati: ", count)
        return route[:len(route) - 1], best_cost

    def three_opt_neighborhood(self, route):
        """
        Intorno 3-opt
        :return:
        """

        best_route = route
        best_cost = self.cost(route)

        # Aggiungo il nodo di start al fondo della lista
        route.append(route[0])

        # Numero di volte in qui e stato calcolato l'intorno
        count = 0
        improved = True
        while improved:
            count += 1
            improved = False
            for i in range(len(route)):
                for j in range(i + 2, len(route) - 1):
                    for k in range(j + 2, len(route) - 1):

                        possibility = []

                        """
                        CASO 4 
                        """
                        reverse_path_1 = route[i + 1:j + 1]
                        reverse_path_2 = route[j + 1:k + 1]
                        new_route = route[:i + 1] + reverse_path_1[::-1] + reverse_path_2[::-1] + route[k + 1:]
                        possibility.append([new_route, self.cost(new_route[:len(new_route) - 1])])

                        """
                        CASO 5
                        """
                        reverse_path = route[j + 1:k + 1]
                        new_route = route[:i + 1] + reverse_path[::-1] + route[i + 1:j + 1] + route[k + 1:]
                        possibility.append([new_route, self.cost(new_route[:len(new_route) - 1])])

                        """
                        CASO 6 
                        """
                        reverse_path = route[i + 1:j + 1]
                        new_route = route[:i + 1] + route[j + 1:k + 1] + reverse_path[::-1] + route[k + 1:]
                        possibility.append([new_route, self.cost(new_route[:len(new_route) - 1])])

                        """
                        CASO 7 
                        """
                        new_route = route[:i + 1] + route[j + 1:k + 1] + route[i + 1:j + 1] + route[k + 1:]
                        possibility.append([new_route, self.cost(new_route[:len(new_route) - 1])])

                        best_option = min(possibility, key=lambda e: e[1])
                        new_route = best_option[0]
                        new_route_cost = best_option[1]

                        # reverse = route[j + 1:k + 1]
                        # new_route = route[:i + 1] + reverse[::-1] + route[i + 1:j + 1] + route[k + 1:]
                        #
                        # # Tolgo l'ultimo elemento (duplicato dell start node) cosi da calcolare il costo
                        # new_route_cost = self.cost(new_route[:len(new_route) - 1])
                        # # new_route_cost = self.cost(new_route)

                        if new_route_cost < best_cost:
                            best_route = new_route
                            best_cost = new_route_cost
                            improved = True

            route = best_route

        print("Numero di intorni 3-opt visitati: ", count)
        return route[:len(route) - 1], best_cost

    @staticmethod
    def test_two_opt_neighborhood(route):
        """
        Intorno 2-opt
        :return:
        """

        # TODO Ho bisogno dell'1 al fondo
        route = [1, 2, 3, 4, 5, 6, 1]
        print(route)

        for i in range(0, len(route)):
            for j in range(i + 2, len(route) - 1):
                print((route[i], route[i + 1]), (route[j], route[j + 1]))

                # Percorso da invertire
                reverse = route[i + 1:j + 1]
                # print reverse

                # Con ::-1 inverto la lista
                print (route[:i + 1] + reverse[::-1] + route[j + 1:])

    @staticmethod
    def test_three_opt_neighborhood(route):
        """
        Intorno 3-opt
        :return:
        """

        # TODO Ho bisogno dell'1 al fondo
        route = [1, 2, 3, 4, 5, 6, 1]
        print(route)

        for i in range(0, len(route)):
            for j in range(i + 2, len(route) - 1):
                for k in range(j + 2, len(route) - 1):
                    print (route[i], route[i + 1]), (route[j], route[j + 1]), (route[k], route[k + 1])

                    # print "Test: ", route[:i+1]
                    # print "Test: ", route[j+1:k+1]
                    # print "Test: ", route[i+2:j+1]
                    # print "Test: ", route[k+1:]

                    """
                    CASO 4 
                    """
                    reverse_path_1 = route[i + 1:j + 1]
                    reverse_path_2 = route[j + 1:k + 1]
                    print route[:i + 1] + reverse_path_1[::-1] + reverse_path_2[::-1] + route[k + 1:]

                    """
                    CASO 5
                    """
                    reverse = route[j + 1:k + 1]
                    print route[:i + 1] + reverse[::-1] + route[i + 1:j + 1] + route[k + 1:]

                    """
                    CASO 6 
                    """
                    reverse_path_1 = route[i + 1:j + 1]
                    print route[:i + 1] + route[j + 1:k + 1] + reverse_path_1[::-1] + route[k + 1:]

                    """
                    CASO 7 
                    """
                    print route[:i + 1] + route[j + 1:k + 1] + route[i + 1:j + 1] + route[k + 1:]

    @staticmethod
    def initial_solution(matrix):
        """
        Soluzione iniziale di tipo: Nearest Neighbor
        :param matrix:
        :return:
        """
        # Funzione obiettivo
        solution = 0

        # Nodo di partenza
        start_node = 0

        # Il current node viene inizializzato al nodo di partenza
        current_node = start_node

        # Ciclo hamiltoniamo (cammino)
        visited_node = []

        # Per ogni nodo
        for idx in range(len(matrix)):

            # Prelevo la riga contenente le distanze del nodo che sto valutando
            row = matrix[current_node]

            # Metto ad infinito le colonne relative ai nodi gia visitati in modo che non possano essere piu considerati
            for v_node in visited_node:
                row[v_node] = sys.maxsize

            # Se sto visitando l'ultimo nodo
            if len(matrix) - 1 == len(visited_node):
                solution += matrix[start_node][current_node]
                visited_node.append(current_node)  # Aggiungo l'ultimo nodo
                # visited_node.append(start_node)  # Aggiungo lo start node, creando il ciclo
            else:
                # Prelevo il valore piu piccolo della riga
                min_value = min(row)

                # Prelevo il numero del nodo che fa riferimento al nodo con distanza piu piccola
                # min_index = matrix[current_node].index(min_value)
                min_index = np.where(matrix[current_node] == min_value)[0][0]

                solution += min_value

                # Aggiungo il nodo appena trattato alla lista dei nodi visitati
                visited_node.append(current_node)
                current_node = min_index

        # print(solution)
        # print(visited_node)

        return visited_node


if __name__ == '__main__':
    start = time.time()
    Tsp()
    print('-' * 50)
    print('Execution time:', round(time.time() - start, 3), 'seconds')
