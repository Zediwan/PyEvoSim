save_csv: bool = False
save_animals_csv: bool = False
save_plants_csv: bool = False

def update_save_csv(value: bool):
    global save_csv
    save_csv = value

def update_save_animals_csv(value: bool):
    global save_animals_csv
    save_animals_csv = value

def update_save_plants_csv(value: bool):
    global save_plants_csv
    save_plants_csv = value