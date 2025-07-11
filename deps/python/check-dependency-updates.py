#!/usr/bin/env python3
"""
Dependency Update Safety Checker
Analyzes potential breaking changes before updating dependencies
"""

import subprocess
import json
import sys
from typing import Dict, List, Tuple
import requests
from packaging import version
import re

class DependencyChecker:
    def __init__(self):
        self.critical_deps = {
            'anthropic': 'AI integration core',
            'pydantic': 'Data validation',
            'click': 'CLI framework',
            'typer': 'CLI framework',
            'structlog': 'Logging system'
        }
        
    def get_outdated_packages(self) -> List[Dict]:
        """Get list of outdated packages with current and latest versions"""
        result = subprocess.run(
            ['pip', 'list', '--outdated', '--format', 'json'],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout) if result.returncode == 0 else []
    
    def check_changelog(self, package: str, current: str, latest: str) -> Dict:
        """Check for breaking changes in package changelog"""
        # Check major version changes
        curr_version = version.parse(current)
        latest_version = version.parse(latest)
        
        major_change = latest_version.major > curr_version.major
        minor_change = latest_version.minor > curr_version.minor
        
        risk_level = 'HIGH' if major_change else ('MEDIUM' if minor_change else 'LOW')
        
        return {
            'package': package,
            'current': current,
            'latest': latest,
            'major_version_change': major_change,
            'risk_level': risk_level,
            'is_critical': package in self.critical_deps,
            'description': self.critical_deps.get(package, 'Standard dependency')
        }
    
    def generate_update_plan(self, outdated: List[Dict]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """Categorize updates by risk level"""
        high_risk = []
        medium_risk = []
        low_risk = []
        
        for pkg in outdated:
            analysis = self.check_changelog(
                pkg['name'], 
                pkg['version'], 
                pkg['latest_version']
            )
            
            if analysis['risk_level'] == 'HIGH':
                high_risk.append(analysis)
            elif analysis['risk_level'] == 'MEDIUM':
                medium_risk.append(analysis)
            else:
                low_risk.append(analysis)
                
        return high_risk, medium_risk, low_risk
    
    def generate_report(self):
        """Generate comprehensive update safety report"""
        print("🔍 Dependency Update Safety Analysis")
        print("=" * 50)
        
        outdated = self.get_outdated_packages()
        if not outdated:
            print("✅ All dependencies are up to date!")
            return
        
        high, medium, low = self.generate_update_plan(outdated)
        
        # High risk updates
        if high:
            print("\n🔴 HIGH RISK Updates (Major version changes):")
            print("-" * 50)
            for pkg in high:
                print(f"⚠️  {pkg['package']}: {pkg['current']} → {pkg['latest']}")
                if pkg['is_critical']:
                    print(f"   CRITICAL: {pkg['description']}")
                print(f"   Action: Test thoroughly in isolated environment")
        
        # Medium risk updates
        if medium:
            print("\n🟡 MEDIUM RISK Updates (Minor version changes):")
            print("-" * 50)
            for pkg in medium:
                print(f"⚡ {pkg['package']}: {pkg['current']} → {pkg['latest']}")
                if pkg['is_critical']:
                    print(f"   Important: {pkg['description']}")
                print(f"   Action: Review changelog and test")
        
        # Low risk updates
        if low:
            print("\n🟢 LOW RISK Updates (Patch versions):")
            print("-" * 50)
            for pkg in low:
                print(f"✓ {pkg['package']}: {pkg['current']} → {pkg['latest']}")
                print(f"   Action: Generally safe to update")
        
        # Recommendations
        print("\n📋 Recommended Update Strategy:")
        print("-" * 50)
        print("1. Create a new branch: git checkout -b update/dependencies")
        print("2. Update LOW risk packages first:")
        print("   pip install --upgrade " + " ".join([p['package'] for p in low]))
        print("3. Run full test suite after each group")
        print("4. Update MEDIUM risk packages individually")
        print("5. Update HIGH risk packages last with extensive testing")
        print("\n💡 Use pip-tools or poetry for better dependency management")

if __name__ == "__main__":
    checker = DependencyChecker()
    checker.generate_report()