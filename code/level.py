import pygame
from support import tile_size, screen_width, screen_height
from tiles import Block, Animated_Tile, Moving_Tile
from enemies import Enemy, Boss, Projectile
from player import Player
from ui import UI

"""
class Level(level_map,surface,change_player,player_health,boss_health,boss_health_full,drain_boss_health,change_coins) : called in main.Game.game_state

    setup_level(level_map) : called in level.Level.__init__
        level_map = list
            goes through every position in level_map 
                (the image mapping can be seen in ../editor/def.txt)
        
    collision() : called in level.Level.run
    
            makes the player unable to pass through the specified sprite groups
            calls door collision for "door", "stdoor", "scdoor"
            controls on_ground to limit the player from jumping while in the air
            invisible bossroomtrigger that activates bossfight
        
    door_collision(sprite_group,key_type,collidables,key_delete) : called in level.Level.collision
        sprite_group = sprite group
        key_type = string
        collidables = sum of sprite groups
        key_delete = boolean
        
            detects collision between player sprite and sprites in sprite_group
                checks for key_type in Level.key_amount
                if True
                    destroys sprite in sprite_group and key_type in Level.key_amount
                    checks key_delete
                    if True
                        empties Level.key_amount
                else
                    adds sprite to collidables
                    
        
    bossfight() : called in level.Level.run
            activates after the player sprite hit the bossroomtrigger
                gives position of player sprite and boss sprite to enemies.Boss.turn_around 
                creates projectile sprites at specified rate
        
    enemy_collision() : called in level.Level.run
            destroys projectile sprites when they leave the screen
            destroys enemy sprites when the player sprites hits them from the top while falling down
                plays a kill_sound and adds a coin
            calls damage_collision
        
    damage_collision(sprite_group,damage) : called in level.Level.enemy_collision
        sprite_group = sprite group
        damage = int
            subtracts damage from player health when the player sprite collides with sprite_group
        
    pickup_collision() : called in level.Level.run
            detects collision between player sprite and coin sprite
                destroys coin, plays coin_sound and adds to coin_amount
            detects if the button "e" is pressed
                checks if player sprite collides with heart sprite
                checks if player health is below 10 and coin_amount is above 5
                    destroys heart, plays heart_sound,subtracts 5 of coin_amount and adds 2 to player health
                if player health goes above 10 it gets put to 10
            calls key_pickup for "key", "stkey", "sckey"
        
    key_pickup() : called in level.Level.pickup_collision
            detects collision between player sprite and sprite_group
                destroys key sprite, plays key_sound, adds key_type to key_amount
        
    transition() : called in level.Level.run
            checks if the player sprite hits the edge of the screen
                changes x_shift or y_shift depending on where the player sprite left screen
            checks if x_shift or y_shift have a value
                makes the player sprite unable to move, adds x_shift/y_shift to Level.stop every iteration
                checks if Level.stop reaches specified number
                    resets x_shift/y_shift and Level.stop
        
    run() : called in main.Game.game_state
        runs all the functions needed for the level to work
"""

class Level:
    def __init__(self,level_map,surface,change_player_health,player_health,boss_health,boss_health_full,drain_boss_health,change_coins):
        
        self.display_surface = surface
        
        # intitiating UI
        self.ui = UI(self.display_surface)
        
        # transition
        self.x_shift = 0
        self.y_shift = 0
        self.stop = 0
        
        # the amount of coins and keys
        self.coin_amount = 0
        self.change_coins = change_coins
        self.key_amount = []
        
        # Player health
        self.player_health = player_health
        self.change_health = change_player_health
        
        #setting up level
        self.setup_level(level_map)
        
        # jumpconditions
        self.player_on_ground = False
        self.player_on_ceiling = False
        
        # bossroom
        self.bossroom_active = False
        self.boss_health = boss_health
        self.boss_health_full = boss_health_full
        self.drain_boss_health = drain_boss_health
        self.shoot = None
        self.shoot_timer = 350
        self.shoot_time = 0
        
        # font
        self.font_name = pygame.font.match_font("Algerian")
        
        # sounds
        self.kill_sound = pygame.mixer.Sound("../music/kill.wav")
        self.kill_sound.set_volume(0.5)
        self.coin_sound = pygame.mixer.Sound("../music/coin.mp3")
        self.coin_sound.set_volume(0.3)
        self.key_sound = pygame.mixer.Sound("../music/key.mp3")
        self.key_sound.set_volume(0.3)
        self.heart_sound = pygame.mixer.Sound("../music/heart.mp3")
        self.door_sound = pygame.mixer.Sound("../music/door.mp3")
        self.door_sound.set_volume(2)
        
        
    def setup_level(self,level_map):
        # spritegroups
        self.heart  = pygame.sprite.Group()
        self.sckey  = pygame.sprite.Group()
        self.stkey  = pygame.sprite.Group()
        self.key    = pygame.sprite.Group()
        self.coins  = pygame.sprite.Group()

        self.spike  = pygame.sprite.Group()
        self.enemy  = pygame.sprite.Group()
        self.saw    = pygame.sprite.Group()
        self.proj   = pygame.sprite.Group()

        self.scdoor = pygame.sprite.Group()
        self.stdoor = pygame.sprite.Group()
        self.door   = pygame.sprite.Group()
        self.tiles  = pygame.sprite.Group()
        
        self.player = pygame.sprite.GroupSingle()
        
        self.brt    = pygame.sprite.Group()
        self.boss   = pygame.sprite.GroupSingle()


        for row_index,row in enumerate(level_map):                  
            for col_index,cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                if cell == "0":
                    pass
                
                elif cell == '1':
                      tile = Block((x,y),'../graphics/terrain/tile000.png')
                      self.tiles.add(tile)
                      
                elif cell == '2':
                      tile = Block((x,y),'../graphics/terrain/tile001.png')
                      self.tiles.add(tile)
                      
                elif cell == '3':
                      tile = Block((x,y),'../graphics/terrain/tile002.png')
                      self.tiles.add(tile)
                      
                elif cell == '4':
                      tile = Block((x,y),'../graphics/terrain/tile003.png')
                      self.tiles.add(tile)
                      
                elif cell == '5':
                      tile = Block((x,y),'../graphics/terrain/tile004.png')
                      self.tiles.add(tile)
                      
                elif cell == '6':
                      tile = Block((x,y),'../graphics/terrain/tile005.png')
                      self.tiles.add(tile)
                              
                elif cell == '7':
                      tile = Block((x,y),'../graphics/terrain/tile006.png')
                      self.tiles.add(tile)
                      
                elif cell == '8':
                      tile = Block((x,y),'../graphics/terrain/tile007.png')
                      self.tiles.add(tile)
                      
                elif cell == '9':
                      tile = Block((x,y),'../graphics/terrain/tile008.png')
                      self.tiles.add(tile)
                      
                elif cell == '=':
                      tile = Block((x,y),'../graphics/terrain/tile009.png')
                      self.tiles.add(tile)
                              
                elif cell == 'Q':
                      tile = Block((x,y),'../graphics/terrain/tile010.png')
                      self.tiles.add(tile)
                      
                elif cell == 'W':
                      tile = Block((x,y),'../graphics/terrain/tile011.png')
                      self.tiles.add(tile)
                      
                elif cell == 'E':
                      tile = Block((x,y),'../graphics/terrain/tile012.png')
                      self.tiles.add(tile)
                      
                elif cell == 'R':
                      tile = Block((x,y),'../graphics/terrain/tile013.png')
                      self.tiles.add(tile)
                      
                elif cell == 'T':
                      tile = Block((x,y),'../graphics/terrain/tile014.png')
                      self.tiles.add(tile)
                      
                elif cell == 'Z':
                      tile = Block((x,y),'../graphics/terrain/tile015.png')
                      self.tiles.add(tile)
                      
                elif cell == 'U':
                      tile = Block((x,y),'../graphics/terrain/tile016.png')
                      self.tiles.add(tile)
                      
                elif cell == 'I':
                      tile = Block((x,y),'../graphics/terrain/tile017.png')
                      self.tiles.add(tile)
                      
                elif cell == 'O':
                      tile = Block((x,y),'../graphics/terrain/tile018.png')
                      self.tiles.add(tile)
                      
                elif cell == 'P':
                      tile = Block((x,y),'../graphics/terrain/tile019.png')
                      self.tiles.add(tile)
                      
                elif cell == ':':
                      tile = Block((x,y),'../graphics/terrain/tile020.png')
                      self.tiles.add(tile)
                      
                elif cell == '*':
                      tile = Block((x,y),'../graphics/terrain/tile021.png')
                      self.tiles.add(tile)
                      
                elif cell == 'A':
                      tile = Block((x,y),'../graphics/terrain/tile022.png')
                      self.tiles.add(tile)
                      
                elif cell == 'S':
                      tile = Block((x,y),'../graphics/terrain/tile023.png')
                      self.tiles.add(tile)
                      
                elif cell == 'D':
                      tile = Block((x,y),'../graphics/terrain/tile024.png')
                      self.tiles.add(tile)
                      
                elif cell == 'F':
                      tile = Block((x,y),'../graphics/terrain/tile025.png')
                      self.tiles.add(tile)
                      
                elif cell == 'G':
                      tile = Block((x,y),'../graphics/terrain/tile026.png')
                      self.tiles.add(tile)
                      
                elif cell == 'H':
                      tile = Block((x,y),'../graphics/terrain/tile027.png')
                      self.tiles.add(tile)
                      
                elif cell == 'J':
                      tile = Block((x,y),'../graphics/terrain/tile028.png')
                      self.tiles.add(tile)
                      
                elif cell == 'K':
                      tile = Block((x,y),'../graphics/terrain/tile029.png')
                      self.tiles.add(tile)
                      
                elif cell == 'L':
                      tile = Block((x,y),'../graphics/terrain/tile030.png')
                      self.tiles.add(tile)
                      
                elif cell == '~':
                      tile = Block((x,y),'../graphics/terrain/tile031.png')
                      self.tiles.add(tile)
                      
                elif cell == '-':
                      tile = Block((x,y),'../graphics/terrain/tile032.png')
                      self.tiles.add(tile)
                                    
                elif cell == 'Y':
                      tile = Block((x,y),'../graphics/terrain/tile033.png')
                      self.tiles.add(tile)
                      
                elif cell == 'X':
                      tile = Block((x,y),'../graphics/terrain/tile034.png')
                      self.tiles.add(tile)
                      
                elif cell == 'C':
                      tile = Block((x,y),'../graphics/terrain/tile035.png')
                      self.tiles.add(tile)
                      
                elif cell == 'V':
                      tile = Block((x,y),'../graphics/terrain/tile036.png')
                      self.tiles.add(tile)
                      
                elif cell == 'B':
                      tile = Block((x,y),'../graphics/terrain/tile037.png')
                      self.tiles.add(tile)
                      
                elif cell == 'N':
                      tile = Block((x,y),'../graphics/terrain/tile038.png')
                      self.tiles.add(tile)
                      
                elif cell == 'M':
                      tile = Block((x,y),'../graphics/terrain/tile039.png')
                      self.tiles.add(tile)
                      
                elif cell == '<':
                      tile = Block((x,y),'../graphics/terrain/tile040.png')
                      self.tiles.add(tile)
                      
                elif cell == '>':
                      tile = Block((x,y),'../graphics/terrain/tile041.png')
                      self.tiles.add(tile)
                      
                elif cell == '|':
                      tile = Block((x,y),'../graphics/terrain/tile042.png')
                      self.tiles.add(tile)
                      
                elif cell == '^':
                      tile = Block((x,y),'../graphics/terrain/tile043.png')
                      self.tiles.add(tile)
                      
                elif cell == '+':
                      tile = Block((x,y),'../graphics/terrain/tile044.png')
                      self.tiles.add(tile)
                      
                elif cell == 'n':
                      tile = Block((x,y),'../graphics/terrain/tile045.png')
                      self.tiles.add(tile)
                      
                elif cell == 'm':
                      tile = Block((x,y),'../graphics/terrain/tile046.png')
                      self.tiles.add(tile)
                     
                elif cell == 'o':
                      tile = Moving_Tile((x,y),'../graphics/saw/run/saw1.png','../graphics/saw/',0.05,{'run':[]},0,1,[1,2,2,2,2,2,4])
                      self.saw.add(tile)

                elif cell == 'u':
                      tile = Moving_Tile((x,y),'../graphics/saw/run/saw1.png','../graphics/saw/',0.05,{'run':[]},1,0,[1,2,2,2,2,2,4])
                      self.saw.add(tile)

                elif cell == 'd':
                    tile = Block((x,y),'../graphics/tiles/door.png')
                    self.door.add(tile)
                                      
                elif cell == 'f':
                    tile = Block((x,y),'../graphics/tiles/stagedoor.png')
                    self.stdoor.add(tile)
                
                elif cell == "q":
                    tile = Block((x,y),'../graphics/tiles/scdoor.png')
                    self.scdoor.add(tile)
                
                elif cell == 'k':
                    tile = Block((x,y),'../graphics/tiles/key.png')
                    self.key.add(tile)
                    
                elif cell == 'j':
                    tile = Block((x,y),'../graphics/tiles/stagekey.png')
                    self.stkey.add(tile)
                    
                elif cell == "w":
                    tile = Block((x,y),'../graphics/tiles/sckey.png')
                    self.sckey.add(tile)
                    
                elif cell == 'c':
                    tile = Animated_Tile((x,y),'../graphics/tiles/coin.png','../graphics/coin/',0.025,{'run':[]})
                    self.coins.add(tile)
                                    
                elif cell == 's':
                    tile = Block((x,y),'../graphics/spikes/spikes.png')
                    self.spike.add(tile)
                    
                elif cell == 'y':
                    tile = Block((x,y),'../graphics/spikes/spikesup.png')
                    self.spike.add(tile)
                    
                elif cell == 'x':
                    tile = Block((x,y),'../graphics/spikes/spikesleft.png')
                    self.spike.add(tile)
                    
                elif cell == 'v':
                    tile = Block((x,y),'../graphics/spikes/spikesright.png')
                    self.spike.add(tile)
                    
                elif cell == 'h': 
                    tile = Block((x,y),'../graphics/tiles/heart.png')
                    self.heart.add(tile)
                
                elif cell == 'e':
                    tile = Enemy((x,y),'../graphics/enemy/run/3.png','../graphics/enemy/',0.1,{'run':[]},1,0,[1,2,2,2,2,2,4])
                    self.enemy.add(tile)
                    
                elif cell == 'i':
                    tile = Block((x,y),'../graphics/tiles/trigger.png')
                    self.brt.add(tile)
                    
                elif cell == 'z':
                    tile = Block((x,y),'../graphics/tiles/secret.png')
                    self.tiles.add(tile)
                    
                elif cell == 'b':
                    tile = Boss((x,y),'../graphics/boss/run/Boss1.png','../graphics/boss/',0.05,{'run':[],'phase_2':[]})
                    self.boss.add(tile)
                    
                elif cell == 'p':
                    player_sprite = Player((x,y),'../graphics/player/idle/0.png','../graphics/player/',0.1,{'idle':[],'run':[],'jump':[]},self.change_health)
                    self.player.add(player_sprite)
                
    def collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        #collision on x-axis
        collidables = self.tiles.sprites()
        
        self.door_collision(self.door.sprites(),"key",collidables,False)
        
        self.door_collision(self.scdoor.sprites(),"sckey",collidables,False)
        
        for sprite in collidables:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
        
        
        #gravity(needs to be after x-axis collisions)
        player.apply_gravity()
        
        #collision on y-axis
        self.door_collision(self.stdoor.sprites(),"stkey",collidables,True)
        
        for sprite in collidables:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    self.player_on_ground = True
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    self.player_on_ceiling = True
        
        if (self.player_on_ground and player.direction.y < 0 or player.direction.y > 1) or self.player_on_ceiling:
            self.player_on_ground = False
            self.player_on_ceiling = False

        #bossroom trigger
        for sprite in self.brt.sprites():
            if sprite.rect.colliderect(self.player.sprite.rect):
                self.bossroom_active = True

    def door_collision(self,sprite_group,key_type,collidables,key_delete):
        player = self.player.sprite
        for sprite in sprite_group:
            if sprite.rect.colliderect(player.rect):
                if self.key_amount.count(key_type) > 0:
                    sprite.kill()
                    self.door_sound.play()
                    self.key_amount.remove(key_type)
                    if key_delete:
                        self.key_amount = []
                else: collidables += sprite_group

    def bossfight(self):
        if self.bossroom_active:
            Boss = self.boss.sprite
            self.boss_health = self.drain_boss_health()
            if self.boss_health <= 0:
                self.shoot = False
            pos1 = Boss.rect.center
            pos2 = self.player.sprite.rect.center
            Boss.turn_around(pos1,pos2)
            if self.shoot:
                self.shoot_time = pygame.time.get_ticks()
                tile = Projectile(pos1,pos2,70)
                self.proj.add(tile)
                self.shoot = False
            else:
                time = pygame.time.get_ticks()
                if time - self.shoot_time > self.shoot_timer:
                    self.shoot = True
            
    def enemy_collision(self):
        player = self.player.sprite
        dmg_coll = self.saw.sprites() + self.boss.sprites() + self.proj.sprites()
                    
        #projectiles
        for sprite in self.proj.sprites():
            if sprite.rect.x > 1280 or sprite.rect.x < 0 or sprite.rect.y > 1024 or sprite.rect.y < 0:
                sprite.kill()
        
        #enemies
        for enemy in self.enemy.sprites():
            if enemy.rect.colliderect(player.rect):
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = player.rect.bottom
                if enemy_top < player_bottom < enemy_center and player.direction.y >= 0:
                    player.direction.y = -10
                    enemy.kill()
                    self.kill_sound.play()
                    self.coin_amount = self.change_coins(1)
                else: dmg_coll += self.enemy.sprites()
        
        #damage collisions
        self.damage_collision(self.spike.sprites(),2)
        self.damage_collision(dmg_coll,1)
        
    def damage_collision(self,sprite_group,damage):
        player = self.player.sprite
        for sprite in sprite_group:
            if sprite.rect.colliderect(player.rect):
                self.player_health = player.hurt(-(damage))
        
    def pickup_collision(self):
        player = self.player.sprite
        
        #coins
        for sprite in self.coins.sprites():
            if sprite.rect.colliderect(player.rect):
                sprite.kill()
                self.coin_amount = self.change_coins(1)
                self.coin_sound.play()

        #heart
        pygame.joystick.init()
        joystick_list = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        joystick = joystick_list[0]
        if pygame.key.get_pressed()[pygame.K_e] or joystick.get_button(3,6):
            for heart in self.heart.sprites():
                if heart.rect.colliderect(player.rect):
                    if self.player_health < 10 and self.coin_amount >= 5:
                        heart.kill()
                        self.coin_amount = self.change_coins(-5)
                        self.player_health = self.change_health(2)
                        self.heart_sound.play()
                    if self.player_health > 10:
                        self.player_health = 10

        #keys
        self.key_pickup(self.key.sprites(),"key")
                
        self.key_pickup(self.stkey.sprites(),"stkey")
                
        self.key_pickup(self.sckey.sprites(),"sckey")

    def key_pickup(self,sprite_group,key_type):
        player = self.player.sprite
        for key in sprite_group:
            if key.rect.colliderect(player.rect):
                key.kill()
                self.key_amount.append(key_type)
                self.key_sound.play()

    def transition(self):
        player = self.player.sprite
        
        if player.rect.right < 0:
            self.x_shift = 32
            self.bossroom_active = False
        elif player.rect.left > screen_width:
            self.x_shift = -32
            self.bossroom_active = False
        if player.rect.bottom < 0:
            self.y_shift = 32
            self.bossroom_active = False
        elif player.rect.top > screen_height:
            self.y_shift = -32
            self.bossroom_active = False

        if self.x_shift:
            self.stop += self.x_shift
            player.direction.x = 0
            player.direction.y = 0
            if self.stop == -1312 or self.stop == 1312:
                self.x_shift = 0
                self.stop = 0
        
        if self.y_shift:
            self.stop += self.y_shift
            player.direction.x = 0
            player.direction.y = 0
            if self.stop == -1056 or self.stop == 1056:
                self.y_shift = 0
                self.stop = 0

    def run(self):
        #pickups
        self.heart.draw(self.display_surface)
        self.heart.update(self.x_shift,self.y_shift)
        self.sckey.draw(self.display_surface)
        self.sckey.update(self.x_shift,self.y_shift)
        self.stkey.draw(self.display_surface)
        self.stkey.update(self.x_shift,self.y_shift)
        self.key.draw(self.display_surface)
        self.key.update(self.x_shift,self.y_shift)
        self.coins.draw(self.display_surface)
        self.coins.update(self.x_shift,self.y_shift)

        #dmg dealing
        self.spike.draw(self.display_surface)
        self.spike.update(self.x_shift,self.y_shift)
        self.enemy.draw(self.display_surface)
        self.enemy.update(self.x_shift,self.y_shift)
        self.saw.draw(self.display_surface)
        self.saw.update(self.x_shift,self.y_shift)
        
        #walls
        self.scdoor.draw(self.display_surface)
        self.scdoor.update(self.x_shift,self.y_shift)
        self.stdoor.draw(self.display_surface)
        self.stdoor.update(self.x_shift,self.y_shift)
        self.door.draw(self.display_surface)
        self.door.update(self.x_shift,self.y_shift)
        self.tiles.draw(self.display_surface)
        self.tiles.update(self.x_shift,self.y_shift)
        
        #player
        self.player.draw(self.display_surface)
        self.player.update(self.x_shift,self.y_shift,self.player_on_ground,self.player_health)
        
        #bossfight
        self.brt.update(self.x_shift,self.y_shift)
        self.proj.draw(self.display_surface)
        self.proj.update(self.x_shift,self.y_shift)
        self.bossfight()
        self.boss.draw(self.display_surface)
        self.boss.update(self.x_shift,self.y_shift,self.bossroom_active,self.boss_health,self.boss_health_full)
        
        #collisions and stuff
        self.ui.run(self.bossroom_active,self.coin_amount,self.key_amount,self.player_health,self.boss_health,self.boss_health_full)
        self.enemy_collision()
        self.pickup_collision()
        self.collision()
        self.transition()