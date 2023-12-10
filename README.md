# AirBnB Clone - The Console

**Project:** 0x00. AirBnB Clone - The Console  
**Team Members:** Mohamed Amyne Boutallaght, Abdelhamid Maaira

Welcome to the AirBnB Clone project! This project is the initial step toward constructing a full web application that replicates Airbnb's functionality. In this phase, we will create a command-line interface (CLI) known as "The Console," allowing us to manage AirBnB objects using various commands.

## Background Context

The primary objective of this project is to impart essential concepts in Python, covering a diverse range of topics, such as:

- Utilization of Python packages and modules
- Implementation of Object-Oriented Programming (OOP) principles
- Development of a command-line interface (CLI) for streamlined interaction
- Mastery of serialization and deserialization techniques for efficient data handling
- Proficiency in conducting unit testing through the utilization of the unittest framework

The overarching goal is to replicate fundamental functionalities of Airbnb. This involves the creation of classes that accurately represent distinct components within the application, effective management of object serialization and deserialization processes, and the provision of a user-friendly command-line interface for seamless interaction with these objects.

## Setup Instructions

- Follow these steps to set up the project:

1. Clone the repository using the following command:
  ```
  git clone https://github.com/Yamix27/AirBnB_clone.git
  ```
2. Move into the project directory:
  ```
  cd AirBnB_clone
  ```
3. Launch the console by running:
  ```
  ./console.py
  ```

## Usage

Upon launching the console, you have the capability to initiate various commands for the management of your AirBnB objects. To access a comprehensive list of available commands, simply input `help` or `help <command>`, providing you with detailed information about a specific command.

## Commands

The console provides the following commands:

- `create`: Initiates the creation of a new instance of a class and saves it to a JSON file.
- `show`: Displays the string representation of a particular instance.
- `destroy`: Deletes an instance based on the class name and ID.
- `all`: Shows all instances of a class or all instances stored in the storage.
- `update`: Facilitates the modification of attributes for a specific instance.


For a comprehensive list of available commands, consult the built-in `help` feature within the console.

## File Structure

The project's file organization is structured as follows:

- `console.py`: The primary command-line interface (CLI) script.
- `models/`: Directory encompassing class definitions for various AirBnB objects.
- `models/engine/`: Directory holding the implementation of the storage engine.
- `tests/`: Directory comprising unit tests for the project.

## Contributors

- [Mohamed Amyne Boutallaght](https://github.com/Yamix27/)
- [Abdelhamid Maaira](https://github.com/Hmddev23/)

## License

This project is governed by the [MIT License](LICENSE).