# QueueTest

[![Build Status](https://img.shields.io/badge/Python-3.9.1-blue)](https://img.shields.io/badge/Python-3.9.1-blue)

As its name suggest, QueueTest is a blockable queue of messages/tasks.
The main objective of QueueTest is to create a list of tasks for asynchronous processing.

The implementation must guarantee that:
- All messages/tasks on QueueTest **must be** processed. (If a thread couldn't process a message, it should go back to the queue)
- A messages/tasks is provided to a single thread on a multithread application. (Multithreads can't get the same message/task to avoid processing waste.)

Queue Behavior/Rules:
- A Queue is initially empty (without any messages)
- On instantiating a Queue, you must choose the max size of it (you can use `0` as infinite size).
- A Queue object must have a `put` method, which inserts a message into the Queue. This method must receive a `str` object as id, an "any type" object as content and an optional `integer` object as insertion timeout.
    - The Id and Content values must be used to create a new QueueMessage object and then, saved into the Queue.
    - A Queue object must raise an `Full` error if the queue is full.
    - If provided, the timeout value must be used to inform how long the Queue object should try to put the message while the queue is full before raising the `Full` error.
    - If an already existing Id is informed, the method should raise the `RepeatedMessage` error.
    - If no value is sent in the Timeout parameter, consider it as `10` (seconds).
    - If an invalid number is sent in the Timeout parameter, it should raise a `ValueError` error.
    - For a better implementation, first check if you should raise `ValueError`. After that you can check if you should raise `RepeatedMessage` error. For last check if you should raise `Full` error.
- A Queue object must have a `qsize` method, which returns the number of messages inside it.
- A Queue object must have a `full` method, which returns if the queue is full or not.
- A Queue object must have a `get` method, which returns a QueueMessage object. This method can receive an optional `integer` object as timeout and a optional `integer` object as acquire_timeout.
    - The timeout value should be used to inform how long the Queue object should try to get the message if the queue is empty before raising the `Empty` error.
    - If no value is sent in the Timeout parameter, consider it as `10` (seconds).
    - The acquire_timeout value should be used to inform how long the thread want to have this object for itself. If another thread tries to get this message after this time, it should be available and not before.
    - If no value is sent in the Acquire Timeout parameter, consider it as `10` (seconds).
    - A Queue object must raise an `Empty` error if the queue is empty.
    - If an invalid number is sent in the Timeout parameter, it should raise a `ValueError` error.
    - For a better implementation, first check if you should raise `ValueError`. After that you can check if you should raise `Empty` error.
- A Queue object must have a `delete` method, which removes the message from the queue. This method must receive an `str` object as id.
    - A Queue object must raise an `DeleteAttemptToUnknownMessage` error if the Id doesn't exists on the queue.
- These are the only public methods that must exists. You can create any number of private methods that you want, as long as you use the prefix `_` to them.

## How to Install? 🤘

The following steps covers the setup process

### Using pyenv with pyenv-virtualenv

You should use virtualenv to build/develop the project and I recommend the use of [pyenv](https://github.com/pyenv/pyenv) with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage multiple python environments.

```bash
pyenv install 3.9.1
pyenv virtualenv 3.9.1 QueueTest
pyenv activate QueueTest
```
### Installing dependencies (Python 3.9.1)

Open your bash and run the follow command to install all the project dependencies, you just need to run the command one time

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
## How to Test? ⚗️

Execute the following command to run tests.

```bash
python -m pytest
```

### Linter

QueueTest uses [black formatting linter](https://github.com/psf/black), the pytest will check the linter usage and will fail if your code isn't respecting it.
