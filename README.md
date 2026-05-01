# Wumpus World AI Agent (Streamlit)

## Project Description
This project is a simple AI agent simulation of the Wumpus World environment.  
The agent moves in a grid, detects hazards like pits and Wumpus, and uses basic logic to make decisions.

The system is built using Python and Streamlit.


## Features
- Dynamic grid size from 3x3 to 10x10
- AI agent movement in the grid
- Detection of breeze (near pits)
- Detection of stench (near Wumpus)
- Simple knowledge base to store percepts
- Basic inference rules for safe movement
- Grid visualization
- Metrics dashboard showing steps and percepts



## How It Works
- The agent starts at position (0,0)
- It senses the environment (breeze and stench)
- It stores percepts in memory
- It uses simple rules to decide safe moves
- It avoids visited and unsafe cells


## Technologies Used
- Python
- Streamlit
- NumPy



## How to Run the Project

pip install streamlit numpy
python -m streamlit run app.py



## Project Files
- app.py: Main Streamlit application
- requirements.txt: Required libraries
- README.md: Project documentation



## Live Demo
Add deployed link here



## Author
AI Course Project