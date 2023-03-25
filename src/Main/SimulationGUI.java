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

    public static boolean showHealth = false;
    public static boolean showEnergy = false;
    private int simulationSpeed = 10;

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
        simPanel = s;
        simPanel.setPreferredSize(w.getWorldDimension()); // Set initial size
        scrollPane = new JScrollPane(simPanel);
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
        scrollPane.setPreferredSize(new Dimension(800, 600)); // Set initial viewport size
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
        scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);
        add(scrollPane, BorderLayout.CENTER);

        // Set up bottom panel
        graphPanel = new JPanel();
        graphPanel.setLayout(new BoxLayout(graphPanel, BoxLayout.Y_AXIS));
        graphPanel.add(new JLabel("Simulation Statistics"));
        add(graphPanel, BorderLayout.SOUTH);

        // Set up right panel
        this.controlPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT);

        this.settingsPane = new JTabbedPane();
        this.animalSettingsPanel = new JPanel();
        this.plantSettingPanel = new JPanel();
        this.organismSettingPanel = new JPanel();
        this.worldSettingPanel = new JPanel();
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
        JCheckBox showHealthCheckBox = new JCheckBox("Show Health");
        showHealthCheckBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showHealth = showHealthCheckBox.isSelected();
            }
        });

        //Show energy checkbox
        JCheckBox showEnergyCheckBox = new JCheckBox("Show Energy");
        showEnergyCheckBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showEnergy = showEnergyCheckBox.isSelected();
            }
        });

        //Slider for maxPlants
        JSlider maxPlantsSlider = new JSlider(JSlider.HORIZONTAL, 1000, 100000, 10000);
        maxPlantsSlider.setMajorTickSpacing(10000);
        maxPlantsSlider.setMinorTickSpacing(1000);
        maxPlantsSlider.setSize(new Dimension(controlPane.getWidth(), 50));
        maxPlantsSlider.setPaintTicks(true);
        maxPlantsSlider.setPaintLabels(true);
        JLabel maxPlantsLabel = new JLabel("Max Plants: " + 10000);
        maxPlantsSlider.addChangeListener(e -> {
            JSlider source = (JSlider)e.getSource();
            if (!source.getValueIsAdjusting()) {
                int maxPlants = source.getValue();
                maxPlantsLabel.setText("Max Plants: " + maxPlants);
                s.setMaxPlants(maxPlants);
            }
        });

        //Add the buttons and sliders to the setting panel
        this.animalSettingsPanel.add(showHealthCheckBox);
        this.animalSettingsPanel.add(showEnergyCheckBox);
        this.worldSettingPanel.add(maxPlantsSlider);
        this.worldSettingPanel.add(maxPlantsLabel);

        this.controlPane.setResizeWeight(.5);
        this.controlPane.setTopComponent(settingsPane);
        this.controlPane.setBottomComponent(statPanel);

        this.add(controlPane, BorderLayout.EAST);
    }
}
