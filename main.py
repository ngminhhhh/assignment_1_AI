from assets.search_func import *
import json

def create_state(test):
    state = []
    for piece_info in test:
        for type, pos in piece_info.items():
            x = 8 - int(pos[1])
            y = ord(pos[0]) - 65

            if type == "Knight":
                state.append(Knight(x, y))
            elif type == "King":
                state.append(King(x, y))
            elif type == "Rook":
                state.append(Rook(x, y))
            elif type == "Queen":
                state.append(Queen(x, y))
            elif type == "Bishop":
                state.append(Bishop(x, y))
            elif type == "Pawn":
                state.append(Pawn(x, y))
            else:
                print("Didn\'t exist")

    return state

def read_testcase(file_address):
    with open(file_address, "r") as file:
        testcase = json.load(file)

    for test in testcase:
        state = create_state(testcase[test])
        print(test)
        render(state)

if __name__ == "__main__":
    BOARD_SIZE = 8
    read_testcase("test/chess_4.json")

