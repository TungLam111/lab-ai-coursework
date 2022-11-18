import time

class Square:
    def __init__(self, height, width, color, number, x0, y0) -> None:
        self.height = height 
        self.width = width 
        self.color = color 
        self.number = number 
        self.x0 = x0
        self.y0 = y0
    def change_color(self, new_color):
        self.color = new_color


def process_input_file(file_path):
    """
    Processes the input file and returns a list of lines.
    Return :
    count_node : The size of maze.
    end_node : The ending node of the graph.
    adjacency_list : The adjacency list of the graph.
    """
    data = []
    with open(file_path, 'r') as f:
        data = f.readlines()
    
    for i in range(len(data)-1):
        data[i] = data[i][:-1].split(' ')
        #print(data[i])
        if len(data[i]) == 1 and data[i][0] == '':
            data[i] = []
        else:
           for j in range(len(data[i])):
               data[i][j] = int(data[i][j])

    
    return data[0][0], int(data[len(data)-1]), data[1:len(data)-1]
        
def export_to_output_file(file_path, output_list):
    """
    Exports the output list to the output file.
    """    
    with open(file_path, 'w') as f:
        for line in output_list:
            f.write(line)

def prepare_input():
    """
    Returns vital inputs for algorithm.
    start_node : The starting node of the graph.
    end_node : The ending node of the graph.
    adjacency_matrix : The adjacency matrix of the graph.
    """
    size_maze, end_node, adjacency_list = process_input_file('./INPUT/input_3.txt')
    return 0, end_node, adjacency_list, size_maze

def get_least_cost_node(priority_queue: list):
    """
    Sorts in ascending order a priority queue
    """
    priority_queue.sort()
    return priority_queue

def solve_UCS_algorithm(start_node, end_node, adjacency_list, size_maze):
    visited_nodes = [] # or expanded nodes
    #start_node, end_node, adjacency_list, _ = prepare_input()
    priority_queue = []
    priority_queue.append((0, start_node)) # (cost, node)
    expandable_nodes = []
    start_t = time.time()
    while(priority_queue):
        priority_queue = get_least_cost_node(priority_queue)
        #print(priority_queue)
        min_node = priority_queue.pop(0)
        #print(min_node)
        if min_node[1] not in visited_nodes:
            
            visited_nodes.append(min_node[1])
            expandable_nodes.append(min_node)
            # condition to end loop
            if min_node[1] == end_node:
                break

            for i in sorted(adjacency_list[min_node[1]]):
                if i not in visited_nodes:
                    priority_queue.append((min_node[0] + 1, i))
    end_t = time.time()
    time_run = end_t - start_t
    return visited_nodes, expandable_nodes, time_run

def get_coordinate_of_node(count_node, size_maze, coordinate_goal):
    """
    Create list of manhantan values of each square in maze
    """
    return [manhantan((i // size_maze, i % size_maze), coordinate_goal) for i in range(count_node)]

def manhantan(coordinate_start, coordinate_end):
    """
    Return manhantan value |x1 - x2| + |y1 - y2| 
    """
    return abs(coordinate_start[0] - coordinate_end[0]) + abs(coordinate_start[1] - coordinate_end[1])

def transform_to_manhantan(priority_queue: list, manhantans):
    """
    Given a queue and manhantans of each node, add each manhantan value to each node
    """
    manhantan_priority_queue = priority_queue.copy()
    for i in range(len(manhantan_priority_queue)):
        manhantan_priority_queue[i] = (manhantan_priority_queue[i][0] + manhantans[manhantan_priority_queue[i][1]], manhantan_priority_queue[i][1])
    return manhantan_priority_queue

def remove_min_node(manhantan_min_node, priority_queue):
    """
    
    """
    min_node = None
    for i in range(len(priority_queue)):
        if priority_queue[i][1] == manhantan_min_node[1]:
            min_node = priority_queue[i]
            priority_queue.pop(i)
            break
    return priority_queue, min_node

def solve_A_star_algorithm(start_node, end_node, adjacency_list, size_maze):
    visited_nodes = [] # or expanded nodes
    #start_node, end_node, adjacency_list, size_maze = prepare_input()
    priority_queue = []
    priority_queue.append((0, start_node)) # (cost, node)
    expandable_nodes = []
    manhantans = get_coordinate_of_node( size_maze * size_maze ,size_maze, (end_node // size_maze, end_node % size_maze))

    assert len(adjacency_list) == len(manhantans)
    start_t = time.time()
    while(priority_queue):
        #print("Priority queue {}".format(priority_queue))
        manhantan_priority_queue = transform_to_manhantan(priority_queue, manhantans)
        assert id(priority_queue) != id(manhantan_priority_queue)

        #print("Manhantan queue {}".format(manhantan_priority_queue))
        manhantan_priority_queue = get_least_cost_node(manhantan_priority_queue)
        #print("Manhantan queue sorted {}".format(manhantan_priority_queue))
        manhantan_min_node = manhantan_priority_queue.pop(0)
        #print("Manhantan min node {}".format(manhantan_min_node))
        priority_queue, min_node = remove_min_node(manhantan_min_node, priority_queue)
        #print("pop priority queue {}, min_node {}".format(priority_queue, min_node))

        if min_node[1] not in visited_nodes:
            
            visited_nodes.append(min_node[1])
            expandable_nodes.append(min_node)
            # condition to end loop
            if min_node[1] == end_node:
                break

            for i in sorted(adjacency_list[min_node[1]]):
                if i not in visited_nodes:
                    priority_queue.append((min_node[0] + 1, i))
    end_t = time.time()
    return visited_nodes, expandable_nodes, end_t - start_t

def solve_DFS(start_node, end_node, adjacency_list, size_maze, current_depth): # dfs
    visited_nodes = [] # or expanded nodes
    stack = [] # first in last out
    stack.append((0, start_node)) # (cost, node)
    expandable_node = []

    while stack:
        cost, current_node = stack.pop(len(stack) - 1)
        
        if current_node not in visited_nodes:
            visited_nodes.append(current_node)
            expandable_node.append((cost, current_node))
            
            if current_node == end_node and cost == current_depth:
                return True, visited_nodes, expandable_node

            neighbor = adjacency_list[current_node].copy()
            neighbor.sort()

            for neigh in neighbor:
                if neigh not in visited_nodes:
                    stack.append((cost + 1, neigh))
    
    return False, None, None
def solve_iterative_deepening_search(start_node, end_node, adjacency_list, size_maze,max_depth = 48):
    #start_node, end_node, adjacency_list, size_maze = prepare_input()
    start_t = time.time()
    for i in range(max_depth):
        check, visited_nodes, expandable_node = solve_DFS(start_node, end_node, adjacency_list, size_maze, i)
        if check == True:
            end_t = time.time()
            return visited_nodes, expandable_node, end_t - start_t
    
    return None, None, time.time() - start_t
def solve_greedy_best_first_search(start_node, end_node, adjacency_list, size_maze):
    
    visited_nodes = [] # or expanded nodes
    #start_node, end_node, adjacency_list,size_maze = prepare_input()
    manhantans = get_coordinate_of_node( size_maze * size_maze ,size_maze, (end_node // size_maze, end_node % size_maze))
    priority_queue = []
    priority_queue.append((manhantans[start_node], start_node)) # (cost, node)
    expandable_nodes = []
    start_t = time.time()
    while(priority_queue):
        priority_queue = get_least_cost_node(priority_queue)
        #print(priority_queue)
        min_node = priority_queue.pop(0)
        #print(min_node)
        if min_node[1] not in visited_nodes:
            
            visited_nodes.append(min_node[1])
            expandable_nodes.append(min_node)
            # condition to end loop
            if min_node[1] == end_node:
                break

            for i in sorted(adjacency_list[min_node[1]]):
                if i not in visited_nodes:
                    priority_queue.append((manhantans[i], i))
    end_t = time.time()
    return visited_nodes, expandable_nodes, end_t - start_t

def print_result(visited_nodes , expandable_nodes, adjacency_list, time_run, is_greedy=False):
    assert len(visited_nodes) == len(expandable_nodes)
    
    path = [expandable_nodes[len(expandable_nodes)-1]]
    min_node = path[len(path)-1]

    while True:
        _, node = min_node
        neighbor = adjacency_list[node]  # [a, b, c, d, ...]
        pairs = []
        for neigh in neighbor:
            for value in expandable_nodes:
                if value[1] == neigh and value not in path:
                    pairs.append(value)
                    break
        pairs.sort()
        if not is_greedy:
            path.append(pairs[0])
            min_node = path[len(path)-1]
        else:
            path.append(pairs[len(pairs) - 1])
            min_node = path[len(path)-1]          
        if min_node == expandable_nodes[0]:
            break
    
    #if not is_greedy:
    #    path.sort()
    path = [val[1] for val in path]
    print("Expanded nodes : {}".format(visited_nodes))
    print("Path : {}".format(path[::-1]))
    print("Cost : {}".format(len(path)-1))
    print("Time run : {}".format(time_run))
    return visited_nodes, path[::-1], len(path)-1
     