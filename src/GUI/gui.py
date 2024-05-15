import tkinter as tk
from tkinter import ttk
import pandas as pd

# loads the database as a table in the GUI
def load_data():
    # Read the csv file
    df = pd.read_csv('databases/organism_database_20240428124116.csv')

    # Create a canvas and put a scrollbar on it
    canvas = tk.Canvas(frame)
    v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    # Bind the scrollable frame to the scroll function
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    # Configure the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Create the treeview widget
    tree = ttk.Treeview(scrollable_frame)

    # Create an invisible column as the first column
    tree['columns'] = [''] + list(df.columns)
    tree.column('', width=0, stretch='no')

    # Create the other columns
    for column in df.columns:
        tree.column(column, width=100)
        tree.heading(column, text=column)

    # Insert the data
    for index, row in df.iterrows():
        tree.insert('', 'end', values=[''] + list(row))

    # Display the treeview widget
    tree.grid(row=0, column=0, sticky='nsew')

    # Display the canvas and scrollbar
    canvas.grid(row=0, column=0, sticky='nsew')
    v_scrollbar.grid(row=0, column=1, sticky='ns')
    h_scrollbar.grid(row=1, column=0, sticky='ew')

root = tk.Tk()
root.title("Evolution Simulation")

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Make the frame expandable
frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)

# Load and display the data
load_data()

root.mainloop()
