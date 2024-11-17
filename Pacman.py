import pygame
import random
pygame.init()

clock=pygame.time.Clock()
size=(800,800)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Pac Man")
done=False
f=open("Maze.txt","r")

pygame.font.init()
font = pygame.font.SysFont('calibri', 46)
score = -1

blocks = []
balls = []
for i in range(20):
    b = f.readline()
    for p in range(20):
        block_position = (40 * p, 40 * i)
        if b[p] == "1":
            blocks.append(block_position)
        else:
            balls.append(block_position)
f.seek(0)
                

WHITE=(255,255,255)
BLUE=(0,0,255)
LBLUE=(170,170,255)
BLACK=(0,0,0)
YELLOW=(255,255,0)
RED = (255,0,0)
GREEN = (0, 255, 0)

class Player():
    def __init__(self):
        self.color=(YELLOW)
        self.y=480
        self.x=400
        self.can_kill = False  
        self.power_up_time = 0
        
    def draw(self):
        pygame.draw.ellipse(screen,self.color,[self.x, self.y, 40,40],0)
class Enemy():
    def __init__(self, x, y):
        self.color = RED
        self.x = x
        self.y = y
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.move_counter = 0

    def can_move(self, direction):
        if direction == 'up':
            target = (self.x, self.y - 40)
        elif direction == 'down':
            target = (self.x, self.y + 40)
        elif direction == 'left':
            target = (self.x - 40, self.y)
        elif direction == 'right':
            target = (self.x + 40, self.y)
        return target not in blocks

    def move(self):
        if self.move_counter % 20 == 0:
            if self.can_move(self.direction):
                if self.direction == 'up':
                    self.y -= 40
                elif self.direction == 'down':
                    self.y += 40
                elif self.direction == 'left':
                    self.x -= 40
                elif self.direction == 'right':
                    self.x += 40
            else:
                self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.move_counter += 1

    def draw(self):
        pygame.draw.ellipse(screen, self.color, [self.x, self.y, 40, 40], 0) 
class Fruit():
    def __init__(self):
        self.color = GREEN
        self.x, self.y = self.spawn_fruit()

    def spawn_fruit(self):
        while True:
            x = random.randint(0, 19) * 40
            y = random.randint(0, 19) * 40
            if (x, y) not in blocks:
                return x, y

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + 20, self.y + 20), 10)
   
def spawn_enemy():
    while True:
        x = random.randint(0, 19) * 40
        y = random.randint(0, 19) * 40
          
        if (x, y) not in blocks:
            return Enemy(x, y)

def load_high_score():
    with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    return high_score

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

high_score = load_high_score()

player = Player()
fruits = [Fruit() for _ in range(3)]
enemies = [spawn_enemy() for _ in range(3)]

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if (player.x+40, player.y) not in blocks:
                    player.x+=40
            elif event.key == pygame.K_LEFT:
                if (player.x-40, player.y) not in blocks:
                    player.x +=-40
            elif event.key ==pygame.K_DOWN:
                if (player.x, player.y+40) not in blocks:
                    player.y+=40
            elif event.key == pygame.K_UP:
                if (player.x, player.y-40) not in blocks:
                    player.y+=-40
        elif event.type == pygame.KEYUP:
            pass
    
    if player.can_kill:
            player.power_up_time -= 1
            if player.power_up_time <= 0:
                player.can_kill = False

    player_position = (player.x, player.y)
    if player_position in balls:
        balls.remove(player_position)
        score+=1
    
    for fruit in fruits[:]:
        if player_position == (fruit.x, fruit.y):
            player.can_kill = True
            player.power_up_time = 300
            fruits.remove(fruit)

    if player.can_kill == True:
        for enemy in enemies[:]:
            enemy.color=LBLUE
    else:
        for enemy in enemies[:]:
            enemy.color=RED

    for enemy in enemies[:]:
        if player_position == (enemy.x, enemy.y):
            if player.can_kill:
                enemies.remove(enemy)
            else:
                done = True
    
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    screen.fill(BLACK)
    for ball in balls:
        pygame.draw.circle(screen, WHITE, (ball[0] + 20, ball[1] + 20), 5)
    for i in range(0,20):
        b= f.readline()
        for p in range(0,20):
            if b[p]== "1":
                pygame.draw.rect(screen,BLUE,[0+(40*(p//1)),0+(40*i),40,40],0)
    f.seek(0)
    player.draw()
    for enemy in enemies:
        enemy.move()
        enemy.draw()
    for fruit in fruits:
        fruit.draw()
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (509, 0))
    pygame.display.flip()
    clock.tick(60)
    
