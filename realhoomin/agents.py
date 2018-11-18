from mesa import Agent
import numpy as np

class GenericHoomin(Agent):


    grid = None
    x = None
    y = None

    startingpos = None

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.startingpos = pos


    def hoomin_dance(self):
        if self.pos is self.startingpos:
            next_moves = self.model.grid.get_neighborhood(self.pos, False, True)
            next_move = self.random.choice(next_moves)
            self.model.grid.move_agent(self, next_move)
        else:
            self.model.grid.move_agent(self, self.startingpos)


class Hoomin(GenericHoomin):
    ROADHOOMIN = 1
    FLIRTHOOMIN = 2
    BUYHOOMIN = 3
    RESTHOOMIN = 4
    WORKHOOMIN = 5

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)
        self.modes = (Hoomin.ROADHOOMIN,
                      Hoomin.FLIRTHOOMIN,
                      Hoomin.BUYHOOMIN,
                      Hoomin.RESTHOOMIN,
                      Hoomin.WORKHOOMIN)

        self.mode = Hoomin.ROADHOOMIN
        self.dst = None



    #checks the new destination for bounds and sets it as this hooman's destination
    def setdst(self, newdst):
        if newdst[0] < 0 or newdst[0] > self.model.width:
            return False
        if newdst[1] < 0 or newdst[1] > self.model.height:
            return False

        self.dst = np.array(newdst)
        return True


    #searches for the nearest road tile and returns it
    def find_nearest_road(self):
        start = np.array(self.pos)
        road = None
        counter = 0
        searchwidth = 3
        mod = np.array((0,-1))
        while searchwidth < self.model.width:
            pstart = start + 1
            for x in range(4):
                for y in range(searchwidth):
                    cells = self.model.get_cell_list_contents([pstart])
                    for item in cells:
                        if type(item) is Road:
                            return item
                    pstart += mod
                mod = np.array((mod[1], -1*mod[0]))

        return None

    #walks in a straight path to the hoomin's destination, ignoring roads.
    def straightwalk_to_dest(self):
        if self.dst is None:
            return

        tovect = np.array((np.sign(self.dst[0] - self.pos[0])
                           ,np.sign(self.dst[1] - self.pos[1])))
        if tovect is not np.array((0,0)):
            self.model.grid.move_agent(self, tuple(self.pos + tovect))

    #moves to the nearest road and randomly moves around it
    def random_road(self):
        True

    def step(self):
        if self.mode is Hoomin.ROADHOOMIN:
            self.random_road()

    def set_mode(self, mode):
        if mode in self.modes:
            self.mode = mode

    def get_mode(self):
        return self.mode


class MeetHoomin(Hoomin):

    def __init__(self, unique_id, pos, model, meettarget):
        super().__init__(unique_id, pos, model)

        self.dst = np.array(meettarget)

    def step(self):
        self.straightwalk_to_dest()

class Road(Agent):
    '''
    A road tile. Roads do nothing on their own, but hoomins can
    interact with them in various ways (mainly following them
    between locations)
    '''
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)

    def step(self):
        True

