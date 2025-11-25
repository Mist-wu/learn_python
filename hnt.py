import turtle
import time

# Configuration
NUM_DISKS = 5
SPEED = 3  # 1 (slowest) to 10 (fastest), or 0 (no animation)

# Setup screen
screen = turtle.Screen()
screen.title("Tower of Hanoi Visualization")
screen.setup(width=800, height=600)
screen.tracer(0)  # Turn off automatic updates for faster drawing setup

# Peg positions
PEG_COORDS = {
    'A': -250,
    'B': 0,
    'C': 250
}
PEG_HEIGHT = 300
BASE_Y = -100

# Stacks to hold disks
pegs = {
    'A': [],
    'B': [],
    'C': []
}

def create_disk(n, total_disks):
    t = turtle.Turtle()
    t.shape("square")
    t.penup()
    t.speed(SPEED)
    
    # Width relative to disk number (largest at bottom)
    width_stretch = (n / total_disks) * 10 + 2
    t.shapesize(stretch_wid=1, stretch_len=width_stretch)
    
    # Color gradient
    colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    t.color(colors[(n-1) % len(colors)])
    
    return t

def init_game():
    # Draw pegs
    for name, x in PEG_COORDS.items():
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        t.penup()
        
        # Draw base line
        t.goto(x - 100, BASE_Y)
        t.pendown()
        t.forward(200)
        t.penup()
        
        # Draw vertical peg
        t.goto(x, BASE_Y)
        t.pendown()
        t.left(90)
        t.forward(PEG_HEIGHT)
        t.penup()
        
        # Label
        t.goto(x, BASE_Y - 30)
        t.write(name, align="center", font=("Arial", 16, "bold"))

    # Create disks on Peg A
    for i in range(NUM_DISKS, 0, -1):
        disk = create_disk(i, NUM_DISKS)
        pegs['A'].append(disk)
        update_disk_position(disk, 'A', len(pegs['A']) - 1)
    
    screen.update()
    screen.tracer(1) # Turn animation back on

def update_disk_position(disk, peg_name, index):
    x = PEG_COORDS[peg_name]
    y = BASE_Y + 20 * index + 12 # 20 is approx height of disk
    disk.goto(x, y)

def move_visual_disk(source, target):
    disk = pegs[source].pop()
    
    # Animation path
    # 1. Move up
    disk.goto(PEG_COORDS[source], BASE_Y + PEG_HEIGHT + 20)
    # 2. Move horizontal
    disk.goto(PEG_COORDS[target], BASE_Y + PEG_HEIGHT + 20)
    # 3. Move down
    pegs[target].append(disk)
    update_disk_position(disk, target, len(pegs[target]) - 1)

def hanoi(n, source, auxiliary, target):
    if n > 0:
        # Move n-1 disks from source to auxiliary
        hanoi(n-1, source, target, auxiliary)
        
        # Move the nth disk from source to target
        move_visual_disk(source, target)
        
        # Move the n-1 disks from auxiliary to target
        hanoi(n-1, auxiliary, source, target)

if __name__ == "__main__":
    init_game()
    time.sleep(1)
    hanoi(NUM_DISKS, 'A', 'B', 'C')
    screen.mainloop()