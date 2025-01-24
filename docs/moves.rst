=====
Moves
=====

.. raw:: html

    <style> .red {color:#BC0C25; font-weight:bold; font-size:16px} </style>
    <style> .blue {color:#1769BC; font-weight:bold; font-size:16px} </style>
    <style> .gold {color:#E1C564; font-weight:bold; font-size:16px} </style>
    <style> .green {color:#469B34; font-weight:bold; font-size:16px} </style>
    <style> .cyan {color:#00FFFF; font-weight:bold; font-size:16px} </style>

.. role:: red
.. role:: blue
.. role:: gold
.. role:: green
.. role:: cyan


Moves are how characters fight and interact with each other. A good moveset can make or break a character and team
composition, so pay attention to how they function!

Types of Moves
--------------

There are four (4) types of Moves that a character's Moveset can contain:

================= ========================================================================================
Move Type         Description
================= ========================================================================================
:gold:`Attack`    Deals damage to decrease the target(s)'s health.
:green:`Heal`     Heals the target(s) a set amount to offset damage previously taken.
:red:`Buff`       Increases one of the target(s)'s stats. Good for getting an edge in combat!
:blue:`Debuff`    Decreases one of the target(s)'s stats. Good for putting the opponent at a disadvantage!
================= ========================================================================================


Effects
-------

Some Moves are useful for a character because they have secondary Effects. If a Move has a secondary Effect, the
character is essentially performing two (2) Moves in one turn! Effects fall under the same four (4) categories:

- :gold:`Attack`
- :green:`Heal`
- :red:`Buff`
- :blue:`Debuff`

An Effect can sometimes have a drawback for the user, so be mindful when using a Move with a secondary Effect!


Attack Moves VS Attack Effects
..............................

When it comes to Attack Moves and Attack Effects, they are similar in that they deal damage, but how they deal damage
is different.

- Attack Moves
    - Uses the attacker's Attack stat and the target's Defense stat in the damage formula to return a final value
    - Refer to :doc:`game_logic` for the damage formula

- Attack Effects
    - *Only uses an integer* to deal damage to the target(s)
    - For example, if a Move has an Attack Effect that has 20 damage points, it will deal 20 damage to the
      target(s) regardless of the attacker's Attack stat or target's Defense stat

Special Points
--------------

.. image:: ./_static/images/sp_bar_3.png
   :width: 120
   :align: center

Not all Moves can be used immediately. A character needs to build up the strength to use some moves by increasing
their :cyan:`Special Points`. :cyan:`Special Points` can be gained and lost during a match depending on the Move that's
used. A character can gain a maximum of five (5) :cyan:`Special Points`. How :cyan:`Special Points` are gained and
lost is explained in :ref:`Movesets<movesets>`.


Movesets
--------

.. _movesets:

To contain a character's Moves, they have an attribute called a Moveset. A Moveset will contain 3 Moves that are broken
into three (3) categories:

========================= ==============================================================================================
Moveset Identifier        Description
========================= ==============================================================================================
Normal Move               A character's default Move. By using a Normal Move, a character will gain +1
                          :cyan:`Special Point`.
Special 1                 A Move with some more "oomph" to it. This will *reduce* a character's :cyan:`Special Points`
                          by the cost of the Move.
Special 2                 A Move that tends to be a character's strongest. This will also *reduce* a character's
                          :cyan:`Special Points` by the cost of the Move. *Special 2 is more expensive than Special 1.*
========================= ==============================================================================================

Understanding how a character's Moveset will affect not just the user but all characters on the map will help when
forming a team.

Every character's individual Moveset will be explained in depth in :doc:`characters`.

Accessing a Character's Moveset
...............................

To access a Character's Moveset, you can do the following:

.. code-block::

    character.moveset

When you have access to a Moveset object, if you desire to use it as a dictionary object, you can call the
``as_dict()`` method.

.. code-block::

    moveset_dict = moveset.as_dict()

The structure of a Moveset as a dictionary object is below. Every key is a string, and the value is a Move object.

============ ================================================
Key          Value
============ ================================================
"NM"         The Character's Normal Move object
"S1"         The Character's Special 1 object
"S2"         The Character's Special 2 object
============ ================================================

If an entire dictionary is not necessary, you can simply access an individual Move by using a Character reference and
the following methods:

.. code-block::

    normal_move = character.get_nm()
    special1 = character.get_s1()
    special2 = character.get_s2()


Target Types
------------

When using a Move, the TargetType :doc:`enums` it contains will determine how it behaves. Here is every TargetType
and the target(s) associated with it.

========================== =============================================================================================
TargetType                 Associated Targets
========================== =============================================================================================
TargetType.SELF            The user of the move will be affected
TargetType.ADJACENT_ALLIES Only character's *adjacent* to the user will be affected. This only applies to the user's
                           team, not the opponents
TargetType.ENTIRE_TEAM     *Every* character on the user's team will be affected, regardless of adjacency
TargetType.SINGLE_OPP      The opposing character *across* the user on the game map will be affected
TargetType.ALL_OPPS        *Every* opposing character on the opposing team will be affected
========================== =============================================================================================
