import numpy as np
from SearchNode import Node
import time
from queue import PriorityQueue


class AStarSearch:

	def __init__(self, k, initial_board, final_board, heuristic='manhattan'):
		self.k = k
		self.n = k * k - 1
		self.initial_board = initial_board
		self.final_board = final_board
		self.final_positions = self.get_positions(final_board)
		self.heuristic = heuristic
		self.heuristic_function = None
		self.set_heuristic_function()

	def set_heuristic(self, heuristic):
		self.heuristic = heuristic
		self.set_heuristic_function()

	def set_heuristic_function(self):
		if self.heuristic == 'manhattan distance':
			self.heuristic_function = self.get_manhattan_distance
		elif self.heuristic == 'hamming distance':
			self.heuristic_function = self.get_hamming_distance
		elif self.heuristic == 'linear conflict':
			self.heuristic_function = self.get_linear_conflict
		else:
			self.heuristic_function = None

	def check_solvability(self):

		positions = self.get_positions(self.initial_board)
		inversions = 0

		for i in range(self.n):
			for j in range(i):
				if positions[i][0] < positions[j][0]:
					inversions += 1
				elif (positions[i][0] == positions[j][0]) and (positions[i][1] < positions[j][1]):
					inversions += 1

		if self.k % 2 == 1:
			return inversions % 2 == 0
		else:
			blank_position = np.where(self.initial_board == (self.n + 1))
			row_of_blank = blank_position[0][0]

			return (row_of_blank % 2) != (inversions % 2)

	def get_positions(self, board):
		positions = np.empty(self.n, dtype=tuple)
		for i in range(1, self.n + 1):
			pos = (np.where(board == i))  # returns a tuple of arrays
			positions[i - 1] = (pos[0][0], pos[1][0])  # extract the first elements from the arrays in pos
		return positions

	def get_hamming_distance(self, current_board):

		current_positions = self.get_positions(current_board)
		distance = 0
		for i in range(self.n):
			distance += (current_positions[i] != self.final_positions[i])

		return distance

	def get_manhattan_distance(self, current_board):

		current_position = self.get_positions(current_board)
		distance = 0

		for i in range(self.n):
			distance += abs(current_position[i][0] - self.final_positions[i][0]) + \
			            abs(current_position[i][1] - self.final_positions[i][1])

		return distance
	
	def get_linear_conflict(self, current_board):

		current_positions = self.get_positions(current_board)

		row_matched_positions = [[] for i in range(self.k)]
		for i in range(0, self.n):
			if current_positions[i][0] == self.final_positions[i][0]:
				row = current_positions[i][0]
				row_matched_positions[row].append((current_positions[i][1], self.final_positions[i][1]))
				# row_matched_positions[row].append(i)

		linear_conflicts = 0
		for i in range(self.k):
			for x in row_matched_positions[i]:
				for y in row_matched_positions[i]:
					if (x[0] < y[0]) and (x[1] > y[1]):
						linear_conflicts += 1
					# if x > y:
					# 	linear_conflicts += 1

		return self.get_manhattan_distance(current_board) + 2 * linear_conflicts

	def solve(self):

		start_time = time.time()
		pq = PriorityQueue()
		initial_node = Node(self.k, self.initial_board, 0, self.heuristic_function(self.initial_board))
		pq.put(initial_node)

		close_list = set()

		current_node = initial_node

		while not pq.empty():
			current_node = pq.get()

			if (current_node.current_board == self.final_board).all():
				break

			if map(tuple, current_node.current_board) in close_list:
				continue
			close_list.add(map(tuple, current_node.current_board))  # making it hashable for insertion in set

			neighbours = current_node.get_neighbours()
			for neighbour in neighbours:
				if map(tuple, neighbour) in close_list:
					continue
				new_node = Node(self.k, neighbour, current_node.moves_made + 1, self.heuristic_function(neighbour),
				                current_node)
				pq.put(new_node)

		distance = current_node.moves_made
		expanded = len(close_list)
		explored_set = close_list

		while not pq.empty():
			node = pq.get()
			explored_set.add(node)
		explored = len(explored_set) + 1
		end_time = time.time()

		print("Board states:")
		self.print_solution(current_node)

		print("Optimal distance =", distance)
		print("Expanded nodes =", expanded)
		print("Explored nodes =", explored)
		print("TIme taken: ", end_time - start_time)
		print()

	def print_solution(self, current_node):
		previous_node = current_node.previous_node
		if previous_node is not None:
			self.print_solution(previous_node)

		current_node.print_board()
