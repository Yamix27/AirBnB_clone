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
            lexer = split(arg[: brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[: braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(braces.group())
        return retl


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
            "show": self.do_show,
            "count": self.do_count,
            "update": self.do_update,
            "all": self.do_all,
            "destroy": self.do_destroy,
        }
        match = re.search(r"\.", line)
        if match is not None:
            arg_list = [line[: match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_list[1])
            if match is not None:
                cmd = [arg_list[1][: match.span()[0]], match.group()[1:-1]]
                if cmd[0] in cmd_args.keys():
                    call = "{} {}".format(
                        arg_list[0], cmd[1]
                    )
                    return cmd_args[cmd[0]](call)
        print("*** Unknown syntax: {}".format(line))


if __name__ == "__main__":
    HBNBCommand().cmdloop()
