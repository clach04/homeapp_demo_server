# homeapp_demo_server

Demo SimpleHome-API in Python for https://github.com/Domi04151309/HomeApp/wiki/SimpleHome-API

Works with Android app HomeApp.

Observations

  * HomeApp refreshes every 1 second
      * But does not update Title/Description, until refresh toast returned from an action
  * Mode None type actions/events are never "called"
  
## Setup

Install CherryPy (or DietCherryPy):

    pip install cherrypy

To run:

    python homeapp_server.py

Which will start listening on port 7777.
To override port, set operating system variable `HTTP_PORT`.
Example:

Linux/Unix:

    env HTTP_PORT=1234 python homeapp_server.py

Windows:

    set HTTP_PORT=1234
    python homeapp_server.py
