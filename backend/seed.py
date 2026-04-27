from kyc.models import User, KYCSubmission

# create users
m1 = User.objects.create(username="merchant1", role="merchant")
m2 = User.objects.create(username="merchant2", role="merchant")
r1 = User.objects.create(username="reviewer1", role="reviewer")

# create submissions
KYCSubmission.objects.create(merchant=m1, state="draft")
KYCSubmission.objects.create(merchant=m2, state="under_review")

print("✅ Seed data created")