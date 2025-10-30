import threading
from typing import Dict, Any, List
from datetime import datetime


class CostTracker:
    """
    Centralized cost tracking for all API calls in a workflow.
    Thread-safe implementation for concurrent operations.
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._costs: Dict[str, List[Dict[str, Any]]] = {}
    
    def track_cost(
        self,
        workflow_id: str,
        service: str,
        cost: float,
        details: str = ""
    ):
        """
        Records a cost entry for a specific workflow.
        
        Args:
            workflow_id: Unique identifier for the workflow (e.g., job_id, opportunity_id)
            service: Name of the service (e.g., "DataForSEO SERP", "OpenAI Generation")
            cost: Cost in USD
            details: Additional context about the API call
        """
        with self._lock:
            if workflow_id not in self._costs:
                self._costs[workflow_id] = []
            
            self._costs[workflow_id].append({
                "timestamp": datetime.now().isoformat(),
                "service": service,
                "cost": round(cost, 6),
                "details": details
            })
    
    def get_workflow_cost(self, workflow_id: str) -> float:
        """Returns total cost for a specific workflow."""
        with self._lock:
            if workflow_id not in self._costs:
                return 0.0
            return sum(entry["cost"] for entry in self._costs[workflow_id])
    
    def get_workflow_breakdown(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Returns detailed cost breakdown for a workflow."""
        with self._lock:
            return self._costs.get(workflow_id, []).copy()
    
    def clear_workflow(self, workflow_id: str):
        """Clears cost data for a completed workflow."""
        with self._lock:
            if workflow_id in self._costs:
                del self._costs[workflow_id]
