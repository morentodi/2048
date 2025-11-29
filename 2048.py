import curses
import random


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.timeout(100)

    # warna tiles
    curses.start_color()
    colors = {
        0: 1, 2: 2, 4: 3, 8: 4, 16: 5, 32: 6,
        64: 7, 128: 8, 256: 9, 512: 10, 1024: 11, 2048: 12
    }
    for v, p in colors.items():
        curses.init_pair(p, curses.COLOR_BLACK if v <= 4 else curses.COLOR_WHITE,
                         curses.COLOR_YELLOW if v == 0 else (v % 7) + 1)

    board = [[0]*4 for _ in range(4)]
    score = 0
    game_over = False

    def spawn():
        empty = [(r, c) for r in range(4)
                 for c in range(4) if board[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            board[r][c] = 4 if random.random() < 0.1 else 2

    def draw():
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        if h < 20 or w < 40:
            stdscr.addstr(0, 0, "Terminal terlalu kecil! Min 40x20.")
            stdscr.refresh()
            return

        title = "2048 GAME"
        stdscr.addstr(1, (w-len(title))//2, title, curses.A_BOLD)
        sc = f"Score: {score}"
        stdscr.addstr(2, (w-len(sc))//2, sc)

        gx = (w - 29)//2
        gy = 4

        # border atas
        stdscr.addstr(gy, gx, "+------"*4 + "+")

        for r in range(4):
            row_y = gy + 1 + r*2
            stdscr.addstr(row_y, gx, "|")

            for c in range(4):
                v = board[r][c]
                text = f"{v:^6}" if v else " "*6
                attr = curses.color_pair(colors.get(v, 1)) | curses.A_BOLD
                stdscr.addstr(row_y, gx+1 + c*7, text, attr)
                stdscr.addstr(row_y, gx+7 + c*7, "|")

            stdscr.addstr(row_y+1, gx, "+------"*4 + "+")

        msg = "WASD = gerak | R = restart | Q = keluar"

        if game_over:
            msg = "GAME OVER! Tekan R untuk restart."

        stdscr.addstr(gy+10, (w-len(msg))//2, msg, curses.A_BOLD)

        extra = "Ko Wilbert Ganteng Banget"
        stdscr.addstr(gy+12, (w-len(extra))//2, extra, curses.A_BOLD)

        stdscr.refresh()

    def merge(line):
        new = [x for x in line if x != 0]
        i = 0
        s = 0
        while i < len(new)-1:
            if new[i] == new[i+1]:
                new[i] *= 2
                s += new[i]
                new.pop(i+1)
            i += 1
        new += [0]*(4-len(new))
        return new, s

    def move(dir):
        nonlocal score
        moved = False

        if dir == "L":
            for r in range(4):
                new, add = merge(board[r])
                if new != board[r]:
                    moved = True
                board[r] = new
                score += add

        elif dir == "R":
            for r in range(4):
                rev = board[r][::-1]
                new, add = merge(rev)
                new = new[::-1]
                if new != board[r]:
                    moved = True
                board[r] = new
                score += add

        elif dir == "U":
            for c in range(4):
                col = [board[r][c] for r in range(4)]
                new, add = merge(col)
                for r in range(4):
                    if board[r][c] != new[r]:
                        moved = True
                    board[r][c] = new[r]
                score += add

        elif dir == "D":
            for c in range(4):
                col = [board[r][c] for r in range(4)][::-1]
                new, add = merge(col)
                new = new[::-1]
                for r in range(4):
                    if board[r][c] != new[r]:
                        moved = True
                    board[r][c] = new[r]
                score += add

        return moved

    def check_over():
        if any(0 in row for row in board):
            return False
        for r in range(4):
            for c in range(3):
                if board[r][c] == board[r][c+1]:
                    return False
                if board[c][r] == board[c+1][r]:
                    return False
        return True

    # awal
    spawn()
    spawn()

    while True:
        draw()
        key = stdscr.getch()

        if key == ord('q'):
            break
        if key == ord('r'):
            board = [[0]*4 for _ in range(4)]
            score = 0
            game_over = False
            spawn()
            spawn()
            continue

        if game_over:
            continue

        direction = None
        if key in (ord('a'), ord('A')):
            direction = "L"
        elif key in (ord('d'), ord('D')):
            direction = "R"
        elif key in (ord('w'), ord('W')):
            direction = "U"
        elif key in (ord('s'), ord('S')):
            direction = "D"

        if direction and move(direction):
            spawn()
            if check_over():
                game_over = True


curses.wrapper(main)
