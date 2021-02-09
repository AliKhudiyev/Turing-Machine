import numpy as np
import sys, getopt, time, re
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
        print(f'States:{states}\nSymbols:{symbols}\nBlank:{blank}\nInput symbols:{input_symbols}\nInitial state:\
{init_state}\nFinal state:{final_state}')
        print('\nTransitions:')
        for transition in transitions:
            print(transition[0], '->', transition[1])
        print()
    
    direction = 0
    transition = None
    while machine_state != 'HALT':
        print(machine_state, tape[index])
        is_found = False
        for transition in transitions:
            if machine_state == transition[0][0] and tape[index] == transition[0][1]:
                transition = transition
                print('applying transition:', transition)
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
            print('Halting...')
            machine_state = 'HALT'
            break
        if one_step_run:
            break
    
    return tape, machine_state, index, transition, direction

compute()
# - - - - - - - - - - - - - - - - - - -
if not visual:
    exit(0)
print(f'Animation speed: {speed}')
tape = input_symbols.copy()
state = init_state.copy()[0]
index = 0

root = Tk()
root.title('Turing Machine')

canvas = Canvas(root, width=30*15)
control_frame = Frame(root)

canvas.pack()
control_frame.pack()

transition_label = Label(control_frame, text='Transition', width=50)
transition_label.grid(row=0, column=0, columnspan=3)
# result_label = Label(control_frame, text='Result:')
# result_label.grid(row=1, column=0)

cells = list()
cell_symbols = list()
machine_state_symbol = canvas.create_text(35, 60, text='')
_radius = 30
machine = canvas.create_oval(5+_radius/2, 45, 5+3*_radius/2, 45+_radius)

for i in range(16):
    cell = canvas.create_rectangle(-10, 10, 20+_radius*i, 10+_radius)
    cell_symbol = canvas.create_text(5+_radius*i, 25, text='_')
    cells.append(cell)
    cell_symbols.append(cell_symbol)

for i in range(len(cell_symbols)-1):
    if i >= len(tape):
        break
    canvas.itemconfig(cell_symbols[i+1], text=tape[i])
canvas.itemconfig(machine_state_symbol, text=state)

def move_machine(direction, machine_state):
    sign = -1
    if direction == 'R':
        sign = 1
    for i in range(_radius):
        canvas.move(machine, sign, 0)
    canvas.move(machine_state_symbol, sign*_radius, 0)
    canvas.itemconfigure(machine_state_symbol, text=machine_state)
    
    
def move_tape(direction, machine_state):
    sign = -1
    if direction == 'R':
        sign = 1
    for i in range(_radius):
        for j in range(16):
            canvas.move(cells[j], sign, 0)
    canvas.move(machine_state_symbol, sign*_radius, 0)
    canvas.itemconfigure(machine_state_symbol, text=machine_state)

def run():
    global tape, state, index
    global speed
    
    tape, state, index, transition, dir_ = compute(one_step_run=True, tape=tape, machine_state=state, index=index)
    coord = canvas.coords(machine)
    is_halted = False
    
    if state == 'HALT':
        print(' ========= HALT ==========')
        is_halted = True
    elif coord[0] >= -10+30*14 and dir_ == 'R':
        print('shifting the tape left...')
        move_tape(direction='L', machine_state=state)
    elif coord[2] <= -10+30*2 and dir_ == 'L':
        print('shifting the tape right...')
        move_tape(direction='R', machine_state=state)
    else:
        move_machine(direction=dir_, machine_state=state)
        print(f'moving the machine {dir_}')
    
    if not is_halted:
        if transition is not None:
            transition_label.config(text=f'Transition: {transition[0][0]}, {transition[0][1]} -> {transition[1][0]}, {transition[1][1]}, {transition[1][2]}')
        for i in range(len(cell_symbols)-1):
            if i >= len(tape):
                break
            canvas.itemconfig(cell_symbols[i+1], text=tape[i])

        time_ = 2000-int(500*np.abs(speed))
        if time_ < 0:
            time_ = 10
        root.after(time_, run)

def restart():
    global tape, state, index

    tape = input_symbols.copy()
    state = init_state.copy()[0]
    index = 0

    print('\tRestarted!')
    # print(tape)
    # print(state)

    canvas.move(machine, -canvas.coords(machine)[0]+35-_radius/2, 0)
    canvas.move(machine_state_symbol, -canvas.coords(machine_state_symbol)[0]+35, 0)
    canvas.itemconfig(machine_state_symbol, text=state)
    for i in range(len(cell_symbols)-1):
        if i >= len(tape):
            break
        canvas.itemconfig(cell_symbols[i+1], text=tape[i])

    time_ = 2000-int(500*np.abs(speed))
    if time_ < 0:
        time_ = 10
    root.after(time_, run)

def change_speed(delta):
    global speed
    speed += delta
    print('Animation speed:', speed)

Button(control_frame, text='Restart', command=restart).grid(row=2, column=0)
Button(control_frame, text='Speed up', command=lambda: change_speed(0.1)).grid(row=2, column=1)
Button(control_frame, text='Slow down', command=lambda: change_speed(-0.1)).grid(row=2, column=2)

root.after(1000, run)
root.mainloop()
