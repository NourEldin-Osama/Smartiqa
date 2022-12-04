import pandas as pd
from django.core.management.base import BaseCommand

from Smart.models import *


class Command(BaseCommand):
    def _create_Recommendation_Course(self):
        data = pd.read_excel(r'Recommendation_Course.xlsx')
        for _, row in data.iterrows():
            Recommendation_Course(
                name=row["Name"], organization=row["Organiser"], hours=row["Length (Hours)"],
                user_rating=row["Avg. User Rating"], total_enrollments=row["Total Enrollments"],
                total_ratings=row["Total Ratings"], difficulty=row["Difficulty"], url=row["Public URL"]
            ).save()

    def handle(self, *args, **options):
        self._create_Recommendation_Course()
