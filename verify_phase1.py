"""Test script to verify Phase 1 foundation setup"""

import sys
from pathlib import Path

def test_phase1_foundation():
    """Verify all Phase 1 files and structure are in place"""
    
    print("=" * 60)
    print("Phase 1 Foundation Verification")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    checks = []
    
    # Check project files
    project_files = [
        "pyproject.toml",
        "requirements.txt",
        ".gitignore",
        ".env.example",
        "Dockerfile",
        "docker-compose.yml",
        "README.md",
    ]
    
    # Check source structure
    source_files = [
        "src/__init__.py",
        "src/main.py",
        "src/config/__init__.py",
        "src/config/settings.py",
        "src/config/subagent_configs.py",
        "src/utils/__init__.py",
        "src/utils/logging_config.py",
        "src/utils/langsmith_setup.py",
        "src/agents/__init__.py",
        "src/mcp/__init__.py",
        "src/rag/__init__.py",
    ]
    
    all_files = project_files + source_files
    
    # Verify files exist
    for file_path in all_files:
        full_path = project_root / file_path
        exists = full_path.exists()
        checks.append((file_path, exists))
        status = "✓" if exists else "✗"
        print(f"{status} {file_path}")
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for _, exists in checks if exists)
    total = len(checks)
    success_rate = (passed / total) * 100
    
    print(f"Results: {passed}/{total} files present ({success_rate:.0f}%)")
    
    if passed == total:
        print("✓ Phase 1 Foundation: COMPLETE")
        print("\nNext Steps:")
        print("1. Copy .env.example to .env and add your API keys")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Begin Phase 2: MCP Server Infrastructure")
    else:
        print("✗ Phase 1 Foundation: INCOMPLETE")
        missing = [name for name, exists in checks if not exists]
        print(f"\nMissing files: {', '.join(missing)}")
        return False
    
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_phase1_foundation()
    sys.exit(0 if success else 1)
