from __future__ import annotations
import pytest
from typing import Union, Optional, Callable
from unittest import mock
from src.mode.mode import Mode
from src.grid import Grid
from src.settings import *
from src.tile import Tile


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


@pytest.mark.parametrize("width, height, groups",
                         [
                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT, set(["tiles"]),
                                          id="test with group membership: tiles"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT, set(["tiles", "wall_tiles"]),
                                          id="test with group membership: tiles, wall_tiles"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT, set(["tiles", "wall_tiles", "start_tile"]),
                                          id="test with group membership: tiles, wall_tiles, start_tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          set(["tiles", "wall_tiles", "start_tile", "end_tile"]),
                                          id="test with group membership: tiles, wall_tiles, start_tile, end_tile")
                         ])
def test_remove_tile_from_special_groups(grid, width: Union[int, float], height: Union[int, float],
                                         groups: set[str]):
    """
        test the remove_tile_from_special_groups method in mode.py. The test creates a grid of dimensions width X height
        (passed as arguments) then selects the center tile object and adds it to the groups in the groups argument.
        the test checks to see if remove_tile_tile_from_special_groups removes the tile object from ALL
        the argument member groups EXCEPT for the grid.tiles group.
    """
    # setup
    grid = grid(width, height)
    # disable the abstract methods dynamically at run time to allow for testing
    Mode.__abstractmethods__ = set()
    test_mode = Mode(grid)

    # centre tile of 3X3 grid -> (centre x of central tile, centre y of central tile)
    test_tile_coords = (((((width // TILE_WIDTH) // 2) * TILE_WIDTH) + TILE_WIDTH // 2),
                        ((((height // TILE_HEIGHT) // 2) * TILE_HEIGHT) + TILE_HEIGHT // 2))
    test_tile = grid.tile_map[test_tile_coords]

    # add tiles to the groups listed in the groups argument
    for group in groups:
        exec(f"grid.{group}.add(test_tile)")

    # check if tiles have been added to the groups supplied in the argument
    for group in groups:
        assert test_tile in eval(f"grid.{group}")

    # test
    test_mode.remove_tile_from_special_groups(test_tile)

    # assert
    for group in groups:
        if group == "tiles":
            assert test_tile in grid.tiles
        else:
            assert test_tile not in eval(f"grid.{group}")


"""*****************************************************************************************************************"""


@pytest.mark.parametrize("width, height, mouse_pos, expected_result",
                         [
                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          ((TILE_WIDTH + TILE_WIDTH // 2), (TILE_HEIGHT + TILE_HEIGHT // 2)),
                                          True, id="Mouse on centre of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          (TILE_WIDTH, TILE_HEIGHT), True,
                                          id="Mouse on top left corner of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          (2 * TILE_WIDTH, 2 * TILE_HEIGHT), True,
                                          id="Mouse on bottom right corner of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          (TILE_WIDTH, (TILE_HEIGHT + TILE_HEIGHT // 2)),
                                          True, id="Mouse on centre left edge of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          (2 * TILE_WIDTH, (TILE_HEIGHT + TILE_HEIGHT // 2)),
                                          True, id="Mouse on centre right edge of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          ((TILE_WIDTH + TILE_WIDTH // 2), TILE_HEIGHT),
                                          True, id="Mouse on centre top edge of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          ((TILE_WIDTH + TILE_WIDTH // 2), 2 * TILE_HEIGHT),
                                          True, id="Mouse on centre bottom edge of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          ((TILE_WIDTH // 2), (TILE_HEIGHT + TILE_HEIGHT // 2)),
                                          False, id="Mouse on centre of tile to the left of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          ((2 * TILE_WIDTH + TILE_WIDTH // 2), (TILE_HEIGHT + TILE_HEIGHT // 2)),
                                          False, id="Mouse on centre of tile to the right of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          ((TILE_WIDTH + TILE_WIDTH // 2), (TILE_HEIGHT // 2)),
                                          False, id="Mouse on centre of tile to above of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          ((TILE_WIDTH + TILE_WIDTH // 2), (2 * TILE_HEIGHT + TILE_HEIGHT // 2)),
                                          False, id="Mouse on centre of tile to below of centre tile"),

                             pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                          (-1, -1),
                                          False, id="Mouse off screen"),
                         ])
def test_cursor_on_tile(grid: Callable, width: Union[int, float], height: Union[int, float],
                        mouse_pos: tuple[Union[int, float], Union[int, float]], expected_result: bool):
    """
     test _cursor_on_tile method in mode.py. The test checks if the mouse position supplied as an argument lies within/
     on the bounds of the rect associated with the supplied Tile object.
    """
    # setup
    grid: Grid = grid(width, height)
    # disable the abstract methods dynamically at run time to allow for testing
    Mode.__abstractmethods__ = set()
    test_mode: Mode = Mode(grid)

    # centre tile of 3X3 grid -> (centre x of central tile, centre y of central tile)
    test_tile_coords: tuple[Union[int, float], Union[int, float]] = \
        (((((width // TILE_WIDTH) // 2) * TILE_WIDTH) + TILE_WIDTH // 2),
         ((((height // TILE_HEIGHT) // 2) * TILE_HEIGHT) + TILE_HEIGHT // 2))

    test_tile: Tile = grid.tile_map[test_tile_coords]

    # test
    result: bool = test_mode._cursor_on_tile(mouse_pos, test_tile)

    # assert
    assert result == expected_result
