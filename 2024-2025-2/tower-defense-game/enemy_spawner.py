from enemy import Enemy

class EnemySpawner:
    def __init__(self, path, spawn_interval=1000, enemies_per_wave=10):
        self.path = path
        self.spawn_interval = spawn_interval
        self.enemies_per_wave = enemies_per_wave

        self.spawn_timer = 0
        self.enemies_spawned = 0
        self.enemies = []
        self.wave_active = True

    def start_wave(self, wave_number):
        self.enemies_spawned = 0
        self.enemies = []
        self.wave_active = True
        self.enemies_per_wave = 10 + wave_number * 3
        self.spawn_interval = max(300, 1000 - wave_number * 100)  # min 300ms

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

        self.enemies = [e for e in self.enemies if not e.reached_end and e.hp > 0]

        self.spawn_timer += dt
        if self.enemies_spawned < self.enemies_per_wave and self.spawn_timer >= self.spawn_interval:
            self.enemies.append(Enemy(self.path))
            self.enemies_spawned += 1
            self.spawn_timer = 0

        if self.enemies_spawned >= self.enemies_per_wave and len(self.enemies) == 0:
            self.wave_active = False  # wave finished

        return killed, leaked

    def draw(self, screen):
        for e in self.enemies:
            e.draw(screen)

