# Standard Library
from collections import defaultdict
from itertools import combinations

# Third Party
from ortools.sat.python import cp_model

# Locals
from ..models import Booking, Customer, Pet, Service

customers = [
    Owner("Alice"),
    Owner("Bob"),
    Owner("Charlie"),
]

max_size = 4

dogs = [
    Dog("Abby", customers[0]),
    Dog("Ace", customers[0]),
    Dog("Addie", customers[0]),
    Dog("Bella", customers[1]),
    Dog("Bentley", customers[1]),
    Dog("Casey", customers[2]),
]

for i in range(len(dogs), 12):
    customer = Owner("bob")
    customers.append(customer)
    dogs.append(Dog(f"dog-{i}", customer))

customer_to_dogs = defaultdict(list)
for dog in dogs:
    customer_to_dogs[dog.owner].append(dog)

walk_service = Service("Walk", 60)

shifts = list(map(str, range(len(dogs))))

model = cp_model.CpModel()

walks = {dog: {shift: model.new_bool_var(f"walk_{dog}_{shift}") for shift in shifts} for dog in dogs}


# Creates the solver and solve.
solver = cp_model.CpSolver()

# Ensure each dog is walked exactly once.
for dog in dogs:
    model.add(sum(walks[dog][shift] for shift in shifts) == 1)

# Ensure no more than 4 dogs are walked at the same time.
for shift in shifts:
    model.add(sum(walks[dog][shift] for dog in dogs) <= 4)

# Ensure that all dogs from the same owner are walked at the same time.
for customer in customers:
    customer_dogs = customer_to_dogs[customer]
    for dog1, dog2 in combinations(customer_dogs, 2):
        for shift in shifts:
            model.add(walks[dog1][shift] == walks[dog2][shift])

# Keep the number of walks to a minimum.
walk_used = {shift: model.NewBoolVar(f"walk_used_{shift}") for shift in shifts}
# Set the boolean variables based on whether any dog is assigned to the shift
for shift in shifts:
    model.AddMaxEquality(walk_used[shift], [walks[dog][shift] for dog in dogs])
# Count the number of walks with at least one dog
walk_count = model.NewIntVar(0, len(shifts), "walk_count")
model.Add(walk_count == sum(walk_used[shift] for shift in shifts))

model.Minimize(walk_count)

status = solver.solve(model)


class Planner:
    solver: cp_model.CpSolver
    max_group_size: int

    def __init__(self, max_group_size: int = 4):
        self.solver = cp_model.CpSolver()
        self.max_group_size = max_group_size

    def plan(self, bookings: list[Booking], service: Service):
        pets: set[Pet] = {pet for booking in bookings for pet in booking.pets}
        customers: set[Customer] = {booking.customer for booking in bookings}

        model = cp_model.CpModel()

        return model
