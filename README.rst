########################################
SoftToken OTP
########################################

SoftToken OTP is an application to generate One-Time-Passwords to be used as a
second factor authentication mechanism.
It can either print it when executed in the commandline or type it wherever
your focus is. This can be especially useful when assigning a keybind to use
your token.

.. class:: no-web no-pdf


.. contents::

.. section-numbering::

.. raw:: pdf

   PageBreak oneColumn


=============
Main features
=============

* Generate Time-Based One-Time Passwords
* Multiple tokens support
* Print OTP wherever the focus is (useful for keybindings)

=============
Usage
=============

Create a new token:

.. code-block:: bash

	$ softtoken --new -t token1 --hash sha256 --digits 6

	New Token created:

	token1
	-------------
	Seed (hex): 337ad0410038666829c6446448d0a0d851938193
	Seed (b32): GN5NAQIAHBTGQKOGIRSERUFA3BIZHAMT

Delete a token:

.. code-block:: bash

	$ softtoken --delete -t token1
	Token token1 successfully deleted

List tokens:

.. code-block:: bash

	$ softtoken --list
	[*] token1
	[*] token2
	[*] token3
	[*] token4
	[*] token5

Generate an OTP:

.. code-block:: bash

	$ softtoken -t token1
	630567

Generate an OTP and get it wherever your focus is:

.. code-block:: bash

	$ softtoken -t token1 -X
	630567

Generate an OTP and copy to clipboard (requires xclip):

.. code-block:: bash

	$ softtoken -t token1 -C

=============
TODO
=============

* Add HOTP support
* Parametrize TOTP time
