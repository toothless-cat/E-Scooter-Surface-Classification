# E-Scooter-Surface-Classification
A tool developed during summer 2019 internship at Cal Poly DxHub. It utilizes accelerometer data to detect when an E-Scooter is being ridden on a sidewalk, and then shuts the scooter off.

Here is an outline of the resources included:

# Development Phase (outdated, optimized for skateboard data):

  App: A custom Android app that streams GPS and IMU data to a Kinesis stream via API

  Python Sandbox: Python code with test functions and graph outputs.

  Lambda Function: Final processing algorithm, it parses the kinesis data and 
  outputs a CSV-friendly table of geotagged surface classifications. This function also had a hybrid mode wherein it considered both GPS     and IMU patterns to form an accurate composite classification. The CSV output could be plotted onto a custom Google Maps.

# Deployment Phase (current, optimized for e-scooter):

  STL Files: The 3D printable pieces that attach to the e-scooter and enable hacking.

  Parts list: Contains all of the electronic components and hardware (m3 screws, nuts, arduino nano, battery management board, battery       boost board, mx2125 accelerometer, 18650 lithium ion cell, on/off switch, multi-strand data cable,relay,transistor,diode)

  Serial terminal: Basic Python script for connecting to arduino, can be optimized for datalogging.

  Datalogging program: Arduino code that outputs accelerometer data to a serial terminal at 50hz

  Python Sandbox: Python code with test functions and graph outputs. Used for testing different algorithm concepts.

  Filter Program: Arduino code that classifies surfaces and cuts the scooter’s throttle when on sidewalk.




