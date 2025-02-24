def map_to_block(pos, board_size = 8):
    x, y = pos
    return chr(y + 65) + str(board_size - x) 

def render(state, move_info = None, board_size = 8):
    # Mapping table
    abbr = {
        "King": "K",
        "Knight": "N",
        "Queen": "Q",
        "Rook": "R",
        "Bishop": "B",
        "Pawn": "P"
    }
    
    # Print move infomation
    if move_info is None:
        print(f"Begining state")
    else:
        if move_info["type"] == "move":
            print(f"Move {move_info['piece']} from {map_to_block(move_info['old_pos'])} capture {move_info['captured']} at {map_to_block(move_info['new_pos'])}")
        elif move_info["type"] == "undo":
            print(f"Place back {move_info['piece']} at {map_to_block(move_info['old_pos'])} and {move_info['captured']} at {map_to_block(move_info['new_pos'])}")

    grid = [["." for _ in range(board_size)] for _ in range(board_size)]
    for piece in state:
        symbol = abbr[piece.type]
        grid[piece.x][piece.y] = symbol

    header = "  " + "  ".join(chr(i + 65) for i in range(board_size))
    print(" " + "-" * (3 * board_size))

    for i in range(board_size):
        row_str = "| " + "  ".join(grid[i]) + f" |{(board_size - i):2} "
        print(row_str)
    print(" " + "-" * (3 * board_size))
    print(header)
    print()  

