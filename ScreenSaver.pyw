import pygame
import random
import time

HORIZONTAL=1920
VERTICAL=1080
WIDTH=10
HEIGHT=10
COLS=HORIZONTAL//HEIGHT
ROWS=VERTICAL//WIDTH
QUIT=False
ANT_STEPS=100000
LIFE_STEPS=2000

def ant(screen,font):
   rule=[]
   for i in range(random.randint(1,19)):
      type=random.random()
      if type<.5:
         rule.append(random.randint(0,1))
      elif .5<=type<.7:
         rule.append(random.randint(2,3))
      else:
         rule.append(random.randint(4,7))
   info=''.join([str(i) for i in rule]).replace('0','L').replace('1','R').replace('2','F').replace('3','B').replace('4','N').replace('5','E').replace('6','S').replace('7','W')
   grid=[[1 for i in range(ROWS)] for e in range(COLS)]
   antCol=COLS//2
   antRow=ROWS//2
   antDir=0
   step=0
   if not display([(antCol,antRow,getColor(0))],screen,font,info,step,5):
      return
   while step<ANT_STEPS:
      step+=1
      antDir=antDirection(antCol,antRow,antDir,grid,rule)
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
         antCol=COLS-1
      elif antCol==COLS:
         antCol=0
      if antRow==-1:
         antRow=ROWS-1
      elif antRow==ROWS:
         antRow=0
      if not display([(antCol,antRow,getColor(0)),(oldCol,oldRow,getColor(grid[oldCol][oldRow]))],screen,font,info,step,5):
         return
 
def antDirection(antCol,antRow,antDir,grid,rule):
   if rule[grid[antCol][antRow]-1]==0:
      return (antDir-1)%4
   elif rule[grid[antCol][antRow]-1]==1:
      return (antDir+1)%4
   elif rule[grid[antCol][antRow]-1]==2:
      return antDir
   elif rule[grid[antCol][antRow]-1]==3:
      return (antDir+2)%4
   elif rule[grid[antCol][antRow]-1]==4:
      return 1
   elif rule[grid[antCol][antRow]-1]==5:
      return 2
   elif rule[grid[antCol][antRow]-1]==6:
      return 3
   else:
      return 0
 
def wolfram(screen,font):
   info=random.randint(0,255)
   rule=[int(i) for i in bin(info)[2:].zfill(8)]
   grid=[[0 for i in range(ROWS)] for e in range(COLS)]
   step=0
   type=random.randint(0,2)
   if type==0:
      grid[COLS//2][step]=1
   elif type==1:
      for col in range(random.randint(2,5)):
         grid[random.randint(0,COLS)][step]=1
   else:
      for col in range(COLS):
         grid[col][step]=random.randint(0,1)
   if not display([(col,step,getColor(0)) for col in range(COLS) if grid[col][step]==1],screen,font,'Rule '+str(info),step,1):
      return
   while step<ROWS-1:
      time.sleep(.1)
      step+=1
      changes=[]
      for col in range(COLS):
         pattern=''
         if col==0:
            pattern+=str(grid[COLS-1][step-1])
         else:
            pattern+=str(grid[col-1][step-1])
         pattern+=str(grid[col][step-1])
         if col==COLS-1:
            pattern+=str(grid[0][step-1])
         else:
            pattern+=str(grid[col+1][step-1])
         if pattern=='111':
            grid[col][step]=rule[0]
         elif pattern=='110':
            grid[col][step]=rule[1]
         elif pattern=='101':
            grid[col][step]=rule[2]
         elif pattern=='100':
            grid[col][step]=rule[3]
         elif pattern=='011':
            grid[col][step]=rule[4]
         elif pattern=='010':
            grid[col][step]=rule[5]
         elif pattern=='001':
            grid[col][step]=rule[6]
         else:
            grid[col][step]=rule[7]
         if grid[col][step]==1:
            changes.append((col,step,getColor(0)))
      if not display(changes,screen,font,'Rule '+str(info),step,1):
         return

def life(screen,font):
   generateLife(screen,font,random.randint(0,6),None)
  
def maze(screen,font):
   type=random.randint(0,2)
   if type==0:
      info='Breadth-First Search'
   elif type==1:
      info='Bidirectional Breadth-First Search'
   else:
      info='A*'
   grid=generateLife(screen,font,random.randint(7,10),info)
   if grid==True:
      return
   surround=[]
   for col in range(COLS):
      for row in range(ROWS):
         if col!=0 and row!=0 and col!=COLS-1 and row!=ROWS-1:
            grid[col][row]=grid[col][row][0]
         else:
            grid[col][row]=1
            surround.append((col,row))
   found=False
   attempts=0
   while not found:
      attempts+=1
      start=(random.randint(1,10),random.randint(10,ROWS-10))
      if grid[start[0]][start[1]]==0:
         found=True
      if attempts>100:
         return
   found=False
   attempts=0
   while not found:
      attempts+=1
      end=(COLS-1-random.randint(1,10),random.randint(10,ROWS-10))
      if grid[end[0]][end[1]]==0:
         found=True
      if attempts>100:
         return
   for col,row in surround:
      if not display([(col,row,getColor(grid[col][row]))],screen,font,info,0,1):
         return
   if not display([(start[0],start[1],getColor(3)),(end[0],end[1],getColor(2))],screen,font,info,0,1):
      return
   if type==0:
      bfs(grid,start,end)
   elif type==1:
      bbfs(grid,start,end)
   else:
      astar(grid,start,end)
      
def bfs(grid,start,end):
   neighborLookup=buildNeighborLookup()
   queue=[start]
   visited={start:start}
   step=0
   while queue:
      parent=queue.pop(0)
      step+=1
      if parent!=start:
         if not display([(parent[0],parent[1],getColor(2))],screen,font,'Breadth-First Search',step,1):
            return
      for neighbor in neighborLookup[parent]:
         if neighbor not in visited:
            visited[neighbor]=parent
            if neighbor==end:
               path=visited[end]
               while path!=start:
                  time.sleep(.01)
                  if not display([(path[0],path[1],getColor(4))],screen,font,'Breadth-First Search',step,1):
                     return
                  path=visited[path]
               return
            if grid[neighbor[0]][neighbor[1]]==0:
               queue.append(neighbor)
                 
def bbfs(grid,start,end):
   neighborLookup=buildNeighborLookup()
   startQueue=[start]
   endQueue=[end]
   startVisited={start:start}
   endVisited={end:end}
   step=0
   while startQueue and endQueue:
      startParent=startQueue.pop(0)
      step+=1
      if startParent!=start:
         if not display([(startParent[0],startParent[1],getColor(2))],screen,font,'Bidirectional Breadth-First Search',step,1):
            return
      for neighbor in neighborLookup[startParent]:
         if neighbor not in startVisited:
            startVisited[neighbor]=startParent
            if neighbor in endVisited:
               if not display([(neighbor[0],neighbor[1],getColor(4))],screen,font,'Bidirectional Breadth-First Search',step,1):
                  return
               startPath=startVisited[neighbor]
               endPath=endVisited[neighbor]
               while startPath!=start or endPath!=end:
                  time.sleep(.01)
                  if not display([(startPath[0],startPath[1],getColor(4)),(endPath[0],endPath[1],getColor(4))],screen,font,'Bidirectional Breadth-First Search',step,1):
                     return
                  startPath=startVisited[startPath]
                  endPath=endVisited[endPath]
               return
            if grid[neighbor[0]][neighbor[1]]==0:
               startQueue.append(neighbor)
      endParent=endQueue.pop(0)
      step+=1
      if endParent!=end:
         if not display([(endParent[0],endParent[1],getColor(3))],screen,font,'Bidirectional Breadth-First Search',step,1):
            return
      for neighbor in neighborLookup[endParent]:
         if neighbor not in endVisited:
            endVisited[neighbor]=endParent
            if neighbor in startVisited:
               if not display([(neighbor[0],neighbor[1],getColor(4))],screen,font,'Bidirectional Breadth-First Search',step,1):
                  return
               startPath=startVisited[neighbor]
               endPath=endVisited[neighbor]
               while startPath!=start or endPath!=end:
                  time.sleep(.01)
                  if not display([(startPath[0],startPath[1],getColor(4)),(endPath[0],endPath[1],getColor(4))],screen,font,'Bidirectional Breadth-First Search',step,1):
                     return
                  startPath=startVisited[startPath]
                  endPath=endVisited[endPath]
               return
            if grid[neighbor[0]][neighbor[1]]==0:
               endQueue.append(neighbor)

def astar(grid,start,end):
   neighborLookup=buildNeighborLookup()
   openSet=[(getManhattan(start,end),start,start)]
   closedSet={}
   step=0
   while openSet:
      current=openSet.pop(0)
      step+=1
      if current[1]!=start:
         if not display([(current[1][0],current[1][1],getColor(2))],screen,font,'A*',step,1):
            return
      if current[1] not in closedSet:
         if closedSet:
            closedSet[current[1]]=(closedSet[current[2]][0]+1,current[2])
         else:
            closedSet[current[1]]=(0,current[2])
         for neighbor in neighborLookup[current[1]]:
            if neighbor not in closedSet:
               if neighbor==end:
                  path=current[1]
                  while path!=start:
                     time.sleep(.01)
                     if not display([(path[0],path[1],getColor(4))],screen,font,'A*',step,1):
                        return
                     path=closedSet[path][1]
                  if not display([(path[0],path[1],getColor(4))],screen,font,'A*',step,1):
                     return
                  return
               if grid[neighbor[0]][neighbor[1]]==0:
                  openSet.append((getManhattan(neighbor,end)+closedSet[current[1]][0]+1,neighbor,current[1]))
      openSet.sort()
                  
def getManhattan(a,b):
   return abs(a[0]-b[0])+abs(a[1]-b[1])

def generateLife(screen,font,lifeLike,forceInfo):
   info=getLifeLike(lifeLike)
   neighborLookup=buildNeighborLookup()
   liveRule=[0,0,0,0,0,0,0,0,0]
   deadRule=[0,0,0,0,0,0,0,0,0]
   for index in range(1,info.index('/')):
      deadRule[int(info[index])]=1
   for index in range(info.index('S')+1,len(info)):
      liveRule[int(info[index])]=1
   if forceInfo:
      info=forceInfo
   run=False
   while not run:
      seed=[]
      seedType=random.randint(0,2)
      if seedType==0:
         for col in range(COLS):
            for row in range(ROWS):
               if random.random()<.5:
                  seed.append((col,row))
      elif seedType==1:
         for col in range(COLS//2-1,COLS//2+2):
            for row in range(ROWS//2-1,ROWS//2+2):
               if random.random()<.5:
                  seed.append((col,row))
      else:
         for col in range(COLS//2-10,COLS//2+11):
            for row in range(ROWS//2-10,ROWS//2+11):
               if random.random()<.5:
                  seed.append((col,row))
      grid=[[[1,0] for i in range(ROWS)] for e in range(COLS)]
      for coords in seed:
         grid[coords[0]][coords[1]][0]=0
         for neighbor in neighborLookup[(coords[0],coords[1])]:
            grid[neighbor[0]][neighbor[1]][1]+=1
      testGrid=[[grid[col][row][:] for row in range(ROWS)] for col in range(COLS)]
      changeSet=set()
      changes=[]
      for step in range(100):
         changes=processStep(testGrid,liveRule,deadRule)
         if tuple(changes) in changeSet:
            changes=[]
            break
         changeSet.add(tuple(changes))
         for change in changes:
            testGrid[change[0]][change[1]][0]=change[2]
            for neighbor in neighborLookup[(change[0],change[1])]:
               if change[2]:
                  testGrid[neighbor[0]][neighbor[1]][1]-=1
               else:
                  testGrid[neighbor[0]][neighbor[1]][1]+=1
      if changes:
         run=True
   changeSet=set()
   step=0
   if not display([(coords[0],coords[1],getColor(0)) for coords in seed],screen,font,info,step,1):
      return True
   while step<LIFE_STEPS:
      time.sleep(.01)
      if not forceInfo:
         step+=1
      changes=processStep(grid,liveRule,deadRule)
      if tuple(changes) in changeSet:
         return grid
      changeSet.add(tuple(changes))
      if not changes:
         return grid
      for change in changes:
         grid[change[0]][change[1]][0]=change[2]
         for neighbor in neighborLookup[(change[0],change[1])]:
               if change[2]:
                  grid[neighbor[0]][neighbor[1]][1]-=1
               else:
                  grid[neighbor[0]][neighbor[1]][1]+=1
      if not display([(change[0],change[1],getColor(change[2])) for change in changes],screen,font,info,step,1):
         return True

def processStep(grid,liveRule,deadRule):
   changes=[]
   for col in range(COLS):
      for row in range(ROWS):
         if not grid[col][row][0] and not liveRule[grid[col][row][1]]:
            changes.append((col,row,1))
         elif grid[col][row][0] and deadRule[grid[col][row][1]]:
            changes.append((col,row,0))
   return changes
   
def buildNeighborLookup():
   neighborLookup={}
   for col in range(COLS):
      for row in range(ROWS):
         left=col-1
         if left<0:
            left=COLS-1
         right=col+1
         if right>=COLS:
            right=0
         top=row-1
         if top<0:
            top=ROWS-1
         bottom=row+1
         if bottom>=ROWS:
            bottom=0
         neighborLookup[(col,row)]=((left,top),(left,row),(left,bottom),(col,top),(col,bottom),(right,top),(right,row),(right,bottom))
   return neighborLookup

def getLifeLike(type):
   if type==0:
      return 'B3/S012345678'
   elif type==1:
      return 'B3/S23'
   elif type==2:
      return 'B36/S125'
   elif type==3:
      return 'B36/S23'
   elif type==4:
      return 'B4678/S35678'
   elif type==5:
      return 'B357/S238'
   elif type==6:
      return 'B5678/S34568'
   elif type==7:
      return 'B3/S345'
   elif type==8:
      return 'B35/S234578'
   elif type==9:
      return 'B3/S1234'
   else:
      return 'B3/S12345'

def display(changes,screen,font,info,step,skip):
   for event in pygame.event.get():
      if event.type==pygame.QUIT:
         global QUIT
         QUIT=True
         return False
   for (col,row,color) in changes:
      pygame.draw.rect(screen,color,(col*WIDTH,row*HEIGHT,WIDTH,HEIGHT))
   infoText=font.render(info,True,getColor(0))
   infoRect=infoText.get_rect()
   infoRect.topleft=(0,0)
   stepText=font.render(str(step),True,getColor(0))
   stepRect=stepText.get_rect()
   stepRect.topleft=(0,18)
   pygame.draw.rect(screen,getColor(1),infoRect)
   pygame.draw.rect(screen,getColor(1),stepRect)
   screen.blit(infoText,infoRect)
   screen.blit(stepText,stepRect)
   if step%skip==0:
      pygame.display.flip()
   return True

def getColor(n):
   if n==0:
      return (255,255,255)
   if n==1:
      return (0,0,0)
   if n==2:
      return (255,0,0)
   if n==3:
      return (0,255,0)
   if n==4:
      return (0,0,255)
   if n==5:
      return (255,255,0)
   if n==6:
      return (0,255,255)
   if n==7:
      return (255,0,255)
   if n==8:
      return (127,0,0)
   if n==9:
      return (0,127,0)
   if n==10:
      return (0,0,127)
   if n==11:
      return (127,127,0)
   if n==12:
      return (0,127,127)
   if n==13:
      return (127,0,127)
   if n==14:
      return (255,127,0)
   if n==15:
      return (0,255,127)
   if n==16:
      return (127,0,255)
   if n==17:
      return (127,255,0)
   if n==18:
      return (0,127,255)
   if n==19:
      return (255,0,127)
      
pygame.init()
pygame.display.set_caption("ScreenSaverThingy")
pygame.mouse.set_visible(False)
screen=pygame.display.set_mode([HORIZONTAL,VERTICAL],pygame.FULLSCREEN)
font=pygame.font.SysFont("hack",15)
while not QUIT:
   pygame.draw.rect(screen,getColor(1),(0,0,HORIZONTAL,VERTICAL))
   pygame.display.flip()
   game=random.randint(0,3)
   if game==0:
      ant(screen,font)
   elif game==1:
      wolfram(screen,font)
   elif game==2:
      life(screen,font)
   else:
      maze(screen,font)
