# coding: utf-8
'''
cd /d z:
cd Dropbox/Codes/password_generator
py password_generator.py
'''

# Terms taken from Pythonista

import tkinter
import random
import re

view = tkinter.Frame()

subview_up_left = tkinter.Frame(view)
subview_up_right = tkinter.Frame(view)
subview_left = tkinter.Frame(view)
subview_right = tkinter.Frame(view)
subview_up_left.grid(row=0, column=0)
subview_up_right.grid(row=0, column=1)
subview_left.grid(row=1, column=0, padx=5, pady=20, sticky='n')
subview_right.grid(row=1, column=1, pady=5)

tuple_cc_sym = ((33, 48), (58, 65), (91, 97), (123, 127))
tuple_cc_cap = ((65, 91),)
tuple_cc_low = ((97, 123),)
tuple_cc_num = ((48, 58),)

pattern_space = re.compile(r'\s')


def mk_list_of_characters(tuple_cc):
    ls = []
    for tpl in tuple_cc:
        ls += [chr(c) for c in range(tpl[0], tpl[1])]
    return ls


ls_init_sym = mk_list_of_characters(tuple_cc_sym)
ls_init_cap = mk_list_of_characters(tuple_cc_cap)
ls_init_low = mk_list_of_characters(tuple_cc_low)
ls_init_num = mk_list_of_characters(tuple_cc_num)

str_sym = ''.join(ls_init_sym)
str_cap = ''.join(ls_init_cap)
str_low = ''.join(ls_init_low)
str_num = ''.join(ls_init_num)

var_str_sym = tkinter.StringVar(subview_up_left)
var_str_cap = tkinter.StringVar(subview_up_left)
var_str_low = tkinter.StringVar(subview_up_left)
var_str_num = tkinter.StringVar(subview_up_left)

var_str_sym.set(str_sym)
var_str_cap.set(str_cap)
var_str_low.set(str_low)
var_str_num.set(str_num)

ent_sym = tkinter.Entry(subview_up_right, width=40, textvariable=var_str_sym)
ent_cap = tkinter.Entry(subview_up_right, width=40, textvariable=var_str_cap)
ent_low = tkinter.Entry(subview_up_right, width=40, textvariable=var_str_low)
ent_num = tkinter.Entry(subview_up_right, width=40, textvariable=var_str_num)
entries = (ent_sym, ent_cap, ent_low, ent_num)

for ent in entries:
    ent.pack(pady=3)


var_bool_sym = tkinter.BooleanVar()
var_bool_cap = tkinter.BooleanVar()
var_bool_low = tkinter.BooleanVar()
var_bool_num = tkinter.BooleanVar()
variables_bool = (var_bool_sym, var_bool_cap, var_bool_low, var_bool_num)

lname = ('sym', 'cap', 'low', 'num')
sw_sym = tkinter.Checkbutton(subview_up_left, text=lname[0])
sw_cap = tkinter.Checkbutton(subview_up_left, text=lname[1])
sw_low = tkinter.Checkbutton(subview_up_left, text=lname[2])
sw_num = tkinter.Checkbutton(subview_up_left, text=lname[3])
switches = (sw_sym, sw_cap, sw_low, sw_num,)

for sw in switches:
    sw['variable'] = variables_bool[switches.index(sw)]
    sw.select()
    sw.pack()

var_length = tkinter.IntVar()
var_length.set(12)
var_choices = tkinter.IntVar()
var_choices.set(10)

l_length = tkinter.Label(subview_left, text='length')
l_length.pack()
sc_length = tkinter.Scale(subview_left, variable=var_length, from_=20, to=1, length=60, sliderlength=10, width=20)
sc_length.pack()
l_choices = tkinter.Label(subview_left, text='number')
l_choices.pack()
sc_choices = tkinter.Scale(subview_left, variable=var_choices, from_=20, to=1, length=60, sliderlength=10, width=20)
sc_choices.pack()


def get_available_char():
    ls_sym = list(pattern_space.sub('', var_str_sym.get()))
    ls_cap = list(pattern_space.sub('', var_str_cap.get()))
    ls_low = list(pattern_space.sub('', var_str_low.get()))
    ls_num = list(pattern_space.sub('', var_str_num.get()))
    return {'sym': ls_sym, 'cap': ls_cap, 'low': ls_low, 'num': ls_num}


def set_string_list():
    length = sc_length.get()
    dict_available_char = get_available_char()
    string_list = []
    if var_bool_sym.get():
        string_list += dict_available_char['sym']

    if var_bool_cap.get():
        string_list += dict_available_char['cap']

    if var_bool_low.get():
        string_list += dict_available_char['low']

    if var_bool_num.get():
        string_list += dict_available_char['num']

    if length > len(string_list):
        string_list = string_list * (length // len(string_list) + 1)

    return string_list


def set_pw(string_list):
    choices = sc_choices.get()
    length = sc_length.get()
    pw_list = []
    for k in range(choices):
        pw_list.append(''.join(random.sample(string_list, length)))
    return pw_list


def change_all_state(state):
    for child in subview_right.winfo_children():
        child['state'] = state


def button_tapped(self):
    prefix = 'You chose '
    suffix = ' !'
    if self.widget['state'] == 'disabled':
        return
    elif not self.widget['text'].startswith(prefix):
        self.widget['text'] = prefix + self.widget['text'] + suffix
        self.widget['borderwidth'] = 2
        change_all_state('disabled')
        self.widget['state'] = 'normal'
    else:
        pass

    view.clipboard_clear()
    view.clipboard_append(self.widget['text'][len(prefix):-len(suffix)])


def set_buttons():
    for child in subview_right.winfo_children():
        child.destroy()
    string_list = set_string_list()
    pw_list = set_pw(string_list)
    choices = sc_choices.get()
    buttons = [tkinter.Button(subview_right, text='') for k in range(choices)]
    for k in range(choices):
        buttons[k]['text'] = pw_list[k]
        buttons[k]['borderwidth'] = 1
        buttons[k].bind('<ButtonRelease-1>', button_tapped)
        buttons[k].pack()
    change_all_state('normal')


for sw in switches:
    sw['command'] = set_buttons

set_buttons()


def refresh_tapped(self):
    random.seed()
    set_buttons()


button_refresh = tkinter.Button(subview_left, text='refresh')
button_refresh['state'] = 'normal'
button_refresh.bind('<ButtonRelease-1>', refresh_tapped)
button_refresh.pack(pady=20)

sc_length['command'] = refresh_tapped
sc_choices['command'] = refresh_tapped

top = view.winfo_toplevel()
top.resizable(False, False)
view.pack()
view.mainloop()
