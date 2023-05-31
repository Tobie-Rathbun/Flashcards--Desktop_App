import tkinter as tk


class FlashcardApp:
    def __init__(self, flashcards):
        self.flashcards = flashcards
        self.current_card_index = 0

        self.root = tk.Tk()
        self.root.title("Flashcard App")

        self.front_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.front_label.pack(pady=10)

        self.back_label = tk.Label(self.root, text="", font=("Arial", 12), wraplength=400)
        self.back_label.pack(pady=10)

        self.flip_button = tk.Button(self.root, text="Flip", command=self.flip_card)
        self.flip_button.pack(pady=5)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_card)
        self.next_button.pack(pady=5)

        self.update_card()

        self.root.mainloop()

    def update_card(self):
        if self.current_card_index < len(self.flashcards):
            current_card = self.flashcards[self.current_card_index]
            self.front_label.configure(text=current_card[0])
            self.back_label.configure(text="")
        else:
            self.front_label.configure(text="No more flashcards.")
            self.back_label.configure(text="")
            self.flip_button.configure(state=tk.DISABLED)
            self.next_button.configure(state=tk.DISABLED)

    def flip_card(self):
        if self.current_card_index < len(self.flashcards):
            current_card = self.flashcards[self.current_card_index]
            back_text = "\n".join(current_card[1:])
            self.back_label.configure(text=back_text)

    def next_card(self):
        self.current_card_index += 1
        self.update_card()


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








# Example usage
notes_file = 'notes.txt'
flashcards = generate_flashcards(notes_file)

app = FlashcardApp(flashcards)
