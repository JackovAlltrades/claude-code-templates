#!/usr/bin/env python3
"""
Enhanced notification handler for dependency conflict resolutions
Supports multiple notification channels
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import requests
import logging

class NotificationHandler:
    def __init__(self, config_path: str = "dependency-conflicts.json"):
        with open(config_path) as f:
            self.config = json.load(f)
        self.notification_config = self.config.get("notification", {})
        
    def send_notification(self, resolved_conflicts: List[Dict], test_results: Dict):
        """Send notifications through all configured channels"""
        if not self.notification_config.get("enabled"):
            return
            
        message = self.format_message(resolved_conflicts, test_results)
        
        methods = self.notification_config.get("methods", ["file"])
        if isinstance(self.notification_config.get("method"), str):
            methods = [self.notification_config["method"]]
            
        for method in methods:
            try:
                if method == "file":
                    self.notify_file(message)
                elif method == "console":
                    self.notify_console(message)
                elif method == "webhook":
                    self.notify_webhook(message)
                elif method == "email":
                    self.notify_email(message)
                elif method == "github":
                    self.notify_github(resolved_conflicts)
            except Exception as e:
                logging.error(f"Failed to send {method} notification: {e}")
    
    def format_message(self, resolved_conflicts: List[Dict], test_results: Dict) -> Dict:
        """Format notification message"""
        conflicts_summary = "\n".join([
            f"• {c['name']}: {c['current_version']} → {c['desired_version']}"
            for c in resolved_conflicts
        ])
        
        return {
            "title": f"🎉 {len(resolved_conflicts)} Dependency Conflicts Resolved!",
            "summary": conflicts_summary,
            "details": {
                "resolved_count": len(resolved_conflicts),
                "timestamp": datetime.now().isoformat(),
                "test_results": test_results,
                "conflicts": resolved_conflicts
            },
            "actions": [
                "Review the generated update scripts",
                "Test in a staging environment",
                "Update requirements.txt",
                "Deploy to production"
            ]
        }
    
    def notify_file(self, message: Dict):
        """Write to notification log file"""
        file_config = self.notification_config.get("file_config", {})
        log_path = Path(file_config.get("path", "dependency-resolutions.log"))
        
        # Check if we need to rotate
        if log_path.exists():
            size_mb = log_path.stat().st_size / (1024 * 1024)
            max_size = file_config.get("rotate_size_mb", 10)
            if size_mb > max_size:
                # Rotate the log
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                log_path.rename(f"{log_path}.{timestamp}")
        
        with open(log_path, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{datetime.now().isoformat()}] {message['title']}\n")
            f.write(f"Summary:\n{message['summary']}\n")
            f.write(f"Actions Required:\n")
            for action in message['actions']:
                f.write(f"  - {action}\n")
            f.write(f"{'='*60}\n")
    
    def notify_console(self, message: Dict):
        """Print to console with formatting"""
        print(f"\n{'🎉'*20}")
        print(f"\n{message['title']}")
        print(f"\nResolved Conflicts:")
        print(message['summary'])
        print(f"\nNext Steps:")
        for i, action in enumerate(message['actions'], 1):
            print(f"  {i}. {action}")
        print(f"\n{'🎉'*20}\n")
    
    def notify_webhook(self, message: Dict):
        """Send webhook notifications"""
        webhook_config = self.notification_config.get("webhook_config", {})
        
        # Slack webhook
        if slack_url := webhook_config.get("slack_webhook_url"):
            slack_message = {
                "text": message['title'],
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{message['title']}*\n\n{message['summary']}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Next Steps:*\n" + "\n".join(
                                f"{i}. {action}" 
                                for i, action in enumerate(message['actions'], 1)
                            )
                        }
                    }
                ]
            }
            requests.post(slack_url, json=slack_message)
        
        # Discord webhook
        if discord_url := webhook_config.get("discord_webhook_url"):
            discord_message = {
                "content": message['title'],
                "embeds": [{
                    "title": "Resolved Conflicts",
                    "description": message['summary'],
                    "color": 5763719,  # Green
                    "fields": [
                        {
                            "name": "Next Steps",
                            "value": "\n".join(f"• {action}" for action in message['actions'])
                        }
                    ],
                    "timestamp": datetime.now().isoformat()
                }]
            }
            requests.post(discord_url, json=discord_message)
        
        # Custom webhook
        if custom_url := webhook_config.get("custom_webhook_url"):
            requests.post(custom_url, json=message)
    
    def notify_github(self, resolved_conflicts: List[Dict]):
        """Create GitHub issue/PR for resolved conflicts"""
        github_config = self.notification_config.get("github_config", {})
        
        if not github_config.get("create_issue"):
            return
            
        # This would integrate with GitHub Actions
        # The actual implementation is in the GitHub workflow
        issue_body = f"""
## Dependency Conflicts Resolved! 🎉

The automated dependency conflict monitor has detected that the following conflicts have been resolved:

### Resolved Conflicts:
{chr(10).join(f'- **{c["name"]}**: {c["current_version"]} → {c["desired_version"]}' for c in resolved_conflicts)}

### Next Steps:
1. Review the generated update scripts
2. Test in a staging environment  
3. Update requirements.txt
4. Create a PR with the updates

### Automated Actions:
- [ ] Update scripts have been generated
- [ ] Basic tests have passed
- [ ] Ready for manual review

---
*This issue was automatically created by the Dependency Conflict Monitor*
"""
        
        # Write to file for GitHub Actions to pick up
        Path(".github/dependency-resolution-issue.md").write_text(issue_body)


if __name__ == "__main__":
    # Example usage
    handler = NotificationHandler()
    
    # Test notification
    test_conflicts = [{
        "name": "example-package",
        "current_version": "1.0.0",
        "desired_version": "2.0.0"
    }]
    
    test_results = {
        "all_passed": True,
        "test_count": 5,
        "duration_seconds": 12.5
    }
    
    handler.send_notification(test_conflicts, test_results)