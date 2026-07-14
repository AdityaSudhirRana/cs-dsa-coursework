import math

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def traverse(self):
        if self.is_empty():
            print("\n[!] Stack is empty.")
            return
        print("\n--- Current Stack (Top to Bottom) ---")
        for item in reversed(self.stack):
            print(f"| {item} |")
        print("-------")


def check_delimiter_matching(expression: str) -> bool:
    stack = Stack()
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in expression:
        if char in mapping.values():
            stack.push(char)
        elif char in mapping.keys():
            if stack.is_empty() or stack.pop() != mapping[char]:
                return False
    return stack.is_empty()


def is_operator(char: str) -> bool:
    return char in {'+', '-', '*', '/', '^'}

def prefix_to_postfix(prefix_expr: str) -> str:
    stack = Stack()
    tokens = prefix_expr.split() if " " in prefix_expr else list(prefix_expr)
    
    for token in reversed(tokens):
        if is_operator(token):
            operand1 = stack.pop()
            operand2 = stack.pop()
            if operand1 is None or operand2 is None:
                return "Error: Invalid Prefix Expression"
            new_expr = f"{operand1} {operand2} {token}"
            stack.push(new_expr)
        else:
            stack.push(token)
            
    return stack.pop()

def evaluate_postfix(postfix_expr: str) -> float:
    stack = Stack()
    tokens = postfix_expr.split()
    
    try:
        for token in tokens:
            if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                stack.push(float(token))
            elif is_operator(token):
                operand2 = stack.pop()
                operand1 = stack.pop()
                
                if operand1 is None or operand2 is None:
                    raise ValueError("Malformed expression")
                
                if token == '+': stack.push(operand1 + operand2)
                elif token == '-': stack.push(operand1 - operand2)
                elif token == '*': stack.push(operand1 * operand2)
                elif token == '/': 
                    if operand2 == 0: raise ZeroDivisionError("Division by zero")
                    stack.push(operand1 / operand2)
                elif token == '^': stack.push(operand1 ** operand2)
        
        return stack.pop()
    except Exception as e:
        print(f"[!] Evaluation Error: {e}")
        return None


def menu():
    demo_stack = Stack()
    
    while True:
        print("\n" + "="*40)
        print("       ALL-IN-ONE STACK PROGRAM")
        print("="*40)
        print("1. Push (Insert Element)")
        print("2. Pop (Delete Element)")
        print("3. Peek (View Top Element)")
        print("4. Traverse (View Full Stack)")
        print("5. Check Delimiter Matching")
        print("6. Convert Prefix to Postfix & Evaluate")
        print("7. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            val = input("Enter element to push into the demo stack: ")
            demo_stack.push(val)
            print(f"[+] '{val}' successfully pushed.")
            
        elif choice == '2':
            val = demo_stack.pop()
            if val is not None:
                print(f"[-] Popped element: {val}")
            else:
                print("[!] Stack Underflow! Nothing to pop.")
                
        elif choice == '3':
            val = demo_stack.peek()
            if val is not None:
                print(f"[*] Element at top: {val}")
            else:
                print("[!] Stack is empty.")
                
        elif choice == '4':
            demo_stack.traverse()
            
        elif choice == '5':
            expr = input("Enter expression to check (e.g., {[()]}): ")
            if check_delimiter_matching(expr):
                print("Success! Delimiters are perfectly balanced.")
            else:
                print("Error! Delimiters are unbalanced or incorrectly nested.")
                
        elif choice == '6':
            print("\nNote: Please use spaces between characters for multi-digit evaluation.")
            prefix = input("Enter Prefix Expression (e.g., - + 2 3 4): ").strip()
            
            postfix = prefix_to_postfix(prefix)
            print(f"\n[→] Converted Postfix: {postfix}")
            
            if "Error" not in postfix:
                result = evaluate_postfix(postfix)
                if result is not None:
                    print(f"[✓] Final Evaluation Result: {result}")
                    
        elif choice == '7':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("[!] Invalid option. Please select between 1 and 7.")

if __name__ == "__main__":
    menu()
