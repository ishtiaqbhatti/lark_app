from enum import Enum


class OpportunityStatus(str, Enum):
    """Valid opportunity status values."""
    PENDING = "pending"
    RUNNING = "running"
    IN_PROGRESS = "in_progress"
    VALIDATED = "validated"
    ANALYZED = "analyzed"
    PAUSED_FOR_APPROVAL = "paused_for_approval"
    GENERATED = "generated"
    PUBLISHED = "published"
    FAILED = "failed"
    REJECTED = "rejected"
    REJECTED_BY_USER = "rejected_by_user"
    REFRESH_STARTED = "refresh_started"


class SearchIntent(str, Enum):
    """Valid search intent values per DataForSEO API."""
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    COMMERCIAL = "commercial"
    TRANSACTIONAL = "transactional"


class CompetitionLevel(str, Enum):
    """Valid competition level values per DataForSEO API."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class JobStatus(str, Enum):
    """Valid job status values."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class SocialMediaStatus(str, Enum):
    """Valid social media post status values."""
    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
