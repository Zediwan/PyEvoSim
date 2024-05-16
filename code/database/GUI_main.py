import tkinter as tk
import pandas as pd
from pandasql import sqldf
from pandastable import Table
from tkinter import ttk
from ttkthemes import ThemedTk



#Read the csv into a panda df
db = pd.read_csv("code/database/organism_database_20240428124116.csv")

#Takes sql statement from user and returns the querried pandadf
def querry_input():
    #Retrieve the input from the entry widget
    user_querry = entry.get()

    #Pass input to a pandasql and get the result
    output = pysqldf(user_querry)

    #update the table
    update_table(output)

#Allows user to make a new querry
def new_query():
    #Clear the entry widget
    entry.delete(0, tk.END)

    # Reset the result label
    update_table(db)

#Update the table with new data
def update_table(dataframe):
    table.model.df = dataframe
    table.redraw()

#Define global function for querrying
pysqldf = lambda q: sqldf(q, globals())


#Create the main window
#root = tk.Tk()
root = ThemedTk(theme = "arc")
root.title("Evolution Simulation")

#Define frame globally
frame = ttk.Frame(root)
frame.pack(fill='both', expand=True)

#entry widget for user input
entry = ttk.Entry(root, width=40)
entry.pack(pady=10)

#submit button
submit_button = ttk.Button(root, text="Submit", command=querry_input)
submit_button.pack(pady=5)

#"restart" button
new_query_button = ttk.Button(root, text="restart", command=new_query)
new_query_button.pack(pady=5)

#initial table display
table = Table(frame, dataframe=db)
table.setTheme("dark")
table.show()

root.mainloop()


