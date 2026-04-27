from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.utils.timezone import now
from datetime import timedelta

from .models import KYCSubmission, User
from .serializers import KYCSubmissionSerializer
from .services.state_machine import transition_state


class KYCSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = KYCSubmissionSerializer

    def update(self, request, *args, **kwargs):
        submission = self.get_object()

        if submission.state not in ["draft", "more_info_requested"]:
            return Response(
                {"error": "Cannot edit after submission"},
                status=400
            )

        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        user = User.objects.first()   # TEMP FIX

        if not user:
            return KYCSubmission.objects.none()

        if user.role == "reviewer":
            return KYCSubmission.objects.all()

        return KYCSubmission.objects.filter(merchant=user)

    def perform_create(self, serializer):
        user = User.objects.first()   # TEMP FIX

        if not user:
            raise PermissionError("No test user found")

        serializer.save(merchant=user)

    @action(detail=True, methods=['post'])
    def update_state(self, request, pk=None):
        submission = self.get_object()
        new_state = request.data.get("state")

        user = User.objects.first()   # TEMP FIX

        if user.role == "merchant" and new_state != "submitted":
            return Response(
                {"error": "Merchant can only submit KYC"},
                status=400
            )

        try:
            transition_state(submission, new_state)
            return Response({"message": "State updated"})
        except ValueError as e:
            return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def reviewer_dashboard(request):
    submissions = KYCSubmission.objects.filter(
        state__in=["submitted", "under_review"]
    ).order_by("created_at")

    result = []

    for s in submissions:
        at_risk = (now() - s.created_at) > timedelta(hours=24)

        result.append({
            "id": s.id,
            "state": s.state,
            "merchant_id": s.merchant.id,
            "created_at": s.created_at,
            "at_risk": at_risk
        })

    return Response(result)


from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer