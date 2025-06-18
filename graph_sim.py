#Graph generation
import random
import visualiser_rndgraph as vis
import matplotlib.pyplot as plt
from math import exp

# For given points

def draw_graph(matrix:list, color_info:str, update_info:list):
    '''
    Function that creates graph from given connections, chose colors for graph and optimize the graph if user chose to do it.
    
    >>>matrix = [(0, 1),(1, 2),(2, 3),(3, 0)]
    >>>color_info = "3"
    >>>update_info = ["yes", ["1", 5]]
    >>>draw_graph(matrix, color_info, update_info)'''
    # Obtain a list of the nodes from the matrix
    nodes = list(set().union(*matrix))
    
    #Ensure that the graph is connected
    if not is_connected(matrix, nodes):
        print("Graph is not connected to itself, please change it.")
        return
    
    #Check if there are only unique connections
    for connection in matrix:
        point1, point2 = connection
        if point1==point2 or [point2, point1] in matrix:
          matrix.remove(connection)
          print(f"Removed non unique connection from graph: {connection}")
  
    #Sort the nodes
    nodes.sort()

    #Create an empty dictionary and fill it based on users choice
    color_dict={}
    for i in nodes:
        color_dict[i]= None
    if color_info == "1":
        for i in color_dict:
            color_dict[i]=1.0 
    elif color_info == "2":
        for i in color_dict:
            color_dict[i] = 0.0 
    elif color_info == "3":
        for i in color_dict:
            color_dict[i] = random.choice([0.0,1.0])

    #Create the graph
    graph= vis.Visualiser(matrix, color_dict,vis_labels=True)

    #Check if user wants to optimize the graph
    if "yes" in update_info:
        optimization_choice(graph, matrix, color_dict, update_info)
    vis.Visualiser.wait_close(graph)

def is_connected(connections, nodes):
    '''Check if graph is connected. Returns True if the graph is connected.

    >>>is_connected([(0, 1),(1, 2),(2, 3),(3, 0)],[0,1,2,3])
    True
    '''
    G = {node: set() for node in nodes}
    for edge in connections:
        G[edge[0]].add(edge[1])
        G[edge[1]].add(edge[0])

    visited = set()
    stack = [next(iter(G))]

    while stack:
        node = stack.pop()
        visited.add(node)
        stack.extend(G[node] - visited)

    return len(visited) == len(nodes)

# For random points

def generate_connected_graph(num_nodes:int, color_info:str, update_info:list):
    '''Function for creating graph given random number which corresponds 
    to amount of nodes on the graph. Next this function assign a color to 
    each point and optimize the graph if user chose to do it.
    
    >>>num_nodes = 5
    >>>color_info = "3"
    >>>update_info = ["yes", ["1", 5]]
    >>>generate_connected_graph(num_nodes, color_info, update_info)
    '''
    #Create list of nodes starting from 1
    nodes=list(range(1,num_nodes + 1))
    
    #Empty list for connections
    gr_connections=[]
    
    #Empty dictionary for colors
    color_dict={}
    
    #Fill the empty dictionary with nodes but without values
    for i in range (1,num_nodes + 1):
        color_dict[i]= None
    
    #Create random number of connections
    num_connections = random.randint(1, num_nodes * (num_nodes - 1) // 2)
    
    #Make random connections between nodes
    while len(gr_connections) < num_connections:
        x = int(random.uniform(1, num_nodes + 1))
        y = int(random.uniform(1, num_nodes + 1))

        #Try again if the connections are not unique or reversed or node is connected to itself
        while x == y or [x, y] in gr_connections or [y, x] in gr_connections:
            x = int(random.uniform(1, num_nodes + 1))
            y = int(random.uniform(1, num_nodes + 1))

        gr_connections.append([x, y])

    # Ensure the generated connections form a connected graph
    while not is_connected(gr_connections, nodes):
        gr_connections = generate_connected_graph(num_nodes, color_info, update_info)
    
    
    #Fill the dictionary with values for colors based on users choice
    if color_info == "1":
        for i in color_dict:
            color_dict[i]=1.0 
    elif color_info == "2":
        for i in color_dict:
            color_dict[i]=0.0
    elif color_info == "3":
        for i in color_dict:
            color_dict[i] = random.choice([0.0,1.0])
    
    #Create the graph
    graph= vis.Visualiser(gr_connections, color_dict, vis_labels=True)
    
    #Check if user wants to optimize the graph
    if "yes" in update_info:
        optimization_choice(graph, gr_connections, color_dict, update_info)
    vis.Visualiser.wait_close(graph)

def local_frustration(connections:list, colors:dict):
    '''Function that calculate the local frustration of the graph given its connections and color of each point.
    
    >>>connections = [(0, 1),(1, 2),(2, 3),(3, 0)]
    >>>colors = {0: 0.0, 1: 0.0, 2: 0.0, 3: 1.0}
    >>>local_frustration = (connections, colors)
    {0: -1.0, 1: 1.0, 2: -1.0, 3: -1.0}
    '''
    points = colors.copy()  # Dictionary to store points for each point from list

    #Give each point a starting value based on their color
    for point in points:
        if points[point]==0.0:
            points[point] = 1
        elif points[point]== 1.0:
            points[point] = -1
    
    #Start iterating through each list and create variables
    for point in connections:
        point1, point2= point #Get the adjacent points from list in list
         
        # Get the colors of the connected points from list
        color1 = colors.get(point1)
        color2 = colors.get(point2)

        # Assign points based on the colors of their neighbors
        points[point1] = points.get(point1) * (1-(2*color2))
        points[point2] = points.get(point2) * (1-(2*color1))
    return points

def optimization_choice(graph, connections:list, color_info:dict, update_info:list):
    '''Function that based on first element of second element in update_info calls on corresponding optimization function.
    
    >>>optimization_choice(graph,[(0, 1),(1, 2),(2, 3),(3, 0)], {0: 0.0, 1: 0.0, 2: 0.0, 3: 1.0}, ['yes', ['1', 5]])
    Ordered(graph,[(0, 1),(1, 2),(2, 3),(3, 0)], {0: 0.0, 1: 0.0, 2: 0.0, 3: 1.0}, ['yes', ['1', 5]])
    '''
    if "1" in update_info[1]:
        Ordered(graph, connections, color_info, update_info)
    elif "2" in update_info[1]: 
        Max_Violation(graph, connections, color_info, update_info)
    else:
        Monte_Carlo(graph, connections, color_info, update_info)

def Ordered(graph, connections:list, color_info:dict, update_info:list):
    '''Function that optimizes the graph by changing colors of its nodes. 
    Function tries to find the best color pattern based on local and global frustration of the graph.
    It creates a list with only smaller or equal global frustrations and calls on function to plot that list. 
    
    Ordered(graph,[(0, 1),(1, 2),(2, 3),(3, 0)], {0: 0.0, 1: 0.0, 2: 0.0, 3: 1.0}, ['yes', ['1', 5]])
    '''
    perm_new_color = color_info.copy() #Copy of provided dictionary of colors
    local_fru = local_frustration(connections, color_info) #Calculate local frustration for provided connections and colors
    global_fru = sum(local_fru.values()) / 2 #Calculate global frustration
    global_storage= [global_fru] #Store it as a first value in a list
    test= 0
    num_steps= update_info[1][1] #Get the number of steps from update_info
    
    while num_steps>= test:
        for connection in connections:
            temp_new_color=perm_new_color.copy() #Copy of the colors 
            point1, point2 = connection #Get the adjacent points from list in list
            
            # Get the colors of the connected points from list
            color1=temp_new_color.get(point1)
            color2=temp_new_color.get(point2)

            #Calculate their local frustration
            local_fru1 = local_fru.get(point1)
            local_fru2 = local_fru.get(point2)

            #If its positive then start swapping colors
            if local_fru1 > 0 or local_fru2 > 0:
                if color1 == 0.0 and color2 == 0.0:
                    temp_new_color[point1] = 1.0
                    temp_new_color[point2] = 1.0
                elif color1 == 1.0 and color2 == 1.0:
                    temp_new_color[point1] = 0.0
                    temp_new_color[point2] = 0.0
                elif color1 == 0.0 and color2 == 1.0:
                    temp_new_color[point1] = 1.0
                    temp_new_color[point2] = 0.0
                else:
                    temp_new_color[point1] = 0.0
                    temp_new_color[point2] = 1.0
            
                #Calculate new local and global frustration for new colors
                local_fru= local_frustration(connections, temp_new_color)
                global_fru= sum(local_fru.values()) / 2
            
                #If global frustration is equal or smaller then the previous one assign it to the list
                if global_fru<=global_storage[-1]:
                    global_storage.append(global_fru)
                    perm_new_color[point1]= temp_new_color[point1]
                    perm_new_color[point2]= temp_new_color[point2]
            
                    #Update the graph with new colors
                    vis.Visualiser.update(graph,val_map=perm_new_color)
        test+=1
    
    #Fill the global frustration list if the len of it is smaller then the number of steps
    while len(global_storage) <= num_steps:
        global_storage.append(global_storage[-1])
    #Plot the graph for global frustration
    plotting(global_storage)

def Max_Violation(graph, connections:list, color_info:dict, update_info:list):
    '''Function that optimizes the graph by changing colors of its nodes. 
    Function tries to find the best color pattern based on largest value of a point and swapping its color.
    It creates a list with only smaller or equal global frustrations and calls on function to plot that list.
    
    >>>Max_Violation(graph,[(0, 1),(1, 2),(2, 3),(3, 0)], {0: 0.0, 1: 0.0, 2: 0.0, 3: 1.0}, ['yes', ['1', 5]])
    '''
    perm_new_color = color_info.copy() #Copy of the provided dictionary
    local_fru = local_frustration(connections, color_info) #Calculate the local frustration for provided connections and colors
    global_fru = sum(local_fru.values()) / 2 #Calculate the global frustration
    global_storage= [global_fru] #List for storing the values of global frustration
    test= 0
    num_steps= update_info[1][1] #Get the number of steps for the optimization
    
    while num_steps>= test:
        local_fru_max = max(local_fru, key= local_fru.get) #Get the key of the max value from the local frustration
        for connection in connections:
            temp_new_color=perm_new_color.copy() #Copy for temporary colors
            
            for point in connection: #Get the edge from connection
                edge = point
                
                #Check if this edge corresponds to key of the max value from local frustration
                if edge == local_fru_max:
                    color=temp_new_color.get(edge) #Get its color
                    if color == 0.0: #Swap its color
                        temp_new_color[edge] = 1.0
                    else:
                        temp_new_color[edge] = 0.0
            
                    #Calculate new local and global frustration
                    local_fru= local_frustration(connections, temp_new_color)
                    global_fru= sum(local_fru.values()) / 2
            
                #Store that global frustration if its smaller or equal to previous
                    if global_fru<=global_storage[-1]:
                        global_storage.append(global_fru)
                        perm_new_color[edge]= temp_new_color[edge]
            
                        #Update the graph with new colors
                        vis.Visualiser.update(graph,val_map=perm_new_color)
                        break
        test+=1
    
    #Fill the global frustration list if the len of it is smaller then the number of steps
    while len(global_storage) <= num_steps:
        global_storage.append(global_storage[-1])
    #Plot the graph for global frustration
    plotting(global_storage)

def Monte_Carlo(graph, connections:list, color_info:dict, update_info:list):
    '''Function that optimizes the graph by changing colors of its nodes. 
    Function tries to find the best color pattern based on if the exponential of the local action is greater than a random number between 0 and 1
    It creates a list with all global frustrations and calls on function to plot that list.
    
    >>>Monte_Carlo(graph,[(0, 1),(1, 2),(2, 3),(3, 0)], {0: 0.0, 1: 0.0, 2: 0.0, 3: 1.0}, ['yes', ['1', 5]])
    '''
    perm_new_color = color_info.copy() #Copy of the provided dictionary
    local_fru = local_frustration(connections, color_info) #Calculate the local frustration for provided connections and colors
    global_fru = sum(local_fru.values()) / 2 #Calculate the global frustration
    global_storage= [global_fru] #List for storing the values of global frustration
    test= 0
    num_steps= update_info[1][1] #Get the number of steps
    
    while num_steps>= test:
        montecarlo_number = random.random() #Set random number between 0 and 1
        for connection in connections:
            for point in connection: #Get the edge from connection
                edge = point

                #Get its local frustration and calculate its exponential
                local_fru1 = local_fru.get(edge)
                calc_exp = exp(local_fru1)
                #If its value is bigger then the random number
                if calc_exp >= montecarlo_number:
                    # Get the color of the edge from dictionary
                    color1=perm_new_color.get(edge)
                    if color1 == 0.0: #Swap its color
                        perm_new_color[edge] = 1.0
                    else:
                        perm_new_color[edge] = 0.0
            
                    #Calculate new local and global frustration for new colors
                    local_fru= local_frustration(connections, perm_new_color)
                    global_fru= sum(local_fru.values()) / 2
                    #Store this value
                    global_storage.append(global_fru)
            
                    #Update the graph with new colors
                    vis.Visualiser.update(graph,val_map=perm_new_color)
        test+=1
    plotting(global_storage)

def plotting(global_points:list):
    '''Function that plots number of steps on x-axis and global frustration on y-axis.
    
    >>>plotting([-0.5, -2.5, -2.5, -2.5, -2.5, -2.5, -2.5, -2.5])
    '''
    plt.figure()
    plt.plot(range(len(global_points)), global_points, linestyle= "-")
    plt.yticks(global_points)
    plt.xticks(range(len(global_points)))
    plt.title("Global Frustration over Steps")
    plt.xlabel("Number of update steps")
    plt.ylabel("Global Frustration")
    plt.show()