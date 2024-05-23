""""This is the gui for filtering and querrying data from the organism_database"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from ttkthemes import ThemedTk
import pandas as pd
from pandasql import sqldf
from pandastable import Table
import functions as func

def querry_input() -> None:
    """"Takes sql statement from user and returns the querried pandadf"""
    user_querry = entry.get()
    output = sqldf(user_querry)
    update_table(output)


def new_query() -> None:
    """"Allows user to make a new querry"""
    entry.delete(0, tk.END)  #Clear entry widget
    update_table(db)


def update_table(dataframe) -> None:
    """"Update the table with new data"""
    table.model.df = dataframe
    table.redraw()

def main(db=func.read_csv()) -> None:
    """"Main function for the GUI"""
    #Create the main window
    #root = tk.Tk()
    root = ThemedTk(theme="arc")
    root.title("Evolution Simulation")

    #Define frame globally
    frame = ttk.Frame(root)
    frame.pack(fill='both', expand=True)

    #entry widget for user input
    global entry
    entry = ttk.Entry(root, width=40)
    entry.pack(pady=10)

    #submit button
    submit_button = ttk.Button(root, text="Submit", command=querry_input)
    submit_button.pack(pady=5)

    #"restart" button
    new_query_button = ttk.Button(root, text="restart", command=new_query)
    new_query_button.pack(pady=5)

    #initial table display
    global table
    table = Table(frame, dataframe=db)
    table.setTheme("dark")
    table.show()

    root.mainloop()


if __name__ == "__main__":
    db = func.read_csv()
    main()
