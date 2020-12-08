from cmu_112_graphics import *
import socket
import threading
import pickle

class MyApp(App):

    class Units(object):
        def __init__(self,health,attack,movespd,range,cost):
            self.health = health   # current hp of the unit
            self.maxHealth = health # original hp of the unit
            self.attack = attack   # the damage per attack
            self.moveSpeed = movespd   # how fast the unit moves
            self.range = range   # how far the unit can attack
            self.cost = cost   # how much the unit will cost
            self.state = 'walk'   # what the unit is doing
            self.spriteCounter = 0  # for animation purposes

# the different tuples represent which frame range is used    
    class Bat(Units):
        spritesheet = 0
        
        def __init__(self):
            super().__init__(8,1,40,0,200)
            self.type = 'light'
            
        def action(self):
            if self.state == 'walk':
                return (0,4)
            elif self.state == 'fight':
                return (38,42)

    class Owl(Units):
        spritesheet = 1
        def __init__(self): 
            super().__init__(7,2,25,200,250)
            self.projectile = 1   # number represents index of the sprite in self.projectiles
            self.type = 'light'
        
        def action(self):
            if self.state == 'walk':
                return (0,9)
            elif self.state == 'fight':
                return (9,21)
                    
    class Peacock(Units):
        spritesheet = 2
        def __init__(self):
            super().__init__(12,7,20,0,250)
            self.type = 'midweight'

        def action(self):
            if self.state == 'walk':
                return (27,36)
            elif self.state == 'fight':
                return (36,50)
                
    class Rat(Units):
        spritesheet = 3
        def __init__(self): 
            super().__init__(30,10,10,0,700)
            self.type = 'heavy'

        def action(self):
            if self.state == 'walk':
                return (9,18)
            elif self.state == 'fight':
                return (18,32)

    class Anubis(Units):
        spritesheet = 4
        def __init__(self): 
            super().__init__(15,2,20,0,200)
            self.type = 'midweight'

        def action(self):
            if self.state == 'walk':
                return (42,48)
            elif self.state == 'fight':
                return (2,6)
    
    class Knight(Units):
        spritesheet = 5
        def __init__(self): 
            super().__init__(12,2,30,250,300)
            self.projectile = 0
            self.type = 'midweight'

        def action(self):
            if self.state == 'walk':
                return (0,5)
            elif self.state == 'fight':
                return (11,13)
    
    class Slime(Units):
        spritesheet = 6
        def __init__(self): 
            super().__init__(30,6,15,0,250)
            self.type = 'heavy'

        def action(self):
            if self.state == 'walk':
                return (9,14)
            elif self.state == 'fight':
                return (21,26)

    class Spore(Units):
        spritesheet = 7
        def __init__(self): 
            super().__init__(50,8,45,0,800)
            self.type = 'light'

        def action(self):
            if self.state == 'walk':
                return (27,36)
            elif self.state == 'fight':
                return (0,5)
    
    class EarthWorm(Units):
        spritesheet = 8
        def __init__(self): 
            super().__init__(12,1,35,0,150)
            self.type = 'light'

        def action(self):
            if self.state == 'walk':
                return (18,27)
            elif self.state == 'fight':
                return (3,5)
    
    class Golem(Units):
        spritesheet = 9
        def __init__(self): 
            super().__init__(35,8,10,0,275)
            self.type = 'heavy'

        def action(self):
            if self.state == 'walk':
                return (6,11)
            elif self.state == 'fight':
                return (18,27)
    
    class Phoenix(Units):
        spritesheet = 10
        def __init__(self): 
            super().__init__(20,10,25,300,300)
            self.projectile = 4
            self.type = 'midweight'

        def action(self):
            if self.state == 'walk':
                return (27,36)
            elif self.state == 'fight':
                return (9,18)
    
    class WereWolf(Units):
        spritesheet = 11
        def __init__(self): 
            super().__init__(40,6,50,0,800)
            self.type = 'light'

        def action(self):
            if self.state == 'walk':
                return (0,6)
            elif self.state == 'fight':
                return (12,15)
    
    class DoppelSlime(Units):
        spritesheet = 12
        def __init__(self): 
            super().__init__(20,10,20,0,225)
            self.type = 'heavy'

        def action(self):
            if self.state == 'walk':
                return (15,21)
            elif self.state == 'fight':
                return (9,18)
    
    class Slayer(Units):
        spritesheet = 13
        def __init__(self): 
            super().__init__(23,6,30,0,300)
            self.projectile = 2
            self.type = 'light'

        def action(self):
            if self.state == 'walk':
                return (27,35)
            elif self.state == 'fight':
                return (11,15)
    
    class Whale(Units):
        spritesheet = 14
        def __init__(self): 
            super().__init__(50,6,20,0,375)
            self.type = 'heavy'

        def action(self):
            if self.state == 'walk':
                return (36,45)
            elif self.state == 'fight':
                return (2,7)

    class Wyvern(Units):
        spritesheet = 15
        def __init__(self): 
            super().__init__(50,20,30,275,800)
            self.projectile = 5
            self.type = 'midweight'

        def action(self):
            if self.state == 'walk':
                return (0,8)
            elif self.state == 'fight':
                return (36,42)

    class Angel(Units):
        spritesheet = 16
        def __init__(self): 
            super().__init__(30,9,25,150,250)
            self.type = 'midweight'

        def action(self):
            if self.state == 'walk':
                return (27,36)
            elif self.state == 'fight':
                return (0,9)
    
    class Boss(Units):
        spritesheet = 17
        def __init__(self): 
            super().__init__(37,6,15,0,300)
            self.type = 'heavy'

        def action(self):
            if self.state == 'walk':
                return (27,36)
            elif self.state == 'fight':
                return (0,7)
    
    class Overmind(Units):
        spritesheet = 18
        def __init__(self): 
            super().__init__(25,5,40,0,300)
            self.type = 'light'

        def action(self):
            if self.state == 'walk':
                return (5,13)
            elif self.state == 'fight':
                return (4,7)
    
    class Spike(Units):
        spritesheet = 19
        def __init__(self): 
            super().__init__(65,17,30,400,1000)
            self.projectile = 3
            self.type = 'light'

        def action(self):
            if self.state == 'walk':
                return (0,9)
            elif self.state == 'fight':
                return (9,15)

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

currentID = "0" 
client0Lists=[]
client1Lists=[]

def handleClient(conn, addr):
    global currentID, client0Lists,client1Lists
    yourID = currentID
    currentID = "1"

    connected = True
    while connected: 
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = pickle.loads(conn.recv(msgLength))
            if msg == DISCONNECT:
                connected = False
            if yourID == '0':
                if msg == 'REQUEST':
                    message = pickle.dumps(client1Lists)
                    messageLength = len(message)
                    sendLength = str(messageLength).encode(FORMAT)
                    sendLength += b' ' * (HEADER - len(sendLength))
                    conn.send(sendLength)
                    conn.send(message)
                else:
                    client0Lists = msg
            elif yourID == '1':
                if msg == 'REQUEST':
                    message = pickle.dumps(client0Lists)
                    messageLength = len(message)
                    sendLength = str(messageLength).encode(FORMAT)
                    sendLength += b' ' * (HEADER - len(sendLength))
                    conn.send(sendLength)
                    conn.send(message)
                else:
                    client1Lists = msg
        
def start():
    server.listen(2)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target= handleClient, args = (conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')

print('Server is starting!')
start()

