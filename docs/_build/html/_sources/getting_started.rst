===============
Getting Started
===============

.. raw:: html

    <style> .purple {color:#A020F0; font-weight:bold; font-size:16px} </style>
    <style> .gold {color:#D4AF37; font-weight:bold; font-size:16px} </style>

.. role:: purple
.. role:: gold

TAKE HEED
=========

Please run the following command to install the necessary packages to run the game:

.. code-block:: console

    pip install -r requirements.txt

More useful commands are listed in :doc:`useful_commands`.

Objective
=========

Your objective is to create the perfect team of three mercenaries to defeat your opponents within 400 turns and claim
victory over the battle. Your team will consist of two generic soldiers and one leader. Each character as a special set
of moves, including three actions that they may use on their turn. Some of these actions may cost some special points to
use, which is gathered by using their standard move. Each character will also have their own stats, including their
max health, attack, speed, and defense.

You can find more information on :doc:`characters`, as well as :doc:`stats` and :doc:`moves` in their respective docs.

Tournament Structure
====================

Each pairing of teams will have two games against each other. After one game, both teams will switch countries
affiliations (i.e., if first with :purple:`Turpis`, will next be :gold:`Uroda`). The points gained from both
games will be added to those teams' total points in the tournament.

For more information on tournament structure and scoring, please visit :doc:`scoring`.

Running the Game
================


Python Version
--------------

Make sure to uninstall the visual studio version of python if you have visual studio installed.
You can do this by re-running the installer and unselecting the python development kit then clicking update.

:gold:`We require using Python version 3.12.` You can go to the
`official Python website <https://www.python.org/downloads/release/python-3125/>`_ to download it.

You can use any text editor or IDE for this competition, but we recommend Visual Studio Code.

Getting the Code and your Team
------------------------------

To receive the code and to begin commanding your own team of mercenaries, please clone the repository
`here <https://github.com/acm-ndsu/Byte-le-2025-Client-Package>`_.

When on GitHub, press the green ``<> Code`` button to drop down the menu:

We highly recommend cloning with GitHub Desktop or downloading the ZIP folder.

#. Open with GitHub Desktop
    * Allow the website to open GitHub Desktop if you have it downloaded already
    * Once in GitHub Desktop, the URL to the repository will be provided
    * Choose where you'd like it saved on your device
    * Click ``Clone`` and you're good to go!

#. Download ZIP
    * Click ``Download ZIP`` and find it in your Downloads.
    * Extract the files and save it some where on your device.
    * Use your IDE/text editor (Visual Studio Code is recommended) of choice and open the extracted folder downloaded.
    * You're ready to code!


Submitting Code
---------------

To submit your code, command your team in either your ``base_client.py`` or ``base_client_2.py`` files. When you submit
your code via the command specified in :doc:`server`, you can submit either of these files if you choose to.


Submitting Issues
-----------------

If you run into issues with the game, please submit an issue to the discord in the bugs channel or call a developer
over!

