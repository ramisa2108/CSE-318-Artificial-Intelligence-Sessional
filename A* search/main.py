import numpy as np
from SearchNode import Node
from AStarSearch import AStarSearch

if __name__ == '__main__':

    with open('input.txt', 'r') as file:
        # k = number of rows
        k = int(file.readline().strip())
        n = k * k - 1

        initial_board = np.empty((k, k), dtype=int)
        for i in range(k):
            row = file.readline().strip()
            row = row.replace("*", str(k*k))
            initial_board[i] = [int(x) for x in row.split()]
            i += 1

        final_board = np.arange(1, k*k + 1).reshape((k, k))
        a_star = AStarSearch(k, initial_board, final_board)
        if not a_star.check_solvability():
            print("Not solvable.")
        else:
            for heuristic in ['linear conflict', 'manhattan distance', 'hamming distance']:
                a_star.set_heuristic(heuristic)
                print(heuristic, ':')
                print('-------------------------------\n')
                a_star.solve()



