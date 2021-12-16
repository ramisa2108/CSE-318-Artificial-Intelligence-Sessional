from Mancala import Mancala
from Player import Player

if __name__ == '__main__':

	player1 = Player(6, 4, "Player1", True, 2, 5)
	player2 = Player(6, 4, "Player2", True, 2, 3)
	mancala = Mancala(player1, player2)
	mancala.game_loop()

