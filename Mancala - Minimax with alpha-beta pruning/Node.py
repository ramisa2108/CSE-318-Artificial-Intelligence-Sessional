class Node:

	def __init__(self, chosen_bin=None, parent_node=None, node_type="MAX"):

		self.children = []
		self.parent_node = parent_node
		self.best_child = None
		self.chosen_bin = chosen_bin
		self.best_val = None
		self.node_type = node_type

	def get_alpha(self):
		if self.node_type == "MAX":
			return self.best_val
		else:
			return None

	def get_beta(self):
		if self.node_type == "MIN":
			return self.best_val
		else:
			return None

