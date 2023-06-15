import cv2
import numpy as np
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

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0 : self.image.shape[0], 0 : self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


if __name__ == "__main__":
    background = np.zeros((500, 704, 3), np.uint8)
    tiles = cv2.imread("data/tiles.png")

    market = SupermarketMap(MARKET, tiles)

    while True:
        frame = background.copy()
        market.draw(frame)

        # https://www.ascii-code.com/
        key = cv2.waitKey(1)

        if key == 113:  # 'q' key
            break

        cv2.imshow("frame", frame)

    cv2.destroyAllWindows()

    market.write_image("supermarket.png")
