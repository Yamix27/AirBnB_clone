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

    def count_instance(self, line):
        """
        Usage: count <class> or <class>.count()
        Returns the count of instances for a specified class.
        """
        arguments = parse_arguments(line)
        counter = 0
        for objct in storage.all().values():
            if arguments[0] == objct.__class__.__name__:
                counter += 1
        print(counter)

    def update_instance(self, arg):
        """
        Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Updates a class instance identified by ID by adding or modifying
        the specified attribute key/value pair or dictionary.
        """
        arguments = parse_arguments(arg)
        object_dict = storage.all()

        if len(arguments) == 0:
            print("** class name missing **")
            return False
        if arguments[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False
        if len(arguments) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arguments[0], arguments[1]) not in object_dict.keys():
            print("** no instance found **")
            return False
        if len(arguments) == 2:
            print("** attribute name missing **")
            return False
        if len(arguments) == 3:
            try:
                type(eval(arguments[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arguments) == 4:
            objct = object_dict["{}.{}".format(arguments[0], arguments[1])]
            if arguments[2] in objct.__class__.__dict__.keys():
                value_type = type(objct.__class__.__dict__[arguments[2]])
                objct.__dict__[arguments[2]] = value_type(arguments[3])
            else:
                objct.__dict__[arguments[2]] = arguments[3]
        elif type(eval(arguments[2])) == dict:
            objct = object_dict["{}.{}".format(arguments[0], arguments[1])]
            for key, val in eval(arguments[2]).items():
                if (key in objct.__class__.__dict__.keys() and
                            type(objct.__class__.__dict__[key]) in {str, int, float}):
                    value_type = type(objct.__class__.__dict__[key])
                    objct.__dict__[key] = value_type(val)
                else:
                    objct.__dict__[key] = val
        storage.save()

    def all_instance(self, line):
        """
        Usage: all or all <class> or <class>.all()
        Displays string representations of all instances of a specified class.
        If no class is specified, it shows representations of all instantiated objects.
        """
        arguments = parse_arguments(line)

        if len(arguments) > 0:
            class_name = arguments[0]
            try:
                cls = globals()[class_name]
            except KeyError:
                print("** class doesn't exist **")
                return
        else:
            class_name = None

        obj_line = []

        for objct in storage.all().values():
            if class_name is None or isinstance(objct, cls):
                obj_line.append(objct.__str__())

        print(obj_line)

    def destroy_instance(self, line):
        """
        Deletes an instance based on the class name and ID
        (saves the change to the JSON file).
        Example: $ destroy BaseModel 1111-2222-3333.
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
            data_k = storage.all().get(key)
            if data_k is None:
                print("** no instance found **")
                return
            else:
                result = storage.all()
                del result[key]
                storage.save()
        except Exception:
            pass

    def quit_instance(self, line):
        """Quit command to exit from cmd"""
        return True

    def blank_line_instance(self):
        """Handles blank lines."""
        pass

    def EOF_instance(self, line):
        """Ctrl D - to kill the program or exit from cmd"""
        print("")
        return True

if __name__ == "__main__":
    HBNBCommand().cmdloop()
