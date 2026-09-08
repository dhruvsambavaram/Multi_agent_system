class Vehicle:
    def __init__(self, make, license_plate):
        self.make = make
        self.license_plate = license_plate

    def get_make(self):
        return self.make

    def get_license_plate(self):
        return self.license_plate

    def info(self):
        return f"Vehicle(make={self.make}, license_plate={self.license_plate})"


class Car(Vehicle):
    def __init__(self, make, license_plate):
        super().__init__(make, license_plate)

    def info(self):
        return f"Car(make={self.get_make()}, license_plate={self.get_license_plate()})"


if __name__ == "__main__":
    v1 = Vehicle("Toyota", "ABC123")
    v2 = Car("Ford", "XYZ789")
    v3 = Vehicle("Honda", "DEF456")

    print(v1.info())
    print(v2.info())
    print(v3.info())
