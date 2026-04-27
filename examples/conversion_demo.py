"""
SIM Card Conversion Example

Demonstrates the conversion process from SIM card to nanobot.
"""
import numpy as np
from src.sim_card import SIMCard, SIMToNanobotConverter
from src.nanobot import Nanobot


def main():
    print("=" * 60)
    print("SIM CARD TO NANOBOT CONVERSION")
    print("=" * 60)
    
    # Create a SIM card
    print("\n1. Creating SIM card...")
    sim = SIMCard(
        iccid="89014103211234567890",
        imsi="310150123456789",
        network_provider="NanoNet"
    )
    
    # Display SIM info
    print("\n2. SIM Card Information:")
    sim_info = sim.get_sim_info()
    for key, value in sim_info.items():
        print(f"   {key}: {value}")
    
    # Add some contacts and messages
    print("\n3. Adding contacts and messages...")
    sim.add_contact("Base Station", "+1-555-0100")
    sim.add_contact("Medical Monitor", "+1-555-0101")
    sim.add_contact("Emergency", "+1-555-0911")
    
    sim.store_message("Base Station", "Initialization sequence ready")
    sim.store_message("Medical Monitor", "Awaiting deployment")
    
    print(f"   Added {len(sim.contacts)} contacts")
    print(f"   Stored {len(sim.stored_messages)} messages")
    
    # Configure for nanobot conversion
    print("\n4. Configuring nanobot parameters...")
    nanobot_config = {
        "size_scale": 1e-9,
        "sensor_suite": ["proximity", "chemical", "temperature", "pressure"],
        "actuator_types": ["movement", "manipulation", "delivery"],
        "communication_protocol": "RF-nano",
        "power_source": "biochemical",
        "operating_mode": "semi-autonomous"
    }
    
    sim.configure_nanobot(nanobot_config)
    print(f"   Configuration complete")
    print(f"   Status: {sim.conversion_status}")
    
    # Create converter
    print("\n5. Initializing converter...")
    converter = SIMToNanobotConverter()
    
    # Perform conversion
    print("\n6. Initiating conversion process...")
    result = converter.convert(sim)
    
    if result:
        print("   ✓ Conversion successful!")
        print("\n   Conversion steps:")
        for i, step in enumerate(result.get("conversion_steps", []), 1):
            print(f"      {i}. {step}")
        
        print("\n   Nanobot parameters:")
        params = result.get("nanobot_parameters", {})
        for key, value in params.items():
            if key not in ["authentication_key"]:  # Hide sensitive data
                print(f"      {key}: {value}")
    else:
        print("   ✗ Conversion failed")
    
    # Create nanobot from converted parameters
    if result:
        print("\n7. Instantiating nanobot...")
        nanobot_params = result["nanobot_parameters"]
        bot = Nanobot(
            bot_id=nanobot_params["bot_id"],
            initial_position=nanobot_params["initial_position"]
        )
        
        print(f"   Created: {bot.bot_id}")
        print(f"   Position: {bot.position}")
        print(f"   Battery: {bot.battery_level}%")
        
        # Test nanobot functionality
        print("\n8. Testing nanobot functionality...")
        
        # Movement test
        print("   Testing movement...")
        bot.move(np.array([1, 0, 0]), speed=2.0)
        print(f"      New position: {bot.position.round(2)}")
        
        # Sensor test
        print("   Testing sensors...")
        sensors = bot.sense_environment()
        print(f"      Temperature: {sensors['temperature']:.2f} K")
        print(f"      Pressure: {sensors['pressure']:.2f} kPa")
        
        # Communication test
        print("   Testing communication...")
        success = bot.transmit_message(
            "Nanobot online. All systems operational.",
            "base_station"
        )
        print(f"      Message sent: {success}")
        
        # Display final status
        print("\n9. Final nanobot status:")
        status = bot.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")
    
    # Display conversion history
    print("\n10. Conversion history:")
    history = converter.get_conversion_history()
    for entry in history:
        print(f"   SIM: {entry.get('sim_iccid', 'N/A')} → "
              f"Bot: {entry.get('bot_id', 'N/A')} "
              f"[{entry.get('status', 'unknown')}]")
    
    # Try converting another SIM card
    print("\n11. Converting additional SIM card...")
    sim2 = SIMCard(
        iccid="89014103219876543210",
        imsi="310150987654321",
        network_provider="NanoNet"
    )
    sim2.configure_nanobot({"operating_mode": "autonomous"})
    result2 = converter.convert(sim2)
    
    if result2:
        print(f"   ✓ Second conversion successful!")
        print(f"   Bot ID: {result2['nanobot_parameters']['bot_id']}")
    
    # Final converter summary
    print("\n12. Converter summary:")
    print(f"   Total conversions: {len(converter.conversion_log)}")
    print(f"   Active nanobots: {len(converter.converted_bots)}")
    print(f"   Bot IDs: {', '.join(converter.converted_bots)}")
    
    print("\n" + "=" * 60)
    print("CONVERSION DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
