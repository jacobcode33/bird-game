## this will aim to create a bird which can be controlled by the user
## cute and kinda physics based

from graphics import *
import math, time, random
import keyboard

def draw(creatures, camx, camy, drops):
    global fakehealth
    global screenwidth
    
    if round(health) < round(fakehealth):
        fakehealth -= 0.5
    def limb(p,width):
        for i in range(len(p)-1):
            line = Line(Point(p[i][0], p[i][1]), Point(p[i+1][0], p[i+1][1]))
            line.setWidth(width-i*width/(1.5*len(p))) #width-ik  width/2 = k(len(p))
            line.draw(canvas)
            joint = Circle(Point(p[i+1][0], p[i+1][1]), width/2-1-i*width/(3*len(p)))# rounded joints
            joint.setFill("Black")
            joint.draw(canvas)

    for o in range(len(creatures)):
        b = creatures[o].body
        wl = creatures[o].wingl
        wr = creatures[o].wingr
        t = creatures[o].trail
        p = [] ## point of drawing
        for i in range(len(b)): # change to relative pos
            p.append([b[i][0]+camx, -b[i][1]+camy])
        if creatures[o].type == "player":
            limb(p, 15)
        else:
            limb(p, 6.5)
        
        p = []
        for i in range(len(wl)): # repeat for wl
            p.append([wl[i][0]+camx, -wl[i][1]+camy])
        limb(p, 10)
        
        p = []
        for i in range(len(wr)): # repeat for wr
            p.append([wr[i][0]+camx, -wr[i][1]+camy])
        limb(p, 10)

        if creatures[o].type == "player":
            head = Circle(Point(b[0][0]+camx, -b[0][1]+camy), 9)
        else:
            head = Circle(Point(b[0][0]+camx, -b[0][1]+camy), 4)
        head.setFill("Black")
        head.draw(canvas)

        for i in range(len(t)):
            trail = Circle(Point(t[i][0]+camx, -t[i][1]+camy), 1)
            shade = round(255 - i*(250/20))
            shade = 0
            trail.setFill(color_rgb(shade,shade,shade))
            trail.draw(canvas)

    frames = Text(Point(30,40), str(round(fps)))
    frames.draw(canvas)
    healthbar = Rectangle(Point(screenwidth/2-100, 30), Point(screenwidth/2+100, 60))
    healthbar.setFill("white")
    healthbar.draw(canvas)
    bar = Rectangle(Point(screenwidth/2-100, 30), Point(screenwidth/2-100+fakehealth*2, 60))
    bar.setFill("black")
    bar.draw(canvas)

    #for i in range(len(drops)):
        #line = Line(Point(drops[i].x, drops[i].y), Point(drops[i].x, drops[i].y-random.randint(35,50)))
        #line.draw(canvas)

def refresh():
    canvas.update()
    for item in canvas.items[:]:
          item.undraw()

def movecam(camx, camy, focus, w, h, speed):
    speed -= 3800/(fps**0.8)
    speed /= 500/fps
    if speed > 0:
        camx += random.uniform(-speed, speed)
        camy += random.uniform(-speed, speed) #for shake
    camx += ((w/2-focus[0])-camx)*0.8/fps # set both to 1 for full follow
    camy += ((focus[1]+h/2)-camy)*3/fps # set both to 9999999999 for no follow
    return(camx, camy)

class bird:    
    def __init__(self, Type, x, y):
        def create(Type, x, y):
            b = [] ## create the self.body
            wl = [] #left wing
            wr = [] # right wing
            if Type == "player":
                for i in range(6):
                    b.append([0, i*-10]) ## this is real position (ignoring camera)
                for i in range(5):
                    wl.append([0, i*-8])
                    wr.append([0, i*-8])
            elif Type == "dim":
                for i in range(3):
                    b.append([x, y+i*-10])
            return(b, wl, wr)
        
        self.body,self.wingl,self.wingr = create(Type,x,y)
        self.type = Type
        if self.type == "player":
            self.lastl = self.wingl[len(self.wingl)-1][1]-self.body[1][1]
            self.lastr = self.wingr[len(self.wingr)-1][1]-self.body[1][1]
        self.velocity = [0,0]
        self.trail = []
        self.live = True

    def nextframe(self):
        def move(points, length, external): # copied from chain (another project)
            def direction(p1, p2):
                dis = math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
                dx = p1[0]-p2[0]
                dy = p1[1]-p2[1]
                angle = [(dx/dis), (dy/dis)] # its not really an angle
                return(angle)

            def shorten(angle, p1, length):
                p2 = [p1[0]-(angle[0]*length), p1[1]-(angle[1]*length)]
                return(p2)


            for i in range(len(points)-1):
                points[i+1][0] += external[0]+random.uniform(-0.001,0.001) # external forces of gravity and muscle affect it
                points[i+1][1] += external[1]+random.uniform(-0.001,0.001)
                angle = direction(points[i], points[i+1])
                points[i+1] = shorten(angle, points[i], length)
            return(points)

        def choose(s):
            if self.type == "player" and self.live:
                l = [-0.14*s,-0.67*s]
                r = [0.14*s,-0.67*s]
                if keyboard.is_pressed("left arrow"):
                    l = [-0.24*s,0.6*s]
                if keyboard.is_pressed("right arrow"):
                    r = [0.24*s,0.6*s]
            elif not self.live:
                if random.randint(0,5) == 0:
                    l = [random.uniform(-s,s), random.uniform(-s,s)]
                    r = [random.uniform(-s,s), random.uniform(-s,s)]
                else:
                    l = [0,0]
                    r = [0,0]
            return([l,r])
        
        self.body[0][0] += self.velocity[0]/20 # move the entire body based on previous velocity
        self.body[0][1] += self.velocity[1]/20
        
        if self.type == "dim": # move the dim blob
            if self.live:
                self.velocity[0] *= 0.997
                self.velocity[1] *= 0.997
                
                difx = creatures[0].body[2][0] - self.body[0][0] + random.randint(-50, 50)
                dify = creatures[0].body[2][1] - self.body[0][1] + random.randint(-50, 50)
                self.velocity[0] += difx/3000
                self.velocity[1] += dify/3000
                self.body = move(self.body, 10, [0,-gravity])
            else:
                self.velocity[0] *= 0.999
                self.velocity[1] *= 0.999
                #self.velocity[0] += random.randint(-2,2)
                self.velocity[1] -= gravity/2
                self.body = move(self.body, 10, [0,-gravity])

        elif self.type == "player":
            self.velocity[1] *= 0.9988 + (self.wingl[len(self.wingl)-1][0]-self.wingr[len(self.wingl)-1][0])/13000 # further out wings = more resistance
            self.velocity[0] *= 0.998 # air resistance
            
            musclel, muscler = choose(382/fps) # take inputs to affect wings
            self.body = move(self.body, 10, [0,-gravity]) # body acts like a rope
            self.wingl[0], self.wingr[0] = self.body[1], self.body[1] # bring start of each wing to neck of body
            self.wingl = move(self.wingl, 8, [musclel[0],musclel[1]-gravity]) # move wings based on forces
            self.wingr = move(self.wingr, 8, [muscler[0],muscler[1]-gravity])

            self.difr = (self.wingr[len(self.wingr)-1][1]-self.body[1][1])-self.lastr # this section calculates current velocity based on wing movement
            self.difr /= 2.5
            if self.difr > 0:
                self.difr /= 10
            self.velocity[1] -= self.difr*1.1
            self.velocity[0] += self.difr*0.44
            
            self.difl = (self.wingl[len(self.wingl)-1][1]-self.body[1][1])-self.lastl
            self.difl /= 2.5
            if self.difl > 0:
                self.difl /= 10
            self.velocity[1] -= self.difl*1.1
            self.velocity[0] -= self.difl*0.44

            self.velocity[1] -= gravity/4.5 # whole body goes down
            
            self.lastl = self.wingl[len(self.wingl)-1][1]-self.body[1][1]
            self.lastr = self.wingr[len(self.wingr)-1][1]-self.body[1][1]

            if random.randint(-1,round(35/abs(self.difl*fps))) == 0:
                self.trail.append(self.wingl[len(self.wingl)-1])
            if random.randint(-1,round(35/abs(self.difr*fps))) == 0:
                self.trail.append(self.wingr[len(self.wingr)-1])
            if len(self.trail) > 0 and (random.randint(0,15) == 0 or fps < 80):
                self.trail.pop(0)
            if len(self.trail) > 8:
                self.trail.pop(0)

class rain:
    def __init__(self):
        self.x = random.randint(0,500)
        self.y = random.randint(-40,10)
        self.state = True
    
    def down(self, speed):
        if self.y > 540:
            self.__init__()
        self.y += speed

def newblob():
    x = creatures[0].velocity[0]+random.uniform(-5,5)
    y = creatures[0].velocity[1]+random.uniform(-5,5)
    dis = math.sqrt(x**2+y**2)
    spawndis = math.sqrt(screenwidth**2+screenheight**2)
    x *= spawndis/dis
    y *= spawndis/dis
    x += creatures[0].body[0][0]
    y += creatures[0].body[0][1]
    creatures.append(bird("dim",x,y))

def collisions():
    global health
    def bounce(v1, v2, p1, p2, s):
        dis = math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
        angle = [(p1[0]-p2[0]),(p1[1]-p2[1])]
        angle = [angle[0]/dis, angle[1]/dis]
        v1[0] += angle[0]*s
        v1[1] += angle[1]*s
        v2[0] -= angle[0]*s
        v2[1] -= angle[1]*s
        return(v1,v2)
        
    global fps

    kill = []
    for i in range(len(creatures)):
        for o in range(len(creatures)):
            if i != o and creatures[i].live and creatures[o].live:
                xi = creatures[i].body[math.floor(len(creatures[i].body)/2)][0] # the middle of the body
                yi = creatures[i].body[math.floor(len(creatures[i].body)/2)][1]
                xo = creatures[o].body[math.floor(len(creatures[o].body)/2)][0]
                yo = creatures[o].body[math.floor(len(creatures[o].body)/2)][1]
                dis = math.sqrt((xi-xo)**2+(yi-yo)**2)
                if dis < 80: # heuristic to only proceed to high processing check when theyre close
                    #fps *= 0.999 # anticipating this slowing everything down (could make this into an intentional slow mo effect)
                    if creatures[i].type == "player":
                        #check for head
                        xi = creatures[i].body[0][0]
                        yi = creatures[i].body[0][1]
                        xo = creatures[o].body[0][0] # only the top of body
                        yo = creatures[o].body[0][1]
                        dis = math.sqrt((xi-xo)**2+(yi-yo)**2)
                        if dis < 13: #(4+9)
                            health -= random.randint(5,20)
                            if health <= 0:
                                health = 0
                                creatures[i].live = False
                            creatures[o].live = False
                            while len(creatures[o].body) > 1:
                                creatures[o].body.pop(0)
                                creatures[i].velocity, creatures[o].velocity = bounce(creatures[i].velocity, creatures[o].velocity, creatures[i].body[0], creatures[o].body[0], 15)
                        for u in range(len(creatures[i].body)): # for each of the joints of body
                            pass
                                
                    elif creatures[o].type != "player": # two blobs collide head on head
                        xi = creatures[i].body[0][0] # both heads
                        yi = creatures[i].body[0][1]
                        xo = creatures[o].body[0][0]
                        yo = creatures[o].body[0][1]
                        dis = math.sqrt((xi-xo)**2+(yi-yo)**2)
                        if dis < 8: #(4+4)
                            creatures[i].live = False
                            creatures[o].live = False
                            creatures[i].velocity, creatures[o].velocity = bounce(creatures[i].velocity, creatures[o].velocity, creatures[i].body[0], creatures[o].body[0], 10)
                            while len(creatures[i].body) > 1:
                                creatures[i].body.pop(0)
                            while len(creatures[o].body) > 1:
                                creatures[o].body.pop(0)
            else:
                xi = creatures[0].body[0][0] ## assumes that the only player is pos 0
                yi = creatures[0].body[0][1]
                xo = creatures[i].body[0][0]
                yo = creatures[i].body[0][1]
                dis = math.sqrt((xi-xo)**2+(yi-yo)**2)
                if dis > 3000:
                    if i not in kill:
                        kill.append(i)
    kill.sort(reverse = True)
    for i in range(len(kill)):
        creatures.pop(kill[i])



screenwidth = 1080
screenheight = 720
canvas = GraphWin("canvas", screenwidth, screenheight, autoflush = False)
canvas.setBackground (color_rgb(255, 255, 255))

camerax = screenwidth / 2
cameray = screenheight / 2
creatures = [] # first in list is player
creatures.append(bird("player",0,0))
drops = [] # not using rain currently
newblob()

lastadded = time.time()
lasttime = time.time()
fps = 80
count = 0
health = 100
fakehealth = 100
while True:
    gravity = 105/fps
    count += 1
    if count % 30 == 0: # dont check every time to make more efficient
        timedif = time.time()-lasttime # 30 per (amount of time) 30*(1/amount of time)
        fps = (fps+30/timedif)/2
        lasttime = time.time()
        if time.time() > lastadded+1:
            newblob()
            lastadded = time.time()
    for i in range(len(creatures)):
        creatures[i].nextframe()
    #for i in range(len(drops)):
    #    drops[i].down(25)
    camerax, cameray = movecam(camerax, cameray, creatures[0].body[0], screenwidth, screenheight, math.sqrt(creatures[0].velocity[0]**2+creatures[0].velocity[1]**2))
    draw(creatures, camerax, cameray, drops)
    collisions()
    refresh()
