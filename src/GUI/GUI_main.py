import tkinter as tk
import pandas as pd
from pandasql import sqldf
from pandastable import Table

#Define global function for querrying
pysqldf = lambda q: sqldf(q, globals())
file_path_Andrin = 'C:\\Users\\andri\\OneDrive - Universitaet Bern\\6. Semester\\Programming for Data Science\\EvolutionSimulation-1\\src\\GUI\\organism_database_20240428124116.csv'
file_path_Milos = 'C:\\Users\Milos-Uni\EvolutionSimulation\databases\organism_database_20240428124116.csv'
# Read the csv into a panda df
db = pd.read_csv(file_path_Andrin)

# Create the main window
root = tk.Tk()
root.title("Evolution Simulation")

# Define frame globally
frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

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
    global frame
    frame.destroy()

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)
    pt = Table(frame, dataframe=dataframe)
    pt.show()

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
table = Table(frame, dataframe=db)
table.show()

root.mainloop()


