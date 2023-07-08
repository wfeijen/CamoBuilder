import tkinter as tk
from math import sqrt
def calculate_text_color(color):
    r, g, b = color
    brightness = sqrt(0.299 * r**2 + 0.587 * g**2 + 0.114 * b**2)
    text_color = "#000000" if brightness > 128 else "#FFFFFF"
    return text_color

root = tk.Tk()
root.title("RGB Color Grid")
n = 9
factor = 255 / (n-1)
count = range(n)

for c in count:
    print(int(c * factor))

for r in count:
    for g in count:
        for b in count:
            color = (int(r*factor), int(g*factor),int(b*factor))
            hex_code = "#%02x%02x%02x" % color
            decimal_code = f"{color[0]}, {color[1]}, {color[2]}"
            label = tk.Label(root, bg=hex_code, width=10, height=3, text=decimal_code, fg=calculate_text_color(color))
            label.grid(row=r + b%3 * n, column=g + b//3 * n)

root.mainloop()



