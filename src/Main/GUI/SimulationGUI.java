package Main.GUI;

import Main.Organisms.Animal;
import Main.Organisms.Plant;
import Main.World.Simulation;
import Main.World.World;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class SimulationGUI extends JFrame {
    private JPanel simPanel;
    public static JScrollPane scrollPane;
    private JPanel graphPanel;
    private JSplitPane controlPane;

    private JTabbedPane settingsPane;
    private JPanel animalSettingsPanel;
    private JPanel plantSettingPanel;
    private JPanel organismSettingPanel;
    private JPanel worldSettingPanel;

    private JTabbedPane statPanel;
    private final JScrollPane animalStatPanel;
    private final JScrollPane plantStatPanel;
    private final JScrollPane organismStatPanel;
    private final JPanel worldStatPanel;

    private JCheckBox showHealthCheckBox;
    private JCheckBox showEnergyCheckBox;
    private JCheckBox showAnimalQTCheckBox;
    private JCheckBox showPlantQTCheckBox;

    private JPanel maxPlantsPanel;
    private JSlider maxPlantsSlider;
    private JLabel maxPlantsLabel;
    private JPanel minPlantsPanel;
    private JSlider minPlantsSlider;
    private JLabel minPlantsLabel;

    private JPanel maxAnimalsPanel;
    private JSlider maxAnimalsSlider;
    private JLabel maxAnimalsLabel;
    private JPanel minAnimalsPanel;
    private JSlider minAnimalsSlider;
    private JLabel minAnimalsLabel;

    private JPanel simulationSpeedPanel;
    private JSlider simulationSpeedSlider;
    private JLabel simulationSpeedLabel;

    private JLabel fpsLabel;

    private Object[][] animalData;
    private Object[][] plantData;

    public static boolean showHealth = false;
    public static boolean showEnergy = false;
    public static boolean showAnimalQT = false;
    public static boolean showPlantQT = false;
    public static boolean showSteering = true;
    public static boolean showDirection = true;
    public static boolean showSensoryRadius = true;
    public static int viewportWidth;
    public static int viewportHeight;
    public static double scrollOffsetX;
    public static double scrollOffsetY;

    public SimulationGUI() {
        // Set up main frame
        setTitle("Simulation");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Set up simulation panel
        World w =new World(2000,2000, 50, 50);
        Simulation s = new Simulation(2000,1000,2000,
                1,3000,1000,
                1,1,
                w);
        this.simPanel = s;
        this.simPanel.setPreferredSize(w.getWorldDimension()); // Set initial size
        this.simPanel.setFocusable(true);
        this.scrollPane = new JScrollPane(this.simPanel);
        this.scrollPane.setPreferredSize(new Dimension(800, 600)); // Set initial viewport size
        this.scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
        this.scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);

        //This is used to be able to pause when pressing enter and having focused the scroll panel
        this.scrollPane.addKeyListener(new KeyAdapter() {
            public void keyPressed(KeyEvent e) {
                System.out.println("");
                if (e.getKeyCode() == KeyEvent.VK_SPACE) {
                    if(s.simulationIsRunning()){
                        s.stopSimulation();
                    }
                    else{
                        s.startSimulation();
                    }
                }
            }
        });

        /*
        scrollPane.addComponentListener(new ComponentAdapter() {
            public void componentResized(ComponentEvent e) {
                // update the viewport size when the scroll pane is resized
                viewportWidth = scrollPane.getViewport().getWidth();
                viewportHeight = scrollPane.getViewport().getHeight();
            }
        });

        scrollPane.getViewport().addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                // update the scroll offset when the viewport position changes
                scrollOffsetX = scrollPane.getViewport().getViewPosition().getX();
                scrollOffsetY = scrollPane.getViewport().getViewPosition().getY();
            }
        });
         */
        this.scrollPane.setFocusable(true); // Set focusable to false

        this.add(scrollPane, BorderLayout.CENTER);

        // Set up bottom panel
        this.graphPanel = new JPanel();
        this.graphPanel.setLayout(new BoxLayout(graphPanel, BoxLayout.Y_AXIS));
        this.graphPanel.add(new JLabel("Simulation Statistics"));
        this.add(this.graphPanel, BorderLayout.SOUTH);

        // Set up right panel
        this.controlPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT);

        this.settingsPane = new JTabbedPane();
        this.animalSettingsPanel = new JPanel(new GridLayout(0, 2));
        this.plantSettingPanel = new JPanel(new GridLayout(0, 2));
        this.organismSettingPanel = new JPanel(new GridLayout(0, 2));
        this.worldSettingPanel = new JPanel(new GridLayout(0, 2));
        this.settingsPane.addTab("Animals", this.animalSettingsPanel);
        this.settingsPane.addTab("Plants", this.plantSettingPanel);
        this.settingsPane.addTab("Organisms", this.organismSettingPanel);
        this.settingsPane.addTab("World", this.worldSettingPanel);

        this.statPanel =  new JTabbedPane();
        this.organismStatPanel = new JScrollPane();
        this.worldStatPanel = new JPanel();
        this.statPanel.addTab("Organisms", this.organismStatPanel);
        this.statPanel.addTab("World", this.worldStatPanel);

        //Show health checkbox
        this.showHealthCheckBox = new JCheckBox("Show Health");
        this.showHealthCheckBox.setToolTipText("Toggle the visualization of the current Health");
        this.showHealthCheckBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showHealth = showHealthCheckBox.isSelected();
            }
        });
        showHealthCheckBox.setSelected(this.showHealth);

        //Show energy checkbox
        this.showEnergyCheckBox = new JCheckBox("Show Energy");
        this.showEnergyCheckBox.setToolTipText("Toggle the visualization of the current Energy");
        this.showEnergyCheckBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showEnergy = showEnergyCheckBox.isSelected();
            }
        });
        showEnergyCheckBox.setSelected(this.showEnergy);

        //Show direction checkbox
        JCheckBox showDirectionCheckBox = new JCheckBox("Show Direction");
        //TODO add descr
        showDirectionCheckBox.setToolTipText("");
        showDirectionCheckBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showDirection = showDirectionCheckBox.isSelected();
            }
        });
        showDirectionCheckBox.setSelected(this.showDirection);

        //Show direction checkbox
        JCheckBox showAccelerationCheckBox = new JCheckBox("Show Acceleration");
        //TODO add descr
        showAccelerationCheckBox.setToolTipText("");
        showAccelerationCheckBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showSteering = showAccelerationCheckBox.isSelected();
            }
        });
        showAccelerationCheckBox.setSelected(this.showSteering);

        //Show sensoryRad
        JCheckBox showSensoryRadiusCheckBox = new JCheckBox("Show Sensory Radius");
        //TODO add descr
        showSensoryRadiusCheckBox.setToolTipText("");
        showSensoryRadiusCheckBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showSensoryRadius = showSensoryRadiusCheckBox.isSelected();
            }
        });
        showSensoryRadiusCheckBox.setSelected(this.showSensoryRadius);

        //Show Animal QT checkbox
        this.showAnimalQTCheckBox = new JCheckBox("Show Animal Quad Tree");
        this.showAnimalQTCheckBox.setToolTipText("Toggle the visualization of the Animal Quad Tree");
        this.showAnimalQTCheckBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showAnimalQT = showAnimalQTCheckBox.isSelected();
            }
        });
        this.showAnimalQTCheckBox.setSelected(this.showAnimalQT);

        //Show Plant QT checkbox
        this.showPlantQTCheckBox = new JCheckBox("Show Plant Quad Tree");
        this.showPlantQTCheckBox.setToolTipText("Toggle the visualization of the Plant Quad Tree");
        this.showPlantQTCheckBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showPlantQT = showPlantQTCheckBox.isSelected();            }
        });
        showPlantQTCheckBox.setSelected(this.showPlantQT);

        JTextField animalQTCapacity = new JTextField();
        animalQTCapacity.setToolTipText("Set the capacity of a square in the Animal Quad Tree");
        animalQTCapacity.addKeyListener(new KeyAdapter() {
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                    try {
                        int capacity = Integer.parseInt(animalQTCapacity.getText());
                        if(capacity > 0){
                            s.getWorld().getAnimalQuadTree().setCapacity(capacity);
                        }
                        // Set the capacity of your quad tree here
                    }
                    catch (NumberFormatException ex) {
                        // Handle the case where the user enters an invalid value
                    }
                }
            }
        });

        JTextField plantQTCapacity = new JTextField();
        plantQTCapacity.setToolTipText("Set the capacity of a square in the Plant Quad Tree");
        plantQTCapacity.addKeyListener(new KeyAdapter() {
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                    try {
                        int capacity = Integer.parseInt(plantQTCapacity.getText());
                        if(capacity > 0){
                            s.getWorld().getPlantQuadTree().setCapacity(capacity);
                        }
                        // Set the capacity of your quad tree here
                    }
                    catch (NumberFormatException ex) {
                        // Handle the case where the user enters an invalid value
                    }
                }
            }
        });

        JTextField animalQTMaxDepth = new JTextField();
        animalQTMaxDepth.setToolTipText("Set the maximum depth of the Animal Quad Tree");
        animalQTMaxDepth.addKeyListener(new KeyAdapter() {
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                    try {
                        int maxDepth = Integer.parseInt(animalQTMaxDepth.getText());
                        if(maxDepth > 0){
                            s.getWorld().getAnimalQuadTree().setMaxDepth(maxDepth);
                        }
                        // Set the capacity of your quad tree here
                    }
                    catch (NumberFormatException ex) {
                        // Handle the case where the user enters an invalid value
                    }
                }
            }
        });

        JTextField plantQTMaxDepth = new JTextField();
        plantQTMaxDepth.setToolTipText("Set the maximum depth of the Plant Quad Tree");
        plantQTMaxDepth.addKeyListener(new KeyAdapter() {
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                    try {
                        int maxDepth = Integer.parseInt(plantQTMaxDepth.getText());
                        if(maxDepth > 0){
                            s.getWorld().getPlantQuadTree().setMaxDepth(maxDepth);
                        }
                        // Set the capacity of your quad tree here
                    }
                    catch (NumberFormatException ex) {
                        // Handle the case where the user enters an invalid value
                    }
                }
            }
        });

        //TODO create rangeSliders
        //Slider for maxPlants
        this.maxPlantsPanel = new JPanel(new BorderLayout());
        int startingValue = 2000;
        this.maxPlantsSlider = new JSlider(JSlider.HORIZONTAL, 0, 50000, startingValue);
        this.maxPlantsSlider.setMajorTickSpacing(10000);
        this.maxPlantsSlider.setMinorTickSpacing(5000);
        this.maxPlantsSlider.setPaintTicks(true);
        this.maxPlantsSlider.setPaintTrack(true);
        this.maxPlantsLabel = new JLabel("Max Plants: " + startingValue, JLabel.CENTER);
        s.setMaxPlants(startingValue);
        this.maxPlantsSlider.addChangeListener(e -> {
            JSlider source = (JSlider)e.getSource();
            int maxPlants = source.getValue();
            int minPlants = s.getMinNumPlants();
            if(minPlants > maxPlants){
                this.minPlantsSlider.setValue(maxPlants);
            }
            this.maxPlantsLabel.setText("Max Plants: " + maxPlants);
            s.setMaxPlants(maxPlants);

        });
        this.maxPlantsPanel.add(this.maxPlantsLabel, BorderLayout.NORTH);
        this.maxPlantsPanel.add(this.maxPlantsSlider, BorderLayout.CENTER);

        //Slider for minPlants
        this.minPlantsPanel = new JPanel(new BorderLayout());
        startingValue = 1;
        this.minPlantsSlider = new JSlider(JSlider.HORIZONTAL, 0, 10000, startingValue);
        this.minPlantsSlider.setMajorTickSpacing(2500);
        this.minPlantsSlider.setMinorTickSpacing(1250);
        this.minPlantsSlider.setPaintTicks(true);
        this.minPlantsSlider.setPaintTrack(true);
        this.minPlantsLabel = new JLabel("Min Plants: " + startingValue, JLabel.CENTER);
        s.setMinNumPlants(startingValue);
        this.minPlantsSlider.addChangeListener(e -> {
            JSlider source = (JSlider)e.getSource();
            int minPlants = source.getValue();
            int maxPlants = this.maxPlantsSlider.getValue();
            if(minPlants > maxPlants){
                this.maxPlantsSlider.setValue(minPlants);
            }
            this.minPlantsLabel.setText("Min Plants: " + minPlants);
            s.setMinNumPlants(minPlants);

        });
        this.minPlantsPanel.add(this.minPlantsLabel, BorderLayout.NORTH);
        this.minPlantsPanel.add(this.minPlantsSlider, BorderLayout.CENTER);

        //Slider for amount plants respawned
        JPanel plantRespawnAmountPanel = new JPanel(new BorderLayout());
        startingValue = 1;
        JSlider plantRespawnAmountSlider = new JSlider(JSlider.HORIZONTAL, 0, 100, startingValue);
        plantRespawnAmountSlider.setMajorTickSpacing(20);
        plantRespawnAmountSlider.setMinorTickSpacing(10);
        plantRespawnAmountSlider.setPaintTicks(true);
        plantRespawnAmountSlider.setPaintTrack(true);
        JLabel plantRespawnAmountLabel = new JLabel("Respawned Plants at once: " + startingValue, JLabel.CENTER);
        s.setNumNewPlants(startingValue);
        plantRespawnAmountSlider.addChangeListener(e -> {
            JSlider source = (JSlider)e.getSource();
            int numNewPlants = source.getValue();
            plantRespawnAmountLabel.setText("Respawned Plants at once: " + numNewPlants);
            s.setNumNewPlants(numNewPlants);

        });
        plantRespawnAmountPanel.add(plantRespawnAmountLabel, BorderLayout.NORTH);
        plantRespawnAmountPanel.add(plantRespawnAmountSlider, BorderLayout.CENTER);

        //Slider for amount animals spawned
        JPanel animalRespawnAmountPanel = new JPanel(new BorderLayout());
        startingValue = 2;
        JSlider animalRespawnAmountSlider = new JSlider(JSlider.HORIZONTAL, 0, 100, startingValue);
        animalRespawnAmountSlider.setMajorTickSpacing(20);
        animalRespawnAmountSlider.setMinorTickSpacing(10);
        animalRespawnAmountSlider.setPaintTicks(true);
        animalRespawnAmountSlider.setPaintTrack(true);
        JLabel animalRespawnAmountLabel = new JLabel("Respawned Animals at once: " + startingValue, JLabel.CENTER);
        s.setNumNewAnimals(startingValue);
        animalRespawnAmountSlider.addChangeListener(e -> {
            JSlider source = (JSlider)e.getSource();
            int numNewAnimals = source.getValue();
            animalRespawnAmountLabel.setText("Respawned Animals at once: " + numNewAnimals);
            s.setNumNewAnimals(numNewAnimals);

        });
        animalRespawnAmountPanel.add(animalRespawnAmountLabel, BorderLayout.NORTH);
        animalRespawnAmountPanel.add(animalRespawnAmountSlider, BorderLayout.CENTER);

        //Slider for maxAnimals
        this.maxAnimalsPanel = new JPanel(new BorderLayout());
        startingValue = 3000;
        this.maxAnimalsSlider = new JSlider(JSlider.HORIZONTAL, 0, 100000, startingValue);
        this.maxAnimalsSlider.setMajorTickSpacing(25000);
        this.maxAnimalsSlider.setMinorTickSpacing(12500);
        this.maxAnimalsSlider.setPaintTicks(true);
        this.maxAnimalsSlider.setPaintTrack(true);
        this.maxAnimalsLabel = new JLabel("Max Animals: " + startingValue, JLabel.CENTER);
        s.setMaxAnimals(startingValue);
        this.maxAnimalsSlider.addChangeListener(e -> {
            JSlider source = (JSlider)e.getSource();
            int maxAnimals = source.getValue();
            int minAnimals = s.getMinNumAnimals();
            if(minAnimals > maxAnimals){
                this.minAnimalsSlider.setValue(maxAnimals);
            }
            maxAnimalsLabel.setText("Max Animals: " + maxAnimals);
            s.setMaxAnimals(maxAnimals);

        });
        this.maxAnimalsPanel.add(this.maxAnimalsLabel, BorderLayout.NORTH);
        this.maxAnimalsPanel.add(this.maxAnimalsSlider, BorderLayout.CENTER);

        //Slider for minAnimals
        this.minAnimalsPanel = new JPanel(new BorderLayout());
        startingValue = 1000;
        this.minAnimalsSlider = new JSlider(JSlider.HORIZONTAL, 0, 10000, startingValue);
        this.minAnimalsSlider.setMajorTickSpacing(2500);
        this.minAnimalsSlider.setMinorTickSpacing(1250);
        this.minAnimalsSlider.setPaintTicks(true);
        this.minAnimalsSlider.setPaintTrack(true);
        this.minAnimalsLabel = new JLabel("Min Animals: " + startingValue, JLabel.CENTER);
        s.setMinNumAnimals(startingValue);
        this.minAnimalsSlider.addChangeListener(e -> {
            JSlider source = (JSlider)e.getSource();
            int minAnimals = source.getValue();
            int maxAnimals = this.maxAnimalsSlider.getValue();
            if(minAnimals > maxAnimals){
                this.maxAnimalsSlider.setValue(minAnimals);
            }
            this.minAnimalsLabel.setText("Min Animals: " + minAnimals);
            s.setMinNumAnimals(minAnimals);

        });
        this.minAnimalsPanel.add(this.minAnimalsLabel, BorderLayout.NORTH);
        this.minAnimalsPanel.add(this.minAnimalsSlider, BorderLayout.CENTER);

        //Simulation Speed Slider
        this.simulationSpeedPanel = new JPanel(new BorderLayout());
        startingValue = 100;
        this.simulationSpeedSlider = new JSlider(JSlider.HORIZONTAL,0,120,startingValue);
        this.simulationSpeedSlider.setMajorTickSpacing(10);
        this.simulationSpeedSlider.setPaintTrack(true);
        this.simulationSpeedLabel = new JLabel("Frames per Sec: " + startingValue, JLabel.CENTER);
        s.setTimerDelay(1000/startingValue);
        this.simulationSpeedSlider.addChangeListener(e ->{
            JSlider source = (JSlider)e.getSource();
            int simulationSpeed = source.getValue();
            this.simulationSpeedLabel.setText("Frames per Sec: " + simulationSpeed);
            //TODO make the time since start stop when simulation stops
            if(simulationSpeed <= 0){
                s.stopSimulation();
            }
            else{
                s.startSimulation();
                s.setTimerDelay(1000/simulationSpeed);
            }
        });
        this.simulationSpeedPanel.add(this.simulationSpeedLabel, BorderLayout.NORTH);
        this.simulationSpeedPanel.add(this.simulationSpeedSlider, BorderLayout.CENTER);

        this.fpsLabel = new JLabel();
        JLabel timeLabel = new JLabel();
        Timer timer = new Timer(1000, new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                fpsLabel.setText("FPS: " + s.getFps());

                double timeInSeconds = (System.currentTimeMillis() - s.startTime) / 1000.0;
                int hours = (int) (timeInSeconds / 3600);
                int minutes = (int) ((timeInSeconds % 3600) / 60);
                int seconds = (int) (timeInSeconds % 60);

                String formattedTime = String.format("Runtime: %02d:%02d:%02d", hours, minutes, seconds);
                timeLabel.setText(formattedTime);
            }
        });
        timer.start();

        // Create a 2D array to hold your statistics data
        this.animalData = new Object[][]{
                { "Amount of Animals: " , s.getAnimals().size() },
                { "All-time of Animals: " , Animal.aniCount },

                { "Average Age: ", Animal.avgAge },
                { "Average Animals Killed: ", Animal.avgAniKilled},
                { "Average Plants Killed: ", Animal.avgPlaKilled},
                { "Average Offspring Birthed: ", Animal.avgOffspringBirthed},

                { "Average Max Health: ", Animal.avgMaxHealth },
                { "Average Health: ", Animal.avgHealth },
                { "Average Health Ratio: ", Animal.avgHealthRatio },

                { "Average Max Energy: ", Animal.avgMaxEnergy },
                { "Average Energy: ", Animal.avgEnergy },
                { "Average Energy Ratio: ", Animal.avgEnergyRatio },

                { "All-time Animals born: ", Animal.aniBornCount}
                // Add more rows as needed
        };

        // Create an array of column names
        String[] columnNamesAnimals = { "Statistic Name", "Value" };

        // Create the JTable with the data and column names
        JTable animalStatTable = new JTable(this.animalData, columnNamesAnimals);

        // Add the JScrollPane to your statPanel
        this.animalStatPanel = new JScrollPane(animalStatTable);
        this.statPanel.addTab("Animals", this.animalStatPanel);

        // Create a 2D array to hold your statistics data
        this.plantData = new Object[][]{
                { "Amount of Plants: " , s.getPlants().size() },
                { "All-time of Plants: " , Plant.plaCount },
                { "Average Age: ", Plant.avgAge },
                //{ "Average Animals Killed: ", s.getAVGAnimalsKilled()},
                //{ "Average Plants Killed: ", s.getAVGPlantsKilled()},
                //{ "Average Offspring Birthed: ", s.getAVGOffspringBirthed()},

                { "Average Max Health: ", Plant.avgMaxHealth },
                { "Average Health: ", Plant.avgHealth },
                { "Average Health Ratio: ", Plant.avgHealthRatio },

                { "Average Max Energy: ", Plant.avgMaxEnergy },
                { "Average Energy: ", Plant.avgEnergy },
                { "Average Energy Ratio: ", Plant.avgEnergyRatio },

                //{ "All-time Animals born: ", Animal.aniBornCount}
                // Add more rows as needed
        };

        // Create an array of column names
        String[] columnNamesPlants = { "Statistic Name", "Value" };

        // Create the JTable with the data and column names
        JTable plantStatTable = new JTable(this.plantData, columnNamesPlants);

        // Add the JScrollPane to your statPanel
        this.plantStatPanel = new JScrollPane(plantStatTable);
        this.statPanel.addTab("Plants", this.plantStatPanel);

        Timer statRefreshTimer = new Timer(2000, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Update the table data here
                animalData[0][1] = s.getAnimals().size();
                animalData[1][1] = Animal.aniCount;

                animalData[2][1] = String.format("%.2f", Animal.avgAge);
                animalData[3][1] = Math.round(Animal.avgAniKilled);
                animalData[4][1] = Math.round(Animal.avgPlaKilled);
                animalData[5][1] = Math.round(Animal.avgOffspringBirthed);

                animalData[6][1] = String.format("%.2f", Animal.avgMaxHealth);
                animalData[7][1] = String.format("%.2f", Animal.avgHealth);
                animalData[8][1] = String.format("%.2f", Animal.avgHealthRatio);

                animalData[9][1] = String.format("%.2f", Animal.avgMaxEnergy);
                animalData[10][1] = String.format("%.2f", Animal.avgEnergy);
                animalData[11][1] = String.format("%.2f", Animal.avgEnergyRatio);

                animalData[12][1] = Animal.aniBornCount;

                plantData[0][1] = s.getPlants().size();
                plantData[1][1] = Plant.plaCount;
                plantData[2][1] = String.format("%.2f", Plant.avgAge);
                //plantData[3][1] = Math.round(Animal.avgAniKilled);
                //plantData[4][1] = Math.round(Animal.avgPlaKilled);
                //plantData[5][1] = Math.round(Animal.avgOffspringBirthed);

                plantData[3][1] = String.format("%.2f", Plant.avgMaxHealth);
                plantData[4][1] = String.format("%.2f", Plant.avgHealth);
                plantData[5][1] = String.format("%.2f", Plant.avgHealthRatio);

                plantData[6][1] = String.format("%.2f", Plant.avgMaxEnergy);
                plantData[7][1] = String.format("%.2f", Plant.avgEnergy);
                plantData[8][1] = String.format("%.2f", Plant.avgEnergyRatio);

                // Repaint the table
                statPanel.repaint();
            }
        });
        statRefreshTimer.start();

        //Add the buttons and sliders to the setting panel
        this.animalSettingsPanel.add(this.showHealthCheckBox);
        this.animalSettingsPanel.add(this.showEnergyCheckBox);
        this.animalSettingsPanel.add(showAccelerationCheckBox);
        this.animalSettingsPanel.add(showDirectionCheckBox);
        this.animalSettingsPanel.add(showSensoryRadiusCheckBox);
        this.animalSettingsPanel.add(this.showAnimalQTCheckBox);
        this.animalSettingsPanel.add(animalQTCapacity);
        this.animalSettingsPanel.add(animalQTMaxDepth);

        this.plantSettingPanel.add(this.showPlantQTCheckBox);
        this.plantSettingPanel.add(plantQTCapacity);
        this.plantSettingPanel.add(plantQTMaxDepth);
        this.worldSettingPanel.add(this.minPlantsPanel);
        this.worldSettingPanel.add(this.maxPlantsPanel);
        this.worldSettingPanel.add(plantRespawnAmountPanel);
        this.worldSettingPanel.add(animalRespawnAmountPanel);
        this.worldSettingPanel.add(this.minAnimalsPanel);
        this.worldSettingPanel.add(this.maxAnimalsPanel);
        this.worldSettingPanel.add(this.simulationSpeedPanel);

        //Add info in the stat panel
        this.worldStatPanel.add(this.fpsLabel);
        this.worldStatPanel.add(timeLabel);

        this.controlPane.setResizeWeight(.5);
        this.controlPane.setTopComponent(settingsPane);
        this.controlPane.setBottomComponent(statPanel);

        this.add(controlPane, BorderLayout.EAST);
    }
}
