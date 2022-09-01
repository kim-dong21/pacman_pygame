#Pacman in Python with PyGame
#https://github.com/hbokmann/Pacman
  
import pygame
import time
import math

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
yellow   = ( 255, 255,   0)

frozen_time=(5)
power_fireball_time=(10)
super_block_time=(5)


Trollicon=pygame.image.load("./images/Trollman.png")
pygame.display.set_icon(Trollicon)

#Add music
#pygame.mixer.init()
#pygame.mixer.music.load('E:/Pacman_py/Pacman/pacman.mp3')
#pygame.mixer.music.play(-1, 0.0)

# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.RenderPlain()
     
    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],
              [300,0,6,66],
              [60,60,186,6], 
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [120,180,126,6],
              [120,180,6,126],
              [360,180,126,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,240,6,66],
              [240,300,126,6],
              [360,240,6,66],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6]
            ]
     
    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)
        
    # return our new list
    return wall_list

def setupGate(all_sprites_list):
      gate = pygame.sprite.RenderPlain()
      gate.add(Wall(282,242,42,2,white))
      all_sprites_list.add(gate)
      return gate

# This class represents the ball        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])

        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect() 


#This is fireball class
class FireBall(Block):

  def __init__(self, color, width, height,p_dir,x,y):
    super().__init__(color, width, height)
    self.p_dir=p_dir
    self.rect.x=x
    self.rect.y=y

  def update(self):
    if self.p_dir=="RIGHT":
      self.rect.x+=30
    elif self.p_dir=="LEFT":
      self.rect.x-=30
    elif self.p_dir=="UP":
      self.rect.y-=30
    elif self.p_dir=="DOWN":
      self.rect.y+=30





# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):

    fireball_power_on=False
    super_power_on=False
    my_direction=""
    


    # Set speed vector
    change_x=0
    change_y=0


    #to check if the walls exist between pacman,ghosts
    def is_wall(self,gx,gy,walls):
      #x position
      
      for w in walls:
        
        print(w.x,w.y,w.width,w.height)
        #세로 벽인 경우
        if (w.width)==6:

          #벽이 고스트,팩맨 사이에 있는지 체크
          #Are they left side
          if self.rect.x<w.x and gx<w.x:
            print("wall left")
            return False
          #Are they right side
          elif self.rect.x > w.x and gx > w.x:
            print("wall right")
            return False

          #고스트,팩맨 사이에 벽이 존재하는 경우
          #벽의 세로 길이 내에 존재하는지 체크
          else:
            #팩맨,고스트가 벽의 세로 길이 내에 들어있는지 체크
            if (self.rect.y> w.y and self.rect.y<(w.y+w.height)) and (gy > w.y and gy<(w.y+w.height)):
              print("wall between")
              continue
            
            else:
              print("panic")
              return True
            



        else:
          #벽이 고스트,팩맨 사이에 있는지 체크
          #Are they up side
          if self.rect.y<w.y and gy<w.y:
            return False
          #Are they down side
          elif self.rect.y > w.y and gy > w.y:
            return False

          #고스트,팩맨 사이에 벽이 존재하는 경우
          #벽의 가로 길이 내에 존재하는지 체크
          else:
            #팩맨,고스트가 벽의 가로 길이 내에 들어있는지 체크
            if (self.rect.x> w.x and self.rect.x<(w.x+w.width)) and (gx > w.x and gx<(w.x+w.width)):
              continue
            
            else:
              return True
      #y position
      
        

    def is_panic_range(self,ghostx,ghosty,walls):

      #in panic range,It checks if the walls exist between Ghosts and pacman
        if self.rect.x+100>ghostx>self.rect.x-100 and self.rect.y==ghosty:
          if self.is_wall(ghostx,ghosty,walls):
            return False

          else:
            return True

        elif self.rect.y+100>ghosty>self.rect.y-100 and self.rect.x==ghostx:
          if self.is_wall(ghosty,ghosty,walls):
            return False

          else:
            return True

        else : 
          return False
      
      


    # Constructor function
    def __init__(self,x,y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert()
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
          
    # Find a new position for the player
    def update(self,walls,gate):
        # Get the old position, in case we need to go back to it
        
        old_x=self.rect.left
        new_x=old_x+self.change_x
        prev_x=old_x+self.prev_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        prev_y=old_y+self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left=old_x
            # self.rect.top=prev_y
            # y_collide = pygame.sprite.spritecollide(self, walls, False)
            # if y_collide:
            #     # Whoops, hit a wall. Go back to the old position
            #     self.rect.top=old_y
            #     print('a')
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top=old_y
                # self.rect.left=prev_x
                # x_collide = pygame.sprite.spritecollide(self, walls, False)
                # if x_collide:
                #     # Whoops, hit a wall. Go back to the old position
                #     self.rect.left=old_x
                #     print('b')

        if gate != False:
          gate_hit = pygame.sprite.spritecollide(self, gate, False)
          if gate_hit:
            self.rect.left=old_x
            self.rect.top=old_y

    def direction(self,key):
      if key == pygame.K_LEFT:
        self.my_direction="LEFT"
      if key == pygame.K_RIGHT:
        self.my_direction="RIGHT"
      if key == pygame.K_UP:
        self.my_direction="UP"
      if key == pygame.K_DOWN:
        self.my_direction="DOWN"

#Inheritime Player klassist
class Ghost(Player):
    

    #running away from pacman
    def panic(self,x,y,walls):

      collide=pygame.sprite.spritecollide(self,walls,False)

      #벽에 부딫힐시
      if collide:
        pass


      
      else :



        #팩맨과 x가 같은 줄
        if self.rect.x==x:
          #팩맨 y의 반대 방향으로 도망
          if self.rect.y<y:
            self.rect.y-=30
          else:
            self.rect.y+=30

        #팩맨과 y가 같은 줄
        elif self.rect.y==y:
          #팩맨 x의 반대 방향으로 도망 
          if self.rect.x<x:
            self.rect.x-=30
          else:
            self.rect.x+=30


    def reset_postion(self):
      self.rect.x=w
      self.rect.y=b_h
    
    # Change the speed of the ghost
    #list=Ghost_direction,ghost=False,l=방향 길이
    def changespeed(self,list,ghost,turn,steps,l):
      try:
        z=list[turn][2]#발걸음 수 가 저장된 배열
        #list속 지정된 발걸음을 넘으면 방향을 바꿈
        if steps < z:
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps+=1

        #방향을 계속 바꿔줌
        else:
          #배열 길이 내 인 경우
          if turn < l:
            turn+=1
          #현재 방향을 바꾸는 고스트가 Clyde인 경우
          elif ghost == "clyde":
            turn = 2
          #배열 밖인 경우
          else:
            turn = 0
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps = 0
        return [turn,steps]
      except IndexError:
         return [0,0]


#to Calculate fireball power time
fireball_second=0
fireball_start=0

#to calculate power block time 
power_second=0
power_start=0

#Calculate frozen time      
sec=0
start=0

def calc_frozen_time(end):
  global start
  global sec

  #start가 0인 경우 초기화, 아닌 경우 frozen 시작 시간 저장, 계산을 통해 시작 시각부터 현재까지의 5초 구함
  if start==0:
    start=time.time()

  sec=end-start
  sec=math.trunc(sec)
  print(sec)
  return sec

def calc_fire_power_time(end):
  global fireball_start
  global fireball_second

  if fireball_start==0:
    fireball_start=time.time()

  fireball_second=end-fireball_start
  fireball_second=math.trunc(fireball_second)
  print(fireball_second)
  return fireball_second


#팩맨 슈퍼파워 지속 시간 계산
def calc_power_time(end):
  global power_start
  global power_second

  if power_start==0:
    power_start=time.time()

  power_second=end-power_start
  power_second=math.trunc(power_second)
  print(power_second)
  return power_second





Pinky_directions = [
[0,-30,4],
[15,0,9],
[0,15,11],
[-15,0,23],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,19],
[0,15,3],
[15,0,3],
[0,15,3],
[15,0,3],
[0,-15,15],
[-15,0,7],
[0,15,3],
[-15,0,19],
[0,-15,11],
[15,0,9]
]

Blinky_directions = [
[0,-15,4],
[15,0,9],
[0,15,11],
[15,0,3],
[0,15,7],
[-15,0,11],
[0,15,3],
[15,0,15],
[0,-15,15],
[15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,3],
[-15,0,7],
[0,-15,3],
[15,0,15],
[0,15,15],
[-15,0,3],
[0,15,3],
[-15,0,3],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,11],
[0,-15,7],
[15,0,5]
]

Inky_directions = [
[30,0,2],
[0,-15,4],
[15,0,10],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,3],
[0,-15,15],
[-15,0,15],
[0,15,3],
[15,0,15],
[0,15,11],
[-15,0,3],
[0,-15,7],
[-15,0,11],
[0,15,3],
[-15,0,11],
[0,15,7],
[-15,0,3],
[0,-15,3],
[-15,0,3],
[0,-15,15],
[15,0,15],
[0,15,3],
[-15,0,15],
[0,15,11],
[15,0,3],
[0,-15,11],
[15,0,11],
[0,15,3],
[15,0,1],
]

Clyde_directions = [
[-30,0,2],
[0,-15,4],
[15,0,5],
[0,15,7],
[-15,0,11],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,7],
[0,15,15],
[15,0,15],
[0,-15,3],
[-15,0,11],
[0,-15,7],
[15,0,3],
[0,-15,11],
[15,0,9],
]

pl = len(Pinky_directions)-1
bl = len(Blinky_directions)-1
il = len(Inky_directions)-1
cl = len(Clyde_directions)-1

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'


# Set the title of the window
pygame.display.set_caption('Pacman')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(black)



clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

#default locations for Pacman and monstas
w = 303-16 #Width
p_h = (7*60)+19 #Pacman height
m_h = (4*60)+19 #Monster height
b_h = (3*60)+19 #Blinky height
i_w = 305-16-32 #Inky width
c_w = 301+(32-16) #Clyde width

def startGame():

  all_sprites_list = pygame.sprite.RenderPlain()

  block_list = pygame.sprite.RenderPlain()

  fire_block_list=pygame.sprite.RenderPlain()

  freeze_block_list=pygame.sprite.RenderPlain()

  super_block_list=pygame.sprite.RenderPlain()

  super_block_hit=pygame.sprite.RenderPlain()

  fire_bullet_list=pygame.sprite.RenderPlain()

  bullets=pygame.sprite.RenderPlain()

  Pinky_hit_list=pygame.sprite.RenderPlain()

  Blinky_hit_list=pygame.sprite.RenderPlain()

  Inky_hit_list=pygame.sprite.RenderPlain()

  Clyde_hit_list=pygame.sprite.RenderPlain()

  monsta_list = pygame.sprite.RenderPlain()

  pacman_collide = pygame.sprite.RenderPlain()

  wall_list = setupRoomOne(all_sprites_list)

  gate = setupGate(all_sprites_list)


  p_turn = 0
  
  p_steps = 0

  b_turn = 0
  b_steps = 0

  i_turn = 0
  i_steps = 0

  c_turn = 0
  c_steps = 0


  # Create the player paddle object
  Pacman = Player( w, p_h, "./images/pacman.png" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
  
  Blinky=Ghost( w, b_h, "./images/Blinky.png" )
  monsta_list.add(Blinky)
  all_sprites_list.add(Blinky)

  Pinky=Ghost( w, m_h, "./images/Pinky.png" )
  monsta_list.add(Pinky)
  all_sprites_list.add(Pinky)
   
  Inky=Ghost( i_w, m_h, "./images/Inky.png" )
  monsta_list.add(Inky)
  all_sprites_list.add(Inky)
   
  Clyde=Ghost( c_w, m_h, "./images/Clyde.png" )
  monsta_list.add(Clyde)
  all_sprites_list.add(Clyde)



  # Draw the grid
  for row in range(19):#0 1 2 3 4 5 6 9 10 ...
      for column in range(19):#0 1 2 3 4 5 6 7 11 12 ...
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue #Pass Ghosts house
          else:
            block = Block(yellow, 4, 4)
            fire_block=Block(red,10,10)
            freeze_block=Block(blue,10,10)
            super_block=Block(green,10,10)

            if ( row==14 and column==10):#fire block
              fire_block.rect.x=(30*column+6)+26
              fire_block.rect.y=(30*row+6)+26

              fire_block_list.add(fire_block)
              all_sprites_list.add(fire_block)
              

            elif (row==14 and column==11):#freeze block
              freeze_block.rect.x=(30*column+6)+26
              freeze_block.rect.y=(30*row+6)+26

              freeze_block_list.add(freeze_block)
              all_sprites_list.add(freeze_block)


            elif (row==14 and column==6):#super block
              super_block.rect.x=(30*column+6)+26
              super_block.rect.y=(30*row+6)+26

              super_block_list.add(super_block)
              all_sprites_list.add(super_block)

            else:
            # Set a random location for the block
              block.rect.x = (30*column+6)+26
              block.rect.y = (30*row+6)+26
              
            
            
            
            b_collide = pygame.sprite.spritecollide(block, wall_list, False)#벽과 충돌한 스프라이트 리스트 반환
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            

            if b_collide:
              continue
            elif p_collide:
              continue
            else:
                
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)
              
            
              
  

  bll = len(block_list)
  
  score = 0

  done = False


  frozen=False
  
  
  while done == False:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-30,0)
                  Pacman.direction(event.key)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(30,0)
                  Pacman.direction(event.key)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,-30)
                  Pacman.direction(event.key)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,30)
                  Pacman.direction(event.key)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-30)



      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
      
      

      
      
      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
      fire_block_hit=pygame.sprite.spritecollide(Pacman,fire_block_list,True)
      freeze_block_hit=pygame.sprite.spritecollide(Pacman,freeze_block_list,True)
      super_block_hit=pygame.sprite.spritecollide(Pacman,super_block_list,True)

      #Ghosts Hit by bullets logic
      Blinky_hit_list=pygame.sprite.spritecollide(Blinky,fire_bullet_list,True)
      Inky_hit_list=pygame.sprite.spritecollide(Inky,fire_bullet_list,True)
      Pinky_hit_list=pygame.sprite.spritecollide(Pinky,fire_bullet_list,True)
      Clyde_hit_list=pygame.sprite.spritecollide(Clyde,fire_bullet_list,True)

      #check the bullets collide to the walls
      pygame.sprite.groupcollide(wall_list,bullets,False,True)



      Pacman.update(wall_list,gate)

      if fire_block_hit:
        Pacman.fireball_power_on=True
        print("you ate fire ball")


      if Pacman.fireball_power_on:
        if power_fireball_time==calc_fire_power_time(time.time()):
          Pacman.fireball_power_on=False
        
        key=pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
          print("fire")
          bullet=FireBall(red,6,6,Pacman.my_direction,Pacman.rect.centerx,Pacman.rect.centery)
          fire_bullet_list.add(bullet)
          all_sprites_list.add(bullet)
          bullets.add(bullet)
      bullets.update()
        
      
      if Blinky_hit_list:
        Blinky.reset_postion()


      if Pinky_hit_list:
        Pinky.reset_postion()

      
      if Inky_hit_list:
        Inky.reset_postion()


      if Clyde_hit_list:
        Clyde.reset_postion()

      if freeze_block_hit:
        frozen=True
        
        
      if frozen:
        if frozen_time==calc_frozen_time(time.time()):
          #지속시간이 끝나면 초기화
          frozen=False
          
            

      else:

        if Pacman.super_power_on==True:
          if Pacman.is_panic_range(Blinky.rect.x,Blinky.rect.y,wall_list):
          
          #only Blinky is panic
            Blinky.panic(Pacman.rect.x,Pacman.rect.y,wall_list)
            print("Blinky panic")

          

          if Pacman.is_panic_range(Pinky.rect.x,Pinky.rect.y,wall_list):
          
          #only Pinky is panic
            Pinky.panic(Pacman.rect.x,Pacman.rect.y,wall_list)
            print("Pinky panic")
          

          if Pacman.is_panic_range(Inky.rect.x,Inky.rect.y,wall_list):
            Inky.panic(Pacman.rect.x,Pacman.rect.y,wall_list)
            print("Inky panic")
          


          if Pacman.is_panic_range(Clyde.rect.x,Clyde.rect.y,wall_list):
            Clyde.panic(Pacman.rect.x,Pacman.rect.y,wall_list)
            print("Clyde panic")
          
      
                                                    #p_turn=0,p_steps=0,pl=Pinky 방향 배열 길이
        returned = Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
        p_turn = returned[0]
        p_steps = returned[1]
        Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
        Pinky.update(wall_list,False)

        returned = Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
        b_turn = returned[0]
        b_steps = returned[1]
        Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
        Blinky.update(wall_list,False)

        returned = Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
        i_turn = returned[0]
        i_steps = returned[1]
        Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
        Inky.update(wall_list,False)

        returned = Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
        c_turn = returned[0]
        c_steps = returned[1]
        Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
        Clyde.update(wall_list,False)


      # See if the Pacman block has collided with anything.
      
      
      
      # Check the list of collisions.
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      


      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
   
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(black)
        
      wall_list.draw(screen)
      gate.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)

      text=font.render("Score: "+str(score)+"/"+str(bll), True, red)
      screen.blit(text, [10, 10])

      if score == bll:
        doNext("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)


      #팩맨 슈퍼블록 먹을시
      if super_block_hit:
        Pacman.super_power_on=True
        
      
      Blinky_hit=False
      Inky_hit=False
      Pinky_hit=False
      Clyde_hit=False

      #슈퍼파워 타임 동안 고스트들은 팩맥에게 먹힘
      if Pacman.super_power_on:


        Blinky_hit=pygame.sprite.collide_rect(Pacman,Blinky)
        Inky_hit=pygame.sprite.collide_rect(Pacman,Inky)
        Pinky_hit=pygame.sprite.collide_rect(Pacman,Pinky)
        Clyde_hit=pygame.sprite.collide_rect(Pacman,Clyde)


      if Blinky_hit:
        print("Blinky hit")
        Blinky.reset_postion()
        

      if Inky_hit:
        print("Inky hit")
        Inky.reset_postion()
        

      if Pinky_hit:
        print("Pinky hit")
        Pinky.reset_postion()

      if Clyde_hit:
        print("Clyde hit")
        Clyde.reset_postion()
        
      #수퍼타임 해제
      else:
        monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)


      if monsta_hit_list:
        doNext("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
      pygame.display.flip()
    
      clock.tick(10)

def doNext(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del pacman_collide
            del wall_list
            del gate
            startGame()


      #reset power time
      global power_start
      global fireball_start
      global start
      power_start=0
      fireball_start=0
      start=0

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1=font.render(message, True, white)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, white)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, white)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)

startGame()

pygame.quit()