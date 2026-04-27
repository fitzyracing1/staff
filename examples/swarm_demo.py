"""
Swarm Demonstration Example

Shows multi-bot swarm control with formations and visualization.
"""
import numpy as np
from src.nanobot import Nanobot
from src.control_system import ControlSystem
from src.visualization import NanobotVisualizer, generate_report


def main():
    print("=" * 60)
    print("NANOBOT SWARM DEMONSTRATION")
    print("=" * 60)
    
    # Create control system
    print("\n1. Initializing control system...")
    control = ControlSystem()
    
    # Create multiple nanobots
    print("\n2. Creating nanobot swarm (15 bots)...")
    n_bots = 15
    for i in range(n_bots):
        # Random initial positions
        pos = (
            np.random.uniform(-20, 20),
            np.random.uniform(-20, 20),
            np.random.uniform(-20, 20)
        )
        bot = Nanobot(f"NB-{i:03d}", initial_position=pos)
        control.register_nanobot(bot)
        print(f"   Registered: {bot.bot_id} at position {np.array(pos).round(1)}")
    
    # Display initial status
    print("\n3. Initial swarm status:")
    status = control.get_swarm_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Form sphere pattern
    print("\n4. Forming sphere pattern...")
    control.swarm_formation(formation_type="sphere", 
                          center=(0, 0, 0), 
                          radius=25.0)
    print(f"   Formation targets set for {len(control.formation_targets)} bots")
    
    # Move toward formation
    print("\n5. Moving to formation (20 steps)...")
    for step in range(20):
        control.maintain_formation(speed=1.5)
        control.update_all(dt=0.1)
        if step % 5 == 0:
            status = control.get_swarm_status()
            print(f"   Step {step}: Avg battery = {status['average_battery']:.1f}%, "
                  f"Active bots = {status['active_bots']}")
    
    # Broadcast message
    print("\n6. Broadcasting message to swarm...")
    control.broadcast_message("Formation complete. Standing by.")
    print("   Message sent to all nanobots")
    
    # Collect sensor data
    print("\n7. Collecting sensor data from swarm...")
    sensor_data = control.collect_sensor_data()
    temps = [data['temperature'] for data in sensor_data.values()]
    avg_temp = np.mean(temps)
    print(f"   Average temperature: {avg_temp:.2f} K")
    print(f"   Temperature range: {min(temps):.2f} - {max(temps):.2f} K")
    
    # Switch to grid formation
    print("\n8. Switching to grid formation...")
    control.swarm_formation(formation_type="grid", 
                          center=(0, 0, 0), 
                          radius=20.0)
    
    for step in range(20):
        control.maintain_formation(speed=1.5)
        control.update_all(dt=0.1)
    
    print("   Grid formation complete")
    
    # Recharge all bots
    print("\n9. Recharging all nanobots...")
    status_before = control.get_swarm_status()
    control.recharge_all(amount=30.0)
    status_after = control.get_swarm_status()
    print(f"   Battery: {status_before['average_battery']:.1f}% → "
          f"{status_after['average_battery']:.1f}%")
    
    # Generate final report
    print("\n10. Final Status Report:")
    report = generate_report(control)
    print(report)
    
    # Visualize if matplotlib is available
    print("\n11. Generating visualizations...")
    try:
        viz = NanobotVisualizer(control)
        
        print("   Creating 3D swarm plot...")
        viz.plot_swarm_3d(show_velocity=True, show_battery=True)
        
        print("   Creating battery level chart...")
        viz.plot_battery_levels()
        
        print("   Creating sensor heatmap...")
        viz.plot_sensor_heatmap(sensor_type="temperature")
        
    except Exception as e:
        print(f"   Visualization skipped: {e}")
    
    print("\n" + "=" * 60)
    print("SWARM DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
