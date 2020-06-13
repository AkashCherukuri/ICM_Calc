from collections import defaultdict
import copy
import itertools   

class ICM_Calc:
	def __init__(self):
		self.score = defaultdict(int)
		self.prob = defaultdict(int)
		self.Rew = []
		self.num_players = 0

	def init(self):
		self.num_players = int(input(f"Enter the number of Players: "))
		for i in range(self.num_players):
			self.score[i+1] = int(input(f"Chip count of Player{i+1}: "))

		print(f"\nEnter the Prize pool and press x when done.")
		for i in range(self.num_players):
			reward = input(f"Prize for position{i+1}: ")
			if reward == 'x' or reward == 'X':
				break
			else:
				self.Rew.append(int(reward))
		print()
			
	def Prob_First(self, player, player_list):
		total = 0.0
		for i in player_list:
			total = total + self.score[i]
		prob = (self.score[player]/total)
		return prob

	def Prob_Set(self):
		#Calculating 1st pos Probabilities for all players
		for player in range(1, self.num_players+1, 1):
			self.prob[player, 1] = self.Prob_First(player, range(1, self.num_players+1, 1))

		#Calculating rest except last probabilities
		pl_list = list(range(1, self.num_players+1, 1))
		for player in pl_list:
			temp_list = copy.deepcopy(pl_list)
			temp_list.remove(player)
			for position in range(2, self.num_players, 1):
				todo = list(itertools.permutations(temp_list, position-1))
				prob = 0
				for List in todo:
					t_list = copy.deepcopy(pl_list)
					for i in List:
						if List[0] == i:
							case_prob = self.prob[i, 1]
						else:
							case_prob = case_prob * self.Prob_First(i, t_list)
						t_list.remove(i)
					case_prob = case_prob * self.Prob_First(player, t_list)
					prob += case_prob
				self.prob[player, position] = prob

		#Calculating Last Probabilities
		for player in pl_list:
			total = 0
			for position in range(1, self.num_players, 1):
				total = total + self.prob[player, position]
			self.prob[player, self.num_players] = 1 - total

	def Expected_Prize(self):
		self.init()
		self.Prob_Set()
		for player in range(1, self.num_players+1, 1):
			Exp = 0
			for position in range(len(self.Rew)):
				Exp = Exp + self.prob[player, position+1]*self.Rew[position]
			print(f"Expected Reward for Player{player} is {Exp}")

new = ICM_Calc()
new.Expected_Prize()