"""
Visualization - Tools for visualizing nanobot swarms and their behavior.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from typing import Dict, List, Any, Optional
from src.nanobot import Nanobot
from src.control_system import ControlSystem


class NanobotVisualizer:
    """
    Visualizes nanobots in 2D and 3D space.
    """
    
    def __init__(self, control_system: ControlSystem):
        self.control_system = control_system
        self.fig = None
        self.ax = None
        self.animation = None
    
    def plot_swarm_3d(self, show_velocity: bool = True, 
                      show_battery: bool = True) -> None:
        """
        Create a 3D plot of the nanobot swarm.
        
        Args:
            show_velocity: Display velocity vectors
            show_battery: Color-code by battery level
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        nanobots = list(self.control_system.nanobots.values())
        if not nanobots:
            print("No nanobots to visualize")
            return
        
        positions = np.array([bot.position for bot in nanobots])
        velocities = np.array([bot.velocity for bot in nanobots])
        batteries = np.array([bot.battery_level for bot in nanobots])
        
        # Color by battery level if requested
        if show_battery:
            colors = plt.cm.viridis(batteries / 100.0)
            scatter = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                               c=batteries, cmap='viridis', s=100, alpha=0.6,
                               vmin=0, vmax=100)
            plt.colorbar(scatter, ax=ax, label='Battery Level (%)')
        else:
            ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                      c='blue', s=100, alpha=0.6)
        
        # Show velocity vectors
        if show_velocity:
            for pos, vel in zip(positions, velocities):
                if np.linalg.norm(vel) > 0.01:
                    ax.quiver(pos[0], pos[1], pos[2],
                            vel[0], vel[1], vel[2],
                            color='red', alpha=0.5, arrow_length_ratio=0.3)
        
        ax.set_xlabel('X (nm)')
        ax.set_ylabel('Y (nm)')
        ax.set_zlabel('Z (nm)')
        ax.set_title('Nanobot Swarm Visualization')
        
        # Set equal aspect ratio
        max_range = np.array([positions[:, 0].max() - positions[:, 0].min(),
                             positions[:, 1].max() - positions[:, 1].min(),
                             positions[:, 2].max() - positions[:, 2].min()]).max() / 2.0
        
        mid_x = (positions[:, 0].max() + positions[:, 0].min()) * 0.5
        mid_y = (positions[:, 1].max() + positions[:, 1].min()) * 0.5
        mid_z = (positions[:, 2].max() + positions[:, 2].min()) * 0.5
        
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        plt.tight_layout()
        plt.show()
    
    def plot_battery_levels(self) -> None:
        """Plot battery levels for all nanobots."""
        nanobots = list(self.control_system.nanobots.values())
        if not nanobots:
            print("No nanobots to visualize")
            return
        
        bot_ids = [bot.bot_id for bot in nanobots]
        batteries = [bot.battery_level for bot in nanobots]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(bot_ids)), batteries)
        
        # Color bars based on battery level
        for bar, battery in zip(bars, batteries):
            if battery > 70:
                bar.set_color('green')
            elif battery > 30:
                bar.set_color('orange')
            else:
                bar.set_color('red')
        
        ax.set_xlabel('Nanobot')
        ax.set_ylabel('Battery Level (%)')
        ax.set_title('Nanobot Battery Levels')
        ax.set_xticks(range(len(bot_ids)))
        ax.set_xticklabels([f"Bot {i+1}" for i in range(len(bot_ids))], 
                          rotation=45, ha='right')
        ax.set_ylim(0, 100)
        ax.axhline(y=30, color='r', linestyle='--', alpha=0.5, label='Low Battery')
        ax.axhline(y=70, color='g', linestyle='--', alpha=0.5, label='Good Battery')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_trajectories(self, history: List[Dict[str, np.ndarray]], 
                         bot_ids: Optional[List[str]] = None) -> None:
        """
        Plot historical trajectories of nanobots.
        
        Args:
            history: List of position snapshots over time
            bot_ids: Optional list of specific bot IDs to plot
        """
        if not history:
            print("No history data to visualize")
            return
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Extract trajectories
        if bot_ids is None:
            bot_ids = list(history[0].keys())
        
        for bot_id in bot_ids:
            trajectory = np.array([snapshot[bot_id] for snapshot in history 
                                  if bot_id in snapshot])
            if len(trajectory) > 0:
                ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
                       alpha=0.6, linewidth=2, label=bot_id)
                
                # Mark start and end
                ax.scatter(*trajectory[0], c='green', s=100, marker='o')
                ax.scatter(*trajectory[-1], c='red', s=100, marker='x')
        
        ax.set_xlabel('X (nm)')
        ax.set_ylabel('Y (nm)')
        ax.set_zlabel('Z (nm)')
        ax.set_title('Nanobot Trajectories')
        ax.legend()
        
        plt.tight_layout()
        plt.show()
    
    def create_animation(self, duration: float = 10.0, fps: int = 30) -> None:
        """
        Create an animated visualization of the swarm.
        
        Args:
            duration: Animation duration in seconds
            fps: Frames per second
        """
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        def update(frame):
            self.ax.clear()
            
            # Update nanobot states
            self.control_system.update_all(0.1)
            self.control_system.maintain_formation(speed=0.5)
            
            # Get current positions
            nanobots = list(self.control_system.nanobots.values())
            if nanobots:
                positions = np.array([bot.position for bot in nanobots])
                batteries = np.array([bot.battery_level for bot in nanobots])
                
                scatter = self.ax.scatter(positions[:, 0], positions[:, 1], 
                                        positions[:, 2],
                                        c=batteries, cmap='viridis', s=100, 
                                        alpha=0.6, vmin=0, vmax=100)
                
                self.ax.set_xlabel('X (nm)')
                self.ax.set_ylabel('Y (nm)')
                self.ax.set_zlabel('Z (nm)')
                self.ax.set_title(f'Nanobot Swarm Animation (Frame {frame})')
                
                # Set consistent axis limits
                max_range = 50
                self.ax.set_xlim(-max_range, max_range)
                self.ax.set_ylim(-max_range, max_range)
                self.ax.set_zlim(-max_range, max_range)
        
        frames = int(duration * fps)
        self.animation = FuncAnimation(self.fig, update, frames=frames,
                                      interval=1000/fps, repeat=False)
        
        plt.show()
    
    def plot_sensor_heatmap(self, sensor_type: str = "temperature") -> None:
        """
        Create a heatmap of sensor readings across the swarm.
        
        Args:
            sensor_type: Type of sensor data to visualize
        """
        nanobots = list(self.control_system.nanobots.values())
        if not nanobots:
            print("No nanobots to visualize")
            return
        
        sensor_data = self.control_system.collect_sensor_data()
        
        positions = []
        values = []
        
        for bot_id, data in sensor_data.items():
            bot = self.control_system.nanobots[bot_id]
            positions.append(bot.position[:2])  # Use x, y only
            values.append(data.get(sensor_type, 0))
        
        positions = np.array(positions)
        values = np.array(values)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        scatter = ax.scatter(positions[:, 0], positions[:, 1],
                           c=values, cmap='coolwarm', s=200, alpha=0.6)
        
        plt.colorbar(scatter, ax=ax, label=f'{sensor_type.capitalize()}')
        ax.set_xlabel('X (nm)')
        ax.set_ylabel('Y (nm)')
        ax.set_title(f'Nanobot Swarm - {sensor_type.capitalize()} Sensor Readings')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


def generate_report(control_system: ControlSystem) -> str:
    """
    Generate a text report of the swarm status.
    
    Args:
        control_system: The control system managing the swarm
        
    Returns:
        Formatted report string
    """
    status = control_system.get_swarm_status()
    
    report = f"""
    ╔══════════════════════════════════════════════════════════╗
    ║           NANOBOT SWARM STATUS REPORT                    ║
    ╚══════════════════════════════════════════════════════════╝
    
    Total Nanobots:     {status['total_bots']}
    Active Nanobots:    {status['active_bots']}
    Inactive Nanobots:  {status['inactive_bots']}
    Average Battery:    {status['average_battery']:.1f}%
    Center of Mass:     ({status['center_of_mass'][0]:.2f}, 
                         {status['center_of_mass'][1]:.2f}, 
                         {status['center_of_mass'][2]:.2f}) nm
    Formation Active:   {status['formation_active']}
    
    ══════════════════════════════════════════════════════════
    """
    
    return report
