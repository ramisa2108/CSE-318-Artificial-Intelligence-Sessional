from Node import Node
import copy
import time
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
		self.order = list(range(1, self.number_of_bins+1))
		random.shuffle(self.order)

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

	def heuristic_1(self, boards, node):
		return boards[0][0] - boards[1][0]

	def heuristic_2(self, boards, node):
		return 10 * self.heuristic_1(boards, node) + 5 * (sum(boards[0][1:]) - sum(boards[1][1:]))

	def heuristic_3(self, boards, node):
		return self.heuristic_2(boards, node) + 2 * node.free_rounds

	def heuristic_4(self, boards, node):
		return self.heuristic_1(boards, node) + 2 * node.captured

	def heuristic_5(self, boards, node):
		half_stones = (self.number_of_stones * self.number_of_bins) // 2
		return 5 * (boards[0][0] - half_stones) - 3 * (boards[1][0] - half_stones)

	def heuristic_6(self, boards, node):

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
				special_state = 1
				break

		# check free move
		if special_state == 0 and current_bin == 0:
			special_state = 2

		own_new_board, opponent_new_board = boards[0], boards[1]
		return own_new_board, opponent_new_board, special_state, captured

	def choose_best_move(self):

		st = time.time()
		root_node = Node()

		self.build_game_tree(root_node, [copy.deepcopy(self.board), copy.deepcopy(self.opponent.board)])
		print("Best move for ", self.player_name, ":", root_node.best_child.chosen_bin, ", possible score: ", root_node.best_val)
		en = time.time()
		print(en - st, "Seconds")
		return root_node.best_child.chosen_bin

	def build_game_tree(self, current_node, current_boards, current_level=0, alpha=float('-inf'), beta=float('inf')):

		if current_level < self.max_depth:

			for i in self.order:

				if current_level % 2 == 0:
					relative_board = copy.deepcopy(current_boards)
					b0, b1, special_state, captured = self.make_move(relative_board, i)
				else:
					relative_board = [copy.deepcopy(current_boards[1]), copy.deepcopy(current_boards[0])]
					b1, b0, special_state, captured = self.make_move(relative_board, i)

				if b0 is None:
					continue

				if special_state != 2:
					new_node = Node(i, current_node, 1-current_node.node_type)
				else:
					new_node = Node(i, current_node, current_node.node_type)

				if captured > 0 and new_node.node_type == 1:
					new_node.captured += captured

				if special_state == 0:  # normal game
					self.build_game_tree(new_node, copy.deepcopy([b0[:], b1[:]]), current_level+1, alpha, beta)
				elif special_state == 1:  # someone won
					new_node.best_val = self.heuristic_function([b0[:], b1[:]], new_node)

				else:  # free round
					if new_node.node_type == 1:
						new_node.free_rounds += 1
					self.build_game_tree(new_node, copy.deepcopy([b0[:], b1[:]]), current_level, alpha, beta)

				if current_level % 2 == 0:
					if current_node.best_val is None or new_node.best_val > current_node.best_val:
						current_node.best_val = new_node.best_val
						current_node.best_child = new_node

					if current_node.parent_node is not None:
						beta_val = current_node.get_prev_beta()
						if beta_val is not None and current_node.best_val >= beta_val:
							break

				else:
					if current_node.best_val is None or new_node.best_val < current_node.best_val:
						current_node.best_val = new_node.best_val
						current_node.best_child = new_node

					if current_node.parent_node is not None:
						alpha_val = current_node.get_prev_alpha()
						if alpha_val is not None and current_node.best_val <= alpha_val:
							break

		else:
			current_node.best_val = self.heuristic_function(current_boards, current_node)

