"""
Basic Nanobot Simulation Example

Demonstrates basic nanobot creation, movement, and sensing.
"""
import numpy as np
from src.nanobot import Nanobot


def main():
    print("=" * 60)
    print("BASIC NANOBOT SIMULATION")
    print("=" * 60)
    
    # Create a nanobot
    print("\n1. Creating nanobot...")
    bot = Nanobot(bot_id="NB-001", initial_position=(0, 0, 0))
    print(f"   Created: {bot.bot_id}")
    print(f"   Initial position: {bot.position}")
    print(f"   Battery level: {bot.battery_level}%")
    
    # Move the nanobot
    print("\n2. Moving nanobot...")
    for i in range(5):
        direction = np.array([1.0, 0.5, 0.2])
        bot.move(direction, speed=2.0)
        print(f"   Step {i+1}: Position = {bot.position.round(2)}, "
              f"Battery = {bot.battery_level:.1f}%")
    
    # Sense environment
    print("\n3. Sensing environment...")
    sensor_data = bot.sense_environment()
    print(f"   Temperature: {sensor_data['temperature']:.2f} K")
    print(f"   Pressure: {sensor_data['pressure']:.2f} kPa")
    print(f"   Proximity: {sensor_data['proximity']:.2f}")
    
    # Send a message
    print("\n4. Communication test...")
    success = bot.transmit_message("Hello from nanobot!", "base_station")
    if success:
        print(f"   Message sent successfully")
        print(f"   Messages in queue: {len(bot.message_queue)}")
    
    # Recharge
    print("\n5. Recharging...")
    print(f"   Battery before: {bot.battery_level:.1f}%")
    bot.recharge(20.0)
    print(f"   Battery after: {bot.battery_level:.1f}%")
    
    # Final status
    print("\n6. Final status:")
    status = bot.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Simulate time steps
    print("\n7. Running simulation (10 time steps)...")
    for step in range(10):
        bot.update(dt=0.1)
        if step % 3 == 0:
            print(f"   Step {step}: Battery = {bot.battery_level:.1f}%, "
                  f"Status = {bot.status}")
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
