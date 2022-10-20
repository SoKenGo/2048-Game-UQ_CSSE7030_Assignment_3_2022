# You may import any submodules of tkinter here if you wish
# You may also import anything from the typing module
# All other additional imports will result in a deduction of up to 100% of your A3 mark
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from a3_support import *
from tkinter.filedialog import askopenfilename, asksaveasfilename, askopenfile

class Model:
	def __init__(self) -> None:
		"""
		Constructs a new 2048 model instance. This includes setting up a new game (see new_game
		method below).
		"""
		self.column = 4#Designed for changing the size of the board
		#Initialization of the board using list[list[int]] without using numpy
		self.matrix = [[None for _ in range(self.column)] for _ in range(self.column)]
		#2 new tiles randommly be created 
		self.add_tile()
		self.add_tile()
		#A list for recording the history of the history
		self.history = list()
		#Only 3 undo can be done
		self.undoable_move = list()
		self.score = 0
		#Remaining undo chances
		self.undo_remained = 3
		#Add first record
		self.record()

	def new_game(self) -> None:
		"""
		Sets, or resets, the game state to an initial game state. Any information is set to its initial
		state, the tiles are all set to empty, and then two new starter tiles are randomly generated
		(see the add_tile method below).
		"""
		self.matrix = [[None for _ in range(self.column)] for _ in range(self.column)]
		self.add_tile()
		self.add_tile()
		self.score = 0
		self.undo_remained = 3
		self.history = list()
		self.undoable_move = list()
		self.record()

	def get_tiles(self) -> list[list[Optional[int]]]:
		"""
		Return the current tiles matrix. Each internal list represents a row of the grid, ordered from
		top to bottom. Each item in each row list is the integer value on the tile occupying that
		space, or None if no tile is occupying that space.
		"""
		return self.matrix

	def add_tile(self) -> None:
		"""
		Randomly generate a new tile at an empty location (you must use generate_tile for this)
		and add it to the current tiles matrix.
		"""
		(position, number) = generate_tile(self.matrix)
		row = position[0]
		col = position[1]
		self.matrix[row][col] = number

	def move_left(self) -> None:
		"""
		Moves all tiles to their left extreme, merging where necessary. This involves stacking all tiles
		to the left, merging to the left, and then restacking to the left to fill in any gaps created. If
		you are keeping track of a score (see Task 2), this method should also add any points gained
		from the history to the total score.
		"""
		#stack left -> combine left -> stack left
		combined = combine_left(stack_left(self.matrix))
		self.matrix = stack_left(combined[0])
		self.score += combined[1]

	def move_right(self) -> None: 
		"""
		Moves all tiles to their right extreme, merging where neces-
		sary. This can be achieved by reversing the tiles matrix, moving left, and then reversing
		the matrix again. If you are keeping track of a score (see Task 2), this method should also
		result in gained points being added to the total score.
		"""
		#reverse -> history left -> reverse
		self.matrix = reverse(self.matrix)
		self.move_left()
		self.matrix = reverse(self.matrix)

	def move_up(self) -> None:
		"""
		Moves all tiles to their top extreme, merging where necessary. This can be achieved by
		transposing the tiles matrix, moving left, and then transposing the matrix again. If you are
		keeping track of a score (see Task 2), this method should also result in gained points being
		added to the total score.
		"""
		#transpose -> history left -> transpose
		self.matrix = transpose(self.matrix)
		self.move_left()
		self.matrix = transpose(self.matrix)

	def move_down(self) -> None:
		"""
		Moves all tiles to their bottom extreme, merging where necessary. This can be achieved by
		transposing the tiles matrix, moving right, and then transposing the matrix again. If you
		are keeping track of a score (see Task 2), this method should also result in gained points
		being added to the total score.
		"""
		#transpose -> history right -> transpose
		self.matrix = transpose(self.matrix)
		self.move_right()
		self.matrix = transpose(self.matrix)

	def attempt_move(self, history: str) -> bool:
		"""
		Makes the appropriate history according to the history string provided. Returns True if the
		history resulted in a change to the game state, else False. The history provided must be one
		of wasd (this is a pre-condition, not something that must be handled within this method).
		"""

		if len(self.undoable_move) >= 3:
			del(self.undoable_move[0])
			self.undoable_move.append(self.history[-1])
		else:
			self.undoable_move.append(self.history[-1])
		
		if history in ['Up', 'w', 'Down', 's', 'Left', 'a', 'Right', 'd']:
			if history in ['Up', 'w']:    
				self.move_up()
			elif history in ['Down', 's']:  
				self.move_down()
			elif history in ['Left', 'a']: 
				self.move_left()
			elif history in ['Right', 'd']:
				self.move_right()
			return True
		return False
	
	def has_won(self) -> bool:
		"""
		Returns True if the game has been won, else False. The game has been won if a 2048 tile
		exists on the grid.
		"""
		#Winning condition
		if 2048 in [i for li in self.matrix for i in li]:
			return True
		return False

	def has_lost(self) -> bool:
		"""
		Returns True if the game has been lost, else False. The game has been lost if there are
		no remaining empty places in the grid, but no history would result in a change to the game
		state.
		"""
		matrix = self.matrix
		column = self.column
		if None in [i for li in matrix for i in li]:
			return False

		for row in range(column):
			for col in range(column-1):
				if matrix[row][col] == matrix[row][col+1]:
					return False

		for row in range(column-1):
			for col in range(column):
				if matrix[row][col] == matrix[row+1][col]:
					return False
		return True

	def prev_step(self):
		if self.history !=[]:
			#get the latest data
			prev_data = self.undoable_move.pop()
			self.score = prev_data['score']
			self.matrix = prev_data['matrix']

	def record(self):
		prev_step = {
				'score': self.score,
				'matrix': self.cheat_copy(self.matrix),
			}
		self.history.append(prev_step)

	def cheat_copy(self, original):
		return [item[:] for item in original]

	def	get_score(self) -> int: 
		"""
		Returns the current score for the game. Each time a new tile is
		created by a merge, its new value should be added to the score. The total score to be added
		after a merge is calculated for you by the combine_left function in a3_support.py.
		"""
		return self.score

	def get_undos_remaining(self) -> int: 
		"""
		Get the number of undos the player has remaining.
		This should start at 3 at the beginning of a new game, and reduce each time an undo is
		used.
		"""
		return self.undo_remained

	def use_undo(self) -> None: 
		"""
		Attempts to undo the previous history, returning the current tiles
		to the previous tiles state before the last history that made changes to the tiles matrix. If the
		player does not have any undos remaining, or they are back at the initial state, this method
		should do nothing.
		"""
		if self.undo_remained > 0:
			self.undo_remained -= 1
			self.prev_step()
		else:
			return None

class StatusBar(tk.Frame):
	"""
	You must add a class StatusBar that inherits from tk.Frame and represents information about
	score and remaining undos, as well as a button to start a new game and a button to undo the
	previous history. You can see the layout of the StatusBar frame below the 4x4 grid in Figure 1.
	While you will likely need to construct tk.Frame instances in this class to achieve the layout, these
	frames (and the things inside them) must be in the StatusBar itself, not directly in master.

	"""
	def __init__(self, master: tk.Tk, **kwargs): 
		"""
		Sets up self to be an instance of tk.Frame
		and sets up inner frames, labels and buttons in this status bar.
		# """
		super().__init__(
			master,
			 **kwargs
			 )
		#frame for containing the score counter
		frame_score = tk.Frame(self, bg=BACKGROUND_COLOUR)
		#undo for containning the remaining undos counter
		undo = tk.Frame(self, bg=BACKGROUND_COLOUR)
		#Frame for the buttons
		button_list = tk.Frame(self)
		#Title label
		score_title = tk.Label(frame_score, fg=COLOURS[None], font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text= 'SCORE')
		#Score label
		self.score = tk.Label(frame_score, fg='#f5ebe4', font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text='0')
		#Title label
		undo_title = tk.Label(undo, fg=COLOURS[None], font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text= 'UNDOS')
		#Undo label
		self.remaining_undo = tk.Label(undo, fg='#f5ebe4', font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text='3')
		#Pack the labels
		undo_title.pack()
		self.remaining_undo.pack()
		score_title.pack()
		self.score.pack()
		#Pack the frames
		frame_score.pack(side = tk.LEFT, padx=10)
		undo.pack(side = tk.LEFT, padx=40)
		#Create the buttons
		self.reset_bot = tk.Button(button_list, text='New Game', bg='#f5ebe4', font=('Arial bold', 10))
		self.undo_bot = tk.Button(button_list, text='Undo Move', bg='#f5ebe4', font=('Arial bold', 10))
		#Pack the buttons
		self.reset_bot.grid(row=1, padx=10, pady=3)
		self.undo_bot.grid(row=2, padx=10, pady=3)
		button_list.pack(side=tk.RIGHT)
		self.pack(side=tk.BOTTOM)

	def redraw_infos(self, score: int, undos: int) -> None: 
		"""
		Updates the score and undos
		labels to reflect the information given.
		"""
		#Change the text of counters
		self.score.config(text=str(score))
		self.score.update()
		self.remaining_undo.config(text=str(undos))
		self.remaining_undo.update()

	def set_callbacks(self, new_game_command: callable, undo_command: callable) -> None:

		"""
		Sets the commands for the new game and undo buttons to the given commands. 
		The arguments here are references to functions to be called when the buttons are pressed.
		"""
		#Set the callback reference
		self.reset_bot.config(command=new_game_command)
		self.undo_bot.config(command=undo_command)

class GameGrid(tk.Canvas):
	"""
	The GameGrid is a view class which inherits from tk.Canvas and represents the 4x4 grid. On
	the GameGrid canvas, tiles should be drawn using a combination of the create_rectangle and
	create_text method on self. You should not create a new tk.Canvas instance as an attribute
	within this class; doing so will cause the Gradescope tests to report that your GameGrid canvas
	contains no items.
	"""
	def __init__(self, root:tk.Tk, **kwargs) -> None:
		"""
		Sets up a new GameGrid in the master window. **kwargs is used to allow GameGrid to
		support any named arguments supported by tk.Canvas. The canvas should be 400 pixels
		wide and 400 pixels tall.
		"""
		canvas_size = 400
		self.data = Model()
		self.column = self.data.column
		self.space_size = 10
		self.cell_size = 87.5
		self._root = self.init_root(root)
		#Initialization for the canvas
		super().__init__(
			self._root,
			width = canvas_size,
			height = canvas_size,
			**kwargs,
			bg = BACKGROUND_COLOUR
		)
		
	def init_root(self, root:tk.Tk):
		#Modify the attributes of the root
		root.title('CSSE1001/7030 2022 Semester 2 A3')
		root.resizable(False, False)
		header = tk.Frame(root)
		self.init_header(header)
		return root

	def init_header(self, master):
		#Create the title label
		master['bg'] = 'yellow'
		header = tk.Label(master, fg= '#f5ebe4', bg='yellow', font=TITLE_FONT, text='2048', compound='center')
		header.pack(side = tk.TOP)
		master.pack(side = tk.TOP, expand = False, fill = tk.X)

	def _get_bbox(self, position: tuple[int, int]) -> tuple[int, int, int, int]:
		"""
		Return the bounding box for the (row, column) position, in the form
		(x_min, y_min, x_max, y_max).
		Here, (x_min, y_min) is the top left corner of the position with 10 pixels of padding
		added, and (x_max, y_ma[x) is the bottom right corner of the cell with 10 pixels of padding
		subtracted.
		"""
		#Cordinations for each box
		row = position[0]
		col = position[1]
		#NW corner
		x_min = (col + 1)*self.space_size + col*self.cell_size 
		y_min = (row + 1)*self.space_size + row*self.cell_size 
		#SE corner
		x_max = x_min + self.cell_size
		y_max = y_min + self.cell_size
		return x_min, y_min, x_max, y_max

	def _get_midpoint(self, position: tuple[int, int]) -> tuple[int, int]:
		"""
		Return the graphics coordinates for the center of the cell at the given (row, col) position.
		"""
		#Positions for the labels
		x_min, y_min, x_max, y_max = self._get_bbox(position)
		x = (x_min + x_max) // 2
		y = (y_min + y_max) // 2
		return x, y

	#Unused function
	def clear(self) -> None:
		"""
		Clears all items.
		"""
		pass

	def redraw(self, tiles: list[list[Optional[int]]]) -> None:
		"""
		Clears and redraws the entire grid based on the given tiles.
		"""
		#Draw the grid
		self.delete("all")
		for row in range(4):
			for col in range(4):
				position = (row, col)
				if tiles[row][col] == None:
					self._draw_box(position)
				else:
					self._draw_box(position, COLOURS[tiles[row][col]])
					self._draw_number(position, tiles[row][col])
					
	def _draw_box(self, position: tuple[int, int], colour = COLOURS[None]) -> None:
		"""
		Draw the <row, col> box.
		"""
		x_min, y_min, x_max, y_max = self._get_bbox(position)
		box = self.create_rectangle(
			x_min, y_min,
			x_max, y_max,
			#Fill the boxes with the colour according to number
			fill=colour,
			#Hide the outline
			outline=colour,
			width=1
		)
		
	def _draw_number(self, position: tuple[int, int], number: int) -> None:
		"""
		Draw <number> in the <row, col> box.
		"""
		x, y = self._get_midpoint(position)
		num = self.create_text(
			x, y,
			text=str(number),
			#Use the given font
			font=TILE_FONT,
			fill=FG_COLOURS[number]
		)
		
class Game():
	"""
	You must implement a class for the controller, called Game. This class should be instantiated in
	your main function to cause the game to be created and run. The controller class is responsible
	for maintaining the model and view classes, binding some event handlers, and facilitating com-
	munication between model and view classes.
	"""
	def __init__(self, master: tk.Tk) -> None:
		"""
		Constructs a new 2048 game. This method should create a Model instance, set the window
		title, create the title label and create instances of any view classes packed into master. It
		should also bind key press events to an appropriate handler, and cause the initial GUI to
		be drawn.
		"""
		self.root = master
		self.view = GameGrid(self.root)
		self.status = StatusBar(self.root)
		#Add attributes to the StatusBar instance
		self.status.config(padx=20, pady=20)
		#Set the callback function
		self.status.set_callbacks(self.start_new_game, self.undo_previous_move)
		#Using the same Model() data
		self.data = self.view.data
		#Create top-level menu
		self.menu = tk.Menu(self.root)
		#Second-level menu
		file_menu = tk.Menu(self.menu)
		#Append the labels
		self.menu.add_cascade(menu = file_menu, label="File")
		file_menu.add_command(label="Save game", command=self.save_as_file)
		file_menu.add_command(label="Load game", command=self.load_from_file)
		file_menu.add_command(label="New game", command=self.start_new_game)
		file_menu.add_command(label="Quit", command=self.file_menu_quit)
		#Add the file menu to the master
		self.root.config(menu=self.menu)
		self.view.pack()
		self.saved_files = 0

	def start_new_game(self):
		"""
		Start a new game
		"""
		self.data.new_game()
		self.status.redraw_infos(self.data.get_score(), self.data.get_undos_remaining())
		self.view.redraw(self.data.get_tiles())

	def undo_previous_move(self):
		if self.data.get_undos_remaining() == 3:
			self.data.history.pop()
		self.data.use_undo()
		self.status.redraw_infos(self.data.get_score(), self.data.get_undos_remaining())
		self.view.redraw(self.data.get_tiles())

	def draw(self) -> None:
		"""
		Redraws any view classes based on the current model state.
		"""
		self.view.redraw(self.data.get_tiles())

	def attempt_move(self, event: tk.Event) -> None:
		"""
		Attempt a history if the event represents a key press on character ‘a’, ‘w’, ‘s’, or ‘d’. Once
		a history has been made, this method should redraw the view, display the appropriate mes-
		sagebox if the game has been won, or create a new tile after 150ms if the game has not been
		won.
		"""
		ans = self.data.attempt_move(event.keysym)
		#Valid movement
		if ans == True:	
			self.new_tile()
			self.draw()
			self.status.redraw_infos(self.data.get_score(), self.data.get_undos_remaining())

	def draw_tile(self):
		#Only create new tile when there is a spare space
		if None in [i for li in self.data.matrix for i in li]:
			self.data.add_tile()
			self.draw()
			#Judging win or lost
			self.judge()
			#Record the changes
			self.data.record()

	def new_tile(self) -> None: 
		"""
		Adds a new tile to the model and redraws. If the game has
		been lost with the addition of the new tile, then the player should be prompted with the
		appropriate messagebox displaying the LOSS_MESSAGE.
		"""
		#Add a delay on GUI
		self.root.after(150, self.draw_tile)		

	def reset(self) -> None:
		self.data.new_game()
		self.draw()

	def judge(self):
		if self.data.has_won() == True:
			res = tkMessageBox.askyesno(title="2048", message=WIN_MESSAGE)
			if res:
				#Delete the items on background
				self.view.delete('all')
				self.reset()
				self.view.redraw(self.data.get_tiles())
			else:
				self.root.quit()
		if self.data.has_lost() == True:
			res = tkMessageBox.askyesno(title="2048", message=LOSS_MESSAGE)
			if res:
				self.view.delete('all')
				self.reset()
				self.view.redraw(self.data.get_tiles())
			else:
				self.root.quit()

	def main(self):
		self.draw()
        #Binding keyboard events
		self.root.bind('<Key>', self.attempt_move)

	def file_menu_quit(self) -> None:
		"""
		file_menu -> quit handler
		"""
		res = tkMessageBox.askyesno(title="2048", message="Are you sure you want to quit?")
		if res:
			self.root.destroy()
		else:
			return None
	
	def save_as_file(self) -> None:
		self.saved_files += 1
		files = [('All Files', '*.*'), ('text files', '*.txt')]
		file_name = asksaveasfilename(filetypes = files, defaultextension = ".py")
		#Handle the "Cancel"
		if file_name:
			f = open(file_name, "w")
			f.write("%s=%s\n" %("self.data.matrix", self.data.get_tiles()))
			f.write("%s=%s\n" %("self.data.score", self.data.get_score()))
			f.write("%s=%s\n" %("self.data.undo_remained", self.data.get_undos_remaining()))
			f.write("%s=%s\n" %("self.data.history", self.data.history))
			f.write("%s=%s\n" %("self.data.undoable_move", self.data.undoable_move))
			f.close()

	def load_from_file(self) -> None:
		f = askopenfile(mode ='r', filetypes =[('text files', '*.txt')])
		#Handle the "Cancel"
		if f:
			self.data.matrix = eval(f.readline().split("=")[-1].strip())
			self.data.score = int(f.readline().split("=")[-1].strip())
			self.data.undo_remained = int(f.readline().split("=")[-1].strip())
			self.data.history =eval(f.readline().split("=")[-1].strip())
			self.data.undoable_move = eval(f.readline().split("=")[-1].strip())
			#Resume the game
			self.data.record()
			self.status.redraw_infos(self.data.get_score(), self.data.get_undos_remaining())
			self.view.redraw(self.data.get_tiles())
			f.close()

def play_game(root):
	game = Game(root)
	game.main()
	game.view.pack()

if __name__ == '__main__':
	root = tk.Tk()
	play_game(root)
	root.mainloop()
