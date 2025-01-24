=====
Stats
=====

Every character has a unique set of stats, including health, attack, defense, and speed.

Health
------

.. image:: ./_static/images/hp_bar_7.png
   :width: 175
   :align: center

Health... represents how healthy a character is. What did you expect? The health will be represented by a character's
``current_health`` over their ``max_health``, such as ``current_health/max_health``.

Attack Stat
-----------

.. image:: ./_static/images/attack_buff.png
   :width: 90
   :align: center

Attack is the amount of base damage a character can deal when using an Attack Move without any modifiers.
Essentially, it is the strength of the character, reflected by an integer between 0 and 100.

For example, if the attack stat is 50, the character will attempt to deal 50 points of damage to the target.

To access a character's attack stat, you can do the following:

Defense Stat
------------

.. image:: ./_static/images/defense_buff.png
   :width: 90
   :align: center

Defense is a percentage of the amount of damage a character can prevent from taking from an Attack, represented by an
integer between 0 - 100.

For example, if the defense stat is 50, and the incoming damage is 50, the character will prevent 50% of the damage
and take 25 points of damage.

Speed Stat
----------

.. image:: ./_static/images/speed_buff.png
   :width: 90
   :align: center

Speed is the stat that determines the order of your team and who gets to act first each turn. Visit
:doc:`game_logic` for more details about turn order
how the speed stat affects it.

Accessing a Character's Stats
---------------------------------

Here is how you can access any of a character's stats:

.. code-block::

    character.current_health
    character.max_health
    character.attack
    character.defense
    character.speed

Here is how you can access the base values (what the original stat of the character's stat is; this is static)
and the modified values (the value that will constantly change with stat buffs and debuffs) of the attack,
defense, and speed stats:

Accessing the base values:

.. code-block::

    character.attack.base_value
    character.defense.base_value
    character.speed.base_value

Accessing the modified values:

.. code-block::

    character.attack.value
    character.defense.value
    character.speed.value

Comparing Stats
---------------

It may be useful to compare stats to others, and you can easily do so! You can treat the attack, defense, and speed
stats like regular integers. You can also compare any stat with any stat (e.g., attack == speed). You can perform the
following comparisons below with any of the stats. These are just a few examples:

.. code-block::

    character.attack == other_character.attack
    character.defense == other_character.defense
    character.speed == other_character.speed

    character.attack > other_character.defense
    character.speed >= other_character.defense

    character.defense < other_character.attack
    character.speed <= other_character.attack

    character.speed != other_character.attack
