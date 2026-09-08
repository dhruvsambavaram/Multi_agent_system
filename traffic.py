# traffic.py
# Traffic Management System using Object-Oriented Programming in Python


class Vehicle:
    def __init__(self, vehicle_id, speed=0, position=0):
        self.vehicle_id = vehicle_id
        self.speed = speed
        self.position = position

    def move(self, distance):
        self.position += distance
        print(f"Vehicle {self.vehicle_id} moved to position {self.position}")

    def stop(self):
        self.speed = 0
        print(f"Vehicle {self.vehicle_id} stopped")


class TrafficLight:
    STATES = ["Red", "Yellow", "Green"]

    def __init__(self):
        self.state = "Green"
        self.timer = 0

    def change_state(self):
        index = self.STATES.index(self.state)
        self.state = self.STATES[(index + 1) % len(self.STATES)]
        self.timer = 0
        print(f"Traffic light changed to {self.state}")

    def update(self):
        self.timer += 1
        if self.timer >= 3:
            self.change_state()


class TrafficControl:
    def __init__(self):
        self.traffic_light = TrafficLight()
        self.vehicles = []

    def add_vehicle(self, vehicle_id):
        vehicle = Vehicle(vehicle_id)
        self.vehicles.append(vehicle)
        print(f"Vehicle {vehicle_id} added to traffic control system")

    def manage_traffic(self, cycles=3):
        for cycle in range(cycles):
            self.traffic_light.update()
            if self.traffic_light.state == "Green":
                for vehicle in self.vehicles:
                    vehicle.move(10)
            elif self.traffic_light.state == "Red":
                for vehicle in self.vehicles:
                    vehicle.stop()
            print(f"Cycle {cycle + 1} complete. Current state: {self.traffic_light.state}")


def main():
    traffic_control = TrafficControl()
    traffic_control.add_vehicle("V001")
    traffic_control.add_vehicle("V002")

    print("Starting traffic management simulation...")
    traffic_control.manage_traffic(cycles=5)

    for vehicle in traffic_control.vehicles:
        print(f"Final position of Vehicle {vehicle.vehicle_id}: {vehicle.position}")


if __name__ == "__main__":
    main()
