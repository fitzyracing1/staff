"""
Nanobot class - Core nanobot simulation with physical properties and behaviors.
"""
import numpy as np
from typing import Tuple, List, Dict, Any


class Nanobot:
    """
    Represents a nanobot created from a SIM card with physical properties,
    sensors, actuators, and communication capabilities.
    """
    
    def __init__(self, bot_id: str, initial_position: Tuple[float, float, float] = (0.0, 0.0, 0.0)):
        """
        Initialize a nanobot.
        
        Args:
            bot_id: Unique identifier for the nanobot
            initial_position: Initial (x, y, z) coordinates in nanometers
        """
        self.bot_id = bot_id
        self.position = np.array(initial_position, dtype=float)
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.size = 0.85  # nanometers (based on SIM card chip dimensions scaled down)
        
        # Physical properties
        self.battery_level = 100.0  # percentage
        self.temperature = 310.0  # Kelvin (body temperature)
        self.status = "active"
        
        # Sensors
        self.sensor_data = {
            "proximity": 0.0,
            "chemical": {},
            "temperature": self.temperature,
            "pressure": 101.325  # kPa
        }
        
        # Communication
        self.signal_strength = 100.0
        self.message_queue = []
        
    def move(self, direction: np.ndarray, speed: float = 1.0) -> None:
        """
        Move the nanobot in a specified direction.
        
        Args:
            direction: 3D vector indicating movement direction
            speed: Movement speed multiplier
        """
        if self.battery_level > 0:
            # Normalize direction vector
            direction = np.array(direction)
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            
            self.velocity = direction * speed
            self.position += self.velocity
            self.consume_energy(0.1 * speed)
    
    def consume_energy(self, amount: float) -> None:
        """Consume battery energy."""
        self.battery_level = max(0.0, self.battery_level - amount)
        if self.battery_level == 0:
            self.status = "inactive"
    
    def recharge(self, amount: float) -> None:
        """Recharge battery (e.g., from environmental energy)."""
        self.battery_level = min(100.0, self.battery_level + amount)
        if self.battery_level > 0:
            self.status = "active"
    
    def sense_environment(self) -> Dict[str, Any]:
        """
        Simulate environmental sensing.
        
        Returns:
            Dictionary of sensor readings
        """
        # Simulate sensor readings with some noise
        self.sensor_data["proximity"] = np.random.uniform(0, 100)
        self.sensor_data["temperature"] = self.temperature + np.random.normal(0, 0.5)
        self.sensor_data["pressure"] = 101.325 + np.random.normal(0, 1.0)
        
        return self.sensor_data.copy()
    
    def transmit_message(self, message: str, target_id: str = "base_station") -> bool:
        """
        Transmit a message via nanobot communication.
        
        Args:
            message: Message content
            target_id: Target receiver ID
            
        Returns:
            True if transmission successful
        """
        if self.battery_level > 5 and self.signal_strength > 10:
            self.message_queue.append({
                "from": self.bot_id,
                "to": target_id,
                "message": message,
                "timestamp": np.random.randint(0, 1000000)
            })
            self.consume_energy(1.0)
            return True
        return False
    
    def receive_message(self, message: Dict[str, Any]) -> None:
        """Receive and process an incoming message."""
        if message.get("to") == self.bot_id:
            self.message_queue.append(message)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current nanobot status.
        
        Returns:
            Dictionary containing all status information
        """
        return {
            "id": self.bot_id,
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist(),
            "battery": self.battery_level,
            "temperature": self.temperature,
            "status": self.status,
            "signal_strength": self.signal_strength,
            "messages": len(self.message_queue)
        }
    
    def update(self, dt: float = 0.1) -> None:
        """
        Update nanobot state for one time step.
        
        Args:
            dt: Time delta in seconds
        """
        # Passive energy consumption
        self.consume_energy(0.01)
        
        # Update temperature (gradual equilibration)
        target_temp = 310.0 + np.random.normal(0, 1.0)
        self.temperature += (target_temp - self.temperature) * 0.1
        
        # Signal strength varies with battery
        self.signal_strength = min(100.0, self.battery_level * 1.2)
