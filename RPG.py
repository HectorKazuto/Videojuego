import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *

pygame.init()  # Iniciar Pygame
 
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG")

run_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Sprite2_R.png"),
			pygame.image.load("Player_Sprite3_R.png"),pygame.image.load("Player_Sprite4_R.png"),
			pygame.image.load("Player_Sprite5_R.png"),pygame.image.load("Player_Sprite6_R.png"),
			pygame.image.load("Player_Sprite_R.png")]

run_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Sprite2_L.png"),
			pygame.image.load("Player_Sprite3_L.png"),pygame.image.load("Player_Sprite4_L.png"),
			pygame.image.load("Player_Sprite5_L.png"),pygame.image.load("Player_Sprite6_L.png"),
			pygame.image.load("Player_Sprite_L.png")]

attack_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Attack_R.png"),
				pygame.image.load("Player_Attack2_R.png"),pygame.image.load("Player_Attack2_R.png"),
				pygame.image.load("Player_Attack3_R.png"),pygame.image.load("Player_Attack3_R.png"),
				pygame.image.load("Player_Attack4_R.png"),pygame.image.load("Player_Attack4_R.png"),
				pygame.image.load("Player_Attack5_R.png"),pygame.image.load("Player_Attack5_R.png"),
				pygame.image.load("Player_Sprite_R.png")]

attack_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Attack_L.png"),
				pygame.image.load("Player_Attack2_L.png"),pygame.image.load("Player_Attack2_L.png"),
				pygame.image.load("Player_Attack3_L.png"),pygame.image.load("Player_Attack3_L.png"),
				pygame.image.load("Player_Attack4_L.png"),pygame.image.load("Player_Attack4_L.png"),
				pygame.image.load("Player_Attack5_L.png"),pygame.image.load("Player_Attack5_L.png"),
				pygame.image.load("Player_Sprite_L.png")]

class Background(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.bgimage = pygame.image.load("Background.png")
		self.bgY = 0
		self.bgX = 0

	def render(self):
		displaysurface.blit(self.bgimage, (self.bgX, self.bgY))

class Ground(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("Ground.png")
		self.rect = self.image.get_rect(center = (350, 350))

	def render(self):
		displaysurface.blit(self.image, (self.rect.x, self.rect.y)) 

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("Player_Sprite_R.png")
		self.rect = self.image.get_rect()

		self.vx = 0
		self.pos = vec((340, 240))
		self.vel = vec(0,0)
		self.acc = vec(0,0)
		self.jumping = False
		self.running = False
		self.move_frame = 0
		self.direction = "RIGHT"

		self.attacking = False
		self.cooldown = False
		self.attack_frame = 0

	def move(self):

		self.acc = vec(0,0.5)
		if abs(self.vel.x) > 0.3:
			self.running = True
		else:
			self.running = False
		
		pressed_keys = pygame.key.get_pressed()

		if pressed_keys[K_LEFT] or pressed_keys[ord('a')]:
			self.acc.x = -ACC
			
		if pressed_keys[K_RIGHT] or pressed_keys[ord('d')]:
			self.acc.x = ACC

		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH

		self.rect.midbottom = self.pos

	def animation(self):
		if self.move_frame > 6:
			self.move_frame = 0
			return
		
		if self.jumping == False and self.running == True:
			if self.vel.x > 0:
				self.image = run_ani_R[self.move_frame]
				self.direction = "RIGHT"

			else:
				self.image = run_ani_L[self.move_frame]
				self.direction = "LEFT"
			self.move_frame += 1

		if abs(self.vel.x) < 0.2 and self.move_frame != 0:
			self.move_frame = 0
			if self.direction == "RIGHT":
				self.image = run_ani_R[self.move_frame]
			elif self.direction == "LEFT":
				self.image = run_ani_L[self.move_frame]

	def attack(self):
		if self.attack_frame > 10:
			self.attack_frame = 0
			self.attacking = False

		if self.direction == "RIGHT":
			self.image = attack_ani_R[self.attack_frame]
		elif self.direction == "LEFT":
			self.correction()
			self.image = attack_ani_L[self.attack_frame] 

		self.attack_frame += 1

	def correction(self):
		if self.attack_frame == 1:
			self.pos.x -= 10
			if self.attack_frame == 10:
				self.pos.x += 10

	def jump(self):
		self.rect.x += 1

		hits = pygame.sprite.spritecollide(self, ground_group, False)

		self.rect.x -= 1

		if hits and not self.jumping:
			self.jumping = True
			self.vel.y = -12

	def gravity_check(self):
		hits = pygame.sprite.spritecollide(player ,ground_group, False)
		if self.vel.y > 0:
			if hits:
				lowest = hits[0]
				if self.pos.y < lowest.rect.bottom:
					self.pos.y = lowest.rect.top + 1
					self.vel.y = 0
					self.jumping = False


class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("Enemy.png")
		self.rect = self.image.get_rect()
		self.pos = vec(0,0)
		self.vel = vec(0,0)
		self.direction = random.randint(0,1)
		self.vel.x = random.randint(2,6) / 2
		if self.direction == 0:
			self.pos.x = 0
			self.pos.y = 235
		if self.direction == 1:
			self.pos.x = 700
			self.pos.y = 235
		self.cooldown = False
		self.hit_cooldown = pygame.USEREVENT + 1

	def move(self):

		if self.pos.x >= (WIDTH-20):
			self.direction = 1
		elif self.pos.x <= 0:
			self.direction = 0

		if self.direction == 0:
			self.pos.x += self.vel.x
		if self.direction == 1:
			self.pos.x -= self.vel.x

		self.rect.center = self.pos

	def render(self):
		displaysurface.blit(self.image, (self.pos.x, self.pos.y))

	

	def colide(self):
		hits = pygame.sprite.spritecollide(self, Playergroup, False)

		if hits and player.attacking == True:
			self.kill()

		#elif hits and player.attacking == False:
			#self.player_hit()

	def player_hit(self):
		if self.cooldown == False:
			self.cooldown = True
			pygame.time.set_timer(self.hit_cooldown, 1000)

		self.colide()

	def gravity_check(self):
		hits = pygame.sprite.spritecollide(enemy ,ground_group, False)
		if self.vel.y > 0:
			if hits:
				lowest = hits[0]
				if self.pos.y < lowest.rect.bottom:
					self.pos.y = lowest.rect.top + 1
					self.vel.y = 0
					self.jumping = False


background = Background()

ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)

enemy = Enemy()


while True:

	player.gravity_check()
	enemy.gravity_check()
	background.render()
	ground.render()
	player.animation()
	enemy.colide()
	if player.attacking == True:
		player.attack()
	player.move()
	enemy.move()
	displaysurface.blit(player.image, player.rect)
	enemy.render()

	pygame.display.update()
	FPS_CLOCK.tick(FPS)

	for event in pygame.event.get():
		if event.type == enemy.hit_cooldown:
			player.cooldown = False
			pygame.time.set_timer(enemy.hit_cooldown, 0)

		if event.type == QUIT:
			pygame.quit()
			sys.exit() 

		if event.type == pygame.MOUSEBUTTONDOWN:
			if player.attacking == False:
				player.attack()
				player.attacking = True 
 
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE or event.key == ord('w'):
				player.jump()
				#