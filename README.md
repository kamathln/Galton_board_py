# dalton_board_py
A bad simulation(?) of Dalton Board. (used to demonstrate normal/gaussian distribution)

## About the Dalton board/ simulation
There are two parts of the Dalton board. I call the top part "the distributor/randomizer" and the bottom part "the collector". Both of them are made up of equal number of columns, through which the balls can pass. Balls are entered through the top of the randomizer part. The balls descend throught the randomizer one row at a time, shifting at max one column either side randomly. Once the ball has passed to the the collector, the ball simply moves down and gets colelcted at the bottom of that column.

## Usage patterns
 - Running the file with ```$ python daltonboard.py``` runs a simulation(?) of Dalton Board on the terminal with some presets. 
Using command line parameters, you can control the number of balls, the width and height of the distributor/randomizer and the distributor.
 - Running the file with ```$ python daltonboard.py --help``` lists the parameters that can be played with.
 - The app can run the simulation without showing on the screen and output only the collector of the last frame as a CSV.
 - You could import this file as a module and use the DaltonBoard class to run your own simulation.
