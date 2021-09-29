"""
This Python 3.8 code tests the ``source.dggs_classes`` module.
Beware, these tests cover only some functions and only some scenarios.
Keep adding tests!
CHANGELOG:
- 2021-07-19:   David Habgood (DH): Initial version
- 2021-09-20:   DH: converted to pytest
"""
import pytest
from rheal import *


def test_dggs_geom_format_invalid_1():
    with pytest.raises(ValueError):
        Cell("H123")


def test_dggs_geom_format_invalid_2():
    with pytest.raises(ValueError):
        Cell("RH")


def test_dggs_geom_single_cell():
    assert Cell("P012").suids == ("P", 0, 1, 2)


# neighbours
def test_neighbour_up():
    assert Cell("R41").neighbour("up") == Cell("R17")


def test_neighbour_down():
    assert Cell("R47").neighbour("down") == Cell("R71")


def test_neighbour_left():
    assert Cell("R43").neighbour("left") == Cell("R35")


def test_neighbour_right():
    assert Cell("R45").neighbour("right") == Cell("R53")


def test_neighbours():
    assert Cell("R4").neighbours() == CellCollection("R0 R1 R2 R3 R5 R6 R7 R8")


def test_hemisphere_neighbours_res_1():
    assert Cell("P0").neighbours() == CellCollection("N5 N8 O2 O5 P1 P3 P4")


def test_zero_neighbours_P():
    assert Cell("P").neighbours() == CellCollection("N O Q S")


def test_zero_neighbours_N():
    assert Cell("N").neighbours() == CellCollection("O P Q R")


def test_cell_cell_addition():
    assert Cell("R4") + Cell("R5") == CellCollection("R4 R5")


def test_cell_cell_Subtraction():
    difference = Cell("R4") - Cell("R44")
    assert difference == CellCollection("R40 R41 R42 R43 R45 R46 R47 R48")


def test_cell_equal_positive():
    assert Cell("R4") == Cell("R4")


def test_cell_equal_negative():
    assert Cell("R4") != Cell("R1")


def test_cell_collection_equal_positive():
    assert CellCollection("R4 R3") == CellCollection("R3 R4")


def test_cell_collection_equal_negative():
    assert CellCollection("R4 R3") != CellCollection("R3123 R4543")


def test_border_no_resolution_specified():
    assert Cell("R").border() == Cell("R")


def test_border_no_resolution_1():
    assert Cell("R").border(resolution=1) == CellCollection("R0 R1 R2 R3 R5 R6 R7 R8")


def test_border_no_resolution_2():
    assert Cell("R").border(resolution=2) == CellCollection(
        "R00 R01 R02 R03 R06 R10 R11 R12 R20 R21 R22 R25 R28 R30 R33 R36 R52 R55 R58 R60 R63 R66 R67 R68 R76 R77 R78 R82 R85 R86 R87 R88"
    )


def test_collection_neighbours():
    assert CellCollection("P4 P5").neighbours() == CellCollection(
        "P0 P1 P2 P3 P6 P7 P8 Q0 Q3 Q6"
    )


def test_neighbours_at_resolution():
    assert CellCollection("P4").neighbours(resolution=3) == CellCollection(
        "P088 P166 P167 P168 P176 P177 P178 P186 P187 P188 P266 P322 P325 P328 P352 P355 P358 P382 P385 P388 P500 P503 P506 P530 P533 P536 P560 P563 P566 P622 P700 P701 P702 P710 P711 P712 P720 P721 P722 P800"
    )


# def test_collection_creation():
#     assert type(CellCollection("R1 R4 R5") == CellCollection


def test_invalid_collection_creation():
    with pytest.raises(ValueError):
        CellCollection("R1 frog")


def test_deduplication():
    assert CellCollection("R4 R1 R5 R5") == CellCollection("R1 R4 R5")


def test_absorb():
    assert CellCollection("R1 R12 R123") == "R1"


def test_collection_addition():
    assert CellCollection("R1") + CellCollection("R2") == CellCollection("R1 R2")


def test_collection_subtraction():
    assert (CellCollection("R1 R2") - CellCollection("R12")) == CellCollection(
        "R10 R11 R13 R14 R15 R16 R17 R18 R2"
    )


def test_collection_cell_subtraction():
    assert CellCollection("R1") - Cell("R12") == CellCollection(
        "R10 R11 R13 R14 R15 R16 R17 R18"
    )


def test_empty_result():
    assert CellCollection("R1") - CellCollection("R1") == CellCollection()


def test_collection_children():
    assert Cell("R").children() == CellCollection(
        "R0 R1 R2 R3 R4 R5 R6 R7 R8", compress=False
    )


def test_overlaps_true():
    assert Cell("R1").overlaps(Cell("R12"))


def test_overlaps_false():
    assert not Cell("R2").overlaps(Cell("R12"))


def test_collection_matches():
    assert CellCollection("P4", crs="auspix", kind="rHEALPix") == CellCollection(
        "P4", crs="auspix", kind="rHEALPix"
    )


def test_collection_not_matches():
    with pytest.raises(ValueError):
        CellCollection("P4", crs="auspix", kind="rHEALPix") == CellCollection(
            "P4", crs="blahblahblah", kind="rHEALPix"
        )


def test_collection_not_matches_():
    assert CellCollection() + CellCollection("R1") == CellCollection("R1")
