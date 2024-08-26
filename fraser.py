import pygame

pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# loading images
sky = pygame.image.load("images/sky.png").convert_alpha()
sky_image = pygame.transform.scale(sky, (screen_width, screen_height))
sky_image_rect = sky_image.get_rect(topleft=(0, 0))

sun_image = pygame.image.load("images/sun.png").convert_alpha()

# tile_size
tile_size = 25


def draw_sky():
    screen.blit(sky_image, sky_image_rect)
    screen.blit(sun_image, (100, 50))


def draw_line():
    for i in range(24):
        pygame.draw.line(screen, (255, 255, 255), (0, i * tile_size), (screen_width, i * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (i * tile_size, 0), (i * tile_size, screen_height))


class Player:
    def __init__(self):
        self.index = 0
        self.direction = 0
        img1 = pygame.image.load(f"images/guy1.png").convert_alpha()
        img2 = pygame.image.load(f"images/guy2.png").convert_alpha()
        self.img1 = pygame.transform.scale(img1, (21, 47))
        self.img2 = pygame.transform.scale(img2, (21, 47))
        self.player_img = [self.img1, self.img2]
        self.player_rect = self.player_img[self.index].get_rect(midbottom=(100, screen_height - tile_size * 2))

    def update_player(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_RIGHT]:
            self.index += 0.2
            if self.index >= len(self.player_img):
                self.index = 0
            self.player_rect.x += 2
        if pressed_key[pygame.K_LEFT]:
            pass

        screen.blit(self.player_img[int(self.index)], self.player_rect)


class WorldMap:
    def __init__(self, world_map):
        self.tile_list = []
        dirt = pygame.image.load("images/dirt.png").convert()
        grass = pygame.image.load("images/grass.png").convert()

        dirt_image = pygame.transform.scale(dirt, (tile_size, tile_size))
        grass_image = pygame.transform.scale(grass, (tile_size, tile_size))

        row_count = 0
        for row in world_map:
            col_count = 0
            for colomn in row:
                if colomn == 1:
                    dirt_image_rect = dirt_image.get_rect()
                    dirt_image_rect.x = tile_size * col_count
                    dirt_image_rect.y = tile_size * row_count
                    tile = (dirt_image, dirt_image_rect)
                    self.tile_list.append(tile)
                if colomn == 2:
                    grass_image_rect = grass_image.get_rect()
                    grass_image_rect.x = tile_size * col_count
                    grass_image_rect.y = tile_size * row_count
                    tile = (grass_image, grass_image_rect)
                    self.tile_list.append(tile)

                col_count += 1
            row_count += 1

    def drawing_dirt(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

worldmap = WorldMap(world_map)
player = Player()

run = True
while run:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw_sky()
    worldmap.drawing_dirt()
    player.update_player()
    # draw_line()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
