
import random

import numpy as np


num_matches = 3
num_weights = 3
for i in range(2 * num_matches):
	word = ""
	for j in range(num_weights):
		word += str(random.random()) + " "
	print(word[:len(word) - 1])
