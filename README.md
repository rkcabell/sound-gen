# Tuning Fork Simulator

## Instructions
Place both python files in the same directory

$ pip install -r requirements.txt

### Run Command:
$ python forksim.py

This will open a localhost webpage (http://localhost:52470/) running the vpython script to simulate the tuning forks


## Notes
The shape was initially going to change the tone but was scrapped
Density was meant to be changeable, for now it is 5800 for the inital fork and 3000 for subsequent forks
Formula for frequency is (N / (2 * pi * length**2)) * sqrt((young_modulus * moment_of_inertia) / (density * cross_section_area))

I stopped working on this project because vPython is outdated and not fun to work with. It can be reformatted to work with another language as the complexity is low and all the math is done with numpy. I used vPython because it was the first result I found to generate a tone as well as drawing an image.
