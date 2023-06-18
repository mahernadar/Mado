import json
import time
from datetime import date, datetime
from datetime import time as tm
from datetime import timedelta

import cv2
import numpy as np

from customer import Customer, Supermarket
from tiles_coordinates import *

TILE_SIZE = 32

MARKET = """
######################
##..................##
##..ff..DD..dd..SS..##
##..ff..DD..dd..SS..##
##..ff..DD..dd..SS..##
##..ff..DD..dd..SS..##
##...................#
##..C#..C#..C#..C#...#
##..##..##..##..##...#
##...................#
##############GG######
""".strip()


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        self.tiles = tiles
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows * TILE_SIZE, self.ncols * TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def extract_tile(self, position):
        """extract a tile array from the tiles image"""
        y = position[0] * TILE_SIZE
        x = position[1] * TILE_SIZE
        return self.tiles[y : y + TILE_SIZE, x : x + TILE_SIZE]

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile((0, 0))
        elif char == "G":
            return self.extract_tile((7, 3))
        elif char == "f":
            fruit_index = np.random.choice(len(fruits_avatar_tiles_coordinates))
            fruit = fruits_avatar_tiles_coordinates[fruit_index]
            return self.extract_tile(fruit)
        elif char == "D":
            dairy_index = np.random.choice(len(dairy_avatar_tiles_coordinates))
            dairy = dairy_avatar_tiles_coordinates[dairy_index]
            return self.extract_tile(dairy)
        elif char == "d":
            drink_index = np.random.choice(len(drinks_avatar_tiles_coordinates))
            drink = drinks_avatar_tiles_coordinates[drink_index]
            return self.extract_tile(drink)
        elif char == "S":
            spice_index = np.random.choice(len(spices_avatar_tiles_coordinates))
            spice = spices_avatar_tiles_coordinates[spice_index]
            return self.extract_tile(spice)
        elif char == "C":
            return self.extract_tile((2, 8))
        else:
            return self.extract_tile((1, 2))

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row * TILE_SIZE
                x = col * TILE_SIZE
                self.image[y : y + TILE_SIZE, x : x + TILE_SIZE] = bm

    def draw(self, frame, customers=None):
        """
        draws the image into a frame
        """
        frame[0 : self.image.shape[0], 0 : self.image.shape[1]] = self.image

        if customers is not None:
            for customer in customers:
                location = customer.current_location
                location_coordinates = supermarket_locations_coordinates[
                    location
                ]
                avatar = customer.avatar

                x = location_coordinates[0] * TILE_SIZE
                y = location_coordinates[1] * TILE_SIZE

                avatar_tile = self.extract_tile(avatar)
                frame[y : y + TILE_SIZE, x : x + TILE_SIZE] = avatar_tile

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


if __name__ == "__main__":
    # initialize supermarket map:
    background = np.zeros((500, 704, 3), np.uint8)
    tiles = cv2.imread("data/tiles.png")

    market_map = SupermarketMap(MARKET, tiles)

    # set initial states at the start of SuperMarket day:
    # id starts as 1 each day; starting hour is 7:00 am
    id = 1
    sm_time = tm(7, 0)

    supermarket = Supermarket(
        customers_list=[], active_customers=[], time=sm_time, last_id=id
    )

    # load the pre-calculated probas dictionary:
    with open("data/tm_and_entry_probs_per_hour.json", "r") as fp:
        probas_per_hour = json.load(fp)

    while supermarket.time < tm(22, 0):
        frame = background.copy()

        time.sleep(1)

        supermarket.clean_inactive_customers()

        # todo: add customer one by one?
        supermarket.add_customer()
        supermarket.move_customers()

        market_map.draw(frame, customers=supermarket.active_customers)

        key = cv2.waitKey(1)

        if key == 113:  # 'q' key
            # todo: get all paths if interrupted:

            all_clients_paths = supermarket.get_customers_paths()

            with open(
                f"data/customers_paths_{supermarket.time}.json", "w"
            ) as fp:
                json.dump(all_clients_paths, fp)
            break

        cv2.imshow("frame", frame)

        # we choose to jump 20 minutes at a time for the visualization's sake:
        # each hour of the day has its own Transition Matrix + entrance probabilities:
        supermarket.time = (
            datetime.combine(date(1, 1, 1), sm_time) + timedelta(minutes=20)
        ).time()

    cv2.destroyAllWindows()

    market_map.write_image("supermarket.png")
