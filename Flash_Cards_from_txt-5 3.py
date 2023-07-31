import tkinter as tk
from tkinter import ttk
import random

def show_flashcards(flashcards):
    # Create the main window
    window = tk.Tk()
    window.title("Flashcards")
    window.geometry("1200x800")  # Set the window size
    window.configure(background='black')

    # Initialize card display
    current_card_index = 0
    is_front_shown = True
    card_history = []  # The list to keep track of the cards shown
    history_index = -1  # The index in the history list of the currently shown card

    # Configure styles
    style = ttk.Style()
    style.configure("TLabel", background="white", foreground="#333333", padding=(30, 15, 30, 15))
    style.configure("TButton", background="black", font=("Helvetica", 14), padding=(10, 10, 10, 5))

    # Create the outer card frame that acts as padding
    outer_card_frame = tk.Frame(window, bg="#333333")
    outer_card_frame.pack(pady=50, padx=100)

    # Create the inner card frame where the card resides
    inner_card_frame = tk.Frame(outer_card_frame, bg="#333333")
    inner_card_frame.pack(padx=25, pady=25)

    # Initialize card display
    current_card_index = 0
    is_front_shown = True

    title_text = tk.StringVar()
    title_text.set(flashcards[current_card_index][0])  # Show the title of the first card

    line_text = tk.StringVar()
    line_text.set("Line: "+str(flashcards[current_card_index][3]))  # Show the line number of the first card

    card_text = tk.StringVar()
    card_text.set(flashcards[current_card_index][1])  # Show the front of the first card

    # Configure the style for title and line label
    style.configure("Title.TLabel", font=("Helvetica", 14, 'bold'))

    # Create title label
    title_label = ttk.Label(window, textvariable=title_text, style="Title.TLabel", background='black', foreground='white')
    title_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Create line label
    line_label = ttk.Label(window, textvariable=line_text, style="Title.TLabel", background='black', foreground='white')
    line_label.pack(side=tk.RIGHT, padx=10, pady=10)

    # Create card label with larger font
    card_label = tk.Text(inner_card_frame, font=("Helvetica", 16), wrap='word', height=20, state='disabled', 
                         bg='#333333', fg='white', bd=0)  # Set the background, foreground colors and border
    card_label.config(highlightthickness=0, borderwidth=0)
    card_label.pack(fill='both', expand=True)

    def update_card_text(card_index):
        card_label.config(state='normal')
        card_label.delete('1.0', tk.END)

        # If we are showing the question, align it to the center
        if is_front_shown:
            card_label.tag_configure("center", justify='center')
            card_label.insert(tk.END, '\n\n' + flashcards[card_index][1] + '\n\n', "center")
        else:  # If we are showing the answer, left align it and add some padding
            card_label.tag_configure("left", justify='left', lmargin1=25, lmargin2=25)  # Apply padding to the left margin
            card_label.insert(tk.END, flashcards[card_index][2], "left")

        card_label.config(state='disabled')

    def flip_card():
        nonlocal current_card_index, is_front_shown
        is_front_shown = not is_front_shown
        update_card_text(current_card_index)
        flip_button.config(text="Flip to Back" if is_front_shown else "Flip to Front")

    def next_card():
        nonlocal current_card_index, is_front_shown, history_index
        current_card_index = random.choice(range(len(flashcards)))  # Shuffle selection of cards
        is_front_shown = True
        # Add the card to history only if it's not already the last card in history
        if len(card_history) == 0 or (len(card_history) > 0 and card_history[-1] != current_card_index):
            card_history.append(current_card_index)  # Add this card to the history
            history_index += 1  # Update the history index

        title_text.set(flashcards[current_card_index][0])  # Show the section title
        line_text.set("Line: "+str(flashcards[current_card_index][3]))  # Show the line number
        update_card_text(current_card_index)
        flip_button.config(text="Flip to Back")

    def next_history():
        nonlocal current_card_index, is_front_shown, history_index
        # Simply increment the history index and set the current_card_index
        if history_index + 1 < len(card_history):  # Make sure we're within the history range
            history_index += 1
            current_card_index = card_history[history_index]  # Get the next card from the history
            is_front_shown = True

            title_text.set(flashcards[current_card_index][0])  # Show the section title
            line_text.set("Line: "+str(flashcards[current_card_index][3]))  # Show the line number
            update_card_text(current_card_index)
            flip_button.config(text="Flip to Back")


    def prev_history():
        nonlocal current_card_index, is_front_shown, history_index
        if history_index > 0:  # If there is a previous card in the history
            history_index -= 1
            current_card_index = card_history[history_index]  # Get the previous card from the history
            is_front_shown = True

            title_text.set(flashcards[current_card_index][0])  # Show the section title
            line_text.set("Line: "+str(flashcards[current_card_index][3]))  # Show the line number
            update_card_text(current_card_index)
            flip_button.config(text="Flip to Back")

    def try_next_history():
        if history_index + 1 < len(card_history):
            next_history()
        else:
            next_card()


    update_card_text(current_card_index)

    # Create Scrollbar
    scrollbar = tk.Scrollbar(inner_card_frame, width=0)
    scrollbar.pack(side='right', fill='y')

    def update_scrollbar(*args):
        # If the entire content fits within the window, make the scrollbar as thin as possible
        if card_label.yview()[1] == 1.0:
            scrollbar.configure(width=0)
        else:  # Restore the scrollbar's width
            scrollbar.configure(width=16)

    # Configure Scrollbar
    card_label.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=card_label.yview)
    card_label.bind('<<Change>>', update_scrollbar)

    # Create button frame
    button_frame = tk.Frame(window, background='black')
    button_frame.pack(pady=10)

    # Create flip button
    flip_button = ttk.Button(button_frame, text="Flip to Back", command=flip_card)
    flip_button.pack(side=tk.LEFT, padx=5)

    # Next button command
    next_button = ttk.Button(button_frame, text="Next Card", command=next_card)
    next_button.pack(side=tk.LEFT, padx=5)

    # Configure hover styles for buttons
    style.map("TButton",
              foreground=[("active", "black"), ("!active", "dark grey")],
              background=[("active", "white"), ("!active", "black")])

    # Keyboard controls
    window.bind('<Left>', lambda event: prev_history())  # Show previous card with left arrow key
    window.bind('<Right>', lambda event: try_next_history())  # Show next card with right arrow key
    window.bind('<space>', lambda event: flip_card())  # Flip card with spacebar

    # Start the application
    window.mainloop()


def generate_flashcards(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    flashcards = []
    current_front = None
    current_back = []
    section_title = None  # To hold the section title
    line_number = 1  # Starting line number
    question_start_line = 1  # To store the line number where the question starts

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            # Check if line is a section title
            if stripped_line[0] == "\\":
                section_title = stripped_line[1:]
            # Check if line is a comment
            elif stripped_line[0] == "/":
                pass  # Do nothing for comment lines
            # If line is indented, add it to the current back
            elif line[0].isspace():
                if current_front is not None:
                    current_back.append(line)  # Keep the entire line
            else:
                # If we're starting a new front, save the previous one
                if current_front is not None:
                    flashcards.append((section_title, current_front, "\n".join(current_back), question_start_line))
                # Start a new front
                current_front = stripped_line
                current_back = []
                question_start_line = line_number  # Store the line number where the question starts

        line_number += 1  # Increment line number after each line, regardless of its content

    # Save the last flashcard
    if current_front is not None:
        flashcards.append((section_title, current_front, "\n".join(current_back), question_start_line))

    random.shuffle(flashcards)  # Shuffle the flashcards

    return flashcards



filename = "flashcards.txt"  # Replace with your file name
flashcards = generate_flashcards(filename)
show_flashcards(flashcards)
