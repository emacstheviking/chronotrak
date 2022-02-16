#!/usr/bin/env python
import sys
import sqlite3

from datetime import datetime

from typing import Optional, List


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
#
#                              DATABASE
#
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

class DB:
    """A simple database wrapper around our sqlite3 database."""

    DB_NAME = "chronotrak.db"

    def __init__(self):
        self.conn = sqlite3.connect(
            DB.DB_NAME,
            detect_types=sqlite3.PARSE_DECLTYPES)

    def ensure_database(self):
        """
        Ensure that we have a database connection, and that the required
        database table exists, creating it if necessary. If it is such
        that the table cannot be created or an exception is raised then
        we terminate with an appropriate message.

        *COULD* always return a cursor, but, assumptions about usage.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
            """create table if not exists chronotrak
               (
                message    text unique,
                status     integer,
                started_at timestamp,
                stopped_at timestamp
               );
            """)
            self.conn.commit()

            # check the table actually does exist, terminating
            # if not as there is no point in continuing!
            cur.execute(
                """select  count(name) from sqlite_master
                    where  type='table' and name='chronotrak';
                """)
            exists = cur.fetchone()
            if exists[0] == 1:
                return
            print("The chronotrak database could not be created")
        except Exception as e:
            print(str(e))
        sys.exit(-1)

    def get_tasks(self):
        """List all of the current timer tasks"""
        self.ensure_database()
        cur = self.conn.cursor()
        cur.execute(
            """select  rowid, message, status, started_at, stopped_at
               from    chronotrak
               order   by started_at
            """)
        all_rows = cur.fetchall()
        cur.close()  # don't leak handles!
        return all_rows

    def create_task(self, message: str) -> Optional[int]:
        """Create a new task, actively running, starting now!"""
        try:
            self.ensure_database()
            cur = self.conn.cursor()
            cur.execute(
                """insert into chronotrak (message, status, started_at)
                   values (?, 1, ?)
                """,
                (message, datetime.now()))
            self.conn.commit()
            new_id = cur.lastrowid
            cur.close()
            return new_id
        except Exception as e:
            print(str(e))
        return None

    def kill_task(self, task_id: str) -> bool:
        try:
            actual_id = int(task_id)
            self.ensure_database()
            cur = self.conn.cursor()
            cur.execute(
                "delete from chronotrak where rowid=?",
                (actual_id,))
            self.conn.commit()
            was_deleted = cur.rowcount == 1
            cur.close()
            return was_deleted
        except ValueError as ve:
            print(str(ve))
        return False

    def update_task(self, task_id: str, text: str) -> bool:
        try:
            actual_id = int(task_id)  # DRY!
            self.ensure_database()
            cur = self.conn.cursor()
            cur.execute(
                "update chronotrak set message=? where rowid=?",
                (text, actual_id))
            self.conn.commit()
            was_updated = cur.rowcount == 1
            cur.close()
            return was_updated
        except ValueError as ve:
            print(str(ve))
        return False

    def stop_task(self, task_id: str) -> bool:
        try:
            actual_id = int(task_id)  # DRY!
            self.ensure_database()
            cur = self.conn.cursor()
            cur.execute(
                "update chronotrak set status=0 where rowid=?",
                (actual_id, ))
            self.conn.commit()
            was_updated = cur.rowcount == 1
            cur.close()
            return was_updated
        except ValueError as ve:
            print(str(ve))
        return False



# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
#
#                              COMMANDS
#
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

class Command:
    """Simple command base class to manage the various options"""
    def __init__(self, args: List[str]=[]):
        self.args = args
        self.db = DB()

    @staticmethod  # classic factory pattern ftw
    def parse(args: List[str]) -> 'Command':
        if len(args) > 0:
            command = args.pop(0).lower()
            #print("COMMAND:", command)
            #print(args)
            if 'list' == command:
                return ListCommand()
            elif 'create' == command:
                return CreateCommand(args)
            elif 'update' == command:
                return UpdateCommand(args)
            elif 'delete' == command:
                return DeleteCommand(args)
            elif 'stop' == command:
                return StopCommand(args)
        return HelpCommand()

    def run(self):
        raise RuntimeError("Subclass must implement run()")


# ---------------------------------------------------------------------------
#                              CREATE
# ---------------------------------------------------------------------------

class CreateCommand(Command):
    """Creates a new entry in the task timer table.

    The date has the current time, is set as running and we take everything
    after the command as text to be formed as the message entry.
    """
    def __init__(self, args):
        super(CreateCommand, self).__init__(args)

    def run(self):
        text = " ".join(self.args)
        new_id = self.db.create_task(text)
        if new_id is not None:
            print("Created! ID is", new_id)
        else:
            print("It was not possible to create that entry")


# ---------------------------------------------------------------------------
#                              UPDATE
# ---------------------------------------------------------------------------

class UpdateCommand(Command):
    def __init__(self, args):
        super(UpdateCommand, self).__init__(args)

    def run(self):
        if len(self.args):
            update_id = self.args.pop(0)
            new_text = " ".join(self.args)
            if self.db.update_task(update_id, new_text):
                print(f"Entry updated OK")
            else:
                print(f"Entry {update_id} not updated, check ID!")


# ---------------------------------------------------------------------------
#                              STOP
# ---------------------------------------------------------------------------

class StopCommand(Command):
    def __init__(self, args):
        super(StopCommand, self).__init__(args)

    def run(self):
        if len(self.args):
            stop_id = self.args.pop(0)
            if self.db.stop_task(stop_id):
                print(f"Entry stopped OK")
            else:
                print(f"Entry {stop_id} not stopped, check ID!")


# ---------------------------------------------------------------------------
#                              DELETE
# ---------------------------------------------------------------------------

class DeleteCommand(Command):
    def __init__(self, args):
        super(DeleteCommand, self).__init__(args)

    def run(self):
        if len(self.args):
            kill_id = self.args.pop(0)
            if self.db.kill_task(kill_id):
                print("Entry deleted OK")
            else:
                print(f"Entry {kill_id} not deleted, check ID!")
        else:
            print("Please supply an ID")


# ---------------------------------------------------------------------------
#                              LIST
# ---------------------------------------------------------------------------

class ListCommand(Command):
    """List all currently stored time tracker entries"""
    def __init__(self):
        super(ListCommand, self).__init__()

    def run(self):
        tasks = self.db.get_tasks()
        if len(tasks) > 0:
            print()
            print(" id      run?    started              Duration  message")
            print("-------------------------------------------------------")
            for rowid, text, status, started_at, stopped_at in tasks:
                if stopped_at:
                    end_time = stopped_at
                else:
                    end_time = datetime.now()
                if status:
                    mode = 'YES'
                else:
                    mode = 'NO'
                # running: show the elapsed time so far as hours, mins
                duration = (end_time - started_at).total_seconds()
                elapsed = datetime.fromtimestamp(duration)
                delta = datetime.strftime(elapsed, "%H:%M")
                start = datetime.strftime(started_at, "%Y/%m/%d %H:%M:%S")
                print(f"({rowid:4})   {mode:^4}    {start:16}  {delta:5}     {text}")
        else:
            print("No tasks to display at this time, use 'start'!")
        print()


# ---------------------------------------------------------------------------
#                              HELP
# ---------------------------------------------------------------------------

class HelpCommand(Command):
    def __init__(self):
        super(HelpCommand, self).__init__()

    def run(self):
        print("""\nUsage :- chronotrak [COMMAND] arg1 arg2 ..argN

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
        """)


    # -----------------------------------------------------------------------
    # Main command line entry point for ChronoTrak.
    #
    # If no commands are given we display a simple command help
    # output and terminate. If a command is given we attempt to
    # interpret and execute it.
    #
    # Iff a valid command is given, we will check that the required
    # database is present in the current working directory and if
    # not, a default empty database is created.
    #
    # This means that placing this script in the 'path' (whatever
    # that means for your operating system!) will allow ChronoTrak
    # to be used in any project folder.
    #
if __name__ == "__main__":
    # drop application name
    cmd = Command.parse(sys.argv[1:])
    cmd.run()
