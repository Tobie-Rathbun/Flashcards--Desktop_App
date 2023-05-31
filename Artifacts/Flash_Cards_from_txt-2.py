import tkinter as tk
from tkinter import ttk


def show_flashcards(flashcards):
    def flip_card():
        nonlocal current_card_index, is_front_shown
        is_front_shown = not is_front_shown
        if is_front_shown:
            card_text.set(flashcards[current_card_index][0])  # Show front of the card
            flip_button.config(text="Flip to Back")
        else:
            card_text.set(flashcards[current_card_index][1])  # Show back of the card
            flip_button.config(text="Flip to Front")

    def next_card():
        nonlocal current_card_index, is_front_shown
        current_card_index = (current_card_index + 1) % len(flashcards)
        is_front_shown = True
        card_text.set(flashcards[current_card_index][0])  # Show front of the next card
        flip_button.config(text="Flip to Back")

    # Create the main window
    window = tk.Tk()
    window.title("Flashcards")
    window.geometry("600x400")  # Set the window size

    # Configure dark mode theme
    window.configure(bg="black")

    # Configure styles
    style = ttk.Style()
    style.configure("TLabel", background="#333333", foreground="white", padding=(30, 15, 30, 15))
    style.configure("TButton", background="black", font=("Helvetica", 14), padding=(10, 10, 10, 5))

    # Create the card frame
    card_frame = ttk.Frame(window, style="CardFrame.TFrame")
    card_frame.pack(pady=50)

    # Configure the boundary box around the text
    card_frame.configure(padding=20)
    card_frame.configure(relief="solid")
    card_frame.configure(borderwidth=2)

    # Configure the card frame style
    style.configure("CardFrame.TFrame", background="#333333")

    # Initialize card display
    current_card_index = 0
    is_front_shown = True

    card_text = tk.StringVar()
    card_text.set(flashcards[current_card_index][0])  # Show the front of the first card

    # Create card label
    card_label = ttk.Label(card_frame, textvariable=card_text)
    card_label.pack(padx=10, pady=10)

    # Create flip button
    flip_button = ttk.Button(window, text="Flip to Back", command=flip_card)
    flip_button.pack(pady=20)

    # Create next button
    next_button = ttk.Button(window, text="Next Card", command=next_card)
    next_button.pack(pady=10)

    # Configure hover styles for buttons
    style.map("TButton",
              foreground=[("active", "black"), ("!active", "white")],
              background=[("active", "white"), ("!active", "black")])

    # Start the application
    window.mainloop()

def generate_flashcards(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    flashcards = []
    current_front = None
    current_back = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            if line[0].isspace():
                if current_front is not None:
                    current_back.append(stripped_line)
            else:
                if current_front is not None:
                    flashcards.append((current_front, "\n".join(current_back)))
                current_front = stripped_line
                current_back = []

    if current_front is not None:
        flashcards.append((current_front, "\n".join(current_back)))

    return flashcards


filename = "flashcards.txt"  # Replace with your file name
flashcards = generate_flashcards(filename)
show_flashcards(flashcards)


