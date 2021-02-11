#!/usr/local/anaconda3/bin/python

import numpy as np
import sys, getopt, time, re
from collections import deque
from tkinter import *

try:
    program = None
    speed = 1.0
    visual = False

    opts, args = getopt.getopt(sys.argv[1:], 'hi:s:v', ['help', 'program=', 'speed=', 'visual'])
except:
    print('[PROGRAM NOT FOUND!]')
    exit(1)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print('Usage: python tmac.py -i <program> (-s <speed> --visual)')
        exit(0)
    elif opt in ('-i', '--program'):
        program = arg
    elif opt in ('-s', '--speed'):
        speed = float(arg)
    elif opt in ('-v', '--visual'):
        visual = True

if program is None:
    print('[PROGRAM NOT FOUND!]')
    exit(1)

with open(program, 'r') as f:
    states = f.readline()[:-1]
    symbols = f.readline()[:-1]
    blank = f.readline()[:-1]
    input_symbols = f.readline()[:-1]
    init_state = f.readline()[:-1]
    final_state = f.readline()[:-1]
    transitions = list()
    
    
    for i, line in enumerate(f):
        line = line[:-1]
        if len(line) < 1:
            continue
        # print(i, line)
        X, Y = line.split('->')
        
        X_tokens = X.split(',')
        Y_tokens = Y.split(',')
        
        for t in range(2):
            X_tokens[t] = X_tokens[t].replace(' ' , '')
        for t in range(3):
            Y_tokens[t] = Y_tokens[t].replace(' ', '')
        # print(X_tokens, Y_tokens)
        
        transition = [X_tokens, Y_tokens]
        transitions += [transition]
        
f.close()

# - - - - - - - - - - - - - - - - - - -

regex = '{(.*?)}'
states = re.findall(regex, states)[0].split(',')
symbols = re.findall(regex, symbols)[0].split(',')
blank = re.findall(regex, blank)[0].split(',')
input_symbols = re.findall(regex, input_symbols)[0].split(',')
init_state = re.findall(regex, init_state)[0].split(',')
final_state = re.findall(regex, final_state)[0].split(',')

input_symbols_copy = input_symbols.copy()
init_state_copy = init_state.copy()

def compute(one_step_run=False, tape=input_symbols_copy, machine_state=init_state_copy[0], index=0):
    if not one_step_run:
        print(f'States: {states}\nSymbols: {symbols}\nBlank: {blank}\nInput symbols: \
{input_symbols}\nInitial state: {init_state}\nFinal state: {final_state}')
        print('\nTransitions:')
        for transition in transitions:
            print(transition[0], '->', transition[1])
        print()
    if index < -1 or index > len(tape):
        print('Error')
        exit(1)
    
    direction = 0
    recent_transition = None
    while machine_state != 'HALT':
        if index == -1:
            index = 0
            tape.insert(0, blank[0])
        elif index == len(tape):
            tape.append(blank[0])
        print(machine_state, tape[index])
        is_found = False
        for transition in transitions:
            if machine_state == transition[0][0] and tape[index] == transition[0][1]:
                print('applying transition:', transition)
                recent_transition = transition
                is_found = True
                new_symbol = transition[1][0]
                go_to = transition[1][1]
                new_state = transition[1][2]

                tape[index] = new_symbol
                machine_state = new_state
                direction = go_to
            
                if go_to == 'L':
                    index -= 1
                else:
                    index += 1
                print(tape)
                break
        if not is_found:
            print('[TRANSITION NOT FOUND!] Halting...')
            machine_state = 'HALT'
            break
        if one_step_run:
            break
    
    return tape, machine_state, index, recent_transition, direction
# - - - - - - - - - - - - - - - - - - -
if not visual:
    compute()
    exit(0)
print(f'Animation speed: {speed}')
tape = input_symbols.copy()
state = init_state.copy()[0]
index, tape_offset = 0, 1
is_paused = True

root = Tk()
root.resizable(False, False)
root.title('Turing Machine')

canvas = Canvas(root, width=30*16-8, height=80)
control_frame = Frame(root)

canvas.pack()
control_frame.pack()

transition_label = Label(control_frame, text='Transition', width=50)
transition_label.grid(row=1, column=0, columnspan=3)
restart_button = Button(control_frame, text='Restart')
restart_button['state'] = DISABLED

cells = list()          # tkinter rectangle objects
cell_symbols = list()   # tkinter text objects
_radius = 30
machine_state_symbol = canvas.create_text(1.5*_radius, 60, text='', font=('Purisa', 10))
machine = canvas.create_oval(_radius, 45, 2*_radius, 45+_radius)

for i in range(16):
    cell = canvas.create_rectangle(0, 10, 30+_radius*i, 10+_radius)
    cell_symbol = canvas.create_text(_radius/2+_radius*i, 25, text=blank)
    cells.append(cell)
    cell_symbols.append(cell_symbol)

for i in range(1, len(cell_symbols)-1):
    if i - 1 >= len(tape):
        canvas.itemconfig(cell_symbols[i], text=blank[0])
    else:
        canvas.itemconfig(cell_symbols[i], text=tape[i-1])
canvas.itemconfig(machine_state_symbol, text=state)

def move_machine(direction, machine_state):
    sign = -1
    if direction == 'R':
        sign = 1
    canvas.move(machine, sign*_radius, 0)
    canvas.move(machine_state_symbol, sign*_radius, 0)
    canvas.itemconfigure(machine_state_symbol, text=machine_state)
    
def move_tape(direction, machine_state):
    global tape_offset

    sign = -1
    tape_offset += 1
    if direction == 'R':
        sign = 1
        tape_offset -= 2

    for i in range(0, tape_offset):
        canvas.itemconfig(cell_symbols[i], text=blank[0])
    for i in range(tape_offset, 16):
        if i < 0:
            continue
        
        if i - tape_offset >= len(tape):
            canvas.itemconfig(cell_symbols[i], text=blank[0])
        else:
            canvas.itemconfig(cell_symbols[i], text=tape[i-tape_offset])
    
    if machine_state is not None:
        canvas.itemconfigure(machine_state_symbol, text=machine_state)

def run(tape, state, index, transition, dir_):
    global speed
    global restart_button

    if is_paused:
        root.after(100, lambda: run(tape, state, index, transition, dir_))
        return

    restart_button['state'] = DISABLED
    coord = canvas.coords(machine)
    is_halted = False
    
    if state == 'HALT':
        print(' ========= HALT ==========')
        restart_button['state'] = NORMAL
        canvas.itemconfig(machine_state_symbol, text='HALT')
        is_halted = True

        canvas.itemconfig(cell_symbols[0], text=blank[0])
        for i in range(1, len(cell_symbols)-1):
            if i - 1 >= len(tape):
                canvas.itemconfig(cell_symbols[i], text=blank[0])
            else:
                canvas.itemconfig(cell_symbols[i], text=tape[i-1])
    elif coord[0] >= 14*_radius and dir_ == 'R':
        # print('shifting the tape left...')
        move_tape(direction='R', machine_state=state)
    elif coord[2] <= 2*_radius and dir_ == 'L':
        # print('shifting the tape right...')
        move_tape(direction='L', machine_state=state)
    else:
        move_machine(direction=dir_, machine_state=state)
        # print(f'moving the machine {dir_}')
    
    if not is_halted:
        transition_label.config(text=f'Transition: {transition[0][0]}, {transition[0][1]} -> {transition[1][0]}, {transition[1][1]}, {transition[1][2]}')

        canvas.itemconfig(cell_symbols[0], text=blank[0])
        for i in range(1, len(cell_symbols)-1):
            if i - 1 >= len(tape):
                canvas.itemconfig(cell_symbols[i], text=blank[0])
            else:
                canvas.itemconfig(cell_symbols[i], text=tape[i-1])

        time_ = 2000-int(500*np.abs(speed))
        if time_ < 0:
            time_ = 10
        
        tape, state, index, transition, dir_ = compute(one_step_run=True, tape=tape, machine_state=state, index=index)
        root.after(time_, lambda: run(tape, state, index, transition, dir_))

def restart():
    global tape, state, index
    global restart_button

    tape = input_symbols.copy()
    state = init_state.copy()[0]
    index, tape_offset = 0, 1
    is_paused = True

    print('\tRestarted!')
    # print(tape)
    # print(state)
    restart_button['state'] = DISABLED

    canvas.move(machine, -canvas.coords(machine)[0]+_radius, 0)
    canvas.move(machine_state_symbol, -canvas.coords(machine_state_symbol)[0]+1.5*_radius, 0)
    canvas.itemconfig(machine_state_symbol, text=state)

    canvas.itemconfig(cell_symbols[0], text=blank[0])
    for i in range(1, 16):
        if i - 1 >= len(tape):
            canvas.itemconfig(cell_symbols[i], text=blank[0])
        else:
            canvas.itemconfig(cell_symbols[i], text=tape[i-1])
    
    tape, state, index, transition, dir_ = compute(one_step_run=True, tape=tape, machine_state=state, index=index)
    transition_label.config(text=f'Transition: {transition[0][0]}, {transition[0][1]} -> {transition[1][0]}, {transition[1][1]}, {transition[1][2]}')

    time_ = 2000-int(500*np.abs(speed))
    if time_ < 0:
        time_ = 10
    root.after(time_, lambda: run(tape, state, index, transition, dir_))

def change_speed(delta):
    global speed
    speed += delta
    print('Animation speed:', speed)

def resume_pause():
    global control_button
    global is_paused

    if is_paused:
        control_button.config(text='Pause')
    else:
        control_button.config(text='Resume')

    is_paused = not is_paused


restart_button.config(command=restart)
restart_button.grid(row=2, column=0)
Button(control_frame, text='Speed up', command=lambda: change_speed(0.1)).grid(row=2, column=1)
Button(control_frame, text='Slow down', command=lambda: change_speed(-0.1)).grid(row=2, column=2)
Button(control_frame, text=u'\u2190', command=lambda: move_tape(direction='L', machine_state=None)).grid(row=0, column=0)
Button(control_frame, text=u'\u2192', command=lambda: move_tape(direction='R', machine_state=None)).grid(row=0, column=2)
control_button = Button(control_frame, text='Resume', command=resume_pause)
control_button.grid(row=0, column=1)

root.after(1000, restart)
root.mainloop()
