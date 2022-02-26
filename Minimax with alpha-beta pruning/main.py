from Mancala import Mancala
from Player import Player
import random
import pandas as pd


def play_hundred_games():

	all_data = []
	for h1 in range(4, 7):
		for h2 in range(1, 7):
			p1_wins = 0
			p2_wins = 0
			print("Heuristic ", h1, "Heuristic", h2)
			for i in range(100):
				d1 = random.randint(1, 5)
				d2 = d1
				print("Game no.", i+1)
				print("Players 1 playing with depth ", d1)
				print("Player 2 playing with depth", d2)

				player1 = Player(6, 4, "Player1", True, h1, d1)
				player2 = Player(6, 4, "Player2", True, h2, d2)
				mancala = Mancala(player1, player2)
				winner = mancala.game_loop()
				if winner == 1:
					p1_wins += 1
				else:
					p2_wins += 1
			all_data.append(
				{
					"Player1 Heuristic": "H"+str(h1),
					"Player2 Heuristic": "H"+str(h2),
					"Player1 wins": p1_wins,
					"Player2 wins": p2_wins
				}
			)
	results = pd.DataFrame(all_data)
	results.to_csv("./temp.csv", index=False)
	return


if __name__ == '__main__':

	print("Choose game:\n1. Human vs. Human\n2. Human vs. Computer\n3. Computer vs. Computer\n4. Play 100 games\n")
	choice = int(input("Enter choice: "))

	if choice == 4:
		play_hundred_games()
		exit()
	if choice == 3:
		heuristic1 = int(input("Enter heuristic number for player 1: "))
		depth1 = int(input("Enter max depth for player 1: "))
		player1 = Player(6, 4, "Player1", True, heuristic1, depth1)
	else:
		player_name = input("Enter player 1's name: ")
		player1 = Player(6, 4, player_name, False)

	if choice == 1:
		player_name = input("Enter player 2's name: ")
		player2 = Player(6, 4, player_name, False)
	else:
		heuristic2 = int(input("Enter heuristic number for player 2: "))
		depth2 = int(input("Enter max depth for player 2: "))
		player2 = Player(6, 4, "Player2", True, heuristic2, depth2)
	mancala = Mancala(player1, player2)
	mancala.game_loop()





