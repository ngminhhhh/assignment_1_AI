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

def steppest_hill_climbing(init_state, alpha=4.0, perturbation_prob=0.8, is_render=False):
    success = True
    current_state = [p.clone() for p in init_state]
    current_h = heuristic_func(current_state, alpha)
    move_history = []

    while len(current_state) > 1:
        neighbors = []

        for piece in current_state:
            valid_moves = piece.get_valid_moves(current_state)

            for (nx, ny, captured) in valid_moves:
                cloned_state = [p.clone() for p in current_state]

                captured_piece = None
                for p in cloned_state:
                    if p.x == captured.x and p.y == captured.y and p.type == captured.type:
                        captured_piece = p
                        break
                if captured_piece is None:
                    continue  
                cloned_state.remove(captured_piece)

                moving_piece = None
                for p in cloned_state:
                    if p.x == piece.x and p.y == piece.y and p.type == piece.type:
                        moving_piece = p
                        break
                if moving_piece is None:
                    continue

                old_pos = (moving_piece.x, moving_piece.y)

                moving_piece.moves(nx, ny)

                new_h = heuristic_func(cloned_state, alpha)
                move_info = {
                    "type": "move",
                    "piece": moving_piece.type,
                    "old_pos": old_pos,
                    "new_pos": (nx, ny),
                    "captured": captured.type
                }
                neighbors.append((new_h, cloned_state, move_info))

        if not neighbors:
            if is_render:
                print("No neighbors available. Terminating hill climbing.")
            success = False
            break

 
        best_neighbor = min(neighbors, key=lambda x: x[0])
        best_h, best_state, best_move_info = best_neighbor

        if best_h < current_h:
            current_state = best_state
            current_h = best_h
            move_history.append(best_move_info)
            if is_render:
                print("Improved heuristic:", current_h)
                render(current_state, best_move_info)

        else:
            if random.random() < perturbation_prob:
                random_neighbor = random.choice(neighbors)
                current_state = random_neighbor[1]
                current_h = random_neighbor[0]
                move_history.append(random_neighbor[2])
                if is_render:
                    print("Perturbation move. New heuristic:", current_h)
                    render(current_state, random_neighbor[2])
            else:
                if is_render:
                    print("No improvement and no perturbation. Stopping hill climbing.")
                success = False
                break

    return success, move_history

def dfs(state, move_history, is_render=False):
    if len(state) == 1:
        return True

    for piece in state:
        valid_moves = piece.get_valid_moves(state)

        for (nx, ny, captured) in valid_moves:
            cloned_state = [p.clone() for p in state]

            captured_piece = None
            for p in cloned_state:
                if p.x == captured.x and p.y == captured.y and p.type == captured.type:
                    captured_piece = p
                    break
            if captured_piece is None:
                continue  
            cloned_state.remove(captured_piece)

            moving_piece = None
            for p in cloned_state:
                if p.x == piece.x and p.y == piece.y and p.type == piece.type:
                    moving_piece = p
                    break
            if moving_piece is None:
                continue 

            old_pos = (moving_piece.x, moving_piece.y)
            moving_piece.moves(nx, ny)

            move_info = {
                "type": "move",
                "piece": moving_piece.type,
                "old_pos": old_pos,
                "new_pos": (nx, ny),
                "captured": captured.type
            }
            move_history.append(move_info)
            
            if is_render:
                render(cloned_state, move_info)

            if dfs(cloned_state, move_history, is_render):
                return True
            
            move_history.pop()
            move_info["type"] = "undo"
            if is_render:
                render(state, move_info)
                
    return False


