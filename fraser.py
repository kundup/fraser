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
ghost_image = pygame.image.load("images/ghost.png")

# font colors
over_white = (255, 255, 65)
black = (0, 0, 0)

# definition values
tile_size = 25
game_over = 0
score = 0


def draw_environment(image, image_rect):
    screen.blit(image, image_rect)


def draw_line():
    for i in range(24):
        pygame.draw.line(screen, (255, 255, 255), (0, i * tile_size), (screen_width, i * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (i * tile_size, 0), (i * tile_size, screen_height))


def all_text(text, color, size, x, y):
    font_surf = pygame.font.Font("images/Pixeltype.ttf", size)
    font_render = font_surf.render(text, False, color)
    font_rect = font_render.get_rect(midbottom=(x, y))
    screen.blit(font_render, font_rect)


class Button:
    def __init__(self):
        self.restart = pygame.image.load("images/restart_btn.png")
        self.rect = self.restart.get_rect(midbottom=(300, 350))
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pos):
                player.reset()
                self.clicked = True
        else:
            self.clicked = False

        screen.blit(self.restart, self.rect)
        return self.clicked



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.enem = pygame.image.load("images/blob.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.enem, (21, 17))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.counter = 0

    def update(self):
        self.rect.x += self.direction
        if self.counter >= 20:
            self.direction *= -1
            self.counter *= -1
        self.counter += 1


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.coin = pygame.image.load("images/coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.coin, (14, 13))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        super().__init__()
        self.platform = pygame.image.load("images/platform.png").convert_alpha()
        self.image = pygame.transform.scale(self.platform, (tile_size, 14))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direction = 1
        self.counter = 0
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.direction * self.move_x
        self.rect.y += self.direction * self.move_y
        if self.counter >= 50:
            self.counter *= -1
            self.direction *= -1

        self.counter += 1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.lava = pygame.image.load("images/lava.png").convert_alpha()
        self.image = pygame.transform.scale(self.lava, (25, 21))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reset()

    def update_player(self, game_over):

        if not game_over:
            pressed_key = pygame.key.get_pressed()
            dx = 0
            dy = 0

            if pressed_key[pygame.K_RIGHT]:
                self.direction = 0
                self.index += 0.2
                if self.index >= len(self.image):
                    self.index = 0
                dx = self.vel_x
            if pressed_key[pygame.K_LEFT]:
                self.direction = 1
                self.index += 0.2
                if self.index >= len(self.image):
                    self.index = 0
                dx = -self.vel_x

            if pressed_key[pygame.K_SPACE] and not self.jumped:
                self.vel_y = -10
                self.jumped = True

            self.vel_y += 1
            dy += self.vel_y

            # collison detection
            for tile in worldmap.tile_list:
                # x direction collision check
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width,
                                       self.rect.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width,
                                       self.rect.height):
                    if self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.jumped = False
                    elif self.vel_y < 0:  # jumping
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0

            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = 1

            for platforms in platform_group:
                if platforms.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height) :
                    dx = 0
                # Yatay çarpışma
                if platforms.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    # oyuncu platformun altındaysa ve belirli bir mesafedeyse
                    if self.vel_y >= 0:  # Oyuncu aşağı iniyorsa
                        if abs(self.rect.bottom - platforms.rect.top) < self.threshold:
                            self.rect.bottom = platforms.rect.top-1
                            dy = 0
                            self.vel_y = 0
                            self.jumped = False
                    elif self.vel_y < 0:  # Oyuncu yukarı çıkıyorsa
                        if abs(self.rect.top - platforms.rect.bottom) < self.threshold:
                            self.rect.top = platforms.rect.bottom-1
                            dy = 0
                            self.vel_y = 0

            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom >= screen_height - tile_size * 2:
                self.rect.bottom = screen_height - tile_size * 2
                self.vel_y = 0
                self.jumped = False

            screen.blit(self.image[self.direction][int(self.index)], self.rect)

        else:
            self.image = pygame.transform.smoothscale(ghost_image, (tile_size, tile_size))
            self.rect.y -= 2

            screen.blit(self.image, self.rect)

        return game_over

    def reset(self):

        self.index = 0
        self.index_l = 0
        self.direction = 0
        self.vel_y = 0
        self.vel_x = 2
        self.jumped = False
        self.threshold = 20

        img1 = pygame.image.load(f"images/guy1.png").convert_alpha()
        img2 = pygame.image.load(f"images/guy2.png").convert_alpha()

        self.img1 = [pygame.transform.scale(img1, (21, 47)), pygame.transform.scale(img2, (21, 47))]
        self.img1_l = [pygame.transform.flip(num, True, False) for num in self.img1]

        self.image = [self.img1, self.img1_l]
        self.direction = 0
        self.rect = self.image[self.direction][self.index].get_rect(
            midbottom=(100, screen_height - tile_size * 2))


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
                if colomn == 3:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size + 5)
                    enemy_group.add(enemy)

                if colomn == 4:
                    coin = Coin(col_count * tile_size, row_count * tile_size + 3)
                    coin_group.add(coin)

                if colomn == 5:
                    lava = Lava(col_count * tile_size, row_count * tile_size + 4)
                    lava_group.add(lava)

                if colomn == 6:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)

                if colomn == 7:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)

                col_count += 1
            row_count += 1

    def drawing_dirt_grass(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


world_map = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 4, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 1],
    [1, 7, 0, 0, 6, 0, 0, 0, 0, 2, 2, 2, 5, 5, 2, 2, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

enemy_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
button = Button()
player = Player()
worldmap = WorldMap(world_map)

run = True
while run:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw_environment(sky_image, sky_image_rect)
    draw_environment(sun_image, pygame.Rect(100, 50, sun_image.get_width(), sun_image.get_height()))

    worldmap.drawing_dirt_grass()
    game_over = player.update_player(game_over)

    if game_over:
        if player.rect.y <= 100:
            player.rect.y = 100
            all_text("Game Over", over_white, 80, 300, 300)

            if button.draw():
                game_over = 0

    else:
        enemy_group.update()
        platform_group.update()
        if pygame.sprite.spritecollide(player, coin_group, True):
            score += 1
        if pygame.sprite.spritecollide(player, lava_group, False):
            game_over = 1

    enemy_group.draw(screen)
    coin_group.draw(screen)
    lava_group.draw(screen)
    platform_group.draw(screen)
    all_text(f"My Score: {str(score)}", black, 35, 100, 35)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

# collisions (done)
# adding enemies (done)
# adding coins and scores
# adding levels
# moving platforms
# adding sounds
# adding AI onto enemies
