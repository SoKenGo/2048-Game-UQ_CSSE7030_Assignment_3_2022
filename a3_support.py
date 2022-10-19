import random
from typing import Optional

NUM_COLS = NUM_ROWS = 4
BACKGROUND_COLOUR = '#bbada0'
LIGHT = '#f5ebe4'
DARK = '#615b56'
COLOURS = {
    None: '#ccc0b3',
    2: "#fcefe6",
    4: "#f2e8cb",
    8: "#f5b682",
    16: "#f29446",
    32: "#ff775c",
    64: "#e64c2e",
    128: "#ede291",
    256: "#fce130",
    512: "#ffdb4a",
    1024: "#f0b922",
    2048: "#fad74d"
}
FG_COLOURS = {
    2: DARK,
    4: DARK,
    8: LIGHT,
    16: LIGHT,
    32: LIGHT,
    64: LIGHT,
    128: LIGHT,
    256: LIGHT,
    512: LIGHT,
    1024: LIGHT,
    2048: LIGHT,
}

TITLE_FONT = ('Arial bold', 50)
TILE_FONT = ('Arial bold', 30)

LEFT = 'a'
UP = 'w'
DOWN = 's'
RIGHT = 'd'

NEW_TILE_DELAY = 150
MAX_UNDOS = 3

WIN_MESSAGE = 'You won! Would you like to play again?'
LOSS_MESSAGE = 'You lost :( Play again?'

BOARD_WIDTH = 400
BOARD_HEIGHT = 400
BUFFER = 10

def generate_tile(current_tiles: list[list[Optional[int]]]) -> tuple[tuple[int, int], int]:
    """ Generates a random position for a new tile, and the number (either 2 or
    4) to display on that tile.

    Parameters:
        current_tiles: The tiles currently on the grid. This is a list of rows
                       in the grid (i.e. each internal list represents one
                       row), where each element is the number on the tile (or
                       None if no tile exists) at the corresponding row in the
                       column.

    Returns:
        A tuple containing ((row, column), value), where (row, column) is the
        position for the new tile, and value is the value for that tile (either
        2 or 4.)
    """
    candidate_positions = []
    for i, row in enumerate(current_tiles):
        for j, tile in enumerate(row):
            if tile is None:
                candidate_positions.append((i, j))
    return random.choice(candidate_positions), random.choice([2] * 5 + [4])

def stack_left(tiles: list[list[Optional[int]]]) -> list[list[Optional[int]]]:
    """ Moves all tiles as far as possible to the left without merging.

    Parameters:
        tiles: The tiles currently on the grid, where each internal list
               represents a row in the grid.

    Returns:
        A copy of the tiles list, in which all the tiles have stacked to the left.
    """
    stacked_tiles = [[None for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    for i in range(NUM_ROWS):
        to_fill = 0
        for j in range(NUM_COLS):
            if tiles[i][j] is not None:
                stacked_tiles[i][to_fill] = tiles[i][j]
                to_fill += 1
    return stacked_tiles

def combine_left(tiles: list[list[Optional[int]]]) -> list[list[Optional[int]]]:
    """ Merges tiles to the left (i.e. if two 8's are next to each other
    horizontally, this method will merge them together into a single 16 tile,
    which sits as far left as possible.)

    Parameters:
        tiles: The tiles currently on the grid, where each internal list
               represents a row in the grid.

    Returns:
        A copy of the tiles list, in which merges have been made to the left.
    """
    combined_tiles = [row[:] for row in tiles]
    score_added = 0
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS - 1):
            if combined_tiles[i][j] is not None and combined_tiles[i][j] == combined_tiles[i][j + 1]:
                combined_tiles[i][j] *= 2
                combined_tiles[i][j + 1] = None
                score_added += combined_tiles[i][j]
    return combined_tiles, score_added

def reverse(tiles: list[list[Optional[int]]]) -> list[list[Optional[int]]]:
    """ Flips the grid of tiles horizontally.

    Parameters:
        tiles: The tiles currently on the grid, where each internal list
               represents a row in the grid.

    Returns:
        A copy of the tiles list, which has been flipped horizontally.
    """
    reversed_tiles = []
    for i in range(NUM_ROWS):
        reversed_tiles.append([])
        for j in range(NUM_COLS):
            reversed_tiles[i].append(tiles[i][3-j])
    return reversed_tiles

def transpose(tiles: list[list[Optional[int]]]) -> list[list[Optional[int]]]:
    """ Transposes the grid of tiles.

    Parameters:
        tiles: The tiles currently on the grid, where each internal list
               represents a row in the grid.

    Returns:
        A copy of the tiles, transposed.
    """
    transposed_tiles = [[None for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            transposed_tiles[i][j] = tiles[j][i]
    return transposed_tiles
