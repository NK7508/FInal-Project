'''
Student Name: Neil Kakkassery
Game title: Pool game
Period: 6 
Features of Game: play 8 ball, 2 player, choose power and angle. Winner decided by normal 8 ball rules
'''

import pygame, sys, box2d-py, random                                   
pygame.init()                                           #initialize game engine

w=1000                                                    #set window size
h=800                                                   
size=(w,h)
surface = pygame.display.set_mode(size)

pygame.display.set_caption("Kakkassery Pool")          # window title

#declare global variables here

BLACK    = (   0,   0,   0)                             #Color Constants 
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
ORANGE   = ( 242, 169, 26)
YELLOW   = ( 219, 226, 6)
BROWN    = (150, 100, 50)
GREY     = (128, 128, 128)
DARK_GREY = (38,38,38)


#other global variables (WARNING: use sparingly):
xu = w/32
yu = h/32


tableImg = pygame.image.load('Images/table.png') 
tableRect = pygame.Rect(-20, 120, 800, 500)

stickImg = pygame.image.load('Images/stick.png') 

playImg = pygame.image.load('Images/play .png')
playRect = pygame.Rect(w/4 -80,h-150,250,99)

infoImg = pygame.image.load('Images/info .png')
infoRect = pygame.Rect(w*(3/4)-220,h-150,250,99)

exitImg = pygame.image.load('Images/exit .png') 
exitRect = pygame.Rect(w*(3/4)-30,h-120,220,89)
playExitRect = pygame.Rect(w/2-150,650,220,89)

name1Rect = pygame.Rect (w/2 - 60,h/4 + 100,260,25)
name2Rect = pygame.Rect(w/2 - 60,h*(3/4),260,25)

cue = pygame.image.load("Images/balls/Cue.png")
cueRect = pygame.Rect(180,400,25,25)

ball1 = pygame.image.load("Images/balls/1.png")
ball1Rect = pygame.Rect(600,400,25,25)

ball2 = pygame.image.load("Images/balls/2.png")
ball2Rect = pygame.Rect(620,412,25,25)

ball3 = pygame.image.load("Images/balls/3.png")
ball3Rect = pygame.Rect(640,424,25,25)

ball4 = pygame.image.load("Images/balls/4.png")
ball4Rect = pygame.Rect(660,436,25,25)

ball12 = pygame.image.load("Images/balls/12.png")
ball12Rect = pygame.Rect(680,448,25,25)

ball9 = pygame.image.load("Images/balls/9.png")
ball9Rect = pygame.Rect(620,388,25,25)

ball10 = pygame.image.load("Images/balls/10.png")
ball10Rect = pygame.Rect(640,376,25,25)

ball11 = pygame.image.load("Images/balls/11.png")
ball11Rect = pygame.Rect(660,364,25,25)

ball5 = pygame.image.load("Images/balls/5.png")
ball5Rect = pygame.Rect(680,352,25,25)

ball8 = pygame.image.load("Images/balls/8.png")
ball8Rect = pygame.Rect(640,400,25,25)

ball7 = pygame.image.load("Images/balls/7.png")
ball7Rect = pygame.Rect(660,388,25,25)

ball14 = pygame.image.load("Images/balls/14.png")
ball14Rect = pygame.Rect(660,412,25,25)

ball13 = pygame.image.load("Images/balls/13.png")
ball13Rect = pygame.Rect(680,376,25,25)

ball15 = pygame.image.load("Images/balls/15.png")
ball15Rect = pygame.Rect(680,400,25,25)

ball6 = pygame.image.load("Images/balls/6.png")
ball6Rect = pygame.Rect(680,424,25,25)

pygame.time.set_timer (pygame.USEREVENT,1000)

solids = [ball1,ball2,ball3,ball4,ball5,ball6,ball7]
stripes = [ball9,ball10,ball1,ball13,ball14,ball15]







clock = pygame.time.Clock()                            # Manage timing for screen updates


#Program helper functions:
def showMessage(words, size,x,y,color,bg=None):
    font = pygame.font.SysFont("bitstreamveraserif",size,True,False)
    textImage = font.render(words,True,color, bg)
    textBounds =textImage.get_rect()  #bounding box of the text image
    textBounds.center=(x,y) #center text within the bounding box
    surface.blit(textImage,textBounds)    #put on screen
    return textBounds

def showMessageMono(words, size,x,y,color,bg=None):
    font = pygame.font.SysFont("bitstreamverasansmono",size,True,False)
    textImage = font.render(words,True,color, bg)
    textBounds =textImage.get_rect()  #bounding box of the text image
    textBounds.center=(x,y) #center text within the bounding box
    surface.blit(textImage,textBounds)    #put on screen
    return textBounds    

def howToPlayMSG ():
    offset = 20
    MSG = [
        "The game consists of 7 striped",
        "balls, 7 solid balls, a cue ball",
        ",and an 8 ball. The goal is to",
        "use the cue ball to pocket all of",
        "your balls (either the solid-colored",
        "or striped ones) before pocketing",
        "the 8 ball in a chosen pocket to",
        "win. Players start by breaking",
        "the triangle formation of balls on",
        "the table with the cue ball. If a",
        "player pockets a ball during the",
        "break, they are assigned that type",
        "of ball and get to keep shooting,",
        "trying to pocket as many of their",
        "designated balls as they can while",
        "avoiding scratching (hitting the",
        "cue ball into a pocket). Once a",
        "player has pocketed all of their",
        "designated balls, they can then",
        "try to pocket the 8 ball. However,",   
        "if they scratch the 8 ball before",
        "clearing their selected balls, they",
        "automatically lose the game. If a player",
        "pockets the 8 ball after all of their",
        "designated balls are gone in their",
        "chosen pockets, they win the game."   
    ]
    for line in MSG:
        showMessage(line, 16, 180, 240 + offset, WHITE)
        offset+=20

        
def rulesMSG ():
    offset = 20
    MSG = [
       "If a player pockets the cue ball during",
       "their turn, it's a scratch, and it becomes", 
       "the other player's turn regardless of",
       "whether they pocketed a ball or not. The", 
       "other player can also place the cue ball", 
       "wherever they want on the table for Their", 
       "next shot.If a player pockets the 8 ball", 
       "before it's their turn or scratches the cue", 
       "ball while attempting to pocket the 8 ball,", 
       "they automatically lose the game. If they", 
       "pocket the 8 ball in a pocket that they did", 
       "not choose before the game, the 8 ball is",
       "placed back in its previous spot, and it", 
       "becomes the other player's turn. Players",
       "don't have to hit their designated ball",
       "first and can choose not to hit a ball",
       "during their turn. They can use this to", 
       "block their opponent's shots. In this game,",
       "players don't have access to spin, so they",
       "must rely ontheir skills and strategies",
       "to win"
         
    ]
    for line in MSG:
        showMessage(line, 16, 510, 240 + offset, WHITE)
        offset+=20
        
        
def controlMSG ():
    offset = 20
    MSG = [
        "You may use the mouse to choose an",
        "angle for the ball to go. After choosing",
        "an angle. Click the stick and use",
        "the arrow keys to increase or decrease", 
        "your power. For choosing the 8 ball",
        "pocket you can click on one of the", 
        "pockets and it will have a little green", 
        "dot in the middle of it."
    ]
    for line in MSG:
        showMessage(line, 16, 820, 240 + offset, WHITE)
        offset+=20
        
def getNames (gotName1,gotName2,name1,name2,name1Color, name2Color):
    surface.fill(BLACK)
    showMessage("Enter Player Names", 80, w/2, 80, WHITE)
    showMessage("Maximum 20 Characters. Press Enter to submit name.", 20, w/2, 160, WHITE)
    showMessage("Player 1:", 25, w/2 - 130,h/4 + 112, WHITE)
    showMessage("Player 2:", 25, w/2 - 130,h*(3/4)+12, WHITE)        
    pygame.draw.rect(surface, WHITE,name1Rect,name1Color) 
    pygame.draw.rect(surface, WHITE, name2Rect,name2Color)
    if name1Color == 0:
        showMessageMono(name1, 20, (w/2 - 50)+ 6 *len(name1),h/4 + 112, BLACK)
    elif name1Color == 1:
        showMessageMono(name1, 20, (w/2 - 50)+ 6 *len(name1),h/4 + 112, WHITE)
    if name2Color == 0:
        showMessageMono(name2, 20, (w/2 - 50)+ 6 *len(name2),h*(3/4) + 12, BLACK)
    elif name2Color == 1:
        showMessageMono(name2, 20, (w/2 - 50)+ 6 *len(name2),h*(3/4) + 12, WHITE)
    if gotName1:
        pygame.draw.line(surface, GREEN, (w/2 - 210,h/4 + 110),(w/2 - 204,h/4 + 117),6)
        pygame.draw.line(surface, GREEN, (w/2 - 195,h/4 + 100),(w/2 - 204,h/4 + 117),6)
    if gotName2:
        pygame.draw.line(surface, GREEN,(w/2 - 204,h*(3/4) + 14), (w/2 - 210,h*(3/4) + 7),6)
        pygame.draw.line(surface, GREEN,(w/2 - 204,h*(3/4) + 15), (w/2 - 195,h*(3/4) - 2),6)         
        

def drawInfoScreen():
    showMessage("8 Ball", 100, w/2, 65, WHITE)
    showMessage("How to Play", 40, w/3 -140, 200, WHITE)
    howToPlayMSG ()
    pygame.draw.line(surface, WHITE, [w/3+20,180], [w/3+20,800])
    showMessage("Rules", 40, w/2, 200, WHITE)  
    rulesMSG()
    pygame.draw.line(surface, WHITE, [w*(2/3)-3,180], [w*(2/3)-3,800])    
    showMessage("Controls", 40,w*(3/4)+60,200,WHITE)
    controlMSG ()
    surface.blit(exitImg,exitRect)
    
    
def drawPlayScreen(gotName1,gotName2,name1,name2,name1Color, name2Color,stickColor, break1,break2, stickRect ):
    if (not (gotName1 and gotName2)):
        getNames(gotName1, gotName2, name1, name2, name1Color, name2Color)
    else:
        player1offset = 0
        player2offset = 0
        showMessage("8 Ball", 100, w/2, 65, WHITE)    
        surface.blit(tableImg, tableRect)
        pygame.draw.rect(surface, stickColor, [915, 85, 40, 620],4 )
        surface.blit(stickImg,stickRect)
        surface.blit(cue,cueRect)
        surface.blit (ball1,ball1Rect)
        surface.blit(ball2,ball2Rect)
        surface.blit(ball3,ball3Rect)
        surface.blit(ball4,ball4Rect)
        surface.blit(ball12,ball12Rect)
        surface.blit(ball9,ball9Rect)        
        surface.blit(ball10,ball10Rect)
        surface.blit(ball11,ball11Rect)
        surface.blit(ball5,ball5Rect)
        surface.blit(ball8,ball8Rect)
        surface.blit(ball7,ball7Rect)
        surface.blit(ball14,ball14Rect)
        surface.blit(ball13,ball13Rect)
        surface.blit(ball15,ball15Rect)
        surface.blit(ball6,ball6Rect)
        
        showMessage(name1,18,110,175,WHITE)
        showMessage("VS", 22, 450,175, WHITE)
        showMessage(name2,18,790,175,WHITE)
        for i in range (7):
            pygame.draw.circle(surface, BLACK,( 220 + player1offset,175), 12)
            player1offset += 30
        for i in range (7):
            pygame.draw.circle(surface, BLACK,( 680 - player2offset,175), 12)
            player2offset += 30   
            
        if break1:
            showMessage("Player 1 Breaks", 40, w/2-50, 700, WHITE)
        if break2:
            showMessage("Player 2 Breaks", 40, w/2-50, 700, WHITE)
            
        if not (break1 or break2):
            surface.blit(exitImg,playExitRect)
            

            
        
            
            
        
        
        
    


def drawScreen(stickRect):
    showMessage("8 Ball", 100, w/2, 65, WHITE)    
    surface.blit(tableImg, tableRect)
    pygame.draw.rect(surface, BLACK, [915, 85, 40, 620],4 )
    surface.blit(stickImg,stickRect)
    surface.blit(playImg,playRect)
    surface.blit(infoImg,infoRect)

# -------- Main Program Loop -----------
def main():                                             #every program should have a main function
                                                        #other functions go above main
    
    # local  variables  
    stickColor = BLACK
    info = False
    play = False
    name1 = ""
    name2 = ""
    name1Color = 1
    name2Color = 1
    gotName1 = False
    gotName2 = False
    delMax1 = False
    delMax2 = False
    whoBreaks = random.randint(1,2)
    seconds = 8
    break1 = False 
    break2 = False     
    stickRect = pygame.Rect(900, 90, 66, 500)
    power = 0
    

    
    
    while (True):
                
        for event in pygame.event.get():                #captures state of the game - loops thru changes
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): #end game
                pygame.quit();                          
                sys.exit();
            if (event.type == pygame.USEREVENT and seconds>0 and whoBreaks == 1 and play):
                break1 = True
                seconds -= 1
                if seconds == 0:
                    break1 = False
            if (event.type == pygame.USEREVENT and seconds>0 and whoBreaks == 2 and play):
                break2 = True
                seconds -= 1    
                if seconds == 0:
                    break2 = False
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and infoRect.collidepoint(pygame.mouse.get_pos()):
                info = True
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and playRect.collidepoint(pygame.mouse.get_pos()):
                play = True
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and exitRect.collidepoint(pygame.mouse.get_pos()) and info:
                info = False            
            if play:
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and playExitRect.collidepoint(pygame.mouse.get_pos()):
                    play = False
                if not gotName1:     
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and name1Rect.collidepoint(pygame.mouse.get_pos()):
                        name1Typing = True
                        name1Color = 0
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and not(name1Rect.collidepoint(pygame.mouse.get_pos())): 
                        name1Typing = False
                        name1Color = 1
                else:
                    name1Color = 0
                if not gotName2:
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and name2Rect.collidepoint(pygame.mouse.get_pos()):
                        name2Typing = True
                        name2Color = 0                    
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and not(name2Rect.collidepoint(pygame.mouse.get_pos())): 
                        name2Typing = False    
                        name2Color = 1
                else:
                    name2Color = 0
                if event.type==pygame.KEYDOWN: 
                    if name1Typing and gotName1 == False:
                        if len(name1) <= 19:
                            name1 += str(event.unicode)
                        if event.key==pygame.K_RETURN:
                            gotName1 = True
                            if len(name1) != 20:
                                name1 = name1[0:-1]                            
                        if event.key==pygame.K_BACKSPACE:
                            if len(name1) != 20 or delMax1:
                                name1 = name1[0:-2]
                                delMax1 = False
                            if len(name1) == 20:
                                name1 = name1[0:-1]
                                delMax1 = True
                    if name2Typing and gotName2 == False:
                        if len(name2) <= 19:
                            name2 += str(event.unicode)
                        if event.key==pygame.K_RETURN:
                            gotName2 = True
                            if len(name2) != 20:                            
                                name2 = name2[0:-1]                                            
                        if event.key==pygame.K_BACKSPACE:
                            if len(name2) != 20 or delMax2:                            
                                name2 = name2[0:-2]
                                delMax2 = False
                            if len(name2) == 20:
                                name2 = name2[0:-1]
                                delMax2 = True
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and stickRect.collidepoint(pygame.mouse.get_pos()):
                    stickColor = WHITE
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and not(stickRect.collidepoint(pygame.mouse.get_pos())):
                    stickColor = BLACK
                    stickRect = pygame.Rect(900, 90, 66, 500)
                if stickColor == WHITE and event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and power < 10:
                    power +=1
                    stickRect = pygame.Rect(900, 90 + power*11, 66, 500)
                if stickColor == WHITE and event.type == pygame.KEYDOWN and event.key == pygame.K_UP and power > 0:
                    power -= 1
                    stickRect = pygame.Rect(900, 90 + power*11, 66, 500)
          
                    
                
 
        
            # button, mouse, or keyboard interaction here
        
        # ongoing game logic here  (repeats every 1/60 second) 
     
        
        
      
        surface.fill(DARK_GREY)                             #set background color
        
        #drawing code goes here
        if info:
            drawInfoScreen()
        if play:
            drawPlayScreen(gotName1,gotName2,name1, name2,name1Color, name2Color, stickColor, break1, break2, stickRect)
        if not(play or info):
            drawScreen(stickRect)
   
    
        
        
        
        
        
        pygame.display.update()                          #updates the screen-
        
        
#----------------------------------------------------------------            
main()                                                   #runs the game
