
*** Test Cases ***
Empty test 1
    Test    1

Empty test 2
    Test    2

Empty test 3
    Test    3

Empty test 4
    Test    4

Empty test 5
    Test    5

Empty test 6
    Test    6

Empty test 7
    Test    7

Empty test 8
    Test    8

Empty test 9
    Test    9

Empty test 10
    Test    10
*** Keywords ***
Test
    [Arguments]     ${test_number}
    Sleep   ${test_number}
#    Log to console      Test${test_number}