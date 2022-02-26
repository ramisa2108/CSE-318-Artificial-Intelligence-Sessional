import time


class Mancala:

	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.player1.set_opponent(self.player2)
		self.player2.set_opponent(self.player1)
		self.round = 0

	def game_loop(self):
		start_time = time.time()
		self.print_game()
		while True:

			if self.round % 2 == 0:
				game_state = self.make_move(self.player1, self.player2)
			else:
				game_state = self.make_move(self.player2, self.player1)

			if game_state is None:   # invalid move
				print("Invalid Move.")
				continue

			self.print_game()
			if (game_state == 1 and self.round % 2 == 0) or (game_state == -1 and self.round % 2 == 1):  # player1 won
				print(self.player1.player_name, "Won!")
				res = 1
				break

			elif (game_state == -1 and self.round % 2 == 0) or (game_state == 1 and self.round % 2 == 1):  # player2 won
				print(self.player2.player_name, "Won!")
				res = 2
				break
			elif game_state == 0:  # normal game
				self.round += 1
			elif game_state == 2:  # free round for current player
				print("Free Round.")

		end_time = time.time()
		print("Total time taken =", end_time - start_time)
		return res

	def make_move(self, current_player, opponent_player):

		print(current_player.player_name + "'s move.")

		chosen_bin = current_player.get_bin_choice()

		current_player_board, opponent_player_board, special_state, _ = \
			current_player.make_move([current_player.board, opponent_player.board], chosen_bin)

		if current_player_board is None:
			return None

		current_player.update_board(current_player_board)
		opponent_player.update_board(opponent_player_board)

		return special_state

	def print_game(self):

		# bin numbers
		print('Player 2:', end='')
		for i in range(1, self.player1.number_of_bins + 1):
			print('\t', "(" + str(i) + ")", end=' \t')
		print("\n")

		# player 2 bins
		print('\t', " ", end=' \t|')
		for x in self.player2.board[1:]:
			print('\t', x, end=' \t\t|')
		print(' \t\t', " ", end=' \t')
		print("\n")

		# storages for the players
		print(" ", self.player2.board[0], end=' \t')
		for i in range(self.player2.number_of_bins):
			print(' \t', " ", end=' \t\t')
		print('\t', self.player1.board[0], end=' \t')
		print("\n")

		# player1 bins
		print('\t', " ", end=' \t|')
		for x in self.player1.board[::-1][:-1]:
			print('\t', x, end=' \t\t|')
		print(' \t\t', " ", end=' \t')
		print("\n")

		# player1 bin numbers
		print("Player 1:", end='')
		for i in range(self.player1.number_of_bins, 0, -1):
			print('\t', "("+str(i)+")", end=' \t')
		print("\n")






