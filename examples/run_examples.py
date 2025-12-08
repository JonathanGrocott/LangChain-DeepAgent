"""
Example Scenarios Runner
"""
import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.scenarios.production_monitoring import run_production_monitoring
from examples.scenarios.predictive_maintenance import run_predictive_maintenance

def main():
    parser = argparse.ArgumentParser(description="Run Deep Agent Example Scenarios")
    parser.add_argument(
        "scenario",
        choices=["production", "maintenance", "all"],
        help="Which scenario to run"
    )
    
    args = parser.parse_args()
    
    if args.scenario in ["production", "all"]:
        run_production_monitoring()
        
    if args.scenario in ["maintenance", "all"]:
        run_predictive_maintenance()

if __name__ == "__main__":
    main()
