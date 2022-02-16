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

    (env) {21:32}~/Documents/code/python/chronotrak:main ✓ ➭ ./chronotrak.py

    Usage :- chronotrak [COMMAND] arg1 arg2 ..argN

    The values of arg1 etc are COMMAND specific where COMMAND may
    have one of the following options:

    list        : list all current tasks and their ID numbers.
    create      : create a new task and start tracking immediately.
    update  ID  : modify the message for the given entry.
    stop    ID  : stop tracking the given entry.
    delete  ID  : delete the given entry.

    Some examples:

    ./chronotrak list
    ./chronotrak create This is a test issue
    ./chronotrak update 2 This is the new message string
    ./chronotrak stop 2
    ./chronotrak delete 2

