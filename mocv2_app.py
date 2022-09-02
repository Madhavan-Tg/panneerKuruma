#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 06:59:44 2022

@author: aki
"""
from pygasflow.nozzles.moc import min_length_supersonic_nozzle_moc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import streamlit as st
import time 
import pandas as pd

st.write('# A MOC nozzle solver_Visualisation')
ht = 1.5
n = 20
Me = 5
gamma = 1.4
#pr_bar = st.progress(0)
st.sidebar.markdown('## Parameters')
st.sidebar.write('Height of Throat area of planar nozzle')
ht = st.sidebar.number_input('ht',0.001)
st.sidebar.write('number of Charecteristic lines')
n = st.sidebar.number_input('n',3)
st.sidebar.write('Mach Number at Exit')
Me = st.sidebar.number_input('Me',1.1)
st.sidebar.write('Ratio of Specific Heats')
gamma = st.sidebar.number_input('gamma',1.1)
wall, characteristics, left_runn_chars, theta_w_max = min_length_supersonic_nozzle_moc(ht, n, Me, None, gamma)
x, y, z = np.array([]), np.array([]), np.array([])
#pr_bar.progress(50)
#time.sleep(0.1)
for char in left_runn_chars:
    x = np.append(x, char["x"])
    y = np.append(y, char["y"])
    z = np.append(z, char["M"])
fig = plt.figure()
# draw characteristics lines
for c in characteristics:
    plt.plot(c["x"], c["y"], "k:", linewidth=0.25)

# draw nozzle wall
plt.plot(wall[:, 0], wall[:, 1], "k")
#plt.plot(wall[:, 0], -wall[:, 1], "k")
# over impose grid points colored by Mach number
sc = plt.scatter(x, y, c=z, s=15, vmin=min(z), vmax=max(z), cmap=cmx.tab20)
cbar = plt.colorbar(sc, orientation='vertical', aspect=40)
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel("Mach number", rotation=270)
plt.xlabel("Length of Nozzle in m")
plt.ylabel("Height of nozzle in m")
plt.title(r"$M_e$ = {}, n = {}, ht = {} ".format(Me, n, ht))
plt.grid()
plt.axis('equal')
plt.xlim(0,)
plt.tight_layout()
plt.show()
st.pyplot(fig)
#pr_bar.progress(100)
if st.button('save to text file'):
    df  = pd.DataFrame({'x':wall[:, 0],'y':wall[:, 1]})
    df.to_csv('moc_nozzle.txt',header=False,index=False)