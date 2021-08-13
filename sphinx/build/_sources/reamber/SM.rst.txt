#########
StepMania
#########

********
Examples
********

1. Read and Write
=================

.. code-block:: python

    from reamber.sm.SMMapSet import SMMapSet
    sms = SMMapSet.read_file("file.sm")
    sms.write_file("file_out.sm")

2. Print all Mine Offsets from First Difficulty
===============================================

.. code-block:: python

    from reamber.sm.SMMapSet import SMMapSet
    sms = SMMapSet.read_file("file.sm")
    print(sms[0].mines.offset)

3. Swap Col 2 with 3 for First Difficulty
=========================================

.. code-block:: python

    from reamber.sm.SMMapSet import SMMapSet
    sms = SMMapSet.read_file("file.sm")
    sm = sms[0]
    stack = sm.stack()

    # Assign 2 to temporary column -1
    stack.loc[stack.column == 2, 'column'] = -1

    # Replace 3 with 2
    stack.loc[stack.column == 3, 'column'] = 2

    # Replace 2 with 3
    stack.loc[stack.column == 2, 'column'] = 3
