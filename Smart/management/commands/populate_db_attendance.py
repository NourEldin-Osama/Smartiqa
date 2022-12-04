import pandas as pd
from django.core.management.base import BaseCommand

from Smart.models import *


class Command(BaseCommand):
    def _create_Attendance(self):
        data = pd.read_excel(r"C:\Users\NourEldin\Desktop\Test\result.xlsx")
        for _, row in data.iterrows():
            Attendance(name=row["name"], date=row["date"], state=row["state"],
                       instructor=Instructor.objects.get(user_id=str(row["instructor"])),
                       course=Course.objects.get(code=str(row["course"]))).save()

    def handle(self, *args, **options):
        self._create_Attendance()
