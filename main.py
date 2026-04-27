"""
Main Entry Point for Nanobot Simulation

Interactive menu for running different simulation scenarios.
"""
import sys
from examples import basic_simulation, swarm_demo, conversion_demo


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 60)
    print("NANOBOT SIMULATION - MAIN MENU")
    print("=" * 60)
    print("\nAvailable Simulations:")
    print("  1. Basic Simulation     - Single nanobot demo")
    print("  2. Swarm Demo          - Multi-bot swarm control")
    print("  3. Conversion Demo     - SIM card to nanobot conversion")
    print("  4. Run All             - Execute all demonstrations")
    print("  5. Exit")
    print("\n" + "=" * 60)


def main():
    """Main application loop."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║    NANOBOT SIMULATION: SIM CARD TO NANOBOT CONVERSION    ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n🤖 Running Basic Simulation...")
                basic_simulation.main()
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                print("\n🤖 Running Swarm Demo...")
                swarm_demo.main()
                input("\nPress Enter to continue...")
                
            elif choice == "3":
                print("\n🤖 Running Conversion Demo...")
                conversion_demo.main()
                input("\nPress Enter to continue...")
                
            elif choice == "4":
                print("\n🤖 Running All Demonstrations...")
                print("\n" + "-" * 60)
                print("PART 1: BASIC SIMULATION")
                print("-" * 60)
                basic_simulation.main()
                input("\nPress Enter to continue to Part 2...")
                
                print("\n" + "-" * 60)
                print("PART 2: CONVERSION DEMO")
                print("-" * 60)
                conversion_demo.main()
                input("\nPress Enter to continue to Part 3...")
                
                print("\n" + "-" * 60)
                print("PART 3: SWARM DEMO")
                print("-" * 60)
                swarm_demo.main()
                
                print("\n✓ All demonstrations complete!")
                input("\nPress Enter to continue...")
                
            elif choice == "5":
                print("\n👋 Exiting simulation. Goodbye!")
                sys.exit(0)
                
            else:
                print("\n❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Simulation interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
