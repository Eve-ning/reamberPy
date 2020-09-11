####
APIs
####

This provides a neat wrapper to access popular game APIs without having to deal with boilercode.

.. toctree::
   :maxdepth: 1

   osu! API <api/OsuAPI>

*******************
Setting Up cfg_path
*******************

For security purposes, keys, tokens, ids shouldn't be leaked as they can compromise your authenticity.

This is why you shouldn't hardcode them into the code, and should put them in a separate folder.

In Python, there's a library called ``ConfigParser``. It is able to read a specific file format, and allow you to
extract information.

Consider the following ``(api.ini)`` ::

   [API]
   id = 1234
   secret = abcd
   token = AbcD
   key = ABCD

This is a valid format for the API constructors to use, e.g. ``OsuAPIV1.fromCfg(cfg_path="api.ini")``.

