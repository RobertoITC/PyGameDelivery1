def check_collision(bullet, enemy):
    return enemy.x < bullet.x < enemy.x + 40  and enemy.y < bullet.y < enemy.y + 40