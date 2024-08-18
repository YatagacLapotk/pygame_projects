import pygame

WIDTH,HEIGHT = 900,900

def x_drawer(surf:pygame.Surface,x,rectangle:pygame.Rect)->pygame.Rect:   
    pygame.Surface.blit(surf,x,rectangle)
    
def o_drawer(surf:pygame.Surface,o,rectangle:pygame.Rect)->pygame.Rect:  
    pygame.Surface.blit(surf,o,rectangle)


def draw_winnner(screen,text,drawns):
    isdraw = 0
    for i in range(3):
        sumh,sumv,sumcross1,sumcross2=0,0,0,0
        for j in range(3):
            sumcross1 += drawns[j][j]
            if i+j==2:
                sumcross2+=drawns[i][j]
            sumh+= drawns[i][j]
            sumv+= drawns[j][i]
            if drawns[i][j]!=0:
                isdraw+=1
        if sumh ==3 or sumv==3 or sumcross1==3 or sumcross2==3:
            text = "Payer x wins"
            break
        if sumh ==-3 or sumv==-3 or sumcross1==-3 or sumcross2==-3:
            text = "Player o wins"
            break
    if isdraw==9:
        text="Draw!"
    draw_winner2(screen,text)


def draw_exit(screen):
    exit_rect = pygame.Rect(320,500,200,200) 
    pygame.draw.rect(screen,"white",exit_rect)
    menu = pygame.font.SysFont("comicsans",100)
    text = menu.render("Exit",1,"black")
    text_rect = text.get_rect(center=(exit_rect.center))
    screen.blit(text,text_rect)
    return exit_rect


def draw_start(screen):
    start_rect = pygame.Rect(320,200,200,200) 
    pygame.draw.rect(screen,"white",start_rect)
    menu = pygame.font.SysFont("comicsans",100)
    text = menu.render("Start",1,"black")
    text_rect = text.get_rect(center=(start_rect.center))
    screen.blit(text,text_rect)
    return start_rect

def draw_winner2(screen,text):
    if text!="":    
        winner_rect = pygame.Rect(140,320,600,200) 
        pygame.draw.rect(screen,"black",winner_rect)
        menu = pygame.font.SysFont("comicsans",100)
        text1 = menu.render(text,1,"blue")
        text1_rect = text1.get_rect(center=(winner_rect.center))
        screen.blit(text1,text1_rect)
    
def xox():   
    screen = pygame.display.set_mode((900, 900))
    clock = pygame.time.Clock()
    running = True
    screen.fill("purple")
    text = ""
    drawns = [[0 for _ in range(3)] for _ in range(3)]
    rects = [[[]for k in range(3)] for _ in range(3)]
    player_select = 0
    xs = pygame.image.load("/Users/yatagaclapotk/Desktop/Genel Çalişmalar/pygame/xox/images/x_image.png").convert()
    x = pygame.transform.scale(xs,[225,225])
    os = pygame.image.load("/Users/yatagaclapotk/Desktop/Genel Çalişmalar/pygame/xox/images/o_image.png").convert()
    o = pygame.transform.scale(os,[225,225])


    a=0
    for i in range(3):
        b = 0 
        for j in range(3): 
            rects[i][j]= pygame.draw.rect(screen,"yellow",pygame.Rect(75+a,75+b,225,225))
            b+=250
        a+=250 
    
    while running:
        mos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(3):
                    for j in range(3):
                        if pygame.Rect.collidepoint(rects[i][j],mos[0],mos[1]):
                            if pygame.mouse.get_pressed()[0]==True and player_select%2==0 and drawns[i][j] == 0:
                                x_drawer(screen,x,rects[i][j])
                                drawns[i][j] = 1 
                                pygame.time.delay(200)
                                player_select+=1
                            elif pygame.mouse.get_pressed()[0]==True and player_select%2==1 and drawns[i][j]==0:
                                o_drawer(screen,o,rects[i][j])
                                pygame.time.delay(200)
                                drawns[i][j] = -1
                                player_select+=1

        draw_winnner(screen,text,drawns)                       
        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

def main(text):
    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    screen.fill("blue")
    pygame.display.set_caption("XOX")
    clock=pygame.time.Clock()
    start_button = draw_start(screen)
    exit_button = draw_exit(screen)
    run = True
    if text!="":  
        draw_winner2(screen,text)
    while run:
        mos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mos):  
                    xox()
                if exit_button.collidepoint(mos):  
                    run= False 
        clock.tick(60)
        pygame.display.flip()
if __name__=="__main__":
    main("")

pygame.quit()