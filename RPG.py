import pygame
from pygame.locals import *
import sys
import random
import time
from tkinter import filedialog
from tkinter import *
import numpy

pygame.init()  

#Declarar variables que seran usados en el programa
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

# display
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


# light shade of the button 
color_light = (170,170,170)
color_dark = (100,100,100)
color_white = (255,255,255) 
  
# defining a font
headingfont = pygame.font.SysFont("Verdana", 40)
regularfont = pygame.font.SysFont('Corbel',25)
smallerfont = pygame.font.SysFont('Corbel',16) 
text = regularfont.render('LOAD' , True , color_light)



# animacion de correr a la derecha
run_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Sprite2_R.png"),
             pygame.image.load("Player_Sprite3_R.png"),pygame.image.load("Player_Sprite4_R.png"),
             pygame.image.load("Player_Sprite5_R.png"),pygame.image.load("Player_Sprite6_R.png"),
             pygame.image.load("Player_Sprite_R.png")]

# animacion de correr a la izquierda
run_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Sprite2_L.png"),
             pygame.image.load("Player_Sprite3_L.png"),pygame.image.load("Player_Sprite4_L.png"),
             pygame.image.load("Player_Sprite5_L.png"),pygame.image.load("Player_Sprite6_L.png"),
             pygame.image.load("Player_Sprite_L.png")]

# animacion de atacar a la derecha
attack_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Attack_R.png"),
                pygame.image.load("Player_Attack2_R.png"),pygame.image.load("Player_Attack2_R.png"),
                pygame.image.load("Player_Attack3_R.png"),pygame.image.load("Player_Attack3_R.png"),
                pygame.image.load("Player_Attack4_R.png"),pygame.image.load("Player_Attack4_R.png"),
                pygame.image.load("Player_Attack5_R.png"),pygame.image.load("Player_Attack5_R.png"),
                pygame.image.load("Player_Sprite_R.png")]

# animacion de atacar a la izquierda
attack_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Attack_L.png"),
                pygame.image.load("Player_Attack2_L.png"),pygame.image.load("Player_Attack2_L.png"),
                pygame.image.load("Player_Attack3_L.png"),pygame.image.load("Player_Attack3_L.png"),
                pygame.image.load("Player_Attack4_L.png"),pygame.image.load("Player_Attack4_L.png"),
                pygame.image.load("Player_Attack5_L.png"),pygame.image.load("Player_Attack5_L.png"),
                pygame.image.load("Player_Sprite_L.png")]

# animacion de vida
health_ani = [pygame.image.load("heart0.png"), pygame.image.load("heart.png"),
              pygame.image.load("heart2.png"), pygame.image.load("heart3.png"),
              pygame.image.load("heart4.png"), pygame.image.load("heart5.png")]


class Background(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.bgimage = pygame.image.load("Background.png")
            self.rectBGimg = self.bgimage.get_rect()        
            self.bgY = 0
            self.bgX = 0

      def render(self):
            displaysurface.blit(self.bgimage, (self.bgX, self.bgY))      


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ground.png")
        self.rect = self.image.get_rect(center = (350, 350))
        self.bgX1 = 0
        self.bgY1 = 285

    def render(self):
        displaysurface.blit(self.image, (self.bgX1, self.bgY1)) 


class Item(pygame.sprite.Sprite):
      def __init__(self, itemtype):
            super().__init__()
            if itemtype == 1: self.image = pygame.image.load("heart.png")
            elif itemtype == 2: self.image = pygame.image.load("coin.png")
            self.rect = self.image.get_rect()
            self.type = itemtype
            self.posx = 0
            self.posy = 0
            
      def render(self):
            self.rect.x = self.posx
            self.rect.y = self.posy
            displaysurface.blit(self.image, self.rect)

      def update(self):
            hits = pygame.sprite.spritecollide(self, Playergroup, False)
            
            if hits:
                  if player.health < 5 and self.type == 1:
                        player.health += 1
                        health.image = health_ani[player.health]
                        self.kill()
                  if self.type == 2:
                        handler.money += 1
                        self.kill()
                        


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        # POSICION Y DIRECCIOIN
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "RIGHT"

        # MOVIMIENTO
        self.jumping = False
        self.running = False
        self.move_frame = 0

        #COMBATIR
        self.attacking = False
        self.cooldown = False
        self.immune = False
        self.special = False
        self.experiance = 0
        self.attack_frame = 0
        self.health = 5
        self.mana = 0


    def move(self):
          if cursor.wait == 1: return
          
          
          self.acc = vec(0,0.5)

          
          if abs(self.vel.x) > 0.3:
                self.running = True
          else:
                self.running = False

          
          pressed_keys = pygame.key.get_pressed()

          
          if pressed_keys[K_LEFT]:
                self.acc.x = -ACC
          if pressed_keys[K_RIGHT]:
                self.acc.x = ACC 

          
          self.acc.x += self.vel.x * FRIC
          self.vel += self.acc
          self.pos += self.vel + 0.5 * self.acc  

          
          if self.pos.x > WIDTH:
                self.pos.x = 0
          if self.pos.x < 0:
                self.pos.x = WIDTH
        
          self.rect.midbottom = self.pos            

    def gravity_check(self):
          hits = pygame.sprite.spritecollide(player ,ground_group, False)
          if self.vel.y > 0:
              if hits:
                  lowest = hits[0]
                  if self.pos.y < lowest.rect.bottom:
                      self.pos.y = lowest.rect.top + 1
                      self.vel.y = 0
                      self.jumping = False


    def update(self):
          if cursor.wait == 1: return
          
          
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
          

    def jump(self):
        self.rect.x += 1

        
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        
        self.rect.x -= 1

        
        if hits and not self.jumping:
           self.jumping = True 
           self.vel.y = -12

    def correction(self):
          
          if self.attack_frame == 1:
                self.pos.x -= 20
          if self.attack_frame == 10:
                self.pos.x += 20
                
    def player_hit(self):
        if self.cooldown == False:      
            self.cooldown = True 
            pygame.time.set_timer(hit_cooldown, 1000) 

            self.health = self.health - 1
            health.image = health_ani[self.health]
            
            if self.health <= 0:
                self.kill()
                pygame.display.update()

      
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()     
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        self.wait = 0
        self.wait_status = False
        self.turning = 0

        self.direction = random.randint(0,1) 
        self.vel.x = random.randint(2,6) / 2 
        self.mana = random.randint(1, 3)  

        
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235

      def direction_check(self):
        if (player.pos.x - self.pos.x < 0 and self.direction == 0):
          return 1
        elif (player.pos.x - self.pos.x > 0 and self.direction == 1):
          return 1
        else:
          return 0

      def move(self):
        if cursor.wait == 1: return
        
           
        if self.pos.x >= (WIDTH-20):
              self.direction = 1
        elif self.pos.x <= 0:
              self.direction = 0

            
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
            
        self.rect.topleft = self.pos

        if self.wait > 60:
          self.wait_status = True
        elif int(self.wait) <= 0:
          self.wait_status = False
        if (self.direction_check()):
          self.turn()
          self.wait = 90
          self.turning = 1

      def update(self):
            
            hits = pygame.sprite.spritecollide(self, Playergroup, False)

            
            if hits and player.attacking == True:
                  self.kill()
                  handler.dead_enemy_count += 1
                  
                  if player.mana < 100: player.mana += self.mana 
                  player.experiance += 1   
                  rand_num = numpy.random.uniform(0, 100)
                  item_no = 0
                  if rand_num >= 0 and rand_num <= 5:  
                        item_no = 1
                  elif rand_num > 5 and rand_num <= 15:
                        item_no = 2

                  if item_no != 0:
                        
                        item = Item(item_no)
                        Items.add(item)
                        
                        item.posx = self.pos.x
                        item.posy = self.pos.y
                 

                    
            elif hits and player.attacking == False:
                  player.player_hit()
                  
      def render(self):
            
            displaysurface.blit(self.image, self.rect)
      def turn(self):
        if self.wait > 0:
          self.wait -= 1
          return
        elif int(self.wait) <= 0:
          self.turning = 0
           
        if (self.direction):
            self.direction = 0
            self.image = pygame.image.load("enemy.png")
        else:
            self.direction = 0
            self.image = pygame.image.load("enemy.png")


class Castle(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.hide = False
            self.image = pygame.image.load("castle.png")

      def update(self):
            if self.hide == False:
                  displaysurface.blit(self.image, (400, 80))


class EventHandler():
      def __init__(self):
            self.enemy_count = 0
            self.dead_enemy_count = 0
            self.battle = False
            self.enemy_generation = pygame.USEREVENT + 2
            self.stage = 1
            self.money = 0

            self.stage_enemies = []
            for x in range(1, 21):
                  self.stage_enemies.append(int((x ** 2 / 2) + 1))
            
      def stage_handler(self):
            
            self.root = Tk()
            self.root.geometry('200x170')
            
            button1 = Button(self.root, text = "Twilight Dungeon", width = 18, height = 2,
                            command = self.world1)
            button2 = Button(self.root, text = "Skyward Dungeon", width = 18, height = 2,
                            command = self.world2)
            button3 = Button(self.root, text = "Hell Dungeon", width = 18, height = 2,
                            command = self.world3)
             
            button1.place(x = 40, y = 15)
            button2.place(x = 40, y = 65)
            button3.place(x = 40, y = 115)
            
            self.root.mainloop()
      
      def world1(self):
            self.root.destroy()
            pygame.time.set_timer(self.enemy_generation, 2000)
            button.imgdisp = 1
            castle.hide = True
            self.battle = True

      def world2(self):
            self.battle = True
            button.imgdisp = 1
            

      def world3(self):
            self.battle = True
            button.imgdisp = 1
 
      def next_stage(self):  
            button.imgdisp = 1
            self.stage += 1
            print("Stage: "  + str(self.stage))
            self.enemy_count = 0
            self.dead_enemy_count = 0
            pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))      

      def update(self):
            if self.dead_enemy_count == self.stage_enemies[self.stage - 1]:
                  self.dead_enemy_count = 0
                  stage_display.clear = True
                  stage_display.stage_clear()

      def home(self):
            
            pygame.time.set_timer(self.enemy_generation, 0)
            self.battle = False
            self.enemy_count = 0
            self.dead_enemy_count = 0
            self.stage = 1

            
            for group in Enemies, Items:
                  for entity in group:
                        entity.kill()
            
            
            castle.hide = False
            background.bgimage = pygame.image.load("Background.png")
            ground.image = pygame.image.load("Ground.png")



class HealthBar(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.image = pygame.image.load("heart5.png")

      def render(self):
            displaysurface.blit(self.image, (10,10))


class StageDisplay(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.text = headingfont.render("STAGE: " + str(handler.stage), True, color_dark)
            self.rect = self.text.get_rect()
            self.posx = -100
            self.posy = 100
            self.display = False
            self.clear = False

      def move_display(self):
            
            self.text = headingfont.render("STAGE: " + str(handler.stage), True, color_dark)
            if self.posx < 720:
                  self.posx += 6
                  displaysurface.blit(self.text, (self.posx, self.posy))
            else:
                  self.display = False
                  self.posx = -100
                  self.posy = 100


      def stage_clear(self):
            self.text = headingfont.render("STAGE CLEAR!", True , color_dark)
            button.imgdisp = 0
            
            if self.posx < 720:
                  self.posx += 10
                  displaysurface.blit(self.text, (self.posx, self.posy))
            else:
                  self.clear = False
                  self.posx = -100
                  self.posy = 100
                  
     

class StatusBar(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.surf = pygame.Surface((90, 66))
            self.rect = self.surf.get_rect(center = (500, 10))
            self.exp = player.experiance
            
      def update_draw(self):
            
            text1 = smallerfont.render("STAGE: " + str(handler.stage) , True , color_white)
            text2 = smallerfont.render("EXP: " + str(player.experiance) , True , color_white)
            text3 = smallerfont.render("MANA: " + str(player.mana) , True , color_white)
            text4 = smallerfont.render("FPS: " + str(int(FPS_CLOCK.get_fps())) , True , color_white)
            self.exp = player.experiance

            
            displaysurface.blit(text1, (585, 7))
            displaysurface.blit(text2, (585, 22))
            displaysurface.blit(text3, (585, 37))
            displaysurface.blit(text4, (585, 52))


class Cursor(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.image = pygame.image.load("cursor.png")
            self.rect = self.image.get_rect()
            self.wait = 0

      def pause(self):
            if self.wait == 1:
                  self.wait = 0
            else:
                  self.wait = 1

      def hover(self):
          if 620 <= mouse[0] <= 660 and 300 <= mouse[1] <= 345:
                pygame.mouse.set_visible(False)
                cursor.rect.center = pygame.mouse.get_pos()  
                displaysurface.blit(cursor.image, cursor.rect)
          else:
                pygame.mouse.set_visible(True)
                

class PButton(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.vec = vec(620, 300)
            self.imgdisp = 0

      def render(self, num):
            if (num == 0):
                  self.image = pygame.image.load("home_small.png")
            elif (num == 1):
                  if cursor.wait == 0:
                        self.image = pygame.image.load("pause_small.png")
                  else:
                        self.image = pygame.image.load("play_small.png")
                                    
            displaysurface.blit(self.image, self.vec)

                  
            


Enemies = pygame.sprite.Group()

player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)

background = Background()
button = PButton()
ground = Ground()
cursor = Cursor()

ground_group = pygame.sprite.Group()
ground_group.add(ground)

castle = Castle()
handler = EventHandler()
health = HealthBar()
stage_display = StageDisplay()
status_bar = StatusBar()
Fireballs = pygame.sprite.Group()
Items = pygame.sprite.Group()

hit_cooldown = pygame.USEREVENT + 1

          
            
            

while True:
    player.gravity_check()
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == hit_cooldown:
            player.cooldown = False
          
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == handler.enemy_generation and cursor.wait == 0:
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                  enemy = Enemy()
                  Enemies.add(enemy)
                  handler.enemy_count += 1
        
         
        if event.type == pygame.MOUSEBUTTONDOWN:
              if 620 <= mouse[0] <= 660 and 300 <= mouse[1] <= 350:
                    if button.imgdisp == 1:
                          cursor.pause()
                    elif button.imgdisp == 0:
                          handler.home()


            
        if event.type == pygame.KEYDOWN and cursor.wait == 0:
            if event.key == pygame.K_n:
                  if handler.battle == True and len(Enemies) == 0:
                        handler.next_stage()
                        stage_display = StageDisplay()
                        stage_display.display = True
            if event.key == pygame.K_q and 450 < player.rect.x < 550:
                handler.stage_handler()
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_RETURN:
                if player.attacking == False:
                    player.attack()
                    player.attacking = True      


    
    player.update()
    if player.attacking == True:
          player.attack() 
    player.move()                

             
    background.render()
    ground.render()
    button.render(button.imgdisp)
    cursor.hover()


    
    if stage_display.display == True:
          stage_display.move_display()
    if stage_display.clear == True:
          stage_display.stage_clear()

    
    castle.update()
    if player.health > 0:
        displaysurface.blit(player.image, player.rect)
    health.render()

   
    displaysurface.blit(status_bar.surf, (580, 5))
    status_bar.update_draw()
    handler.update()

    
    for i in Items:
          i.render()
          i.update() 
   
    for entity in Enemies:
          entity.update()
          entity.move()
          entity.render()
      

    pygame.display.update()      
    FPS_CLOCK.tick(FPS)
