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


When listing the current tasks, the timer status is shown as YES or NO, and 
the elapsed time is shown in hours and minutes. If it rolls over you need a 
better way of task management...meh etc.

Here would be a typical use sequence:

    (env) {21:34}~/Documents/code/python/chronotrak:main ✗ ➭
    (env) {21:34}~/Documents/code/python/chronotrak:main ✗ ➭ ./chronotrak.py create Do this first
    Created! ID is 1
    (env) {21:34}~/Documents/code/python/chronotrak:main ✗ ➭ ./chronotrak.py create No, no, do that first
    Created! ID is 2
    (env) {21:34}~/Documents/code/python/chronotrak:main ✗ ➭ ./chronotrak.py create Friday, break out the beer
    s
    Created! ID is 3
    (env) {21:35}~/Documents/code/python/chronotrak:main ✗ ➭ ./chronotrak.py list

     id      run?    started              Duration  message
    -------------------------------------------------------
    (   1)   YES     2022/02/16 21:34:43  01:00     Do this first
    (   2)   YES     2022/02/16 21:34:50  01:00     No, no, do that first
    (   3)   YES     2022/02/16 21:35:00  01:00     Friday, break out the beers

    (env) {21:35}~/Documents/code/python/chronotrak:main ✗ ➭ ./chronotrak.py update 3 Friday, break out the beers AND cakes
    Entry updated OK
    (env) {21:35}~/Documents/code/python/chronotrak:main ✗ ➭ ./chronotrak.py list

     id      run?    started              Duration  message
    -------------------------------------------------------
    (   1)   YES     2022/02/16 21:34:43  01:00     Do this first
    (   2)   YES     2022/02/16 21:34:50  01:00     No, no, do that first
    (   3)   YES     2022/02/16 21:35:00  01:00     Friday, break out the beers AND cakes

