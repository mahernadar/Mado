import json
import time

import numpy as np

from tiles_coordinates import *

# from tiles_skeleton import *
# load the pre-calculated probas dictionary:
with open("data/tm_and_entry_probs_per_hour.json", "r") as fp:
    probas_per_hour = json.load(fp)


class Customer:
    def __init__(self, id, location):
        self.id = id
        self.avatar = self.set_customer_avatar()
        self.current_location = location
        self.path = [self.current_location]
        self.active = True

    def set_customer_avatar(self):
        avatar_index = np.random.choice(len(customers_avatar_tiles_coordinates))
        avatar_tuple = customers_avatar_tiles_coordinates[avatar_index]
        return avatar_tuple

    def move(self, transition_matrix: dict):
        if self.current_location != "checkout":
            tm = transition_matrix[self.current_location]
            next_location = np.random.choice(
                list(tm.keys()),
                p=list(tm.values()),
            )
            self.current_location = next_location
            # append the next location to the path of the customer in question:
            self.path.append(next_location)
        else:
            self.active = False

    def get_path(self):
        return self.path

    def get_customer_data(self):
        return {"id": self.id, "avatar": self.avatar, "path": self.path}


class Supermarket:
    def __init__(self, customers_list, active_customers, time, last_id):
        self.customers_list = customers_list
        self.active_customers = active_customers
        self.time = time
        self.last_id = last_id

    def generate_gif(self):
        paths = [customer.get_path() for customer in self.customers]
        time.sleep()

    def add_customer(self):
        current_hour = self.time.hour
        initial_location = np.random.choice(
            list(probas_per_hour[str(current_hour)]["entry_probas"].keys()),
            p=list(probas_per_hour[str(current_hour)]["entry_probas"].values()),
        )
        customer = Customer(id=id, location=initial_location)
        self.customers_list.append(customer)
        self.active_customers.append(customer)
        self.last_id += 1

    def move_customers(self):
        for customer in self.active_customers:
            transition_dict = probas_per_hour[str(self.time.hour)]["tm"]
            customer.move(transition_matrix=transition_dict)

    def clean_inactive_customers(self):
        for customer in self.active_customers:
            if not customer.active:
                self.active_customers.remove(customer)

    def get_customers_paths(self):
        return [{str(customer.id): customer.get_path()} for customer in self.customers_list]
