# Nanobot Simulation: SIM Card to Nanobot Conversion

A Python-based simulation framework for converting SIM cards into functional nanobots with control systems, communication interfaces, and visualization capabilities.

## Overview

This project explores the conceptual transformation of a SIM card into a nanobot, maintaining the SIM card's communication capabilities while adding sensors, actuators, and autonomous control systems at the nanoscale.

## Features

- **SIM Card Modeling**: Simulate SIM card properties and conversion process
- **Nanobot Physics**: Realistic nanobot behavior with position, velocity, and energy management
- **Control Systems**: Advanced swarm control with formation patterns and task scheduling
- **Communication**: Nanobot-to-nanobot and base station communication protocols
- **Visualization**: 2D/3D plotting, animations, and sensor heatmaps
- **Sensor Suite**: Temperature, pressure, proximity, and chemical sensors

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

```
staff/
├── src/
│   ├── nanobot.py          # Core nanobot class with physics and sensors
│   ├── sim_card.py         # SIM card model and conversion system
│   ├── control_system.py   # Swarm control and task scheduling
│   └── visualization.py    # Plotting and animation tools
├── examples/
│   ├── basic_simulation.py # Simple nanobot demo
│   ├── swarm_demo.py       # Multi-bot swarm demonstration
│   └── conversion_demo.py  # SIM-to-nanobot conversion example
├── tests/                  # Unit tests (future)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Quick Start

### Basic Nanobot Creation

```python
from src.nanobot import Nanobot
import numpy as np

# Create a nanobot
bot = Nanobot(bot_id="NB-001", initial_position=(0, 0, 0))

# Move the nanobot
bot.move(direction=np.array([1, 0, 0]), speed=2.0)

# Sense the environment
sensor_data = bot.sense_environment()

# Get status
print(bot.get_status())
```

### SIM Card Conversion

```python
from src.sim_card import SIMCard, SIMToNanobotConverter

# Create a SIM card
sim = SIMCard(iccid="89014103211234567890", 
              imsi="310150123456789",
              network_provider="NanoNet")

# Configure for nanobot conversion
sim.configure_nanobot({
    "sensor_suite": ["temperature", "pressure", "chemical"],
    "operating_mode": "autonomous"
})

# Convert to nanobot
converter = SIMToNanobotConverter()
nanobot_params = converter.convert(sim)
print(f"Created nanobot: {nanobot_params['bot_id']}")
```

### Swarm Control

```python
from src.nanobot import Nanobot
from src.control_system import ControlSystem
from src.visualization import NanobotVisualizer

# Create control system
control = ControlSystem()

# Register multiple nanobots
for i in range(10):
    bot = Nanobot(f"NB-{i:03d}", initial_position=(
        np.random.uniform(-10, 10),
        np.random.uniform(-10, 10),
        np.random.uniform(-10, 10)
    ))
    control.register_nanobot(bot)

# Form sphere pattern
control.swarm_formation(formation_type="sphere", radius=20.0)

# Visualize
viz = NanobotVisualizer(control)
viz.plot_swarm_3d(show_velocity=True, show_battery=True)
```

## Examples

Run the example scripts to see the system in action:

```bash
python examples/basic_simulation.py
python examples/swarm_demo.py
python examples/conversion_demo.py
```

## Core Components

### Nanobot Class
- Position and velocity tracking
- Battery/energy management
- Environmental sensors
- Communication capabilities
- Status monitoring

### SIM Card Class
- ICCID/IMSI authentication
- Memory and processor modeling
- Contact and message storage
- Nanobot configuration
- Conversion process simulation

### Control System
- Multi-bot registration and management
- Navigation and path planning
- Swarm formation patterns (sphere, grid, line)
- Broadcast communication
- Sensor data aggregation
- Status reporting

### Visualization Tools
- 3D swarm plotting
- Battery level charts
- Trajectory tracking
- Animated simulations
- Sensor heatmaps
- Status reports

## Technical Details

### Scale
- Nanobot size: ~0.85 nm (based on scaled SIM chip dimensions)
- Coordinates in nanometers (nm)
- Operating temperature: 310 K (body temperature)

### Energy Model
- Battery capacity: 0-100%
- Movement cost: 0.1% per unit speed
- Communication cost: 1% per message
- Idle consumption: 0.01% per update
- Recharge from environmental sources

### Communication Protocol
- RF-based (simulated)
- Message queue system
- Signal strength based on battery level
- Broadcast and targeted messaging

## Future Enhancements

- [ ] Add collision avoidance algorithms
- [ ] Implement chemical delivery mechanisms
- [ ] Add medical diagnostic scenarios
- [ ] Real-time pygame visualization
- [ ] Machine learning for autonomous behavior
- [ ] Network topology optimization
- [ ] Multi-threaded simulation for large swarms

## Requirements

- Python 3.8+
- NumPy 1.21+
- Matplotlib 3.4+

## License

This is a simulation/educational project. Use freely for learning and research purposes.

## Contributing

Feel free to fork and extend this simulation with additional features!

## Contact

For questions or suggestions, please open an issue in the repository.
