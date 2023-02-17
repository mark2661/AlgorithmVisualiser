import pytest
from src.grid import Grid
from src.eventHandler import EventHandler
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


@pytest.fixture
def event_handler():
    def _event_handler_factory(grid: Grid):
        return EventHandler(grid)

    return _event_handler_factory


"""*****************************************************************************************************************"""


@pytest.mark.parametrize("index, result",
                         [
                             (0, 1),
                             (1, 2),
                             (2, 0),
                         ])
def test__change_mode(grid, event_handler, index, result):
    """ tests if _change_mode method in eventHandler.py correctly increments the mode_index instance
        variable by one per call and wraps back around to zero if mode_index >= len(modes).
        Also tests the mode instance variable has been updated/assigned the corresponding value from modes[mode_index]
    """

    # set up
    grid = grid(WIDTH, HEIGHT)
    event_handler = event_handler(grid)

    # use a known fixed list of modes (the contents and data types of the list are irrelevant for this test)
    event_handler.modes = ["test_mode_1", "test_mode_2", "test_mode_3"]

    # test
    event_handler.mode_index = index
    event_handler.mode = event_handler.modes[event_handler.mode_index]

    event_handler._change_mode()

    # assert
    assert event_handler.mode_index == result
    assert event_handler.mode == event_handler.modes[result]


"""*****************************************************************************************************************"""
