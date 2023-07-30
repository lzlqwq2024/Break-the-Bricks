import pygame,sys,time,random,threading,os
from pygame.locals import *
from PIL import Image
pygame.init()
pygame.mixer.init()

#创建窗口
canvas = pygame.display.set_mode((800,560))
pygame.display.set_caption('block (Press P/SPACE to Pause,move platform,Hit all the bricks without letting the ball fall off the screen!)')

#监听事件
def HandleEvent():
    global state,start_button_state,more_button_state,ball_state,controlshow,mouse_see,circlex,volumn_drag
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == 'START':
                mx = event.pos[0]
                my = event.pos[1]
                if mouse(192,256,415,49,mx,my):
                    state = 'RUNNING'
                elif mouse(179,372,442,51,mx,my):
                    state = 'MOREGAME'
                elif mouse(20,20,61,61,mx,my):
                    if controlshow == 0:
                        controlshow = 1
                    elif controlshow == 1:
                        controlshow = 0
                elif mouse(641,43,32,32,mx,my):
                    if controlshow == 1:
                        if mouse_see == 0:
                            mouse_see = 1
                        elif mouse_see == 1:
                            mouse_see = 0
                elif mouse(circlex-8,58-8,16,16,mx,my):
                    if controlshow == 1:
                        volumn_drag = 1
            elif state == 'RUNNING':
                if ball_state == 'on':
                    ball_state = 'off'

        elif event.type == pygame.MOUSEBUTTONUP:
            if state == 'START':
                if volumn_drag == 1:
                    volumn_drag = 0

        elif event.type == pygame.MOUSEMOTION:
            if state == 'START':
                mx = event.pos[0]
                my = event.pos[1]
                if mouse(192,256,415,49,mx,my):
                    start_button_state = 'b'
                elif not(mouse(192,256,415,49,mx,my)):
                    start_button_state = 'n'
                if mouse(179,372,442,51,mx,my):
                    more_button_state = 'b'
                elif not(mouse(179,372,442,51,mx,my)):
                    more_button_state =  'n'

        elif event.type == pygame.KEYDOWN:
            if state == 'RUNNING':
                if event.key == 112 or event.key == 32:
                    state = 'PAUSE'
            elif state == 'PAUSE':
                if event.key == 112 or event.key == 32:
                    pygame.mouse.set_pos(player_plat.x+69,player_plat.y)  #防止提前移动鼠标，设置鼠标位置
                    state = 'RUNNING'
                elif event.key == 98:
                    ClearGame()
                    state = 'START'
            elif state == 'GAMEOVER':
                if event.key == 115:
                    ClearGame()
                    state = 'RUNNING'
                elif event.key == 98:
                    ClearGame()
                    state = 'START'
                    

#显示字体
def write(word,position,size,color,fontpath="font/font1.ttf"):
    text = pygame.font.Font(fontpath,size)
    writeText = text.render(word,True,color)
    canvas.blit(writeText,position)

#鼠标位置判断
def mouse(x,y,width,height,mx,my):
    return mx >= x and mx <= x+width and my >= y and my <= y+height

#播放音乐
def play_music():
    global music
    music.play(loops=-1)

#设置音量
def set_loud(loud):
    global music
    music.set_volume(loud)

#改变图片大小
def ResizeImg(imgpath,width,height):
    resize_img = Image.open(imgpath)
    new_img = resize_img.resize((width,height))
    new_img.save('resizeimages/new_resize_img.png')
    return pygame.image.load('resizeimages/new_resize_img.png')

#导入图片与变量
title = pygame.image.load('images/title.png')
startbutton = pygame.image.load('images/startbutton.png')
startbutton1 = pygame.image.load('images/startbutton1.png')
morebutton = pygame.image.load('images/morebutton.png')
morebutton1 = pygame.image.load('images/morebutton1.png')
controlbutton = pygame.image.load('images/controlbutton.png')
mouse_see_button = pygame.image.load('images/mouse_see_button.png')
mouse_see_button1 = pygame.image.load('images/mouse_see_button1.png')
defeatskill = pygame.image.load('images/ball_defeatbutton.png')
addballskill = pygame.image.load('images/addball.png')
platshortskill = pygame.image.load('images/platshort.png')
platlongskill = pygame.image.load('images/platlong.png')
have_volumn = pygame.image.load('images/have_volumn.png')
unhave_volumn = pygame.image.load('images/unhave_volumn.png')
controlrect = pygame.image.load('images/controlrect.png')
gameover = pygame.image.load('images/gameover.png')
gamepause = pygame.image.load('images/gamepause.png')
gameover_flat = pygame.image.load('images/gameover_flat.png')
lifeplat = pygame.image.load('images/lifeplat.png')
platform = pygame.image.load('images/platform.png')
ball = pygame.image.load('images/ball.png').convert_alpha()
ball2 = pygame.image.load('images/ball2.png').convert_alpha()
baseblock = pygame.image.load('images/baseblock.png')
goldblock = pygame.image.load('images/goldblock.png')
brownblock = pygame.image.load('images/brownblock.png')
airblock = pygame.image.load('images/airblock.png')
redblock = pygame.image.load('images/redblock.png')
greenblock = pygame.image.load('images/greenblock.png')
orangeblock = pygame.image.load('images/orangeblock.png')
blueblock = pygame.image.load('images/blueblock.png')

state = 'START'
start_button_state = 'n'
more_button_state = 'n'
ball_state = 'on'
ball1_speed = [6,3]
ball2_speed = [8,5]
all_block = []
gameover_setflat = 0
canwritelevel = 0
startball_x1 = random.randint(1,799)
startball_y1 = random.randint(1,559)
startball_x2 = random.randint(1,799)
startball_y2 = random.randint(1,559)
position1 = Rect(startball_x1,startball_y1,20,18)
position2 = Rect(startball_x2,startball_y2,20,18)
basic_xspeed = 5
basic_yspeed = -4
score = 0
levelnum = 1
all_level_data = []
collide_block = []
update_block = []
skills = []
balls = []
controlshow = 0
mouse_see = 1
music = pygame.mixer.Sound("music/music.mp3")
volumn_drag = 0
circlex = 376

#平板类
class PlatForm():
    def __init__(self,img,x,y,width,height):
        self.img = img
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def draw(self):
        canvas.blit(self.img,(self.x,self.y))
    def move(self):
        mousepos = pygame.mouse.get_pos()[0]
        self.x = mousepos-self.width/2
        if self.x < 0:
            self.x = 0
        if self.x+self.width > 800:
            self.x = 800-self.width
    def hit(self,object):
        o = object
        if (o.position.left > (self.x-o.width) and o.position.left < (self.x+self.width) and o.position.top > (self.y-o.height) and o.position.top < (self.y+self.height)):
            if (o.position.left > (self.x-o.width) and o.position.left <= (self.x+self.width/3)):
                return 1
            elif (o.position.left > (self.x+self.width/3) and o.position.left <= (self.x+self.width/3*2)):
                return 2
            elif (o.position.left >(self.x+self.width/3*2) and o.position.left <= (self.x+self.width)):
                return 3

#球类
class Ball():
    def __init__(self,img,x,y,width,height,speed,life):
        self.img = img
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.position = Rect(self.x,self.y,self.width,self.height)
        self.defeat = 0
        self.life = life
    def draw(self):
        canvas.blit(self.img,self.position)        
    def move(self):
        global state
        self.position = self.position.move(self.speed)
        if self.position.left <= 0:
            self.speed[0] = -self.speed[0]
            self.position.left = 1
        elif self.position.right >= 800:
            self.speed[0] = -self.speed[0]
            self.position.right = 799
        if self.position.top <= 0:
            self.speed[1] = -self.speed[1]
            self.position.top = 1
        if self.position.top > 560:
            self.position.top = -100
            self.life -= 1
            if self.life <= 0:
                state = 'GAMEOVER'
            else:
                state = 'RETURN'

#衍生球类
class AddBall():
    def __init__(self,img,x,y,width,height,speed):
        self.img = img
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.position = Rect(self.x,self.y,self.width,self.height)
        self.canDelete = 0
    def draw(self):
        canvas.blit(self.img,self.position)        
    def move(self):
        global balls
        self.position = self.position.move(self.speed)
        if self.position.left <= 0:
            self.speed[0] = -self.speed[0]
            self.position.left = 1
        elif self.position.right >= 800:
            self.speed[0] = -self.speed[0]
            self.position.right = 799
        if self.position.top <= 0:
            self.speed[1] = -self.speed[1]
            self.position.top = 1
        if self.position.top > 560:
            self.canDelete = 1            

#砖块类
class Block():
    def __init__(self,img,x,y,width,height,score,blocktype):
        self.img = img
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = Rect(self.x,self.y,self.width,self.height)
        self.score = score
        self.blocktype = blocktype
    def draw(self):
        canvas.blit(self.img,(self.x,self.y))
    def hit(self,object):
        o = object
        if (o.position.right >= self.x and o.position.left <= self.x+self.width and o.position.bottom >= self.y and o.position.top <= self.y+self.height):
            if o.position.bottom <= self.y+abs(o.speed[1]) and o.position.bottom >= self.y:
                return 1
            elif o.position.top >= self.y+self.height-abs(o.speed[1]) and o.position.top <= self.y+self.height:
                return 2
            elif o.position.right <= self.x+abs(o.speed[0]) and o.position.right >= self.x:
                return 3
            elif o.position.left >= self.x+self.width-abs(o.speed[0]) and o.position.left <= self.x+self.width:
                return 4

#技能类
class Skill():
    def __init__(self,img,x,y,width,height,skilltype):
        self.img = img
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canDelete = 0
        self.skilltype = skilltype
    def draw(self):
        canvas.blit(self.img,(self.x,self.y))
    def move(self):
        self.y += 3
        if self.y >= 560:
            self.canDelete = 1
    def hit(self,object):
        o = object
        return (self.x > (o.x-self.width) and self.x < (o.x+o.width) and self.y > (o.y-self.height) and self.y < (o.y+o.height))     

player_plat = PlatForm(platform,331,485,138,14)
game_ball = Ball(ball,390,467,20,18,[5,-4],4)
clock = pygame.time.Clock()

def GetData():
    global all_level_data
    all_level_data = []
    file = open('detail/level.txt','r')
    all_data = file.readlines()
    for line in all_data:
        if line != '' and line != '\n': 
            all_level_data.append(line.strip())
    file.close()

def ObjectMove():
    global skills,balls
    player_plat.move()
    game_ball.move()

    if len(skills) > 0:
        for skill in skills:
            skill.move()
    if len(balls) > 0:
        for add_gameball in balls:
            add_gameball.move()

def BallOn():
    player_plat.move()
    game_ball.position.left = player_plat.x+69-10

def DrawObject():
    global all_block,lifeplat,skills,balls
    if game_ball.life == 4:
        canvas.blit(lifeplat,(738,10))
        canvas.blit(lifeplat,(676,10))
        canvas.blit(lifeplat,(614,10))
    elif game_ball.life == 3:
        canvas.blit(lifeplat,(738,10))
        canvas.blit(lifeplat,(676,10))
    elif game_ball.life == 2:
        canvas.blit(lifeplat,(738,10))

    player_plat.draw()

    for block in all_block:
        block.draw()
    if len(skills) > 0:
        for skill in skills:
            skill.draw()
    if len(balls) > 0:
        for add_gameball in balls:
            add_gameball.draw()

    game_ball.draw()

def BallUpdate(speed):
    if abs(game_ball.speed[0]) == game_ball.speed[0]:
        game_ball.speed[0] = game_ball.speed[0] + speed+0.05
    elif abs(game_ball.speed[0]) != game_ball.speed[0]:
        game_ball.speed[0] = game_ball.speed[0] - speed+0.05
    if abs(game_ball.speed[1]) == game_ball.speed[1]:
        game_ball.speed[1] = game_ball.speed[1] + speed
    elif abs(game_ball.speed[1]) != game_ball.speed[1]:
        game_ball.speed[1] = game_ball.speed[1] - speed

def BlockUpdate():
    global update_block,collide_block
    for datalist in update_block:
        if pygame.time.get_ticks() >= datalist[0]:
            collide_block.append(datalist[1])
            update_block.remove(datalist)

def hit():
    global all_block,score,state,collide_block,update_block,skills,state,balls,player_plat
    if player_plat.hit(game_ball):
        if player_plat.hit(game_ball) == 1:
            game_ball.speed[0] = -abs(game_ball.speed[0])
            game_ball.speed[1] = -abs(game_ball.speed[1])
        elif player_plat.hit(game_ball) == 2:
            game_ball.speed[1] = -abs(game_ball.speed[1])
        elif player_plat.hit(game_ball) == 3:
            game_ball.speed[0] = abs(game_ball.speed[0])
            game_ball.speed[1] = -abs(game_ball.speed[1])
        BallUpdate(0.07)

    for block in collide_block:
        if block.hit(game_ball):
            if block.hit(game_ball) == 1:
                game_ball.speed[1] = -abs(game_ball.speed[1])
            elif block.hit(game_ball) == 2:
                game_ball.speed[1] = abs(game_ball.speed[1])
            elif block.hit(game_ball) == 3:
                game_ball.speed[0] = -abs(game_ball.speed[0])
            elif block.hit(game_ball) == 4:
                game_ball.speed[0] = abs(game_ball.speed[0])
            if block.blocktype == 'base':
                all_block.remove(block)
                collide_block.remove(block)
                score+=block.score
            elif block.blocktype == 'gold':
                all_block.remove(block)
                newblock = Block(baseblock,block.x,block.y,51,28,20,'base')
                all_block.append(newblock)
                collide_block.remove(block)
                update_block.append([pygame.time.get_ticks()+10,newblock])
            elif block.blocktype == 'brown':
                all_block.remove(block)
                newblock = Block(goldblock,block.x,block.y,51,28,0,'gold')
                all_block.append(newblock)
                collide_block.remove(block)
                update_block.append([pygame.time.get_ticks()+10,newblock])
            elif block.blocktype == 'air':
                newblock = Block(airblock,block.x,block.y,51,28,10,'base')
                all_block.append(newblock)
                collide_block.remove(block)
                update_block.append([pygame.time.get_ticks()+10,newblock])
            elif block.blocktype == 'red':
                newskill = Skill(defeatskill,block.x-12,block.y-20,40,48,'defeat')
                skills.append(newskill)
                all_block.remove(block)
                collide_block.remove(block)
                score += block.score
            elif block.blocktype == 'green':
                newskill = Skill(addballskill,block.x-12,block.y-20,40,48,'addball')
                skills.append(newskill)
                all_block.remove(block)
                collide_block.remove(block)
                score += block.score
            elif block.blocktype == 'orange':
                newskill = Skill(platshortskill,block.x-12,block.y-20,40,48,'platshort')
                skills.append(newskill)
                all_block.remove(block)
                collide_block.remove(block)
                score += block.score
            elif block.blocktype == 'blue':
                newskill = Skill(platlongskill,block.x-12,block.y-20,40,48,'platlong')
                skills.append(newskill)
                all_block.remove(block)
                collide_block.remove(block)
                score += block.score

    if len(balls) > 0:
        for add_game_ball in balls:
            if add_game_ball.canDelete == 1:
                if add_game_ball in balls:
                    balls.remove(add_game_ball)
            for block in collide_block:
                if block.hit(add_game_ball):
                    if block.hit(add_game_ball) == 1:
                        add_game_ball.speed[1] = -abs(add_game_ball.speed[1])
                    elif block.hit(add_game_ball) == 2:
                        add_game_ball.speed[1] = abs(add_game_ball.speed[1])
                    elif block.hit(add_game_ball) == 3:
                        add_game_ball.speed[0] = -abs(add_game_ball.speed[0])
                    elif block.hit(add_game_ball) == 4:
                        add_game_ball.speed[0] = abs(add_game_ball.speed[0])
                    if block.blocktype == 'base':
                        if block in all_block:
                            all_block.remove(block)
                            collide_block.remove(block)
                        score+=block.score
                    elif block.blocktype == 'gold':
                        if block in all_block:
                            all_block.remove(block)
                        newblock = Block(baseblock,block.x,block.y,51,28,20,'base')
                        all_block.append(newblock)
                        collide_block.remove(block)
                        update_block.append([pygame.time.get_ticks()+50,newblock])
                    elif block.blocktype == 'brown':
                        if block in all_block:
                            all_block.remove(block)
                            collide_block.remove(block)
                        newblock = Block(goldblock,block.x,block.y,51,28,0,'gold')
                        all_block.append(newblock)
                        update_block.append([pygame.time.get_ticks()+50,newblock])
                    elif block.blocktype == 'air':
                        newblock = Block(airblock,block.x,block.y,51,28,10,'base')
                        all_block.append(newblock)
                        if block in all_block:
                            collide_block.remove(block)
                        update_block.append([pygame.time.get_ticks()+50,newblock])
                    elif block.blocktype == 'red':
                        newskill = Skill(defeatskill,block.x-12,block.y-20,40,48,'defeat')
                        skills.append(newskill)
                        if block in all_block:
                            all_block.remove(block)
                            collide_block.remove(block)
                        score += block.score
                    elif block.blocktype == 'green':
                        newskill = Skill(addballskill,block.x-12,block.y-20,40,48,'addball')
                        skills.append(newskill)
                        if block in all_block:
                            all_block.remove(block)
                            collide_block.remove(block)
                        score += block.score
                    elif block.blocktype == 'orange':
                        newskill = Skill(platshortskill,block.x-12,block.y-20,40,48,'platshort')
                        skills.append(newskill)
                        if block in all_block:
                            all_block.remove(block)
                            collide_block.remove(block)
                        score += block.score
                    elif block.blocktype == 'blue':
                        newskill = Skill(platlongskill,block.x-12,block.y-20,40,48,'platlong')
                        skills.append(newskill)
                        if block in all_block:
                            all_block.remove(block)
                            collide_block.remove(block)
                        score += block.score
    
    if len(skills) > 0:
        for skill in skills:
            if skill.hit(player_plat):
                skills.remove(skill)
                if skill.skilltype == 'defeat':
                    game_ball.life -= 1
                    if game_ball.life == 0:
                        state = 'GAMEOVER'
                    else:
                        state = 'RETURN'
                elif skill.skilltype == 'addball':
                    strf = random.choice('-1')
                    if strf == '-':
                        game_ball1 = AddBall(ball2,game_ball.position.left,game_ball.position.top,20,18,[random.randint(5,8)*-1,random.randint(4,7)*-1])
                    elif strf == '1':
                        game_ball1 = AddBall(ball2,game_ball.position.left,game_ball.position.top,20,18,[random.randint(5,8),random.randint(4,7)*-1])
                    balls.append(game_ball1)
                elif skill.skilltype == 'platshort':
                    player_plat = PlatForm(ResizeImg('images/platform.png',player_plat.width//5*4,14),pygame.mouse.get_pos()[0]-player_plat.width/2,player_plat.y,player_plat.width//5*4,14)
                elif skill.skilltype == 'platlong':
                    player_plat = PlatForm(ResizeImg('images/platform.png',player_plat.width//5*6,14),pygame.mouse.get_pos()[0]-player_plat.width/2,player_plat.y,player_plat.width//5*6,14)

def Return():
    global ball_state,state,gameover_setflat,skills,balls,player_plat
    pygame.mouse.set_pos(331+69,485)
    player_plat.x = 331
    game_ball.position = Rect(390,467,20,18)
    game_ball.speed = [5,-4]
    ball_state = 'on'
    player_plat = PlatForm(platform,331,485,138,14)
    gameover_setflat = 0
    skills = []
    balls = []
    state = 'RUNNING'

def turnblock(gamemap):
    global baseblock,all_block,collide_block
    all_block = []
    collide_block = []
    for row in gamemap:
        listrow = row.split(',')
        for item in listrow:
            rownum = gamemap.index(row)
            if item == '1':
                itemnum = listrow.index(item)
                block = Block(baseblock,(itemnum*51+68),(rownum*28+60),51,28,10,'base')
                all_block.append(block)
                collide_block.append(block)
                listrow.insert(itemnum,'0')
                listrow.remove(item)
            elif item == '2':
                itemnum = listrow.index(item)
                block = Block(goldblock,(itemnum*51+68),(rownum*28+60),51,28,0,'gold')
                all_block.append(block)
                collide_block.append(block)
                listrow.insert(itemnum,'0')
                listrow.remove(item)
            elif item == '3':
                itemnum = listrow.index(item)
                block = Block(brownblock,(itemnum*51+68),(rownum*28+60),51,28,0,'brown')
                all_block.append(block)
                collide_block.append(block)
                listrow.insert(itemnum,'0')
                listrow.remove(item)
            elif item == '4':
                itemnum = listrow.index(item)
                block = Block(airblock,(itemnum*51+68),(rownum*28+60),51,28,0,'air')
                collide_block.append(block)
                listrow.insert(itemnum,'0')
                listrow.remove(item)
            elif item == '5':
                itemnum = listrow.index(item)
                block = Block(redblock,(itemnum*51+68),(rownum*28+60),51,28,10,'red')
                all_block.append(block)
                collide_block.append(block)
                listrow.insert(itemnum,'0')
                listrow.remove(item)
            elif item == '6':
                itemnum = listrow.index(item)
                block = Block(greenblock,(itemnum*51+68),(rownum*28+60),51,28,10,'green')
                all_block.append(block)
                collide_block.append(block)
                listrow.insert(itemnum,'0')
                listrow.remove(item)
            elif item == '7':
                itemnum = listrow.index(item)
                block = Block(orangeblock,(itemnum*51+68),(rownum*28+60),51,28,10,'orange')
                all_block.append(block)
                collide_block.append(block)
                listrow.insert(itemnum,'0')
                listrow.remove(item)
            elif item == '8':
                itemnum = listrow.index(item)
                block = Block(blueblock,(itemnum*51+68),(rownum*28+60),51,28,10,'blue')
                all_block.append(block)
                collide_block.append(block)
                listrow.insert(itemnum,'0')
                listrow.remove(item)  
        gamemap.insert(rownum,[0,0,0,0,0,0,0,0,0,0,0,0])
        gamemap.remove(row)

def getlevelmap():
    global all_level_data,levelnum
    level_data = []
    for x in range(levelnum*10-10,levelnum*10):
        level_data.append(all_level_data[x])
    return level_data

def levelturn():
    global all_block,levelnum,ball_state,gameover_setflat,skills,balls,player_plat
    player_plat.x = 331
    pygame.mouse.set_pos(331+69,485)
    game_ball.position = Rect(390,467,20,18)
    game_ball.speed = [5,-4]
    ball_state = 'on'
    player_plat = PlatForm(platform,331,485,138,14)
    gameover_setflat = 0
    levelnum += 1
    skills = []
    balls = []
    turnblock(getlevelmap())
    time.sleep(0.5)

def ClearGame():
    global levelnum,ball_state,gameover_setflat,score,skills,player_plat
    player_plat.x = 331
    pygame.mouse.set_pos(331+69,485)
    game_ball.position = Rect(390,467,20,18)
    game_ball.speed = [5,-4]
    ball_state = 'on'
    player_plat = PlatForm(platform,331,485,138,14)
    gameover_setflat = 0
    levelnum = 1
    score = 0
    GetData()
    skills = []
    balls = []
    turnblock(getlevelmap())
    game_ball.life = 4

GetData()
turnblock(getlevelmap())

thread1 = threading.Thread(target=play_music,daemon=True)
thread1.start()

#主循环
while True:
    if state == 'START':
        if mouse_see == 0:
            pygame.mouse.set_visible(True)

        canvas.fill((0,0,0))
        canvas.blit(controlbutton,(20,20))
        canvas.blit(title,(79,124))
        
        position1 = position1.move(ball1_speed)
        position2 = position2.move(ball2_speed)
        canvas.blit(ball,position1)
        canvas.blit(ball,position2)

        if start_button_state == 'n':
            canvas.blit(startbutton,(192,256))
        elif start_button_state == 'b':
            canvas.blit(startbutton1,(192,256))
        if more_button_state == 'n':
            canvas.blit(morebutton,(179,372))
        elif more_button_state == 'b':
            canvas.blit(morebutton1,(179,372))

        if position1.left <= 0 or position1.right >= 800:
            ball = pygame.transform.flip(ball,True,False)
            ball1_speed[0] = -ball1_speed[0]
            if position1.left <= 0:
                position1.left = 1
            elif position1.right >= 800:
                position1.right = 799
        if position1.top <= 0 or position1.bottom >= 560:
            ball1_speed[1] = -ball1_speed[1]
            if position1.top <= 0:
                position1.top = 1
            elif position1.bottom >= 560:
                position1.bottom = 559
        if position2.left <= 0 or position2.right >= 800:
            ball = pygame.transform.flip(ball,True,False)
            ball2_speed[0] = -ball2_speed[0]
            if position2.left <= 0:
                position2.left = 1
            elif position2.right >= 800:
                position2.right = 799
        if position2.top <= 0 or position2.bottom >= 560:
            ball2_speed[1] = -ball2_speed[1]
            if position2.top <= 0:
                position2.top = 1
            elif position2.bottom >= 560:
                position2.bottom = 559

        if controlshow == 1:
            canvas.blit(controlrect,(91,20))
            pygame.draw.line(canvas,(255,255,255),(226,58),(426,58),width=3)
            pygame.draw.circle(canvas,(150,150,150),(circlex,58),8)
            if circlex == 226:
                canvas.blit(unhave_volumn,(165,39))
            else:
                canvas.blit(have_volumn,(165,39))                
            if mouse_see == 0:
                canvas.blit(mouse_see_button1,(641,43))
            elif mouse_see == 1:
                canvas.blit(mouse_see_button,(641,43))
            if volumn_drag == 1:
                circlex = pygame.mouse.get_pos()[0]
                if circlex < 226:
                    circlex = 226
                elif circlex > 426:
                    circlex = 426
                set_loud(float((circlex-226)/200))                    

    elif state == 'RUNNING':
        if mouse_see == 0:
            pygame.mouse.set_visible(False)
        elif mouse_see == 1:
            pygame.mouse.set_visible(True)
        canvas.fill((0,0,0))
        if ball_state == 'on':
            BallOn()
        elif ball_state == 'off':
            ObjectMove()
        hit()
        DrawObject()
        BlockUpdate()
        if len(all_block) == 0:
            levelturn()

    elif state == 'GAMEOVER':
        if gameover_setflat == 0:
            for x in range(20):
                gameover_flat.set_alpha(10)
                canvas.blit(gameover_flat,(0,0))
                pygame.display.update()
                time.sleep(0.015)
            gameover_setflat = 1
        time.sleep(1)
        canvas.blit(gameover,(178,125))
        write(str(score),(446,241),40,(255,255,255))

    elif state == 'RETURN':
        if gameover_setflat == 0:
            for x in range(20):
                gameover_flat.set_alpha(10)
                canvas.blit(gameover_flat,(0,0))
                pygame.display.update()
                time.sleep(0.015)
            gameover_setflat = 1        
        Return()
        time.sleep(1)

    elif state == 'PAUSE':
        if mouse_see == 0:
            pygame.mouse.set_visible(False)
        elif mouse_see == 1:
            pygame.mouse.set_visible(True)
        canvas.fill((0,0,0))
        DrawObject()
        canvas.blit(gamepause,(178,125))
        write(str(levelnum),(465,242),40,(255,255,255))

    elif state == 'MOREGAME':
        canvas.fill((0,0,0))
        thread2.start()

    HandleEvent()
    pygame.display.update()
    clock.tick(80)
