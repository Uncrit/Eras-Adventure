import pygame
"""
    Everything displayed ontop of or outside the Level

class UI(surface) : called in level.Level.run
    surface = display_surface
        in Level Overlay
            # display surface
            display_surface = output screen
            
            # font
            myfont = general font
            
            # boss healthbar
            boss_health_bar = image of outer shell of healthbar
            boss_bar_width = width of boss health bar
            boss_bar_height = height of boss health bar
            
            # coin
            coin = image of coin
            
            # keys
            key = image of key
            stkey = image of stage key
            sckey = image of secret key
            
            #player hearts
            player_heart_full = image of full player heart
            player_heart_half = image of half player heart

    show_coin_amount(coin_amount) : called in ui.UI.run
        coin_amount = int
            amount coins picked up
                renders it into a font and displays it and the coin image
        
    show_key_amount(key_amount) : called in ui.UI.run
        key_amount = list of string
            amount of keys and what type of keys picked up
                cycles through key_amount and displays them
    
    show_player_health(player_health) : called in ui.UI.run
        player_health = int
            Player health amount
                for every 2 health it displays a full heart
                for leftover health it displays a half heart
        
    show_boss_health(boss_healt,boss_health_full) : called in ui.UI.run
        boss_health = int
        boss_health_full = int
            Boss health amount
                calculates the ratio of boss_health and boss_full_health
                displays it as a rectangle as the healthbar
        
    show_boss_health_bar() : called in ui.UI.run
            Boss health bar
                displays the outer shell of the healthbar
    
    run(bossroom_active,coin_amount,key_amount,player_health,boss_health,boss_health_full) : called in level.Level.run
        bossroom_active = boolean
        passes coin_amount to show_coin_amount
        passes key_amount to show_key_amount
        passes player_health to show_player_health
        passes boss_health, boss_health_full to show_boss_health
            runs all the functions in UI
                determines when show_boss_health and show_boss_health_bar need to be active
            gets coin_amount,key_amount,player_health,boss_health,boss_health_full from level.Level.run
                distributes every variable to the right functions and runs them

class Menu(surface) : called in main.Game.__init__
    surface = display_surface
        #display surface
        display_surface = output screen
        
        #font
        myfont = general font
        
    show_screen(image) : called in main.Game.game_state
        displays the given screen
"""
class UI:
    def __init__(self,surface):
        #display surface
        self.display_surface = surface
        
        #font
        self.myfont = pygame.font.Font("../graphics/font/Alkhemikal.ttf", 35)
        
        #boss healthbar
        self.boss_health_bar = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha()
        self.boss_bar_width = 480
        self.boss_bar_height = 32
        
        #coin
        self.coin = pygame.image.load ("../graphics/tiles/coin.png")
        
        #keys
        self.key = pygame.image.load("../graphics/tiles/key.png")
        self.stkey = pygame.image.load("../graphics/tiles/stagekey.png")
        self.sckey = pygame.image.load('../graphics/tiles/sckey.png')
        
        #player hearts
        self.player_heart_full = pygame.image.load('../graphics/ui/heart_full.png')
        self.player_heart_half = pygame.image.load('../graphics/ui/heart_half.png')
        
    def show_coin_amount(self,coin_amount):
        coins = self.myfont.render(str(coin_amount),False,(255,255,255))
        self.display_surface.blit(coins,(70,35))
        self.display_surface.blit(self.coin,(35,35))
        
    def show_key_amount(self,key_amount):
        x = 35
        for key in key_amount:
            if key == "key":
                image = self.key
            elif key == "stkey":
                image = self.stkey
            elif key == "sckey":
                image = self.sckey
            self.display_surface.blit(image,(x,110))
            x += 35
        
    def show_player_health(self,player_health):
        x = 35
        for _ in range(0,int(player_health / 2)):
            self.display_surface.blit(self.player_heart_full,(x,80))
            x += 24
        if player_health % 2:
            self.display_surface.blit(self.player_heart_half,(x,80))
        
    def show_boss_health(self,boss_health,boss_health_full):
        cur_health_ratio = boss_health / boss_health_full
        cur_bar_width = self.boss_bar_width * cur_health_ratio
        health_bar_rect = pygame.Rect((400,100),(cur_bar_width,self.boss_bar_height))
        pygame.draw.rect(self.display_surface ,'white',health_bar_rect)
        
    def show_boss_health_bar(self):
        self.display_surface.blit(self.boss_health_bar,(396,96))
        
    def run(self,bossroom_active,coin_amount,key_amount,player_health,boss_health,boss_health_full):
        self.show_key_amount(key_amount)
        self.show_coin_amount(coin_amount)
        self.show_player_health(player_health)
        if bossroom_active and boss_health > 0:
            self.show_boss_health_bar()
            self.show_boss_health(boss_health,boss_health_full)
        
class Menu:
    def __init__(self,surface):
        #display surface
        self.display_surface = surface
        
        #font
        self.myfont = pygame.font.Font("../graphics/font/Alkhemikal.ttf", 35)
        
    def show_screen(self,image):
        self.display_surface.blit(image,(0,0))
        
    