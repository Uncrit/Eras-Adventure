from os import walk
import pygame

""" generally used variables

import_folder(path) : called in tiles.Animated_Tile.import_character_assets / player.Player.import_character_assets
    
        imports images and puts them in a folder for use in animations
        
    path = the directory of the image folder
"""

tile_size = 32
screen_width = 1280
screen_height = 1024


def import_folder(path):                        
	surface_list = []

	for _,__,image_files in walk(path):
		for image in image_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list


        
        

