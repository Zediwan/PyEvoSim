# Evolution Simulation Project

Welcome to the Evolution Simulation project!

Our goal is to simulate the evolution of virtual organisms using neural networks within a dynamic environment. Our main vision is to maintain procedural simulation, avoiding the implementation of predefined animal types. This approach allows evolutionary selection to unfold freely, potentially surprising us with its results.

The goal is to continually make the simulation more complex by adding new features from real life to enable vast amount of different adaptations to the simulations settings.

Below, you'll find information on how to set up and run the simulation, as well as an overview of its features.

## Features

- Animals consuming food and utilizing energy to survive.
- Reproduction based on accumulated energy.
- DNA system defining various aspects of an animal (work in progress).
- Organism Database to filter and query (work in progress)
- Visualization of gene distribution in the simulation (work in progress).
- User-friendly GUI for simulation settings adjustment (work in progress).

## Usage

### Simulation

To run the simulation you need to run the [main.py](code/simulation/main.py) file. When an organism dies in the simulation it is logged to a database with all the relevant information.

Note: the database can be inspected without running the simulation as it uses a database from an older run.

#### World generation

Then you get the [starting menu](assets/images/Screenshot_Starting_Menu.png). From here you can press `GENERATE WORLD` to get to the [world generator](assets/images/Screenshot_Generate_World_empty.png).

Now by pressing `GENERATE WORLD` you can repeatedly [generate new worlds](assets/images/Screenshot_Generate_World_filled.png) until you find one you like.

With the mouse you can hover over the world and when [pressing the mouse button you can lower the height level of the tiles](assets/images/Screenshot_Generate_World_world_editing.png), eventually creating rivers and lakes.

Additionally by pressing `p` you can spawn plants and by pressing `a` you can spawn animals, see [here](assets/images/Screenshot_Generate_World_plants_and_animals.png) (note if the world has not been populated by the user when the simulation is started, animals and plants are spawned automatically)

#### Simulating

When pressing `START` the simulation begins to run.

Now when clicking on an animal or a tile with a plant the [stats of said organism are displayed](assets/images/Screenshot_Simulation_stat_example.png).

When pressing `SPACE` the user can pause the simulation and run it again by pressing `SPACE` again.

With the `ESCAPE` button the user can acces the [simulation settings](assets/images/Screenshot_Simulation_settings.png). (This is work in progress and has no use case for now, except from returning to the main menu)

By pressing with the mouse on a tile without and organism a new animal can be spawned.

### Database
To access, filter and query the database, you need to run the [GUI_main.py](code/database/GUI_main.py) file.

To sort data in ascending/descending order in a column, right-click on the column and choose `Sort by "column name"` followed by an arrow.

You can also apply a function (e.g. calculate the mean of a column with numerical data) by right-clicking on a column and choosing `Apply function`.
A little window pops up and you can choose between various functions, choose if the column will be updated by the values or a column will be created with a given name.

To filter data to your liking, click on a row, right-click and choose `Filter Rows`.

![panels_filter](https://github.com/Zediwan/EvolutionSimulation/assets/42497189/9473d428-6164-4782-b09c-cdbdc4cb21cb)

Either you can use String Queries or by clicking on the green plus symbol, you can define a custom filter where you can specify the column, the condition and the comparison value:

![example_filter](https://github.com/Zediwan/EvolutionSimulation/assets/42497189/482f922f-0e04-46e5-b325-97b1eaec54d9)

It is also possible to add more filters by clickinig on the green plus symbol.

To apply filters, check the box `show filtered only` and click on the key symbol.

To delete filters, click on the red cross symbol.

## Contributing

If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/new-feature`).
6. Create a new pull request.

## Credits

This project was initiated by Jeremy Moser.

Later on it was worked on as a project for a lecture Programmig for Data Science by Jeremy Moser, Andrin Müller, Dimoth Pathiniwasam and Milos Kecman.

Inspirations for the project were other projects like [the Bibites](https://www.youtube.com/@TheBibitesDigitalLife), [Coding Train](https://github.com/CodingTrain), [Sebastian Lague](https://github.com/SebLague) and many more.

## License

This project is licensed under the MPL-2.0 License. See the [LICENSE](LICENSE) file for details.
