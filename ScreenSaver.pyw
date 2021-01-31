import math
import pygame
import random
import sys
import time

pygame.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("ScreenSaverThingy")
HORIZONTAL=1920
VERTICAL=1080
SCREEN=pygame.display.set_mode([HORIZONTAL,VERTICAL],pygame.FULLSCREEN)
FONT=pygame.font.SysFont("hack",15)
COLORS=[]
COLORS.append((255,255,255)) # White
COLORS.append((0,0,0)) # Black
COLORS.append((255,0,0)) # Red
COLORS.append((0,255,0)) # Green
COLORS.append((0,0,255)) # Blue
COLORS.append((255,255,0)) # Yellow
COLORS.append((0,255,255)) # Cyan
COLORS.append((255,0,255)) # Magneta
COLORS.append((127,0,0)) # Maroon 
COLORS.append((0,127,0)) # Fern
COLORS.append((0,0,127)) # Navy
COLORS.append((127,127,0)) # Olive
COLORS.append((0,127,127)) # Teal
COLORS.append((127,0,127)) # Purple
COLORS.append((255,127,0)) # Orange
COLORS.append((0,255,127)) # Mint
COLORS.append((127,0,255)) # Violet
COLORS.append((127,255,0)) # Chartreuse
COLORS.append((0,127,255)) # Azure
COLORS.append((255,0,127)) # Pink
NEIGHBORS={} # Lookup table for life-like cellular automata adjacent cells
for col in range(HORIZONTAL//10):
   for row in range(VERTICAL//10):
      left=col-1
      if left<0:
         left=HORIZONTAL//10-1
      right=col+1
      if right>=HORIZONTAL//10:
         right=0
      top=row-1
      if top<0:
         top=VERTICAL//10-1
      bottom=row+1
      if bottom>=VERTICAL//10:
         bottom=0
      NEIGHBORS[(col,row)]=((left,top),(left,row),(left,bottom),(col,top),(col,bottom),(right,top),(right,row),(right,bottom))
LIFELIKE=[] # Some of the nicer looking life-like cellular automata rule sets
LIFELIKE.append(([1,1,1,1,1,1,1,1,1],[0,0,0,1,0,0,0,0,0])) # B3/S012345678
LIFELIKE.append(([0,0,1,1,0,0,0,0,0],[0,0,0,1,0,0,0,0,0])) # B3/S23
LIFELIKE.append(([0,1,1,0,0,1,0,0,0],[0,0,0,1,0,0,1,0,0])) # B36/S125
LIFELIKE.append(([0,0,1,1,0,0,0,0,0],[0,0,0,1,0,0,1,0,0])) # B36/S23
LIFELIKE.append(([0,0,0,1,0,1,1,1,1],[0,0,0,0,1,0,1,1,1])) # B4678/S35678
LIFELIKE.append(([0,0,1,1,0,0,0,0,1],[0,0,0,1,0,1,0,1,0])) # B357/S238
LIFELIKE.append(([0,0,0,1,1,1,1,0,1],[0,0,0,0,0,1,1,1,1])) # B5678/S34568
LIFELIKE.append(([0,0,0,1,1,1,0,0,0],[0,0,0,1,0,0,0,0,0])) # B3/S345
LIFELIKE.append(([0,0,1,1,1,1,0,1,1],[0,0,0,1,0,1,0,0,0])) # B35/S234578
LIFELIKE.append(([0,1,1,1,1,0,0,0,0],[0,0,0,1,0,0,0,0,0])) # B3/S1234
LIFELIKE.append(([0,1,1,1,1,1,0,0,0],[0,0,0,1,0,0,0,0,0])) # B3/S12345

def ant():
   rule=[]
   for i in range(random.randint(1,19)):
      searchType=random.random()
      if searchType<.5: # Good chance for left/right
         rule.append(random.randint(0,1))
      elif .5<=searchType<.8: # Smaller chance for forwards/backwards
         rule.append(random.randint(2,3))
      else: # Smallest chance for cardinal directions
         rule.append(random.randint(4,7))
   info=''.join(['L' if i==0 else 'R' if i==1 else 'F' if i==2 else 'B' if i==3 else 'N' if i==4 else 'E' if i==5 else 'S' if i==6 else 'W' for i in rule])
   grid=[[1 for row in range(VERTICAL//10)] for col in range(HORIZONTAL//10)]
   antCol=HORIZONTAL//10//2
   antRow=VERTICAL//10//2
   antDir=0
   step=0
   displaySquare([(antCol,antRow,0)],info,step,5)
   while step<100000:
      step+=1
      antDir=antDirection(antDir,rule,grid[antCol][antRow]-1)
      grid[antCol][antRow]+=1
      if grid[antCol][antRow]==len(rule)+1:
         grid[antCol][antRow]=1
      oldCol=antCol
      oldRow=antRow
      if antDir==0:
         antCol-=1
      elif antDir==1:
         antRow-=1
      elif antDir==2:
         antCol+=1
      else:
         antRow+=1
      if antCol==-1:
         antCol=HORIZONTAL//10-1
      elif antCol==HORIZONTAL//10:
         antCol=0
      if antRow==-1:
         antRow=VERTICAL//10-1
      elif antRow==VERTICAL//10:
         antRow=0
      displaySquare(((antCol,antRow,0),(oldCol,oldRow,grid[oldCol][oldRow])),info,step,5)
 
def antDirection(antDir,rule,color):
   if rule[color]==0:
      return (antDir-1)%4
   elif rule[color]==1:
      return (antDir+1)%4
   elif rule[color]==2:
      return antDir
   elif rule[color]==3:
      return (antDir+2)%4
   elif rule[color]==4:
      return 1
   elif rule[color]==5:
      return 2
   elif rule[color]==6:
      return 3
   else:
      return 0
 
def wolfram():
   rule=random.randint(0,255)
   info=f'Rule {rule}'
   rule=[int(i) for i in bin(rule)[2:].zfill(8)]
   grid=[[0 for row in range(VERTICAL//10)] for col in range(HORIZONTAL//10)]
   step=0
   searchType=random.randint(0,2)
   if searchType==0:
      grid[HORIZONTAL//10//2][step]=1
   elif searchType==1:
      for col in range(random.randint(2,5)):
         grid[random.randint(0,HORIZONTAL//10)][step]=1
   else:
      for col in range(HORIZONTAL//10):
         grid[col][step]=random.randint(0,1)
   displaySquare([(col,step,0) for col in range(HORIZONTAL//10) if grid[col][step]==1],info,step,1)
   while step<VERTICAL//10-1:
      time.sleep(.1)
      step+=1
      changes=[]
      for col in range(HORIZONTAL//10):
         pattern=''
         if col==0:
            pattern+=str(grid[HORIZONTAL//10-1][step-1])
         else:
            pattern+=str(grid[col-1][step-1])
         pattern+=str(grid[col][step-1])
         if col==HORIZONTAL//10-1:
            pattern+=str(grid[0][step-1])
         else:
            pattern+=str(grid[col+1][step-1])
         grid[col][step]=rule[7-int(pattern,2)]
         if grid[col][step]==1:
            changes.append((col,step,0))
      displaySquare(changes,info,step,1)

def life():
   lifeType=random.randrange(7)
   info='B'
   for rule in enumerate(LIFELIKE[lifeType][1]):
      if rule[1]:
         info+=str(rule[0])
   info+='/S'
   for rule in enumerate(LIFELIKE[lifeType][0]):
      if rule[1]:
         info+=str(rule[0])
   grid=generateSeed(lifeType)
   changeSet=set()
   step=0
   displaySquare([(col,row,grid[col][row][0]) for col in range(HORIZONTAL//10) for row in range(VERTICAL//10)],info,step,1)
   while step<2000:
      time.sleep(.01)
      step+=1
      changes=stepLife(grid,lifeType)
      if tuple(changes) in changeSet: # Once it dies or loops, exit
         break
      changeSet.add(tuple(changes))
      displaySquare([(change[0],change[1],change[2]) for change in changes],info,step,1) 

def maze():
   searchType=random.randrange(3)
   if searchType==0:
      info='BFS'
   elif searchType==1:
      info='Bidirectional BFS'
   else:
      info='A*'
   lifeType=random.randint(7,10)
   grid=generateSeed(lifeType)
   changeSet=set()
   displaySquare([(col,row,grid[col][row][0]) for col in range(HORIZONTAL//10) for row in range(VERTICAL//10)],info,0,1)
   while True: # Maze-type cellular automata will eventually settle or loop
      time.sleep(.01)
      changes=stepLife(grid,lifeType)
      if tuple(changes) in changeSet: # This means it's ready to "maze" over
         break
      changeSet.add(tuple(changes))
      displaySquare([(change[0],change[1],change[2]) for change in changes],info,0,1)
   possibleStarts=set()
   possibleEnds=set()
   for col in range(HORIZONTAL//10):
      for row in range(VERTICAL//10):
         if col!=0 and row!=0 and col!=HORIZONTAL//10-1 and row!=VERTICAL//10-1:
            grid[col][row]=grid[col][row][0] # Can disregard neighbor count now
            if not grid[col][row]: # Also looks for possible start and end positions
               if col<10:
                  possibleStarts.add((col,row))
               elif col>=HORIZONTAL//10-10:
                  possibleEnds.add((col,row))
         else: # Constrains the maze edges so the taxicab heuristic works
            grid[col][row]=1
            displaySquare([(col,row,1)],info,0,1)
   displaySquare([(col,row,grid[col][row]) for col in range(HORIZONTAL//10) for row in range(VERTICAL//10)],info,0,1)
   if not possibleStarts or not possibleEnds:
      return
   start=random.choice([*possibleStarts])
   end=random.choice([*possibleEnds])
   displaySquare([(start[0],start[1],3),(end[0],end[1],2)],info,0,1)
   if searchType==0: # BFS
      queue=[start]
      visited={start:start}
      step=0
      while queue:
         parent=queue.pop(0)
         step+=1
         if parent!=start:
            displaySquare([(parent[0],parent[1],2)],info,step,1)
         for neighbor in NEIGHBORS[parent]:
            if neighbor not in visited:
               visited[neighbor]=parent
               if neighbor==end:
                  path=visited[end]
                  while path!=start:
                     time.sleep(.01)
                     displaySquare([(path[0],path[1],4)],info,step,1)
                     path=visited[path]
                  return
               if grid[neighbor[0]][neighbor[1]]==0:
                  queue.append(neighbor)
   elif searchType==1: # Bidirectional BFS
      startQueue=[start]
      endQueue=[end]
      startVisited={start:start}
      endVisited={end:end}
      step=0
      while startQueue and endQueue:
         startParent=startQueue.pop(0)
         step+=1
         if startParent!=start:
            displaySquare([(startParent[0],startParent[1],2)],info,step,1)
         for neighbor in NEIGHBORS[startParent]:
            if neighbor not in startVisited:
               startVisited[neighbor]=startParent
               if neighbor in endVisited:
                  displaySquare([(neighbor[0],neighbor[1],4)],info,step,1)
                  startPath=startVisited[neighbor]
                  endPath=endVisited[neighbor]
                  while startPath!=start or endPath!=end:
                     time.sleep(.01)
                     displaySquare([(startPath[0],startPath[1],4),(endPath[0],endPath[1],4)],info,step,1)
                     startPath=startVisited[startPath]
                     endPath=endVisited[endPath]
                  return
               if grid[neighbor[0]][neighbor[1]]==0:
                  startQueue.append(neighbor)
         endParent=endQueue.pop(0)
         step+=1
         if endParent!=end:
            displaySquare([(endParent[0],endParent[1],3)],info,step,1)
         for neighbor in NEIGHBORS[endParent]:
            if neighbor not in endVisited:
               endVisited[neighbor]=endParent
               if neighbor in startVisited:
                  displaySquare([(neighbor[0],neighbor[1],4)],info,step,1)
                  startPath=startVisited[neighbor]
                  endPath=endVisited[neighbor]
                  while startPath!=start or endPath!=end:
                     time.sleep(.01)
                     displaySquare([(startPath[0],startPath[1],4),(endPath[0],endPath[1],4)],info,step,1)
                     startPath=startVisited[startPath]
                     endPath=endVisited[endPath]
                  return
               if grid[neighbor[0]][neighbor[1]]==0:
                  endQueue.append(neighbor)
   else: # A* (Manhattan distance heuristic)
      openSet=[(abs(start[0]-end[0])+abs(start[1]-end[1]),start,start)]
      closedSet={}
      step=0
      while openSet:
         current=openSet.pop(0)
         step+=1
         if current[1]!=start:
            displaySquare([(current[1][0],current[1][1],2)],info,step,1)
         if current[1] not in closedSet:
            if closedSet:
               closedSet[current[1]]=(closedSet[current[2]][0]+1,current[2])
            else:
               closedSet[current[1]]=(0,current[2])
            for neighbor in NEIGHBORS[current[1]]:
               if neighbor not in closedSet:
                  if neighbor==end:
                     path=current[1]
                     while path!=start:
                        time.sleep(.01)
                        displaySquare([(path[0],path[1],4)],info,step,1)
                        path=closedSet[path][1]
                     displaySquare([(path[0],path[1],4)],info,step,1)
                     return
                  if grid[neighbor[0]][neighbor[1]]==0:
                     openSet.append((abs(neighbor[0]-end[0])+abs(neighbor[1]-end[1])+closedSet[current[1]][0]+1,neighbor,current[1]))
         openSet.sort()

def stepLife(grid,lifeType): # Steps the grid and returns changes
   changes=[]
   for col in range(HORIZONTAL//10): # Make sure to find the changes...
      for row in range(VERTICAL//10):
         if not grid[col][row][0] and not LIFELIKE[lifeType][0][grid[col][row][1]]:
            changes.append((col,row,1))
         elif grid[col][row][0] and LIFELIKE[lifeType][1][grid[col][row][1]]:
            changes.append((col,row,0))
   for change in changes: # ...then execute them
      grid[change[0]][change[1]][0]=change[2]
      for neighbor in NEIGHBORS[(change[0],change[1])]:
         if change[2]:
            grid[neighbor[0]][neighbor[1]][1]-=1
         else:
            grid[neighbor[0]][neighbor[1]][1]+=1
   return changes

def generateSeed(lifeType): # Generates an "interesting" grid for cellular automata
   regenerate=True
   while regenerate:
      seed=[]
      seedType=random.randint(0,2) 
      if seedType==0: # Fill the grid with ~half live and ~half dead cells
         for col in range(HORIZONTAL//10):
            for row in range(VERTICAL//10):
               if random.random()<.5:
                  seed.append((col,row))
      elif seedType==1: # Only populates a small box in the center with half live/half dead
         for col in range(HORIZONTAL//10//2-1,HORIZONTAL//10//2+2):
            for row in range(VERTICAL//10//2-1,VERTICAL//10//2+2):
               if random.random()<.5:
                  seed.append((col,row))
      else: # Populates a larger box with half live/half dead
         for col in range(HORIZONTAL//10//2-10,HORIZONTAL//10//2+11):
            for row in range(VERTICAL//10//2-10,VERTICAL//10//2+11):
               if random.random()<.5:
                  seed.append((col,row))
      grid=[[[1,0] for row in range(VERTICAL//10)] for col in range(HORIZONTAL//10)]
      for coords in seed:
         grid[coords[0]][coords[1]][0]=0
         for neighbor in NEIGHBORS[(coords[0],coords[1])]:
            grid[neighbor[0]][neighbor[1]][1]+=1
      testGrid=[[grid[col][row][:] for row in range(VERTICAL//10)] for col in range(HORIZONTAL//10)]
      changeSet=set()
      regenerate=False
      for step in range(250): # Ensures the grid remains "interesting" for at least 250 steps
         changes=stepLife(testGrid,lifeType)
         if tuple(changes) in changeSet:
            regenerate=True
            break
         changeSet.add(tuple(changes))
   return grid

def gravity():
   planets=[]
   totalMass=0
   while totalMass<random.randrange(1000,10000):
      sizeType=random.random()
      if sizeType<.5: # Small
         mass=random.randrange(10,50)
      elif sizeType<.95: # Medium
         mass=random.randrange(50,500)
      else: # Large
         mass=random.randrange(500,2000)
      planets.append([random.randrange(HORIZONTAL),random.randrange(VERTICAL),random.randrange(3)-1,random.randrange(3)-1,mass])
      totalMass+=mass
   prevDraw=[(planet[0],planet[1],(planet[4]/math.pi)**.5,1) for planet in planets]
   step=0
   displayCircle(prevDraw+[(planet[0],planet[1],(planet[4]/math.pi)**.5,0) for planet in planets],'Gravity',0,1)
   while step<2000 and len([planet for planet in planets if planet[0]>0 and planet[0]<HORIZONTAL and planet[1]>0 and planet[1]<VERTICAL])>1:
      time.sleep(.02)
      step+=1
      prevDraw=[(planet[0],planet[1],(planet[4]/math.pi)**.5,1) for planet in planets]
      tempPlanets=[planet[:] for planet in planets]
      for (index,planetA) in enumerate(tempPlanets): # Look for collisions
         for planetB in tempPlanets[index+1:]:
            if ((planetA[0]-planetB[0])**2+(planetA[1]-planetB[1])**2)**.5<(planetA[4]/math.pi)**.5+(planetB[4]/math.pi)**.5:
               if planetA[4]>planetB[4]:
                  x=planetA[0]
                  y=planetA[1]
               elif planetA[4]<planetB[4]:
                  x=planetB[0]
                  y=planetB[1]
               else:
                  x=(planetA[0]+planetB[0])/2
                  y=(planetA[1]+planetB[1])/2
               dx=(planetA[2]*planetA[4]+planetB[2]*planetB[4])/(planetA[4]+planetB[4]) # Inelastic collision
               dy=(planetA[3]*planetA[4]+planetB[3]*planetB[4])/(planetA[4]+planetB[4])
               if planetA in planets and planetB in planets:
                  planets.append([x,y,dx,dy,planetA[4]+planetB[4]])
               if planetA in planets:
                  planets.remove(planetA)
               if planetB in planets:
                  planets.remove(planetB)
      for planetA in planets: # Gravity calculations
         for planetB in planets:
            if planetA!=planetB:
               inverseSquare=1/((planetA[0]-planetB[0])**2+(planetA[1]-planetB[1])**2)
               angle=math.atan((planetA[1]-planetB[1])/(planetA[0]-planetB[0])) if planetA[0]!=planetB[0] else math.pi # Special case for same x
               if planetA[0]>planetB[0]:
                  angle+=math.pi
               planetA[2]+=math.cos(angle)*inverseSquare*planetB[4]*2
               planetA[3]+=math.sin(angle)*inverseSquare*planetB[4]*2
      for planet in planets: # Apply velocity
         planet[0]+=planet[2]
         planet[1]+=planet[3]
      displayCircle(prevDraw+[(planet[0],planet[1],(planet[4]/math.pi)**.5,0) for planet in planets],'Gravity',step,1)
   if step<1800: # A little extra period if the simulation was ended prematurely due to planets on screen
      for extra in range(200):
         time.sleep(.02)
         step+=1
         prevDraw=[(planet[0],planet[1],(planet[4]/math.pi)**.5,1) for planet in planets]
         for planetA in planets:
            if planetA!=planetB:
               inverseSquare=1/((planetA[0]-planetB[0])**2+(planetA[1]-planetB[1])**2)
               angle=math.atan((planetA[1]-planetB[1])/(planetA[0]-planetB[0])) if planetA[0]!=planetB[0] else math.pi # Special case for same x
               if planetA[0]>planetB[0]:
                  angle+=math.pi
               planetA[2]+=math.cos(angle)*inverseSquare*planetB[4]*2
               planetA[3]+=math.sin(angle)*inverseSquare*planetB[4]*2
         for planet in planets:
            planet[0]+=planet[2]
            planet[1]+=planet[3]
         displayCircle(prevDraw+[(planet[0],planet[1],(planet[4]/math.pi)**.5,0) for planet in planets],'Gravity',step,1)
      
def displaySquare(changes,info,step,skip):
   if pygame.QUIT in [event.type for event in pygame.event.get()]:
      sys.exit()
   for (col,row,color) in changes:
      pygame.draw.rect(SCREEN,COLORS[color],(col*10,row*10,10,10))
   infoText=FONT.render(info,True,COLORS[0])
   stepText=FONT.render(str(step),True,COLORS[0])
   infoRect=infoText.get_rect()
   stepRect=stepText.get_rect()
   infoRect.topleft=(0,0)
   stepRect.topleft=(0,18)
   pygame.draw.rect(SCREEN,COLORS[1],infoRect)
   pygame.draw.rect(SCREEN,COLORS[1],stepRect)
   SCREEN.blit(infoText,infoRect)
   SCREEN.blit(stepText,stepRect)
   if step%skip==0: # The fastest "games" can be limited by the speed of flip() and opt to not display every step
      pygame.display.flip() # For some reason, flipping specific parts of the screen for speed doesn't work on my machine

def displayCircle(changes,info,step,skip):
   if pygame.QUIT in [event.type for event in pygame.event.get()]:
      sys.exit()
   for (x,y,radius,color) in changes:
      pygame.draw.circle(SCREEN,COLORS[color],(x,y),radius)
   infoText=FONT.render(info,True,COLORS[0])
   stepText=FONT.render(str(step),True,COLORS[0])
   infoRect=infoText.get_rect()
   stepRect=stepText.get_rect()
   infoRect.topleft=(0,0)
   stepRect.topleft=(0,18)
   pygame.draw.rect(SCREEN,COLORS[1],infoRect)
   pygame.draw.rect(SCREEN,COLORS[1],stepRect)
   SCREEN.blit(infoText,infoRect)
   SCREEN.blit(stepText,stepRect)
   if step%skip==0:
      pygame.display.flip()

while pygame.QUIT not in [event.type for event in pygame.event.get()]:
   pygame.draw.rect(SCREEN,COLORS[1],(0,0,HORIZONTAL,VERTICAL))
   pygame.display.flip()
   game=random.randrange(5)
   if game==0:
      ant()
   elif game==1:
      wolfram()
   elif game==2:
      life()
   elif game==3:
      maze()
   else:
      gravity()
