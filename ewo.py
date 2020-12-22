import matplotlib.pyplot as plt
import numpy as np
from random import uniform, shuffle, sample, randint


def sum(x,a1,k1,p1,a2,k2,p2,a3,k3,p3, c):
    y= a1 * np.sin(k1*x+p1)+ a2*np.sin(k2*x+p2) + a3* np.sin(k3*x+p3)+c
    return y

def primers():
    pr = []
    for i in range (0,200):
        w = []
        for j in range (0,10):
            w.append(uniform(-2.5,2.5))
        pr.append(w)
    return pr


def points():

    x = []
    y = []
    for i in range (0,5):
        x.append(uniform(-4,4))
        y.append(uniform(-2,2))

    return [x,y]

def dostosowanie(men):
    s_av = 0
    for index, i in enumerate(p[0]):
        perf = p[1][index]
        f = sum(i,*men)
        s_av += (perf - f)**2
    av = s_av/len(men)
    return av   
                
def sort_by_dosto(world):

    world.sort(key=dostosowanie)
    return world

def draw(winner=None, sin=True):
    x = np.linspace(-4, 4, 1000)
    if(sin):
        y = sum(x, *(winner)) if sin else 0
        plt.plot(x,y,linewidth=1,)
    plt.scatter(p[0],p[1],s=10)
    plt.figure(num=1,figsize=(5,5))
    plt.show()

def kill(world):
    l = len(world)//2
    world = world[0:l]
    return world

def mutuj(szczur):
    if (randint(1,2) == 1):
        szczur *= 1.30
    elif (randint(1,2) == 1):
        szczur *= 0.7
    if (randint(1,2) == 1):
        szczur *= (-1)
    return szczur



def dzieci(world):
    shuffle(world)

    leng = len(world)
    for i in range (0,leng,2):
        gens = sample([j for j in range (0,10)],5)
        dz1 = world[i][:]
        dz2 = world[i+1][:]


        for g in gens:
            dz2.insert(g,dz1[g])
            dz1.insert(g,dz2[g+1])
            dz2.pop(g+1)
            dz1.pop(g+1)
            
        for i in range (0, len(dz1)):
            if randint(0,100)<20:
                 dz1[i] = mutuj(dz1[i])
            
        for i in range (0, len(dz2)):  
            if randint(0,100)<20:
                dz2[i] = mutuj(dz2[i])
           
        world.append(dz1)
        world.append(dz2)
    return(world)


if __name__ == "__main__": 
    ############
    p  = points()
    #p=[[1.4444,3.33,0.1,-1.97,1.33],[1,3.33,2.132,2,-0.1]]

    ##########3

    draw(sin=False)

    populacja = primers()#[[2, 1, 2, 1, 4, 3, 0, 0, 0, 1], [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]]

    populacja = sort_by_dosto(populacja)

  #  draw(populacja[0])

    licz = 0
    while (dostosowanie(populacja[0])>0.001 and licz <750): #or dostosowanie(populacja[0])>=0.1 :

        
       # print("przed kilkl",populacja,len(populacja))
        populacja = kill(populacja)

        populacja = dzieci(populacja)
        
       # print("...")
        #print(populacja)
        #print("...")
    #draw()
        populacja = sort_by_dosto(populacja)
        
        licz+=1


    draw(populacja[0])
  

