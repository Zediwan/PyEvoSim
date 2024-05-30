import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pygame.display
import pygame_menu
import warnings
import pygame
import os

class Data_Analyser():
    def __init__(self, width: int, height: int, pos: tuple[int, int] = (0, 0), csv_path: str = None, dataframe: pd.DataFrame = None) -> None:
        # if width < 0:
        #     raise ValueError(f"Width must be bigger than 0. {width}")
        # if height < 0:
        #     raise ValueError(f"Height must be bigger than 0. {height}")
        # self.rect = pygame.Rect(pos[0], pos[1], width, height)
        # self.surface = pygame.Surface(self.rect.size)

        if dataframe is None:
            if csv_path is None:
                csv_path = Data_Analyser.get_newest_csv()
            elif not os.path.isfile(csv_path):
                raise ValueError(f"Path {csv_path} does not exist!")
            dataframe = pd.read_csv(csv_path)
        else:
            if csv_path is not None:
                warnings.warn("CSV path and dataframe has been given. Note that the df is used and csv ignored", Warning, stacklevel=1)
        self.df = dataframe
        self.df.drop(axis="rows", index=0, inplace=True)
        self.df = self.df.drop(["Type", "ID"], axis=1)
        
        #print(self.df.describe())
        self.df["Generation"] = 1000 * (self.df["Birth time (milsec)"] // 1000)
        grouped = self.df.groupby(["Generation"]).mean()
        print(grouped)

        x_vals = grouped.index.tolist()
        print(x_vals)
        y_vals = grouped["Number of Offsprings"]
        
        plt.plot(x_vals, y_vals)
        plt.show()
        
        #region starting menu
        # self.starting_menu = pygame_menu.Menu("Data Analyser", width=self.rect.w, height=self.rect.h)
        # self.starting_menu.add.button("Table", self.show_table)
        # self.starting_menu.add.button("Graphs", self.show_graphs)
        # self.starting_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)
        #endregion

    def show_table(self):
        pass

    def show_graphs(self):
        pass

    def mainloop(self):
        pass

    @classmethod
    def get_newest_csv(cls):
        csvs = glob.glob("data/organism_database_*.csv")
        newest_csv = max(csvs)
        if newest_csv is None:
            raise ValueError("Cannot find newest csv!")
        return newest_csv
