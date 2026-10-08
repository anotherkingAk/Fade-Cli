from __future__ import annotations
import shutil, sys, time

RESET="\033[0m"; DIM="\033[2m"; BOLD="\033[1m"; CYAN="\033[36m"; VIOLET="\033[95m"; GREEN="\033[32m"; YELLOW="\033[33m"; RED="\033[31m"

def width(): return shutil.get_terminal_size((80,24)).columns

def logo():
    return f"{VIOLET}        ╭──────────────╮{RESET}\n{VIOLET}     ╭──╯              ╰──╮{RESET}\n{VIOLET}    ╱                      ╲{RESET}\n{VIOLET}   │        ▮      ▮        │{RESET}\n{VIOLET}   │                        │{RESET}\n{VIOLET}    ╲                      ╱{RESET}\n{VIOLET}     ╰───────╮  ╭─────────╯{RESET}\n{VIOLET}             ╰──╯{RESET}"

def title():
    w=width()
    if w<52: return f"{VIOLET}◇{RESET} {BOLD}FADE{RESET} {DIM}1.1{RESET}"
    return f"{VIOLET}◇{RESET} {BOLD}FADE{RESET} {DIM}1.1 · local coding agent{RESET}"

def status(label, detail=""):
    if detail and width()>=60: print(f"{CYAN}│{RESET} {label} {DIM}{detail}{RESET}")
    else: print(f"{CYAN}│{RESET} {label}")

def think(label="Thinking"):
    frames="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for ch in frames:
        print(f"\r{VIOLET}{ch}{RESET} {label}…", end="", flush=True); time.sleep(.035)
    print("\r"+" "*min(width(),42)+"\r", end="")

def ok(s): print(f"{GREEN}✓{RESET} {s}")
def warn(s): print(f"{YELLOW}!{RESET} {s}")
def err(s): print(f"{RED}×{RESET} {s}")
