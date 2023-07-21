# mcc-build-scenarios-shared
Python script for streamlining the process of building maps with shared resources.
Currently supports H3 and H4, with more support on the way.

# Requirements
[Python](https://www.python.org/) - preferably 3.10.6 or newer, older versions not tested

# Usage
* Place the .py file somewhere on your pc (don't put it in a protected folder!).
* Run the .py file from CMD with **py mcc_build_scenarios_shared.py**.
* Choose the engine you want to build scenarios for with the drop-down menu.
* Click "Add Scenario", and browse to and select your scenario file.
* Add more scenarios in the same way.
* If you wish to remove a scenario from the list, click it (it will be highlighted in blue), and use the "Remove Selected Scenario" button.
* Once you have added all of the scenarios you wish to compile together using shared resources, hit "Compile Scenarios!".
* This process will take a fairly long time. You can monitor the progress in the CMD window.
* The tool will notify you with a message once the process completes successfully.