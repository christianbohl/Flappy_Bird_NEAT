#!/usr/bin/env python
# coding: utf-8

# In[1]:


from random import randint
from random import randrange
import random
import math
import pygame, sys
import numpy as np
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox
import time
from PIL import ImageOps,Image
import math
import datetime
import time

import neat


# # Imagenes

# In[2]:


bird=Image.open('/Users/christianbohl/Documents/Vida_Profesional/AI/Flappy Bird/pajaro.png')
bg=Image.open('/Users/christianbohl/Documents/Vida_Profesional/AI/Flappy Bird/bg_bird.png')
pipe=Image.open('/Users/christianbohl/Documents/Vida_Profesional/AI/Flappy Bird/pipe.png')


# In[3]:


print("bird:",bird.size,"background:",bg.size,"pipe:",pipe.size)


# In[4]:


bird=bird.crop([550,200,1150,550])
bg=bg.crop([95,64,975,864])
bird=bird.resize((70,40),Image.ANTIALIAS)
pipe=pipe.resize((170,580),Image.ANTIALIAS)
pipe_upper=ImageOps.flip(pipe)


# In[5]:


#bg.save("bg_resize.png")
#bird.save("bird_resize.png")
#pipe.save("pipe_lower.png")
#pipe_upper.save("pipe_upper.png")


# In[6]:


black = (0,0,0)
darkgrey=(82,82,82)
lightgrey=(175,175,175)
white = (255,255,255)
grey = (128,128,128)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkred=(139,0,0)
rojo_level=(102,0,0)
darkblue=(0,0,63)


# # Classes

# In[7]:


class Bird():
    def __init__(self):
        self.x=100
        self.y=400
        self.w=46
        self.h=34
        self.angle=0
        self.acel=2
        self.vel=0
        self.time_ini=0
        self.time_trans=0
        
        
    def tiempo_ini(self):
        self.time_ini=time.time()
        
    def tiempo_dif(self):
        self.time_trans= (time.time()-self.time_ini)
    
    def gravedad(self):
        self.vel=self.vel-(self.acel*self.time_trans)
        self.y=self.y-self.vel
        
    def jump(self):
        self.tiempo_ini()
        self.vel=8
    
    def drawBird(self,im):
#        pygame.draw.rect(displaySurface,red,(self.x,self.y,self.w,self.h))
        displaySurface.blit(im, [self.x-10,self.y-3])
    
    
## x=610
class Pipe():
    def __init__(self,x):
        self.x=x
        self.y=0
        self.w=150
        self.h=random.randint(100,550)
        self.gap=175
    
    def moverse(self):
        self.x-=5
    
    def drawPipeUpper(self,im):
#        pygame.draw.rect(displaySurface,red,(self.x,self.h-550,self.w,550))
        displaySurface.blit(im, [self.x-8,self.h-552])
    
    def drawPipeLower(self,im):
#        pygame.draw.rect(displaySurface,red,(self.x,self.h+self.gap,self.w,550))
        displaySurface.blit(im, [self.x-8,self.h+self.gap-28])
      
    
class Fondo():
    def __init__(self):
        self.x=0
        self.y=0
        self.w=880
    
    def moverse(self):
        self.x-=3
    
    def drawBG(self,im,x,y):
        displaySurface.blit(im, [x,y])


# # Game

# In[8]:


def drawTime(time_pas):
    timeSurf=font.render("TIME: %s" %(time_pas),True,white)
    timeWrite=timeSurf.get_rect()
    timeWrite.center=(300,15)
    displaySurface.blit(timeSurf,timeWrite)
    
def drawText(string,size,location,color):
    font_var = pygame.font.Font('freesansbold.ttf', size) 
    textSurf=font_var.render(string,True,color)
    textWrite=textSurf.get_rect()
    textWrite.center=location
    displaySurface.blit(textSurf,textWrite)
    
def drawLine(color,start,end,w):
    pygame.draw.line(displaySurface,color,start,end,w)


# In[9]:


fps=30

create_pipe = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe, 2350)

def main(genomes, config):
    global displaySurface, clock, font, start_time
    
    nets=[]
    ge=[]
    players=[]
    pipes=[]
    
    for _, g in genomes:
        net= neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Bird())
        g.fitness=0
        ge.append(g)
    
    pygame.init()
    displaySurface=pygame.display.set_mode((600, 800))
    
    pygame.display.set_caption('FLAPPY BIRD')
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 18)
    
    bg_image = pygame.image.load("bg_resize.png").convert()
    bird_image = pygame.image.load("bird_resize.png").convert_alpha()
    pipe_lower = pygame.image.load("pipe_lower.png").convert_alpha()
    pipe_upper = pygame.image.load("pipe_upper.png").convert_alpha()
    fondo=Fondo()
    
    score_play=0
    
    run=True
    empezar=False
    
    while run:
        if empezar==False:
        
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    empezar=True
                    pipes.append(Pipe(610))
                    for p in players:
                        p.tiempo_ini()
                
                else:
                    pass
    
        else:
            
            for event in pygame.event.get():
                if event.type==QUIT:
                    run=False
                    
                elif (event.type==KEYDOWN):
                    keys = pygame.key.get_pressed()
                    
                    if keys[pygame.K_SPACE]:
                        for x in players:
                            x.jump()
            
            
            if pipes[-1].x<=250:
                pipes.append(Pipe(610))
                
            
            if (fondo.x<=-880):
                fondo.x=0
            
            fondo.drawBG(bg_image,fondo.x,fondo.y)
            fondo.drawBG(bg_image,fondo.x+880,fondo.y)
            fondo.moverse()
                
        
            result=[]
            for i in pipes:
                distx=(i.x+i.w)-players[0].x
                    
                result.append(distx)
                    
                
            dist_sigx=min([e for e in result if e>0])
            
            arr_sig=pipes[result.index(min([e for e in result if e>0]))].h
            baj_sig=pipes[result.index(min([e for e in result if e>0]))].h+pipes[result.index(min([e for e in result if e>0]))].gap
                    
                    
            
            
            for c,i in enumerate(players):
                if i.y>=800 or i.y+i.h<=0:
                    ge[c].fitness-=10
                    players.pop(c)
                    nets.pop(c)
                    ge.pop(c)
                    
                    
            
            for i in pipes:
                i.moverse()
                i.drawPipeUpper(pipe_upper)
                i.drawPipeLower(pipe_lower)
                
                
                for pos,j in enumerate(players):
                    if ((j.x >= i.x and j.x <= (i.x+i.w) and j.y <= (i.y+i.h)) or
                    (j.x >= i.x and j.x <= (i.x+i.w) and (j.y+j.h) >= (i.y+i.h+i.gap)) or
                    ((j.x+j.w) >= i.x and (j.x+j.w) <= (i.x+i.w) and (j.y+j.h) >= (i.y+i.h+i.gap)) or
                    ((j.x+j.w) >= i.x and (j.x+j.w) <= (i.x+i.w) and (j.y) <= (i.y+i.h))):
                        
                        
                        ge[pos].fitness-=10
                        
                        players.pop(pos)
                        nets.pop(pos)
                        ge.pop(pos)
                        
            
            for i in pipes:
                for pos, j in enumerate(players):
                    if j.x>=(i.x+i.w):
                        ge[pos].fitness+=20
                        
            
            
            for x,i in enumerate(players):
                i.tiempo_dif()
                i.gravedad()
                i.drawBird(bird_image)
                ge[x].fitness+=0.1
                
                output= nets[x].activate((i.y , dist_sigx,arr_sig,baj_sig))
                
                if output[0]>0.5:
                    i.jump()
            
            if len(players)==0:
                run=False
            
            if len(ge)>=1:
                max_fit=[]
                for g in ge:
                    max_fit.append(round(g.fitness,1))
                
                
            drawText("Max Fitness: %s" %(max(max_fit)), 20,(120,30),white)
            
            
            if len(pipes)>=1 and len(players)>=1 and (players[0].x+players[0].w<=pipes[result.index(min([e for e in result if e>0]))].x ) and len(players)<=3:
                
                drawLine(darkblue,
                         (players[0].x+players[0].w, players[0].y+(players[0].h/2)),
                         (pipes[result.index(min([e for e in result if e>0]))].x , players[0].y+(players[0].h/2)),
                         5
                        )
                
            if len(players)>=1 and len(players)<=3:
                
                drawLine(darkblue,
                         (players[0].x+(players[0].w/2),players[0].y+players[0].h),
                         (players[0].x+(players[0].w/2),800),
                         5
                        )
                
            if len(pipes)>=1 and len(players)<=3:
                
                pipe_imp=pipes[result.index(min([e for e in result if e>0]))]
                
                drawLine(darkblue,
                        (pipe_imp.x+(pipe_imp.w/2),pipe_imp.h),
                        (pipe_imp.x+(pipe_imp.w/2),pipe_imp.h+pipe_imp.gap),
                         5
                        )
            
            pygame.display.update()
            clock.tick(fps)


# In[ ]:


path_file='/Users/christianbohl/Documents/Vida_Profesional/AI/Flappy Bird'+'/config-feedforward.txt'

def run(file_path):
    config=neat.config.Config(neat.DefaultGenome, 
                              neat.DefaultReproduction,
                              neat.DefaultSpeciesSet,
                              neat.DefaultStagnation,
                              file_path)
    
    population=neat.Population(config)
    
    population.add_reporter(neat.StdOutReporter(True))
    
    stats=neat.StatisticsReporter()
    
    population.add_reporter(stats)
    
    winner = population.run(main,50)

if __name__=="__main__":
        run(path_file)


# # Juego sin AI

# In[9]:


fps=30

def juego():
    global displaySurface, clock, font, start_time
    
    players=[]
    pipes=[]
    
    
    pygame.init()
    displaySurface=pygame.display.set_mode((600, 800))
    
    pygame.display.set_caption('FLAPPY BIRD')
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 18)
    
    bg_image = pygame.image.load("bg_resize.png").convert()
    bird_image = pygame.image.load("bird_resize.png").convert_alpha()
    pipe_lower = pygame.image.load("pipe_lower.png").convert_alpha()
    pipe_upper = pygame.image.load("pipe_upper.png").convert_alpha()
    fondo=Fondo()
    
    score_play=0
    
    run=True
    empezar=False
    
    while run:
        if empezar==False:
        
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    empezar=True
                    players.append(Bird())
                    pipes.append(Pipe(610))
                    for p in players:
                        p.tiempo_ini()
                
                else:
                    pass
    
        else:
            
            for event in pygame.event.get():
                if event.type==QUIT:
                    run=False
                    
                elif (event.type==KEYDOWN):
                    keys = pygame.key.get_pressed()
                    
                    if keys[pygame.K_SPACE]:
                        for x in players:
                            x.jump()
                        
            
            
            if pipes[-1].x<=250:
                pipes.append(Pipe(610))
                
            
            if (fondo.x<=-880):
                fondo.x=0
            
            fondo.drawBG(bg_image,fondo.x,fondo.y)
            fondo.drawBG(bg_image,fondo.x+880,fondo.y)
            fondo.moverse() 
            
            
            for c,i in enumerate(players):
                if i.y>=800 or i.y+i.h<=0:
                    run=False
                    
                    
            
            for i in pipes:
                i.moverse()
                i.drawPipeUpper(pipe_upper)
                i.drawPipeLower(pipe_lower)
                
                
                for pos,j in enumerate(players):
                    if ((j.x >= i.x and j.x <= (i.x+i.w) and j.y <= (i.y+i.h)) or
                    (j.x >= i.x and j.x <= (i.x+i.w) and (j.y+j.h) >= (i.y+i.h+i.gap)) or
                    ((j.x+j.w) >= i.x and (j.x+j.w) <= (i.x+i.w) and (j.y+j.h) >= (i.y+i.h+i.gap)) or
                    ((j.x+j.w) >= i.x and (j.x+j.w) <= (i.x+i.w) and (j.y) <= (i.y+i.h))):
                        
                        
                        run=False
                        
            
            
            for x,i in enumerate(players):
                i.tiempo_dif()
                i.gravedad()
                i.drawBird(bird_image)
                    
            
            pygame.display.update()
            clock.tick(fps)


# In[10]:


juego()


# In[ ]:




