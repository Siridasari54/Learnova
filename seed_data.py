"""
Learnova Seed Data Script
Run AFTER migrate to populate initial topics and sample rooms:
  python seed_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from rooms.models import Topic, Room, RoomMembership, Message

TOPICS = [
    "Python",
    "Java",
    "JavaScript",
    "Data Structures & Algorithms",
    "Web Development",
    "Machine Learning",
    "Artificial Intelligence",
    "Computer Networks",
    "Database Management",
    "Operating Systems",
    "Cybersecurity",
    "Mobile Development",
    "Cloud Computing",
    "DevOps",
    "Mathematics",
    "Physics",
    "React",
    "Django",
    "System Design",
    "Interview Preparation",
]

print("🌱 Seeding topics...")
for name in TOPICS:
    topic, created = Topic.objects.get_or_create(name=name)
    if created:
        print(f"  ✅ Created topic: {name}")
    else:
        print(f"  ⏭️  Topic exists: {name}")

print(f"\n✨ Done! {Topic.objects.count()} topics in database.")
print("\n💡 Tip: Register an account at http://127.0.0.1:8000/accounts/register/ to create study rooms.")
