import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import pandas as pd
from pandasql import sqldf
from pandastable import Table

def read_csv() :
    db = pd.read_csv("organism_database_20240428124116.csv", header=None,
                     names=["Type", "ID", "Birth_Time_ms", "Deathtime_Time_ms", "Time_lived", "Max_Health", "Updates", "Health_Ratio", "Energy", "Max_Energy", "Energy_Ratio", "Tiles_Travel",
                            "Attack_Power", "Organism_Attacked", "Animals_Kill", "Plants_Killed", "Number_Offspring", "R", "G", "B"])
    assert db is not None
    return db


def querry_input() -> None:
    """"Takes sql statement from user and returns the querried pandadf"""
    user_querry = entry.get()
    output = pysqldf(user_querry)
    update_table(output)


def new_query() -> None:
    """"Allows user to make a new querry"""
    entry.delete(0, tk.END)  #Clear entry widget
    update_table(db)


def update_table(dataframe) -> None:
    """"Update the table with new data"""
    table.model.df = dataframe
    table.redraw()


def pysqldf(query):
    """Wrapper function for sqldf"""
    return sqldf(query, globals())
