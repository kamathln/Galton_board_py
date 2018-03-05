#!/usr/bin/python
# The MIT License (MIT)
# Copyright (c) 2018 "Laxminarayan Kamath G A"<kamathln@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import pygame
import numpy
import random

class Ball(object):
    def __init__(self, container, row, col):
        self.container = container
        self.row = row
        self.col = col
        self.cant_move_count = 0

class GaltonBoard(object):
    def __init__(self, width=25, distributorheight=22, collectorheight=22, numballs=200):
        self.width = width
        self.distributorheight = distributorheight
        self.collectorheight = collectorheight
        self.numballs = numballs
        self.ballcount = 0
        self.boardfull = False
        self.allballsin = False
        self.simdone = False
        self.balls = []

        self.distributor = numpy.zeros((self.distributorheight, self.width), dtype=object)
        self.collector = numpy.zeros((self.collectorheight, self.width), dtype=object)
        self.distributor[:,:] = None
        self.collector[:,:] = None

    def add_ball(self, col=None):
        if self.allballsin:
            return
        if col == None:
            col = self.width//2
        if self.distributor[self.distributorheight - 1,col] == None:
            newball = Ball(self.distributor, self.distributorheight-1,col)
            self.distributor[self.distributorheight - 1,col] = newball
            self.balls.append(newball)
            self.ballcount += 1
            self.boardfull = False
            self.allballsin = not (self.ballcount <= self.numballs)
        else:
            self.boardfull = True

    def process(self):
        for nr,r in enumerate(self.distributor):
            islastrow = (nr == 0)

            for nc,c in enumerate(r):
                if c is not None:
                    toss = random.randint(-1,1)
                    ballnewcol = c.col + toss
                    if not (0 < ballnewcol < self.width):
                        ballnewcol = c.col
                    if islastrow:
                        ballnewrow = self.collectorheight - 1
                        if self.collector[ballnewrow, ballnewcol] == None:
                            self.collector[ballnewrow, ballnewcol] = c
                            self.distributor[c.row, c.col] = None
                            c.container = self.collector
                            c.row = ballnewrow
                            c.col = ballnewcol
                            c.cant_move_count = 0
                        else:
                            c.cant_move_count += 1
                    else:
                        ballnewrow = c.row - 1
                        if self.distributor[ballnewrow, ballnewcol] == None:
                            self.distributor[ballnewrow, ballnewcol] = c
                            self.distributor[c.row, c.col] = None
                            c.row = ballnewrow
                            c.col = ballnewcol
                            c.cant_move_count = 0
                        else:
                            c.cant_move_count += 1
            #self.show()
            #time.sleep(0.05)
        for nr,r in enumerate(self.collector):
            islastrow = (nr == 0)
            for nc,c in enumerate(r):
                if c is not None:
                    if not islastrow:
                        ballnewrow = c.row - 1
                        if self.collector[ballnewrow, c.col] == None:
                            self.collector[ballnewrow, c.col] = c
                            self.collector[c.row, c.col] = None
                            c.row = ballnewrow
                            c.cant_move_count = 0
                        else:   
                            c.cant_move_count += 1
                    else:
                        c.cant_move_count += 1
                    
            #self.show()            
            #time.sleep(0.05)
            self.simdone = all([ball.cant_move_count >= 1 for ball in self.balls])

    def show(self):
        #print "\33c", ''.join(['o' if ball.cant_move_count >= 1 else 'O' for ball in self.balls])
        #print "Balls ", self.ballcount
        print "\33cBalls ", self.ballcount
        for nr, r in enumerate(self.distributor[::-1]):
            print ("%03d"%nr), ('|').join([ " " if c ==None else "O" for c in r])
        print ' |' * (self.width + 1)        
        for nr, r in enumerate(self.collector[::-1]):
            print ("%03d"%nr), ('|').join([ " " if c ==None else "O" for c in r])

        
    def showcollectoronly(self):
        for nr, r in enumerate(self.collector[::-1]):
            print (',').join([ "0" if c == None else "1" for c in r])
        


if __name__ == '__main__':
    import argparse
    import time
    import sys

    argparser = argparse.ArgumentParser(description="A bad Simulation of a Galton board, demonstrating Normal/Gaussian distribution")
    argparser.add_argument('--balls',   action='store', nargs='?', help="number of balls to simulate",type=int,default=200)
    argparser.add_argument('--width',   action='store', nargs='?', help="width of the Galton Board in terms of number of balls",type=int,default=30)
    argparser.add_argument('--distributorrows',   action='store', nargs='?', help="height of the distributor/randomizer/top section of the Galton board",type=int,default=24)
    argparser.add_argument('--collectorrows',   action='store', nargs='?', help="height of the collector/bottom section of the Galton board",type=int,default=24)
    argparser.add_argument('--showfullsimulation',   action='store', nargs='?', help="height of the collector/bottom section of the Galton board",type=str,default="yes")
    options=argparser.parse_args(sys.argv[1:])
    showfullsim = options.showfullsimulation.lower() in ["yes","1","true"]

    gaboard = GaltonBoard(width=int(options.width), distributorheight=int(options.distributorrows), collectorheight=int(options.collectorrows), numballs=int(options.balls))

    while not (gaboard.boardfull or gaboard.simdone):
        gaboard.add_ball()
        gaboard.process()
        if showfullsim:
            gaboard.show()
            time.sleep(0.05)

    if not showfullsim:
        gaboard.showcollectoronly()
