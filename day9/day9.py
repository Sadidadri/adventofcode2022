"""
--- Day 9: Rope Bridge ---
This rope bridge creaks as you walk along it. You aren't sure how old it is, or whether it can even support your weight.

It seems to support the Elves just fine, though. The bridge spans a gorge which was carved out by the massive river far below you.

You step carefully; as you do, the ropes stretch and twist. You decide to distract yourself by modeling rope physics; maybe you can even figure out where not to step.

Consider a rope with a knot at each end; these knots mark the head and the tail of the rope. If the head moves far enough away from the tail, the tail is pulled toward the head.

Due to nebulous reasoning involving Planck lengths, you should be able to model the positions of the knots on a two-dimensional grid. Then, by following a hypothetical series of motions (your puzzle input) for the head, you can determine how the tail will move.

Due to the aforementioned Planck lengths, the rope must be quite short; in fact, the head (H) and tail (T) must always be touching (diagonally adjacent and even overlapping both count as touching):

....
.TH.
....

....
.H..
..T.
....

...
.H. (H covers T)
...
If the head is ever two steps directly up, down, left, or right from the tail, the tail must also move one step in that direction so it remains close enough:

.....    .....    .....
.TH.. -> .T.H. -> ..TH.
.....    .....    .....

...    ...    ...
.T.    .T.    ...
.H. -> ... -> .T.
...    .H.    .H.
...    ...    ...
Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail always moves one step diagonally to keep up:

.....    .....    .....
.....    ..H..    ..H..
..H.. -> ..... -> ..T..
.T...    .T...    .....
.....    .....    .....

.....    .....    .....
.....    .....    .....
..H.. -> ...H. -> ..TH.
.T...    .T...    .....
.....    .....    .....
You just need to work out where the tail goes as the head follows a series of motions. Assume the head and the tail both start at the same position, overlapping.

For example:

R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
This series of motions moves the head right four steps, then up four steps, then left three steps, then down one step, and so on. After each step, you'll need to update the position of the tail if the step means the head is no longer adjacent to the tail. Visually, these motions occur as follows (s marks the starting position as a reference point):

== Initial State ==

......
......
......
......
H.....  (H covers T, s)

== R 4 ==

......
......
......
......
TH....  (T covers s)

......
......
......
......
sTH...

......
......
......
......
s.TH..

......
......
......
......
s..TH.

== U 4 ==

......
......
......
....H.
s..T..

......
......
....H.
....T.
s.....

......
....H.
....T.
......
s.....

....H.
....T.
......
......
s.....

== L 3 ==

...H..
....T.
......
......
s.....

..HT..
......
......
......
s.....

.HT...
......
......
......
s.....

== D 1 ==

..T...
.H....
......
......
s.....

== R 4 ==

..T...
..H...
......
......
s.....

..T...
...H..
......
......
s.....

......
...TH.
......
......
s.....

......
....TH
......
......
s.....

== D 1 ==

......
....T.
.....H
......
s.....

== L 5 ==

......
....T.
....H.
......
s.....

......
....T.
...H..
......
s.....

......
......
..HT..
......
s.....

......
......
.HT...
......
s.....

......
......
HT....
......
s.....

== R 2 ==

......
......
.H....  (H covers T)
......
s.....

......
......
.TH...
......
s.....
After simulating the rope, you can count up all of the positions the tail visited at least once. In this diagram, s again marks the starting position (which the tail also visited) and # marks other positions the tail visited:

..##..
...##.
.####.
....#.
s###..
So, there are 13 positions the tail visited at least once.

Simulate your complete hypothetical series of motions. How many positions does the tail of the rope visit at least once?

"""

__author__ = "Adrián Ángel Moya Moruno"

data = {}
data['current_head_position'] = "0,0"
data['current_tail_position'] = "0,0"

tail_visited_positions = ['0,0']
test = []

def execute_line(direction,n_moves):
    for i in range(n_moves):
        execute_movement(direction)

def execute_movement(direction):
    #Get the value of a single movement:
    movement_coordinate = move_one_cell(direction)
    
    #First move the head:
    data['current_head_position'] = add_coordinates(data['current_head_position'],movement_coordinate)
    #Then check if the tail needs to follow the head:
    xHeadCoor,yHeadCoor = data['current_head_position'].split(',')
    xTailCoor,yTailCoor = data['current_tail_position'].split(',')
    xResult = int(xHeadCoor) - int(xTailCoor)
    yResult = int(yHeadCoor) - int(yTailCoor)
    if (needToMoveTail(xResult,yResult)):
        if(isDiagonalMovement(xResult,yResult)):
            xFinalCoordinate = xResult
            yFinalCoordinate = yResult
            if (xResult == 2):
                xFinalCoordinate = 1
            elif (xResult == -2):
                xFinalCoordinate = -1
            elif (yResult == 2):
                yFinalCoordinate = 1
            else: #(xResult == -2)
                yFinalCoordinate = -1
            #Finally move in diagonal
            finalCoordinate = str(xFinalCoordinate)+","+str(yFinalCoordinate)
            data['current_tail_position'] = add_coordinates(data['current_tail_position'],finalCoordinate)
        else:
            data['current_tail_position'] = add_coordinates(data['current_tail_position'],movement_coordinate)
        #Register tail movement in our historic
        if data['current_tail_position'] not in tail_visited_positions:
            tail_visited_positions.append(data['current_tail_position'])
    
    test.append(data['current_head_position'])

def move_one_cell(direction):
    if(direction == 'L'): #LEFT
        return "-1,0"
    elif(direction == 'R'): #RIGHT
        return "1,0"
    elif(direction == 'D'): #DOWN
        return "0,-1"
    else: #UP
        return "0,1"

def add_coordinates(current_coordinate,coordinate_to_add):
    xCurrentCoor,yCurrentCoor = current_coordinate.split(',')
    xAddCoor,yAddCoor = coordinate_to_add.split(',')
    
    xResult = int(xCurrentCoor) + int(xAddCoor)
    yResult = int(yCurrentCoor) + int(yAddCoor)

    return str(xResult)+","+str(yResult)

#We check both positions, if there is a difference of 2 in one of the edges, we know that we have to move the tail also
def needToMoveTail(xResult,yResult):
    return abs(xResult) >= 2 or abs(yResult) >= 2

def isDiagonalMovement(xResult,yResult):
    return abs(xResult) > 0 and abs(yResult) > 0

f = open("./input.txt", "r")
for line in f.readlines():
    line = line.replace("\n", "")
    direction, n_moves = line.split(' ')
    n_moves = int(n_moves)
    execute_line(direction,n_moves)


print("The tail has visited "+str(len(tail_visited_positions))+" cells")