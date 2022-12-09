"""
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390
Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

To begin, get your puzzle input.

--- Part Two ---
Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390
Looking up, its view is not blocked; it can see 1 tree (of height 3).
Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
Looking right, its view is not blocked; it can see 2 trees.
Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).
A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390
Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?

"""
__author__ = "Adrián Ángel Moya Moruno"

def isVisibleInRow(tree_value,column_index,tree_row):
    visibleInLeft = True
    visibleInRight = True
    for index, tree in enumerate(tree_row):
        if index < column_index:
            if(tree_value <= int(tree)):
                visibleInLeft = False
        elif index == column_index: # Here the tree in the row is the same that we are comparing
            continue
        else:
            if(tree_value <= int(tree)):
                visibleInRight = False
    return visibleInLeft or visibleInRight

def isVisibleInColumn(tree_value,tree_row_index,tree_col_index):
    visibleInTop = True
    visibleInBottom = True
    for row_index, row in enumerate(grid):
        if row_index < tree_row_index:
            if(tree_value <= int(row[tree_col_index])):
                visibleInTop = False
        elif row_index == tree_row_index:
            continue
        else:
            if(tree_value <= int(row[tree_col_index])):
                visibleInBottom = False
    return visibleInTop or visibleInBottom

def calculateRowScore(tree_value,column_index,tree_row):
    leftScore = 0
    rightScore = 0
    left_trees = tree_row[:column_index]
    left_trees.reverse()
    right_trees = tree_row[column_index+1:]
    for tree in left_trees:
        leftScore+=1
        if (int(tree) >= tree_value):
            break
    for tree in right_trees:
        rightScore+=1
        if (int(tree) >= tree_value):
            break
    return leftScore * rightScore

def calculateColumnScore(tree_value,tree_row_index,tree_col_index):
    topScore = 0
    bottomScore = 0
    for i in range (tree_row_index-1,-1,-1):
        topScore += 1
        if(int(grid[i][tree_col_index]) >= tree_value):
            break
    for j in range (tree_row_index+1,len(grid)):
        bottomScore += 1
        if(int(grid[j][tree_col_index]) >= tree_value):
            break
            
    return bottomScore * topScore


    
f = open("./input.txt", "r")
grid = []
for line in f.readlines():
    line = line.replace("\n", "")
    tree_column = [tree for tree in line]
    grid.append(tree_column)

max_rows = len(grid)
max_columns = len(grid[0])
#we count here the trees that are outside
visible_trees = max_rows*2-2+max_columns*2-2

for row_index, row in enumerate(grid):
    if row_index != 0 and row_index != max_rows-1:# 1st and last rows are visibles
        for col_index, tree_height in enumerate(row):
            if col_index != 0 and col_index != max_columns-1:# 1st and last columns are visibles
                if isVisibleInRow(int(tree_height),col_index,row) or isVisibleInColumn(int(tree_height),row_index,col_index):
                    visible_trees += 1
    
print("Solution 1: "+str(visible_trees))


#Let's do a really similar logic in part 2
maximum_score = 0

for row_index, row in enumerate(grid):
    if row_index != 0 and row_index != max_rows-1:# 1st and last row are in borders
        for col_index, tree_height in enumerate(row):  
            if col_index != 0 and col_index != max_columns-1:# 1st and last columns are in the borders   
                tree_score =  calculateRowScore(int(tree_height),col_index,row) * calculateColumnScore(int(tree_height),row_index,col_index)
                if tree_score > maximum_score:
                    maximum_score = tree_score
                 

print("Part 2. The maximum score is: "+str(maximum_score))
