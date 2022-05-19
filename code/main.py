import pygame, sys
from support import screen_width, screen_height
from level import Level
from level_data import level_map
from ui import Menu

"""
     Game class and main gameloop 

class Game: controlling the music and the gamestate

    change_player_health(value) : called in level.Level.pickup_collision / player.Player.hurt
        value = int
            adds value to player_health
       
    check_gameover() : called in main.Game.game_state
        when player_health reaches 0 main.Game.active changes
    
    check_win() : called in main.Game.game_state
        when boss_health reaches 0 main.Game.active changes
    
    music_on(music) : called in main.Game.game_state
        music = Sound file
            music gets turned on
    
    music_off(music) : called in main.Game.game_state
        music = Sound file
            music gets turned off
    
    game_state() : called in main.Game.run
        checks for content of main.Game.active
    
    run() : called in main in the main game loop

Main Gameloop: 
    - buttonpress detection for moving between game states
"""
pygame.mixer.init()
pygame.init()
pygame.font.init()
pygame.joystick.init()

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
class Game:
    def __init__(self):
        
        self.menu = Menu(screen)
        
        #controls what part of the game is active
        self.active = "Start"
        
        #font
        self.font = pygame.font.Font("../graphics/font/Alkhemikal.ttf", 35)
        
        #game music and volume
        self.volume = True
        self.bg_Music = pygame.mixer.Sound("../music/bgnice.mp3")
        self.bg_Music.set_volume(2)
        self.boss_Music = pygame.mixer.Sound("../music/bossnice.mp3")
        self.boss_Music.set_volume(0.5)
        
        #screens to be displayed in game_state()
        self.start_menu = pygame.image.load("../graphics/screens/bg.png")
        self.win = pygame.image.load("../graphics/screens/win.png")
        self.game_over = pygame.image.load("../graphics/screens/go.png")
        self.pause = pygame.image.load("../graphics/screens/pause.png")
        
        #Player health used as gameovertrigger
        self.player_health = 10
        
        #Boss health to use it as wintrigger
        self.boss_health_full = 1500
        self.boss_health = self.boss_health_full
        
        #score
        self.coin_amount = 0
        
    def get_inputs(self):
        # pygame.joystick.init()
        # joystick_list = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        # joystick = joystick_list[0]
        if e.type == pygame.KEYDOWN:
            if self.active == "Start" and e.key == pygame.K_q:
                self.active = "ShowHighscore"
            elif self.active == "ShowHighscore" and e.key == pygame.K_q:
                self.active = "Start"
            elif self.active == "Start":
                self.active = "LevelStart"
                
            if self.active == "Level" and e.key == pygame.K_q:
                self.active = "Pause"
            elif self.active == "Pause" and e.key == pygame.K_r:
                self.music_off(self.bg_Music)
                self.music_off(self.boss_Music)
                self.active = "LevelStart"
            elif self.active == "Pause" and e.key == pygame.K_e:
                if self.volume:
                    self.volume = False
                    self.music_off(self.bg_Music)
                    self.music_off(self.boss_Music)
                else: 
                    self.volume = True
                    if not self.boss_health == 1500:
                        self.music_on(self.boss_Music)
                    else: self.music_on(self.bg_Music)
                
            elif e.key == pygame.K_q and game.active == "Pause":
                self.active = "Level"
                
            if (self.active == "GameOver" or self.active == "Win") and e.key == pygame.K_m:
                self.active = "Start"
        
    def change_coins(self,value):
        self.coin_amount += value
        return self.coin_amount
        
    def change_player_health(self,value):
        self.player_health += value
        return self.player_health
        
    def drain_boss_health(self):
        self.boss_health -= 1
        return self.boss_health
        
    def music_on(self,music):
        music.play(loops = -1)
        
    def music_off(self,music):
        music.stop()
    
    def game_state(self):
        if self.active == "Start":
            self.menu.show_screen(self.start_menu)
        
        elif self.active == "ShowHighscore":
#           display the highscores
            pass
        
        elif self.active == "LevelStart":
            self.player_health = 10
            self.boss_health = self.boss_health_full
            self.coin_amount = 0
            self.level = Level(level_map,screen,self.change_player_health,self.player_health,self.boss_health,self.boss_health_full,self.drain_boss_health,self.change_coins)
            self.music_on(self.bg_Music)
            self.active = "Level"
            
        elif self.active == "Level":
            self.level.run()
            if self.player_health <= 0:
                self.active = "GameOver_Music"
            if self.boss_health == 1499 and self.volume:
                self.music_on(self.boss_Music)
                self.music_off(self.bg_Music)
            if self.boss_health <= -100:
                self.active = "Win"
            
        elif self.active == "Pause":
            self.menu.show_screen(self.pause)
            
        elif self.active == "GameOver_Music":
            self.music_off(self.bg_Music)
            self.music_off(self.boss_Music)
            self.active = "GameOver"
            
        elif self.active == "GameOver":
            self.menu.show_screen(self.game_over)
            
        elif self.active == "Highscore":
#           putting the score into the highscore
            pass
            
        elif self.active == "Win":
            self.menu.show_screen(self.win)
            self.music_off(self.bg_Music)
            self.music_off(self.boss_Music)

    def update_fps(self):
        fps = str(int(clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color("coral"))
        return fps_text
        
    def run(self):
        self.game_state()
        screen.blit(self.update_fps(), (100,100))

game = Game()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.get_inputs()
        
    screen.fill("black")
    game.run()
    
    pygame.display.update()    
    clock.tick(60)