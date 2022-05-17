import pygame
from tiles import Animated_Tile, Moving_Tile

"""
class Enemy(pos,path,animation_path,animation_speed,animations,random_speed,direction_x,direction_y) : called in level.Level.setup_level
    passes pos,path,animation_path,animation_speed,animations,random_speed,direction_x,direction_y to tiles.Moving_Tile
        animated, moving sprite whose animation can turn around
    
    turn_around() : called im enemies.Enemy.update
        checks which direction the sprite is moving
        
    update(x_shift,y_shift) : called in level.Level.run
        x_shift = int | camera speed
        y_shift = int | camera speed
            movement of the camera, update the animation and movement
                only updates animation and movement when the camrea isnt moving
        
class Projectile(pos1,pos2,bullet_speed) : called in level.Level.bossfight
    pos1 = list of 2 int | start position of the projectile sprite
    pos2 = list of 2 int | position the projectile moves torwards
    bullet_speed = int | speed at which the projectile moves
        # image of the projectile
        image = pygame.image.load("../graphics/boss/projectile/projectile.png")
        rect = image.get_rect(center = pos1)
    
        # start and aim position
        pos1 = position where sprite gets created
        pos2 = position sprite moves torwards
    
        # movement speed
        speed = speed the sprite moves at
    
        # movement direction
        direction = direction the sprite moves
    
        # aim
        direction.x = calculates a path on the x-axis between pos1 and pos2 for the sprite to move on
        direction.y = calculates a path on the y-axis between pos1 and pos2 for the sprite to move on
    
    move() : moves the sprite in the specified direction
        
    update(x_shift,y_shift) : called inlevel.Level.run
        x_shift = int | camera speed
        y_shift = int | camera speed
            updates camera and sprite movement
                updates movement when camera isnt moving
        
class Boss(pos,path,animation_path,animation_speed,animations) : called in level.Level.setup_level
    passes pos,path,animation_path,animation_speed,animations to tiles.Animated_Tile
        moving sprite with different speeds
    
    phase_2() : called in enemies.Boss.update
        changes the speed and the animation of the sprite
        
    turn_around(pos1,pos2) : called in level.Level.bossfight
        pos1 = list of 2 int
        pos2 = list of 2 int
            turns sprite around to whichever side the player sprite is on
        
    move() : called in enemies.Boss.update
        moves the sprite in an arrow shape
        
    update(x_shift,y_shift,bossroom_active,boss_health,boss_health_full) : called in level.Level.run
        x_shift = int | camera speed
        y_shift = int | camera speed
            updates cameramovement, animation, spritemovement, phase_2
            
"""

class Enemy(Moving_Tile):
    def __init__(self,pos,path,animation_path,animation_speed,animations,random_speed,direction_x,direction_y):
        super().__init__(pos,path,animation_path,animation_speed,animations,random_speed,direction_x,direction_y)
        
    def turn_around(self):
        if self.direction.x > 0:
            self.facing_right = True
        else: self.facing_right = False
        
    def update(self,x_shift,y_shift):
        if not x_shift and not y_shift:
            self.turn_around()
            self.animate()
            self.move()
        else:
            self.rect.x += x_shift
            self.rect.y += y_shift
                    
class Projectile(pygame.sprite.Sprite):
    def __init__(self,pos1,pos2,proj_speed):
        super().__init__()
        
        #image of the projectile
        self.image = pygame.image.load("../graphics/boss/projectile/projectile.png")
        self.rect = self.image.get_rect(center = pos1)
        
        #movement direction
        self.direction = pygame.math.Vector2(0,0)
        
        #aim
        self.direction.x = int((pos1[0] - pos2[0])/proj_speed)
        self.direction.y = int((pos1[1] - pos2[1])/proj_speed)
        
    def move(self):
        self.rect.y +=  self.direction.y * -1
        self.rect.x +=  self.direction.x * -1
        
    def update(self,x_shift,y_shift):
        if not x_shift and not y_shift:
            self.move()
        else:
            self.rect.x += x_shift
            self.rect.y += y_shift
            
class Boss(Animated_Tile):
    def __init__(self,pos,path,animation_path,animation_speed,animations):
        super().__init__(pos,path,animation_path,animation_speed,animations)
        # movement 
        self.speed = pygame.math.Vector2(3,1)
        self.direction = pygame.math.Vector2(-1,1)
        self.turn = 0
        self.turns = 0
        self.gravity = 0.5
    
    def phase_2(self):
        self.status = "phase_2"
        self.speed.y = 2
        self.speed.x = 6
    
    def turn_around(self,pos1,pos2):
        #turning him around to always look at the Player
        if pos1[0] < pos2[0]:
            self.facing_right = True
        else: self.facing_right = False
            
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def move(self):
        self.rect.y += self.direction.y * self.speed.y
        self.rect.x += self.direction.x * self.speed.x
        self.turn += self.speed.y
        if self.turn >= 128:
            self.direction.y *= -1
            self.direction.x *= -1
            self.turn = 0
            self.turns += 1
            if self.turns == 2:
                self.direction.x *= -1
                self.turns = 0
            
    def update(self,x_shift,y_shift,bossroom_active,boss_health,boss_health_full):
        if boss_health <= 0:
            self.apply_gravity()
        self.rect.x += x_shift
        self.rect.y += y_shift
        self.animate()
        if bossroom_active and boss_health > 0:
            self.move()
            if boss_health < (boss_health_full / 3):
                self.phase_2()