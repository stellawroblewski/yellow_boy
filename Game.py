from tkinter import *
from geometry import Bounds, Point2D
import sys

class Agent:

    INTENSITIES = [4,5,6,7,8,7,6,5,4,3,2,1,0,1,2,3]

    def __init__(self,position,world):
        self.position = position
        self.world    = world 
        self.world.add(self)
        self.ticks    = 0

    def color(self):
        a = self.ticks % len(self.INTENSITIES)
        return "#0000"+str(self.INTENSITIES[a])+"0"

    def shape(self):
        p1 = self.position + Vector2D( 0.125, 0.125)       
        p2 = self.position + Vector2D(-0.125, 0.125)        
        p3 = self.position + Vector2D(-0.125,-0.125)        
        p4 = self.position + Vector2D( 0.125,-0.125)
        return [p1,p2,p3,p4]

    def update(self):
        self.ticks += 1

    def leave(self):
        self.world.remove(self)

class Game(Frame):

    # Game(name,w,h,ww,wh)
    #
    # Creates a world with a coordinate system of width w and height
    # h, with x coordinates ranging between -w/2 and w/2, and with y
    # coordinates ranging between -h/2 and h/2.
    # 
    # Creates a corresponding graphics window, for rendering 
    # the world, with pixel width ww and pixel height wh.
    #
    # The window will be named by the string given in name.
    #
    # The topology string is used by the 'trim' method to (maybe) keep
    # bodies within the frame of the world. (For example, 'wrapped' 
    # yields "SPACEWAR" topology, i.e. a torus.)
    #
    def __init__(self, name, w, h, ww, wh, topology = 'wrapped', console_lines = 0):

        # Register the world coordinate and graphics parameters.
        self.WINDOW_WIDTH = ww
        self.WINDOW_HEIGHT = wh
        self.bounds = Bounds(-w/2,-h/2,w/2,h/2)
        self.topology = topology

        # Populate the world with creatures
        self.agents = []
        self.GAME_OVER = False

        # Initialize the graphics window.
        self.root = Tk()
        self.root.title(name)
        Frame.__init__(self, self.root)
        self.canvas = Canvas(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)

        # Handle mouse pointer motion and keypress events.
        self.mouse_position = Point2D(0.0,0.0)
        self.mouse_down     = False
        self.bind_all('<Motion>',self.handle_mouse_motion)
        self.canvas.bind('<Button-1>',self.handle_mouse_press)
        self.canvas.bind('<ButtonRelease-1>',self.handle_mouse_release)
        self.bind_all('<Key>',self.handle_keypress)

        self.canvas.pack()
        if console_lines > 0:
            self.text = Text(self.root,height=console_lines,bg="#000000",fg="#A0F090",width=115)
            self.text.pack()
        else:
            self.text = None
        self.pack()

    def report(self,line=""):
        line += "\n"
        if self.text == None:
            print(line)
        else:
            self.text.insert(END,line)
            self.text.see(END)

    def trim(self,agent):
        if self.topology == 'wrapped':
            agent.position = self.bounds.wrap(agent.position)
        elif self.topology == 'bound':
            agent.position = self.bounds.clip(agent.position)
        elif self.topology == 'open':
            pass

    def add(self, agent):
        self.agents.append(agent)

    def remove(self, agent):
        self.agents.remove(agent)

    def update(self):
        for agent in self.agents:
            agent.update()
        self.clear()
        for agent in self.agents:
            self.draw_shape(agent.shape(),agent.color())
        Frame.update(self)

    def draw_shape(self, shape, color):
        wh,ww = self.WINDOW_HEIGHT,self.WINDOW_WIDTH
        h = self.bounds.height()
        x = self.bounds.xmin
        y = self.bounds.ymin
        points = [ ((p.x - x)*wh/h, wh - (p.y - y)* wh/h) for p in shape ]
        first_point = points[0]
        points.append(first_point)
        self.canvas.create_polygon(points, fill=color)

    def clear(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, fill="#000000")

    def window_to_world(self,x,y):
        return self.bounds.point_at(x/self.WINDOW_WIDTH, 1.0-y/self.WINDOW_HEIGHT)

    def handle_mouse_motion(self,event):
        self.mouse_position = self.window_to_world(event.x,event.y)
        #print("MOUSE MOVED",self.mouse_position,self.mouse_down)

    def handle_mouse_press(self,event):
        self.mouse_down = True
        self.handle_mouse_motion(event)
        #print("MOUSE CLICKED",self.mouse_down)

    def handle_mouse_release(self,event):
        self.mouse_down = False
        self.handle_mouse_motion(event)
        #print("MOUSE RELEASED",self.mouse_down)

    def handle_keypress(self,event):
        if event.char == 'q':
            self.GAME_OVER = True
