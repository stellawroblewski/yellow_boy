from tkinter import *
from Game import Game, Agent
from geometry import Point2D, Vector2D
import math
import random
import time


class Ghostboy(Agent):
    WIDTH     = 0.9
    LENGTH    = 0.9
    START_X   = 1.5 
    START_Y   = -1.5
    AGILITY   = 0.6

    def __init__(self, position, world):
        self.length = self.LENGTH
        self.width  = self.WIDTH
        self.direction = random.randint(1,4)
        Agent.__init__(self,position,world)

    def iseaten(self):
        self.world.ghosts.remove(self)
        self.world.agents.remove(self)

    def color(self): #changes color scheme when level increases 
        if self.world.level == 1:
            return "#ffffff"
        elif self.world.level == 2:
            return "#4141f4"
        elif self.world.level == 3:
            return "#ed6425"
        elif self.world.level == 4:
            return "#e52a19"
        elif self.world.level == 5:
            return "#1ab234"
    def shape(self):
        p1 = self.position + Vector2D( self.width/2.0, self.length/2.0)     
        p2 = self.position + Vector2D(-self.width/2.0, self.length/2.0)        
        p3 = self.position + Vector2D(-self.width/2.0,-self.length/2.0)       
        p4 = self.position + Vector2D( self.width/2.0,-self.length/2.0)       
        return [p1,p2,p3,p4]

    def keep_within_ybounds(self):
        if self.position.y < self.world.bounds.ymin:
            self.position.y = self.world.bounds.ymax
        if self.position.y > self.world.bounds.ymax:
            self.position.y = self.world.bounds.ymin


    def keep_within_xbounds(self):
        if self.position.x < self.world.bounds.xmin:
            self.position.x = self.world.bounds.xmax
        if self.position.x > self.world.bounds.xmax:
            self.position.x = self.world.bounds.xmin

    def move_down(self):
        self.position.y += self.length * self.AGILITY

    def move_up(self):
        self.position.y -= self.length * self.AGILITY

    def move_left(self):
        self.position.x -= self.width * self.AGILITY

    def move_right(self):
        self.position.x += self.width * self.AGILITY

    def update(self):
        if self.world.level == 2: #agility increases make the ghostboy's speed increase with level increase 
            self.AGILITY = 0.8
        elif self.world.level == 3:#agility increases make the ghostboy's speed increase with level increase 
            self.AGILITY = 1.3
        elif self.world.level == 4:#agility increases make the ghostboy's speed increase with level increase 
            self.AGILITY = 1.6
        elif self.world.level == 5:#agility increases make the ghostboy's speed increase with level increase 
            self.AGILITY = 2.0
        if self.direction == 1:
            self.move_down()
            self.keep_within_ybounds()
            self.keep_within_xbounds()
        elif self.direction == 2:
            self.move_up()
            self.keep_within_ybounds()
            self.keep_within_xbounds()
        elif self.direction == 3:
            self.move_left()
            self.keep_within_ybounds()
            self.keep_within_xbounds()
        elif self.direction == 4:
            self.move_right()
            self.keep_within_ybounds()
            self.keep_within_xbounds()
        dx = abs(self.position.x - self.world.yellow_boy.position.x) 
        dy = abs(self.position.y - self.world.yellow_boy.position.y)    
        if dx < 1 and dy < 1: #if the distance of the yellowboy is within 1 from the ghostboy, yellowboy gets hit with a life decrease and the ghostboy leaves
            self.world.myscore -= 10
            self.world.report("MINUS 10 POINTS")
            self.world.lives -= 1
            self.leave()

class Food(Agent):
    
    WIDTH     = 0.5
    LENGTH    = 0.5
    START_X   = 0.95 
    START_Y   = -0.95

    def __init__(self, position, world):
        self.length = self.LENGTH
        self.width  = self.WIDTH
        Agent.__init__(self,position,world)

    def iseaten(self):
        self.world.foods.remove(self)
        self.world.agents.remove(self)

    def color(self):  #changes color scheme when level increases 
        if self.world.level == 1:
            return "#a4add8"
        elif self.world.level == 2:
            return "#839b41"
        elif self.world.level == 3:
            return "#bdedeb"
        elif self.world.level == 4:
            return "#98f2d8"
        elif self.world.level == 5:
            return "#b21a35"

    def shape(self):
        p1 = self.position + Vector2D( self.width/2.0, self.length/2.0)     
        p2 = self.position + Vector2D(-self.width/2.0, self.length/2.0)        
        p3 = self.position + Vector2D(-self.width/2.0,-self.length/2.0)       
        p4 = self.position + Vector2D( self.width/2.0,-self.length/2.0)       
        return [p1,p2,p3,p4]

    def update(self):
        dx = abs(self.position.x - self.world.yellow_boy.position.x)
        dy = abs(self.position.y - self.world.yellow_boy.position.y)    
        if dx < 1 and dy < 1:#if the distance of the yellowboy is within 1 from the food, yellowboy gets a one point increase and the food gets eaten
            self.iseaten()
            self.world.myscore += 1

class Treat(Agent):
    
    WIDTH     = 0.8
    LENGTH    = 0.8
    START_X   = 0.95 
    START_Y   = -0.95

    def __init__(self, position, world):
        self.length = self.LENGTH
        self.width  = self.WIDTH
        Agent.__init__(self,position,world)

    def iseaten(self):
        self.world.treats.remove(self)
        self.world.agents.remove(self)

    def color(self):  #changes color scheme when level increases 
        if self.world.level == 1:    
            return "#f44265"
        elif self.world.level == 2:
            return "#5bcc9b"
        elif self.world.level == 3:
            return "#c57ddb"
        elif self.world.level == 4:
            return "#757722"
        elif self.world.level == 5:
            return "#227764"

    def shape(self):
        p1 = self.position + Vector2D( self.width/2.0, self.length/2.0)     
        p2 = self.position + Vector2D(-self.width/2.0, self.length/2.0)        
        p3 = self.position + Vector2D(-self.width/2.0,-self.length/2.0)       
        p4 = self.position + Vector2D( self.width/2.0,-self.length/2.0)       
        return [p1,p2,p3,p4]

    def update(self):
        dx = abs(self.position.x - self.world.yellow_boy.position.x)
        dy = abs(self.position.y - self.world.yellow_boy.position.y)    
        if dx < 1 and dy < 1:#if the distance of the yellowboy is within 1 from the treat, yellowboy gets a ten point increase and the treat gets eaten
            self.world.myscore += 10
            self.world.report("Yellowboy found a treat! Bonus 10 points")
            self.iseaten()

class Powertreat(Treat): #very small hard to find treat that increases in concentration with levels, increases level by 1
    WIDTH = 0.3
    LENGTH = 0.3
    
    def iseaten(self):
        self.world.powertreats.remove(self)
        self.world.agents.remove(self)

    def color(self): 
        return "#ffffff"

    def update(self):
        dx = abs(self.position.x - self.world.yellow_boy.position.x)
        dy = abs(self.position.y - self.world.yellow_boy.position.y)    
        if dx < 1 and dy < 1:
            self.world.level += 1
            self.world.report("Yellowboy found a power treat! Bonus 10 points! Try to eat the ghostboys until their color reverts!")
            self.iseaten()


class Yellowboy(Agent):

    START_X   = 0
    START_Y   = 0
    WIDTH     = 1.0
    LENGTH    = 1.0
    AGILITY   = 0.5

    def __init__(self,world,yellow_boy=True):
        self.on_left = yellow_boy
        self.length = self.LENGTH
        self.width  = self.WIDTH
        self.serving = True
        self.direction = random.randint(1,4)
        xoffset = -self.START_X
        yoffset =  self.START_Y
        position = world.bounds.point_at((xoffset+1.0)/2.0,(yoffset+1.0)/2.0)
        Agent.__init__(self,position,world)
        
    def keep_within_ybounds(self):
        if self.position.y < self.world.bounds.ymin:
            self.position.y = self.world.bounds.ymax
        if self.position.y > self.world.bounds.ymax:
            self.position.y = self.world.bounds.ymin


    def keep_within_xbounds(self):
        if self.position.x < self.world.bounds.xmin:
            self.position.x = self.world.bounds.xmax
        if self.position.x > self.world.bounds.xmax:
            self.position.x = self.world.bounds.xmin

    def color(self):
        return "#efef53"

    def shape(self):
        p1 = self.position + Vector2D( self.width/2.0, self.length/2.0)       
        p2 = self.position + Vector2D(-self.width/2.0, self.length/2.0)        
        p3 = self.position + Vector2D(-self.width/2.0,-self.length/2.0)       
        p4 = self.position + Vector2D( self.width/2.0,-self.length/2.0)       
        return [p1,p2,p3,p4]
        
    def move_down(self):
        self.position.y += self.length * self.AGILITY
        self.keep_within_ybounds()

    def move_up(self):
        self.position.y -= self.length * self.AGILITY
        self.keep_within_ybounds()

    def move_left(self):
        self.position.x -= self.width * self.AGILITY
        self.keep_within_xbounds()

    def move_right(self):
        self.position.x += self.width * self.AGILITY
        self.keep_within_xbounds()

    def update(self):
        if self.direction == 1:
            self.move_down()
        elif self.direction == 2:
            self.move_up()
        elif self.direction == 3:
            self.move_left()
        elif self.direction == 4:
            self.move_right()



class Pacman(Game):

    def __init__(self):
        Game.__init__(self,"YELLOWBOIIIIIIIIIIII!",60.0,45.0,800,600,topology='bound',console_lines=6)

        self.report("To move up and down:  hit 'j' or 'k'.")
        self.report("To move right and left: hit 'n' or 'm'.")
        self.report("Mac users will want to make this window full screen.")
        self.myscore  = 0
        self.report("Score:" + str(self.myscore))
        self.lives = 5
        self.left_turn = True
        self.level = 1
        self.serving = True
        self.foods = []
        self.ghosts = []
        self.treats = []
        self.powertreats = []
        self.addtreats()
        self.addpowertreats()
        self.addfood()
        self.addghosts()

        self.yellow_boy  = Yellowboy(self,yellow_boy=True)

    def handle_keypress(self,event):
        Game.handle_keypress(self,event)
        if event.char == 'i':
            self.yellow_boy.direction = 1
        elif event.char == 'k':
            self.yellow_boy.direction = 2
        elif event.char == 'j':
            self.yellow_boy.direction = 3
        elif event.char == 'l':
            self.yellow_boy.direction = 4
        elif event.char == 'v':
            if  self.left_turn and self.serving:
                self.serving = True

    def addfood(self):
        y = self.bounds.ymin
        while y <= self.bounds.ymax:   
            x = self.bounds.xmin
            while x <= self.bounds.xmax:  
                f = Food(Point2D(x,y),self)
                self.foods.append(f)
                x += 2
            y += 2

    def addghosts(self):
        self.ghostnumber = 0
        x = random.randint(-20,25)
        y = random.randint(-20,25)
        x = 0
        p = Ghostboy(Point2D(x,y),self)
        self.ghosts.append(p)

    def addtreats(self):
        self.treatnumber = 0
        x = random.randint(-25,25)
        y = random.randint(-25,25)
        p = Treat(Point2D(x,y),self)
        self.treats.append(p)

    def addpowertreats(self):
        self.powertreatsnumber = 0
        x = random.randint(-25,25)
        y = random.randint(-25,25)
        p = Powertreat(Point2D(x,y),self)
        self.powertreats.append(p)

    def serve(self):
        if self.left_turn:
            self.report("It's LEFT's serve. Hit 'x' to send the ball.")
        self.serving = True

    def display_score(self):
        self.report("SCORE:"+str(self.myscore))

    def display_lives(self):
        self.report("LIVES:"+str(self.lives))

    def update(self):
        if self.level == 1: #for each level increase, more ghosts are added, less treats are added, plus the addition of powertreats
            if len(self.ghosts) < 10:
                self.addghosts()
            if len(self.treats) < 25:
                self.addtreats()
        elif self.level == 2:
            if len(self.ghosts) < 15:
                self.addghosts()
            if len(self.treats) < 20:
                self.addtreats()
            if len(self.powertreats) < 3:
                self.addpowertreats()
        elif self.level == 3:
            if len(self.ghosts) < 18:
                self.addghosts()
            if len(self.treats) < 15:
                self.addtreats()
            if len(self.powertreats) < 5:
                self.addpowertreats()
        elif self.level == 4:
            if len(self.ghosts) < 21:
                self.addghosts()
            if len(self.treats) < 10:
                self.addtreats()
            if len(self.powertreats) < 7:
                self.addpowertreats()
        elif self.level == 5:
            if len(self.ghosts) < 24:
                self.addghosts()
            if len(self.treats) < 8:
                self.addtreats()
            if len(self.powertreats) < 9:
                self.addpowertreats()
        if self.myscore >= 100 and self.myscore < 200: #raises level
            self.level = 2
        elif self.myscore >= 200 and self.myscore < 300:
            self.level = 3
        elif self.myscore >= 300 and self.myscore < 400:
            self.level = 4
        elif self.myscore >= 400 and self.myscore < 500:
            self.level = 5
        p = 0
        if self.myscore % 10 == 0: #creates incremental change in direction for ghostboys 
            for i in self.ghosts:
                self.ghosts[p].direction = random.randint(1,4)
                p += 1
        if self.lives < 1:
            self.yellow_boy.leave()
            self.report("GAME OVER")
            self.GAME_OVER = True

        
        Game.update(self)
        self.display_score()
        self.display_lives()

            
game = Pacman()
while not game.GAME_OVER:
    time.sleep(1.0/60.0)
    game.update()
