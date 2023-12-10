#!/usr/bin/python3
"""
console.py

This module serves as the entry point for
the command interpreter of the AirBnB clone project.
The HBNBCommand class defines the command interpreter,
enabling users to interact with the project's objects.

Usage:
python3 console.py
"""

import cmd
import re
from shlex import split

from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.city import City
from models.place import Place
from models import storage


def parse_arguments(arg):
    braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            segment = split(arg[: brackets.span()[0]])
            ret_lt = [i.strip(",") for i in segment]
            ret_lt.append(brackets.group())
            return ret_lt
    else:
        segment = split(arg[: braces.span()[0]])
        ret_lt = [i.strip(",") for i in segment]
        ret_lt.append(braces.group())
        return ret_lt


class HBNBCommand(cmd.Cmd):
    """
    The entry point for the command interpreter class for the AirBnB clone project.
    """

    prompt = '(hbnb) '
    classes = {
        'BaseModel',
        'User',
        'Amenity',
        'Review',
        'State',
        'City',
        'Place',
    }

    def default(self, line):
        """Default behavior for the cmd module when processing input"""
        cmd_args = {
            "show": self.show_instance,
            "count": self.count_instance,
            "update": self.update_instance,
            "all": self.all_instance,
            "destroy": self.destroy_instance
        }
        match = re.search(r"\.", line)
        if match is not None:
            cmd_arg_list = [line[: match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", cmd_arg_list[1])
            if match is not None:
                cmd = [cmd_arg_list[1][: match.span()[0]], match.group()[1:-1]]
                if cmd[0] in cmd_args.keys():
                    call = "{} {}".format(
                        cmd_arg_list[0], cmd[1]
                    )
                    return cmd_args[cmd[0]](call)
        print("*** Unknown syntax: {}".format(line))

    def create_instance(self, line):
        """
        Generates a new instance of BaseModel,
        saves it to the JSON file, and displays the ID.
        Example: $ create BaseModel
        """
        arguments = parse_arguments(line)
        if not arguments:
            print("** class name missing **")
            return
        try:
            new_inst_cls = globals()[arguments[0]]
            new_inst = new_inst_cls()
            new_inst.save()
            print(new_inst.id)
        except Exception:
            print("** class doesn't exist **")
        return

    def show_instance(self, line):
        """
        Displays the string representation of
        an instance identified by the class name and ID.
        Example: $ show BaseModel 1111-2222-3333
        """
        arguments = parse_arguments(line)
        if not arguments:
            print("** class name missing **")
            return
        class_name = arguments[0]
        try:
            cls = globals()[class_name]
        except Exception:
            print(f"** class doesn't exist **")
            return
        if len(arguments) < 2:
            print("** instance id missing **")
            return
        inst_id = arguments[1]
        key = f"{class_name}.{inst_id}"
        try:
            res = storage.all().get(key)
            if res is None:
                print("** no instance found **")
            else:
                print(res)
        except Exception:
            pass

    def quit_instance(self, line):
        """Quit command to exit the cmd module"""
        return True

if __name__ == "__main__":
    HBNBCommand().cmdloop()
