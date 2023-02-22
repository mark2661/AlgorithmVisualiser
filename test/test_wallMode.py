from __future__ import annotations
import pytest
import pygame
from typing import Union, Callable, Optional
from src.grid import Grid
from src.tile import Tile
from src.mode.wallMode import WallMode
from src.settings import *


@pytest.fixture
def grid() -> Callable:
    """ creates and returns a grid object using the global WIDTH and Height defined above
        for testing
    """

    def _grid_factory(width: Union[int, float], height: Union[int, float]) -> Grid:
        return Grid((width, height))

    return _grid_factory


"""*****************************************************************************************************************"""


@pytest.mark.parametrize("width, height, groups",
                            [
                                pytest.param(3*TILE_WIDTH,3*TILE_HEIGHT, set(["tiles"]),
                                             id="Tile object with group membership: tiles"),

                                pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT, set(["tiles", "wall_tiles"]),
                                             id="Tile object with group membership: tiles, wall_tiles"),

                                pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT, set(["start_tile"]),
                                             id="Tile object with group membership: start_tile"),

                                pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT, set(["end_tile"]),
                                             id="Tile object with group membership: end_tile"),

                            ])
def test_set_tile(grid: Callable, width: Union[int, float], height: Union[int, float],
                  groups: set[str]) -> None:
    """
        test set_tile method in src.mode.wallMode.py. The test checks to see if method removes the tile object from all
        special groups (i.e. All groups except for the tiles group), Adds the tile object to the wall_tiles group and
        correctly updates the colour to the WALL_TILE_COLOUR in src.settings.py
    """

    # setup
    grid: Grid = grid(width, height)
    test_wall_mode: WallMode = WallMode(grid)
    test_tile: Tile = Tile((0, 0), grid.tiles)

    assert test_tile.colour == BLANK_TILE_COLOUR

    # add tile object to groups supplied as an argument
    for group in groups:
        exec(f"grid.{group}.add(test_tile)")

    # check tile has been added to the argument groups
    for group in groups:
        assert test_tile in eval(f"grid.{group}")

    # test
    test_wall_mode.set_tile(test_tile)

    # assert
    # check tile has been removed from ALL groups EXCEPT grid.tiles and grid.wall_tiles
    for group in groups:
        if group in ["tiles", "wall_tiles"]:
            assert test_tile in eval(f"grid.{group}")
        else:
            assert test_tile not in eval(f"grid.{group}")

    # check the tile colour has been changed to WALL_TILE_COLOUR
    assert test_tile.colour == WALL_TILE_COLOUR


"""*****************************************************************************************************************"""


@pytest.mark.parametrize("width, height, groups",
                            [
                                pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT, set(["tiles", "wall_tiles"]),
                                             id="tile with group membership: tiles, wall_tiles"),

                                pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                             set(["tiles", "wall_tiles", "start_tile"]),
                                             id="tile with group membership: tiles, start_tile"),

                                pytest.param(3 * TILE_WIDTH, 3 * TILE_HEIGHT,
                                             set(["tiles", "wall_tiles", "end_tile"]),
                                             id="tile with group membership: tiles, end_tile"),
                            ])
def test_reset_tile(grid: Callable, width: Union[int, float], height: Union[int, float],
                    groups: set[str]) -> None:
    """
    test reset_tile method in src.mode.wallMode.py. The test checks to see if the method removes a tile object
    from the wall_tiles group ONLY. The test also checks to see if the tile objects colour is correctly reset
    to BLANK_WALL_TILE colour
    """
    # setup
    grid: Grid = grid(width, height)
    test_wall_mode: WallMode = WallMode(grid)
    test_tile: Tile = Tile((0, 0), grid.tiles)

    # add tile object to groups supplied as an argument
    for group in groups:
        exec(f"grid.{group}.add(test_tile)")

    # check tile has been added to the argument groups
    for group in groups:
        assert test_tile in eval(f"grid.{group}")

    # test
    assert test_tile in grid.wall_tiles
    test_wall_mode.reset_tile(test_tile)

    # assert
    # check tile has been removed grid.wall_tiles group ONLY
    for group in groups:
        if group == "wall_tiles":
            assert test_tile not in eval(f"grid.{group}")
        else:
            assert test_tile in eval(f"grid.{group}")

    # check tile colour has been reset to BLANK_TILE_COLOUR from src.settings
    assert test_tile.colour == BLANK_TILE_COLOUR



