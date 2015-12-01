TMB
===

.. image:: https://travis-ci.org/tdf/tmb.svg?branch=master
    :target: https://travis-ci.org/tdf/tmb

.. image:: https://coveralls.io/repos/tdf/tmb/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/tdf/tmb?branch=master


TMB is a Telegram Bot to send monitoring notifications, typically from an Icinga or Nagios installation to Telegram users.

Installation
------------

For the moment, TMB is not available in the Python Package Index, so you have to use github as source.
TMB requires Python 3 and uses some advanced features for concurrent programming from the great asyncio lib, so at least Python 3.4 is needed.

To install directly from github, first install pip, git and then run this command as root:

.. code-block:: bash

    pip3 install git+git://github.com/tdf/tmb@master


Configuration
-------------

First of all, talk to `Botfather <https://telegram.me/BotFather>`_. Start creating a new bot by issuing the command ``/newbot`` and following the instructions.

Create the file ``~/.config/tmb/tmb.ini`` that will hold the configuration, with the following contents:

.. code-block:: ini

    [global]
    host = 127.0.0.1
    port = 64321
    password = changeme #replace by the password required to register at your bot
    token = invalid #replace by the token you got from BotFather

Next is to run the ``tmb`` command, and thats it!


Usage
-----

Tell your users to talk to the Bot you've just created, you can also send them links to ``https://telegram.me/YourBotName``. They should use the ``/register`` command and then send the password needed for registration

To send notifications to your registered users, use nc as follows:

.. code-block:: bash

    /bin/echo -e "$NOTIFICATIONTYPE$\nHost: $HOSTALIAS$\nService: $SERVICEDESC$\nState: $SERVICESTATE$\nInfo: $SERVICEOUTPUT$" | nc localhost 64321
