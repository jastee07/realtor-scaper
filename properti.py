class Properti:

    def __init__(
            self, address = None, 
            second_address = None, 
            price = None, 
            beds = None, 
            baths = None, 
            sqft = None, 
            lot_sqft = None,
            property_type = None
        ):
        self.address = address
        self.second_address = second_address
        self.price = price
        self.beds = beds
        self.baths = baths
        self.sqft = sqft
        self.lot_sqft = lot_sqft
        self.property_type = property_type

    def __str__():
        return self.address

    def get_cells(self):
        return [
            self.address,
            self.second_address,
            self.price,
            self.beds,
            self.baths,
            self.sqft,
            self.lot_sqft,
            self.property_type
        ]