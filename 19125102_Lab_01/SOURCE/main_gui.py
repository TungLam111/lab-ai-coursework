from tkinter import *
from tkinter import ttk
import tkinter
import main
from PIL import ImageTk, Image 

LARGEFONT =("Verdana", 35)
WIDTH_WINDOW = 1000
HEIGHT_WINDOW = 650
RJ_FILE = './INPUT/rj.png'
RJ_SIZE = 70
class RunningAlgorithm():
    
    def __init__(self, ):
        self.root = Tk()
        self.root.title("Algorithm AI")
        self.frame = ttk.Frame(self.root, padding=0)
        self.frame.pack()
        self.algorithm = None
        self.width = 640
        self.height = 640
        self.num_square = None
        self.data = []
        self.rect_width, self.rect_height = None, None
        self.expanded_nodes = None
        self.path = None 
        self.cost = None
        self.canvas = tkinter.Canvas(self.frame, width=WIDTH_WINDOW, height=HEIGHT_WINDOW)
        self.current_rj = None
        self.image = None 
        self.isRunning = False
        self.start_node = None
        self.end_node = None 
        self.adjacency_list = None 
        self.adjacency_barrier_list = None
        self.size_maze = None
        self.init_rj()
        self.draw_button()
        self.prepare()

    def init_rj(self):
        image = Image.open(RJ_FILE)
        image = image.resize((RJ_SIZE, RJ_SIZE), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)  

    def deleteAll(self):
        print("----------DELETIIIIIIIIIIIIIIING-----------")
        self.canvas.delete(ALL)

    def check_side(self, current_number, side):
        if side < current_number and current_number - side < self.num_square:
            return "top"
        elif side <current_number and current_number - side == self.num_square:
            return "left"
        elif side > current_number and side - current_number < self.num_square:
            return "bottom"
        else:
            return "right"

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
        self.isRunning = False
        self.choose_algorithm()
    
    def check(self):
        print("You are running ", self.algorithm)

    def prepare(self):

        self.start_node, self.end_node, self.adjacency_list, self.size_maze = main.prepare_input()
        self.num_square = self.size_maze
        self.rect_width, self.rect_height = self.width // self.num_square, self.height // self.num_square
        self.adjacency_barrier_list = self.adjacency_list.copy()

        for key, value in enumerate(self.adjacency_barrier_list):
            four_side = []
            if key % self.num_square > 0 and key % self.num_square < self.num_square:
                four_side.append(key + 1)
                four_side.append(key - 1)
            if key - self.num_square > 0 :
                four_side.append(key - self.num_square)
            if key + self.num_square < self.num_square * self.num_square:
                four_side.append(key + self.num_square)

            self.adjacency_barrier_list[key] = list(set(four_side) - set(value))

        for i in range(self.num_square):
            column = []
            for j in range(self.num_square):
                color = "red"
                square = main.Square(self.height/self.num_square, self.width/self.num_square, color, self.num_square * i + j, i * self.rect_height, j * self.rect_width )
                column.append(square)
            self.data.append(column)

        for col in range(len(self.data)):
            for row in range(len(self.data[0])):
                #print("col = {} row = {}".format(col , row))
                x0, y0 = self.data[col][row].x0, self.data[col][row].y0
                x1, y1 = x0 + self.rect_height, y0 + self.rect_width
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.data[col][row].color, )
                obstacles = self.adjacency_barrier_list[self.data[col][row].number]
                for obstacle in obstacles :
                    check = self.check_side(self.data[col][row].number, obstacle)
                    if check == "top":
                        self.canvas.create_rectangle(x0, y0 - 5 , x1 , y0 , fill="white", outline="white")
                    elif check == "left":
                        self.canvas.create_rectangle(x0-5, y0, x0 , y1, fill ="white" , outline="white")
                    elif check == "bottom":
                        self.canvas.create_rectangle(x0 , y0 + self.rect_width , x1 , y0 + self.rect_width +5, fill="white", outline="white")
                    else:
                        self.canvas.create_rectangle( x0 + self.rect_height , y0 ,  x0 + self.rect_height+5 ,y1, fill="white", outline="white")
                self.canvas.create_text(x0 + self.rect_height / 2, y0 + self.rect_width / 2, text="{}".format(self.data[col][row].number),font="Helvetica 20 italic bold", fill="white")
        
        self.current_rj = self.canvas.create_image(self.data[0][0].x0, self.data[0][0].y0 ,  anchor=NW, image=self.image ) 

    def choose_algorithm(self):
        if self.algorithm == "usc":
           self.check()
           visited_nodes, expandable_nodes, time_run = main.solve_UCS_algorithm(self.start_node, self.end_node, self.adjacency_list, self.size_maze)
           self.expanded_nodes, self.path , self.cost = main.print_result(visited_nodes, expandable_nodes, self.adjacency_list, time_run)
        if self.algorithm == "gbfs":
           self.check()
           visited_nodes, expandable_nodes, time_run = main.solve_greedy_best_first_search(self.start_node, self.end_node, self.adjacency_list, self.size_maze)
           self.expanded_nodes, self.path , self.cost = main.print_result(visited_nodes, expandable_nodes, self.adjacency_list, time_run, is_greedy=True)
        if self.algorithm == "idfs":
           self.check()
           visited_nodes, expandable_nodes, time_run = main.solve_iterative_deepening_search(self.start_node, self.end_node, self.adjacency_list, self.size_maze, max_depth=self.size_maze * self.size_maze)
           self.expanded_nodes, self.path , self.cost = main.print_result(visited_nodes, expandable_nodes, self.adjacency_list, time_run)
        if self.algorithm == "a_star":
           self.check()
           visited_nodes, expandable_nodes, time_run = main.solve_A_star_algorithm(self.start_node, self.end_node, self.adjacency_list, self.size_maze)
           self.expanded_nodes, self.path , self.cost = main.print_result(visited_nodes, expandable_nodes, self.adjacency_list,time_run)

    def draw_button(self):
        button_run = ttk.Button(self.canvas, text ="Start running algorithm",
        command = lambda: self.run())
        button_run.place(x = 700, y = 200)

        button_exit = ttk.Button(self.canvas, text ="Exit",
        command = lambda: self.root.destroy())
        button_exit.place(x = 900, y = 200)

        button_USC = ttk.Button(self.canvas, text="Uninformed Cost Search", 
        command= lambda: self.set_algorithm("usc"))
        button_USC.place(x = 800, y = 300)

        button_IDFS = ttk.Button(self.canvas, text="Iterative deepening search", 
        command= lambda: self.set_algorithm("idfs"))
        button_IDFS.place(x = 800, y = 400)

        button_GBFS = ttk.Button(self.canvas, text="Greedy Best First Search", 
        command= lambda: self.set_algorithm("gbfs"))
        button_GBFS.place(x=800, y = 500)

        button_AStar = ttk.Button(self.canvas, text="A* search", 
        command= lambda: self.set_algorithm("a_star"))
        button_AStar.place(x= 800, y = 600)
    
    def run(self):
        if self.algorithm == None :
            return
        self.isRunning = True 
        self.moving()
    
    def pause(self):
        self.isRunning = False 

    def moving(self):
        if self.isRunning == False:
            return
        if len(self.expanded_nodes) == 0:
            return 
        number = self.expanded_nodes.pop(0)
        col = number // self.num_square
        row = number % self.num_square
        self.canvas.moveto(self.current_rj , self.data[col][row].x0, self.data[col][row].y0 )
        print("go..go..")
        self.root.after(500, self.moving)

game = RunningAlgorithm()
game.canvas.pack()
#game.run_alrogithm()
game.root.mainloop()
