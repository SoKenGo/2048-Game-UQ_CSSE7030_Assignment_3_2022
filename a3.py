# You may import any submodules of tkinter here if you wish
# You may also import anything from the typing module
# All other additional imports will result in a deduction of up to 100% of your A3 mark
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from a3_support import *

class Model:
	def __init__(self) -> None:
		"""
		Constructs a new 2048 model instance. This includes setting up a new game (see new_game
		method below).
		"""
		self.column = 4
		self.matrix = [[None for _ in range(self.column)] for _ in range(self.column)]
		self.add_tile()
		self.add_tile()
		self.move = list()
		self.score = 0
		self.undo_times = 3
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
		self.undo_times = 3
		self.move = list()
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
		from the move to the total score.
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
		self.matrix = transpose(self.matrix)
		self.move_right()
		self.matrix = transpose(self.matrix)

	def attempt_move(self, move: str) -> bool:
		"""
		Makes the appropriate move according to the move string provided. Returns True if the
		move resulted in a change to the game state, else False. The move provided must be one
		of wasd (this is a pre-condition, not something that must be handled within this method).
		"""
		if move in ['Up', 'w', 'Down', 's', 'Left', 'a', 'Right', 'd']:
			if move in ['Up', 'w']:    
				self.move_up()
			elif move in ['Down', 's']:  
				self.move_down()
			elif move in ['Left', 'a']: 
				self.move_left()
			elif move in ['Right', 'd']:
				self.move_right()
			return True
		return False
	
	def has_won(self) -> bool:
		"""
		Returns True if the game has been won, else False. The game has been won if a 2048 tile
		exists on the grid.
		"""
		if 2048 in [i for li in self.matrix for i in li]:
			return True
		return False

	def has_lost(self) -> bool:
		"""
		Returns True if the game has been lost, else False. The game has been lost if there are
		no remaining empty places in the grid, but no move would result in a change to the game
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
		if self.move!=[]:
			prev_data = self.move[-1]
			self.score = prev_data['score']
			self.matrix = prev_data['matrix']
			self.move = self.move[0:-1]
		# if self.move!=[]:
		# 	# self.move.pop()
		# 	prev_data = self.move.pop()
		# 	self.score = prev_data['score']
		# 	self.matrix = prev_data['matrix']


		#prev_data = self.history[-1]
		# self.score = prev_data['score']
		# self.matrix = prev_data['matrix']
		# self.history = self.history[0:-1]

			
	def record(self):
		prev_step = {
				'score': self.score,
				'matrix': self.cheat_copy(self.matrix),
			}
		self.move.append(prev_step)

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
		return self.undo_times

	def use_undo(self) -> None: 
		"""
		Attempts to undo the previous move, returning the current tiles
		to the previous tiles state before the last move that made changes to the tiles matrix. If the
		player does not have any undos remaining, or they are back at the initial state, this method
		should do nothing.
		"""
		# print(self.move)
		if self.undo_times >= 1:
			self.undo_times -= 1
			self.prev_step()
		else:
			return None


class StatusBar(tk.Frame):
	"""
	You must add a class StatusBar that inherits from tk.Frame and represents information about
	score and remaining undos, as well as a button to start a new game and a button to undo the
	previous move. You can see the layout of the StatusBar frame below the 4x4 grid in Figure 1.
	While you will likely need to construct tk.Frame instances in this class to achieve the layout, these
	frames (and the things inside them) must be in the StatusBar itself, not directly in master.

	"""
	def __init__(self, master: tk.Tk, **kwargs): 
		"""
		Sets up self to be an instance of tk.Frame
		and sets up inner frames, labels and buttons in this status bar.
		"""
		self.root = master
		#footer = tk.Frame(master, padx=20, pady=10)
		footer = super().__init__(
			self.root,
			 **kwargs
			# padx=0,
			# pady=10
			 )

		# super().__init__(
		# 	self.root,
		# 	width = canvas_size,
		# 	height = canvas_size,
		# 	**kwargs,
		# 	bg = BACKGROUND_COLOUR
		# )

		frame = tk.Frame(footer, bg=BACKGROUND_COLOUR)
		undo = tk.Frame(footer, bg=BACKGROUND_COLOUR)
		button_list = tk.Frame(footer)
		score_title = tk.Label(frame, fg=COLOURS[None], font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text= 'SCORE')
		self.score = tk.Label(frame, fg='white', font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text='0')

		undo_title = tk.Label(undo, fg=COLOURS[None], font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text= 'UNDOS')
		self.remaining_undo = tk.Label(undo, fg='white', font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text='3')

		undo_title.pack()
		self.remaining_undo.pack()

		score_title.pack()
		self.score.pack()
		frame.pack(side = tk.LEFT, padx=10, pady=5)
		undo.pack(side = tk.LEFT, padx=40, pady=5)
		self.reset_bot = tk.Button(button_list, text='New Game', bg='white', font=('Arial bold', 10))
		self.undo_bot = tk.Button(button_list, text='Undo Move', bg='white', font=('Arial bold', 10))
		self.reset_bot.grid(row=1, padx=10, pady=3)
		self.undo_bot.grid(row=2, padx=10, pady=3)
		button_list.pack(side=tk.RIGHT)
		#footer.pack(side=tk.BOTTOM, expand=False, fill=tk.X)

	def redraw_infos(self, score: int, undos: int) -> None: 
		"""
		Updates the score and undos
		labels to reflect the information given.
		"""
		self.score.config(text=str(score))
		self.score.update()
		self.remaining_undo.config(text=str(undos))
		self.remaining_undo.update()

	def set_callbacks(self, new_game_command: callable, undo_command: callable) -> None:

		"""
		Sets the commands for the new game and undo buttons to the given commands. 
		The arguments here are references to functions to be called when the buttons are pressed.
		"""
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
		self.root = self.init_root(root)
		#self.status = StatusBar(self.root)
		super().__init__(
			self.root,
			width = canvas_size,
			height = canvas_size,
			**kwargs,
			bg = BACKGROUND_COLOUR
		)
		self.boxes, self.labels = list(), list()
		
	def init_root(self, root:tk.Tk):
		root.title('CSSE1001/7030 2022 Semester 2 A3')
		root.resizable(False, False)
		header = tk.Frame(root)
		self.init_header(header)
		#self.init_footer(root)
		return root

	def init_header(self, master):
		master['bg'] = 'yellow'
		header = tk.Label(master, fg= 'white', bg='yellow', font=TITLE_FONT, text='2048', compound='center')
		header.pack(side = tk.TOP)
		master.pack(side = tk.TOP, expand = False, fill = tk.X)

	# def init_footer(self, master):
	# 	footer = tk.Frame(master, padx=20, pady=10)
	# 	frame = tk.Frame(footer, bg=BACKGROUND_COLOUR)
	# 	undo = tk.Frame(footer, bg=BACKGROUND_COLOUR)
	# 	button_list = tk.Frame(footer)
	# 	score_title = tk.Label(frame, fg=COLOURS[None], font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text= 'SCORE')
	# 	self.score = tk.Label(frame, fg='white', font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text=self.data.get_score())

	# 	undo_title = tk.Label(undo, fg=COLOURS[None], font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text= 'UNDOS')
	# 	self.remaining_undo = tk.Label(undo, fg='white', font=('Arial bold', 20), bg=BACKGROUND_COLOUR, compound='center', text=self.data.get_undos_remaining())

	# 	undo_title.pack()
	# 	self.remaining_undo.pack()

	# 	score_title.pack()
	# 	self.score.pack()
	# 	frame.pack(side = tk.LEFT)
	# 	undo.pack(side = tk.LEFT, padx=40)
	# 	reset_bot = tk.Button(button_list, text='New Game', bg='white', font=('Arial bold', 10), command=self.clear)
	# 	undo_bot = tk.Button(button_list, text='Undo Move', bg='white', font=('Arial bold', 10), command=self.undo)
	# 	reset_bot.grid(row=1, padx=3, pady=3)
	# 	undo_bot.grid(row=2, padx=3, pady=3)
	# 	button_list.pack(side=tk.RIGHT)
	# 	footer.pack(side=tk.BOTTOM, expand=False, fill=tk.X)
		
	def _get_bbox(self, position: tuple[int, int]) -> tuple[int, int, int, int]:
		"""
		Return the bounding box for the (row, column) position, in the form
		(x_min, y_min, x_max, y_max).
		Here, (x_min, y_min) is the top left corner of the position with 10 pixels of padding
		added, and (x_max, y_ma[x) is the bottom right corner of the cell with 10 pixels of padding
		subtracted.
		"""
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
		x_min, y_min, x_max, y_max = self._get_bbox(position)
		x = (x_min + x_max) // 2
		y = (y_min + y_max) // 2
		return x, y

	def clear(self) -> None:
		"""
		Clears all items.
		"""
		#self.status.redraw_infos(self.data.get_score(), self.data.get_undos_remaining())
		self.redraw(self.data.get_tiles())
	# 	self.data.new_game()
	# 	# self.score.config(text=str(self.data.get_score()))
	# 	# self.score.update()
	# 	# self.remaining_undo.config(text=str(self.data.get_undos_remaining()))
	# 	# self.remaining_undo.update()
	# 	self.status.redraw_infos(self.data.get_score(), self.data.get_undos_remaining())
	# 	self.redraw(self.data.get_tiles())
	
	# def undo(self):
	# 	if self.data.get_undos_remaining() == 3:
	# 		self.data.move.pop()
	# 	self.data.use_undo()
	# 	self.score.config(text=str(self.data.get_score()))
	# 	self.score.update()

	# 	self.remaining_undo.config(text=str(self.data.get_undos_remaining()))
	# 	self.remaining_undo.update()

	# 	self.redraw(self.data.get_tiles())

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
			fill=colour,
			outline=colour,
			width=1
		)
		self.boxes.append(box)
		
	def _draw_number(self, position: tuple[int, int], number: int) -> None:
		"""
		Draw <number> in the <row, col> box.
		"""
		x, y = self._get_midpoint(position)
		num = self.create_text(
			x, y,
			text=str(number),
			font=TILE_FONT,
			fill=FG_COLOURS[number]
		)
		self.labels.append(num)
		
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
		self.view.pack()
		self.status = StatusBar(self.root)
		self.status.config(padx=20, pady=20)
		self.status.set_callbacks(self.start_new_game, self.undo_previous_move)
		self.data = self.view.data

	def start_new_game(self):
		self.data.new_game()
		self.status.redraw_infos(self.data.get_score(), self.data.get_undos_remaining())
		self.view.redraw(self.data.get_tiles())

	def undo_previous_move(self):
		if self.data.get_undos_remaining() == 3:
			self.data.move.pop()
		self.data.use_undo()
		self.status.redraw_infos(self.data.get_score(), self.data.get_undos_remaining())
		self.view.redraw(self.data.get_tiles())
		#self.view.redraw(self.data.get_tiles())

	def draw(self) -> None:
		"""
		Redraws any view classes based on the current model state.
		"""
		self.view.redraw(self.data.get_tiles())

	def attempt_move(self, event: tk.Event) -> None:
		"""
		Attempt a move if the event represents a key press on character ‘a’, ‘w’, ‘s’, or ‘d’. Once
		a move has been made, this method should redraw the view, display the appropriate mes-
		sagebox if the game has been won, or create a new tile after 150ms if the game has not been
		won.
		"""
		ans = self.data.attempt_move(event.keysym)
		if ans == True:	
			self.new_tile()
			#self.data.record()
			self.draw()
			self.status.redraw_infos(self.data.get_score(), self.data.get_undos_remaining())

	def draw_tile(self):
		if None in [i for li in self.data.matrix for i in li]:
			self.data.add_tile()
			self.data.record()
			self.draw()
			self.judge()
			# self.data.record()

	def new_tile(self) -> None: 
		"""
		Adds a new tile to the model and redraws. If the game has
		been lost with the addition of the new tile, then the player should be prompted with the
		appropriate messagebox displaying the LOSS_MESSAGE.
		"""
		self.root.after(150, self.draw_tile)
		# self.draw()		

	def reset(self) -> None:
		self.data.new_game()
		self.view.clear()

	def judge(self):
		if self.data.has_won() == True:
			res = tkMessageBox.askyesno(title="2048", message=WIN_MESSAGE)
			if res:
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

def play_game(root):
	game = Game(root)
	game.main()
	game.view.pack()

if __name__ == '__main__':
	root = tk.Tk()
	play_game(root)
	root.mainloop()
