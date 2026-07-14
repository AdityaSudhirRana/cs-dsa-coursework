import os
import time
from termcolor import colored, cprint

import sys
import tkinter as tk
from tkinter import messagebox, ttk


class Stack:
    def __init__(self):
        self.books_stack = []

    def is_empty(self):
        return len(self.books_stack) == 0

    def push(self, book):
        self.books_stack.append(book)
        print(colored(f"'{book}' has been pushed into the books_stack", "green"))
        self.animate_push(book)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from an empty stack!")
        book = self.books_stack.pop()
        print(colored(f"'{book}' has been popped out!", "red"))
        self.animate_pop(book)
        return book

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self.books_stack[-1]

    def size(self):
        return len(self.books_stack)

    def __str__(self):
        return " <- ".join(reversed(self.books_stack)) if self.books_stack else "Stack is empty"

    def animate_push(self, book):
        for _ in range(3):
            print(colored(f"Pushing {book}...", "yellow"))
            time.sleep(0.3)
            self.clear_screen()

    def animate_pop(self, book):
        for _ in range(3):
            print(colored(f"Popping {book}...", "yellow"))
            time.sleep(0.3)
            self.clear_screen()

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

def stack_operations():
    stack = Stack()
    cprint("Welcome to the interactive stack operations program!", "cyan")
    cprint("You can perform the following operation")

    while True:
        print("\nCurrent Book: ", colored(str(stack), "blue"))
        print(colored("1 - Push a book", "yellow"))
        print(colored("2 - Pop a book", "yellow"))
        print(colored("3 - Peek at the top book", "yellow"))
        print(colored("4 - Check if the stack is empty", "yellow"))
        print(colored("5 - Get the size of the stack", "yellow"))
        print(colored("6 - Quit", "yellow"))

        try:
            choice = int(input(colored("Choose an operation (1-6): ", "green")))
        except ValueError:
            cprint("Invalid input. Please enter a nuber between 1 and 6.", "red")
            continue

        if choice == 1:
            book = input(colored("Enter a book to push: ", "green"))
            stack.push(book)
        elif choice == 2:
            try:
                stack.pop()
            except IndexError as e:
                cprint(e, "red")
        elif choice == 3:
            try:
                cprint("Top books: " + stack.peek(), "blue")
            except IndexError as e:
                cprint(e, "red")
        elif choice == 4:
            cprint("Is the stack empty? " + ("Yes" if stack.is_empty() else "No"), "blue")
        elif choice == 5:
            cprint("Is the stack empty? " + str(stack.size()), "blue")
        elif choice == 6:
            cprint("Exiting the program. GoodBye!", "cyan", attrs=["bold"])
            break
        else:
            cprint("Invalid choice. Please select a number between 1 to 6.", "red")

if __name__ == "__main__":
    stack_operations()




