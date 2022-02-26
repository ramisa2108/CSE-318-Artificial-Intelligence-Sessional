class Node:

	def __init__(self, chosen_bin=None):

		self.best_child = None
		self.chosen_bin = chosen_bin
		self.children = []
