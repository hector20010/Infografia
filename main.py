import math
import random

import arcade

# definicion de constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Guerra de tanques asesinos"
SCALING = 0.15
SPEED = 5
BULLET_SPEED = 15

class Wall(arcade.Sprite):
    def __init__(self, filename, scale, x, y):
        super().__init__(filename, scale)
        self.center_x = x
        self.center_y = y


class App(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.DARK_GRAY)
        self.sprites = arcade.SpriteList()

        #Jugador 1
        self.player = arcade.Sprite("img/tanque1.png", SCALING)
        self.player.center_x = SCREEN_WIDTH - 50
        self.player.center_y = SCREEN_HEIGHT / 2

        self.sprites.append(self.player)
        self.player_speed = 0
        self.bullets = arcade.SpriteList()

        #Jugador 2
        self.player2 = arcade.Sprite("img/tanque2.png", SCALING)
        self.player2.center_x = 50
        self.player2.center_y = SCREEN_HEIGHT / 2

        self.sprites.append(self.player2)
        self.player2_speed = 0
        self.bullets2 = arcade.SpriteList()

        self.enemies = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        self.score = 0
        self.score2 = 0
        self.game_over = False
        self.paused = False
        self.player1_wins = False

        #Crear paredes
        wall1 = Wall("img/wall.png", 2, 150, 150)
        wall2 = Wall("img/wall.png", 2, 850, 650)
        wall3 = Wall("img/wall.png", 2, 500, 400)
        wall4 = Wall("img/wall.png", 2, 350, 700)
        wall5 = Wall("img/wall.png", 2, 700, 200)

        self.sprites.append(wall1)
        self.sprites.append(wall2)
        self.sprites.append(wall3)
        self.sprites.append(wall4)
        self.sprites.append(wall5)
        self.walls.append(wall1)
        self.walls.append(wall2)
        self.walls.append(wall3)
        self.walls.append(wall4)
        self.walls.append(wall5)

        arcade.schedule(self.add_enemy, 5.0)

    def on_key_press(self, symbol: int, modifiers: int):
        """Metodo para detectar teclas que han sido presionada
        El punto se movera con las teclas de direccion.
        Argumentos:
            symbol: tecla presionada
            modifiers: modificadores presionados
        """

        #Teclas para jugador 1
        if symbol == arcade.key.UP:
            if not self.player.collides_with_list(self.walls):
                self.player_speed = SPEED
        if symbol == arcade.key.DOWN:
            if not self.player.collides_with_list(self.walls):
                self.player_speed = -SPEED

        if symbol == arcade.key.LEFT:
            self.player.change_angle += 5
        if symbol == arcade.key.RIGHT:
            self.player.change_angle -= 5

        #Teclas para jugador 2
        if symbol == arcade.key.W:
            if not self.player2.collides_with_list(self.walls):
                self.player2_speed = SPEED
        if symbol == arcade.key.S:
            if not self.player2.collides_with_list(self.walls):
                self.player2_speed = -SPEED

        if symbol == arcade.key.A:
            self.player2.change_angle += 5
        if symbol == arcade.key.D:
            self.player2.change_angle -= 5

        if symbol == arcade.key.SPACE:
            bullet = arcade.Sprite(
                "img/bullet.png",
                0.1,
                angle=self.player.angle + 90,
                center_x=self.player.center_x,
                center_y=self.player.center_y,
            )
            bullet.velocity = (
                BULLET_SPEED * math.cos(math.radians(self.player.angle + 90)),
                BULLET_SPEED * math.sin(math.radians(self.player.angle + 90))
            )
            self.bullets.append(bullet)
            self.sprites.append(bullet)

        if symbol == arcade.key.E:
            bullet2 = arcade.Sprite(
                "img/bullet.png",
                0.1,
                angle=self.player2.angle + 90,
                center_x=self.player2.center_x,
                center_y=self.player2.center_y,
            )
            bullet2.velocity = (
                BULLET_SPEED * math.cos(math.radians(self.player2.angle + 90)),
                BULLET_SPEED * math.sin(math.radians(self.player2.angle + 90))
            )
            self.bullets2.append(bullet2)
            self.sprites.append(bullet2)

        #Colicion de jugadores con enemigo
        for enemy in self.enemies:
            if self.player.collides_with_sprite(enemy):
                self.player1_wins = False
                self.game_over = True
                break
            if self.player2.collides_with_sprite(enemy):
                self.player1_wins = True
                self.game_over = True
                break

        # Colision de jugadores con paredes
        for wall in self.walls:
            if self.player.collides_with_sprite(wall):
                self.player_speed = 0
                if symbol == arcade.key.UP:
                    self.player.center_y -= 5
                elif symbol == arcade.key.DOWN:
                    self.player.center_y += 5
                elif symbol == arcade.key.LEFT:
                    self.player.center_x += 5
                elif symbol == arcade.key.RIGHT:
                    self.player.center_x -= 5
                break

            if self.player2.collides_with_sprite(wall):
                self.player2_speed = 0
                if symbol == arcade.key.W:
                    self.player2.center_y += 5
                elif symbol == arcade.key.S:
                    self.player2
                elif symbol == arcade.key.A:
                    self.player2.center_x += 5
                elif symbol == arcade.key.D:
                    self.player2.center_x -= 5
                break

            if symbol == arcade.key.UP:
                if not self.player.collides_with_list(self.walls):
                    self.player_speed = SPEED
                else:
                    self.player_speed = 0
            if symbol == arcade.key.DOWN:
                if not self.player.collides_with_list(self.walls):
                    self.player_speed = -SPEED
                else:
                    self.player_speed = 0
            if symbol == arcade.key.W:
                if not self.player2.collides_with_list(self.walls):
                    self.player2_speed = SPEED
                else:
                    self.player2_speed = 0
            if symbol == arcade.key.S:
                if not self.player2.collides_with_list(self.walls):
                    self.player2_speed = -SPEED
                else:
                    self.player2_speed = 0


    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.UP, arcade.key.DOWN):
            self.player_speed = 0
        if symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_angle = 0 
        
        if symbol in (arcade.key.W, arcade.key.S):
            self.player2_speed = 0
        if symbol in (arcade.key.A, arcade.key.D):
            self.player2.change_angle = 0 

    def on_update(self, delta_time: float):
        """Metodo para actualizar objetos de la app"""
        if not self.paused:
            self.player.center_x += -self.player_speed * math.sin(math.radians(self.player.angle))
            self.player.center_y += self.player_speed * math.cos(math.radians(self.player.angle))

            self.player2.center_x += -self.player2_speed * math.sin(math.radians(self.player2.angle))
            self.player2.center_y += self.player2_speed * math.cos(math.radians(self.player2.angle))

            # Evitar que los jugadores se salgan de la pantalla
            if self.player.center_x < 0:
                self.player.center_x = 0
            if self.player.center_x > SCREEN_WIDTH:
                self.player.center_x = SCREEN_WIDTH
            if self.player.center_y < 0:
                self.player.center_y = 0
            if self.player.center_y > SCREEN_HEIGHT:
                self.player.center_y = SCREEN_HEIGHT

            if self.player2.center_x < 0:
                self.player2.center_x = 0
            if self.player2.center_x > SCREEN_WIDTH:
                self.player2.center_x = SCREEN_WIDTH
            if self.player2.center_y < 0:
                self.player2.center_y = 0
            if self.player2.center_y > SCREEN_HEIGHT:
                self.player2.center_y = SCREEN_HEIGHT

            # Colisión de jugadores con paredes
            for wall in self.walls:
                if self.player.collides_with_sprite(wall):
                    self.player_speed = 0
                    if self.player_speed > 0:
                        self.player.center_y -= 5
                    elif self.player_speed < 0:
                        self.player.center_y += 5
                    break
    
                if self.player2.collides_with_sprite(wall):
                    self.player2_speed = 0
                    if self.player2_speed > 0:
                        self.player2.center_y -= 5
                    elif self.player2_speed < 0:
                        self.player2.center_y += 5
                    break

             # Verificar si el jugador colisionó con algún enemigo
            for enemy in self.enemies:
                if self.player.collides_with_sprite(enemy):
                    self.player1_wins = False
                    self.game_over = True
                    self.paused = True
                    break

                if self.player2.collides_with_sprite(enemy):
                    self.player1_wins = True
                    self.game_over = True
                    self.paused = True
                    break

            #Colision de bala con enemigo

            for bullet2 in self.bullets2:
                if self.player.collides_with_sprite(bullet2):
                    self.player1_wins = False
                    self.game_over = True
                    self.paused = True
                    break

            for bullet in self.bullets:
                if self.player2.collides_with_sprite(bullet):
                    self.player1_wins = True
                    self.game_over = True
                    self.paused = True
                    break

            #Comprobamos si las balas colicionan con la pared

            for bullet in self.bullets:
                if bullet.collides_with_list(self.walls):
                    bullet.remove_from_sprite_lists()

            for bullet2 in self.bullets2:
                if bullet2.collides_with_list(self.walls):
                    bullet2.remove_from_sprite_lists()

            self.update_bullets()
            self.update_bullets2()
            self.update_enemies()
            self.update_enemies2()
            self.sprites.update()

    def on_draw(self):
        """Metodo para dibujar en la pantalla"""
        arcade.start_render()
        self.sprites.draw()
        arcade.draw_text(
            f"Minas eliminadas player 1: {self.score}",
            700,
            35,
            arcade.color.DARK_RED,
            15,
            width=SCREEN_WIDTH,
            align="left"
        )

        arcade.draw_text(
            f"Minas eliminadas player 2: {self.score2}",
            35,
            35,
            arcade.color.DARK_RED,
            15,
            width=SCREEN_WIDTH,
            align="left"
        )

        # Dibujar las paredes
        self.walls.draw()

        # Si el juego terminó, mostrar la pantalla de Game Over
        if self.game_over:
            if self.player1_wins:
                arcade.draw_text(
                    "Game Over Player 1 Wins",
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2,
                    arcade.color.WHITE,
                    30,
                    anchor_x="center",
                    anchor_y="center"
                )
            else:
                arcade.draw_text(
                    "Game Over Player 2 Wins",
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2,
                    arcade.color.WHITE,
                    30,
                    anchor_x="center",
                    anchor_y="center"
                ) 

    def update_bullets(self):
        for b in self.bullets:
            if b.top > SCREEN_HEIGHT or b.bottom < 0 or b.left < 0 or b.right > SCREEN_WIDTH:
                b.remove_from_sprite_lists()

    def update_bullets2(self):
        for b in self.bullets2:
            if b.top > SCREEN_HEIGHT or b.bottom < 0 or b.left < 0 or b.right > SCREEN_WIDTH:
                b.remove_from_sprite_lists()

    def update_enemies(self):
        for e in self.enemies:
            if e.collides_with_list(self.bullets):
                e.remove_from_sprite_lists()
                self.score += 1
                b_list = arcade.check_for_collision_with_list(e, self.bullets)
                for b in b_list:
                    b.remove_from_sprite_lists()

    def update_enemies2(self):
        for e in self.enemies:
            if e.collides_with_list(self.bullets2):
                e.remove_from_sprite_lists()
                self.score2 += 1
                b_list = arcade.check_for_collision_with_list(e, self.bullets2)
                for b in b_list:
                    b.remove_from_sprite_lists()

    def add_enemy(self, delta_time: float):
        if not self.paused:
            #enemy = arcade.SpriteSolidColor(30, 30, arcade.color.BLACK)
            enemy = arcade.Sprite("img/mina.png", SCALING)
            enemy.left = random.randint(10, SCREEN_WIDTH - 10)
            enemy.top = random.randint(10, SCREEN_HEIGHT - 10)
            self.enemies.append(enemy)
            self.sprites.append(enemy)


if __name__ == "__main__":
    app = App()
    arcade.run()