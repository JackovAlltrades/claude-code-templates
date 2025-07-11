#!/usr/bin/env python3
"""
Dependency Conflict Monitor
Automatically tracks and resolves dependency conflicts when upstream packages update
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import requests
import logging
from packaging import version
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dependency-monitor.log'),
        logging.StreamHandler()
    ]
)

class DependencyConflictMonitor:
    def __init__(self, config_path: str = "dependency-conflicts.json"):
        self.config_path = config_path
        self.conflicts = self.load_conflicts()
        self.resolved = []
        self.still_blocked = []
        
    def load_conflicts(self) -> Dict:
        """Load known dependency conflicts from config file"""
        config_file = Path(self.config_path)
        if not config_file.exists():
            # Create default config
            default_config = {
                "conflicts": [
                    {
                        "name": "protobuf",
                        "current_version": "4.25.8",
                        "blocked_by": [
                            {"package": "unsloth", "requires": "<4.0.0"},
                            {"package": "unsloth-zoo", "requires": "<4.0.0"}
                        ],
                        "desired_version": ">=5.0.0",
                        "priority": "high",
                        "security_issue": False
                    }
                ],
                "notification": {
                    "enabled": True,
                    "method": "file",  # or "email", "slack", "webhook"
                    "email_config": {
                        "smtp_server": "smtp.gmail.com",
                        "smtp_port": 587,
                        "from_email": "your-email@example.com",
                        "to_emails": ["admin@example.com"],
                        "password_env_var": "EMAIL_PASSWORD"
                    }
                }
            }
            config_file.write_text(json.dumps(default_config, indent=2))
            return default_config
        
        return json.loads(config_file.read_text())
    
    def check_pypi_version(self, package: str) -> Optional[str]:
        """Check the latest version of a package on PyPI"""
        try:
            response = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data["info"]["version"]
        except Exception as e:
            logging.error(f"Error checking PyPI for {package}: {e}")
        return None
    
    def check_if_conflict_resolved(self, conflict: Dict) -> bool:
        """Check if blocking packages have updated to support newer versions"""
        for blocker in conflict["blocked_by"]:
            package_name = blocker["package"]
            required_spec = blocker["requires"]
            
            # Check latest version on PyPI
            latest_version = self.check_pypi_version(package_name)
            if not latest_version:
                logging.warning(f"Could not check {package_name} on PyPI")
                continue
                
            # Check if latest version has updated requirements
            try:
                # Try to get requirements from PyPI
                response = requests.get(
                    f"https://pypi.org/pypi/{package_name}/{latest_version}/json",
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    requires_dist = data.get("info", {}).get("requires_dist", [])
                    
                    # Check if protobuf requirement has changed
                    protobuf_req_changed = True
                    for req in requires_dist or []:
                        if conflict["name"] in req:
                            if required_spec in req:
                                protobuf_req_changed = False
                                break
                    
                    if protobuf_req_changed:
                        logging.info(
                            f"🎉 {package_name} {latest_version} may now support "
                            f"{conflict['name']} {conflict['desired_version']}"
                        )
                        return True
                        
            except Exception as e:
                logging.error(f"Error checking requirements for {package_name}: {e}")
                
        return False
    
    def test_update_in_venv(self, conflict: Dict) -> Tuple[bool, str]:
        """Test if the update works in an isolated environment"""
        import tempfile
        import shutil
        
        with tempfile.TemporaryDirectory() as tmpdir:
            logging.info(f"Testing update in temporary environment: {tmpdir}")
            
            try:
                # Create virtual environment
                subprocess.run(
                    [sys.executable, "-m", "venv", f"{tmpdir}/test_env"],
                    check=True,
                    capture_output=True
                )
                
                # Activate and install current requirements
                if sys.platform == "win32":
                    pip_path = f"{tmpdir}/test_env/Scripts/pip"
                    python_path = f"{tmpdir}/test_env/Scripts/python"
                else:
                    pip_path = f"{tmpdir}/test_env/bin/pip"
                    python_path = f"{tmpdir}/test_env/bin/python"
                
                # Install requirements
                subprocess.run(
                    [pip_path, "install", "-r", "requirements.txt"],
                    check=True,
                    capture_output=True
                )
                
                # Try to update the conflicted package
                result = subprocess.run(
                    [pip_path, "install", "--upgrade", f"{conflict['name']}{conflict['desired_version']}"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    # Run basic tests
                    test_result = subprocess.run(
                        [python_path, "verify-core-functionality.py"],
                        capture_output=True,
                        text=True
                    )
                    
                    if test_result.returncode == 0:
                        return True, "All tests passed!"
                    else:
                        return False, f"Tests failed: {test_result.stderr}"
                else:
                    return False, f"Update failed: {result.stderr}"
                    
            except Exception as e:
                return False, f"Error during testing: {str(e)}"
    
    def notify_resolution(self, conflict: Dict, message: str):
        """Send notification about resolved conflict"""
        notification_config = self.conflicts.get("notification", {})
        
        if not notification_config.get("enabled"):
            return
            
        method = notification_config.get("method", "file")
        
        if method == "file":
            # Write to notification file
            with open("dependency-resolutions.log", "a") as f:
                f.write(f"\n[{datetime.now().isoformat()}] RESOLVED: {conflict['name']}\n")
                f.write(f"Message: {message}\n")
                f.write("-" * 50 + "\n")
                
        elif method == "email":
            # Send email notification
            email_config = notification_config.get("email_config", {})
            self.send_email_notification(conflict, message, email_config)
            
        elif method == "webhook":
            # Send to webhook (e.g., Slack, Discord)
            webhook_url = notification_config.get("webhook_url")
            if webhook_url:
                requests.post(webhook_url, json={
                    "text": f"Dependency Conflict Resolved: {conflict['name']}",
                    "details": message
                })
    
    def send_email_notification(self, conflict: Dict, message: str, email_config: Dict):
        """Send email notification about resolved conflict"""
        import os
        
        password = os.environ.get(email_config.get("password_env_var", "EMAIL_PASSWORD"))
        if not password:
            logging.warning("Email password not found in environment variables")
            return
            
        msg = MIMEMultipart()
        msg['From'] = email_config['from_email']
        msg['To'] = ', '.join(email_config['to_emails'])
        msg['Subject'] = f"Dependency Conflict Resolved: {conflict['name']}"
        
        body = f"""
        Good news! A dependency conflict has been resolved.
        
        Package: {conflict['name']}
        Previous Version: {conflict['current_version']}
        Desired Version: {conflict['desired_version']}
        
        Details:
        {message}
        
        You can now update this dependency safely.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['from_email'], password)
            server.send_message(msg)
            server.quit()
            logging.info("Email notification sent successfully")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
    
    def run_check(self):
        """Run the main conflict checking process"""
        logging.info("Starting dependency conflict check...")
        
        for conflict in self.conflicts.get("conflicts", []):
            logging.info(f"Checking {conflict['name']}...")
            
            if self.check_if_conflict_resolved(conflict):
                # Test the update
                success, message = self.test_update_in_venv(conflict)
                
                if success:
                    self.resolved.append(conflict)
                    logging.info(f"✅ {conflict['name']} conflict resolved!")
                    self.notify_resolution(conflict, message)
                    
                    # Create update script
                    self.create_update_script(conflict)
                else:
                    logging.warning(f"Conflict seems resolved but testing failed: {message}")
                    self.still_blocked.append(conflict)
            else:
                self.still_blocked.append(conflict)
                logging.info(f"❌ {conflict['name']} still blocked")
        
        # Generate report
        self.generate_report()
    
    def create_update_script(self, conflict: Dict):
        """Create a script to safely update the resolved dependency"""
        script_content = f"""#!/bin/bash
# Auto-generated script to update {conflict['name']}
# Generated on {datetime.now().isoformat()}

set -e

echo "Updating {conflict['name']} to {conflict['desired_version']}..."

# Backup current state
pip freeze > requirements-backup-$(date +%Y%m%d-%H%M%S).txt

# Update the package
pip install --upgrade "{conflict['name']}{conflict['desired_version']}"

# Run tests
python verify-core-functionality.py

if [ $? -eq 0 ]; then
    echo "✅ Update successful and tests passed!"
    echo "Don't forget to update requirements.txt"
else
    echo "❌ Tests failed, consider rolling back with:"
    echo "pip install -r requirements-backup-*.txt"
fi
"""
        
        script_path = f"update-{conflict['name']}-{datetime.now().strftime('%Y%m%d')}.sh"
        Path(script_path).write_text(script_content)
        Path(script_path).chmod(0o755)
        logging.info(f"Created update script: {script_path}")
    
    def generate_report(self):
        """Generate a summary report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "resolved": [c["name"] for c in self.resolved],
            "still_blocked": [c["name"] for c in self.still_blocked],
            "total_conflicts": len(self.conflicts.get("conflicts", [])),
            "resolved_count": len(self.resolved)
        }
        
        report_path = f"conflict-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        Path(report_path).write_text(json.dumps(report, indent=2))
        
        logging.info(f"\n📊 Summary Report:")
        logging.info(f"Total conflicts tracked: {report['total_conflicts']}")
        logging.info(f"Resolved: {report['resolved_count']}")
        logging.info(f"Still blocked: {len(self.still_blocked)}")
        logging.info(f"Full report saved to: {report_path}")


if __name__ == "__main__":
    monitor = DependencyConflictMonitor()
    monitor.run_check()