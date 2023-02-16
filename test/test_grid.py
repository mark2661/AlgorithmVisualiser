from __future__ import annotations
import pytest
from src.grid import Grid
from src.tile import Tile
from src.settings import *

WIDTH, HEIGHT = 1000, 1000


@pytest.fixture
def grid():
    """ creates and returns a grid object using the global WIDTH and Height defined above
        for testing
    """
    def _grid_factory(width, height):
        return Grid((width, height))
    print("Making grid")
    return _grid_factory


"""*****************************************************************************************************************"""


@pytest.mark.parametrize("width, height", [(WIDTH, HEIGHT)])
def test_add_tiles(grid, width, height):
    """ tests add_tiles method in grid.py.
        first checks all pygame.Sprite.Group objects are empty upon initialisation.
        checks that only grid.tiles group is populated after function call and that all tiles have the correct
        BLANK_TILE_COLOUR
    """

    # set up
    grid = grid(width, height)
    # remove all tiles from grid.tiles
    grid.tiles.empty()
    # check all groups are empty
    assert all(len(group) == 0 for group in [grid.tiles, grid.wall_tiles, grid.start_tile, grid.end_tile])

    # test
    grid.add_tiles()

    # asset
    # number of tiles in grid should equal gird area divided by tile area
    assert len(grid.tiles) == (WIDTH * HEIGHT) // (TILE_WIDTH * TILE_HEIGHT)
    # check wall_tiles, start_tile and end_tile group is empty
    assert all(len(group) == 0 for group in [grid.wall_tiles, grid.start_tile, grid.end_tile])
    # check all tiles are correct colour (BLANK_TILE_COLOUR)
    assert all(tile.colour == BLANK_TILE_COLOUR for tile in grid.tiles)


"""*****************************************************************************************************************"""


@pytest.mark.parametrize("width, height", [(TILE_WIDTH*3, TILE_HEIGHT*3)])
def test_get_valid_neighbours_center_tile_with_four_valid_neighbours(grid, width, height):
    """ test get_valid_neighbours method in grid.py.
        creates a tile in the centre of the grid which should have 4 valid neighbours (up, down, left, right)
        providing input dimensions are correct.
        The test checks:
        1. 4 neighbour tiles are returned
        2. all neighbours are Tile objects
        3. the correct neighbours are returned (up, down, left, right)
        4. checks all tiles have the correct "colour" (BLANK_TILE_COLOUR from settings.py)
    """

    # set up
    grid = grid(width, height)
    top_left_coord_of_center_tile = (((width // TILE_WIDTH) // 2) * TILE_WIDTH,
                                     ((height // TILE_HEIGHT) // 2) * TILE_HEIGHT)

    test_tile_in_center_of_grid = Tile(top_left_coord_of_center_tile, grid.tiles)

    # test
    valid_neighbours = grid.get_valid_neighbours(test_tile_in_center_of_grid)

    # assert
    assert len(valid_neighbours) == 4  # check four neighbours returned
    assert all(type(tile) == Tile for tile in valid_neighbours) # check all return values are the correct type
    assert any(tile.rect.topleft == (TILE_WIDTH, 0) for tile in valid_neighbours) # check up neighbour is present
    assert any(tile.rect.topleft == (TILE_WIDTH, 2*TILE_HEIGHT) for tile in valid_neighbours)  # check down neighbour is present
    assert any(tile.rect.topleft == (0, TILE_HEIGHT) for tile in valid_neighbours)  # check left neighbour is present
    assert any(tile.rect.topleft == (2*TILE_WIDTH, TILE_HEIGHT) for tile in valid_neighbours)  # check right neighbour is present
    assert all(tile.colour == BLANK_TILE_COLOUR for tile in valid_neighbours) # check all tiles have correct "colour"


"""*****************************************************************************************************************"""


@pytest.mark.parametrize("width, height, invalid_neighbours, valid_neighbour_booleans",
                         [
                             pytest.param(TILE_WIDTH*3, TILE_HEIGHT*3, [(0, TILE_HEIGHT)],
                                          {"up":True, "down":True, "left":False, "right":True},
                                          id="left neighbour not valid"),

                             pytest.param(TILE_WIDTH * 3, TILE_HEIGHT * 3, [(TILE_WIDTH*2, TILE_HEIGHT)],
                                          {"up":True, "down":True, "left":True, "right":False},
                                          id="right neighbour not valid"),

                             pytest.param(TILE_WIDTH * 3, TILE_HEIGHT * 3, [(TILE_WIDTH, 0)],
                                          {"up":False, "down":True, "left":True, "right":True},
                                          id="up neighbour not valid"),

                             pytest.param(TILE_WIDTH * 3, TILE_HEIGHT * 3, [(TILE_WIDTH, TILE_HEIGHT*2)],
                                          {"up":True, "down":False, "left":True, "right":True},
                                          id="down neighbour not valid")
                         ])
def test_get_valid_neighbours_center_tile_with_three_valid_neighbours(grid, width: int, height: int,
                                                                      invalid_neighbours: tuple[float, float],
                                                                      valid_neighbour_booleans: dict[bool]):
    """ test get_valid_neighbours method in grid.py.
        creates a tile in the centre of the grid which should have 3 valid neighbours out of (up, down, left, right)
        neighbours.
        providing input dimensions are correct.
        The test checks:
        1. 3 neighbour tiles are returned
        2. all neighbours are Tile objects
        3. the correct neighbours are returned 3/4 from (up, down, left, right) neighbours
        4. checks all tiles have the correct "colour" (BLANK_TILE_COLOUR from settings.py)
    """

    # set up
    grid = grid(width, height)
    top_left_coord_of_center_tile = (((width // TILE_WIDTH) // 2) * TILE_WIDTH,
                                     ((height // TILE_HEIGHT) // 2) * TILE_HEIGHT)

    test_tile_in_center_of_grid = Tile(top_left_coord_of_center_tile, grid.tiles)

    # make tiles in invalid_neighbours wall tiles
    for tile_top_left_cords in invalid_neighbours:
        center_x, center_y = tile_top_left_cords[0] + (TILE_WIDTH // 2), tile_top_left_cords[1] + (TILE_HEIGHT // 2)
        grid.wall_tiles.add(grid.tile_map.get((center_x, center_y), None))

    # test
    valid_neighbours = grid.get_valid_neighbours(test_tile_in_center_of_grid)

    # assert
    assert len(valid_neighbours) == 3  # check three neighbours returned
    assert all(type(tile) == Tile for tile in valid_neighbours) # check all return values are the correct type
    assert all(tile.colour == BLANK_TILE_COLOUR for tile in valid_neighbours) # check all tiles have correct "colour"

    # check up neighbour is present
    if valid_neighbour_booleans.get("up", None):
        assert any(tile.rect.topleft == (TILE_WIDTH, 0) for tile in valid_neighbours)

    # check down neighbour is present
    if valid_neighbour_booleans.get("down", None):
        assert any(tile.rect.topleft == (TILE_WIDTH, 2*TILE_HEIGHT) for tile in valid_neighbours)

    # check left neighbour is present
    if valid_neighbour_booleans.get("left", None):
        assert any(tile.rect.topleft == (0, TILE_HEIGHT) for tile in valid_neighbours)

    # check right neighbour is present
    if valid_neighbour_booleans.get("right", None):
        assert any(tile.rect.topleft == (2*TILE_WIDTH, TILE_HEIGHT) for tile in valid_neighbours)


"""*****************************************************************************************************************"""


@pytest.mark.parametrize("width, height, include_wall_tiles",
                         [
                             pytest.param(TILE_WIDTH * 3, TILE_HEIGHT * 3, False, id="left neighbour not valid"),
                             pytest.param(TILE_WIDTH * 3, TILE_HEIGHT * 3, True, id="right neighbour not valid")
                         ])
def test_reset(grid, width: int, height: int, include_wall_tiles: bool):
    """
    test reset method in grid.py
    the test sets the centre tile of a grid to a wall tile and changes the tile to the appropriate colour.
    the test checks that all tiles have been reset to "blank tiles" if include_wall_tiles is True. And test wall tiles
    are left unchanged if include_wall_tiles is False.
    """
    # setup
    grid = grid(width, height)

    top_left_coord_of_center_tile = (((width // TILE_WIDTH) // 2) * TILE_WIDTH,
                                     ((height // TILE_HEIGHT) // 2) * TILE_HEIGHT)

    test_tile_in_center_of_grid = Tile(top_left_coord_of_center_tile, grid.tiles)

    # turn centre tile into wall tile
    grid.wall_tiles.add(test_tile_in_center_of_grid)
    # change centre tile to wall tile colour
    test_tile_in_center_of_grid.colour = WALL_TILE_COLOUR

    # check all groups have the correct number of tiles
    assert len(grid.wall_tiles) == 1
    assert len(grid.start_tile) == 0
    assert len(grid.end_tile) == 0
    assert len(grid.tiles) > 0

    # test
    grid.reset(include_wall_tiles)

    # assert
    # check the start and end tile groups have been reset
    assert len(grid.start_tile) == 0
    assert len(grid.end_tile) == 0

    if include_wall_tiles:
        assert len(grid.wall_tiles) == 0
        assert all(tile.colour == BLANK_TILE_COLOUR for tile in grid.tiles)

    else:
        assert len(grid.wall_tiles) == 1
        assert all(tile.colour == BLANK_TILE_COLOUR for tile in grid.tiles if tile not in grid.wall_tiles)

