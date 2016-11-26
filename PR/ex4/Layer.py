from Cell import Cell
import numpy

'''
implement the struct for each layer
'''
class Layer:
    def __init__(self, active_func, cell_amount):
        self.active_func = active_func
        self.cells = []

        for i in range(cell_amount):
            self.cells.append(Cell(active_func, 0))

    def set_net_vals_from_vec(self, val_vec):
        if len(val_vec) != len(self.cells):
            raise Exception("par amount don't meet the amount of cells")
        else:
            for i in range(len(val_vec)):
                self.cells[i].net_val = val_vec[i]

    '''
    active all cells of this layer
    '''
    def active_cells(self):
        for cell in self.cells:
            cell.active()

    def get_active_val_as_vec(self):
        vector = []
        for cell in self.cells:
            vector.append(cell.active_val)

        return numpy.asarray(vector)

    def get_net_val_as_vec(self):
        vector = []
        for cell in self.cells:
            vector.append(cell.net_val)

        return numpy.asarray(vector)
