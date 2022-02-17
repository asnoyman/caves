# Caves: AKA Akari / Light Up
An interface to play some pre-loaded cave puzzles or make your own. Alternatively you can use the solver to watch the puzzles solve themselves!

# Preview
![Alt text](caves_img.png?raw=True "Title")

# Goal
Light up every square in the cave (except the black blocks) such that every numbered block touches that many lights orthogonally and no two lights light up each other. 

# Procedures
When you want to load a pre-existing puzzle to play, enter l1 (or whichever number in test you wish to play). Then immediately press enter and the timer will start. If you want to build you own puzzle, enter a number for the grid size and then build the puzzle using your mouse. Each click will toggle the next type of block. Alternatively you can hover your mouse over the cell and click the number you wish to make (with space being an unclued block and backspace being empty). When happy with the layout, click enter and the cells will lock in andthe timer will start.

To watch a solve, run the solver file and enter the test cave in the terminal (just the number NOT tests/). If it is too slow, lower the SLEEP variable in the code.

# Playing the Game
Once the timer starts, you will be able to click for a light, click again for a cross, and finally click again to clear the cell. When you think the puzzle is solved, click enter and you will get a message in the terminal whether you are right or not and the timer will stop if you are. Upon a correct solution, you won't be able to edit the grid anymore.

# Reason for Creation
With only the experience I had from my Towers of Hanoi experiment, I wanted to test my newfound skills in a more challenging setting. Cave puzzles require complex logic to solve, and the solution can't be found online like the Towers of Hanoi. This required me to implement some logic to optimize the solve, as well as learn to manipulate images in the GUI and handle logic involving time with the timer. I also wanted to allow a user to input their own puzzle within the interface, which required a mixture of monitoring mouse clicks, position and keyboard inputs. The solver uses a depth first search algorithm when it can not see any more logic, which was a more complex algorithm than the simple recursion of Towers of Hanoi.
