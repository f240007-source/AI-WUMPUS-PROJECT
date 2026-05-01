import streamlit as st
import numpy as np
import random

st.set_page_config(layout="wide")
st.title("Dynamic Wumpus World Knowledge Agent")

rows = st.slider("Rows", 3, 10, 5)
cols = st.slider("Cols", 3, 10, 5)

if "init" not in st.session_state:
    st.session_state.init = False

if not st.session_state.init:
    st.session_state.agent = (0, 0)
    st.session_state.visited = set()
    st.session_state.pits = set()
    st.session_state.wumpus = (0, 0)
    st.session_state.kb = []
    st.session_state.cnf = []
    st.session_state.steps = 0
    st.session_state.percepts = []

def generate_world(r, c):
    pits = set()
    for _ in range((r * c) // 5):
        pits.add((random.randint(0, r-1), random.randint(0, c-1)))
    w = (random.randint(0, r-1), random.randint(0, c-1))
    return pits, w

def percept(x, y):
    p = []
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx, ny = x + dx, y + dy
        if (nx, ny) in st.session_state.pits:
            p.append("B")
        if (nx, ny) == st.session_state.wumpus:
            p.append("S")
    return p

def tell(x, y, p):
    st.session_state.kb.append((x, y, p))
    clause = {"pos": (x, y), "B": "B" in p, "S": "S" in p}
    st.session_state.cnf.append(clause)

def neighbors(x, y):
    n = []
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            n.append((nx, ny))
    return n

def ask(x, y):
    st.session_state.steps += 1
    for c in st.session_state.cnf:
        if c["B"] and (x, y) in neighbors(*c["pos"]):
            return False
        if c["S"] and (x, y) in neighbors(*c["pos"]):
            return False
    return True

def move():
    x, y = st.session_state.agent
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    random.shuffle(dirs)
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if (nx, ny) not in st.session_state.visited:
                if ask(nx, ny):
                    st.session_state.agent = (nx, ny)
                    return

if st.button("New Episode"):
    st.session_state.pits, st.session_state.wumpus = generate_world(rows, cols)
    st.session_state.agent = (0, 0)
    st.session_state.visited = set()
    st.session_state.kb = []
    st.session_state.cnf = []
    st.session_state.steps = 0
    st.session_state.init = True

x, y = st.session_state.agent

if st.button("Move Agent"):
    p = percept(x, y)
    st.session_state.percepts = p
    tell(x, y, p)
    st.session_state.visited.add((x, y))
    move()

st.subheader("Grid Visualization")

for i in range(rows):
    cols_ui = st.columns(cols)
    for j in range(cols):
        color = "#D3D3D3"
        if (i, j) in st.session_state.visited:
            color = "#90EE90"
        if (i, j) in st.session_state.pits or (i, j) == st.session_state.wumpus:
            color = "#FF4B4B"
        if (i, j) == st.session_state.agent:
            color = "#1E90FF"
        cols_ui[j].markdown(
            f"<div style='width:45px;height:45px;background:{color};border:2px solid black'></div>",
            unsafe_allow_html=True
        )

st.subheader("Metrics Dashboard")

c1, c2, c3 = st.columns(3)
c1.metric("Inference Steps", st.session_state.steps)
c2.write("Percepts")
c2.write(st.session_state.percepts)
c3.write("CNF Clauses")
c3.write(len(st.session_state.cnf))