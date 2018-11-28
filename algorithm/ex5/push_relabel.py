import numpy
from IOHelper import IOHelper


class PushRelabel:
    def __init__(self, cap_mat):
        self.capicity_mat = numpy.asarray(cap_mat)  # a map restore the capacity of every edge
        self.n = len(cap_mat)  # nodes amount
        self.f_G = numpy.zeros((self.n, self.n))  # flow,  restore the max flow
        self.h_level = [0] * self.n  # restore level for every node
        self.h_level[0] = self.n  # initial the level of source node s

        ## f(e) = C(e) for all e = (s, u);
        for i in range(1, self.n - 1):
            self.f_G[0][i] = self.capicity_mat[0][i]

    def get_residual_edge(self, u, v):
        cap = self.capicity_mat[u][v]
        residual = [0, 0]
        if cap == 0:
            cap = self.capicity_mat[v][u]
            forward = self.f_G[v][u]
            backward = cap - forward
            residual = [forward, backward]
            return residual
        else:
            forward = cap - self.f_G[u][v]
            backward = self.f_G[u][v]
            residual = [forward, backward]
            return residual

    """
    compute excess of node v : e = f_in - f_out
    @:param     v : node index
    @:return    excess of node v
    """

    def compute_E(self, v):
        f_in = sum(self.f_G[:, v])
        f_out = sum(self.f_G[v, :])
        return f_in - f_out

    """
    judge whether exist node has excess
    @:return v : the first node found has excess
    """

    def exist_excess(self):
        for i in range(1, self.n - 1):
            e = self.compute_E(i);
            if e > 0:
                return i

        return 0

    """
    find exist an edge (v,w) where (v,w)>0 or (w,v)>0
    @:param v : index of one end point
    @:return w : index of another end point index
    """

    def exist_edge_st_level(self, v):
        for i in range(self.n):
            if i == v:
                continue
            else:
                resdual = self.get_residual_edge(v, i)
                v_level = self.h_level[v]
                i_level = self.h_level[i]
                if resdual[0] > 0 and v_level > i_level:
                    return i
        return -1

    """
    relabel v
    @:param v : node index
    """

    def relabel(self, v):
        self.h_level[v] = self.h_level[v] + 1

    """
    call thie method to compute push-relabel algorithm
    @:return the max flow map
    """

    def push_relabel(self):
        v = self.exist_excess()
        while v > 0 and v < self.n - 1:
            w = self.exist_edge_st_level(v)
            if w < 0:
                self.relabel(v)
            else:
                forward = self.is_forward_edge(v, w)

                residual = self.get_residual_edge(v, w)
                Ef = self.compute_E(v)
                bottleneck = min(Ef, residual[0])

                if forward:
                    self.f_G[v][w] += bottleneck
                else:
                    self.f_G[w][v] -= bottleneck
            v = self.exist_excess()

        return self.f_G

    def is_forward_edge(self, v, w):
        vw_cap = self.capicity_mat[v][w]
        if vw_cap > 0:
            return True
        else:
            return False


def build_matrix_map_from_data(data):
    row = data[0]
    col = data[1]
    n = row.__len__() + col.__len__() + 2
    map = numpy.zeros((n, n))
    for i in range(len(row)):
        map[0][i + 1] = row[i]
        for j in range(len(col)):
            map[i + 1][len(row) + j + 1] = 1
    for i in range(len(col)):
        map[len(row) + i + 1][n - 1] = col[i]
    return map


if __name__ == '__main__':
    file = "problem2.data"
    io = IOHelper(file)
    data = io.get_next_data()
    while data:
        row = len(data[0])
        col = len(data[1])
        map = build_matrix_map_from_data(data)
        pr = PushRelabel(map)
        max_flow = pr.push_relabel()
        [m, n] = max_flow.shape
        mat = max_flow[1:row + 1, row + 1:n - 1]
        print("matrix as follow:")
        print(mat)
        data = io.get_next_data()
