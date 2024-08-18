import pygame
import random as r

WIDTH = 700
HEIGHT = 400
MOVESPEED = 10
BALLSPEED = [4,4]
BALLSIZE = 20
PLAYERW = 20
PLAYERH = 60

halfsideimgs = pygame.image.load("/Users/yatagaclapotk/Desktop/Genel Çalişmalar/pygame/pong/images/halfside.png")
halfsidimg = pygame.transform.scale(halfsideimgs,(halfsideimgs.get_width(),HEIGHT))
ballimgs = pygame.image.load("/Users/yatagaclapotk/Desktop/Genel Çalişmalar/pygame/pong/images/ball.png")
ballimg = pygame.transform.scale(ballimgs,(BALLSIZE,BALLSIZE))
playerimgs = pygame.image.load("/Users/yatagaclapotk/Desktop/Genel Çalişmalar/pygame/pong/images/player.png")
playerimg = pygame.transform.scale(playerimgs,(PLAYERW,PLAYERH))

def set_it_right(number,bottom,upper):
    if number<=bottom:
        return bottom
    elif number >= upper:
        return upper
    else:
        return number

class Player:
    def __init__(self,name) -> None:
        self.name = name
        self.position = pygame.math.Vector2(0,0)
        self.goal = 0
        self.direction = 0
    def goal_conceded(self):
        self.goal+=1
        goal_sound = pygame.mixer.Sound("/Users/yatagaclapotk/Desktop/Genel Çalişmalar/pygame/pong/sounds/goal.mp3")
        goal_sound.play()
    def won(self):
        if self.goal==10:
            return True
        else:
            return False
    def set_position(self,x,y):
        self.position.update(x,y)
    def set_direction(self,ins):
        if ins == "UP":
            self.direction = -1
        if ins == "DOWN":
            self.direction = 1
        if ins == "":
            self.direction = 0
    def move(self):
        speed = self.direction *MOVESPEED
        self.position.update(self.position.x,set_it_right(self.position.y+speed,20,HEIGHT-80))
            
class Ball:
    def __init__(self) -> None:
        self.position = pygame.math.Vector2(WIDTH//2,HEIGHT//2)
        self.velocity =[r.choice([-5,-4,-3,3,4,5]),r.randint(-4,4)]
    def set_position(self,x,y):
        self.position.update(x,y)
    def bounce_walls(self):
        self.velocity[0] = r.choice([x for x in [-5,-4,-3,3,4,5] if self.velocity[0]*x>0]) 
        self.velocity[1] = -self.velocity[1] 
    def bounce_player(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = r.randint(-4,4)
    def move(self):
        self.position.update(self.position.x + self.velocity[0],self.position.y + self.velocity[1])

def draw_player(screen,player:Player):
    player_rect = pygame.Rect(player.position.x,player.position.y,PLAYERW,PLAYERH)
    pygame.draw.rect(screen,"white",player_rect)
    screen.blit(playerimg,player_rect)
    return player_rect

def draw_ball(screen,ball:Ball):
    ball_rect = pygame.Rect(ball.position.x-ballimg.get_width()/2,ball.position.y-ballimg.get_height()/2,BALLSIZE,BALLSIZE)
    pygame.draw.rect(screen,"white",ball_rect)
    screen.blit(ballimg,ball_rect)
    return ball_rect

def draw_winner(screen:pygame.Surface,player:Player,ball:Ball):
    screen.fill("black")
    font = pygame.font.SysFont("comicsans",36)
    text = font.render(f""" {player.name} wins! Game over!!!""",1,"white")
    screen.blit(text,(WIDTH//2-text.get_width()/2,HEIGHT//2-text.get_height()/2))
    ball.velocity = [0,0]

def draw_begin(player1:Player,player2:Player,ball:Ball,screen:pygame.Surface):
    player1.set_position(WIDTH-30,HEIGHT//2-30)
    player2.set_position(10,HEIGHT//2-30)
    ball.set_position(WIDTH//2,HEIGHT//2)
    ball.velocity = [r.choice([-5,-4,-3,3,4,5]),r.randint(-4,4)]

def draw_goal(screen:pygame.Surface,player:Player,x,y):
    font = pygame.font.Font("/Users/yatagaclapotk/Desktop/Genel Çalişmalar/pygame/pong/pong-score/pong-score.ttf",40)
    text = font.render(f"""{player.goal}""",1,"white")
    screen.blit(text,(x,y))



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()
    run = True 
    player1 = Player("Player1")
    player2 = Player("Player2")
    ball = Ball()   
    draw_begin(player1,player2,ball,screen)
    while run:
        screen.fill("black")
        screen.blit(halfsidimg,(WIDTH//2-halfsidimg.get_width(),0))
        player1_rect = draw_player(screen,player1)
        player2_rect = draw_player(screen,player2)
        ball_rect = draw_ball(screen,ball)
        draw_goal(screen,player1,WIDTH//2-35,30)
        draw_goal(screen,player2,WIDTH//2+10,30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player1.set_direction("UP")
                if event.key == pygame.K_DOWN:
                    player1.set_direction("DOWN")
                if event.key == pygame.K_w:
                    player2.set_direction("UP")
                if event.key == pygame.K_s:
                    player2.set_direction("DOWN")
            if event.type == pygame.KEYUP:
                player1.set_direction("")
                player2.set_direction("")
        if ball.position.y >= HEIGHT or ball.position.y <= 0:
            ball.bounce_walls()
            wall_sound = pygame.mixer.Sound("/Users/yatagaclapotk/Desktop/Genel Çalişmalar/pygame/pong/sounds/wall.mp3")
            wall_sound.play()
        if ball_rect.colliderect(player1_rect) or ball_rect.colliderect(player2_rect):
            ball.bounce_player()
            player_sound = pygame.mixer.Sound("/Users/yatagaclapotk/Desktop/Genel Çalişmalar/pygame/pong/sounds/player.mp3")
            player_sound.play()
        if ball.position.x >= WIDTH:
            player1.goal_conceded()
            draw_begin(player1,player2,ball,screen)
        if ball.position.x <= 0:
            player2.goal_conceded()
            draw_begin(player1,player2,ball,screen)
        if player1.won():
            draw_winner(screen,player1,ball)
        if player2.won():
            draw_winner(screen,player2,ball)

        player1.move()
        player2.move()
        ball.move()
        clock.tick(60)
        pygame.display.flip()
if __name__== "__main__":
    main()
    