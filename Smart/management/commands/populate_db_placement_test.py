import os

import pandas as pd
from django.core.management.base import BaseCommand

from Smart.models import *


class Command(BaseCommand):

    def _create_Placement_test(self):
        base_path = r'C:\Users\NourEldin\Desktop\edited'
        files = os.listdir(base_path)
        for file in files:
            data = pd.read_excel(os.path.join(base_path, file))
            test_name = file.split(".")[0]
            test = Test(name=test_name, field=test_name)
            test.save()
            for _, row in data.iterrows():
                Question(test=test, q=row["q"], right_ans=row["right_ans"], wrong_ans1=row["wrong_ans1"],
                         wrong_ans2=row["wrong_ans2"], wrong_ans3=row["wrong_ans3"], ).save()

    def handle(self, *args, **options):
        self._create_Placement_test()
