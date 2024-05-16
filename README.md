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

To run the simulation you need to run the [main.py](code/simulation/main.py) file.

#### World generation

Then you get the [starting menu](assets/images/Screenshot Starting Menu.png). From here you can press `GENERATE WORLD` to get to the [world generator](assets/images/Screenshot_Generate_World_empty.png).

Now by pressing `GENERATE WORLD` you can repeatedly [generate new worlds](assets/images/Screenshot_Generate_World_filled.png) until you find one you like.

With the mouse you can hover over the world and when [pressing the mouse button you can lower the height level of the tiles](assets/images/Screenshot_Generate_World_world_editing.png), eventually creating rivers and lakes.

Additionally by pressing `p` you can spawn plants and by pressing `a` you can spawn animals, see [here](assets/images/Screenshot_Generate_World_plants_and_animals.png) (note if the world has not been populated by the user when the simulation is started, animals and plants are spawned automatically)

#### Simulating

When pressing `START` the simulation begins to run.

Now when clicking on an animal or a tile with a plant the [stats of said organism are displayed](assets/images/Screenshot_Simulation_stat_example.png).

When pressing `SPACE` the user can pause the simulation and run it again by pressing `SPACE` again.

With the `ESCAPE` button the user can acces the [simulation settings](assets/images/Screenshot_Simulation_settings.png). (This is work in progress and has no use case for now, except from returning to the main menu)


### Database interaction

Provide instructions and examples for use. Include screenshots as needed.

To add a screenshot, create an `assets/images` folder in your repository and upload your screenshot to it. Then, using the relative filepath, add it to your README using the following syntax:

    ```md
    ![alt text](assets/images/screenshot.png)
    ```

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
