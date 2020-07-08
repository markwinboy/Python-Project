"""Project #3 Game by Tkinter Python "Arcanoid"
Developer:
Karapetyants Mark Surenovich
"""
from tkinter import *

#Глобальные переменные
speed_x=10
speed_y=-10
speed_rec_r=25
speed_rec_l=-25
score=0
    
#Создание мишеней
def create_list_of_balls(number):
    y1=0
    y2=40
    l=[]
    color=["white","blue","red"]
    k=0
    while number != 0:
        x1=0
        x2=40
        lst = []
        if number >= 16:
            while len(lst) < 16:
                next_ball = canvas.create_rectangle(x1,y1,x2,y2,fill=color[k])
                lst.append(next_ball)
                x1+=40
                x2+=40
                l.append(next_ball)
        else:
            while len(lst) < (16-number):
                next_ball = canvas.create_rectangle(x1,y1,x2,y2,color[0])
                lst.append(next_ball)
                x1+=40
                x2+=40
                l.append(next_ball)
        k+=1
        y1+=40
        y2+=40
        number-=16
    return l

#Сдвиг блока вправо
def move_right(event):
    canvas.move(rec,speed_rec_r, 0)
    if canvas.coords(rec)[2] > 640 :
        canvas.move(rec,640-canvas.coords(rec)[2],0)
    pass

#Сдвиг блока влево
def move_left(event):
    canvas.move(rec, speed_rec_l, 0)
    if canvas.coords(rec)[0]< 0 :
        canvas.move(rec,-canvas.coords(rec)[0],0)

    pass

#Столкновение с мишенями
def collision(ball):
        a = abs(canvas.coords(Ball)[0]+10+speed_x-(canvas.coords(ball)[0]+20))
        b = abs(canvas.coords(Ball)[1]+10+speed_y-(canvas.coords(ball)[1]+20))
        return (a*a+b*b)**0.5 <= 30

#Движение Шара
def move_ball():
    global speed_x,speed_y,speed_rec_r,speed_rec_l,score
    if (canvas.coords(Ball)[0]+speed_x>=630) or (canvas.coords(Ball)[0]+speed_x<=0):
        speed_x=-speed_x
    if (canvas.coords(Ball)[3]+speed_y>=490) or (canvas.coords(Ball)[3]+speed_y<=0):
        speed_y=-speed_y
    if (canvas.coords(rec)[0]<canvas.coords(Ball)[2]<canvas.coords(rec)[2]) and (canvas.coords(rec)[1]==canvas.coords(Ball)[3]):
        speed_y=-speed_y
    if canvas.coords(Ball)[3]==480:
        canvas.create_text(320,240,text = "GAME OVER",font="Arial 30",fill = "red")
        speed_x=0
        speed_y=0
        speed_rec_r=0
        speed_rec_l=0
    if len(balls)==0:
        canvas.create_text(320,240,text = "YOU WIN!",font="Arial 30",fill = "green")
        speed_x=0
        speed_y=0
        speed_rec_r=0
        speed_rec_l=0
    for ball in balls:
        if collision(ball):
            if (canvas.coords(ball)[0]<canvas.coords(Ball)[0]<canvas.coords(ball)[2])and (canvas.coords(ball)[3]==canvas.coords(Ball)[1]):
                speed_y=-speed_y
            elif (canvas.coords(ball)[1]<canvas.coords(Ball)[1]<canvas.coords(ball)[3])and (canvas.coords(ball)[2]==canvas.coords(Ball)[0]):
                speed_x=-speed_x
            elif (canvas.coords(ball)[0]<canvas.coords(Ball)[2]<canvas.coords(ball)[2])and (canvas.coords(ball)[3]==canvas.coords(Ball)[1]):
                speed_y=-speed_y
            elif (canvas.coords(ball)[1]<canvas.coords(Ball)[3]<canvas.coords(ball)[3])and (canvas.coords(ball)[0]==canvas.coords(Ball)[2]):
                speed_x=-speed_x
            elif(canvas.coords(ball)[2]-20)==(canvas.coords(Ball)[0]+10):
                speed_y=-speed_y
            elif(canvas.coords(ball)[3]-20)==(canvas.coords(Ball)[1]+10):
                speed_x=-speed_x
            elif(canvas.coords(ball)[1]+20)==(canvas.coords(Ball)[3]-10):
                speed_y=-speed_y
            elif(canvas.coords(ball)[0]+20)==(canvas.coords(Ball)[2]+10):
                speed_x=-speed_x
            else:
                speed_y=-speed_y
            score+=2
            canvas.itemconfig(text,text=score)
            canvas.delete(ball)
            balls.remove(ball)

    canvas.move(Ball,speed_x,speed_y)

# Основная часть
def main():
    global Ball
    move_ball()
    root.after(50,main)
    

root = Tk()
root.title("Арканоид")
canvas = Canvas(root, width = 640, height = 480, bg = "#003300")
canvas.pack()
canvas.focus_set()
balls = create_list_of_balls(48)
text = canvas.create_text(610,450 ,text=score,font="Arial 20",fill="white")
canvas.create_line(0,470,640,470,fill="black")
rec = canvas.create_rectangle(260,470,420,480,fill = "white",outline = "black")
Ball=canvas.create_oval(320,440,340,460,fill="white")
root.bind('<Right>', move_right)
root.bind('<Left>', move_left)
main()
root.mainloop()
