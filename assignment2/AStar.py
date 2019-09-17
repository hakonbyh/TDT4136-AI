from assignment2.Map import Map_Obj, Node

"""Returns a list of tuples as a path from the given start to the given end in the given maze"""
def astar(map):
    """
    :param map:
    :return path:
    """

    """map.open_list is nonempty by default, because it is initialized in Map with the starter_node"""

    # Loop until empty list
    while len(map.open_list) > 0:

        # Pop current off open list and store in the current node
        current_node = map.open_list.pop(0)

        # Add node to closed list
        map.closed_list.append(current_node)

        # Check if the goal is found
        if current_node.position == map.end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            return path[::-1] # Returns reversed path

        current_node.children = generate_children(current_node, map) # see method

        # Loop through children
        for child in current_node.children:
            # check if child is unvisited
            if child not in map.closed_list and child not in map.open_list:
                attach_and_eval(child, current_node, map)
                map.open_list.append(child)
            # else (child has been visited,) checks if new path is cheaper
            elif current_node.g + child.h < child.g:
                attach_and_eval(child, current_node, map) # see method
                if child in map.closed_list:
                    propogate_path_improvements(child) # finds best parent


"""Generarates valid children with induvidual costs"""
def generate_children(current_node, map):
    """
    :param current_node:
    :param map:
    :return children:
    """
    maze = map.int_map

    # Generate children
    children = []
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Neighbour squares

        # Get node position
        node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

        # Make sure within range
        if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
            continue

        # Make sure walkable terrain
        if maze[node_position[0]][node_position[1]] == -1:
            continue

        # Create new node
        new_node = Node(current_node, node_position, cost=map.get_cell_value(node_position))

        # Append
        children.append(new_node)

    return children

# attaches child to parent, and reevaluate, g, h, and f value
def attach_and_eval(child, parent, map):
    """
    :param child:
    :param parent:
    :param map:
    :return:
    """
    child.parent = parent # attach  child to parent
    # Create the f, g, and h values
    child.g = parent.g + child.cost
    child.h = (abs(child.position[0] - map.end_node.position[0])) + abs(child.position[1] - map.end_node.position[1]) #Manhattan Distance
    child.f = child.g + child.h

# insures that all nodes in the search graph
# are aware of their current best parent through recursion
def propogate_path_improvements(node):
    """
    :param node:
    :return:
    """
    for child in node.children:
        if node.g + child.cost < child.g:
            child.parent = node
            child.g = node.g + child.cost
            propogate_path_improvements(child)

def main():
    #  for task 1-4:
    for i in range(1,5):
        map= Map_Obj(task=i) #  instantiate a map
        path = astar(map) #  calculate the path
        for p in path[1:len(path)-1]:  # add path to map
            map.set_cell_value(p, ' P ')
        map.show_map() #print path


if __name__ == '__main__':
    main()