import arcade
import random
from enum import Enum

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche Papier Ciseaux"


class GameState(Enum):
    NOT_STARTED = 0
    ROUND_ACTIVE = 1
    ROUND_DONE = 2
    GAME_OVER = 3


class AttackType(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.DARK_SEA_GREEN)

        self.game_state = GameState.NOT_STARTED
        self.player_score = 0
        self.computer_score = 0

        self.player_attack_type = None
        self.computer_attack_type = None
        self.attack_animation = None

        self.rock = arcade.Sprite("assets/srock.png", 0.5)
        self.paper = arcade.Sprite("assets/spaper.png", 0.5)
        self.scissors = arcade.Sprite("assets/scissors.png", 0.5)

        self.rock.center_x = 200
        self.rock.center_y = 150

        self.paper.center_x = 400
        self.paper.center_y = 150

        self.scissors.center_x = 600
        self.scissors.center_y = 150

        self.result_text = ""

    def setup(self):
        self.game_state = GameState.NOT_STARTED
        self.player_score = 0
        self.computer_score = 0
        self.player_attack_type = None
        self.computer_attack_type = None
        self.attack_animation = None
        self.result_text = ""

    def on_draw(self):
        self.clear()

        arcade.draw_text("ROCHE, PAPIER, CISEAUX", 200, 550, arcade.color.WHITE, 30)

        arcade.draw_text(f"Score Joueur: {self.player_score}", 20, 560, arcade.color.GREEN, 18)
        arcade.draw_text(f"Score Ordinateur: {self.computer_score}", 600, 560, arcade.color.RED, 18)

        self.rock.draw()
        self.paper.draw()
        self.scissors.draw()

        if self.game_state == GameState.NOT_STARTED:
            arcade.draw_text("Appuie sur ESPACE pour commencer", 250, 400, arcade.color.WHITE, 24)
        elif self.game_state == GameState.ROUND_ACTIVE:
            arcade.draw_text("Choisis ton attaque en cliquant une image", 200, 400, arcade.color.WHITE, 18)
        elif self.game_state == GameState.ROUND_DONE:
            arcade.draw_text(self.result_text, 300, 400, arcade.color.YELLOW, 24)
            arcade.draw_text("Appuie sur ESPACE pour continuer", 260, 350, arcade.color.WHITE, 18)
        elif self.game_state == GameState.GAME_OVER:
            arcade.draw_text(self.result_text, 300, 400, arcade.color.YELLOW, 24)
            arcade.draw_text("Appuie sur ESPACE pour recommencer", 260, 350, arcade.color.WHITE, 18)

        if self.attack_animation and not self.attack_animation.is_animation_done:
            self.attack_animation.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.game_state == GameState.NOT_STARTED:
                self.game_state = GameState.ROUND_ACTIVE
            elif self.game_state == GameState.ROUND_DONE:
                self.game_state = GameState.ROUND_ACTIVE
                self.player_attack_type = None
                self.computer_attack_type = None
                self.attack_animation = None
            elif self.game_state == GameState.GAME_OVER:
                self.setup()
                self.game_state = GameState.ROUND_ACTIVE

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_state != GameState.ROUND_ACTIVE:
            return

        if self.rock.collides_with_point((x, y)):
            self.player_attack_type = AttackType.ROCK
        elif self.paper.collides_with_point((x, y)):
            self.player_attack_type = AttackType.PAPER
        elif self.scissors.collides_with_point((x, y)):
            self.player_attack_type = AttackType.SCISSORS
        else:
            return

        pc_attack = random.randint(0, 2)
        self.computer_attack_type = AttackType(pc_attack)

        self.determine_winner()

        self.game_state = GameState.ROUND_DONE

    def determine_winner(self):
        p = self.player_attack_type
        c = self.computer_attack_type

        if p == c:
            self.result_text = "Égalité"
        elif (p == AttackType.ROCK and c == AttackType.SCISSORS) or \
                (p == AttackType.PAPER and c == AttackType.ROCK) or \
                (p == AttackType.SCISSORS and c == AttackType.PAPER):
            self.player_score += 1
            self.result_text = "Tu gagnes cette manche"
        else:
            self.computer_score += 1
            self.result_text = "L'ordinateur gagne cette manche"

        if self.player_score >= 3:
            self.result_text = "Tu as gagné la partie"
            self.game_state = GameState.GAME_OVER
        elif self.computer_score >= 3:
            self.result_text = "L'ordinateur a gagné la partie"
            self.game_state = GameState.GAME_OVER

    def on_update(self, delta_time):
        if self.attack_animation and not self.attack_animation.is_animation_done:
            self.attack_animation.update(delta_time)


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
