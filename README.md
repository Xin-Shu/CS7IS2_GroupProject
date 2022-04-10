# CS7IS2_GroupProject
This is a GitHub repository which codes and analysis are submitted in partial fulfilment of the requirements for Trinity College Dublin Computer Science module CS7IS2 Artificially Intelligence.

## Participant:
- Fan Bu, bufa@tcd.ie
- Xin Lyu, lyux@tcd.ie
- Xin Shu, xins@tcd.ie
- Yanxiang Chen, cheny16@tcd.ie

## Environment and packages
**The version listed below are used, developed and tested.**\
**Using other versions may or may not compile the scripts.**\
**Packages that are not listed in here do not require specific version.**
- Python 3.6.13 or higher
- numpy 1.22.3
- pygame 2.1.2
- tensorflow:
  - On Intel and NVidia core: 1.15.5
  - On AMD Ryzen and Radeon core: tensorflow-directml 1.15.5, but require version of Python to be not higher than 3.6.*

## Addressed and solved game
Sudoku is a logic-based, combinatorial number-placement puzzle. In classic Sudoku, the objective is to fill a 9 × 9 
grid with digits so that each column, each row, and each of the nine 3 × 3 subgrids that compose the grid (also called 
"boxes", "blocks", or "regions") contain all the digits from 1 to 9. The puzzle setter provides a partially 
completed grid, which for a well-posed puzzle has a single solution.

## Usage
Clone git repository:
```
git clone https://github.com/Xin-Shu/CS7IS2_GroupProject.git
```
With an installed conda environmnet or python virtual environment:
```
pip install ./requirement.txt
```
Compile sudoku game:
```
python sudokuGame.py
```

To use algorithms on the game:
- Press `q` to set an Easy level sudoku puzzle with up to 35 blanks.
- Press `w` to set a medium level sudoku puzzle with up to 41 blanks.
- Press `e` to set a hard level sudoku puzzle with up to 52 blanks.
- Press `s` to crack the game using algorithm **Backtracking**.
- Press `l` to crack the game using algorithm **Deep Neural Network**, with a given pretrained model.
- Press `g` to crack the game using algorithm **Genetic Solver**.

## Used AI Algorithms 
- Backtracking, average solving time:
- Genetic Algorithm, average solving time:
- Deep Neural Network, average solving time:

## Links
- Link to our GitHub repository: 
```
github.com/Xin-Shu/CS7IS2_GroupProject
```
- Link to our Overleaf report: 
```
overleaf.com/read/mpsjcjhrgcqp
```
- Link to our presentation video: 
```
drive.google.com/file/d/13ugbmA0oZOj8Vhty6x3yIHxstCvHyJrI/view?usp=sharing
```

## Contributions
- Bu Fan:
- Xin Lyu:
- Xin Shu: proposal and development of CNN solution, refine the sudoku game scripts from forked repositories, 
settle project GitHub repository, voice over the presentation video.
- Yanxiang Chen:
