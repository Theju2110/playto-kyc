ALLOWED_TRANSITIONS = {
    "draft": ["submitted"],
    "submitted": ["under_review"],
    "under_review": ["approved", "rejected", "more_info_requested"],
    "more_info_requested": ["submitted"],
}

def transition_state(submission, new_state):
    current = submission.state

    if new_state not in ALLOWED_TRANSITIONS.get(current, []):
        raise ValueError(f"Invalid transition from {current} to {new_state}")

    submission.state = new_state
    submission.save()
    create_notification(submission, new_state)

from ..models import Notification

def create_notification(submission, new_state):
    Notification.objects.create(
        merchant=submission.merchant,
        event_type=new_state,
        payload=f"Submission {submission.id} moved to {new_state}"
    )

from ..models import Notification

def create_notification(submission, new_state):
    Notification.objects.create(
        merchant=submission.merchant,
        event_type=new_state,
        payload=f"Submission {submission.id} moved to {new_state}"
    )