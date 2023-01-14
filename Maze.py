# MAIN FUNCTION
def find_path(file, start_tile="S", end_tile="E", step_tile=".", door_tile="D", obs_tile="#", step_score=1, door_score=2):
    import queue

    # turn the txt into a matrix
    def creat_maze(path):
        try:
            file = open(path, "r")
        except FileNotFoundError:
            return "File not found"
        else:
            read = file.readlines()
            my_maze = []
            for line in read:
                if line != "\n":
                    my_maze.append(list(line.strip()))
            return my_maze

    # Create a graph from the matrix and handle errors
    def creat_graph(my_maze):
        walkables = [start_tile, end_tile, step_tile, door_tile]
        start_count = 0
        end_count = 0
        my_graph = []
        for y in range(len(my_maze) - 1):
            for x in range(len(my_maze[y]) - 1):
                if my_maze[y][x] in walkables:
                    if my_maze[y][x] == start_tile:
                        start_count += 1
                    elif my_maze[y][x] == end_tile:
                        end_count += 1
                    if my_maze[y + 1][x] in walkables:
                        my_graph.append(((x, y), (x, y+1)))
                    if my_maze[y][x + 1] in walkables:
                        my_graph.append(((x, y), (x + 1, y)))
        for y in range(len(my_maze) - 1):
            if my_maze[y][-1] in walkables:
                if my_maze[y][-1] == start_tile:
                    start_count += 1
                elif my_maze[y][-1] == end_tile:
                    end_count += 1
                if my_maze[y + 1][-1] in walkables:
                    my_graph.append(((len(my_maze[0]) - 1, y), (len(my_maze[0]) - 1, y + 1)))
        for x in range(len(my_maze[-1]) - 1):
            if my_maze[-1][x] in walkables:
                if my_maze[-1][x] == start_tile:
                    start_count += 1
                elif my_maze[-1][x] == end_tile:
                    end_count += 1
                if my_maze[-1][x + 1] in walkables:
                    my_graph.append(((x, len(my_maze) - 1), (x + 1, len(my_maze) - 1)))
        if start_count == 0 and end_count == 0:
            return "THERE IS NO START NOR END! (ᕗ🔥益🔥)ᕗ︵┻━┻"
        elif start_count == 0:
            return "THERE IS NO START! (ᕗ🔥益🔥)ᕗ︵┻━┻"
        elif end_count == 0:
            return "THERE IS NO END! (ᕗ🔥益🔥)ᕗ︵┻━┻"
        elif start_count > 1:
            return f"Can't solve for {start_count} starts! ¯\_(°_｣°)_/¯"
        elif end_count > 1:
            return f"Can't solve for {end_count} ends! ¯\_(°_｣°)_/¯"
        else:
            return my_graph

    # Get start coordinates
    def find_start(my_graph, my_maze):
        for connection in my_graph:
            for tile in connection:
                if my_maze[tile[1]][tile[0]] == start_tile:
                    return tile

    #check if last coordinates are end
    def find_end(my_path, my_maze):
        if my_maze[my_path[-2][1]][my_path[-2][0]] == end_tile:
            return True
        else:
            return False

    # find connected nodes with the last step and calculate score of path
    def draw_paths(my_path, my_graph, my_maze, my_queue):
        last_step = my_path[-2]
        for edge in my_graph:
            if last_step in edge:
                for i in range(2):
                    if edge[i] != last_step:
                        connection = edge[i]
                        if not (connection in my_path):
                            new_path = my_path.copy()
                            add_score = 0
                            if my_maze[connection[1]][connection[0]] == step_tile:
                                add_score = step_score
                            elif my_maze[connection[1]][connection[0]] == door_tile:
                                add_score = door_score
                            new_path.insert(-1, connection)
                            new_path[-1] += add_score
                            my_queue.put(new_path)
        return my_queue

    # loop through the maze and reprint it solved
    def print_maze(my_maze, my_path):
        for y in range(len(my_maze)):
            for x, tile in enumerate(my_maze[y]):
                if (x, y) in my_path:
                    if my_maze[y][x] == step_tile:
                        step_before = my_path[my_path.index((x, y)) - 1]
                        step_after = my_path[my_path.index((x, y)) + 1]
                        up = (x, y-1)
                        down = (x, y+1)
                        left = (x-1, y)
                        right = (x+1, y)
                        if step_before == down:
                            if step_after == up:
                                print("↑ ", end="")
                            elif step_after == right:
                                print("↱ ", end="")
                            elif step_after == left:
                                print("↰ ", end="")

                        elif step_before == up:
                            if step_after == down:
                                print("↓ ", end="")
                            elif step_after == right:
                                print("↳ ", end="")
                            elif step_after == left:
                                print("↲ ", end="")

                        elif step_before == left:
                            if step_after == right:
                                print("→ ", end="")
                            elif step_after == up:
                                print("⬏ ", end="")
                            elif step_after == down:
                                print("⬎ ", end="")

                        elif step_before == right:
                            if step_after == left:
                                print("← ", end="")
                            elif step_after == up:
                                print("⬑ ", end="")
                            elif step_after == down:
                                print("⬐ ", end="")
                    elif my_maze[y][x] == end_tile:
                        print("🏁", end="")
                    elif my_maze[y][x] == start_tile:
                        print("🚩", end="")

                    elif my_maze[y][x] == door_tile:
                        print("🚪", end="")
                    else:
                        print(tile + " ", end="")
                else:
                    if my_maze[y][x] == obs_tile:
                        print("# ", end="")
                    elif my_maze[y][x] == step_tile:
                        print("  ", end="")
                    else:
                        print(tile + " ", end="")
            print()


    # MAIN ALGO
    maze = creat_maze(file)
    if isinstance(maze, str):
        print(maze)
    else:
        graph = creat_graph(maze)
        if isinstance(graph, str):
            print(graph)
        else:
            end_paths = {}
            start = find_start(graph, maze)
            paths_queue = queue.Queue()
            paths_queue.put([start, 0])
            while paths_queue.qsize() != 0:
                add = paths_queue.get()
                if find_end(add, maze):
                    end_paths[tuple(add[:-1])] = add[-1]
                else:
                    draw_paths(add, graph, maze, paths_queue)

            if len(end_paths) == 0:
                print("NO SOLUTION! (ᕗ🔥益🔥)ᕗ︵┻━┻")
            else:
                shortest_path = min(end_paths, key=end_paths.get)
                output = f"x{start[0]}y{start[1]}"
                for step in shortest_path[1:]:
                    output += f"-x{step[0]}y{step[1]}"
                print(output)
                print(f"It takes {end_paths[shortest_path]} actions.")
                print_maze(maze, shortest_path)


file = input("File path: ")
find_path(file)








