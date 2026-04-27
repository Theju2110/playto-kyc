from rest_framework import serializers
from .models import KYCSubmission, Document, Notification


# 🔐 Document Serializer (FILE VALIDATION)
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def validate_file(self, file):
        # ✅ Size validation (max 5MB)
        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File too large (max 5MB)")

        # ✅ Type validation
        allowed_types = [
            "application/pdf",
            "image/jpeg",
            "image/png"
        ]

        if file.content_type not in allowed_types:
            raise serializers.ValidationError("Invalid file type. Only PDF/JPG/PNG allowed")

        return file


# 📄 KYC Submission Serializer
class KYCSubmissionSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = KYCSubmission
        fields = '__all__'
        read_only_fields = ['merchant', 'state', 'created_at']

    def validate(self, data):
        # Optional: basic validation example
        personal = data.get("personal_details")
        business = data.get("business_details")

        if not personal:
            raise serializers.ValidationError("Personal details required")

        if not business:
            raise serializers.ValidationError("Business details required")

        return data


# 🔔 Notification Serializer (for debugging / optional API)
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'