import pygame
from support import import_folder
from random import choice

""" display simple sprites with animations or movement

class Block(pos,path) : called in level.Level.setup_level / Animated_Tile
    pos = list of 2 int
    path = string
        # image and rect
        image = loads image
        rect = creates rect around the image and positions it
        
    update(x_shift,y_shift) : called in level.Level.run
        x_shift = int | camera speed
        y_shift = int | camera speed
            movement of the camera

class Animated_Tile(pos,path,anim_path,anim_speed,animations) : called in level.Level.setup_level / enemies.Boss / Moving_Tile
    passes pos,path to tiles.Block
    anim_path = string
    anim_speed = int
    animations = dictionairy
        # animation
        import_character_assets(anim_path,animations) | call of function
        frame_index = counts up to control what image is being shown in animate()
        animation_speed = gets added to frame_index every iteration
        status = controls which animation is being shown
    
        # turning around
        facing_right = turns the image around
        
    import_character_assets(anim_path,animations) : tiles.Animated_Tile.__init__
        import the folder with the animation images
            loads the images in a folder and puts it in a dictionairy under a status

    animate() : called in tiles.Animated_Tile.update
        displaying current image, adding to index to cycle images, turns the sprite around
            checks for status change
            adds the animations speed to frame_index and resets it
            checks if sprite needs to turn and display image
    
    update(x_shift,y_shift) : called in level.Level.run
        x_shift = int
        y_shift = int
            movement of the camera and update the animation
                only updates animation when camera isnt moving

class Moving_Tile(pos,path,anim_path,anim_speed,animations,direction_x,direction_y,random_speed) : called in level.Level.setup_level
    passes pos,path,anim_path,anim_speed,animations to tiles.Animated_Tile
    direction_x = int
    direction_y = int
    random_speed = list of int
        # movement
        speed = speed the sprite moves at
        turn = counts up to determine time to move sprite in opposite direction
        direction = direction the sprite is moving
        random_speed = vaiation of speed on turn 

    move() : called in tiles.Moving_Tile.update
        moves sprite 128 pixels from side to side
            moves sprite by specified speed and diection
            counts until 128 pixels have been run
            moves sprite opposite direction and randomises the speed

    update(x_shift,y_shift) : called in level.Level.run
        x_shift = int
        y_shift = int
            movement of the camera, update the animation and movement
                only updates animation and movement when camera isnt moving
"""

class Block(pygame.sprite.Sprite):
    def __init__(self,pos,path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self,x_shift,y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift
        
class Animated_Tile(Block):
    def __init__(self,pos,path,anim_path,anim_speed,animations):
        super().__init__(pos,path)
        
        #animation
        self.import_character_assets(anim_path,animations)
        self.frame_index = 0
        self.animation_speed = anim_speed
        self.status = "run"
        
        #turning around
        self.facing_right = True

    def import_character_assets(self,anim_path,animations):
        character_path = anim_path
        self.animations = animations

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        image = animation[int(self.frame_index)]
        
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
    
    def update(self,x_shift,y_shift):
        if not x_shift and not y_shift:
            self.animate()
        else:
            self.rect.x += x_shift
            self.rect.y += y_shift
        
class Moving_Tile(Animated_Tile):
    def __init__(self,pos,path,anim_path,anim_speed,animations,direction_x,direction_y,random_speed):
        super().__init__(pos,path,anim_path,anim_speed,animations)
        self.speed = 2
        self.turn = 0
        self.direction = pygame.math.Vector2(direction_x,direction_y)
        self.random_speed = random_speed
    
    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.turn += self.speed
        if self.turn >= 128:
            self.direction.y *= -1
            self.direction.x *= -1
            self.speed = choice(self.random_speed)
            self.turn = 0
    
    def update(self,x_shift,y_shift):
        if not x_shift and not y_shift:
            self.animate()
            self.move()
        else:
            self.rect.x += x_shift
            self.rect.y += y_shift