#Werewolf
from engine import LoadImages, LoadImagesSheet
from unit.base_unit import BaseUnit
from animation import Animation
import unit
from ai import AI

class BaseEnemyUnit(BaseUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords):
		
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords)
		self.anim_standing = LoadImages(dirr, ["stand_frame0.png","stand_frame1.png", "stand_frame2.png"]).sequence
		self.anim_walking = LoadImages(dirr, []).sequence
		self.anim_warn1 = LoadImages(dirr, []).sequence 
		self.anim_atk1 = LoadImages(dirr, []).sequence
		self.anim_death = LoadImages(dirr, []).sequence	
		self.AI = AI(self,[])
		self.AI.sequence.append([self.Approach])
		self.AI.sequence.append([self.queue_warn1, self.queue_warn1, self.queue_attack1])
		self.AI.sequence.append([self.queue_warn1, self.queue_warn1, self.queue_attack1])

		#self.ai_Attack
		#self.ai_sequence0 = [self.move_right, self.move_right, self.move_right, self.queue_warn1, self.queue_warn1, self.queue_attack1]
		#self.ai_sequence1 = [self.move_left, self.move_left, self.move_left]

		#self.AI = AI(self, [self.ai_sequence0, self.ai_sequence1,self.ai_Approach])
	
	def draw_atk1(self, screen):
		#Stab
		rate = 1
		Animation(screen, self, 0, self.anim_atk1, rate).animate()
		#Animation(screen, self, self.width, self.stab_effect, rate).animate()
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"

	def draw_warn1(self, screen):
		#Stab 
		rate = 4
		Animation(screen, self, 0, self.anim_warn1, rate).animate()
		#Animation(screen, self, self.width, self.stab_effect, rate).animate()
		if self.anim_warn1[-2] == len(self.anim_warn1) - 3 and self.anim_warn1[-1] == rate-1:
			Animation(screen, self, 0, self.anim_warn1, 5).animate()
			self.anim_warn1[-2] = 0
			self.attack_status = "none"


	def draw_atk2(self, screen):
		#slash
		rate = 3
		Animation(screen, self, 0, self.anim_atk2, rate).animate()
		Animation(screen, self, self.width, self.slash_effect, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"

	def check_attack_1(self):
		unit_x,unit_y = self.get_position()
		player_ofa = self.AI.find_closest_player()
		pl_x, pl_y = player_ofa.get_position()
		pl_to_enm_right = player_ofa.width + (abs(pl_x-unit_x))
		pl_to_enm_left = (abs(pl_x-unit_x)) 
		pl_to_enm_top = player_ofa.height + (abs(pl_y-unit_y))
		pl_to_enm_bottom = (abs(pl_y-unit_y))

		x1_attk_rng = self.attacks_dict[one][x_range]
		y1_attk_rng = self.attacks_dict[one][y_range]
		offset = 0.5

		#Check if long attack in range:
		if (x1_attk_rng*offset <= pl_to_enm_right and unit_x >= pl_x):

			if y1_attk_rng*offset <= pl_to_enm_bottom and unit_y > pl_y:
				return True
			
			elif y1_attk_rng*offset <= pl_to_enm_top and unit_y < pl_y:
				return True

		elif (x1_attk_rng*offset <= pl_to_enm_left and unit_x <= pl_x):

			if y1_attk_rng*offset <= pl_to_enm_bottom and unit_y > pl_y:
				return True
			
			elif y1_attk_rng*offset <= pl_to_enm_top and unit_y < pl_y:
				return True

		return False

	def check_attack_2(self):

		unit_x,unit_y = self.get_position()
		player_ofa = self.AI.find_closest_player()
		pl_x, pl_y = player_ofa.get_position()
		pl_to_enm_right = player_ofa.width + (abs(pl_x-unit_x))
		pl_to_enm_left = (abs(pl_x-unit_x))
		pl_to_enm_top = player_ofa.height + (abs(pl_y-unit_y))
		pl_to_enm_bottom = (abs(pl_y-unit_y))

		x2_attk_rng = self.attacks_dict[two][x_range]
		y2_attk_rng = self.attacks_dict[two][y_range]
		offset = 0.5


		#Check if short attack in range:
		if (x2_attk_rng*offset <= pl_to_enm_right and unit_x >= pl_x):

			if y2_attk_rng*offset <= pl_to_enm_bottom and unit_y > pl_y:
				return True
			
			elif y2_attk_rng*offset <= pl_to_enm_top and unit_y < pl_y:
				return True

		elif (x2_attk_rng*offset <= pl_to_enm_left and unit_x <= pl_x):

			if y2_attk_rng*offset <= pl_to_enm_bottom and unit_y > pl_y:
				return True
			
			elif y2_attk_rng*offset <= pl_to_enm_top and unit_y < pl_y:
				return True

		return False


	def Attack1(self):

		return [self.queue_warn1, self.queue_warn1, self.queue_attack1]

	def Attack2(self):
		return [self.queue_warn1, self.queue_warn1, self.queue_attack1]

	def AI_update(self):
		#self.attack_status = "one"
		#self.check_dmg_done(self.unit_roster)
		
		if self.check_attack_2:
			self.AI.seq_execute(2)
		elif self.check_attack_1:
			self.AI.seq_execute(1)
		else:
			self.AI.seq_execute(0)

	def queue_warn1(self):
		self.attack_status = "warn1"


	def Approach(self):

		unit_x,unit_y = self.get_position()
		player_ofa = self.AI.find_closest_player()
		pl_x, pl_y = player_ofa.get_position()

		if unit_x < pl_x:
			self.move_right()
		elif unit_x > pl_x:
			self.move_left()

		if unit_y < pl_y:
			self.move_down()
		elif unit_y > pl_y:
			self.move_up()


unit.unit_types["BaseEnemyUnit"] = BaseEnemyUnit