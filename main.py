from assets.search_func import *
import tracemalloc
import json
import time

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

def measure(state, index, search, is_render):
    is_found_ans = False
    run_time = 0
    mem_usage = 0  # Bộ nhớ peak, tính bằng KB

    if search == "DFS":
        tracemalloc.start()  # Bắt đầu theo dõi bộ nhớ
        start_time = time.perf_counter()
        move_history = []
        is_found_ans = dfs(state, move_history, is_render)
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        run_time = (end_time - start_time) * 1000  # ms
        mem_usage = peak / 1024  # KB

    elif search == "Heuristic":
        tracemalloc.start()
        start_time = time.perf_counter()
        is_found_ans, move_history = steppest_hill_climbing(init_state=state, is_render=is_render)
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        run_time = (end_time - start_time) * 1000  # ms
        mem_usage = peak / 1024

    print(f"    Testcase {index}: is_found_ans: {is_found_ans}, time: {run_time:.2f} ms, memory: {mem_usage:.2f} KB")

    return is_found_ans, run_time, mem_usage

    
def read_testcase(file_address, search, is_render):
    with open(file_address, "r") as file:
        testcase = json.load(file)

    total_time = []
    for i, test in enumerate(testcase):
        state = create_state(testcase[test])
        total_time.append(measure(state, i, search, is_render))
    
    return total_time
        
def evaluate(search, is_render):
    print(f"Evaluate {search} function:")
    for i in range(4, 9):
        file_address = f'test/chess_{i}.json'
        print(f"Testcase {i} pieces: ")

        total_time = read_testcase(file_address, search, is_render)

        num_success = 0
        total_run_time = 0
        total_mem_usage = 0

        for success, run_time, mem_usage in total_time:
            if success:
                num_success += 1
            total_run_time += run_time
            total_mem_usage += mem_usage

        print(f"{search} success: {num_success}/{len(total_time)}, average time: {total_run_time / len(total_time)} ms, average memory: {total_mem_usage / len(total_time)} KB")

    print("----------------------------------------------------------------------------------------")

if __name__ == "__main__":
    BOARD_SIZE = 8
    is_render = False
    search_method = ["DFS", "Heuristic"]

    for search in search_method:
        evaluate(search, is_render)



