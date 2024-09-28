from datetime import datetime, timedelta
from typing import Optional

def calc_due_date(priority: str) -> Optional[datetime]:
    # Implementing simple logic to add X days based on priority but could be any logic
    # Can implement logic to determing due date based on recurrence etc.
    if priority == 'HIGH':
        return (datetime.now() + timedelta(days=1)).isoformat()  
    elif priority == 'MEDIUM':
        return (datetime.now() + timedelta(days=3)).isoformat()  
    elif priority == 'LOW':
        return (datetime.now() + timedelta(days=7)).isoformat()  
    else:
        return None  # Return None if priority is not recognized