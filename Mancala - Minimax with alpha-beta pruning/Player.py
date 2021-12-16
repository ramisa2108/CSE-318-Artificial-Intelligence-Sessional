from Node import Node
import copy


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

	def heuristic_1(self, boards):
		return boards[0][0] - boards[1][0]

	def heuristic_2(self, boards):
		return 10 * self.heuristic_1(boards) + 5 * (sum(boards[0][1:]) - sum(boards[1][1:]))

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
			return None, None, None

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
		# check stealing move
		if row == 0 and current_bin != 0 and boards[0][current_bin] == 1 \
				and boards[1][self.number_of_bins+1-current_bin] != 0:
			boards[0][0] += (boards[0][current_bin] + boards[1][self.number_of_bins+1-current_bin])
			boards[0][current_bin] = 0
			boards[1][self.number_of_bins+1-current_bin] = 0

		# check game over
		for i in range(2):
			if sum(boards[i][1:]) == 0:
				boards[1-i] = [boards[1-i][0] + sum(boards[1-i][1:])] + [0] * self.number_of_bins
				special_state = 1
				break

		# check free move
		if special_state == 0 and current_bin == 0:
			special_state = 2

		own_new_board, opponent_new_board = boards[0], boards[1]
		return own_new_board, opponent_new_board, special_state

	def choose_best_move(self):
		root_node = Node()

		self.build_game_tree(root_node, [copy.deepcopy(self.board), copy.deepcopy(self.opponent.board)])
		print("Best move for ", self.player_name, ":", root_node.best_child.chosen_bin, ", possible score: ", root_node.best_val)
		return root_node.best_child.chosen_bin

	def build_game_tree(self, current_node, current_boards, current_level=0):

		current_node.children = []
		if current_level < self.max_depth:

			for i in range(1, self.number_of_bins + 1):

				if current_level % 2 == 0:
					relative_board = copy.deepcopy(current_boards)
					b0, b1, special_state = self.make_move(relative_board, i)
				else:
					relative_board = [copy.deepcopy(current_boards[1]), copy.deepcopy(current_boards[0])]
					b1, b0, special_state = self.make_move(relative_board, i)

				if b0 is None:
					continue

				# print("in level: ", current_level)
				# print(current_boards[1])
				# print(current_boards[0][::-1])
				# print("--> ", i)
				# print(b1)
				# print(b0[::-1])
				if current_node.node_type == "MIN":
					new_node = Node(i, current_node, "MAX")
				else:
					new_node = Node(i, current_node, "MIN")

				if special_state == 0:
					self.build_game_tree(new_node, copy.deepcopy([b0[:], b1[:]]), current_level+1)
				elif special_state == 1:
					new_node.best_val = self.heuristic_function([b0[:], b1[:]])
				else:
					new_node.node_type = current_node.node_type
					self.build_game_tree(new_node, copy.deepcopy([b0[:], b1[:]]), current_level)

				if current_level % 2 == 0:
					if current_node.best_val is None or new_node.best_val > current_node.best_val:
						current_node.best_val = new_node.best_val
						current_node.best_child = new_node

					# if current_node.parent_node is not None:
					# 	beta_val = current_node.parent_node.get_beta()
					# 	if beta_val is not None and current_node.best_val > beta_val:
					# 		break

				else:
					if current_node.best_val is None or new_node.best_val < current_node.best_val:
						current_node.best_val = new_node.best_val
						current_node.best_child = new_node

					# if current_node.parent_node is not None:
					# 	alpha_val = current_node.parent_node.get_alpha()
					# 	if alpha_val is not None and current_node.best_val < alpha_val:
					# 		break
				current_node.children.append(new_node)

		else:
			current_node.best_val = self.heuristic_function(current_boards)
			# print("Leaf max level:")
			# self.print_rec(copy.deepcopy(current_node))
			# print()
			# print(current_boards, "heuristic val =", current_node.best_val)

	def print_rec(self, current_node):
		if current_node.parent_node is not None:
			self.print_rec(copy.deepcopy(current_node.parent_node))
		print(current_node.chosen_bin, end=" --> ")













