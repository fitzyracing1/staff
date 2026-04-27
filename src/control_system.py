"""
Control System - Manages nanobot behavior, navigation, and task execution.
"""
import numpy as np
from typing import List, Tuple, Dict, Any, Optional, Callable
from src.nanobot import Nanobot


class ControlSystem:
    """
    Advanced control system for managing individual nanobots or swarms.
    Implements navigation, task scheduling, and coordination algorithms.
    """
    
    def __init__(self):
        self.nanobots: Dict[str, Nanobot] = {}
        self.tasks = []
        self.formation_targets = {}
        
    def register_nanobot(self, nanobot: Nanobot) -> None:
        """Register a nanobot with the control system."""
        self.nanobots[nanobot.bot_id] = nanobot
    
    def unregister_nanobot(self, bot_id: str) -> None:
        """Remove a nanobot from the control system."""
        if bot_id in self.nanobots:
            del self.nanobots[bot_id]
    
    def navigate_to_target(self, bot_id: str, target: Tuple[float, float, float], 
                          speed: float = 1.0) -> bool:
        """
        Navigate a nanobot to a target position.
        
        Args:
            bot_id: Nanobot identifier
            target: Target (x, y, z) coordinates
            speed: Movement speed
            
        Returns:
            True if navigation command accepted
        """
        if bot_id not in self.nanobots:
            return False
        
        bot = self.nanobots[bot_id]
        target_array = np.array(target)
        
        # Calculate direction vector
        direction = target_array - bot.position
        distance = np.linalg.norm(direction)
        
        if distance > 0.1:  # Not at target yet
            bot.move(direction, speed)
            return True
        
        return False
    
    def swarm_formation(self, formation_type: str = "sphere", 
                       center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
                       radius: float = 10.0) -> None:
        """
        Arrange nanobots in a formation.
        
        Args:
            formation_type: Type of formation ("sphere", "grid", "line")
            center: Center point of formation
            radius: Formation radius
        """
        n_bots = len(self.nanobots)
        if n_bots == 0:
            return
        
        bot_list = list(self.nanobots.values())
        
        if formation_type == "sphere":
            # Distribute bots evenly on sphere surface
            phi = np.pi * (3.0 - np.sqrt(5.0))  # Golden angle
            for i, bot in enumerate(bot_list):
                y = 1 - (i / float(n_bots - 1 if n_bots > 1 else 1)) * 2
                radius_at_y = np.sqrt(1 - y * y) * radius
                theta = phi * i
                
                x = np.cos(theta) * radius_at_y + center[0]
                z = np.sin(theta) * radius_at_y + center[2]
                y = y * radius + center[1]
                
                self.formation_targets[bot.bot_id] = (x, y, z)
        
        elif formation_type == "grid":
            # Arrange in 3D grid
            grid_size = int(np.ceil(n_bots ** (1/3)))
            spacing = radius * 2 / max(grid_size - 1, 1)
            
            for i, bot in enumerate(bot_list):
                x_idx = i % grid_size
                y_idx = (i // grid_size) % grid_size
                z_idx = i // (grid_size * grid_size)
                
                x = (x_idx - grid_size / 2) * spacing + center[0]
                y = (y_idx - grid_size / 2) * spacing + center[1]
                z = (z_idx - grid_size / 2) * spacing + center[2]
                
                self.formation_targets[bot.bot_id] = (x, y, z)
        
        elif formation_type == "line":
            # Arrange in a line
            spacing = radius * 2 / max(n_bots - 1, 1)
            for i, bot in enumerate(bot_list):
                x = (i - n_bots / 2) * spacing + center[0]
                y = center[1]
                z = center[2]
                
                self.formation_targets[bot.bot_id] = (x, y, z)
    
    def maintain_formation(self, speed: float = 1.0) -> None:
        """Move all nanobots toward their formation targets."""
        for bot_id, target in self.formation_targets.items():
            self.navigate_to_target(bot_id, target, speed)
    
    def broadcast_message(self, message: str, sender_id: str = "control") -> None:
        """Broadcast a message to all nanobots."""
        for bot in self.nanobots.values():
            bot.receive_message({
                "from": sender_id,
                "to": bot.bot_id,
                "message": message,
                "timestamp": np.random.randint(0, 1000000)
            })
    
    def collect_sensor_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Collect sensor data from all nanobots.
        
        Returns:
            Dictionary mapping bot_id to sensor readings
        """
        sensor_data = {}
        for bot_id, bot in self.nanobots.items():
            sensor_data[bot_id] = bot.sense_environment()
        return sensor_data
    
    def get_swarm_status(self) -> Dict[str, Any]:
        """
        Get comprehensive status of the swarm.
        
        Returns:
            Dictionary with swarm statistics
        """
        if not self.nanobots:
            return {
                "total_bots": 0,
                "active_bots": 0,
                "inactive_bots": 0,
                "average_battery": 0.0,
                "center_of_mass": [0.0, 0.0, 0.0]
            }
        
        active_count = sum(1 for bot in self.nanobots.values() if bot.status == "active")
        avg_battery = np.mean([bot.battery_level for bot in self.nanobots.values()])
        
        # Calculate center of mass
        positions = np.array([bot.position for bot in self.nanobots.values()])
        center_of_mass = np.mean(positions, axis=0)
        
        return {
            "total_bots": len(self.nanobots),
            "active_bots": active_count,
            "inactive_bots": len(self.nanobots) - active_count,
            "average_battery": float(avg_battery),
            "center_of_mass": center_of_mass.tolist(),
            "formation_active": len(self.formation_targets) > 0
        }
    
    def recharge_all(self, amount: float = 10.0) -> None:
        """Recharge all nanobots."""
        for bot in self.nanobots.values():
            bot.recharge(amount)
    
    def update_all(self, dt: float = 0.1) -> None:
        """Update all nanobots for one time step."""
        for bot in self.nanobots.values():
            bot.update(dt)


class TaskScheduler:
    """
    Schedules and manages tasks for nanobots.
    """
    
    def __init__(self, control_system: ControlSystem):
        self.control_system = control_system
        self.task_queue = []
        self.completed_tasks = []
    
    def add_task(self, task_name: str, target_bot: str, 
                 action: Callable, priority: int = 0) -> None:
        """
        Add a task to the queue.
        
        Args:
            task_name: Descriptive name for the task
            target_bot: Bot ID to execute the task
            action: Callable function to execute
            priority: Task priority (higher = more important)
        """
        self.task_queue.append({
            "name": task_name,
            "target": target_bot,
            "action": action,
            "priority": priority,
            "status": "queued"
        })
        
        # Sort by priority
        self.task_queue.sort(key=lambda x: x["priority"], reverse=True)
    
    def execute_next_task(self) -> Optional[Dict[str, Any]]:
        """Execute the next task in the queue."""
        if not self.task_queue:
            return None
        
        task = self.task_queue.pop(0)
        task["status"] = "executing"
        
        try:
            task["action"]()
            task["status"] = "completed"
            self.completed_tasks.append(task)
            return task
        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
            return task
    
    def get_task_status(self) -> Dict[str, Any]:
        """Get current task queue status."""
        return {
            "queued": len(self.task_queue),
            "completed": len(self.completed_tasks),
            "next_task": self.task_queue[0]["name"] if self.task_queue else None
        }
