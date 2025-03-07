class EnemyDirector:
    def construct_enemy(self, builder, enemy_type="normal"):

        builder.reset()
        builder.set_position()

        if enemy_type == "normal":
            builder.set_sprite("../assets/images/enemy.png")
            builder.set_speed(2)
        elif enemy_type == "fast":
            builder.set_sprite("../assets/images/red.png")
            builder.set_speed(10)
        elif enemy_type == "strong":
            builder.set_sprite("../assets/images/green.png")
            builder.set_speed(1)

        return builder.get_enemy()
