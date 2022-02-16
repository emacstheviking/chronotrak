import os
from datetime import datetime

from unittest import TestCase

from chronotrak import (
    DB,
    Command,
    CreateCommand,
    HelpCommand,
    ListCommand
)


class TestCommandParsing(TestCase):
    def test_parse_unknown_command_returns(self):
        command = Command.parse(["huh?", "what's this?"])
        self.assertIsInstance(command, HelpCommand)

    def test_parse_list_command(self):
        command = Command.parse(["list", "ignored!"])
        self.assertIsInstance(command, ListCommand)

    def test_parse_create_command(self):
        command = Command.parse(["create", "an", "entry"])
        self.assertIsInstance(command, CreateCommand)

    #  etc etc for commands

TEST_DB = "testdatabase.db"

class TestDatabaseWrapper(TestCase):
    def setUp(self):
        DB.DB_NAME = TEST_DB
        # remove test database, forces new database every test
        if os.path.isfile(TEST_DB):
            os.remove(TEST_DB)
        self.db = DB()

    def test_insert_a_new_entry(self):
        tasks = self.db.get_tasks()
        self.assertEqual(0, len(tasks))
        text = f"test entry {datetime.now()}"
        command = Command.parse(["create", text])
        command.run()
        tasks = self.db.get_tasks()
        self.assertEqual(1, len(tasks))
        # ensure message was correct
        self.assertEqual(text, tasks[0][1])

    def test_insert_entries_delete_one(self):
        command = Command.parse(["create", "test entry 1"])
        command.run()
        command = Command.parse(["create", "test entry 2"])
        command.run()
        command = Command.parse(["create", "test entry 3"])
        command.run()
        tasks = self.db.get_tasks()
        self.assertEqual(3, len(tasks))
        # get ID of the middle row
        dead_id = tasks[1][0]
        command = Command.parse(["delete", str(dead_id)])
        command.run()
        tasks2 = self.db.get_tasks()
        # ensure gone, ensure ID not in list
        self.assertEqual(2, len(tasks2))
        self.assertNotEqual(dead_id, tasks2[0][0])
        self.assertNotEqual(dead_id, tasks2[1][0])

    def test_insert_and_update(self):
        command = Command.parse(["create", "test entry 1"])
        command.run()
        tasks = self.db.get_tasks()
        self.assertEqual(1, len(tasks))
        self.assertEqual('test entry 1', tasks[0][1])
        # update the text
        updated_id = str(tasks[0][0])
        command = Command.parse(["update", updated_id, "test entry 1 *UPDATED*"])
        command.run()
        tasks2 = self.db.get_tasks()
        self.assertEqual('test entry 1 *UPDATED*', tasks2[0][1])
