class Package:

    def __init__(self, ID, address, city, state, zip_code, deadline, weight, notes, status=''):
        self.leave_time = None
        self.delivery_time = None
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status

    def delivery_time(self):
        self.delivery_time = 0
        
    def leave_time(self):
        self.leave_time = 0

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (
        self.ID, self.address, self.city, self.state, self.zip_code, self.deadline, self.weight, self.notes,
        self.status)
