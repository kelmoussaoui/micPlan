# app/backend/logging/logger.py
# Activity logging system

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class ActivityLogger:
    """Logs user activities and system events"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create log file path
        self.log_file = self.log_dir / "activity_log.jsonl"
        
        # Ensure log file exists
        if not self.log_file.exists():
            self.log_file.touch()
    
    def log_activity(self, action: str, category: str, details: str, 
                    user_id: str, tool_name: str, status: str = "info",
                    metadata: Optional[Dict[str, Any]] = None):
        """Log an activity"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "category": category,
                "details": details,
                "user_id": user_id,
                "tool_name": tool_name,
                "status": status,
                "metadata": metadata or {}
            }
            
            # Write to log file
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            
            # Also print to console for development
            print(f"[{log_entry['timestamp']}] {action} - {user_id} - {status}")
            
        except Exception as e:
            print(f"Error logging activity: {e}")
    
    def get_activities(self, user_id: Optional[str] = None, 
                      category: Optional[str] = None,
                      limit: int = 100) -> list:
        """Retrieve logged activities with optional filtering"""
        try:
            activities = []
            
            if not self.log_file.exists():
                return activities
            
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            activity = json.loads(line.strip())
                            
                            # Apply filters
                            if user_id and activity.get("user_id") != user_id:
                                continue
                            if category and activity.get("category") != category:
                                continue
                            
                            activities.append(activity)
                            
                            # Apply limit
                            if len(activities) >= limit:
                                break
                                
                        except json.JSONDecodeError:
                            continue
            
            # Sort by timestamp (newest first)
            activities.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            return activities
            
        except Exception as e:
            print(f"Error retrieving activities: {e}")
            return []
    
    def get_user_activities(self, user_id: str, limit: int = 50) -> list:
        """Get activities for a specific user"""
        return self.get_activities(user_id=user_id, limit=limit)
    
    def get_category_activities(self, category: str, limit: int = 50) -> list:
        """Get activities for a specific category"""
        return self.get_activities(category=category, limit=limit)
    
    def clear_logs(self, days_to_keep: int = 30):
        """Clear old log entries"""
        try:
            if not self.log_file.exists():
                return
            
            cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            temp_file = self.log_file.with_suffix(".tmp")
            
            with open(self.log_file, "r", encoding="utf-8") as infile, \
                 open(temp_file, "w", encoding="utf-8") as outfile:
                
                for line in infile:
                    if line.strip():
                        try:
                            activity = json.loads(line.strip())
                            timestamp = datetime.fromisoformat(activity.get("timestamp", "1970-01-01"))
                            
                            if timestamp.timestamp() > cutoff_date:
                                outfile.write(line)
                                
                        except (json.JSONDecodeError, ValueError):
                            continue
            
            # Replace original file with filtered version
            temp_file.replace(self.log_file)
            
        except Exception as e:
            print(f"Error clearing logs: {e}")
    
    def export_logs(self, output_file: str, format: str = "json"):
        """Export logs to a file"""
        try:
            activities = self.get_activities(limit=10000)  # Get all activities
            
            if format.lower() == "json":
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(activities, f, indent=2, ensure_ascii=False)
            
            elif format.lower() == "csv":
                import csv
                with open(output_file, "w", newline="", encoding="utf-8") as f:
                    if activities:
                        writer = csv.DictWriter(f, fieldnames=activities[0].keys())
                        writer.writeheader()
                        writer.writerows(activities)
            
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return True
            
        except Exception as e:
            print(f"Error exporting logs: {e}")
            return False
