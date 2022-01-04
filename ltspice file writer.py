# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 11:19:10 2021

@author: Henrique
"""

import ltspice as lt
import matplotlib.pyplot as plt
import os
import pandas as pd

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

filename = input(str('File: '))
open_mode = input(str('write or open? '))
directory = input('LTSpice directory: ')
spice_path = find('XVIIx64.exe', directory)

if open_mode == 'write':
    f = open(f'{filename}.cir','w')
    print('Write the Spice NetList\n')
    while True:
        line = input(str())
        f.write(f'{line}\n')
        if line == '.END':
            break
    f.close()

os.system(f'{spice_path} -b {filename}.cir')

directory_python = input("Your python directory: ")
running_file = find(f'{filename}.raw', directory_python)

l = lt.Ltspice(running_file)
l.parse()

n_var = []
time = []
df = pd.DataFrame(l.y_raw)    
   
for n in range(len(l.variables)):
    if l.variables[n] == 'time':
        time = l.get_time()
        df = df.drop(n, 1)
        for v in range(len(l.variables)-1):
            n_var.append(f'var{n}')
            n_var[n] = df.iloc[:,n+1].values
    else:
        n_var.append(f'var{n}')
        n_var[n] = l.y_raw[:,n]
    
for i in range(len(n_var)):
    if len(n_var[i]) <= 1:
        pass
    else:
        if len(time) == 0:
            plt.plot(n_var[i])
            plt.show()
        else:
            plt.plot(time, n_var[i])
            plt.show()
        
        
        
        
        