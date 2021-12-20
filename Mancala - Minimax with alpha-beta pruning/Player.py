from Node import Node
import copy
import random


class Player:

	def __init__(self, number_of_bins, number_of_stones, player_name, is_ai=False, heuristic=1, max_depth=5):
		self.number_of_bins = number_of_bins
		self.number_of_stones = number_of_stones
		self.board = [0] + [self.number_of_stones] * self.number_of_bins
		self.player_name = player_name
		self.is_ai = is_ai
		self.max_depth = max_depth
		self.opponent = None
		self.heuristic = heuristic
		self.heuristic_function = None
		self.get_heuristic_function()

	def get_heuristic_function(self):

		if self.heuristic == 1:
			self.heuristic_function = self.heuristic_1
		elif self.heuristic == 2:
			self.heuristic_function = self.heuristic_2
		elif self.heuristic == 3:
			self.heuristic_function = self.heuristic_3
		elif self.heuristic == 4:
			self.heuristic_function = self.heuristic_4
		elif self.heuristic == 5:
			self.heuristic_function = self.heuristic_5
		else:
			self.heuristic_function = self.heuristic_6

	# number of stones in storage
	def heuristic_1(self, boards, free_rounds=0, captured=0):
		return boards[0][0] - boards[1][0]

	# number of stones in storage and in the bins
	def heuristic_2(self, boards,  free_rounds=0, captured=0):
		return (2 * self.heuristic_1(boards) + 1 * (sum(boards[0][1:]) - sum(boards[1][1:]))) / 3

	# number of stones in storage and the bins and the number of free rounds earned for this move
	def heuristic_3(self, boards,  free_rounds=0, captured=0):
		return (3 * self.heuristic_2(boards) + 2 * free_rounds) / 5

	# number of stones in storage and total stones captured for this move
	def heuristic_4(self, boards,  free_rounds=0, captured=0):
		return (3 * self.heuristic_1(boards) + 2 * captured) / 5

	# how close the players' storage is to being half full
	def heuristic_5(self, boards,  free_rounds=0, captured=0):
		half_stones = (self.number_of_stones * self.number_of_bins) // 2
		return 1.5 * (boards[0][0] - half_stones) - 0.5 * (boards[1][0] - half_stones)

	# how close the stones are to the player's storage
	def heuristic_6(self, boards,  free_rounds=0, captured=0):

		close_to_my_storage = boards[0][0]
		for i in range(1, self.number_of_bins+1):
			stones = boards[0][i]
			close_to_my_storage += min(stones, i)
			for j in range(i+7, i+47, 13):
				if stones >= j:
					close_to_my_storage += min(stones, j+6) - (j-1)
		return close_to_my_storage

	def set_opponent(self, opponent):
		self.opponent = opponent

	def update_board(self, new_board):
		self.board = new_board

	def get_bin_choice(self):
		if self.is_ai:
			chosen_bin = self.choose_best_move()
		else:
			chosen_bin = int(input("Enter bin number: "))
		return chosen_bin

	def make_move(self, current_board, chosen_bin=None):

		stones = current_board[0][chosen_bin]
		if chosen_bin == 0 or stones == 0:
			return None, None, None, None

		row = 0
		current_bin = chosen_bin
		boards = copy.deepcopy(current_board)
		boards[0][chosen_bin] = 0

		while stones > 0:
			current_bin -= 1
			if row == 0 and current_bin < 0:
				row = 1
				current_bin = self.number_of_bins
			elif row == 1 and current_bin == 0:
				row = 0
				current_bin = self.number_of_bins

			boards[row][current_bin] += 1
			stones -= 1

		special_state = 0
		captured = 0
		opposite_position = self.number_of_bins+1-current_bin

		# check capturing move
		if row == 0 and current_bin != 0 and boards[0][current_bin] == 1 and boards[1][opposite_position] != 0:
			captured = boards[1][opposite_position]
			boards[0][0] += (boards[0][current_bin] + boards[1][opposite_position])
			boards[0][current_bin] = 0
			boards[1][opposite_position] = 0

		# check game over
		for i in range(2):
			if sum(boards[i][1:]) == 0:
				boards[1-i] = [sum(boards[1-i])] + [0] * self.number_of_bins
				if boards[0][0] > boards[1][0]:
					special_state = 1
				elif boards[0][0] < boards[1][0]:
					special_state = -1
				elif i == 0:
					special_state = -1
				else:
					special_state = 1
				break

		# check free move
		if special_state == 0 and current_bin == 0:
			special_state = 2

		own_new_board, opponent_new_board = boards[0], boards[1]
		return own_new_board, opponent_new_board, special_state, captured

	def choose_best_move(self):

		root_node = Node()
		val = self.max_player_tree(root_node, [copy.deepcopy(self.board), copy.deepcopy(self.opponent.board)], 0, float('-inf'), float('inf'))
		print("Best move for ", self.player_name, ":", root_node.best_child.chosen_bin, ", possible score: ", val)
		return root_node.best_child.chosen_bin

	def max_player_tree(
			self, current_node, current_boards, current_level, alpha, beta,
			current_free_rounds=0, current_captured=0
	):

		val = float('-inf')
		order = list(range(1, self.number_of_bins + 1))
		random.shuffle(order)

		if current_level < self.max_depth:

			for i in order:
				relative_board = copy.deepcopy(current_boards)
				b0, b1, special_state, captured = self.make_move(relative_board, i)

				if b0 is None:
					continue

				if special_state == 2:
					new_node = Node(i)
					current_free_rounds += 1
					v = self.max_player_tree(
						new_node, copy.deepcopy([b0[:], b1[:]]), current_level,
						alpha, beta, current_free_rounds, current_captured
					)

				elif special_state == 0:
					new_node = Node(i)
					current_captured += captured
					v = self.min_player_tree(
						new_node, copy.deepcopy([b0[:], b1[:]]), current_level + 1, alpha, beta,
						current_free_rounds, current_captured
					)

				else:
					new_node = Node(i)
					current_captured += captured
					v = self.heuristic_function([b0[:], b1[:]], current_free_rounds, current_captured)

				current_node.children.append(new_node)

				if v > val:
					val = v
					current_node.best_child = new_node

				if val >= beta:
					return val
				alpha = max(alpha, val)
		else:
			val = self.heuristic_function(current_boards, current_free_rounds, current_captured)
		return val

	def min_player_tree(
			self, current_node, current_boards, current_level, alpha, beta,
			current_free_rounds=0, current_captured=0
	):

		val = float('inf')
		order = list(range(1, self.number_of_bins + 1))
		random.shuffle(order)

		if current_level < self.max_depth:

			for i in order:
				relative_board = [copy.deepcopy(current_boards[1]), copy.deepcopy(current_boards[0])]
				b1, b0, special_state, captured = self.make_move(relative_board, i)

				if b0 is None:
					continue

				if special_state == 2:
					new_node = Node(i)
					v = self.min_player_tree(
						new_node, copy.deepcopy([b0[:], b1[:]]), current_level, alpha, beta,
						current_free_rounds, current_captured
					)

				elif special_state == 0:
					new_node = Node(i)
					v = self.max_player_tree(
						new_node, copy.deepcopy([b0[:], b1[:]]), current_level + 1, alpha, beta,
						current_free_rounds, current_captured
					)

				else:
					new_node = Node(i)
					v = self.heuristic_function([b0[:], b1[:]], current_free_rounds, current_captured)

				current_node.children.append(new_node)

				if v < val:
					val = v
					current_node.best_child = new_node
				if val <= alpha:
					return val
				beta = min(beta, val)
		else:
			val = self.heuristic_function(current_boards, current_free_rounds, current_captured)
		return val

