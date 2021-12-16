from Mancala import Mancala
from Player import Player

if __name__ == '__main__':

	print("Choose game:\n1. Human vs. Human\n2. Human vs. Computer\n3. Computer vs. Computer")
	choice = int(input("Enter choice: "))
	if choice == 3:
		player1 = Player(6, 4, "Player1", True, 1, 8)
	else:
		player_name = input("Enter player 1's name: ")
		player1 = Player(6, 4, player_name, False)

	if choice == 1:
		player_name = input("Enter player 2's name: ")
		player2 = Player(6, 4, player_name, False)
	else:
		player2 = Player(6, 4, "Player2", True, 1, 8)
	mancala = Mancala(player1, player2)
	mancala.game_loop()


def hundred_games():
	return




