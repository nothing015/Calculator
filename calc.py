# Python package for GUI applications: tkinter
import tkinter as tk

LARGE_FONT_STYLE = ("Arial", 40)
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)
OFF_WHITE = "#F8FAFF"
WHITE = '#FFFFFF'
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"  # Colour of the display frame
LABEL_COLOR = "#25265E"  # Colour of the main label


class Calculator:
    def __init__(self):
        self.window = tk.Tk()  # The window
        self.window.geometry("375x600")  # The size of the window
        self.window.resizable(0, 0)  # The resizing functionality of the window
        self.window.title("Nuaiman's Calculator :)")  # The title

        self.total_expression = ""  # The total result display
        self.current_expression = ""  # The current expression display

        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()  # The two main labels
        # All the digits
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            '.': (4, 1), 0: (4, 2)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        # This helps our rows and columns of buttons to expand
        for x in range(1,5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()

        self.create_special_buttons()

        self.bind_keys()     # To make the keyboard work


    def run(self):
        # To start the calculator
        self.window.mainloop()

    def create_display_frame(self):
        # Creating the frame widget inside our main window and allowing to expand the frame
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame
    def create_buttons_frame(self):
        # Same as the display frame widget, but buttons widget instead
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def clear(self):
        # Simply clear both the current and total expression
        self.current_expression = ""
        self.total_expression = ""
        self.update_total_label()
        self.update_label()

    def evaluate(self):
        # Computing the current expression by exploiting the function eval
        self.total_expression += self.current_expression
        self.update_total_label()
        try:         # To avoid 0/0 showing 0, instead handles it as an error
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

        self.update_label()

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()
    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()
    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0,
        command=self.clear
        )
        button.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,borderwidth=0,
        command=self.evaluate
        )
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)
    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0,
        command=self.sqrt
        )
        button.grid(row=0, column=3, sticky=tk.NSEW)
    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0,
        command=self.square
        )
        button.grid(row=0, column=2, sticky=tk.NSEW)
    def create_special_buttons(self):
        # Method to create the special buttons above
        self.create_equals_button()
        self.create_clear_button()
        self.create_sqrt_button()
        self.create_square_button()

    def create_display_labels(self):
        # Widget total_label displays the total expression, achored to the right with the corresponding colors
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E,
                               bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E,
                         bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_operator_buttons(self):
        # Creating the operator buttons widget and placing them in the last column and 1 above from where the digits start
        i = 0
        for operator,symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0,
            command=lambda x=operator: self.append_operator(x)
            )
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1
    def append_operator(self, operator):
        # For the command of the method above
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def update_total_label(self):
        expression = self.total_expression
        for operator,symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')    # To replace the operator symbol
        self.total_label.config(text=expression)
    def update_label(self):
        self.label.config(text=self.current_expression[:11])    # [:11] to stop the math from overflowing
    def create_digit_buttons(self):
        # Creating the number buttons widget and placing them in a grid(sticks to every side)
        for digit,grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE, borderwidth=0,
            command=lambda x=digit: self.add_to_expression(x)
            )
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
    def add_to_expression(self, value):
        # For the command: of the method above
        self.current_expression += str(value)
        self.update_label()


    def bind_keys(self):
        # To make the keyboard work with the calculator app
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))


# This is the main program, run when the .py file is clicked
if __name__ == "__main__":
    calc = Calculator()
    calc.run()
