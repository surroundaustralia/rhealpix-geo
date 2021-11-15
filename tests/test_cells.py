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


def test_collection_children():
    assert CellCollection('R1 P').children() == "P0 P1 P2 P3 P4 P5 P6 P7 P8 R10 R11 R12 R13 R14 R15 R16 R17 R18"


def test_collection_children_single_res():
    assert CellCollection('R1 P').children(resolution=1) == "P0 P1 P2 P3 P4 P5 P6 P7 P8 R1"


def test_collection_flatten_using_default():
    assert CellCollection(
        'R1 R2 P Q1 Q234').flatten() == "P000 P001 P002 P003 P004 P005 P006 P007 P008 P010 P011 P012 P013 P014 P015 P016 P017 P018 P020 P021 P022 P023 P024 P025 P026 P027 P028 P030 P031 P032 P033 P034 P035 P036 P037 P038 P040 P041 P042 P043 P044 P045 P046 P047 P048 P050 P051 P052 P053 P054 P055 P056 P057 P058 P060 P061 P062 P063 P064 P065 P066 P067 P068 P070 P071 P072 P073 P074 P075 P076 P077 P078 P080 P081 P082 P083 P084 P085 P086 P087 P088 P100 P101 P102 P103 P104 P105 P106 P107 P108 P110 P111 P112 P113 P114 P115 P116 P117 P118 P120 P121 P122 P123 P124 P125 P126 P127 P128 P130 P131 P132 P133 P134 P135 P136 P137 P138 P140 P141 P142 P143 P144 P145 P146 P147 P148 P150 P151 P152 P153 P154 P155 P156 P157 P158 P160 P161 P162 P163 P164 P165 P166 P167 P168 P170 P171 P172 P173 P174 P175 P176 P177 P178 P180 P181 P182 P183 P184 P185 P186 P187 P188 P200 P201 P202 P203 P204 P205 P206 P207 P208 P210 P211 P212 P213 P214 P215 P216 P217 P218 P220 P221 P222 P223 P224 P225 P226 P227 P228 P230 P231 P232 P233 P234 P235 P236 P237 P238 P240 P241 P242 P243 P244 P245 P246 P247 P248 P250 P251 P252 P253 P254 P255 P256 P257 P258 P260 P261 P262 P263 P264 P265 P266 P267 P268 P270 P271 P272 P273 P274 P275 P276 P277 P278 P280 P281 P282 P283 P284 P285 P286 P287 P288 P300 P301 P302 P303 P304 P305 P306 P307 P308 P310 P311 P312 P313 P314 P315 P316 P317 P318 P320 P321 P322 P323 P324 P325 P326 P327 P328 P330 P331 P332 P333 P334 P335 P336 P337 P338 P340 P341 P342 P343 P344 P345 P346 P347 P348 P350 P351 P352 P353 P354 P355 P356 P357 P358 P360 P361 P362 P363 P364 P365 P366 P367 P368 P370 P371 P372 P373 P374 P375 P376 P377 P378 P380 P381 P382 P383 P384 P385 P386 P387 P388 P400 P401 P402 P403 P404 P405 P406 P407 P408 P410 P411 P412 P413 P414 P415 P416 P417 P418 P420 P421 P422 P423 P424 P425 P426 P427 P428 P430 P431 P432 P433 P434 P435 P436 P437 P438 P440 P441 P442 P443 P444 P445 P446 P447 P448 P450 P451 P452 P453 P454 P455 P456 P457 P458 P460 P461 P462 P463 P464 P465 P466 P467 P468 P470 P471 P472 P473 P474 P475 P476 P477 P478 P480 P481 P482 P483 P484 P485 P486 P487 P488 P500 P501 P502 P503 P504 P505 P506 P507 P508 P510 P511 P512 P513 P514 P515 P516 P517 P518 P520 P521 P522 P523 P524 P525 P526 P527 P528 P530 P531 P532 P533 P534 P535 P536 P537 P538 P540 P541 P542 P543 P544 P545 P546 P547 P548 P550 P551 P552 P553 P554 P555 P556 P557 P558 P560 P561 P562 P563 P564 P565 P566 P567 P568 P570 P571 P572 P573 P574 P575 P576 P577 P578 P580 P581 P582 P583 P584 P585 P586 P587 P588 P600 P601 P602 P603 P604 P605 P606 P607 P608 P610 P611 P612 P613 P614 P615 P616 P617 P618 P620 P621 P622 P623 P624 P625 P626 P627 P628 P630 P631 P632 P633 P634 P635 P636 P637 P638 P640 P641 P642 P643 P644 P645 P646 P647 P648 P650 P651 P652 P653 P654 P655 P656 P657 P658 P660 P661 P662 P663 P664 P665 P666 P667 P668 P670 P671 P672 P673 P674 P675 P676 P677 P678 P680 P681 P682 P683 P684 P685 P686 P687 P688 P700 P701 P702 P703 P704 P705 P706 P707 P708 P710 P711 P712 P713 P714 P715 P716 P717 P718 P720 P721 P722 P723 P724 P725 P726 P727 P728 P730 P731 P732 P733 P734 P735 P736 P737 P738 P740 P741 P742 P743 P744 P745 P746 P747 P748 P750 P751 P752 P753 P754 P755 P756 P757 P758 P760 P761 P762 P763 P764 P765 P766 P767 P768 P770 P771 P772 P773 P774 P775 P776 P777 P778 P780 P781 P782 P783 P784 P785 P786 P787 P788 P800 P801 P802 P803 P804 P805 P806 P807 P808 P810 P811 P812 P813 P814 P815 P816 P817 P818 P820 P821 P822 P823 P824 P825 P826 P827 P828 P830 P831 P832 P833 P834 P835 P836 P837 P838 P840 P841 P842 P843 P844 P845 P846 P847 P848 P850 P851 P852 P853 P854 P855 P856 P857 P858 P860 P861 P862 P863 P864 P865 P866 P867 P868 P870 P871 P872 P873 P874 P875 P876 P877 P878 P880 P881 P882 P883 P884 P885 P886 P887 P888 Q100 Q101 Q102 Q103 Q104 Q105 Q106 Q107 Q108 Q110 Q111 Q112 Q113 Q114 Q115 Q116 Q117 Q118 Q120 Q121 Q122 Q123 Q124 Q125 Q126 Q127 Q128 Q130 Q131 Q132 Q133 Q134 Q135 Q136 Q137 Q138 Q140 Q141 Q142 Q143 Q144 Q145 Q146 Q147 Q148 Q150 Q151 Q152 Q153 Q154 Q155 Q156 Q157 Q158 Q160 Q161 Q162 Q163 Q164 Q165 Q166 Q167 Q168 Q170 Q171 Q172 Q173 Q174 Q175 Q176 Q177 Q178 Q180 Q181 Q182 Q183 Q184 Q185 Q186 Q187 Q188 Q234 R100 R101 R102 R103 R104 R105 R106 R107 R108 R110 R111 R112 R113 R114 R115 R116 R117 R118 R120 R121 R122 R123 R124 R125 R126 R127 R128 R130 R131 R132 R133 R134 R135 R136 R137 R138 R140 R141 R142 R143 R144 R145 R146 R147 R148 R150 R151 R152 R153 R154 R155 R156 R157 R158 R160 R161 R162 R163 R164 R165 R166 R167 R168 R170 R171 R172 R173 R174 R175 R176 R177 R178 R180 R181 R182 R183 R184 R185 R186 R187 R188 R200 R201 R202 R203 R204 R205 R206 R207 R208 R210 R211 R212 R213 R214 R215 R216 R217 R218 R220 R221 R222 R223 R224 R225 R226 R227 R228 R230 R231 R232 R233 R234 R235 R236 R237 R238 R240 R241 R242 R243 R244 R245 R246 R247 R248 R250 R251 R252 R253 R254 R255 R256 R257 R258 R260 R261 R262 R263 R264 R265 R266 R267 R268 R270 R271 R272 R273 R274 R275 R276 R277 R278 R280 R281 R282 R283 R284 R285 R286 R287 R288"

def test_collection_flatten():
    assert CellCollection('R1').flatten(2) == "R10 R11 R12 R13 R14 R15 R16 R17 R18"

def test_collection_flatten_invalid_res():
    with pytest.raises(ValueError):
        CellCollection('R1').flatten(0)
