
from animation import LoadImages
from unit.base_unit import BaseUnit
from animation import Animation
import unit
from ai import AI
import engine, random

class BaseEnemyUnit(BaseUnit):
	"""
	Base AI Unit.
	"""

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords):
		
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords)
		self.anim_walking = LoadImages(dirr, []).sequence
		self.anim_warn1 = LoadImages(dirr, []).sequence 
		self.anim_atk1 = LoadImages(dirr, []).sequence
		self.anim_death = LoadImages(dirr, []).sequence	
		self.AI = AI(self,[])
		self.AI.sequence.append([self.Approach])
		self.AI.sequence.append([self.queue_warn1,self.queue_attack1])
		self.AI.sequence.append([self.queue_warn1,self.queue_attack1])
		self.intelligence = 25 # 0 - 100 higher the greater chance he has to execute methods()

	
	def draw_walking(self, screen):
		rate = 5
		Animation(screen, self, 0,0, self.anim_walking, rate).animate()
		if self.anim_walking[-2] == len(self.anim_walking) - 3 and self.anim_walking[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_walking, 5).animate()
			self.anim_walking[-2] = 0
			self.is_walking = 0


	def draw_atk1(self, screen):
		#Stab
		rate = 1
		Animation(screen, self, 0,0, self.anim_atk1, rate).animate()
		#Animation(screen, self, self.width, self.stab_effect, rate).animate()
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"

	def draw_warn1(self, screen):
		#Stab 
		rate = 10
		Animation(screen, self, 0,0, self.anim_warn1, rate).animate()
		#Animation(screen, self, self.width, self.stab_effect, rate).animate()
		if self.anim_warn1[-2] == len(self.anim_warn1) - 3 and self.anim_warn1[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_warn1, 5).animate()
			self.anim_warn1[-2] = 0
			self.attack_status = "one"
			self.dmg_dealt = False


	def draw_atk2(self, screen):
		#slash
		rate = 3
		Animation(screen, self, 0,0, self.anim_atk2, rate).animate()
		Animation(screen, self, self.width, self.slash_effect, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"

	def check_attack_1(self):
		"""
		Check if another targeted unit is within range of attack
		"""

		unit_x,unit_y = self.get_position()
		player_ofa = self.AI.find_closest_player()
		pl_x, pl_y = player_ofa.get_position()
		pl_to_enm_right = (abs(pl_x-unit_x)) - player_ofa.width
		pl_to_enm_left = (abs(unit_x-pl_x)) - self.width
		pl_to_enm_top =  (abs(pl_y-unit_y)) - player_ofa.height
		pl_to_enm_bottom = (abs(pl_y-unit_y)) - self.height

		x1_attk_rng = self.attacks_dict["one"]["x_range"]
		y1_attk_rng = self.attacks_dict["one"]["y_range"]
		offset = 0.5

		#Check if long attack in range:
		
		return engine.in_range_cross(self, player_ofa, x1_attk_rng, y1_attk_rng, self.direction)

	def check_attack_2(self):
		"""
		Check if another targeted unit is within range of attack
		"""

		unit_x,unit_y = self.get_position()
		player_ofa = self.AI.find_closest_player()
		pl_x, pl_y = player_ofa.get_position()
		pl_to_enm_right = (abs(pl_x-unit_x)) - player_ofa.width
		pl_to_enm_left = (abs(unit_x-pl_x)) - self.width
		pl_to_enm_top =  (abs(pl_y-unit_y)) - player_ofa.height
		pl_to_enm_bottom = (abs(pl_y-unit_y)) - self.height

		x2_attk_rng = self.attacks_dict["two"]["x_range"]
		y2_attk_rng = self.attacks_dict["two"]["y_range"]
		offset = 0.5

		return engine.in_range_cross(self, player_ofa, x2_attk_rng, y2_attk_rng, self.direction)

	def AI_update(self, screen):
		"""
		Logic behind AI decisions
		Based on certain criteria executes methods()
		"""
		if self.attack_status == "none":
				if self.check_attack_1():
					self.queue_warn1()
				else:
					self.attack_status = "none"
					self.AI.seq_count = 0
					if random.randint(0,100) < self.intelligence:
						self.Approach()

	def queue_warn1(self):
		self.attack_status = "warn1"


	def Approach(self):
		"""
		Checks for closest player and then
		makes a move toward them
		"""

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