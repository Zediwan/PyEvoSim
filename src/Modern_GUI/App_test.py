from tkinter import *
import customtkinter as ctk
import pandas as pd
import glob
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_csv():
    csv_files = glob.glob("code/database/*.csv")
    if not csv_files:
        raise FileNotFoundError("No CSV files found in the specified directory.")
    csv = csv_files[0]
    db = pd.read_csv(csv, header=None,
                     names=["Type", "ID", "Birth_Time_ms", "Death_Time_ms", "Time_lived", "Max_Health", "Updates", "Health_Ratio", "Energy", "Max_Energy", "Energy_Ratio", "Tiles_Travel",
                            "Attack_Power", "Organism_Attacked", "Animals_Killed", "Plants_Killed", "Number_Offspring", "R", "G", "B"])
    db.drop(axis='rows', index=0, inplace=True)
    return db

def main_menu(root_view, dataframe):
    for widget in root_view.winfo_children():
        widget.destroy()

    title_label = ctk.CTkLabel(master=root_view, text="Evolution Simulator", font=("Arial", 36))
    title_label.pack(pady=20)

    button_frame = ctk.CTkFrame(master=root_view)
    button_frame.pack(expand=True)

    table_button = ctk.CTkButton(master=button_frame, text="Table", command=lambda: table_view(root_view, dataframe), width=250, height=100, font=('Arial', 20))
    table_button.pack(side='top', padx=10, pady=(10, 10))

    dashboard_button = ctk.CTkButton(master=button_frame, text="Dashboard", command=lambda: dashboard(root_view, dataframe), width=250, height=100, font=('Arial', 20))
    dashboard_button.pack(side='top', padx=10, pady=(10, 10))

    exit_button = ctk.CTkButton(master=button_frame, text="Exit", command=root_view.quit, fg_color="red", width=250, height=100, font=('Arial', 20))
    exit_button.pack(side='top', padx=10, pady=(10, 10))

def dashboard(root_view, dataframe):
    # Clear the window
    for widget in root_view.winfo_children():
        widget.destroy()

    # Create a new frame for the dashboard
    dashboard_frame = ctk.CTkFrame(master=root_view)
    dashboard_frame.pack(fill=BOTH, expand=True)

    # Create and display the histogram
    try:
        fig1 = Figure(figsize=(5, 5), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.hist(dataframe['Time_lived'].dropna(), bins=20)  # Drop NaNs to avoid issues
        ax1.set_title('Histogram of Time_lived')

        canvas1 = FigureCanvasTkAgg(fig1, master=dashboard_frame)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    except KeyError as e:
        print(f"Column {e} not found in dataframe")

    # Create and display the scatter plot
    try:
        fig2 = Figure(figsize=(5, 5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.scatter(dataframe['Energy'].dropna(), dataframe['Max_Energy'].dropna())  # Drop NaNs to avoid issues
        ax2.set_title('Scatter plot of Energy vs Max_Energy')

        canvas2 = FigureCanvasTkAgg(fig2, master=dashboard_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    except KeyError as e:
        print(f"Column {e} not found in dataframe")

    # Create and display the pie chart
    try:
        fig3 = Figure(figsize=(5, 5), dpi=100)
        ax3 = fig3.add_subplot(111)
        type_counts = dataframe['Type'].value_counts()
        ax3.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%')
        ax3.set_title('Pie chart of Type')

        canvas3 = FigureCanvasTkAgg(fig3, master=dashboard_frame)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    except KeyError as e:
        print(f"Column {e} not found in dataframe")

    # Add a back button
    back_button = ctk.CTkButton(master=dashboard_frame, text="Back", command=lambda: main_menu(root_view, dataframe), font=("Arial", 14))
    back_button.grid(row=2, column=0, columnspan=2, pady=(10, 10))

    # Configure grid weights to make the widgets resize proportionally
    dashboard_frame.grid_rowconfigure(0, weight=1)
    dashboard_frame.grid_rowconfigure(1, weight=1)
    dashboard_frame.grid_rowconfigure(2, weight=1)
    dashboard_frame.grid_columnconfigure(0, weight=1)
    dashboard_frame.grid_columnconfigure(1, weight=1)

def table_view(root_view, dataframe):
    global table

    for widget in root_view.winfo_children():
        widget.destroy()

    table_frame = ctk.CTkFrame(master=root_view, width=1000, height=700)
    table_frame.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))

    top_button_frame = ctk.CTkFrame(master=root_view, width=200, height=100)
    top_button_frame.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))

    dashboard_button = ctk.CTkButton(master=top_button_frame, text="Dashboard", command=lambda: dashboard(root_view, dataframe), font=("Arial", 12))
    dashboard_button.pack(side='top', padx=(5, 5), pady=(10, 10))

    table_button = ctk.CTkButton(master=top_button_frame, text="Table", command=lambda: table_view(root_view, dataframe), font=("Arial", 12))
    table_button.pack(side='top', padx=(5, 5), pady=(5, 5))

    exit_button = ctk.CTkButton(master=top_button_frame, text="Exit", command=root_view.quit, fg_color="red", font=('Arial', 12))
    exit_button.pack(side='top', padx=10, pady=(5, 5))

    bottom_frame = ctk.CTkFrame(master=root_view, width=1200, height=100)
    bottom_frame.grid(row=1, column=1, padx=(5, 5), pady=(10, 10))
    bottom_frame.grid_propagate(False)

    entry_label = ctk.CTkLabel(master=bottom_frame, text="SQL Queries:")
    entry_label.pack()

    table = Table(parent=table_frame, dataframe=dataframe, width='900', height='700', showtoolbar=False, showstatusbar=False)
    table.Theme = "dark"

    entry = ctk.CTkEntry(master=bottom_frame, width=750, placeholder_text="Enter SQL queries here")
    entry.pack(pady=10)

    buttons_frame = ctk.CTkFrame(master=bottom_frame)
    buttons_frame.pack(anchor='center')

    submit_button = ctk.CTkButton(master=buttons_frame, text="Submit", command=lambda: query_input(entry, dataframe), font=("Arial", 14))
    submit_button.pack(side='left', padx=(5, 5), pady=(5, 5))

    restart_button = ctk.CTkButton(master=buttons_frame, text="Restart", command=lambda: new_query(entry, dataframe), font=("Arial", 14))
    restart_button.pack(side='left', padx=(5, 5), pady=(5, 5))

    table.show()

db = read_csv()

root = ctk.CTk()
root.geometry('1000x900')
root.title("Evolution Simulation")

ctk.set_appearance_mode("dark")

main_menu(root, db)

root.mainloop()
