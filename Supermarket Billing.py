from pathlib import Path
from tkinter import Tk, Canvas, Entry, Label, Button, PhotoImage, Toplevel, messagebox
from tkinter import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("800x350")
window.configure(bg = "#000000")
window.title("Bill Generator")

canvas = Canvas(window,bg = "#000000",height = 350,width = 800,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_text(283.0,52.0,anchor="nw",text="Supermarket Billing",fill="#FFFFFF",font=("SF Pro Text", 24 * -1))
canvas.create_text(260.0,5.0,anchor="nw",text="General Store",fill="#FFFFFF",font=("SF Pro Text", 40 * -1))

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(199.5,173.0,image=entry_image_1)
entry_1 = Entry(bd=0,bg="#8C8C8C",fg="#FFFFFF",font=("SF Pro Text", 20 * -1),highlightthickness=0)
entry_1.place(x=116.0,y=155.0,width=167.0,height=34.0)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(199.5,237.0,image=entry_image_2)
entry_2 = Label(bd=0,bg="#595959",highlightthickness=0)
entry_2.place(x=116.0,y=219.0,width=167.0,height=34.0)

entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(483.5,237.0,image=entry_image_3)
entry_3 = Label(bd=0,bg="#595959",highlightthickness=0)
entry_3.place(x=400.0,y=219.0,width=167.0,height=34.0)

entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(483.0,170.0,image=entry_image_4)
entry_4 = Entry(bd=0,bg="#8C8C8C",fg="#FFFFFF",font=("SF Pro Text", 20 * -1),highlightthickness=0)
entry_4.place(x=399.5,y=152.0,width=167.0,height=34.0)

canvas.create_text(33.0,157.0,anchor="nw",text="Item ID:",fill="#FFFFFF",font=("SF Pro Text", 22 * -1))
canvas.create_text(302.0,157.0,anchor="nw",text="Quantity:",fill="#FFFFFF",font=("SF Pro Text", 22 * -1))

items = []
global total
total = 0

def chips_price():
    entry_2 = Label(bd=0,bg="#595959",text="Rs. 15 each",fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0).place(x=116.0,y=219.0,width=167.0,height=34.0)

def biscuit_price():
    entry_2 = Label(bd=0,bg="#595959",text="Rs. 25 each",fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0).place(x=116.0,y=219.0,width=167.0,height=34.0)

def coke_price():
    entry_2 = Label(bd=0,bg="#595959",text="Rs. 20 each",fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0).place(x=116.0,y=219.0,width=167.0,height=34.0)

def disp_total():
    entry_3 = Label(bd=0,bg="#595959",text="Rs. "+str(total), fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0).place(x=400.0,y=219.0,width=167.0,height=34.0)
   
def add():
    try:
        id = int(entry_1.get())
        quantity = int(entry_4.get())
        if id == 1:
            for x in range(0, quantity):
                items.append("Chips")
                global total
                total += 15
                chips_price()
                disp_total()
        elif id == 2:
            for x in range(0, quantity):
                items.append("Biscuits")
                total += 25
                biscuit_price()
                disp_total()
        elif id == 3:
            for x in range(0, quantity):
                items.append("Coca-Cola")
                total += 20
                coke_price()
                disp_total()
        else:
            messagebox.showerror("Error", "Please enter a valid ID from the Menu")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid ID from the Menu")

def remove():
    global total
    if len(items) > 0:
        x = items.pop()
        if x.lower() == "chips":
            total = total - 15
            disp_total()
        elif x.lower() == "biscuits":
            total = total - 25
            disp_total()
        elif x.lower() == "coca-cola":
            total = total - 20
            disp_total()
        try:
            if items[-1].lower() == "chips":
                chips_price()
            elif items[-1].lower() == "biscuits":
                biscuit_price()
            elif items[-1].lower() == "coca-cola":
                coke_price()
        except IndexError:
            pass

def clear():
    global total
    total = 0
    items.clear()
    entry_3 = Label(bd=0,bg="#595959",text="", fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0)
    entry_3.place(x=400.0,y=219.0,width=167.0,height=34.0)
    entry_2 = Label(bd=0,bg="#595959",text="",fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0)
    entry_2.place(x=116.0,y=219.0,width=167.0,height=34.0)
    entry_1.delete(0, END)
    entry_4.delete(0, END)

def generate():
    if total != 0:
        bill = Toplevel(window)
        bill.title("Bill")
        bill.resizable(0, 0)
        bill.configure(bg="#000000")
        chip_added = False
        biscuit_added = False
        coke_added = False
        Label(bill, text="TRANSACTION RECEIPT",font=("SF Pro Text", 24 * -1),bg="#000000",fg="#FFFFFF").pack()
        Label(bill, text="--------------------------------",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
        for item in items:
            if item.lower() == "chips":
                if chip_added == False:
                    Label(bill, text=str(item) + "  -  " + str(items.count(item)) + " units", font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
                    chip_added = True
            elif item.lower() == "biscuits":
                if biscuit_added == False:
                    Label(bill, text=str(item) + "  -  " + str(items.count(item)) + " units", font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
                    biscuit_added = True
            elif item.lower() == "coca-cola":
                if coke_added == False:
                    Label(bill, text=str(item) + "  -  " + str(items.count(item)) + " units", font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
                    coke_added = True
        Label(bill, text="--------------------------------",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
        Label(bill, text="Your Total is: Rs. " + str(total) + ".00",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
    else:
        pass

def menu():
    menu = Toplevel(window)
    menu.title("Menu")
    menu.resizable(0, 0)
    menu.configure(bg="#000000")
    Label(menu, text="Menu",font=("SF Pro Text", 24 * -1),bg="#000000",fg="#FFFFFF").pack()
    Label(menu, text="--------------------------------",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
    Label(menu, text="001 - Chips - Rs. 15 each",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
    Label(menu, text="002 - Biscuits - Rs. 25 each",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
    Label(menu, text="003 - Coca-Cola - Rs. 20 each",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
    Label(menu, text="--------------------------------",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=menu,relief="flat").place(x=47.0,y=60.0,width=100.0,height=30.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2,borderwidth=0,highlightthickness=0,command=add,relief="flat").place(x=648.0,y=142.0,width=116.0,height=46.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=button_image_3,borderwidth=0,highlightthickness=0,command=remove,relief="flat").place(x=648.0,y=209.0,width=116.0,height=46.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=button_image_4,borderwidth=0,highlightthickness=0,command=clear,relief="flat").place(x=200.0,y=292.0,width=116.0,height=46.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(image=button_image_5,borderwidth=0,highlightthickness=0,command=generate,relief="flat").place(x=342.0,y=290.0,width=127.0,height=46.0)

canvas.create_text(47.0,225.0,anchor="nw",text="Price:",fill="#FFFFFF",font=("SF Pro Text", 22 * -1))
canvas.create_text(330.0,225.0,anchor="nw",text="Total:",fill="#FFFFFF",font=("SF Pro Text", 22 * -1))

window.resizable(0, 0)
window.mainloop()