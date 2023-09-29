import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.title("login") # window title

screenWidth = root.winfo_screenwidth() # screen width
screenHeight = root.winfo_screenheight() # screen height
left = int((screenWidth - 200) / 2)
top = int((screenHeight - 300) / 2)

windowwidth = 300
windowheight = 300
root.geometry("{0}x{1}+{2}+{3}".format(windowwidth,windowheight,left,top))

class MyFrame(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)

import json
import os
if not os.path.exists("auth.json"): # check file is exists
    with open("auth.json", "a+", encoding="utf-8") as f:
        json.dump({"root":"123456", "admin":"654321"},f)
    
try: # read auth.json
    with open("auth.json", "r+", encoding="utf-8") as f:
        usermap = json.load(fp=f)
except:
    raise Exception("`auth.json` content is not true")

print (usermap)
# usermap = {"root":"123456", "admin":"654321"}

def login(e):
    passpword = usermap.get(userText.get(), None)
    if passwordText.get() == passpword: # check password
        messagebox.showinfo(title = "login in", message = "login successfully")
        return
    messagebox.showerror(title = "login in", message = "login failed")
        
    # print (userText.get())
    # print (passwordText.get())
    
tk.Label(text="").grid(row=0,column=0,columnspan=10)
tk.Label(text="username:").grid(row=1,column=0)
tk.Label(text="password:").grid(row=2,column=0)
tk.Label(text="press 'ctrl+l' login in it").grid(row=3,column=5,columnspan=10)

userText = tk.Entry()
passwordText = tk.Entry()
userText.focus()
global textFocusIndex # TextBox number
textFocusIndex = 0

root.bind("<Control-l>", func=login) # 绑定ctrl+l按键, global events
def changeTextFocus(e): # change focus
    global textFocusIndex
    if textFocusIndex == 0:
        textFocusIndex = 1
    else:
        textFocusIndex = 0

    textGroup[textFocusIndex].focus()


def setTextFocus(e,index):
    global textFocusIndex
    textFocusIndex = index
    # print ("set",textFocusIndex)
    textGroup[textFocusIndex].focus()

textGroup = [userText, passwordText]
for index in range(len(textGroup)):
    textGroup[index].bind("<Return>", func=changeTextFocus) # key return
    textGroup[index].bind("<Button>", func=lambda e,x = index:setTextFocus(e,x)) # click

userText.grid(row=1,column=5) 
passwordText.grid(row=2,column=5)

frame1 = MyFrame(root)
frame1.grid()

root.mainloop()
