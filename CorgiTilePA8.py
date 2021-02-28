#Импорт
import pygame
from pygame import mixer
from tkinter import *
import tkinter as tk
import random
from PIL import ImageTk,Image
import os
import keyboard
import time
from tkinter import messagebox as mb
import itertools
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from time import gmtime, strftime
import yaml
root = Tk()
mixer.init()
#Есои системный месяц декабрь или январь - включаем новогодний режим
if int(strftime("%m", gmtime())) == 12 or int(strftime("%m", gmtime())) == 1:
    isNewYear = True
else:
    isNewYear = False
#создаем полноэкранное окно
try:
    root.attributes('-fullscreen', True)
except:
    try:
        root.attributes('-zoomed', True)
    except:
        print("Fatal: CreateWindow.")
        input("OK [Enter]")
        exit()
#списки
spr = {}
particles = {}
#версия. Если будете форкаться - прошу добавить название своего проекта сюда
version = "PA8"

water = []
root.iconbitmap('data/icon.ico')
#Называем наше окно. В соответствии с новогодним режимом
if isNewYear == False:
    root.title("CorgiTile "+version)
else:
    root.title("CorgiTile "+version+": Happy New Year!")
#Загружаем продвинутые настройки из файла
with open("data/settings.yml", 'r') as stream:
    try:
        settyaml = yaml.safe_load(stream)
        paramount = int(settyaml["particles-amount"])
    except:
        mb.showerror("Ошибка","Ошибка загрузки settings.yml")
        
#Включаем музычку в фоне
if settyaml["ambient-music"] == True:
    if isNewYear == False:
        pygame.mixer.music.load('data/sound/ambient/ambientmusic.mp3')
    else:
        pygame.mixer.music.load('data/sound/ambient/ambientmusicnewyear.mp3')
    pygame.mixer.music.play(-1)
#Настраиваем и создаем переменные, списки, словари
bu = ""
CHUNK = 1024
fanim = True
prodsm = False
collision=True
gm = []
dogs = []
dogbuf = []
DAI=True
startsm = False
qwerty=False
wwd = settyaml["width-view-distanse"]
hwd = settyaml["hight-view-distanse"]
dogrot = []
fire = []
firebu=[]
gui = {}
sound = {}
nolo = False
plrot = 1
nextseason = True
line = 0

rezervedspr = ["P","B","G"," ","S","H","M","Q","E","#","I","S","N", "V", "!", "X", "C","$",";","@","Z","F","W","*"]
invedger = [0,18,36,54,72,90,108,126,144,162,180]
invedgel = [1,19,37,55,73,91,109,127,145,163]
idtospr = {1:"H",2:"@1",3:" ",4:"E",5:"G",6:"F1",7:"S",8:"W1",9:"Z1",10:"B",11:"M",12:"D1", 13:"X"}
hotbar = [0,1,2,3,4,5,6,7,8,9,10,11,12]
floor = ["P","B","G"," ","#","F","N", "V", "I"]
stdspr = ["P"," ","S","H","M","Q","E","#","I","S","!","X","C","$",";"]
stdload = ["P","B","G"," ","S","H","M","#","!","N","I","V"]
sprpath = ["pepel","sand","grass","floor","woodwall","brickwall","rock","Animated/water/water4","Animated/water/water5","snow","ice","snowysand"]
invspr = [["H","@1", " ","E","G","F1","S","W1","Z1","B", "M","D1","X"],[],[],[],[],[],[],[],[]]
stdplace = ["B","G"," ","S","H","M","S","D","N"]
fireable = ["S","G","Q","E"]
transparent = ["P","B","G"," ","#","F","N", "V", "I","*","@","Z","W", "F"]
natural = ["G","M","B","I","W","#","F", "*"]
#Загружаем моды. 
with open("custom/yamls/tiles.yml", 'r') as stream:
    #try:
    tilesyaml = yaml.safe_load(stream)
    #except:
    #    mb.showerror("Ошибка", "Ошибка пользовательского YAML!")

if tilesyaml["enabled"] == True:
    invlineload = 0
    itr = 13
    register = tilesyaml["register"]
    for i in range(len(register)):
        if register[i] not in rezervedspr:
            itr += 1
            idtospr[len(idtospr)+1] = register[i]
            stdspr.append(register[i])
            stdload.append(register[i])
            sprpath.append(tilesyaml["sprites"][register[i]]["sprite"])
            invspr[invlineload].append(register[i])
            stdplace.append(register[i])
            #print(i,invspr, itr)
            if tilesyaml["sprites"][register[i]]["floor"] == True:
                floor.append(register[i])
            if tilesyaml["sprites"][register[i]]["fireable"] == True:
                fireable.append(register[i])
            if itr == 18:
                itr = 0
                invlineload += 1
            rezervedspr.append(register[i])
        else:
            mb.showerror("Ошибка", "В tiles.yml спользуется зарезервированный символ: "+register[i]+", нажмите 'ОК', и ошимка будет проигнорирована!")
        

#STDSPRITELOADER - загружаем стандартные спрайты. (некоторые стандартные и все модовские)
for s in range(len(stdload)):
    if s < 12:
        spr[stdload[s]] = Image.open("data/sprites/"+sprpath[s]+".png")
    else:
        spr[stdload[s]] = Image.open("custom/sprites/"+sprpath[s]+".png")
    spr[stdload[s]]= spr[stdload[s]].resize((64, 64))
    spr[stdload[s]] = ImageTk.PhotoImage(spr[stdload[s]])

canvas = Canvas(bg="blue", width=1920, height=1080)
canvas.place(x= -5, y= -5)

#Загружаем картинки для GUI
gui["inventory"] = Image.open("data/gui/inventory.png")
gui["inventory"] = gui["inventory"].resize((1200, 700))
gui["inventory"] = ImageTk.PhotoImage(gui["inventory"])
gui["hotbar"] = Image.open("data/gui/hotbar.png")
gui["hotbar"] = gui["hotbar"].resize((1500, 100))
gui["hotbar"] = ImageTk.PhotoImage(gui["hotbar"])

#Загружаем остальные картинки
if True:

    sound["place"] = pygame.mixer.Sound('data/sound/place.mp3')
    sound["dog1"] = pygame.mixer.Sound('data/sound/animal/dog1.mp3')
    sound["dog2"] = pygame.mixer.Sound('data/sound/animal/dog2.mp3')
    sound["duck"] = pygame.mixer.Sound('data/sound/animal/duck.mp3')
    sound["water"] = pygame.mixer.Sound('data/sound/water.mp3')
    
    particles["S1"] = Image.open("data/particles/snow/snow1.png")
    particles["S2"] = Image.open("data/particles/snow/snow2.png")

    particles["S1"]= particles["S1"].resize((9, 9))
    particles["S2"]= particles["S2"].resize((9, 9))

    particles["S1"] = ImageTk.PhotoImage(particles["S1"])
    particles["S2"] = ImageTk.PhotoImage(particles["S2"])
    
    if isNewYear == True:
        spr["C0"] = Image.open("data/sprites/NewYear/corgi.png")
        spr["@0"] = Image.open("data/sprites/NewYear/pembroke.png")
        spr["Z0"] = Image.open("data/sprites/NewYear/duck.png")
    else:
        spr["C0"] = Image.open("data/sprites/corgi.png")
        spr["@0"] = Image.open("data/sprites/pembroke.png")
        spr["Z0"] = Image.open("data/sprites/duck.png")
    spr["Q"] = Image.open("data/sprites/door.png")
    spr["F1"] = Image.open("data/sprites/Animated/fire/fire1.png")
    spr["F2"] = Image.open("data/sprites/Animated/fire/fire2.png")
    spr["F3"] = Image.open("data/sprites/Animated/fire/fire3.png")
    spr["W1"] = Image.open("data/sprites/Animated/water/water1.png")
    spr["W2"] = Image.open("data/sprites/Animated/water/water2.png")
    spr["W3"] = Image.open("data/sprites/Animated/water/water3.png")
    spr["D1"] = Image.open("data/sprites/NewYear/spruce1.png")
    spr["D2"] = Image.open("data/sprites/NewYear/spruce2.png")
    spr["X"] = Image.open("data/sprites/fireplace.png")
        
    spr["C0"] = spr["C0"].resize((64, 64))
    spr["@0"] = spr["@0"].resize((64, 64))
    spr["Z0"] = spr["Z0"].resize((64, 64))
    spr["Q"] = spr["Q"].resize((64, 64))
    spr["F1"] = spr["F1"].resize((64, 64))
    spr["F2"] = spr["F2"].resize((64, 64))
    spr["F3"] = spr["F3"].resize((64, 64))
    spr["W1"] = spr["W1"].resize((64, 64))
    spr["W2"] = spr["W2"].resize((64, 64))
    spr["W3"] = spr["W3"].resize((64, 64))
    spr["D1"]= spr["D1"].resize((64, 64))
    spr["D2"]= spr["D2"].resize((64, 64))
    spr["X"]= spr["X"].resize((64, 64))
        
    spr["E"] = spr["Q"].rotate(90)
    spr["C"] = spr["X"].rotate(90)
    spr["$"] = spr["X"].rotate(180)
    spr[";"] = spr["X"].rotate(270)

    spr["C1"] = spr["C0"].rotate(90)
    spr["C2"] = spr["C0"].rotate(180)
    spr["C3"] = spr["C0"].rotate(270)

    spr["@1"] = spr["@0"].rotate(90)
    spr["@2"] = spr["@0"].rotate(180)
    spr["@3"] = spr["@0"].rotate(270)

    spr["Z1"] = spr["Z0"].rotate(90)
    spr["Z2"] = spr["Z0"].rotate(180)
    spr["Z3"] = spr["Z0"].rotate(270)


    spr["D1"] = ImageTk.PhotoImage(spr["D1"])
    spr["D2"] = ImageTk.PhotoImage(spr["D2"])
    spr["X"] = ImageTk.PhotoImage(spr["X"])
    spr["C"] = ImageTk.PhotoImage(spr["C"])
    spr["$"] = ImageTk.PhotoImage(spr["$"])
    spr[";"] = ImageTk.PhotoImage(spr[";"])
    
    spr["W1"] = ImageTk.PhotoImage(spr["W1"])
    spr["W2"] = ImageTk.PhotoImage(spr["W2"])
    spr["W3"] = ImageTk.PhotoImage(spr["W3"])

    spr["Q"] = ImageTk.PhotoImage(spr["Q"])
    spr["E"] = ImageTk.PhotoImage(spr["E"])

    spr["F1"] = ImageTk.PhotoImage(spr["F1"])
    spr["F2"] = ImageTk.PhotoImage(spr["F2"])
    spr["F3"] = ImageTk.PhotoImage(spr["F3"])

    spr["C0"] = ImageTk.PhotoImage(spr["C0"])
    spr["C1"] = ImageTk.PhotoImage(spr["C1"])
    spr["C2"] = ImageTk.PhotoImage(spr["C2"])
    spr["C3"] = ImageTk.PhotoImage(spr["C3"])

    spr["@0"] = ImageTk.PhotoImage(spr["@0"])
    spr["@1"] = ImageTk.PhotoImage(spr["@1"])
    spr["@2"] = ImageTk.PhotoImage(spr["@2"])
    spr["@3"] = ImageTk.PhotoImage(spr["@3"])

    spr["Z0"] = ImageTk.PhotoImage(spr["Z0"])
    spr["Z1"] = ImageTk.PhotoImage(spr["Z1"])
    spr["Z2"] = ImageTk.PhotoImage(spr["Z2"])
    spr["Z3"] = ImageTk.PhotoImage(spr["Z3"])
    
#Функция возврата в главное меню
def tomain():
    mamen.destroy()
    try:
        summer.destroy()
        winter.destroy()
        l0.destroy()
        moderad1.destroy()
        moderad2.destroy()
    except:
        pass
    try:
        versti.destroy()
        l1.destroy()
        e1.destroy()
        b1.destroy()
        l2.destroy()
        l3.destroy()
        e2.destroy()
        e3.destroy()
        seedentry.destroy()
        summer.destroy()
        winter.destroy()
        ls.destroy()
    except:
        pass
    
    main_menu()

#Генератор карты
def gen():
    global dog
    global gm, fire, firebu, water, seedentry, l4, summer, winter, isWinter, paramount
    global h
    global w
    global n
    global mamen
    global dogs
    global stv
    global startsm
    global qwerty
    global l1
    global l2
    global l3
    global e1
    global e2
    global e3
    global b1
    global mamen, l0, moderad1, moderad2, ls
    asdfg=True
    mmex.destroy()
    dogbuf = []
    dogrot = []
    gm = []
    dogs = []
    fire=[]
    firebu=[]
    duck=[]
    duckbuf=[]
    duckrot=[]
    try:
        mmg.destroy()
        mml.destroy()
        dl.destroy()
        prodo.destroy()
        rodo.destroy()
        erod.destroy()
        sav.destroy()
        exi.destroy()
    except:
        pass
    def br():
        global qwerty
        qwerty=True
    mamen = Button(text="Обратно", width=15, height=3, command=tomain)
    mamen.pack()
    b1 = Button(text="Создать", width=15, height=3, command=br)
    b1.pack()
    varia = BooleanVar()
    varia.set(True)
    l0 = Label(text="Режим:", font="Arial 15")
    l0.pack(side=TOP)
    moderad1 = Radiobutton(text="Продвинутый", variable=varia, value=True)
    moderad2 = Radiobutton(text="Старый", variable=varia, value=False)
    moderad1.pack()
    moderad2.pack()
    vari = IntVar()
    vari.set(0)
    ls = Label(text="Время года:", font="Arial 15")
    ls.pack()
    summer = Radiobutton(text="Лето", variable=vari, value=0)
    winter = Radiobutton(text="Зима", variable=vari, value=1)
    summer.pack()
    winter.pack()
    l1 = Label(text="Имя:", font="Arial 20")
    l1.pack(side=TOP)
    e1 = Entry(width=50)
    e1.pack(side=TOP)
    l2 = Label(text="Высота:", font="Arial 20")
    l2.pack(side=TOP)
    e2 = Entry(width=50)
    e2.pack(side=TOP)
    l3 = Label(text="Ширина:", font="Arial 20")
    l3.pack(side=TOP)
    e3 = Entry(width=50)
    e3.pack(side=TOP)
    if varia.get() == True:
        l4 = Label(text="Зерно:", font="Arial 20")
        l4.pack(side=TOP)
        seedentry = Entry(width=50)
        seedentry.pack(side=TOP)
    while qwerty == False:
        if varia.get() == True:
            l4.pack()
            seedentry.pack(side=TOP)
        else:
            l4.pack_forget()
            seedentry.pack_forget()
        root.update()
        time.sleep(0.1)
    n=e1.get()
    h=e2.get()
    w=e3.get()
    while asdfg==True:
        try:
            w=int(w)
            h=int(h)
            asdfg=False
        except:
            qwerty = False
            while qwerty == False:
                root.update()
                time.sleep(0.1)
            n=e1.get()
            h=e2.get()
            w=e3.get()
            asdfg=True
    l0.destroy()
    ls.destroy()
    moderad1.destroy()
    moderad2.destroy()
    summer.destroy()
    winter.destroy()
    #GENERATOR - выше был GUI и настройки, ниже - сам генератор

    if vari.get() == 0:
        isWinter = False
    else:
        isWinter = True

    if varia.get() == True:
        seed = ""
        seedlist = list(str(seedentry.get()))
        for sad in range(len(seedlist)):
            seed += str(ord(seedlist[sad]))
        try:
            versti.destroy()
            l1.destroy()
            e1.destroy()
            b1.destroy()
            l2.destroy()
            l3.destroy()
            e2.destroy()
            e3.destroy()
            seedentry.destroy()
            l4.destroy()
            mamen.destroy()
            ls.destroy()
        except NameError:
            pass
        progresslabel = Label(text="Генерация: генерация шума Перлина...", font="Arial 20")
        progresslabel.pack(side=TOP)
        root.update()

        noise = PerlinNoise(octaves=int(w/10+2), seed=int(seed))
        xpix, ypix = w, h
        progresslabel["text"] = "Генерация: генерация шума Перлина.."
        root.update()
        pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
        progresslabel["text"] = "Генерация: генерация шума Перлина."
        root.update()
        if isWinter == False:
            for thisline in range(len(pic)):
                for thistile in range(len(pic[thisline])):
                    try:
                        if pic[thisline][thistile] < -0.3:
                            pic[thisline][thistile] = "W"
                        if pic[thisline][thistile] >= -0.3 and pic[thisline][thistile] < -0.1:
                            pic[thisline][thistile] = "B"
                        if pic[thisline][thistile] >= -0.1 and pic[thisline][thistile] < 0.25:
                            pic[thisline][thistile] = "G"
                        if pic[thisline][thistile] >= 0.25:
                            pic[thisline][thistile] = "M"
                    except:
                        pass
                    #progresslabel.destroy()
                    progresslabel["text"] = "Генерация: генерация строк "+str(thisline)+"/"+str(h)# = Label(text="Генерация: генерация строк "+str(thisline)+"/"+str(h), font="Arial 20")
                    root.update()
        else:
            for thisline in range(len(pic)):
                for thistile in range(len(pic[thisline])):
                    try:
                        if pic[thisline][thistile] < -0.3:
                            pic[thisline][thistile] = "I"
                        if pic[thisline][thistile] >= -0.3 and pic[thisline][thistile] < -0.1:
                            pic[thisline][thistile] = "V"
                        if pic[thisline][thistile] >= -0.1 and pic[thisline][thistile] < 0.25:
                            pic[thisline][thistile] = "N"
                        if pic[thisline][thistile] >= 0.25:
                            pic[thisline][thistile] = "M"
                    except:
                        pass
                    progresslabel["text"] = "Генерация: генерация строк "+str(thisline)+"/"+str(h)# = Label(text="Генерация: генерация строк "+str(thisline)+"/"+str(h), font="Arial 20")
                    root.update()
        progresslabel.destroy()
        gm = list(itertools.chain(*pic))
        
        for jf in range(len(gm)):
            if gm[jf] == "W" or gm[jf] == "I":
                water.append(jf)

    else:
        if isWinter == False:
            for x in range(h*w):
                gm.append("G")
        else:
            for x in range(h*w):
                gm.append("N")

     
    dog = 0
    bu = gm[int(len(gm)/2)]
    gm[int(len(gm)/2)] = "*"
    startsm = True
    main(dog, gm, h, w, n, [], int(len(gm)/2), bu, 1, [], [], True, True, True, [], [], [], True, 0, True, isWinter, paramount)
    
#Загрузяик миров
def load():
    #настройки всякие. И GUI
    global nolo
    global qwerty
    qwerty = False
    def bri():
        global qwerty
        qwerty=True
    global l1
    global e1
    global b1
    global dog
    global gm, water
    global h
    global w
    global n
    global dogs
    global startsm
    global stv
    global mamen
    global paramount
    dogbuf = []
    dogrot = []
    gm = []
    dogs = []
    fire = []
    firebu = []
    duckbuf = []
    duckrot = []
    duck = []
    mmex.destroy()
    gysdz = 0
    doopenfile=True
    try:
        mmg.destroy()
        mml.destroy()
        dl.destroy()
        prodo.destroy()
        rodo.destroy()
        erod.destroy()
        sav.destroy()
        exi.destroy()
    except:
        pass
    mamen = Button(text="Обратно", width=15, height=3, command=tomain)
    mamen.pack()
    l1 = Label(text="Имя:", font="Arial 20")
    l1.pack(side=TOP)
    e1 = Entry(width=50)
    e1.pack(side=TOP)
    b1 = Button(text="Загрузить", width=15, height=3, command=bri)
    b1.pack()

    while qwerty == False:
        root.update()
        time.sleep(0.1)

    n=e1.get()
        
    n=e1.get()
    loadvers = ""
    
    #Загружаем основную дату
    try:
        f = open("worlds/"+n+"/data.csave","r")
        for line in f:
            gysdz = gysdz+1
            if gysdz==1:
                w=int(line)
            if gysdz==2:
                h=int(line)
            if gysdz==3:
                stv=int(line)
            if gysdz==4:
                dog=int(line)
            if gysdz==5:
                loadvers=line
            if gysdz==6:
                plrot=int(line)
            if gysdz==7:
                bu=line.replace("\n", "")
            if gysdz==8:
                if line.replace("\n", "") == "True":
                    isWinter = True
                if line.replace("\n", "") == "False":
                    isWinter = False
            if gysdz==9:
                seasontick=int(line)
        f.close()
        #Проверяем версию
        loadvers = loadvers.replace("\n", "")
        if loadvers != version:
            mb.showerror("Ошибка совместимости!", "Мир был в последний раз сохранен в версии "+str(loadvers)+", вы используете "+version+" загружайте на свой страх и риск!")
        f = open("worlds/"+n+"/map.csave")
        gm=list(f.read())
        f.close()
        #Загружаем остальные списки
        f = open("worlds/"+n+"/dogs.csave")
        for line in f:
            if line != "None":
                dogs.append(int(line))
        f.close()

        f = open("worlds/"+n+"/dogrot.csave")
        for line in f:
            if line != "None":
                dogrot.append(int(line))
        f.close()

        f = open("worlds/"+n+"/dogbuf.csave")
        #print(f.closed)
        for line in f:
            mystr = re.sub(r"[\n]", "", line)
            if mystr != "None":
                dogbuf.append(mystr)
        f.close()

        f = open("worlds/"+n+"/firebuf.csave")
        #print(f.closed)
        for line in f:
            mystr = re.sub(r"[\n]", "", line)
            firebu.append(mystr)
        f.close()
        
        f = open("worlds/"+n+"/fire.csave")
        for line in f:
            fire.append(int(line))
        f.close()

        f = open("worlds/"+n+"/water.csave")
        for line in f:
            water.append(int(line))
        f.close()

        f = open("worlds/"+n+"/duck.csave")
        for line in f:
            duck.append(int(line))
        f.close()

        f = open("worlds/"+n+"/duckrot.csave")
        for line in f:
            duckrot.append(int(line))
        f.close()

        f = open("worlds/"+n+"/duckbuf.csave")
        for line in f:
            duckbuf.append(re.sub(r"[\n]", "", line))
        f.close()
    except FileNotFoundError:
        mb.showerror("Ошибка", "Мир",n," не найден!")
    dog=int(dog)
    gm[stv] = "*"
    startsm = True
    main(dog, gm, h, w, n, dogs, stv, bu, plrot, dogrot, dogbuf, True, True, True, duck, duckbuf, duckrot, True, seasontick, True, isWinter, paramount)
#Функция выхода
def exitt():
    print("You don't own the corgi, it is the corgi who own you!") #Пасхалочка)))
    global nolo
    nolo = True
    root.destroy()

turbomode = False

#Функция смены сезонов
def seasonreplacer(dog, gm, h, w, n, dogs, stv, bu, plrot, dogrot, dogbuf, DAI, collision, fanim, duck, duckbuf, duckrot, turbomode, seasontick, nextseason, isWinter, paramount):
    if isWinter == False:
        for hkicsdkhsdhu in range(2):
            isWinter = True
            for rtr in range(len(gm)):
                if gm[rtr] == "#":
                    gm[rtr] = "!"
            for trt in range(len(dogbuf)):
                if dogbuf[trt] == "#":
                    dogbuf[trt] = "!"
                elif dogbuf[trt] == "W":
                    dogbuf[trt] = "I"
            for trt in range(len(duckbuf)):
                if duckbuf[trt] == "W":
                    duckbuf[trt] = "I"
                if duckbuf[trt] == "#":
                    duckbuf[trt] = "!"
            for trt in range(len(water)):
                gm[water[trt]] = "I"

            if bu == "#":
                bu = "!"
            elif bu == "W":
                bu = "I"
    else:
        isWinter = False
        for dkajlkjld in range(2):
            for rtr in range(len(gm)):
                if gm[rtr] == "!":
                    gm[rtr] = "#"
                elif gm[rtr] == "I":
                    gm[rtr] = "W"
            for trt in range(len(dogbuf)):
                if dogbuf[trt] == "!":
                    dogbuf[trt] = "#"
                elif dogbuf[trt] == "I":
                    dogbuf[trt] = "W"
            for trt in range(len(duckbuf)):
                if duckbuf[trt] == "I":
                    duckbuf[trt] = "W"
                if duckbuf[trt] == "!":
                    duckbuf[trt] = "#"
            #for trt in range(len(water)):
            #    gm[water[trt]] = "W"
        if bu == "!":
            bu = "#"
        elif bu == "I":
            bu = "W"
    seasontick = 0
    main(dog, gm, h, w, n, dogs, stv, bu, plrot, dogrot, dogbuf, DAI, collision, fanim, duck, duckbuf, duckrot, turbomode, seasontick, nextseason, isWinter, paramount)


    
#Меню настроек
def settings(dog, gm, h, w, n, dogs, stv, bu, plrot, dogrot, dogbuf, DAI, collision, fanim, duck, duckbuf, duckrot, turbomode, seasontick, nextseason, isWinter, paramount):
    global dogValue, chkExample, vki, chkExample, colValue, colExample, fValue, fExample, turboValue, iswValue, seasonValue
    def toseasonreplacer():
        chkExample.destroy()
        vki.destroy()
        colExample.destroy()
        fExample.destroy()
        turbo.destroy()
        season.destroy()
        nsb.destroy()
        seasonreplacer(dog, gm, h, w, n, dogs, stv, bu, plrot, dogrot, dogbuf, DAI, collision, fanim, duck, duckbuf, duckrot, turbomode, seasontick, nextseason, isWinter, paramount)
    def tom():
        turbomode = turboValue.get()
        #print(turbomode)
        DAI = dogValue.get()
        collision = colValue.get()
        nextseason = seasonValue.get()
        fanim = fValue.get()
        chkExample.destroy()
        vki.destroy()
        colExample.destroy()
        fExample.destroy()
        turbo.destroy()
        season.destroy()
        nsb.destroy()
        main(dog, gm, h, w, n, dogs, stv, bu, plrot, dogrot, dogbuf, DAI, collision, fanim, duck, duckbuf, duckrot, turbomode, seasontick, nextseason, isWinter, paramount)
    sav.destroy()
    exi.destroy()
    sett.destroy()
    prodo.destroy()
    dl.destroy()

    dogValue = BooleanVar() 
    dogValue.set(DAI)
    colValue = BooleanVar()
    colValue.set(collision)
    fValue = BooleanVar() 
    fValue.set(fanim)
    turboValue = BooleanVar()
    turboValue.set(turbomode)
    seasonValue = BooleanVar()
    seasonValue.set(nextseason)


    vki = Button(text="Вернуться к игре", width=15, height=3, command=tom)
    nsb = Button(text="Следующий сезон", width=15, height=3, command=toseasonreplacer)
    chkExample = Checkbutton(root, text='ИИ собак', font="Arial 10", var=dogValue)
    colExample = Checkbutton(root, text='Коллизия', font="Arial 12", var=colValue)
    fExample = Checkbutton(root, text='Анимация огня', font="Arial 12", var=fValue)
    turbo = Checkbutton(root, text='Блокировка TPS', font="Arial 12", var=turboValue)
    season = Checkbutton(root, text='Смена сезонов', font="Arial 12", var=seasonValue)
    vki.pack()
    chkExample.pack()
    colExample.pack()
    fExample.pack()
    turbo.pack()
    season.pack()
    nsb.pack()
    
    root.update()



#Основной код игры
def main(dog, gm, h, w, n, dogs, stv, bu, plrot, dogrot, dogbuf, DAI, collision, fanim, duck, duckbuf, duckrot, turbomode, seasontick, nextseason, isWinter, paramount):
    global dl
    global prodo
    global sett
    global sav
    global exi
    global verti
    global prodsm, canvas, line

    canvas = Canvas(bg="blue", width=1920, height=1080)
    canvas.place(x= -5, y= -5)
    
    asda = True
    cicl = True
    slot=1
    root.config(cursor="none")
    try:
        verti.destroy()
        l1.destroy()
        e1.destroy()
        b1.destroy()
        l2.destroy()
        l3.destroy()
        e2.destroy()
        e3.destroy()
        mmex.destroy()
        s1.destroy()
    except:
        pass

    #lmap = Label(font="Arial 13")
    #lmap.pack(side=TOP)
    Simulation = True
    item=1
    thisdog = 0

    light = []
    for gf in range(len(gm)):
        light.append(0)
    
    def tosett():
        nonlocal turbomode
        settings(dog, gm, h, w, n, dogs, stv, bu, plrot, dogrot, dogbuf, DAI, collision, fanim, duck, duckbuf, duckrot, turbomode, seasontick, nextseason, isWinter, paramount)
    def prmap():
        nonlocal bu, isWinter, paramount
        try:
            canvas.delete("all")
            a=0
            
            imsrdx = 0
            imsrdy = -56
            
            lwt = stv-wwd
            lwt = lwt-hwd*w
            lwt += int(hwd/1.73+hwd/h)*w+int(wwd/2+wwd/w)
            for hlwnji in range(hwd):
                for geruiebrf in range (wwd):
                    if hlwnji != 0:
                        if gm[lwt+a] in stdspr:
                            canvas.create_image(imsrdx, imsrdy, image=spr[gm[lwt+a]])
                        elif gm[lwt+a] == "W" or bu == "W" and lwt+a in water:
                            ani = spr["W"+str(random.randint(1,3))]
                            canvas.create_image(imsrdx, imsrdy, image=ani)
                                    
                        elif gm[lwt+a] == "F":
                            canvas.create_image(imsrdx, imsrdy, image=spr[firebu[fire.index(lwt+a)]])
                                
                            if fanim == True:
                                ani = spr["F"+str(random.randint(1,3))]
                                canvas.create_image(imsrdx, imsrdy, image=ani)
                            else:
                                canvas.create_image(imsrdx, imsrdy, image=spt["F1"])
                        elif gm[lwt+a] == "*":
                            if bu == "G":
                                if isWinter == False:
                                    canvas.create_image(imsrdx, imsrdy, image=spr["G"])
                                else:
                                    canvas.create_image(imsrdx, imsrdy, image=spr["N"])
                            elif bu == "B":
                                if isWinter == False:
                                    canvas.create_image(imsrdx, imsrdy, image=spr["B"])
                                else:
                                    canvas.create_image(imsrdx, imsrdy, image=spr["V"])
                            elif bu == "F":
                                canvas.create_image(imsrdx, imsrdy, image=spr[firebu[fire.index(stv)]])
                                canvas.create_image(imsrdx, imsrdy, image=spr["F"+str(random.randint(1,3))])
                            elif bu == "W":
                                canvas.create_image(imsrdx, imsrdy, image=spr["W"+str(random.randint(1,3))])
                            else:
                                canvas.create_image(imsrdx, imsrdy, image=spr[bu])
                            
                            canvas.create_image(imsrdx, imsrdy, image=spr["C"+str(plrot)])

                        elif gm[lwt+a] == "G":
                            if isWinter == True:
                                canvas.create_image(imsrdx, imsrdy, image=spr["N"])
                            else:
                                canvas.create_image(imsrdx, imsrdy, image=spr["G"])
                        elif gm[lwt+a] == "B":
                            if isWinter == True:
                                canvas.create_image(imsrdx, imsrdy, image=spr["V"])
                            else:
                                canvas.create_image(imsrdx, imsrdy, image=spr["B"])
                        elif gm[lwt+a] == "@":
                            try:
                                thisdog = dogs.index(lwt+a)
                                canvas.create_image(imsrdx, imsrdy, image=spr[dogbuf[thisdog]])
                                canvas.create_image(imsrdx, imsrdy, image=spr["@"+str(dogrot[thisdog])])
                            except:
                                gm[dogs[thisdog]] = dogbuf[thisdog]
                                dogs[thisdog] = None
                                dogbuf[thisdog] = None
                                dogrot[thisdog] = None
                            if random.randint(0,999) == 150:
                                if random.randint(0,1) == 1:
                                    sound["dog1"].play()
                                else:
                                    sound["dog2"].play()
                        elif gm[lwt+a] == "Z":
                            thisduck = duck.index(lwt+a)
                            if duckbuf[thisduck] != "W":
                                canvas.create_image(imsrdx, imsrdy, image=spr[duckbuf[thisduck]])
                            else:
                                canvas.create_image(imsrdx, imsrdy, image=spr["W"+str(random.randint(1,3))])
                            canvas.create_image(imsrdx, imsrdy, image=spr["Z"+str(duckrot[thisduck])])
                            if random.randint(0,999) == 150:
                                sound["duck"].play()

                        elif gm[lwt+a] == "D":
                            if isWinter == True:
                                canvas.create_image(imsrdx, imsrdy, image=spr["D1"])
                            else:
                                canvas.create_image(imsrdx, imsrdy, image=spr["D2"])

                        
                        imsrdx += 64
                        a += 1
                a = 0
                a += w*hlwnji+1
                imsrdy += 64
                imsrdx = 37
            else:
                if isWinter == True:
                    for i in range(paramount):
                        canvas.create_image(random.randint(0, 1920), random.randint(0, 1080), image=particles["S"+str(random.randint(1,2))])
                
            if keyboard.is_pressed("tab"):
                canvas.create_image(775, 800, image=gui["hotbar"])
                itx = 220
                for i in range(len(hotbar)-1):
                    canvas.create_image(itx, 800, image=spr[idtospr[hotbar[i+1]]])
                    if i+1 == slot:
                        canvas.create_rectangle(itx+32, 800+32, itx-32, 800-32, outline="red")
                    itx += 100
        except:
            pass
        

        
                
    while cicl == True:
        if Simulation == True:
            a1 = time.perf_counter()
            if seasontick >= 7500:
                seasonreplacer(dog, gm, h, w, n, dogs, stv, bu, plrot, dogrot, dogbuf, DAI, collision, fanim, duck, duckbuf, duckrot, turbomode, seasontick, nextseason, isWinter, paramount)
        #WASD
            if keyboard.is_pressed('d'):
                plrot = 0
                if stv < w*h-2:
                    if collision == True:
                        if bu != "E":
                            if gm[stv+1] in floor or gm[stv+1] == "Q":
                                gm[stv] = bu
                                bu = gm[stv+1]
                                gm[stv+1] = "*"
                                stv = stv+1
                    else:
                        gm[stv] = bu
                        bu = gm[stv+1]
                        gm[stv+1] = "*"
                        stv = stv+1
            if keyboard.is_pressed('a'):
                plrot = 2
                if stv-1 > -1:
                    if collision == True:
                        if bu != "E":
                            if gm[stv-1] in floor or gm[stv-1] == "Q":
                                gm[stv] = bu
                                bu = gm[stv-1]
                                gm[stv-1] = "*"
                                stv = stv-1
                    else:
                        gm[stv] = bu
                        bu = gm[stv-1]
                        gm[stv-1] = "*"
                        stv = stv-1
            if keyboard.is_pressed('w'):
                plrot = 1
                if stv > w*9-1:
                    if collision == True:
                        if bu != "Q":
                            if gm[stv-w] in floor or gm[stv-w] == "E":
                                gm[stv] = bu
                                bu = gm[stv-w]
                                gm[stv-w] = "*"
                                stv = stv-w
                    if collision == False:
                        gm[stv] = bu
                        bu = gm[stv-w]
                        gm[stv-w] = "*"
                        stv = stv-w
            if keyboard.is_pressed('s'):
                plrot = 3
                if stv < w*h-w*2:
                    if collision == True:
                        if bu != "Q":
                            if gm[stv+w] in floor or gm[stv+w] == "E":
                                gm[stv] = bu
                                bu = gm[stv+w]
                                gm[stv+w] = "*"
                                stv = stv+w
                    if collision == False:
                        gm[stv] = bu
                        bu = gm[stv+w]
                        gm[stv+w] = "*"
                        stv = stv+w
        #BUILD
            try:
                if idtospr[hotbar[slot]] in stdplace:
                    if keyboard.is_pressed("right") and idtospr[hotbar[slot]] != gm[stv+1]:
                        gm[stv+1] = idtospr[hotbar[slot]]
                        sound["place"].play()
                    if keyboard.is_pressed("left") and idtospr[hotbar[slot]] != gm[stv-1]:
                        gm[stv-1] = idtospr[hotbar[slot]]
                        sound["place"].play()
                    if keyboard.is_pressed("up") and idtospr[hotbar[slot]] != gm[stv-w]:
                        gm[stv-w] = idtospr[hotbar[slot]]
                        sound["place"].play()
                    if keyboard.is_pressed("down") and idtospr[hotbar[slot]] != gm[stv+w]:
                        gm[stv+w] = idtospr[hotbar[slot]]
                        sound["place"].play()
                if hotbar[slot] == 4:
                    if keyboard.is_pressed("right") and "Q" != gm[stv+1]:
                        gm[stv+1] = "Q"
                        sound["place"].play()
                    if keyboard.is_pressed("left") and "Q" != gm[stv-1]:
                        gm[stv-1] = "Q"
                        sound["place"].play()
                    if keyboard.is_pressed("up") and "E" != gm[stv-w]:
                        gm[stv-w] = "E"
                        sound["place"].play()
                    if keyboard.is_pressed("down") and "E" != gm[stv+w]:
                        gm[stv+w] = "E"
                        sound["place"].play()
                if hotbar[slot] == 13:
                    if keyboard.is_pressed("right") and ";" != gm[stv+1]:
                        gm[stv+1] = ";"
                        sound["place"].play()
                    if keyboard.is_pressed("left") and "C" != gm[stv-1]:
                        gm[stv-1] = "C"
                        sound["place"].play()
                    if keyboard.is_pressed("up") and "X" != gm[stv-w]:
                        gm[stv-w] = "X"
                        sound["place"].play()
                    if keyboard.is_pressed("down") and "$" != gm[stv+w]:
                        gm[stv+w] = "$"
                        sound["place"].play()
                if hotbar[slot] == 6:
                    if keyboard.is_pressed("right") and "F" != gm[stv+1]:
                        if gm[stv+1] in fireable:
                            firebu.append(gm[stv+1])
                            fire.append(stv+1)
                            gm[stv+1] = "F"
                            sound["place"].play()
                    if keyboard.is_pressed("left") and "F" != gm[stv-1]:
                        if gm[stv-1] in fireable:
                            firebu.append(gm[stv-1])
                            fire.append(stv-1)
                            gm[stv-1] = "F"
                            sound["place"].play()
                    if keyboard.is_pressed("up") and "F" != gm[stv-w]:
                        if gm[stv-w] in fireable:
                            firebu.append(gm[stv-w])
                            fire.append(stv-w)
                            gm[stv-w] = "F"
                            sound["place"].play()
                    if keyboard.is_pressed("down") and "F" != gm[stv+w]:
                        if gm[stv+w] in fireable:
                            firebu.append(gm[stv+w])
                            fire.append(stv+w)
                            gm[stv+w] = "F"
                            sound["place"].play()
                if hotbar[slot] == 8:
                    if isWinter == False:
                        if keyboard.is_pressed("right") and "W" != gm[stv+1]:
                            water.append(stv+1)
                            gm[stv+1] = "W"
                            sound["place"].play()
                        if keyboard.is_pressed("left") and "W" != gm[stv-1]:
                            water.append(stv-1)
                            gm[stv-1] = "W"
                            sound["place"].play()
                        if keyboard.is_pressed("up") and "W" != gm[stv-w]:
                            water.append(stv-w)
                            gm[stv-w] = "W"
                            sound["place"].play()
                        if keyboard.is_pressed("down") and "W" != gm[stv+w]:
                            water.append(stv+w)
                            gm[stv+w] = "W"
                            sound["place"].play()
                    else:
                        if keyboard.is_pressed("right") and "I" != gm[stv+1]:
                            water.append(stv+1)
                            gm[stv+1] = "I"
                            sound["place"].play()
                        if keyboard.is_pressed("left") and "I" != gm[stv-1]:
                            water.append(stv-1)
                            gm[stv-1] = "I"
                            sound["place"].play()
                        if keyboard.is_pressed("up") and "I" != gm[stv-w]:
                            water.append(stv-w)
                            gm[stv-w] = "I"
                            sound["place"].play()
                        if keyboard.is_pressed("down") and "I" != gm[stv+w]:
                            water.append(stv+w)
                            gm[stv+w] = "I"
                            sound["place"].play()
                if hotbar[slot] == 12:
                    if isNewYear == True:
                        if keyboard.is_pressed("right") and "D" != gm[stv+1]:
                            gm[stv+1] = "D"
                            sound["place"].play()
                        if keyboard.is_pressed("left") and "D" != gm[stv-1]:
                            gm[stv-1] = "D"
                            sound["place"].play()
                        if keyboard.is_pressed("up") and "D" != gm[stv-w]:
                            gm[stv-w] = "D"
                            sound["place"].play()
                        if keyboard.is_pressed("down") and "D" != gm[stv+w]:
                            gm[stv+w] = "D"
                            sound["place"].play()
            except:
                pass
        #DOGSPAWN
            try:
                if hotbar[slot] == 2:
                    if keyboard.is_pressed("left") and gm[stv-1] in floor and "@" != gm[stv+1]:
                        dogs.append(stv-1)
                        dogbuf.append(gm[stv-1])
                        gm[dogs[thisdog]] = "@"
                        dog += 1
                        dogrot.append(0)
                        sound["place"].play()
                    if keyboard.is_pressed("up") and gm[stv-w] in floor and "@" != gm[stv-w]:
                        dogs.append(stv-w)
                        dogbuf.append(gm[stv-w])
                        gm[dogs[thisdog]] = "@"
                        dog += 1
                        dogrot.append(2)
                        sound["place"].play()
                    if keyboard.is_pressed("right") and gm[stv+1] in floor and "@" != gm[stv+1]:
                        dogs.append(stv+1)
                        dogbuf.append(gm[stv+1])
                        gm[dogs[thisdog]] = "@"
                        dog += 1
                        dogrot.append(1)
                        sound["place"].play()
                    if keyboard.is_pressed("down") and gm[stv+w] in floor and "@" != gm[stv+w]:
                        dogs.append(stv+w)
                        dogbuf.append(gm[stv+w])
                        gm[dogs[thisdog]] = "@"
                        dog += 1
                        dogrot.append(3)
                        sound["place"].play()
            except:
                pass

        #DUCKSPAWN
            if hotbar[slot] == 9:
                if keyboard.is_pressed("left"):
                    if gm[stv-1] == "W" or gm[stv-1] == "#" and "V" != gm[stv-1]:
                        duck.append(stv-1)
                        duckbuf.append(gm[stv-1])
                        gm[stv-1] = "Z"
                        sound["place"].play()
                        duckrot.append(0)
                if keyboard.is_pressed("up"):
                    if gm[stv-w] == "W" or gm[stv-w] == "#" and "V" != gm[stv-w]:
                        duck.append(stv-w)
                        duckbuf.append(gm[stv-w])
                        gm[stv-w] = "Z"
                        sound["place"].play()
                        duckrot.append(2)
                if keyboard.is_pressed("right"):
                    if gm[stv+1] == "W" or gm[stv+1] == "#" and "V" != gm[stv+1]:
                        duck.append(stv+1)
                        duckbuf.append(gm[stv+1])
                        gm[stv+1] = "Z"
                        sound["place"].play()
                        duckrot.append(1)
                if keyboard.is_pressed("down"):
                    if gm[stv+w] == "W" or gm[stv+w] == "#" and "V" != gm[stv+w]:
                        duck.append(stv+w)
                        duckbuf.append(gm[stv+w])
                        gm[stv+w] = "Z"
                        sound["place"].play()
                        duckrot.append(3)
        #SAVE - сохраняет мир
            def save():
                try:
                    os.mkdir("worlds/"+n)
                except:
                    pass
                
                handle = open("worlds/"+n+"/dogs.csave", "w")
                for savethisa in range(dog):
                    handle.write(str(dogs[savethisa]))
                    handle.write("\n")
                handle.close()
        #
                handle = open("worlds/"+n+"/map.csave", "w")
                for savethis in range(w*h):
                    handle.write(gm[savethis])
                handle.close()
        #
                handle = open("worlds/"+n+"/data.csave", "w")
                handle.write(str(w) + '\n')
                handle.write(str(h) + '\n')
                handle.write(str(stv) + '\n')
                handle.write(str(dog) + '\n')
                handle.write(version+"\n")
                handle.write(str(plrot)+"\n")
                handle.write(bu+"\n")
                handle.write(str(isWinter)+"\n")
                handle.write(str(seasontick)+"\n")
                handle.close()

                handle = open("worlds/"+n+"/dogbuf.csave", "w")
                for savethisa in range(dog):
                    handle.write(str(dogbuf[savethisa]))
                    handle.write("\n")
                handle.close()

                handle = open("worlds/"+n+"/dogrot.csave", "w")
                for savethisa in range(dog):
                    handle.write(str(dogrot[savethisa]))
                    handle.write("\n")
                handle.close()

                handle = open("worlds/"+n+"/firebuf.csave", "w")
                for savethisa in range(len(firebu)):
                    handle.write(str(firebu[savethisa]))
                    handle.write("\n")
                handle.close()

                handle = open("worlds/"+n+"/fire.csave", "w")
                for savethisa in range(len(fire)):
                    handle.write(str(fire[savethisa]))
                    handle.write("\n")
                handle.close()

                handle = open("worlds/"+n+"/water.csave", "w")
                for savethisa in range(len(water)):
                    handle.write(str(water[savethisa]))
                    handle.write("\n")
                handle.close()

                handle = open("worlds/"+n+"/duck.csave", "w")
                for savethisa in range(len(duck)):
                    handle.write(str(duck[savethisa]))
                    handle.write("\n")
                handle.close()

                handle = open("worlds/"+n+"/duckrot.csave", "w")
                for savethisa in range(len(duckrot)):
                    handle.write(str(duckrot[savethisa]))
                    handle.write("\n")
                handle.close()

                handle = open("worlds/"+n+"/duckbuf.csave", "w")
                for savethisa in range(len(duckbuf)):
                    handle.write(str(duckbuf[savethisa]))
                    handle.write("\n")
                handle.close()

                sl = Label(text = "Сохранено как "+n, font="Arial 13")
                sl.pack(side=BOTTOM)
                for hhghjhgh in range(10):
                    time.sleep(0.1)
                    root.update()
        
                sl.destroy()     
        #DOGSAI
            try:
                for thisdog in range(dog):
                    randstep=random.randint(1, 4)
                    if gm[dogs[thisdog]] != "@":
                        dogs.remove(dogs[thisdog])
                        dog -= 1
                    if DAI == True:
                        if random.randint(1,5) == 1:
                            if randstep == 1:
                                if dogs[thisdog] < w*h-1:
                                    if gm[dogs[thisdog]+1] in floor:
                                        gm[dogs[thisdog]] = dogbuf[thisdog]
                                        dogbuf[thisdog] = gm[dogs[thisdog]+1]
                                        gm[dogs[thisdog]+1] = "@"
                                        dogs[thisdog] = dogs[thisdog]+1
                                        dogrot[thisdog] = 0
                            if randstep == 2:
                                if dogs[thisdog-1] > 0:
                                    if gm[dogs[thisdog]-1] in floor:
                                        gm[dogs[thisdog]] = dogbuf[thisdog]
                                        dogbuf[thisdog] = gm[dogs[thisdog]-1]
                                        gm[dogs[thisdog]-1] = "@"
                                        dogs[thisdog] = dogs[thisdog]-1
                                        dogrot[thisdog] = 2
                            if randstep == 3:
                                if dogs[thisdog] > w-1:
                                    if gm[dogs[thisdog]-w] in floor:
                                        gm[dogs[thisdog]] = dogbuf[thisdog]
                                        dogbuf[thisdog] = gm[dogs[thisdog]-w]
                                        gm[dogs[thisdog]-w] = "@"
                                        dogs[thisdog] = dogs[thisdog]-w
                                        dogrot[thisdog] = 1
                            if randstep == 4:
                                if dogs[thisdog] < w*h-w:
                                    if gm[dogs[thisdog]+w] in floor:
                                        gm[dogs[thisdog]] = dogbuf[thisdog]
                                        dogbuf[thisdog] = gm[dogs[thisdog]+w]
                                        gm[dogs[thisdog]+w] = "@"
                                        dogs[thisdog] = dogs[thisdog]+w
                                        dogrot[thisdog] = 3
            except:
                pass
        #FIRE
            for cik in range(len(fire)):
                if isWinter == False:
                    try:
                        
                        if gm[fire[cik]] == "F" or gm[fire[cik]] == "*" or gm[fire[cik]] == "S" or gm[fire[cik]] == "G":
                            if random.randint(0,100) == 0:
                                if gm[fire[cik]+1] in fireable:
                                    fire.append(fire[cik]+1)
                                    firebu.append(gm[fire[cik]+1])
                                    gm[fire[cik]+1] = "F"

                            if random.randint(0,100) == 0:
                                if gm[fire[cik]-1] in fireable:
                                    fire.append(fire[cik]-1)
                                    firebu.append(gm[fire[cik]-1])
                                    gm[fire[cik]-1] = "F"

                            if random.randint(0,100) == 0:
                                if gm[fire[cik]+w] in fireable:
                                    fire.append(fire[cik]+w)
                                    firebu.append(gm[fire[cik]+w])
                                    gm[fire[cik]+w] = "F"

                            if random.randint(0,100) == 0:
                                if gm[fire[cik]-w] in fireable:
                                    fire.append(fire[cik]-w)
                                    firebu.append(gm[fire[cik]-w])
                                    gm[fire[cik]-w] = "F"
                                    
                        if gm[fire[cik]] != "F" and gm[fire[cik]] != "*":
                            gm[fire[cik]] = firebu[cik]
                            fire[cik] = -1
                            firebu[cik] = ""
                        if random.randint(0,120) == 0 and gm[fire[cik]] != "*":
                            gm[fire[cik]] = "P"
                            fire[cik] = -1
                            firebu[cik] = ""
                            

                    except:
                        pass
                else:
                    gm[fire[cik]] = firebu[cik]
                    fire[cik] = -1
                    firebu[cik] = ""
    #WATER
            for waterwater in range(len(water)):
                try:         
                    if gm[water[waterwater]] != "W" and gm[water[waterwater]] != "Z" and gm[water[waterwater]] != "I" and gm[water[waterwater]] != "@" and gm[water[waterwater]] != "*":
                        water.remove(water[waterwater])
                    else:
                        if gm[water[waterwater]] == "W" or gm[water[waterwater]] == "Z":
                            if gm[water[waterwater]+1] in floor and gm[water[waterwater]+1] != "#":
                                gm[water[waterwater]+1] = "#"
                                sound["water"].play()
                            if gm[water[waterwater]-1] in floor and gm[water[waterwater]-1] != "#":
                                gm[water[waterwater]-1] = "#"
                                sound["water"].play()
                            if gm[water[waterwater]-w] in floor and gm[water[waterwater]-w] != "#":
                                gm[water[waterwater]-w] = "#"
                                sound["water"].play()
                            if gm[water[waterwater]+w] in floor and gm[water[waterwater]+w] != "#":
                                gm[water[waterwater]+w] = "#"
                                sound["water"].play()
                                            
                            if stv == water[waterwater]+1 or stv == water[waterwater]-1 or stv == water[waterwater]+w or stv == water[waterwater]-w:
                                bu = "#"
                except:
                    pass

                            

            #DUCKAI
            if isWinter == False:
                try: 
                    for thisduck in range(len(duck)):
                        randstep=random.randint(1, 4)
                        if gm[duck[thisduck]] != "Z":
                            duck.remove(duck[thisduck])
                        else:
                            if random.randint(1,6) == 1:
                                if randstep == 1:
                                    if duck[thisduck] < w*h-1:
                                        if gm[duck[thisduck]+1] == "W" or gm[duck[thisduck]+1] == "#":
                                            gm[duck[thisduck]] = duckbuf[thisduck]
                                            duckbuf[thisduck] = gm[duck[thisduck]+1]
                                            gm[duck[thisduck]+1] = "Z"
                                            duck[thisduck] = duck[thisduck]+1
                                            duckrot[thisduck] = 0
                            
                                if randstep == 2:
                                    if duck[thisduck] > 0:
                                        if gm[duck[thisduck]-1] == "W" or gm[duck[thisduck]-1] == "#":
                                            gm[duck[thisduck]] = duckbuf[thisduck]
                                            duckbuf[thisduck] = gm[duck[thisduck]-1]
                                            gm[duck[thisduck]-1] = "Z"
                                            duck[thisduck] = duck[thisduck]-1
                                            duckrot[thisduck] = 2
                            
                                if randstep == 3:
                                    if duck[thisduck] > w-1:
                                        if gm[duck[thisduck]-w] == "W" or gm[duck[thisduck]-w] == "#":
                                            gm[duck[thisduck]] = duckbuf[thisduck]
                                            duckbuf[thisduck] = gm[duck[thisduck]-w]
                                            gm[duck[thisduck]-w] = "Z"
                                            duck[thisduck] = duck[thisduck]-w
                                            duckrot[thisduck] = 1
                            
                                if randstep == 4:
                                    if duck[thisduck] < w*h-w:
                                        if gm[duck[thisduck]+w] == "W" or gm[duck[thisduck]+w] == "#":
                                            gm[duck[thisduck]] = duckbuf[thisduck]
                                            duckbuf[thisduck] = gm[duck[thisduck]+w]
                                            gm[duck[thisduck]+w] = "Z"
                                            duck[thisduck] = duck[thisduck]+w
                                            duckrot[thisduck] = 3
                except:
                    pass

                
        #PRINT

            if keyboard.is_pressed("f1"):
                slot = 1
            if keyboard.is_pressed("f2"):
                slot = 2
            if keyboard.is_pressed("f3"):
                slot = 3
            if keyboard.is_pressed("f4"):
                slot = 4
            if keyboard.is_pressed("f5"):
                slot = 5
            if keyboard.is_pressed("f6"):
                slot = 6
            if keyboard.is_pressed("f7"):
                slot = 7
            if keyboard.is_pressed("f8"):
                slot = 8
            if keyboard.is_pressed("f9"):
                slot = 9
            if keyboard.is_pressed("f10"):
                slot = 10
            if keyboard.is_pressed("f11"):
                slot = 11
            if keyboard.is_pressed("f12"):
                slot = 12
            
            if keyboard.is_pressed("esc"):
                prodsm = False
                def prodosm():
                    global prodsm
                    prodsm=True
                cicl = False
                root.config(cursor="")
                dl = Label(text = "ПАУЗА", font="Arial 20")
                prodo = Button(text="Продолжить", width=15, height=3, command=prodosm)
                sett = Button(text="Настройки", width=15, height=3, command=tosett)
                sav = Button(text="Сохранить", width=15, height=3, command=save)
                exi = Button(text="Выйти в меню", width=15, height=3, command=tomain)
                dl.pack(side=TOP)
                prodo.pack(side=TOP)
                sett.pack(side=TOP)
                sav.pack(side=TOP)
                exi.pack(side=TOP)
                while prodsm == False:
                    root.update()
                    time.sleep(0.1)
                cicl = True
                exi.destroy()
                sett.destroy()
                dl.destroy()
                prodo.destroy()
                sav.destroy()
                root.config(cursor="none")

            #INVENTORY
            if keyboard.is_pressed("E"):


                while keyboard.is_pressed("E"):
                    prmap()
                    root.config(cursor="")
                    canvas.create_image(770, 440, image=gui["inventory"])
                    imx = 220
                    imy = 140
                    Simulation = False
                    for y in range(len(invspr)):
                        for x in range(len(invspr[y])):
                            #if spr[invspr[x]] != "|p|":
                            canvas.create_image(imx, imy, image=spr[invspr[y][x]])
                            imx += 64
                        imy += 64
                        imx = 220
                    imx=220
                    x = root.winfo_pointerx()
                    y = root.winfo_pointery()
                    canvas.create_rectangle(220-32+(hotbar[slot]-1)*64-line*64*18,140-32+line*64,220+32+(hotbar[slot]-1)*64-line*64*18,140+32+line*64, outline="red")
                    if keyboard.is_pressed("right") and hotbar[slot] not in invedger:
                        hotbar[slot] += 1
                    if keyboard.is_pressed("left") and hotbar[slot] not in invedgel:
                        hotbar[slot] -= 1
                    if keyboard.is_pressed("down") and line < 9:
                        hotbar[slot] += 18
                        line += 1
                    if keyboard.is_pressed("up") and line > 0:
                        hotbar[slot] -= 18
                        line -= 1
                    root.update()
                root.config(cursor="none")
                Simulation = True
                hotbar[slot]
                
            if nextseason == True:
            prmap()
            root.update()
            if turbomode == True:
                if 0.08 - (time.perf_counter()-a1) > 0:
                    time.sleep(0.08 - (time.perf_counter()-a1))
                else:
                    pass
#Главное меню игры
def main_menu():
    root.config(cursor="")
    global mml
    global mmg
    global mmex
    global settin
    global versti

    def prmenbg():
        canvas = Canvas(bg="blue", width=1920, height=1080)
        canvas.place(x= -5, y= -5)
        try:
            canvas.delete("all")
        except:
            pass
        a=0
        #Да-да. Именно так хранится мир, который вы видите у себя на заднем фоне главного меню
        stv = 1308
        dogbuf = list("      ")
        dogrot = [0,2,1,3,1,2]
        dogs = [1408,1111,1154,1462,1508,1453]
        gm = list("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHGGGGGGGGGGGGGGGGGGHGHGGGGGGGGGGGGGGG*GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHHHHHHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHH   H @  HGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGH@H   Q    HGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGH H   H    HGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGH  H   HHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGH  Q  *H    HGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHHHHHEHHH    HGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGH       @H    HGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGH   @     Q  @ HGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGH       @H    HGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHHHHHHHHHHHHEHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
        #Добавим вам немного елочек в новый год
        if isNewYear == True:
            for trt in range(len(gm)):
                if gm[trt] == "G":
                    if random.randint(1, 30) != 1:
                        gm[trt] = "N"
                    else:
                        gm[trt] = "D"
        
        w=50
        h=50
        dog=6
        bu=" "
        
        imsrdx = 0
        imsrdy = -64
        lwt = stv-wwd
        lwt = lwt-hwd*w
        lwt += int(hwd/1.73+hwd/h)*w+int(wwd/2+wwd/w)
        try:
            for hlwnji in range(hwd):
                for geruiebrf in range (wwd):
                    if hlwnji != 0:
                        try:
                            imag = spr[gm[lwt+a]]
                            canvas.create_image(imsrdx, imsrdy, image=imag)
                        except:
                            pass

                                                
                        if gm[lwt+a] == "*":

                            try:
                                imag = spr[bu]
                                canvas.create_image(imsrdx, imsrdy, image=imag)
                            except:
                                pass
                            canvas.create_image(imsrdx, imsrdy, image=spr["C1"])
                        
                        if gm[lwt+a] == "@":
                            thisdog = dogs.index(lwt+a)
                            imag = spr[dogbuf[thisdog]]
                            canvas.create_image(imsrdx, imsrdy, image=imag)
                            canvas.create_image(imsrdx, imsrdy, image=spr["@"+str(dogrot[thisdog])])
                        if gm[lwt+a] == "D":
                            canvas.create_image(imsrdx, imsrdy, image=spr["D1"])
                            
                            
                        imsrdx += 64
                        a += 1
                a = 0
                a += w*hlwnji+1
                imsrdy += 64
                imsrdx = 37
            if isNewYear == True:
                for i in range(1000):
                    canvas.create_image(random.randint(0, 1920), random.randint(0, 1080), image=particles["S"+str(random.randint(1,2))])
        except IndexError:
            pass
    
    try:
        versti.destroy()
        l1.destroy()
        e1.destroy()
        b1.destroy()
        l2.destroy()
        l3.destroy()
        e2.destroy()
        e3.destroy()
        seedentry.destroy()
        l4.destroy()
        summer.destroy()
        winter.destroy()
    except NameError:
        pass
    try:
        sav.destroy()
        exi.destroy()
        sett.destroy()
        prodo.destroy()
        dl.destroy()
    except NameError:
        pass
    prmenbg()

    if isNewYear == True:
        if tilesyaml["enabled"] == True:
            versti = Label(text = "Версия: "+version+" С новым годом!\nЗагрузчик модификаций включен.", font="Arial 13")
        else:
            versti = Label(text = "Версия: "+version+" С новым годом!", font="Arial 13")
    else:
        if tilesyaml["enabled"] == True:
            versti = Label(text = "Версия: "+version+"\nЗагрузчик модификаций включен.", font="Arial 13")
        else:
            versti = Label(text = "Версия: "+version, font="Arial 13")
    mml = Button(text="Создать мир", width=15, height=3, command=gen)
    mmg = Button(text="Загрузить мир", width=15, height=3, command=load)
    mmex = Button(text="Выйти", width=15, height=3, command=exitt)
    mml.pack(side=TOP)
    mmg.pack(side=TOP)
    mmex.pack(side=TOP)
    versti.pack(side=BOTTOM)
    while startsm == False:
        root.update()
        time.sleep(0.1)
#Игра начинается от сюда. С конца.
main_menu()
