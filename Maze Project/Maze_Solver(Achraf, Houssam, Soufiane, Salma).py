def solve_maze(file_path, start_tile="S", end_tile="E", step_tile=".", door_tile="D", obs_tile="#", step_score=1, door_score=2):

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
                my_maze.append(list(line.strip()))
            return my_maze


    def shortest_path(my_maze):
        import heapq

        # Create the graph from the maze
        graph = {}
        my_start = ()
        end = ()
        start_counter = 0
        end_counter = 0
        for i in range(len(my_maze)):
            for j in range(len(my_maze[i])):
                if my_maze[i][j] == start_tile:
                    my_start = (i, j)
                    start_counter += 1

                if my_maze[i][j] == end_tile:
                    end = (i, j)
                    end_counter += 1

                if my_maze[i][j] != obs_tile:
                    graph[(i, j)] = []
                    if i > 0 and my_maze[i - 1][j] != obs_tile:
                        graph[(i, j)].append((i - 1, j))
                    if j > 0 and my_maze[i][j - 1] != obs_tile:
                        graph[(i, j)].append((i, j - 1))
                    if i < len(my_maze) - 1 and my_maze[i + 1][j] != obs_tile:
                        graph[(i, j)].append((i + 1, j))
                    if j < len(my_maze[i]) - 1 and my_maze[i][j + 1] != obs_tile:
                        graph[(i, j)].append((i, j + 1))

        if len(my_start) == 0:
            return "THERE IS NO START! (ᕗ🔥益🔥)ᕗ︵┻━┻", None
        if len(end) == 0:
            return "THERE IS NO END! (ᕗ🔥益🔥)ᕗ︵┻━┻", None
        if start_counter > 1:
            return f"Can't solve for {start_counter} starts! ¯\_(°_｣°)_/¯", None
        if end_counter > 1:
            return f"Can't solve for {end_counter} ends! ¯\_(°_｣°)_/¯", None

        # Initialize the priority queue and visited set
        queue = [(0, [my_start])]
        visited = set()

        # MAIN ALGO
        while queue:
            curr_cost, curr_path = heapq.heappop(queue)
            curr_node = curr_path[-1]
            if curr_node in visited:
                continue
            visited.add(curr_node)
            if curr_node == end:
                return (curr_cost, curr_path), my_start
            for neighbor in graph[curr_node]:
                if neighbor not in visited:
                    if my_maze[neighbor[0]][neighbor[1]] == step_tile:
                        heapq.heappush(queue, (curr_cost + step_score, curr_path + [neighbor]))

                    elif my_maze[neighbor[0]][neighbor[1]] == door_tile:
                        heapq.heappush(queue, (curr_cost + door_score, curr_path + [neighbor]))

                    else:
                        heapq.heappush(queue, (curr_cost, curr_path + [neighbor]))

        return "NO SOLUTION! (ᕗ🔥益🔥)ᕗ︵┻━┻", None


    def setup_maze(my_maze, my_path):
        import turtle

        wn = turtle.Screen()
        wn.bgcolor("black")
        wn.title("maze")
        wn.setup(800, 800)

        class Wall_Pen(turtle.Turtle):
            def __init__(self):
                turtle.Turtle.__init__(self)
                self.hideturtle()
                self.shape("square")
                self.color("white")
                self.penup()
                self.speed(0)

        class Start_Pen(turtle.Turtle):
            def __init__(self):
                turtle.Turtle.__init__(self)
                self.hideturtle()
                self.left(90)
                self.shape("triangle")
                self.color("#32CD32")
                self.penup()
                self.hideturtle()
                self.speed(0)
        class Turtle_pen(turtle.Turtle):
            def __init__(self):
                turtle.Turtle.__init__(self)
                self.hideturtle()
                self.left(90)
                self.shape("turtle")
                self.color("red")
                self.penup()
                self.speed(1)

        class End_Pen(turtle.Turtle):
            def __init__(self):
                turtle.Turtle.__init__(self)
                self.hideturtle()
                self.left(90)
                self.shape("triangle")
                self.color("#0000CD")
                self.penup()
                self.speed(0)

        class Door_Pen(turtle.Turtle):
            def __init__(self):
                turtle.Turtle.__init__(self)
                self.hideturtle()
                self.shape("circle")
                self.color("#6495ED")
                self.penup()
                self.speed(0)

        class Step_Pen(turtle.Turtle):
            def __init__(self):
                turtle.Turtle.__init__(self)
                self.hideturtle()
                self.left(90)
                self.color("#8B4513")
                self.penup()
                self.speed(0)

        wall_pen = Wall_Pen()
        turt_pen = Turtle_pen()
        end_pen = End_Pen()
        start_pen = Start_Pen()
        door_pen = Door_Pen()
        step_pen = Step_Pen()
        for y in range(len(my_maze)):
            for x in range(len(my_maze[y])):
                character = my_maze[y][x]
                screen_x = -360 + (x * 22)
                screen_y = 360 - (y * 22)
                if character == obs_tile:
                    wall_pen.goto(screen_x, screen_y)
                    wall_pen.stamp()
                    wall_pen.showturtle()

                elif character == start_tile:
                    start_pen.goto(screen_x, screen_y)
                    start_pen.stamp()
                    start_pen.showturtle()

                elif character == end_tile:
                    end_pen.goto(screen_x, screen_y)
                    end_pen.stamp()
                    end_pen.showturtle()

                elif character == door_tile:
                    door_pen.goto(screen_x, screen_y)
                    door_pen.stamp()
                    door_pen.showturtle()

                elif character == step_tile:
                    step_pen.goto(screen_x, screen_y)
                    step_pen.stamp()
                    step_pen.showturtle()

        for node in my_path:
            y = node[0]
            x = node[1]
            screen_x = -360 + (x * 22)
            screen_y = 360 - (y * 22)
            turt_pen.goto(screen_x, screen_y)
            turt_pen.pendown()
            turt_pen.showturtle()


    maze = creat_maze(file_path)

    if isinstance(maze, str):
        print(maze)
    else:
        solution, start = shortest_path(maze)
        if isinstance(solution, str):
            print(solution)
        else:
            output = f"x{start[1]}y{start[0]}"
            for node in solution[1][1:]:
                output += f"-x{node[1]}y{node[0]}"
            print(output + "\n")
            print(f"It takes {solution[0]} actions")

            permission = input("Whould you like to print the maze? (could take some time) type 1 for yes and 0 for no: ")
            while not (permission == "0" or permission == "1"):
                permission = input("Whould you like to print the maze? (could take some time) type 1 for yes and 0 for no: ")
            if permission == "1":
                setup_maze(maze, solution[1])
                while True:
                    pass



file = input("File path: ")
solve_maze(file)

