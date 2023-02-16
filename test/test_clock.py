import pytest
import pygame
from src.clock import FpsClock


@pytest.mark.order1
def test_get_clock_object_instantiated():
    """ Test FpsClock.get_clock() returns a pygame clock object that has already been instantiated """

    # set up
    FpsClock.clock = pygame.time.Clock()
    # test
    returned_clock = FpsClock.get_clock()

    # assert
    assert type(returned_clock) == type(pygame.time.Clock())
    assert id(returned_clock) == id(FpsClock.clock)


@pytest.mark.order2
def test_get_clock_object_not_instantiated():
    """ Test FpsClock.get_clock() returns a pygame clock object when no object has been previously instantiated"""

    # set up
    FpsClock.clock = None
    assert FpsClock.clock is None
    # test
    returned_clock = FpsClock.get_clock()

    # assert
    assert type(returned_clock) == type(pygame.time.Clock())
    assert id(returned_clock) == id(FpsClock.clock)
