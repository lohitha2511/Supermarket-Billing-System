from pathlib import Path
from tkinter import Tk, Canvas, Entry, Label, Button, PhotoImage, Toplevel, messagebox
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

BG_COLOR = "#000000"
ENTRY_BG_COLOR = "#8C8C8C"
LABEL_BG_COLOR = "#595959"
TEXT_COLOR = "#FFFFFF"

FONT_LARGE = ("SF Pro Text", 40 * -1)
FONT_MEDIUM = ("SF Pro Text", 28 * -1)
FONT_NORMAL = ("SF Pro Text", 24 * -1)
FONT_SMALL = ("SF Pro Text", 22 * -1)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relativeToAssets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Product:
    def __init__(self, name, id, price, stock, added=False):
        self.name = name
        self.id = id
        self.price = price
        self.stock = stock
        self.added = added

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("DB_URI"))
        self.db = self.client["store_db"]
        self.transactions_col = self.db["transactions"]
        self.inventory_col = self.db["inventory"]

    def load_inventory(self):
        inventory_data = list(self.inventory_col.find())
        return [Product(doc["name"], doc["id"], doc["price"], doc.get("stock", 0)) for doc in inventory_data]

    def decrement_stock(self, item_id, qty=1):
        self.inventory_col.update_one({"id": item_id}, {"$inc": {"stock": -qty}})

    def insert_transaction(self, doc):
        self.transactions_col.insert_one(doc)

class Bill:
    def __init__(self, database: Database, inventory_list):
        self.db = database
        self.inventory = inventory_list
        self.billItems = [] 
        self.total = 0

    def add_by_id(self, item_id, quantity):
        product = next((p for p in self.inventory if int(p.id) == int(item_id)), None)
        if product is None:
            return False, "invalid_id"

        try:
            qty = int(quantity)
            if qty <= 0:
                return False, "invalid_input"
        except Exception:
            return False, "invalid_input"

        if product.stock < qty:
            return False, "out_of_stock"

        self.billItems.extend([product.name] * qty)
        self.total += int(product.price) * qty

        return True, product

    def remove_last(self):
        if not self.billItems:
            return False, None
        removed_name = self.billItems.pop()
        product = next((p for p in self.inventory if p.name == removed_name), None)
        if product:
            self.total -= int(product.price)
        return True, product

    def clear(self):
        self.billItems.clear()
        self.total = 0
        for p in self.inventory:
            p.added = False

    def make_transaction_doc(self):
        doc = {"items": [], "total": self.total, "timestamp": datetime.now()}
        for product in self.inventory:
            count = self.billItems.count(product.name)
            self.db.decrement_stock(product.id, count)
            product.stock -= count
            if count > 0:
                doc["items"].append({
                    "name": product.name,
                    "quantity": count,
                    "unit_price": product.price,
                    "subtotal": count * product.price
                })
        return doc

db = Database()
inventoryList = db.load_inventory()
noOfItem = len(inventoryList)

bill = Bill(db, inventoryList)

window = Tk()
window.geometry("800x350")
window.configure(bg=BG_COLOR)
window.title("Bill Generator")

canvas = Canvas(window, bg=BG_COLOR, height=350, width=800, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_text(283.0, 52.0, anchor="nw", text="BILL GENERATOR", fill=TEXT_COLOR, font=FONT_NORMAL)
canvas.create_text(260.0, 5.0, anchor="nw", text="General Store", fill=TEXT_COLOR, font=FONT_LARGE)

entryImage1 = PhotoImage(file=relativeToAssets("entry_1.png"))
entry_bg_1 = canvas.create_image(199.5, 173.0, image=entryImage1)
entryItemId = Entry(bd=0, bg=ENTRY_BG_COLOR, fg=TEXT_COLOR, font=FONT_SMALL, highlightthickness=0)
entryItemId.place(x=116.0, y=155.0, width=167.0, height=34.0)

entryImage2 = PhotoImage(file=relativeToAssets("entry_2.png"))
entry_bg_2 = canvas.create_image(199.5, 237.0, image=entryImage2)
labelPrice = Label(bd=0, bg=LABEL_BG_COLOR, fg=TEXT_COLOR, font=FONT_SMALL, highlightthickness=0)
labelPrice.place(x=116.0, y=219.0, width=167.0, height=34.0)

entryImage3 = PhotoImage(file=relativeToAssets("entry_3.png"))
entry_bg_3 = canvas.create_image(483.5, 237.0, image=entryImage3)
labelTotal = Label(bd=0, bg=LABEL_BG_COLOR, fg=TEXT_COLOR, font=FONT_SMALL, highlightthickness=0)
labelTotal.place(x=400.0, y=219.0, width=167.0, height=34.0)

entryImage4 = PhotoImage(file=relativeToAssets("entry_4.png"))
entry_bg_4 = canvas.create_image(483.0, 170.0, image=entryImage4)
entryQuantity = Entry(bd=0, bg=ENTRY_BG_COLOR, fg=TEXT_COLOR, font=FONT_SMALL, highlightthickness=0)
entryQuantity.place(x=399.5, y=152.0, width=167.0, height=34.0)

canvas.create_text(33.0, 157.0, anchor="nw", text="Item ID:", fill=TEXT_COLOR, font=FONT_SMALL)
canvas.create_text(302.0, 157.0, anchor="nw", text="Quantity:", fill=TEXT_COLOR, font=FONT_SMALL)

def clear():
    bill.clear()
    labelTotal.config(text="")
    labelPrice.config(text="")
    entryItemId.delete(0, "end")
    entryQuantity.delete(0, "end")

def disp_total():
    labelTotal.config(text="Rs. " + str(bill.total))

def id_err():
    entryItemId.delete(0, "end")
    messagebox.showerror("Error", "Please enter a valid ID from the Menu")


def inv_inp():
    entryItemId.delete(0, "end")
    entryQuantity.delete(0, "end")
    messagebox.showerror("Error", "Invalid Input!")


def add():
    try:
        entered_id = int(entryItemId.get())
        quantity = int(entryQuantity.get())
    except ValueError:
        inv_inp()
        return

    success, payload = bill.add_by_id(entered_id, quantity)
    if not success:
        if payload == "invalid_id":
            id_err()
        elif payload == "invalid_input":
            inv_inp()
        elif payload == "out_of_stock":
            messagebox.showerror("Error", f"Only {next((p for p in inventoryList if int(p.id) == entered_id), None).stock} units available" if next((p for p in inventoryList if int(p.id) == entered_id), None) else "Out of stock")
        return

    product = payload
    disp_total()
    labelPrice.config(text="Rs. " + str(product.price) + " each")


def remove():
    if len(bill.billItems) > 0:
        success, product = bill.remove_last()
        if success:
            disp_total()
        try:
            last_name = bill.billItems[-1]
            last_product = next((p for p in inventoryList if p.name == last_name), None)
            if last_product:
                labelPrice.config(text="Rs. " + str(last_product.price) + " each")
        except IndexError:
            pass


def generate():
    if bill.total != 0:
        billWindow = Toplevel(window)
        billWindow.title("Bill")
        billWindow.resizable(0, 0)
        billWindow.configure(bg=BG_COLOR)
        Label(billWindow, text="TRANSACTION RECEIPT", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR).pack()
        Label(billWindow, text="--------------------------------", font=FONT_SMALL, bg=BG_COLOR, fg=TEXT_COLOR).pack()

        for item_name in bill.billItems:
            for product in inventoryList:
                if str(item_name) == product.name and not product.added:
                    Label(
                        billWindow,
                        text=str(product.name) + "  -   " + str(bill.billItems.count(product.name)) + " units",
                        font=FONT_SMALL, bg=BG_COLOR, fg=TEXT_COLOR
                    ).pack()
                    product.added = True

        Label(billWindow, text="--------------------------------", font=FONT_SMALL, bg=BG_COLOR, fg=TEXT_COLOR).pack()
        Label(billWindow, text="Your Total is: Rs. " + str(bill.total) + ".00", font=FONT_SMALL, bg=BG_COLOR, fg=TEXT_COLOR).pack()

        transaction_doc = bill.make_transaction_doc()
        db.insert_transaction(transaction_doc)

        clear()
    else:
        pass

def menu():
    menuWindow = Toplevel(window)
    menuWindow.title("Inventory")
    menuWindow.resizable(0, 0)
    menuWindow.configure(bg=BG_COLOR)
    Label(menuWindow, text="ITEM LIST", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_COLOR).pack()
    Label(menuWindow, text="-----------------------------------------------", font=FONT_SMALL, bg=BG_COLOR, fg=TEXT_COLOR).pack()
    for product in inventoryList:
        Label(menuWindow, text=str(product.id) + "   -   " + str(product.name) + "   -   Rs. " + str(product.price) + " each", font=FONT_SMALL, bg=BG_COLOR, fg=TEXT_COLOR).pack()
    Label(menuWindow, text="-----------------------------------------------", font=FONT_SMALL, bg=BG_COLOR, fg=TEXT_COLOR).pack()

buttonImage1 = PhotoImage(file=relativeToAssets("button_1.png"))
button_1 = Button(image=buttonImage1, borderwidth=0, highlightthickness=0, command=menu, relief="flat")
button_1.place(x=47.0, y=60.0, width=100.0, height=30.0)

buttonImage2 = PhotoImage(file=relativeToAssets("button_2.png"))
button_2 = Button(image=buttonImage2, borderwidth=0, highlightthickness=0, command=add, relief="flat")
button_2.place(x=648.0, y=142.0, width=116.0, height=46.0)

buttonImage3 = PhotoImage(file=relativeToAssets("button_3.png"))
button_3 = Button(image=buttonImage3, borderwidth=0, highlightthickness=0, command=remove, relief="flat")
button_3.place(x=648.0, y=209.0, width=116.0, height=46.0)

buttonImage4 = PhotoImage(file=relativeToAssets("button_4.png"))
button_4 = Button(image=buttonImage4, borderwidth=0, highlightthickness=0, command=clear, relief="flat")
button_4.place(x=200.0, y=292.0, width=116.0, height=46.0)

buttonImage5 = PhotoImage(file=relativeToAssets("button_5.png"))
button_5 = Button(image=buttonImage5, borderwidth=0, highlightthickness=0, command=generate, relief="flat")
button_5.place(x=342.0, y=290.0, width=127.0, height=46.0)

canvas.create_text(47.0, 225.0, anchor="nw", text="Price:", fill=TEXT_COLOR, font=FONT_SMALL)
canvas.create_text(330.0, 225.0, anchor="nw", text="Total:", fill=TEXT_COLOR, font=FONT_SMALL)

window.resizable(0, 0)
window.mainloop()
