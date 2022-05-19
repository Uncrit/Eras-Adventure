import pygame
from tiles import Animated_Tile

"""

class Player(pos,path,anim_path,anim_speed,animations,change_health) : called in level.Level.setup_level
    passes pos,path,anim_path,anim_speed,animations to tiles.Animated_Tile.__init__
    change_health = function 
        everything around User character
            # movement
            direction = direction and axis of sprite movement
            speed = speed of sprite movement
            gravity = speed of downwards movement of sprite
            jump_height = height of upwards movement on jump
            on_ground = check if player is standing on ground

            # health + hurt animation
            health = main.Game.player_health
            cur_health = int to compare to Player.health for hurt_animation()
            hurt_time = time of hurt() call
            invincible = check for hurt() eligibility
            invincibility = time for hurt() eligibility change
            count = time the hurt_animation() runs
            change_health = main.Game.change_health
            
            # sound
            jump_sound = sound played when jump() called
            hurt_sound = sound played when hurt() called
            
    hurt_animation() : called in player.Player.update
            checks if health has gotten lower to start hurt animation
            updates cur_health to player health
        
    hurt(damage) : called in level.Level.damage_collision
        damage = int
            changes player health, plays sound, calculates if player can be damaged
                updates the player health 
                plays hurt sound
                checks if player health can be lowered
        
    get_status() : called in player.Player.update
            changes status for animate to display the right images
                updates status by checking if player is on ground or moving
        
    jump() : called in player.Player.get_inputs
            moves the player sprite upwards
        
    apply_gravity() : called in level.Level.collisions
            makes the player sprite continuously move downwards
        
    get_inputs() : 
            detects buttonpresses
                detects a and d for left or right movement
                detects spacebar to run Player.jump and play the jump sound
        
    update(x_shift,y_shift,on_ground,health) : called in level.Level.run
        x_shift = int
        y_shift = int
            movement of the camera, getting inputs, update the animation, status and health
            get x_shift,y_shift from level.Level.run
                only updates inputs,animation, status and health when the camera isnt moving

"""

class Player(Animated_Tile):
    def __init__(self,pos,path,anim_path,anim_speed,animations,change_health):
        super().__init__(pos,path,anim_path,anim_speed,animations)

        # movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 5
        self.gravity = 0.5
        self.jump_height = -11
        self.on_ground = True

        # health + hurt animation
        self.health = 0
        self.cur_health = 10
        self.hurt_time = 0
        self.invincible = False
        self.invincibility = 1000
        self.count = 0
        self.change_health = change_health
        
        # sound
        self.jump_sound = pygame.mixer.Sound("../music/jump.mp3")
        self.jump_sound.set_volume(0.4)
        self.hurt_sound = pygame.mixer.Sound("../music/hurt.mp3")
        self.hurt_sound.set_volume(0.4)
        
    def hurt_animation(self):
        if self.cur_health > self.health:
            self.count += 1
            if self.count % 2 == 0:
                self.image.set_alpha(0)
            else: self.image.set_alpha(255)
            if self.count == 50:
                self.image.set_alpha(255)
                self.cur_health = self.health
                self.count = 0
        else:
            self.image.set_alpha(255)
        
        if self.cur_health < self.health:
            self.cur_health = self.health
        
    def hurt(self,damage):
        if not self.invincible:
            self.invincible = True
            self.health = self.change_health(damage)
            self.hurt_sound.play()
            self.hurt_time = pygame.time.get_ticks()
        else:
            time = pygame.time.get_ticks()
            if time - self.hurt_time > self.invincibility:
                self.invincible = False
        return self.health
        
    def get_status(self):
        if not self.on_ground:
            self.status = 'jump'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
            
    def jump(self):
        self.direction.y = self.jump_height
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
            
    def get_inputs(self):
        keys = pygame.key.get_pressed()
        # pygame.joystick.init()
        # joystick_list = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        # joystick = joystick_list[0]
        
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_w]:
            self.image = pygame.image.load("../graphics/player/eg/up.png")
            self.direction.x = 0
        elif keys[pygame.K_s]:
            self.image = pygame.image.load("../graphics/player/eg/down.png")
            self.direction.x = 0
        else:
            self.direction.x = 0
        if (keys[pygame.K_SPACE]) and self.on_ground:
            self.jump()
            self.jump_sound.play()
   
    def update(self,x_shift,y_shift,on_ground,health):
        if not x_shift and not y_shift:
            self.animate()
            self.hurt_animation()
            self.health = health
            self.on_ground = on_ground
            self.get_status()
            self.get_inputs()
        else:
            self.rect.x += x_shift
            self.rect.y += y_shift