from pathlib import Path
from tkinter import Tk, Canvas, Entry, Label, Button, PhotoImage, Toplevel, messagebox
from tkinter import *
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

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
canvas.create_text(283.0,52.0,anchor="nw",text="BILL GENERATOR",fill="#FFFFFF",font=("SF Pro Text", 24 * -1))
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

bill_Item = []
global total
total = 0

class Item:
    def __init__(self, name, id, price, stock, added=False):
        self.name = name
        self.id = id
        self.price = price
        self.stock = stock
        self.added = added

client = MongoClient(os.getenv("DB_URI"))
db = client["store_db"]

transactions_col = db["transactions"]
inventory_col = db["inventory"]

inventory_data = list(inventory_col.find())

inventory = [Item(doc["name"], doc["id"], doc["price"], doc["stock"]) for doc in inventory_data]
no_of_Item = len(inventory)

def clear():
    global total
    total = 0
    bill_Item.clear()
    entry_3 = Label(bd=0,bg="#595959",text="", fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0)
    entry_3.place(x=400.0,y=219.0,width=167.0,height=34.0)
    entry_2 = Label(bd=0,bg="#595959",text="",fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0)
    entry_2.place(x=116.0,y=219.0,width=167.0,height=34.0)
    entry_1.delete(0, END)
    entry_4.delete(0, END)

def disp_total():
    entry_3 = Label(bd=0,bg="#595959",text="Rs. "+str(total), fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0).place(x=400.0,y=219.0,width=167.0,height=34.0)

def id_err():
    entry_1.delete(0, END)
    messagebox.showerror("Error", "Please enter a valid ID from the Menu")

def inv_inp():
    entry_1.delete(0, END)
    entry_4.delete(0, END)
    messagebox.showerror("Error", "Invalid Input!")
    
def add():
    global total
    try:
        x = int(entry_1.get())
        quantity = int(entry_4.get())
        if x <= no_of_Item:
            for thing in inventory:
                if int(thing.id) == x:
                    for x in range(0, quantity):
                        bill_Item.append(str(thing.name))
                        inventory_col.update_one({"id": thing.id}, {"$inc": {"stock": -1}})
                        thing.stock -= 1
                        total = total + int(thing.price)
                        disp_total()
                    entry_2 = Label(bd=0,bg="#595959",text="Rs. " + str(thing.price) + " each",fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0).place(x=116.0,y=219.0,width=167.0,height=34.0)
        else:
            id_err()
    except ValueError:
        inv_inp()   

def remove():
    global total
    if len(bill_Item) > 0:
        x = bill_Item.pop()
        for thing in inventory:
            if str(x) == str(thing.name):
                total = total - int(thing.price)
                disp_total()
        try:
            for bong in inventory:
                if str(bill_Item[-1]) == bong.name:
                    entry_2 = Label(bd=0,bg="#595959",text="Rs. " + str(bong.price) + " each",fg="#FFFFFF",font=("SF Pro Text", 22 * -1),highlightthickness=0).place(x=116.0,y=219.0,width=167.0,height=34.0)
        except IndexError:
            pass

def generate():
    if total != 0:
        bill = Toplevel(window)
        bill.title("Bill")
        bill.resizable(0, 0)
        bill.configure(bg="#000000")
        Label(bill, text="TRANSACTION RECEIPT",font=("SF Pro Text", 24 * -1),bg="#000000",fg="#FFFFFF").pack()
        Label(bill, text="--------------------------------",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
        for item in bill_Item:
            for thing in inventory:
                if str(item) == thing.name:
                    if thing.added == False:
                        Label(bill, text=str(thing.name)+ "  -   " + str(bill_Item.count(thing.name)) + " units",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
                        thing.added = True
        Label(bill, text="--------------------------------",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
        Label(bill, text="Your Total is: Rs. " + str(total) + ".00",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
        transaction_doc = {
            "items": [],
            "total": total,
            "timestamp": datetime.now()
        }
        for thing in inventory:
            count = bill_Item.count(thing.name)
            if count > 0:
                transaction_doc["items"].append({
                    "name": thing.name,
                    "quantity": count,
                    "unit_price": thing.price,
                    "subtotal": count * thing.price
                })
        transactions_col.insert_one(transaction_doc)
        clear()
    else:
        pass

def menu():
    menu = Toplevel(window)
    menu.title("Inventory")
    menu.resizable(0, 0)
    menu.configure(bg="#000000")
    Label(menu, text="ITEM LIST",font=("SF Pro Text", 28 * -1),bg="#000000",fg="#FFFFFF").pack()
    Label(menu, text="-----------------------------------------------",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
    for thing in inventory:
        Label(menu, text=str(thing.id) + "   -   " + str(thing.name) + "   -   Rs. " + str(thing.price) + " each",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()
    Label(menu, text="-----------------------------------------------",font=("SF Pro Text", 22 * -1),bg="#000000",fg="#FFFFFF").pack()

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