from enemy import Enemy

class EnemySpawner:
    def __init__(self, path, spawn_rate=1000, max_enemies=10):
        self.path = path
        self.spawn_rate = spawn_rate
        self.max_enemies = max_enemies
        self.spawn_timer = 0
        self.enemies = []

    def update(self, dt):
        for enemy in self.enemies:
            enemy.update()

        self.enemies = [e for e in self.enemies if not e.reached_end]

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate and len(self.enemies) < self.max_enemies:
            self.enemies.append(Enemy(self.path))
            self.spawn_timer = 0

    def draw(self, screen):
        for e in self.enemies:
            e.draw(screen)

