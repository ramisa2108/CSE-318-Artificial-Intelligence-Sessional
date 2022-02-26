import numpy as np

class HMM:
	def __init__(self, rows, cols, obstacles, grid):
		self.rows = rows
		self.cols = cols
		self.grid = grid
		self.obstacles = obstacles
		self.prob_matrix = self.calc_init_probabilities()
		self.time_step = 0
		self.sensor_correct_probability = 0.85
		self.cumulative_adjacent_probability = 0.9
		self.move_adj_prob = np.zeros((rows, cols))
		self.move_corner_or_stay_prob = np.zeros((rows, cols))
		self.calc_moving_probabilities()
		self.print_grid()
		self.print_probability()

	def calc_init_probabilities(self):
		init_prob = 1.0 / (self.rows * self.cols - self.obstacles)
		prob_matrix = init_prob * (1 - self.grid)
		return prob_matrix

	def calc_moving_probabilities(self):

		for i in range(self.rows):
			for j in range(self.cols):
				adjacents = self.get_adjacent_count(i, j)
				corners = self.get_corner_count(i, j)

				if adjacents:
					self.move_adj_prob[i][j] = self.cumulative_adjacent_probability / adjacents
					self.move_corner_or_stay_prob[i][j] = (1.0 - self.cumulative_adjacent_probability) / (corners + 1)

				else:
					self.move_adj_prob[i][j] = 0.0
					self.move_corner_or_stay_prob[i][j] = 1.0 / (corners + 1)

	def print_probability(self):
		print("Time step:", self.time_step)
		for i in range(self.rows):
			for j in range(self.cols):
				print("{:.4f}".format(self.prob_matrix[i][j] * 100), end=" ")
			print()

		print("Sanity check sum = {:.2f}".format(np.sum(self.prob_matrix) * 100))
		print("-----------------------------------------------------\n")

	def print_grid(self):
		print("Grid layout:")
		for i in range(self.rows):
			for j in range(self.cols):
				print(self.grid[i][j], end="\t")
			print()

	def get_max_probability(self):
		max_r, max_c = np.unravel_index(self.prob_matrix.argmax(), self.prob_matrix.shape)
		return max_r, max_c

	def calc_probability(self, ei, ej, et):

		self.time_step += 1
		temp = np.zeros((n, m), dtype=float)

		for i in range(self.rows):
			for j in range(self.cols):
				if grid[i][j] == 1:
					temp[i][j] = 0.0
				else:
					p_et_xt = self.p_et_xt(ei, ej, i, j, et)
					sum = 0.0
					for ii in range(self.rows):
						for jj in range(self.cols):
							if self.is_adjacent(i, j, ii, jj):
								p_xx = self.move_adj_prob[ii][jj]
							elif self.is_corner(i, j, ii, jj) or (i, j) == (ii, jj):
								p_xx = self.move_corner_or_stay_prob[ii][jj]
							else:
								p_xx = 0.0
							p_xx *= self.prob_matrix[ii][jj]
							sum += p_xx
					temp[i][j] = p_et_xt * sum

		total = np.sum(temp)
		for i in range(self.rows):
			for j in range(self.cols):
				self.prob_matrix[i][j] = temp[i][j] / total

	def get_adjacent_count(self, r, c):
		adjacent = 0
		if r > 0 and self.grid[r-1][c] == 0:
			adjacent += 1
		if r < self.rows-1 and self.grid[r+1][c] == 0:
			adjacent += 1
		if c > 0 and self.grid[r][c-1] == 0:
			adjacent += 1
		if c < self.cols-1 and grid[r][c+1] == 0:
			adjacent += 1
		return adjacent

	def get_corner_count(self, r, c):
		corners = 0
		if r > 0 and c > 0 and self.grid[r-1][c-1] == 0:
			corners += 1
		if r > 0 and c < self.cols-1 and self.grid[r-1][c+1] == 0:
			corners += 1
		if r < self.rows-1 and c > 0 and self.grid[r+1][c-1] == 0:
			corners += 1
		if r < self.rows-1 and c < self.cols-1 and self.grid[r+1][c+1] == 0:
			corners += 1
		return corners

	def is_adjacent(self, r1, c1, r2: int, c2: int):
		return (abs(r1 - r2) + abs(c1 - c2)) == 1

	def is_corner(self, r1, c1, r2, c2):
		return abs(r1-r2) == 1 and abs(c1-c2) == 1

	def p_et_xt(self, ei, ej, xi, xj, et):

		if ((ei, ej) == (xi, xj)) or self.is_adjacent(ei, ej, xi, xj) or self.is_corner(ei, ej, xi, xj):
			if et == 0:
				return 1-self.sensor_correct_probability
			else:
				return self.sensor_correct_probability
		else:
			if et == 0:
				return self.sensor_correct_probability
			else:
				return 1-self.sensor_correct_probability


if __name__ == '__main__':

	with open("input.txt", "r") as file:
		n, m, k = [int(x) for x in file.readline().strip().split()]
		grid = np.zeros((n, m), dtype=int)

		for i in range(k):
			r, c = [int(x) for x in file.readline().strip().split()]
			grid[r][c] = 1

		hmm = HMM(n, m, k, grid)

		while True:
			line = file.readline().strip().split()
			if line[0] == 'Q':
				print("Bye Casper!")
				break
			elif line[0] == 'R':
				u, v, b = [int(x) for x in line[1:]]
				print("Sensor gives output", b, "at (", u, ",", v, ")")
				hmm.calc_probability(u, v, b)
				hmm.print_probability()
			else:
				r, c = hmm.get_max_probability()
				print("Max value at row = ", r, " col = ", c, '\n')

