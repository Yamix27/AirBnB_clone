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
import shlex
import ast
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.city import City
from models.place import Place
from models import storage


def clean_update_prompt(inp_arg):
    """
    Splits the curly braces for the update method
    """
    braces = re.search(r"\{(.*?)\}", inp_arg)

    if braces:
        unf_id = shlex.split(inp_arg[:braces.span()[0]])
        id = [i.strip(",") for i in unf_id][0]

        strng_data = braces.group(1)
        try:
            arg_dict = ast.literal_eval("{" + strng_data + "}")
        except Exception:
            print("**  invalid dictionary format **")
            return
        return id, arg_dict
    else:
        commands = inp_arg.split(",")
        if commands:
            try:
                id = commands[0]
            except Exception:
                return "", ""
            try:
                attrib_name = commands[1]
            except Exception:
                return id, ""
            try:
                attrib_value = commands[2]
            except Exception:
                return id, attrib_name
            return f"{id}", f"{attrib_name} {attrib_value}"


class HBNBCommand(cmd.Cmd):
    """
    The entry point for the command interpreter class for
    the AirBnB clone project.
    """

    prompt = '(hbnb) '
    classes = [
        'BaseModel',
        'User',
        'Amenity',
        'Review',
        'State',
        'City',
        'Place'
    ]
    
    def default(self, arg):
        """
        Default behavior for the cmd module when processing input
        """
        arglt = arg.split('.')
        cls_nm = arglt[0]
        cmd = arglt[1].split('(')
        command_md = cmd[0]
        inp_arg = cmd[1].split(')')[0]

        cmd_args = {
            'all': self.do_all,
            'show': self.do_show,
            'destroy': self.do_destroy,
            'update': self.do_update,
            'count': self.do_count
        }

        if command_md in cmd_args.keys():
            if command_md != "update":
                return cmd_args[command_md]("{} {}".format(cls_nm, inp_arg))
            else:
                if not cls_nm:
                    print("** class name missing **")
                    return
                try:
                    obj_id, arg_dict = clean_update_prompt(inp_arg)
                except Exception:
                    pass
                try:
                    call = cmd_args[command_md]
                    return call("{} {} {}".format(cls_nm, obj_id, arg_dict))
                except Exception:
                    pass
        else:
            print("*** Unknown syntax: {}".format(arg))
            return False

    def do_create(self, arg):
        """
        Generates a new instance of a given class,
        saves it to the JSON file, and displays the ID.
        Example: $ create BaseModel
        """
        command_prompts = shlex.split(arg)

        if len(command_prompts) == 0:
            print("** class name missing **")
        elif command_prompts[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{command_prompts[0]}()")
            storage.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Displays the string representation of
        an instance identified by the class name and ID.
        Example: $ show BaseModel 1111-2222-3333
        """
        command_prompts = shlex.split(arg)

        if len(command_prompts) == 0:
            print("** class name missing **")
        elif command_prompts[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(command_prompts) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(command_prompts[0], command_prompts[1])
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_count(self, arg):
        """
        Usage: count <class> or <class>.count()
        Returns the count of instances for a specified class.
        """
        objcs = storage.all()
        command_prompts = shlex.split(arg)

        if arg:
            class_nm = command_prompts[0]

        count = 0

        if command_prompts:
            if class_nm in self.valid_classes:
                for obj in objcs.values():
                    if obj.__class__.__name__ == class_nm:
                        count += 1
                print(count)
            else:
                print("** invalid class name **")
        else:
            print("** class name missing **")

    def do_update(self, arg):
        """
        Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Updates a class instance identified by ID by adding or modifying
        the specified attribute key/value pair or dictionary.
        """
        command_prompts = shlex.split(arg)

        if len(command_prompts) == 0:
            print("** class name missing **")
        elif command_prompts[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(command_prompts) < 2:
            print("** instance id missing **")
        else:
            objs = storage.all()

            key = "{}.{}".format(command_prompts[0], command_prompts[1])
            if key not in objs:
                print("** no instance found **")
            elif len(command_prompts) < 3:
                print("** attribute name missing **")
            elif len(command_prompts) < 4:
                print("** value missing **")
            else:
                obj = objs[key]
                braces = re.search(r"\{(.*?)\}", arg)

                if braces:
                    try:
                        strng_data = braces.group(1)

                        arg_dict = ast.literal_eval("{" + strng_data + "}")

                        attrib_names = list(arg_dict.keys())
                        attrib_values = list(arg_dict.values())
                        try:
                            attrib_name1 = attrib_names[0]
                            attrib_value1 = attrib_values[0]
                            setattr(obj, attrib_name1, attrib_value1)
                        except Exception:
                            pass
                        try:
                            attrib_name2 = attrib_names[1]
                            attrib_value2 = attrib_values[1]
                            setattr(obj, attrib_name2, attrib_value2)
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:

                    attrib_name = command_prompts[2]
                    attrib_value = command_prompts[3]

                    try:
                        attrib_value = eval(attrib_value)
                    except Exception:
                        pass
                    setattr(obj, attrib_name, attrib_value)

                obj.save()

    def do_all(self, arg):
        """
        Usage: all or all <class> or <class>.all()
        Displays string representations of all instances
        of a specified class.
        If no class is specified, it shows representations
        of all instantiated objects.
        """
        objs = storage.all()
        command_prompts = shlex.split(arg)

        if len(command_prompts) == 0:
            for key, value in objs.items():
                print(str(value))
        elif command_prompts[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, value in objs.items():
                if key.split('.')[0] == command_prompts[0]:
                    print(str(value))

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and ID
        (saves the change to the JSON file).
        Example: $ destroy BaseModel 1111-2222-3333.
        """
        command_prompts = shlex.split(arg)

        if len(command_prompts) == 0:
            print("** class name missing **")
        elif command_prompts[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(command_prompts) < 2:
            print("** instance id missing **")
        else:
            objs = storage.all()
            key = "{}.{}".format(command_prompts[0], command_prompts[1])
            if key in objs:
                del objs[key]
                storage.save()
            else:
                print("** no instance found **")

    def emptyline(self):
        """
        Handles blank lines.
        """
        pass

    def do_EOF(self, arg):
        """
        Ctrl D - to kill the program or exit from cmd.
        """
        return True

    def do_quit(self, arg):
        """
        Quit command to exit from cmd.
        """
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()