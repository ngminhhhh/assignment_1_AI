from assets.piece import *
from assets.render_func import *
import random

def heuristic_func(state, alpha = 1.0):
    '''
        return number of pieces + number of valid steps - 1
    '''
    if len(state) == 1:
        return -float("inf")

    n = len(state)
    cost = 0
    for piece in state:
        cost += len(piece.get_valid_moves(state))

    return n * alpha - cost

def steppest_hill_climbing(init_state, alpha = 1.0, perturbation_prob = 0.8):
    num = 0
    current_state = [p.clone() for p in init_state]

    current_h = heuristic_func(current_state, alpha)
    move_history = []

    while len(current_state) > 1:
        neighbors = []
        num += 1

        for i, piece in enumerate(current_state):
            valid_moves = piece.get_valid_moves(current_state)

            for (nx, ny, captured) in valid_moves:
                new_state = [p.clone() for p in current_state]
                moving_piece = new_state[i]

                old_pos = (moving_piece.x, moving_piece.y)
                new_state = [p for p in new_state if not (p.x == captured.x and p.y == captured.y and p.type == captured.type)]

                moving_piece.moves(nx, ny)

                h_val = heuristic_func(new_state, alpha)
                # Generate all neighbors and calculate each neighbor's heuristic
                move_info = {
                    "type": "move",
                    "piece": moving_piece.type,
                    "old_pos": old_pos,
                    "new_pos": (nx, ny),
                    "captured": captured.type
                }
                neighbors.append((h_val, new_state, move_info))

        if not neighbors:
            print("No neighbors available. Terminating hill climbing.")
            break

        # choose the best neighbor
        best_neighbor = min(neighbors, key=lambda x: x[0])
        best_h, best_state, best_move_info = best_neighbor

        if best_h < current_h:
            current_state = best_state
            current_h = best_h
            move_history.append(best_move_info)
            print("Improved heuristic:", current_h)
            render(current_state, best_move_info)
        # using Random Perturbation
        else:
            if random.random() < perturbation_prob:
                random_neighbor = random.choice(neighbors)
                current_state = random_neighbor[1]
                current_h = random_neighbor[0]
                move_history.append(random_neighbor[2])
                print("Perturbation move. New heuristic:", current_h)
                render(current_state, random_neighbor[2])
            else:
                print("No improvement and no perturbation. Stopping hill climbing.")
                break

    return num, move_history

def dfs(state, move_history):
    # Goal state
    if (len(state) == 1):
        return True
    
    for i, piece in enumerate(state):
        valid_moves = piece.get_valid_moves(state)

        for (nx, ny, captured) in valid_moves:
            # Clone new state with that move
            new_state = [p.clone() for p in state]
            # Take the piece that will move
            moving_piece = new_state[i]
            # Store old position of moving piece
            old_pos = (moving_piece.x, moving_piece.y)

            # delete captured piece
            new_state = [p for p in new_state if not (p.x == captured.x and p.y == captured.y and p.type == captured.type)]
                
            moving_piece.moves(nx, ny)

            move_info = {
                "type": "move",
                "piece": moving_piece.type,
                "old_pos": old_pos,
                "new_pos": (nx, ny),
                "captured": captured.type
            }

            move_history.append(move_info)
            render(new_state, move_info)

            if dfs(new_state, move_history):
                return True
            
            # backtracking
            move_history.pop()
            move_info["type"] = "undo"
            render(state, move_info)

    return False

