# Pason Coding Contest
Entry for the January 2016 Pason Coding Contest.

## Todo List
* Conversion of map into grid
- see Game State - Map object -- has game board description using integer values for board and objects on board
https://en.wikipedia.org/wiki/Euclidean_shortest_path shortest path wrt the real grid
https://users.cs.duke.edu/~reif/paper/storer/shotestpathplane.pdf # we could be really lazy and see if there is an obstacle in the way, go to the left or right
side of it.

* Implementation of pathfinding from tank to point/tank
- if we want to move in the 8 squares around the tank -- just fix the radians to those location with the tracks on the tank
- eg a constant value for each of the directions.
- we can run all path shortest path to find the shortest path from each of our tanks to each of the enemies I think
- then the tanks can move on all of the passable objects
- CAVEAT: if there is a quicker path using a straight line that is not based on one of our 8 directions we will not take it
- CAVEAT: if there is a curved route that works better, we will not take it with the 8 directions choice

* Move queue for tanks to follow path through algorithm
* Tanks move just out of (within?) firing range of enemy tanks before firing
my_tank.projectiles[0].range < enemy_tank.projectiles[0].range? # can tanks have more than 1 projectile?
- do all tanks have same range
- consider if they are not equal?
* Optional, tank pairing?
* Optional, handling of Sudden Death mode? (move to center while walls close in)
* Optional, orbit enemy tank and approximate where they will move and shoot there? (complicated)

## Links
* Specifications: [https://codingcontest.pason.com/static/common/pdf/BattleTanks-1.1.3.pdf](https://codingcontest.pason.com/static/common/pdf/BattleTanks-1.1.3.pdf)
* Contest Site Details: [https://codingcontest.pason.com](https://codingcontest.pason.com)

Team Members:
* Alexander Wong
* Stephen Kalen Romansky

## License
The MIT License (MIT)

Copyright (c) 2015 Alexander Wong, Stephen Kalen Romansky

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

