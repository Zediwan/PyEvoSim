package Main;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class SimulationGUI extends JFrame {
    private JPanel simPanel;
    private JScrollPane scrollPane;
    private JPanel graphPanel;

    private JSplitPane controlPane;

    private JTabbedPane settingsPane;
    private JPanel animalSettingsPanel;
    private JPanel plantSettingPanel;
    private JPanel organismSettingPanel;
    private JPanel worldSettingPanel;

    private JTabbedPane statPanel;
    private final JPanel animalStatPanel;
    private final JPanel plantStatPanel;
    private final JPanel organismStatPanel;
    private final JPanel worldStatPanel;

    private JCheckBox showHealthCheckBox;
    private JCheckBox showEnergyCheckBox;

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

    public static boolean showHealth = false;
    public static boolean showEnergy = false;
    public static int simulationSpeed = 10;

    public SimulationGUI() {
        // Set up main frame
        setTitle("Simulation");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Set up simulation panel
        World w =new World(5000,5000,10,10);
        Simulation s = new Simulation(50000,2000,80000,
                8000,5000,100,
                100,10,
                w);
        this.simPanel = s;
        this.simPanel.setPreferredSize(w.getWorldDimension()); // Set initial size
        this.scrollPane = new JScrollPane(this.simPanel);
        /*
        scrollPane.addMouseWheelListener(new MouseWheelListener() {
            public void mouseWheelMoved(MouseWheelEvent e) {
                System.out.println("Test");
                int notches = e.getWheelRotation();
                Dimension size = simPanel.getSize();
                double scale = 1.0 + (0.1 * notches); // Adjust scale based on mouse wheel
                size.width = (int) (size.width * scale);
                size.height = (int) (size.height * scale);
                simPanel.setPreferredSize(size);
                scrollPane.revalidate(); // Redraw scroll pane
            }
        });
         */
        this.scrollPane.setPreferredSize(new Dimension(800, 600)); // Set initial viewport size
        this.scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
        this.scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);
        this.add(scrollPane, BorderLayout.CENTER);

        // Set up bottom panel
        this.graphPanel = new JPanel();
        this.graphPanel.setLayout(new BoxLayout(graphPanel, BoxLayout.Y_AXIS));
        this.graphPanel.add(new JLabel("Simulation Statistics"));
        this.add(this.graphPanel, BorderLayout.SOUTH);

        // Set up right panel
        this.controlPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT);

        this.settingsPane = new JTabbedPane();
        this.animalSettingsPanel = new JPanel();
        this.plantSettingPanel = new JPanel();
        this.organismSettingPanel = new JPanel();
        this.worldSettingPanel = new JPanel(new GridLayout(0, 2));
        this.settingsPane.addTab("Animals", this.animalSettingsPanel);
        this.settingsPane.addTab("Plants", this.plantSettingPanel);
        this.settingsPane.addTab("Organisms", this.organismSettingPanel);
        this.settingsPane.addTab("World", this.worldSettingPanel);

        this.statPanel =  new JTabbedPane();
        this.animalStatPanel = new JPanel();
        this.plantStatPanel = new JPanel();
        this.organismStatPanel = new JPanel();
        this.worldStatPanel = new JPanel();
        this.statPanel.addTab("Animals", this.animalStatPanel);
        this.statPanel.addTab("Plants", this.plantStatPanel);
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

        //Show energy checkbox
        this.showEnergyCheckBox = new JCheckBox("Show Energy");
        this.showEnergyCheckBox.setToolTipText("Toggle the visualization of the current Energy");
        this.showEnergyCheckBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showEnergy = showEnergyCheckBox.isSelected();
            }
        });

        //TODO create rangeSliders
        //Slider for maxPlants
        this.maxPlantsPanel = new JPanel(new BorderLayout());
        this.maxPlantsSlider = new JSlider(JSlider.HORIZONTAL, 0, 100000, 10000);
        this.maxPlantsSlider.setMajorTickSpacing(25000);
        this.maxPlantsSlider.setMinorTickSpacing(12500);
        this.maxPlantsSlider.setPaintTicks(true);
        this.maxPlantsSlider.setPaintTrack(true);
        this.maxPlantsLabel = new JLabel("Max Plants: " + 10000, JLabel.CENTER);
        this.maxPlantsSlider.addChangeListener(e -> {
            JSlider source = (JSlider)e.getSource();
            int maxPlants = source.getValue();
            this.maxPlantsLabel.setText("Max Plants: " + maxPlants);
            s.setMaxPlants(maxPlants);

        });
        this.maxPlantsPanel.add(this.maxPlantsLabel, BorderLayout.NORTH);
        this.maxPlantsPanel.add(this.maxPlantsSlider, BorderLayout.CENTER);

        //Slider for minPlants
        this.minPlantsPanel = new JPanel(new BorderLayout());
        this.minPlantsSlider = new JSlider(JSlider.HORIZONTAL, 0, 100000, 100);
        this.minPlantsSlider.setMajorTickSpacing(25000);
        this.minPlantsSlider.setMinorTickSpacing(12500);
        this.minPlantsSlider.setPaintTicks(true);
        this.minPlantsSlider.setPaintTrack(true);
        this.minPlantsLabel = new JLabel("Min Plants: " + 10000, JLabel.CENTER);
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

        //Slider for maxAnimals
        this.maxAnimalsPanel = new JPanel(new BorderLayout());
        this.maxAnimalsSlider = new JSlider(JSlider.HORIZONTAL, 0, 100000, 10000);
        this.maxAnimalsSlider.setMajorTickSpacing(25000);
        this.maxAnimalsSlider.setMinorTickSpacing(12500);
        this.maxAnimalsSlider.setPaintTicks(true);
        this.maxAnimalsSlider.setPaintTrack(true);
        this.maxAnimalsLabel = new JLabel("Max Animals: " + 10000, JLabel.CENTER);
        this.maxAnimalsSlider.addChangeListener(e -> {
            JSlider source = (JSlider)e.getSource();
            int maxAnimals = source.getValue();
            maxAnimalsLabel.setText("Max Animals: " + maxAnimals);
            s.setMaxAnimals(maxAnimals);

        });
        this.maxAnimalsPanel.add(this.maxAnimalsLabel, BorderLayout.NORTH);
        this.maxAnimalsPanel.add(this.maxAnimalsSlider, BorderLayout.CENTER);

        //Slider for minAnimals
        this.minAnimalsPanel = new JPanel(new BorderLayout());
        this.minAnimalsSlider = new JSlider(JSlider.HORIZONTAL, 0, 100000, 10000);
        this.minAnimalsSlider.setMajorTickSpacing(25000);
        this.minAnimalsSlider.setMinorTickSpacing(12500);
        this.minAnimalsSlider.setPaintTicks(true);
        this.minAnimalsSlider.setPaintTrack(true);
        this.minAnimalsLabel = new JLabel("Min Animals: " + 10000, JLabel.CENTER);
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

        //Add the buttons and sliders to the setting panel
        this.animalSettingsPanel.add(showHealthCheckBox);
        this.animalSettingsPanel.add(showEnergyCheckBox);
        this.worldSettingPanel.add(maxPlantsPanel);
        this.worldSettingPanel.add(minPlantsPanel);
        this.worldSettingPanel.add(maxAnimalsPanel);
        this.worldSettingPanel.add(minAnimalsPanel);

        this.controlPane.setResizeWeight(.5);
        this.controlPane.setTopComponent(settingsPane);
        this.controlPane.setBottomComponent(statPanel);

        this.add(controlPane, BorderLayout.EAST);
    }
}
