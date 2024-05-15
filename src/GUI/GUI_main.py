import tkinter as tk
import pandas as pd
from pandasql import sqldf
from pandastable import Table

#Define global function for querrying
pysqldf = lambda q: sqldf(q, globals())

# Read the csv into a panda df
db = pd.read_csv("organism_database_20240428124116.csv")

def querry_input():
    # Retrieve the input from the entry widget
    user_querry = entry.get()
    
    # Pass input to a pandasql and get the result
    output = pysqldf(user_querry)

    #update the table
    update_table(output)
    
    # Print the result to the console
    #print(output)
    
def new_query():
    # Clear the entry widget
    entry.delete(0, tk.END)
    
    # Reset the result label
    update_table(db)

# Update the table with new data
def update_table(dataframe):
    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)
    pt = Table(frame, dataframe=dataframe)
    pt.show()

# Create the main window
root = tk.Tk()
root.title("Evolution Simulation")

# entry widget for user input
entry = tk.Entry(root, width=40)
entry.pack(pady=10)

# submit button
submit_button = tk.Button(root, text="Submit", command=querry_input)
submit_button.pack(pady=5)

# "New Query" button
new_query_button = tk.Button(root, text="New Query", command=new_query)
new_query_button.pack(pady=5)

# Initial table display
initial_frame = tk.Frame(root)
initial_frame.pack(fill='both', expand=True)
table = Table(initial_frame, dataframe=db)
table.show()

root.mainloop()


