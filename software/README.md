# The·Grid Software

This is the computer-side control software for The·Grid.

## Getting Set Up
You'll need Python 3.4.2 or 3.5. The requirements are listed in 
`requirements.txt`, you might want to install numpy and scipy via your package 
manager or Python distribution first and then use pip to install the rest:
`pip install -r requirements.txt`. You might want to use `pip3` on various 
Linux distributions. Consider installing into a virtualenv too.

For a basic Ubuntu setup, the following should work:
```
sudo apt-get install python3 python3-numpy python3-scipy
sudo pip3 install -r requirements.txt
```

## Writing Your Own Patterns
Patterns live in `thegrid/patterns/`. Simply copy the `template.py` file you'll 
find there to a new file, modify it as appropriate (see instructions inside the 
`template.py` file), and then add an import line for your new pattern to 
`thegrid/patterns/__init__.py`.

You can then check your new pattern locally in the simulator, and submit a pull 
request on GitHub to have it included in The·Grid at EMF. Or drop us an email 
with your new pattern file if pull requests aren't your thing.

## Running The Software

Should just need to:

`python3 main.py`

You can then connect to http://localhost:8080/ to access the web interface, 
which has links to the simulator and control panel.
