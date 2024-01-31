# mail.tm
Simple wrapper to interact with the the mail.tm API.

An example of its usage can be found in [example.py](example.py).

(Currently) Available functionalities: 

- Getting the list of available domains.
- Registering a user defined (address, password) pair.
- Registering a randomly generated (address, password) pair.
- Getting the associated bearer token (after registering).
- Fetching the list of received emails.