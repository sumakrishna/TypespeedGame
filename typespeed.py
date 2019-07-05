import pygame as pg
import random
from pygame import mixer
from os import path
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
pg.init()

WIDTH = 990
HEIGHT = 480
SCORE = 0
HIGHSCORE = 0
MISSES = 0
LEVEL = 1
LENGTH = 0
angle = 0
inc = 0
time_elapsed_since_last_action = 0
pos_list = []
screen = pg.display.set_mode((WIDTH, HEIGHT))
font = pg.font.Font(None, 32)
wordsfile = open("sowpods.txt", "r")
textlist = [line.strip().lower() for line in wordsfile.readlines() if len(line.strip()) == 3]
levelTextList = []  
clock = pg.time.Clock()
color = pg.Color('dodgerblue2')
typedword = ''
img_dir = path.join(path.dirname(__file__), 'img')
font_name = pg.font.match_font('arial')
HS_FILE=r"C:\Users\suma mounika\Appdata\Local\Programs\Python\Python36-32\highscore.txt"
pg.mixer.music.load("Fantasy_Game_Background.mp3")
pg.mixer.music.play()
background = pg.image.load(path.join(img_dir, "coudsParallaxmmm2.png")).convert()
background = pg.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
'''play = pg.image.load(path.join(img_dir, "play.png")).convert()
play = pg.transform.scale(play, (40, 20))
play_rect = play.get_rect()
pause = pg.image.load(path.join(img_dir, "pause.png")).convert()
pause = pg.transform.scale(play, (40, 20))
pause_rect = pause.get_rect()'''
#screen.blit(pause, (800, 20))

def removeWord(word):
    global pos_list
    for i in pos_list:
        if i[0] == word:
            pos_list.remove(i)
        

def genWords():
    global pos_list
    word = random.choice(textlist)
    textlist.remove(word)
    levelTextList.append(word)
    font = pg.font.Font(None, 32)
    image = font.render(word, True, (255, 255, 255))
    text_rect = image.get_rect()
    text_rect.x = random.randrange(-100, -40)
    text_rect.y = random.randrange(50, HEIGHT - 50, 50)
    text2, textsurf, textpos = [word, image, [text_rect.x, text_rect.y]]
    pos_list += [[text2, textsurf, textpos]]
    screen.blit(textsurf, textpos)
    
sched.add_job(genWords, 'interval', seconds = 0.5)
sched.start()

def updatePosition():
    global angle
    global MISSES
    global pos_list
    global levelTextList
    for i in pos_list:
        i[2][0] += random.randrange(4, 15, 4)
        if i[2][0] > WIDTH:
            MISSES += 1
            levelTextList.remove(i[0])
            pos_list.remove(i)
        if LEVEL in range(3, 4):
            angle += 1
            rotated_surface = pg.transform.rotate(i[1], angle)
            rect = rotated_surface.get_rect(x = i[2][0], y = i[2][1])
            screen.blit(rotated_surface, (rect.x, rect.y))
        else:
            screen.blit(i[1], (i[2][0], i[2][1]))



def drawText(surf, text, size, x, y, color):
    font = pg.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x = x
    text_rect.y = y
    surf.blit(text_surface, text_rect)            
    
def showGameOverScreen():
    textlist = [line.strip().lower() for line in wordsfile.readlines() if len(line.strip()) == 3]
    screen.blit(background, background_rect)
    drawText(screen, "GAME OVER!!!", 64, WIDTH / 3, HEIGHT / 4, (255, 255, 255))
    drawText(screen, "Press a key to RESTART", 18, 400, HEIGHT / 2, (255, 255, 255))
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(10)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sched.shutdown()
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False
                

def showLevelCompletedScreen():
    global textlist
    global levelTextList
    screen.blit(background, background_rect)
    drawText(screen, "LEVEL " + str(LEVEL) + " COMPLETED!!!", 64, WIDTH / 3, HEIGHT / 4, (255, 255, 255))
    drawText(screen, "Press a key to RESTART", 18, 400, HEIGHT / 2, (255, 255, 255))
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(10)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sched.shutdown()
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False


        
 
    
    

         
GAMEOVER = False
playing = True 

while playing:
    if GAMEOVER:
        SCORE = 0
        MISSES = 0
        LEVEL = 1
        showGameOverScreen()
        GAMEOVER = False
        levelTextList.clear()
        pos_list.clear()
        
    if SCORE >= LEVEL * 50 and MISSES < 10:
        showLevelCompletedScreen()
        LEVEL += 1
        if LEVEL % 2 == 0:
            LENGTH += 1
            textlist += [line.strip().lower() for line in wordsfile.readlines() if len(line.strip()) == 3 + LENGTH]
        
    clock.tick(10)
    cur = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sched.shutdown()
            pg.quit()
        '''if (800 + 50 > cur[0] > 800 and 20 + 30 > cur[1] > 20) and pg.mouse.get_pressed()[0]:
            inc += 1
            button()'''
        if typedword in levelTextList:
            SCORE += 10
            removeWord(typedword)
            levelTextList.remove(typedword)
            typedword = ''
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                typedword = typedword[:-1]
            else:
                typedword += event.unicode

    
    screen.fill((255, 255, 255))
    screen.blit(background, background_rect)
    #pg.draw.rect(screen, (0, 120, 0), (800, 20, 50, 30))
    #button()
    pg.draw.rect(screen, (255, 0, 0), pg.Rect(5, 440, 250, 35), 1)
    drawText(screen, "SCORE: " + str(SCORE), 32, 300, 450, (0, 0, 0))
    drawText(screen, typedword, 32, 10, 450, (0, 0, 0))
    drawText(screen, "MISSES : " + str(MISSES), 32, 700, 450, (0, 0, 0))

    
     
    if MISSES == 10:
       GAMEOVER = True
    if SCORE > HIGHSCORE:
        HIGHSCORE = SCORE
        with open(path.join(dir , HS_FILE) , "w") as f:
            f.write(str(SCORE))
    else:
        txt_surface1 = font.render("HIGH SCORE : " + str(HIGHSCORE) , True, (0, 0, 0))
        screen.blit(txt_surface1, (440, 450))
    dir = path.dirname(r"C:\Users\suma mounika\Appdata\Local\Programs\Python\Python36-32")
    with open(path.join(dir , HS_FILE), 'r') as f:
        try:
            HIGHSCORE = int(f.read())
        except:
            HIGHSCORE = 0
    updatePosition()
    pg.display.flip()
    


