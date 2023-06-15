import time


class Customer:
    def __init__(self, customer):
        self.id = customer["id"]
        self.current_location = list(customer["transition_probabilities"].keys())[0]
        self.transition_probabilities = customer["transition_probabilities"]
        self.path = [self.current_location]

    def move(self):
        while self.current_location != "checkout":
            current_transition_probabilities = self.transition_probabilities[
                self.current_location
            ]
            self.current_location = np.random.choice(
                list(current_transition_probabilities.keys()),
                p=list(current_transition_probabilities.values()),
            )
            self.path.append(self.current_location)

    def get_path(self):
        return self.path

    def get_customer_data(self):
        return {"id": self.id, "path": self.path}


customer = {
    "id": 1,
    "transition_probabilities": {
        "entrance": {
            "checkout": 0.0,
            "dairy": 0.2,
            "drinks": 0.2,
            "fruit": 0.3,
            "spices": 0.3,
        },
        "dairy": {
            "checkout": 0.3,
            "dairy": 0.0,
            "drinks": 0.2,
            "fruit": 0.2,
            "spices": 0.3,
        },
        "drinks": {
            "checkout": 0.4,
            "dairy": 0.1,
            "drinks": 0.0,
            "fruit": 0.2,
            "spices": 0.3,
        },
        "fruit": {
            "checkout": 0.5,
            "dairy": 0.1,
            "drinks": 0.1,
            "fruit": 0.1,
            "spices": 0.2,
        },
        "spices": {
            "checkout": 0.6,
            "dairy": 0.1,
            "drinks": 0.1,
            "fruit": 0.05,
            "spices": 0.15,
        },
        "checkout": {"checkout": 1.0},
    },
}


class Supermarket:
    def __init__(self, customers, transition_probabilities):
        self.customers = customers
        self.transition_probabilities = transition_probabilities

    def generate_gif(self):
        paths = [customer.get_path() for customer in self.customers]
        time.sleep()

    def move_customers(self):
        for customer in self.customers:
            customer.move()

    def get_customers_paths(self):
        return [customer.get_path() for customer in self.customers]


cust1 = Customer(customer)

cust1.move()
print(cust1.current_location)

cust1.move()
print(cust1.current_location)


print(cust1.get_customer_data())
