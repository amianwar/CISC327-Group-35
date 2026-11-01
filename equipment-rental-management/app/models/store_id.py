from datetime import date, timedelta

RENTAL_PERIOD_DAYS = 7

# This model is essentially an updated version of the existing
# Rental model.

class Store_ID:
    def __init__ (
        self,
        id,
        equipment_id,
        renter_id,
        id_type,
        id_number,
        due_date,
        rental_date=None,
        return_date=None,
        deposit_amount=0.0,
        deposit_released=False,
    ):
        self.id = id
        self.equipment_id = equipment_id
        self.renter_id = renter_id
        self.id_type = id_type
        self.id_number = id_number
        self.rental_date = rental_date or date.today()
        self.due_date = due_date
        self.return_date = return_date
        self.deposit_amount = deposit_amount
        self.deposit_released = deposit_released

    def to_dict(self):
        return {
            "id": self.id,
            "equipment_id": self.equipment_id,
            "renter_id": self.renter_id,
            "id_type": self.id_type,
            "id_number": self.id_number,
            "rental_date": self.rental_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "return_date": self.return_date.isoformat() if self.return_date else None,
            "deposit_amount": self.deposit_amount,
            "deposit_released": self.deposit_released,
        }

    @staticmethod
    def default_due_date():
        return date.today() + timedelta(days=RENTAL_PERIOD_DAYS)
