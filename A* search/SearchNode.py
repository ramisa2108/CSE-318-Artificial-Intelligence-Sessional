import numpy as np
import copy


class Node:

	def __init__(self, k, current_board, moves_made, assumed_distance, previous_node=None):
		self.k = k
		self.current_board = current_board
		self.moves_made = moves_made
		self.total_distance = moves_made + assumed_distance
		self.previous_node = copy.deepcopy(previous_node)
		self.blank_position = (np.where(current_board == self.k * self.k))
		self.blank_position = (self.blank_position[0][0], self.blank_position[1][0])

	def __lt__(self, other):
		return (self.total_distance < other.total_distance) \
		        or ((self.total_distance == other.total_distance) and (self.moves_made <= other.moves_made))

	def get_neighbours(self):
		# up neighbour
		blank_row = self.blank_position[0]
		blank_col = self.blank_position[1]
		neighbours = []

		if blank_row > 0:
			neighbour = self.switch_positions(blank_row, blank_col, blank_row - 1, blank_col)
			if self.previous_node is None or not (neighbour == self.previous_node.current_board).all():
				neighbours.append(neighbour)

		if blank_row < (self.k-1):
			neighbour = self.switch_positions(blank_row, blank_col, blank_row + 1, blank_col)
			if self.previous_node is None or not (neighbour == self.previous_node.current_board).all():
				neighbours.append(neighbour)

		if blank_col > 0:
			neighbour = self.switch_positions(blank_row, blank_col, blank_row, blank_col - 1)
			if self.previous_node is None or not (neighbour == self.previous_node.current_board).all():
				neighbours.append(neighbour)

		if blank_col < (self.k - 1):
			neighbour = self.switch_positions(blank_row, blank_col, blank_row, blank_col + 1)
			if self.previous_node is None or not (neighbour == self.previous_node.current_board).all():
				neighbours.append(neighbour)

		return neighbours

	def switch_positions(self, row1, col1, row2, col2):
		neighbour = copy.deepcopy(self.current_board)
		neighbour[row1, col1], neighbour[row2, col2] = neighbour[row2, col2], neighbour[row1, col1]
		return neighbour

	def print_board(self):
		for i in range(self.k):
			row = " ".join(str(x) for x in self.current_board[i])
			row = row.replace(str(self.k*self.k), "*")
			print(row)
		print('\n')


