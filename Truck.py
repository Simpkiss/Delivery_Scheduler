import datetime


class Truck:

    return_time = datetime.timedelta(hours=0)
    mileage = 0

    def __init__(self, packages, depart_time):
        self.packages = packages
        self.depart_time = depart_time

    def mileage(self):
        self.mileage = 0

    def return_time(self):
        self.return_time = 0