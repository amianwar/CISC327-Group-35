class TempID:
    def __init__(self, id, renter_id, id_type, id_number, rental_date, return_date, returned=False):
        self.id = id
        self.renter_id = renter_id
        self.id_type = id_type
        self.id_number = id_number
        self.rental_date = rental_date
        self.return_date = return_date
        self.returned = returned # True when equipment has been returned; flags for removal

    def to_dict(self):
        return {
            "id": self.id,
            "renter_id": self.renter_id,
            "id_type": self.id_type,
            "id_number": self.id_number,
            "rental_date": self.rental_date,
            "return_date": self.return_date,
            "returned": self.returned,
        }