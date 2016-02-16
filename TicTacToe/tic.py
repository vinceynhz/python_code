import random

def count( vector, values = (1,2) ):
    ''' 
    This helps us to count how many of each value are in a given row
    to determine how high is the risk of playing
    '''
    count = { i : vector.count(i) for i in values }
    return count
    
class Board():
    _string = "  {0}|{1}|{2}\n  {line}\n  {3}|{4}|{5}\n  {line}\n  {6}|{7}|{8}\n"
    _line = "---+---+---"
    # define which indexes are corners and which one sides, and the center
    _corners = [0, 2, 6, 8] 
    _sides = [1, 3, 5, 6]
    _center = [4]
    
### PRIVATE CLASS METHODS
    def _tochar( item ):
        ''' For a given item, get its char representation '''
        return { 0 : ' ', 1 : 'o', 2 : 'x', 3 : ' ' }[ item ]

    def _translate( position = None, coords = None ):
        ''' 
        Transform a positional value (from the vector) to it's coordinates
        or a coordinate tuple (from the board) to its positional value '''
        if position is not None:
            return ( position // 3, position % 3 )
        
        if coords is not None:
            return coords[0] * 3 + coords [1]
        
        return None

### CONSTRUCTOR
    def __init__( self, **kwargs ):
        self.board = None
        self.reset()

### TO STRING
    def __str__( self ):
        output = "\n"
        values = [ str( Board._tochar( item ) ).center(3) for row in self.board for item in row ]
        output += Board._string.format( *values, line = Board._line )

        return output

### PRIVATE INSTANCE METHODS
    def _vector( self ):
        ''' Transform the board (3x3) into a vector (1x9) '''
        new = [ item for row in self.board for item in row ]
        return new

    def _empties( self, rand = True ):
        ''' Take from the vector and just return the indexes for the empty ones '''
        plays = self._vector()

        if plays.count(0) == 0: # No empties
            return None

        positions = [ index for index, value in enumerate(plays) if value == 0 ]

        if rand and positions is not None:
            random.shuffle( positions )

        return positions

    def _rdiag( self ):
        ''' Get the right diagonal of the board '''
        return [ self.board[i][i] for i in range(3) ]

    def _ldiag( self ):
        ''' Get the left diagonal of the board '''
        return [ self.board[i][2 - i] for i in range(3) ]

    def _cdiag( self ):
        ''' Get both diagonals in an array '''
        return [ self._rdiag(), self._ldiag() ]

    def _diags( self, position ):
        ''' Get a diagonal given a position '''
        if (position not in Board._corners and 
            position not in Board._center):
            return None

        return{
            0 : self._rdiag(), #tl corner
            2 : self._ldiag(), #tr corner
            4 : self._cdiag(), #center : both diagonals
            6 : self._ldiag(), #bl corner
            8 : self._rdiag()  #br corner
        }[ position ] 

    def _count( self, position, value ):
        ''' 
        This method will count how many of each value are in the lines (h,v or d's)
        depending on the given position.

        The result will be a dictionary with each direction (h,v, or d's)
        '''
        # this dict will have all the values
        status = {}

        # get the coords
        coords = Board._translate( position )

        # verify position is playable
        if not self.assign( value, coords ): return None

        #let's count the horizontal cells
        row = self.board[ coords[0] ]
        status['hcount'] = count( row )
        #print( row, status['hcount'] )

        #let's count the vertical cells
        column = [ self.board[i][coords[1]] for i in range(3) ]
        status['vcount'] = count( column )
        #print( column, status['vcount'] )

        #if corner
        if (position) in Board._corners:
            # let's count the diagonal
            diag = self._diags( position )
            status['dcount'] = count( diag )
            #print( diag, status['dcount'] )

        #if center
        if position in Board._center:
            # for center we need both diagonals
            diag = self._diags( position )
            status['drcount'] = count( diag[0] )
            status['dlcount'] = count( diag[1] )
            #print( diag, status['drcount'], status['dlcount'] )

        # reset the position to the board
        self.board[ coords[0] ][ coords[1] ] = 0

        return status

    def _calculate( self, position, value ):
        ''' Get the calculated value for a given position in the board '''
        status = self._count( position, value )
        
        #### Here comes the calculations ####
        
        # Note: to get the oposite of the current value it will be 3 - value
        # if value = 1, then the opposite is 3-1 = 2
        # if value = 2, then the opposite is 3-2 = 1... tada!
        total = { 
                  'win' : False, # or if we're just about to win
                  'risk' : False, # if we are in risk of losing
                  'togo' : 3, # best number of pieces to go in this play (2, 1)
                  'value' : 0, # calculated value
                  'blocks' : 0, # how many we are blocking from the oponent
                  'possibles' : 0, # possible plays in the line (h,v,d's)
                  'preferred' : False,
                  'position' : position
                }

        for item in status:
            # determine if this play wins the game, if so, say so and leave
            if status[item][value] == 3:
                total['win'] = True
                break

            #determine if this one could be a possible play
            if status[item][3 - value] == 0:
                total['possibles'] += 1
                # if a possiblity, determine how many plays we need in the line:
                if 3 - status[item][value] < total['togo']:
                    total['togo'] = 3 - status[item][value]

            # or if this play can block the oponent (and ourselves...)
            elif status[item][3 - value] == 1:
                total['blocks'] += 1

            # or if we are about to lose, say so and leave
            elif status[item][3 - value] == 2:
                total['risk'] = True
                break

            # if any diagonal from me (meaning I'm a center or a corner)
            if item in ['dlcount', 'drcount', 'dcount']:
                # has an oponent value, I can suggest this one
                if status[item][3 - value] > 0:
                    total['preferred'] = True

        # the function if I have more plays to go than blocks to make, go for the blocks
        if total['togo'] > total['blocks']:
            total['value'] = ( total['blocks'] + total['togo'] ) / total['possibles'] if total['possibles'] > 0 else -1
        # else if, I'm getting closer to win, go for it!
        else:
            total['value'] = ( total['possibles'] + total['togo'] ) / total['blocks'] if total['blocks'] > 0 else -1

        return total

### PUBLIC INSTANCE METHODS
    def reset( self ):
        self.board = [[ 0 for j in range(3) ] for i in range(3) ]

    def has_space( self ):
        ''' to verify if there are available spaces '''
        vect = self._vector()
        return vect.count(0) > 0

    def has_winner( self ):
        #let's check each hline
        for row in self.board:
            c = count(row)
            if c[1] == 3: return 1
            if c[2] == 3: return 2

        # let's check each vline
        for j in range(3):
            col = [ self.board[i][j] for i in range(3) ]
            c = count(col)
            if c[1] == 3: return 1
            if c[2] == 3: return 2

        # let's check the diagonals
        diag = self._cdiag()
        c = count(diag[0])
        if c[1] == 3: return 1
        if c[2] == 3: return 2
        c = count(diag[1])
        if c[1] == 3: return 1
        if c[2] == 3: return 2

        return False

    def assign( self, value, coords ):
        ''' To assign safely a value to a cell '''
        if coords is None: return False
        # if the cell is already occuppied return False
        if self.board[coords[0]][coords[1]] != 0: return False
        
        # if not, assign and return True
        self.board[coords[0]][coords[1]] = value

        return True
    
    def play( self, value, rand = True ):
        # This will return all the possible empty cells in the board
        # so I can go and iterate through them
        plays = self._empties(rand)
        
        # I start with no movement
        maxval = None
        for position in plays:
            # get the value for this position in the current board
            movement = self._calculate(position, value)

            # make sure we can play it...
            if movement is not None: 
                # if we are about to lose, save to see if we can also win
                if movement['risk']:
                    maxval = movement

                # if this is our winning movement return it immediately
                if movement['win']:
                    return movement

                # this is the rule... If we don't have a value yet (first cell)
                # or if we do, we verify that we are not in risk (more important)
                # and that the current movement is not preferred (meaning a corner)
                # and this movement represents a better value than the current
                # or is preferred
                if ( maxval is None or ( 
                        maxval is not None and 
                        not maxval['risk'] and 
                        not maxval['preferred'] and( 
                            movement['value'] > maxval['value'] or 
                            movement['preferred'] )
                    )): maxval = movement

        return maxval

class Player():
    def __init__(self, **kwargs):
        # 0 Human, 1 PC
        self.type = kwargs['type'] if 'type' in kwargs else 0 # Human
        self.name = kwargs['name'] if 'name' in kwargs else "player"
        # 1 o, 2 x
        self.value = kwargs['value'] if 'value' in kwargs else 0 # no value
        self.score = kwargs['score'] if 'score' in kwargs else 0 # no score

    def __str__(self):
        output = "{name} ".format(name = self.name)
        output += "Human" if self.type == 0 else "PC"
        output += "({char}) - Score: {score}".format( char=Board._tochar(self.value), score=self.score )
        return output

    def win( self ):
        self.score += 1

class Game():
    def __init__(self, **kwargs):
        self.players = {}
        self.current = 1 # who's turn is it
        self.old_current = 1
        self.board = Board() # and we start a clean board
        self.alternate = False
        
        if 'p1' in kwargs:
            self.players[1] = kwargs['p1']
        else:
            self.players[1] = Player( name='p1', value=1 )  # by default, player 1 is o

        if 'p2' in kwargs:
            self.players[2] = kwargs['p2']
        else:
            self.players[2] = Player( name='p2', value=2 )  # and by default, player 2 is x

    def reset( self, alternate = False ):
        self.current = 1
        self.board.reset()
        
        if alternate:
            self.current = 3 - self.old_current

            self.players[1].value = 3 - self.players[1].value
            self.players[2].value = 3 - self.players[2].value

        self.old_current = self.current

    def next(self, position = None):
        # Let's check if there is no space available 
        if not self.board.has_space(): return False
        if self.board.has_winner(): return False

        t = self.players[self.current].type
        v = self.players[self.current].value
        
        if t == 1: # meaning that it should be played by the PC
            # then we get the position to be played
            play = self.board.play(v)
            p = play['position']

        else: # meaning that we expect a movement
            if position is None: return False
            p = position

        if self.board.assign(v, Board._translate(p)):
            # move to the next one to play
            self.current = 3 - self.current
            #print(t, self.current)

            return p

        return False
