import pytest
from unittest import mock
from src.mode.mode import Mode
from src.grid import Grid
from src.settings import *


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


@pytest.mark.parametrize("width, height, mouse_pos, expected_result",
                         [
                             pytest.param(
                                 TILE_WIDTH * 3, TILE_HEIGHT * 3,
                                 (TILE_WIDTH + TILE_WIDTH // 2, TILE_HEIGHT + TILE_HEIGHT // 2),
                                 (TILE_WIDTH + TILE_WIDTH // 2, TILE_HEIGHT + TILE_HEIGHT // 2),
                                 id="mouse on center tile of 3x3 grid"
                             ),
                             pytest.param(
                                 TILE_WIDTH * 3, TILE_HEIGHT * 3,
                                 (-1, -1),
                                 None,
                                 id="mouse not on screen"
                             )

                         ]
                         )
def test_get_tile(grid, width, height, mouse_pos, expected_result):
    """
    test the get_tile method in mode.py.
    the test creates a grid of size width x height (input parameters) and mocks the call to pygame.mouse.get_pos method
    in get_tile with mouse coordinates passed in as an argument. The center coordinates of the tile objects rect is
    then compared with the expected_result since this coordinate is unique to the tile object.
    in the case that the mouse coordinates are not within bounds of any tile objects the test checks to see that None
    was returned.
    """

    # setup
    grid = grid(width, height)
    # disable the abstract methods dynamically at run time to allow for testing
    Mode.__abstractmethods__ = set()
    test_mode = Mode(grid)

    # test
    # using monkey patching to mock the output of pygame.mouse.get_pos with the argument mouse coordinates
    with mock.patch("pygame.mouse.get_pos", return_value=mouse_pos):
        test_tile = test_mode.get_tile()

    # assert
    if expected_result:
        assert test_tile.rect.center == expected_result
    else:
        assert test_tile is None


"""*****************************************************************************************************************"""
