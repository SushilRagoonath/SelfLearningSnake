import pygame as p
from pygame.locals import *
import array as ar
import random as ra
import numpy as np
from genetic import *
Size_x=800
Size_y=800
disp = p.display.set_mode((Size_x,Size_y))
class Snake_piece:
    def __init__(self,color=[255,255,255],size=[Size_x/2,Size_y/2,Size_x/20,Size_y/20],d_snake=4):
        self.n_dir=np.array([1,0,0,0])
        self.size=size
        self.rect = p.rect.Rect(self.size)
        self.color=color
        self.d_snake=d_snake
    def draw(self):
        p.draw.rect(disp, self.color, self.rect)
    def key_d_snake(self):
        # d_snakeections 0=up w ,1=down s ,2=left a,3=right d
        keys=p.key.get_pressed()
        if keys[K_a] and self.d_snake!= 3:
            self.d_snake=0
            self.n_dir=np.array([1,0,0,0])
        elif keys[K_s] and self.d_snake!=2:
            self.d_snake=1
            self.n_dir=np.array([0,1,0,0])
        elif keys[K_d] and self.d_snake!=0:
            self.d_snake=3
            self.n_dir=np.array([0,0,1,0])
        elif keys[K_w] and self.d_snake!=1:
            self.d_snake=2
            self.n_dir=np.array([0,0,0,1])
    def self_key(self,outputs):
        #print(outputs)
        '''
        if outputs[0]==np.max(outputs) and self.d_snake!= 3:
            self.d_snake=0
        elif outputs[1]==np.max(outputs) and self.d_snake!=2:
            self.d_snake=1
        elif outputs[2]==np.max(outputs) and self.d_snake!=0:
            self.d_snake=3
        elif outputs[3]==np.max(outputs) and self.d_snake!=1:
            self.d_snake=2
        '''
        if outputs[0]>0.5 and self.d_snake!= 3:
            self.d_snake=0
        elif outputs[0]>0 and self.d_snake!=2:
            self.d_snake=1
        elif outputs[0]>-0.5 and self.d_snake!=0:
            self.d_snake=3
        else :
            self.d_snake=2
         
    def movement(self,direction):
        # d_snakeections 0=up w ,1=down s ,2=left a,3=right d
        if self.d_snake==0:
            self.rect.x-=50
        elif self.d_snake==1:
            self.rect.y+=50
        elif self.d_snake==2:
            self.rect.y-=50
        elif self.d_snake==3:
            self.rect.x+=50
    def reset(self):
        if(  self.rect.x >Size_x or self.rect.x < 0 or self.rect.y > Size_y or self.rect.y < 0 ):
            print("reset")
            self.d_snake=4
            self.rect = p.rect.Rect(self.size)


class Snake:
    def __init__(self,colour=[ra.randint(0,255),ra.randint(0,255),ra.randint(0,255)],direction=np.array([1,0,0,0]),head=Snake_piece()):
        self.head= head
        self.colour=colour
        self.h_dir=direction
        self.size=[Size_x,Size_y,Size_x/20,Size_y/20]
        self.f_size=[ra.randint(0,Size_x),ra.randint(0,Size_y),Size_x/20,Size_y/20]
        self.snake_piece= [[Size_x,Size_y]]  # just an array of x and y values  x= [0] y=[1] e.g head = x is [0][0] y is [0][1]
        self.f_rect=p.rect.Rect(self.f_size)
        self.score=1 # needs to be one or else movement function needs to change
        self.best_score=1
        self.previous_head=[[Size_x,Size_y]] # not being used
        self.loops_last_eaten=0
        self.network=NeuralNetwork(np.array([1,1,1,1]),np.array([1]) )
        self.reset_times=0
        self.f_colour=[ra.randint(0,255), ra.randint(0,255),ra.randint(0,255)]
        self.previous_moves=[4,4,4,4]
    def movement(self):
        self.loops_last_eaten+=1
        self.previous_moves.append(self.head.d_snake)
        if(self.head.rect.colliderect(self.f_rect)):
            self.food([ra.randint(0,255), ra.randint(0,255),ra.randint(0,255)])
            self.loops_last_eaten=0
            #print("eaten")
            self.score=self.score+1
            self.snake_piece.append([Size_x,Size_y] )
        if len(self.snake_piece) ==1:
            self.head.movement(4)
        else :
            self.head.movement(4)
            self.snake_piece.insert(0,[self.head.rect.x,self.head.rect.y])
            self.snake_piece.pop(self.score-1)  # dependant on score

        if self.score >self.best_score:
            self.best_score=self.score


    def food(self,f_colour=[ra.randint(0,255), ra.randint(0,255),ra.randint(0,255)] ):
        self.f_colour=f_colour
        self.f_size=[ra.randint(0,Size_x-50),ra.randint(0,Size_y-50),Size_x/20,Size_y/20]
        self.f_rect=p.rect.Rect(self.f_size)
        p.draw.rect(disp, f_colour, self.f_size)
        #print("food")
    def draw(self):
        for i in range(1,len(self.snake_piece)):
            p.draw.rect(disp, [255,255,255], p.rect.Rect([self.snake_piece[i][0],self.snake_piece[i][1],Size_x/20,Size_y/20]))
        p.draw.rect(disp,self.f_colour,self.f_rect)
        self.head.draw()

    def reset(self):
        if(  self.head.rect.x >Size_x or self.head.rect.x < 0 or self.head.rect.y > Size_y or self.head.rect.y < 0 or [self.head.rect.x,self.head.rect.y] in self.snake_piece[1:]):
            #print("reset")
            self.d_snake=4
            #self.snake_piece.clear()
            self.snake_piece= [[Size_x,Size_y]]
            self.head=Snake_piece()
            #self.loops_last_eaten=0
            self.score=2
            self.reset_times+=1
            #print(self.reset_times)
            self.previous_moves=[4,4,4,4]
    def kill(self):
        if(  self.loops_last_eaten>150):
            #print("reset")
            self.d_snake=4
            #self.snake_piece.clear()
            self.snake_piece= [[Size_x,Size_y]]
            self.head=Snake_piece()
            #self.loops_last_eaten=0
            self.score=2
            self.reset_times+=1
            #print(self.reset_times
            self.previous_moves=[4,4,4,4]
    def score_print(self):
        font=p.font.Font(None,50)
        text =font.render(str(self.score-1),True,self.f_colour)
        disp.blit(text,[self.head.rect.x,self.head.rect.y])
