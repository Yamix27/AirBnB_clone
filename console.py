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
from models.__init__ import storage


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
    The entry point for the command interpreter class for
    the AirBnB clone project.
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
        Generates a new instance of a given class,
        saves it to the JSON file, and displays the ID.
        Example: $ create BaseModel
        """
        if line == '':
            print('** class name missing **')
        elif line not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        else:
            if line == 'BaseModel':
                obj = BaseModel()
            elif line == 'User':
                obj = User()
            elif line == 'Place':
                obj = Place()
            elif line == 'State':
                obj = State()
            elif line == 'City':
                obj = City()
            elif line == 'Amenity':
                obj = Amenity()
            elif line == 'Review':
                obj = Review()
            storage.save()
            print(obj.id)

    def show_instance(self, line):
        """
        Displays the string representation of
        an instance identified by the class name and ID.
        Example: $ show BaseModel 1111-2222-3333
        """
        arguments = line.split()
        if line == '':
            print('** class name missing **')
        elif arguments[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        else:
            if len(arguments) < 2:
                print('** instance id missing **')
            else:
                class_name = arguments[0]
                inst_id = arguments[1]
                key = class_name + '.' + inst_id
                try:
                    print(storage.all()[key])
                except KeyError:
                    print('** no instance found **')

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

    def update_instance(self, line):
        """
        Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Updates a class instance identified by ID by adding or modifying
        the specified attribute key/value pair or dictionary.
        """
        arguments = line.split()
        
        if not line:
            print('** class name missing **')
        elif arguments[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        elif len(arguments) < 2:
            print('** instance id missing **')
        elif len(arguments) < 3:
            print('** attribute name missing **')
        elif len(arguments) < 4:
            print('** value missing **')
        else:
            class_name, objid, attr, value = arguments[:4]
            objAttr = ['id', 'created_at', 'updated_at']
            
            if attr in objAttr:
                print('** attribute can\'t be updated **')
                return

            if (value[0] == '"' and value[-1] == '"') or value[0] == "'":
                if value[0] != '"':
                    print("** A string argument must be between double quotes **")
                    return
                value = value[1:-1]
            else:
                try:
                    for c in value:
                        if c == '.':
                            value = float(value)
                            break
                    else:
                        value = int(value)
                except ValueError:
                    print("** The value must be a string, int, or float **")
                    return

            if (attr[0] == '"' and attr[-1] == '"') or attr[0] == "'" or attr[-1] == "'":
                if attr[0] != '"' or attr[-1] == "'":
                    print("** The attribute name must be between double quotes **")
                    return
                attr = attr[1:-1]
            
            key = f"{class_name}.{objid}"
            try:
                instance = storage.all()[key]
                setattr(instance, attr, value)
                instance.save()
            except KeyError:
                print('** no instance found **')

    def all_instance(self, line):
        """
        Usage: all or all <class> or <class>.all()
        Displays string representations of all instances
        of a specified class.
        If no class is specified, it shows representations
        of all instantiated objects.
        """
        arguments = line.split()
        obj_line = []
        if len(arguments) != 0:
            if arguments[0] not in HBNBCommand.classes:
                print('** class doesn\'t exist **')
                return
            else:
                for key, value in storage.all().items():
                    if type(value).__name__ == arguments[0]:
                        obj_line.append(value.__str__())
        else:
            for key, value in storage.all().items():
                obj_line.append(value.__str__())
        print(obj_line)

    def destroy_instance(self, line):
        """
        Deletes an instance based on the class name and ID
        (saves the change to the JSON file).
        Example: $ destroy BaseModel 1111-2222-3333.
        """
        arguments = line.split()
        if line == '':
            print('** class name missing **')
        elif arguments[0] not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
        else:
            if len(arguments) < 2:
                print('** instance id missing **')
            else:
                class_name = arguments[0]
                objid = arguments[1]
                key = class_name + '.' + objid
                try:
                    del storage.all()[key]
                    storage.save()
                except KeyError:
                    print('** no instance found **')

    def quit_instance(self, line):
        """Quit command to exit from cmd"""
        return True

    def blank_line_instance(self):
        """Handles blank lines."""
        pass

    def EOF_instance(self, line):
        """Ctrl D - to kill the program or exit from cmd"""
        print()
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
