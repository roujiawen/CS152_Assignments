#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from query import search
import ttk
import csv
import sys
import os.path

MAX_DISTANCE = 10
F1_WIDTH = 550
F2_WIDTH = 300
W_HEIGHT = 600
SMALL_FONT = ("Arial", 10)
OPTIONS_PADDING = 10

QUESTION_ORDER = ["take_out", "food_type", "price", "english", "diet", "distance", "open_late"]

QUESTIONS = {"take_out":{
    "text": "Do you want take-out?",
    "type": "yes_no",
    "range": ["Yes", "No"]
    },

    "food_type":{
    "text": "What type of food do you want?",
    "flag": True,
    "type": "multiple",
    "range": ["Chinese", "BBQ", "Japanese", "Korean", "American", "Western", "Italian", "Asian"]
    },

    "price":{
    "text": "What price range is acceptable?",
    "flag": True,
    "type": "multiple",
    "range": ["$", "$$", "$$$"]
    },

    "english":{
    "text": "Must have English menu?",
    "type": "yes_no",
    "range": ["Yes", "No"]
    },

    "diet":{
    "text": "Do you have dietary restrictions?",
    "flag": False,
    "type": "multiple",
    "range": ["Vegan", "Vegetarian", "Gluten Free", "Halal"]
    },

    "distance":{
    "text": "Within a walking distance of (km)",
    "type": "entry",
    "range": [0, MAX_DISTANCE],
    },
    "open_late":{
    "text": "Do you want a place that opens late?",
    "type": "yes_no",
    "range": ["Yes", "No"]
    }
}

RESULT_HEADINGS = {
    "take_out": "Take Out",
    "food_type": "Type of Food",
    "price": "Price Range",
    "english": "English Menu Available",
    "diet": "Dietary-Restricion Friendly",
    "distance": "Walking Distance from UP",
    "open_late": "Open Late"
}

def read_res_data(filename="data.csv"):
    res_data = {}
    with open(filename, "r") as f:
        table = csv.reader(f)
        table.next()
        for row in table:
            res_data["rest"+str(row[0])]={
              "name":row[1],
              "take_out":[["No", "Yes"][int(row[11])]],
              "food_type":[row[4]],
              "price":[["$", "$$", "$$$"][int(row[3])-1]],
              "english":[["No", "Yes"][int(row[6])]],
              "diet":(["Vegetarian"] if row[8]=="1" else [])+
                    (["Vegan"] if row[9]=="1" else [])+
                    (["Halal"] if row[7]=="1" else [])+
                    (["Gluten Free"] if row[10]=="1" else []),
              "distance":float(row[5]),
              "address": row[2],
              "open_late":[["No", "Yes"][int(row[12])]]
            }
    return res_data


#Reference: https://stackoverflow.com/questions/38951047/anyone-successfully-bundled-data-files-into-a-single-file-with-pyinstaller
if hasattr(sys, "_MEIPASS"):
    datadir = os.path.join(sys._MEIPASS, "data.csv")
else:
    datadir = "data.csv"

RESTAURANTS = read_res_data(datadir)

class WidgetMultiple(Frame):
    def __init__(self, parent, info):
        Frame.__init__(self, parent)
        l = Label(self, text=info["text"])
        l.grid(sticky="w")
        self.choose_all_flag = info["flag"]

        self.items = []
        for each in info["range"]:
            v = IntVar()
            c = Checkbutton(self, text=each, variable=v, font=SMALL_FONT)
            c.formatted = each.lower() if each[0] != "$" else "_"+str(len(each))
            c.val = v
            c.grid(sticky="w", padx=OPTIONS_PADDING)
            self.items.append(c)

    def clear(self):
        for each in self.items:
            each.deselect()

    def get(self):
        selected = [each.formatted for each in self.items if each.val.get() == 1]
        if len(selected) == 0:
            if self.choose_all_flag:
                return [each.formatted for each in self.items]
        return selected

class WidgetYesNo(Frame):
    def __init__(self, parent, info):
        Frame.__init__(self, parent)
        l = Label(self, text=info["text"])
        l.grid(sticky="w")

        v = IntVar()
        c = Checkbutton(self, text="Yes", variable=v, font=SMALL_FONT)
        c.val = v
        c.grid(sticky="w", padx=OPTIONS_PADDING)
        self.checkbutton = c

    def clear(self):
        self.checkbutton.deselect()

    def get(self):
        return ["yes"] if self.checkbutton.val.get() == 1 else ["no"]

class WidgetEntry(Frame):
    def __init__(self, parent, info):
        Frame.__init__(self, parent)
        self.maxlen = 5
        self.upper = info["range"][1]
        self.lower = info["range"][0]
        l = Label(self, text=info["text"])
        l.grid(sticky="w")

        vcmd = (self.register(self.is_okay),'%P')
        e = Entry(self, font=SMALL_FONT, width=self.maxlen, validate="all", validatecommand=vcmd)
        e.grid(sticky="w", padx=OPTIONS_PADDING)
        self.entry = e

    def is_okay(self, value):
        if len(value)>self.maxlen:
            return False
        if value is "": return True
        try:
            value = float(value)
            if (self.lower <= value) and (value <= self.upper):
                return True
        except:
            pass
        return False

    def clear(self):
        self.entry.delete(0, END)

    def get(self):
        value = self.entry.get()
        try:
            return float(value)
        except:
            return MAX_DISTANCE

class WidgetResult(Frame):
    def __init__(self, parent, info):
        Frame.__init__(self, parent)
        l = Label(self, text=info["name"], font=("Arial", 15, "bold"))
        l.grid(sticky="w")

        for each in QUESTION_ORDER:
            temp = Frame(self)
            temp.grid(sticky="w")
            cate = Label(temp, text=RESULT_HEADINGS[each]+" : ")
            cate.grid(row=0, column=0, sticky="w")
            if isinstance(info[each], list):
                body = Label(temp, text=", ".join(info[each]))
            else:
                body = Label(temp, text="{} km".format(info[each]))
            body.grid(row=0, column=1, sticky="w")



widget_classes = {
"multiple" : WidgetMultiple,
"yes_no" : WidgetYesNo,
"entry" : WidgetEntry
}

root = Tk()
root.title("Restaurant Recommendation Engine")

############## Result Frame ##############

# Canvas and Scrollbar
result_canvas = Canvas(root, height=W_HEIGHT, width=F1_WIDTH, highlightthickness=0)
result_canvas.grid(row=0, column=0)
result_scrollbar = Scrollbar(root, command=result_canvas.yview)
result_scrollbar.grid(row=0, column=1, sticky="ns")
result_canvas.configure(yscrollcommand = result_scrollbar.set)

# Result Frame
result_frame = Frame(result_canvas, pady=15)
result_canvas.create_window((0,0), window=result_frame)
result_frame.columnconfigure(0, minsize=F1_WIDTH)

# Default Widgets
temp = Frame(result_frame)
temp.grid()
temp.rowconfigure(0, minsize=W_HEIGHT)
default_label = Label(temp, text="Please Submit a Form",
    font=("Arial", 30, "bold"), fg="grey")
default_label.grid()
result_widgets = [temp, default_label]

# Question Widgets
def display_results(data):
    for each in result_widgets:
        each.destroy()
    del result_widgets[:]
    for info in data:
        w = WidgetResult(result_frame, info)
        w.grid(sticky="w", padx=20, pady=5)
        result_widgets.append(w)

# Bindings
def result_on_vertical(event):
    result_canvas.yview_scroll(-1 * event.delta, 'units')

def result_bound_to_mousewheel(event):
    result_canvas.unbind_all("<MouseWheel>")
    result_canvas.bind_all('<MouseWheel>', result_on_vertical)

result_frame.bind('<Enter>', result_bound_to_mousewheel)

############## Question Frame ##############

# Canvas and Scrollbar
canvas = Canvas(root, height=W_HEIGHT, highlightthickness=0)
canvas.grid(row=0, column=2)
scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.grid(row=0, column=3, sticky="ns")
canvas.configure(yscrollcommand = scrollbar.set)

# Question Frame
question_frame = Frame(canvas, pady=15)
canvas.create_window((0,0), window=question_frame)

# Question Widgets
question_widgets = []
for question in QUESTION_ORDER:
    info = QUESTIONS[question]
    w = widget_classes[info["type"]](question_frame, info)
    w.grid(sticky="w", padx=15, pady=2)
    question_widgets.append(w)

# Buttons
def clear_form():
    for each in question_widgets:
        each.clear()

def submit_form():
    user_input = {}
    for question, widget in zip(QUESTION_ORDER, question_widgets):
        user_input[question] = widget.get()
    print user_input
    results = search(user_input)
    print results
    display_results([RESTAURANTS[i] for i in results])

temp = Frame(question_frame)
temp.grid()
clear_button = Button(temp, text="Clear", command=clear_form)
clear_button.grid(row=0, column=0)
submit_button = Button(temp, text="Submit", command=submit_form)
submit_button.grid(row=0, column=1)

# Bindings
def on_vertical(event):
    canvas.yview_scroll(-1 * event.delta, 'units')
def bound_to_mousewheel(event):
    result_canvas.unbind_all("<MouseWheel>")
    canvas.bind_all('<MouseWheel>', on_vertical)
question_frame.bind('<Enter>', bound_to_mousewheel)

# Root binding
def on_configure(event=None):
    result_canvas.configure(scrollregion=result_canvas.bbox('all'))
    canvas.configure(scrollregion=canvas.bbox('all'))
root.bind('<Configure>', on_configure)

mainloop()
