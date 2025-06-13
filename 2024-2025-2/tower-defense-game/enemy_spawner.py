from enemy import Enemy

class EnemySpawner:
    def __init__(self, path, spawn_rate=1000, max_enemies=10):
        self.path = path
        self.spawn_rate = spawn_rate
        self.max_enemies = max_enemies
        self.spawn_timer = 0
        self.enemies = []

    def update(self, dt):
        killed = 0
        leaked = 0

        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.hp <= 0:
                killed += 1
            elif enemy.reached_end:
                leaked += 1

        self.enemies = [e for e in self.enemies if not e.reached_end]

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate and len(self.enemies) < self.max_enemies:
            self.enemies.append(Enemy(self.path))
            self.spawn_timer = 0

        return killed, leaked

    def draw(self, screen):
        for e in self.enemies:
            e.draw(screen)

