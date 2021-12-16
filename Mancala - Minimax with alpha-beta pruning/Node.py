class Node:

	def __init__(self, chosen_bin=None, parent_node=None, node_type=1):

		self.parent_node = parent_node
		self.best_child = None
		self.chosen_bin = chosen_bin
		self.node_type = node_type
		self.free_rounds = 0
		self.captured = 0
		if node_type == 1:
			self.best_val = self.get_prev_alpha()
		else:
			self.best_val = self.get_prev_beta()

		if parent_node is not None:
			self.free_rounds = parent_node.free_rounds
			self.captured = parent_node.captured
			
	def get_prev_beta(self):
		if self.parent_node is None:
			return None
		elif self.parent_node.node_type == 0:
			return self.parent_node.best_val
		else:
			return self.parent_node.get_prev_beta()

	def get_prev_alpha(self):
		if self.parent_node is None:
			return None
		elif self.parent_node.node_type == 1:
			return self.parent_node.best_val
		else:
			return self.parent_node.get_prev_alpha()




