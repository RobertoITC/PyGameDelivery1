class EnemyDirector:
    def construct_enemy(self, builder, enemy_type):
        builder.reset()

        # NUEVOS TIPOS PARA CENTIPEDE
        if enemy_type == "centipede_head":
            builder.set_sprite("../assets/images/centipede_head.png")
            builder.set_speed(5)
            builder.set_health(1)
            builder.set_is_head(True)    # <-- Usar un flag en el builder

        elif enemy_type == "centipede_body":
            builder.set_sprite("../assets/images/centipede_body.png")
            builder.set_speed(5)
            builder.set_health(1)
            builder.set_is_head(False)

        elif  enemy_type == "normal":
            builder.set_sprite("../assets/images/green.png")
            builder.set_speed(8)
            builder.set_health(2)
            builder.set_behavior("normal")
        elif enemy_type == "fast":
            builder.set_sprite("../assets/images/red.png")
            builder.set_speed(15)
            builder.set_health(1)
            builder.set_behavior("normal")

        elif enemy_type == "strong":
            builder.set_sprite("../assets/images/enemy.png")
            builder.set_speed(2)
            builder.set_health(3)
            builder.set_behavior("normal")

        return builder.get_enemy()