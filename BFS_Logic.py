import sys

import Data_Structures as DS


class BFS:
    def shortestPath(self, matrix, start, end):
        """
        Finds the shortest path between two points on a matrix using breadth-first search (BFS).

        Parameters:
        - matrix (list of lists): The matrix/grid where each cell is represented by a value from Val_dict.
        - start (tuple): A tuple containing the coordinates (x, y) of the starting point.
        - end (tuple): A tuple containing the coordinates (x, y) of the destination point.

        Returns:
        - list or None: A list of Cell objects representing the shortest path from start to end, or None if no path exists.
        """
        sx = start.X()
        sy = start.Y()
        dx = end.X()
        dy = end.Y()

        # initialize the cells
        m = len(matrix)
        n = len(matrix[0])
        cells = []
        for i in range(0, m):
            row = []
            for j in range(0, n):
                if (matrix[i][j] == DS.Val_dict.EMPTY or matrix[i][j] == DS.Val_dict.PARKING_SLOT or
                        matrix[i][j] == 255 or matrix[i][j] == DS.Val_dict.CAR or DS.Val_dict.BFS_ROAD):
                    row.append(DS.Cell(i, j, sys.maxsize, None))
                else:
                    row.append(None)
            cells.append(row)
            # breadth first search

        queue = []
        src = cells[int(sx)][int(sy)]
        src.dist = 0
        queue.append(src)
        dest = None
        p = queue.pop(0)
        while p is not None:
            # find destination
            if p.x == dx and p.y == dy:
                dest = p
                break

            # moving up
            BFS.visit(cells, queue, p.x - 1, p.y, p)
            # moving left
            BFS.visit(cells, queue, p.x, p.y - 1, p)
            # moving down
            BFS.visit(cells, queue, p.x + 1, p.y, p)
            # moving right
            BFS.visit(cells, queue, p.x, p.y + 1, p)
            if len(queue) > 0:
                p = queue.pop(0)
            else:
                p = None

        # compose the path if path exists
        if dest is None:
            print("there is no path")
            return
        else:
            path = []
            p = dest
            while p is not None:
                path.insert(0, p)
                p = p.prev
            print("\nshortestPath - OUT\n\n")
            return path

    # function to update cell visiting status, Time O(1), Space O(1)

    @staticmethod
    def visit(cells, queue, x, y, parent):
        # out of boundary
        if x < 0 or x >= len(cells) or y < 0 or y >= len(cells[0]) or cells[x][y] == None:
            return
        # update distance, and previous node
        dist = parent.dist + 1
        p = cells[x][y]
        if dist < p.dist:
            p.dist = dist
            p.prev = parent
            queue.append(p)
