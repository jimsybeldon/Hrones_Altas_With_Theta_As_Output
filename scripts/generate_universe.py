# generate_universe.py
from fourbar_synthesis.universe_engine import UniverseEngine

if __name__ == "__main__":
    engine = UniverseEngine()

    # Run all seeds (default pp_mode = 3)
    engine.run_all(pp_mode=3)

    # Export CAD packets for global top‑10
    engine.export_top10()

    # Export CAD packet for best candidate
    engine.export_best()

    # Print precision‑point overlay summary
    engine.print_best_overlay()

    # Plot + animate best candidate
    engine.visualize_best()

    print("\nUniverse generation complete.")
