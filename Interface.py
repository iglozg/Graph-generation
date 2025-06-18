#File for interface
import graph_sim as graph
def menu_main():
  """ Main menu of the program, users can select the random number or provided file graph generation
    or to terminate. """

  option = input('''Select one of the following:
  1) Generate graph from random numbers
  2) Generate graph from provided file
  9) Quit.
Enter your choice: ''').strip()
  if option == "1":
    menu_random() # display the menu for random numbers
  elif option == "2":
    menu_provided() # display the menu for provided numbers
  elif option == "9":
    print("Bye")
    exit(0) # quit the program 
  else:
    print("Option \"" + option + "\" not recognised, please enter a number that corresponds to one of the options displayed.")
    menu_main()

def menu_random():
    """Submenu of the program, users define how many numbers of sites the random graph has."""
    sites_random = input('''How many sites do you want the graph to have (number needs to be bigger then 1)? ''').strip()
    try: #Try to convert this number to an integer
      edges_random = int(sites_random)
      try: #Assert it is bigger then 1
        assert edges_random>1
      except AssertionError:
        print("Oops something went wrong, please provide a number that's bigger then 1")
        menu_random()  
    except ValueError:
      print("Oops something went wrong, please provide a number that's bigger then 1")
      menu_random()
    color_info = menu_colors()
    update_info = update_question()
    graph.generate_connected_graph(edges_random,color_info, update_info)


def menu_colors():
    """Submenu of the program, users define the coloring pattern for the sites in the graph."""
    color_random = input('''Select colors for the graph:
    1) All points are yellow
    2) All points are blue
    3) All points are random colored with blue or yellow.
  Enter your choice: ''').strip()
    if color_random not in ["1", "2", "3"]:
        print("Option \"" + color_random + "\" not recognised, please enter a number that corresponds to one of the options displayed.")
        menu_colors()
    else:
        return color_random
    

def menu_provided():
    """Submenu of the program, users define from which file they create the graph."""
    option = input("""Is the file in the same folder as this python file (Yes or No)?: """).strip().lower()
    if option == "yes":
        file_yes = input("""Please type full name of the file with its extension (for example: my_txt.txt): """)
        try:
            opener(file_yes)
        except FileNotFoundError: # If the file is not in the same folder as the python file, it will print this message
            print("Oops it seems that this file is not in the same folder as the python file, please try again")
            menu_provided()
    elif option == "no":
        file_no = input("""Please provide the whole path to that file (for example: C:/path/to/your/file/file_name.txt): """).strip()
        try:
          opener(file_no)
        except FileNotFoundError:
           print("Oops it seems that this is incorrect path to the file, please try again")
           menu_provided()
    else:
        print("Oops, I think you made a typo, please try again")
        menu_provided()

def opener(a):
   """Function that opens a file, read each line skipping lines that start with #. 
   Function puts each line in a list stripping them from "\n" symbol and splitting each line based on "," symbol. 
   Then function tries to turn each line into an integer and if it fails it prints this line.
   If the length of created list is odd function deletes last value.
   After that function puts adjacent values together in a matrix and calls on other functions."""
   with open(a) as reader:
    b=[]
    for line in reader.readlines(): # Read each line in file
        if line.startswith("#"): # Skip each line that starts with #
            continue
        line= line.strip("\n") # Strip each line with \n symbol
        values = line.split(",") # Divide each line by the comma 
        try:
            for value in values:
                num = int(value)  # Convert the value to an integer
                b.append(num)  # Append it to the list
        except ValueError:
            print(f"Skipping non-integer value(s) in line: {line}")
    if len(b) % 2 != 0: # If the length of list is odd (missing value at the end)
        b.pop() # Delete last value
    matrix = [b[i:i+2] for i in range(0, len(b), 2)] # Create a matrix with adjacent values in their own list 
    color_info = menu_colors()
    update_info = update_question()
    graph.draw_graph(matrix, color_info, update_info)
    

def update_question():
   """Small menu that asks user if he/she wants to optimize the graph."""
   update_info= None
   update_question = input(''' Do you wish to optimize the graph? (Yes or No): ''').strip().lower()
   if update_question == "yes":
      update_info = ["yes", menu_update()]
   elif update_question == "no":
      update_info = "no"
   else: 
      print("Oops I think you made a typo, please try again")
      update_question()
   return update_info


def menu_update():
    """Submenu of the program, users choose the graph which they want to update and which update function they want to use."""
    update = input('''Which update function do you want to use?:
    1) Ordered
    2) MaxViolation
    3) Monte Carlo.
Enter your choice: ''').strip()
    if update not in ["1", "2", "3"]:
       print("Option \"" + update + "\" not recognised, please enter a number that corresponds to one of the options displayed.")
       menu_update()
    else:
       steps = input('''In how many steps do you want to optimize the graph?: ''').strip()
       try: #Try to convert to integer
          num_steps = int(steps)
          try: #Assert that this number is bigger then 0
             assert num_steps > 0
          except AssertionError:
             print("Oops there is an error please provide number bigger then 0")
             menu_update() 
       except ValueError:
          print("Oops there is an error please provide a number bigger then 0")
          menu_update()
       return [update, num_steps]

menu_main()
