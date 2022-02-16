# Task Timer

Run the script to activate the environment and make sure that all required
dependencies are present, so after checking out this project, move into
the project folder and execute:

    $ python3 -m venv env
    $ . ./env/bin/activate
    $ pip install -r requirements.txt


# Running Tests

To run the tests and see all the console output:

    $ pytest -s

or just to see them run fine:

    $ pytest


# Running the tool

The utility is self-contained within a single file, it has been designed
to be able to run as a shell command, first, (not on Windows):

    $ chmod +x chronotrak

and then you can run it as:

    $ ./chronotrak

You may also run it as:

    $ python chronotrak.py  [command line args]...

With no command line arguments given it will print a list of the available
commands with some examples, or you can see the test code for some hints!
