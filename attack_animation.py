import arcade

SPRITE_SCALE = 0.5
ATTACK_SPEED = 5


def load_sprite(attack, is_player):
    if attack == "rock":
        path = "assets/srock-attack.png"
    elif attack == "paper":
        path = "assets/spaper-attack.png"
    elif attack == "scissors":
        path = "assets/scissors-close.png"
    else:
        path = "assets/compy.png"

    sprite = arcade.Sprite(path, SPRITE_SCALE)
    if is_player:
        sprite.center_x = 150
    else:
        sprite.center_x = 850
        sprite.angle = 180
    sprite.center_y = 300
    return sprite


class AttackAnimation:
    def __init__(self, player_attack, computer_attack):
        self.player_attack = player_attack
        self.computer_attack = computer_attack

        self.player_sprite = load_sprite(player_attack, True)
        self.computer_sprite = load_sprite(computer_attack, False)

        self.is_animation_done = False

    def update(self):
        if self.player_sprite.center_x < 400:
            self.player_sprite.center_x += ATTACK_SPEED
        if self.computer_sprite.center_x > 600:
            self.computer_sprite.center_x -= ATTACK_SPEED
        if self.player_sprite.center_x >= 400 and self.computer_sprite.center_x <= 600:
            self.is_animation_done = True

    def draw(self):
        self.player_sprite.draw()
        self.computer_sprite.draw()
