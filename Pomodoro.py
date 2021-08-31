import time
import pygame
import tkinter as tk
from tkinter import ttk
from datetime import timedelta
import re


class Menu(tk.Tk): # this class will create all window and access it
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.title("Pomodoro")
        self.geometry("700x447")
        self.resizable(0,0)
        self.iconbitmap("Timer.ico")
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand="True")
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)


        self.frame={} # dito lahat lalagay yung mga window para maaccess

        for F in (FirstPage,TimerPage):
            frame = F(container,self)
            self.frame[F] = frame
            frame.grid(row=0,column=0,sticky = "nsew")

        self.show_frame(FirstPage)

    def show_frame(self,cont):
            frame = self.frame[cont]
            frame.tkraise()

class FirstPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.background(controller)
        self.widgets = self.winfo_children()

    def changeWindow(self,controller):  # this point you will change other frame
        your_name = self.name.get()
        your_set = self.age.get()
        if(len(your_name)==0 or len(your_set)==0): # check if you dont type a word or number in Name and age
            return
        self.entry1.destroy() # this will destroy the entry box before you change window
        self.entry2.destroy()
        controller.show_frame(TimerPage)

    def background(self,controller):
        self.name = tk.StringVar()
        self.age = tk.StringVar()
        self.images=tk.PhotoImage(file="Pomodoro.png")
        self.backround_label = tk.Label(self,image=self.images,highlightthickness=0)
        self.backround_label.place(x=0,y=0,relwidth=1,relheight=1)
        self.label1=ttk.Label(self,text="Pomodoro",font=("Gill Sans MT",34,),background="#FFBFBF")
        self.label1.place(x=400,y=70)
        self.label2=ttk.Label(self,text="Name: ",font=("Gill Sans MT",20),background="#FFBFBF")
        self.label2.place(x=400,y=180)
        self.entry1 = ttk.Entry(font=("Gill Sans MT",13),justify="center",textvariable=self.name)
        self.entry1.focus()
        self.entry1.place(x=490,y=187,width=180,height=30)
        self.label3=ttk.Label(self,text="Age: ",font=("Gill Sans MT",20),background="#FFBFBF")
        self.entry2 = ttk.Entry(font=("Gill Sans MT",13),justify="center",textvariable=self.age)
        self.entry2.place(x=460,y=258)
        self.label3.place(x=400, y=250)
        self.button1=ttk.Button(self,text="Start",command=lambda:self.changeWindow(controller))
        self.button1.place(x=450,y=330,relheight=0.1)

class TimerPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.config(bg="gray")
        self.controller=controller
        self.hour = tk.StringVar()
        self.second = tk.StringVar()
        self.minute = tk.StringVar()
        self.widget()
        self.check=0 # check if you stop the timer siya yung mag hohold nung natira
        self.timer_stop=False # if you want to reset
        self.freeze_timer=False # if you want to freeze and maybe if you think to continue
        self.state_button=tk.NORMAL
        # start button, reset , stop
    def hr_limit_character_checker(self,*args):
        value = self.hour.get()
        if len(value) > 2 : self.hour.set(value[:2])

    def min_limit_character_checker(self,*args):
        value = self.minute.get()
        if len(value) > 2 : self.minute.set(value[:2])

    def sec_limit_character_checker(self,*args):
        value = self.second.get()
        if len(value) > 2 : self.second.set(value[:2])

    def widget(self):
        pygame.mixer.init()
        pygame.mixer.music.load("lofi.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(50)
        self.hour.trace('w',self.hr_limit_character_checker)
        self.minute.trace('w',self.min_limit_character_checker)
        self.second.trace('w',self.sec_limit_character_checker)

        self.entry1 = ttk.Entry(self, width=4,textvariable=self.hour,justify="center")
        self.hour.set("00")
        self.entry1.place(x=290,y=300)
        self.entry2 = ttk.Entry(self, width=4,textvariable=self.minute,justify="center")
        self.minute.set("00")
        self.entry2.place(x=330,y=300)
        self.entry3 = ttk.Entry(self,width=4,textvariable=self.second,justify="center")
        self.second.set("00")
        self.entry3.place(x=370,y=300)
        self.button1=ttk.Button(self,text="Start Time",command=self.start_timer,)
        self.button1.place(x=310,y=340)
        self.button2 = ttk.Button(self, text="Reset Time",command=self.reset_timer,state=tk.DISABLED)
        self.button2.place(x=310,y=380)
        self.button3 = ttk.Button(self, text="Stop Time",state=tk.DISABLED,command=self.stop_timer)
        self.button3.place(x=260,y=420)
        self.button4 = ttk.Button(self, text="Continue", command=self.countdown,state=tk.DISABLED)
        self.button4.place(x=360, y=420)
        self.label_time = tk.Label(self, text=str(timedelta(hours=int(self.hour.get()),minutes=int(self.minute.get()),seconds=int(self.second.get()))), font=("Times", 90))
        self.label_time.place(x=160, y=100)



    def stop_timer(self):
        self.check = self.time
        self.freeze_timer=True
        self.button4["state"] = tk.NORMAL
        self.button1["state"] = tk.DISABLED
        self.button2["state"] = tk.NORMAL
        self.button3["state"] = tk.NORMAL



    def reset_timer(self):
        self.hour.set("00")
        self.minute.set("00")
        self.second.set("00")
        self.label_time.config(text=str(timedelta(hours=int(self.hour.get()),minutes=int(self.minute.get()),seconds=int(self.second.get()))))
        self.timer_stop="True"
        self.button1["state"]= tk.NORMAL
        self.button2["state"] = tk.DISABLED
        self.button3["state"] = tk.DISABLED
        self.button4["state"]=tk.DISABLED

    def start_timer(self):
        try:
            int(self.hour.get())
            int(self.second.get())
            int(self.minute.get())
        except:
            return
        self.button1["state"] = tk.DISABLED
        self.button2["state"] = tk.NORMAL
        self.button3["state"] = tk.NORMAL
        self.time =  int(self.hour.get())*3600 + int(self.minute.get())*60 + int(self.second.get())
        self.countdown()

    def countdown(self):
        if(self.freeze_timer == False):
            self.button3["state"] = tk.NORMAL
        if(self.time==-1):
            self.button1["state"] = tk.NORMAL
            self.button2["state"] = tk.DISABLED
            self.button3["state"] = tk.DISABLED
            self.button4["state"] = tk.DISABLED
            return
        if self.timer_stop:
            self.button4["state"]=tk.DISABLED
            self.button3["state"] = tk.DISABLED
            self.timer_stop = False
            return
        if(self.freeze_timer):
            self.freeze_timer = False
            self.button3["state"] = tk.DISABLED
            return

        minute,second=(int(self.time)//60,int(self.time)%60)
        hour =0
        if minute>60:
            hour,minute=(int(minute)//60,int(minute)%60)

        self.label_time.config(text=str(timedelta(hours=hour,minutes=minute,seconds=second)))

        self.time -=1
        self.after(1000,self.countdown)

window = Menu()
window.mainloop()