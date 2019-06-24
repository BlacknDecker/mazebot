from pprint import pprint

import networkx as nx

from mazebot.connection_manager import ConnectionManager
from mazebot.maze_rederer import MazeRenderer


class MazeBot:
    cm = None

    def __init__(self):
        self.cm = ConnectionManager("https://api.noopschallenge.com")

    def solve_random_maze(self, dimension):
        maze_dict = self.get_random_maze(dimension)
        result, path, directions = self.solve(maze_dict)
        self.print_maze_statistics(maze_dict, result, directions)
        #TODO: render
        maze_dim = self.get_maze_dim(maze_dict['name'])
        mr = MazeRenderer(600, maze_dim, maze_dict['name'])
        mr.render_maze(maze_dict['map'])
        mr.render_solution(path)
        mr.show()

    def race(self):
        ## Login ##
        log_status = self.cm.post_data(path="/mazebot/race/start", data={"login": "BlacknDecker"})
        if log_status['message'] != "Start your engines!":
            print("LOGIN FAILED:\n")
            pprint(log_status)
            return
        ## Start Race ##
        print("=== RACE START ===\n")
        challenge_list = []
        maze_dict = self.cm.make_request(path=log_status['nextMaze'])
        while True:
            result, path , directions= self.solve(maze_dict)    # SOLVE
            print('.')
            challenge_list.append({"name": maze_dict['name'], "result": result})  # Save info
            if "nextMaze" not in result:                # Race END
                pprint(result)
                break
            else:
                maze_dict = self.cm.make_request(path=result['nextMaze'])
        print("\n=== RACE END ===\n")
        #pprint(challenge_list)


    def print_maze_statistics(self, maze_dict, result, directions):
        # Show
        print("=== {} ===\n".format(maze_dict['name']).upper())
        print("Solution: {}\n".format(directions))
        print("Result: {}".format(result['result']).upper())
        print("Message: {}".format((result['message'])))
        print("==================")

    def get_random_maze(self, dimension):
        return self.cm.make_request(path="/mazebot/random", parameters={"minSize": dimension, "maxSize": dimension})

    def solve(self, maze_dict):
        maze_dim = self.get_maze_dim(maze_dict['name'])
        maze_graph = self.setup_maze_graph(maze_dict, maze_dim)
        path = self.find_shortest_path(maze_dict, maze_graph)
        directions = self.nodespath_to_directions(path)
        result = self.cm.post_data(path=maze_dict['mazePath'], data={"directions": "".join(directions)})
        return result, path, directions

    def get_maze_dim(self, maze_name):
        return int(maze_name.split('(')[1].split('x')[0])

    def setup_maze_graph(self, maze_dict, maze_dim):
        G = nx.Graph()
        maze = maze_dict['map']
        ### ADD NODES ###
        for i in range(maze_dim):
            for j in range(maze_dim):
                if maze[i][j] != 'X':
                    G.add_node((i, j))
        ### ADD EDGES ###
        for node in G.nodes:
            self.add_edges(G, node, maze_dim)
        return G

    def add_edges(self, graph, node, maze_dimension):
        nodes = graph.nodes()
        # NORD
        if node[0] > 0:
            to_check = (node[0]-1, node[1])
            if to_check in nodes:
                graph.add_edge(node, to_check)
        # SUD
        if node[0] < maze_dimension:
            to_check = (node[0]+1, node[1])
            if to_check in nodes:
                graph.add_edge(node, to_check)
        # OVEST
        if node[1] > 0:
            to_check = (node[0], node[1]-1)
            if to_check in nodes:
                graph.add_edge(node, to_check)
        # EST
        if node[1] < maze_dimension:
            to_check = (node[0], node[1]+1)
            if to_check in nodes:
                graph.add_edge(node, to_check)

    def find_shortest_path(self, maze_dict, maze_graph):
        start_cell = (maze_dict['startingPosition'][1], maze_dict['startingPosition'][0])
        end_cell = (maze_dict['endingPosition'][1], maze_dict['endingPosition'][0])
        path = nx.shortest_path(maze_graph, source=start_cell, target=end_cell)
        return path

    def nodespath_to_directions(self, node_list):
        directions = []
        for i in range(len(node_list) - 1):
            directions.append(self.get_direction(node_list[i], node_list[i+1]))
        return directions

    def get_direction(self, node, next_node):
        if node[0] == next_node[0]:             # Est/WEST
            if node[1] > next_node[1]:
                return "W"
            else:
                return "E"
        else:
            if node[0] > next_node[0]:  # S/N
                return "N"
            else:
                return "S"


mb = MazeBot()
mb.solve_random_maze(200)
#mb.race()
