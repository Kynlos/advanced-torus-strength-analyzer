import curses
import importlib
import os
from main import calculate_torus_stresses, fatigue_analysis
from modules import advanced_calculations
from visualization import create_advanced_animation

def load_modules():
    modules = {}
    module_dir = "modules"
    for filename in os.listdir(module_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module = importlib.import_module(f"{module_dir}.{module_name}")
            if hasattr(module, "run_analysis"):
                modules[module_name.replace("_", " ").title()] = module.run_analysis
    return modules

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    modules = load_modules()
    menu_options = list(modules.keys())

    current_option = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        stdscr.addstr(0, 0, "Advanced Torus Strength Analyzer")
        stdscr.addstr(1, 0, "Use up/down arrows to navigate, enter to select, 'q' to quit")

        for i, option in enumerate(menu_options):
            if i == current_option:
                stdscr.addstr(i+3, 0, f"{i+1}. {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(i+3, 0, f"{i+1}. {option}")

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            current_option = (current_option - 1) % len(menu_options)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(menu_options)
        elif key == 10:  # Enter key
            selected_module = menu_options[current_option]
            curses.endwin()
            modules[selected_module](calculate_torus_stresses, fatigue_analysis, advanced_calculations, create_advanced_animation)
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            stdscr.keypad(True)

def run_tui():
    curses.wrapper(main_menu)

if __name__ == "__main__":
    from main import calculate_torus_stresses, fatigue_analysis, advanced_calculations
    from visualization import create_advanced_animation
    run_tui()
