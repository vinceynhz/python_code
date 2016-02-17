#  Conway's rule
#  Death rule:
#  Any live cell with fewer than two live neighbours dies, as if caused by under-population.
#  Any live cell with more than three live neighbours dies, as if by over-population.
#  - For any given cell, count neighbours 
#       All around cells: abs(x0 - x) == 1 and abs(y0 - y) == 1
#
#       sum( 1 for coord in elements if ( x0 != coord[0] and y0 != coord[1] ) and abs(x0-coord[0]) <= 1 and abs(y0-coord[1]) <= 1)
#
#       If neighbours == 1 or neighbours > 3: dies
#       Else: lives to next generation
#  
#  Birth rule:
#  Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
#  - For any given cell, count extended neighbourhood considering the cell as the mid-edge cell of a hypothetical square
#       x0, y0:
#           First           Second          Third           Fourth
#       (0) - x0+1, y0      - x0, y0-1      - x0-1, y0      - x0, y0+1
#       (1) - x0+1, y0+1    - x0+1, y0-1    - x0-1, y0-1    - x0-1, y0+1
#       (2) - x0+1, y0+2    - x0+2, y0-1    - x0-1, y0-2    - x0-2, y0+1
#       (3) - x0, y0+2      - x0+2, y0      - x0, y0-2      - x0-2, y0
#       (4) - x0-1, y0+2    - x0+2, y0+1    - x0+1, y0-2    - x0-2, y0-1
#       (5) - x0-1, y0+1    - x0+1, y0+1    - x0+1, y0-1    - x0-1, y0-1
#       (6) - x0-1, y0      - x0, y0+1      - x0+1, y0      - x0, y0-1
#    
#       [ (i-3) // -abs(i-3)    if i != 3 else 0 for i in range(7) ]
#       u1 = [1, 1, 1, 0, -1, -1, -1]
#    
#       [ 3-abs(i-3)            if i != 3 else 2 for i in range(7) ]    : [0, 1, 2, 2, 2, 1, 0]
#       u2 = [0, 1, 2, 2, 2, 1, 0]
#
#       sum( 1 for p in buf for i in range(7) if p[0] == pivot[0] + u1[i] and p[1] == pivot[1] + u2[i] ) 
#       sum( 1 for p in buf for i in range(7) if p[0] == pivot[0] + u2[i] and p[1] == pivot[1] - u1[i] )
#       sum( 1 for p in buf for i in range(7) if p[0] == pivot[0] - u1[i] and p[1] == pivot[1] - u2[i] )
#       sum( 1 for p in buf for i in range(7) if p[0] == pivot[0] - u2[i] and p[1] == pivot[1] + u2[i] )
#      
#       If sum == 2 ( we count the current one, that makes 3 neighbours ):
#           Then we add 1 to the elements:
#               If first sum:
#                   Add x0, y0+1
#               If second sum:
#                   Add x0+1, y0
#               If third sum:
#                   Add x0, y0-1
#               If fourth sum:
#                   Add x0-1, y0
#       v1 = [0, 1, 0, -1]
#       v2 = [1, 0, -1, 0]

# All those that do not die
def survivors(elements):
    result = []
    for cell in elements:
        s = sum( 1 for c in elements if cell != c and abs(cell[0]-c[0]) <= 1 and abs(cell[1]-c[1]) <= 1 )
        if s >= 2 and s <= 3:
            result.append(cell)

    return result

def births(elements):
    result = []
    for cell in elements:
        s = count_neighbourhoods(elements, cell)
        n = newborns(cell, s)
        if len(n) >= 1:
            addnodup(result, n)

    return result

def addnodup(vector, new):
    if type(new) is list:
        for ind in new:
            if ind not in vector:
                vector.append(ind)
    else:
        vector.append(new)

def count_neighbourhoods(elements, cell):
    u1 = [1, 1, 1, 0, -1, -1, -1]
    u2 = [0, 1, 2, 2, 2, 1, 0]

    # If the cell above the current one is occupied
    if [ cell[0], cell[1]+1 ] in elements:
        w = 0
    else:
        w = sum( 1 for c in elements for i in range(7) if c[0] == cell[0] + u1[i] and c[1] == cell[1] + u2[i] )

    # If the cell to the right of the current one is occupied
    if [ cell[0] + 1, cell[1] ] in elements:
        x = 0
    else:
        x = sum( 1 for c in elements for i in range(7) if c[0] == cell[0] + u2[i] and c[1] == cell[1] - u1[i] )

    # If the cell below the current one is occupied
    if [ cell[0], cell[1]-1 ] in elements:
        y = 0
    else:
        y = sum( 1 for c in elements for i in range(7) if c[0] == cell[0] - u1[i] and c[1] == cell[1] - u2[i] )

    # If the cell to the left of the current one is occupied
    if [ cell[0]-1, cell[1] ] in elements:
        z = 0
    else:
        z = sum( 1 for c in elements for i in range(7) if c[0] == cell[0] - u2[i] and c[1] == cell[1] + u1[i] )

    return [w,x,y,z]

def newborns(cell, count):
    v1 = [0, 1, 0, -1]
    v2 = [1, 0, -1, 0]

    return [ [ cell[0] + v1[i], cell[1] + v2[i] ] for i,v in enumerate(count) if v == 2 ]
