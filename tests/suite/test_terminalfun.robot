*** Settings ***
Documentation    Test cases for terminal-fun snap
Resource         kvm.resource


*** Test Cases ***
Terminal Fun Launches And Renders
    [Documentation]    Verify terminal-fun snap launches and renders a UI on Mir
    [Tags]    smoke    yarf:certification_status: blocker
    Log Screenshot
