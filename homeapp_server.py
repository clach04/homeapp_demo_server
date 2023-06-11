#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
# homeapp_server - SimpleHome API demo server
# Copyright (C) 2023  Chris Clark
#
# Python 3.x and 2.x script

try:
    # Python 3.8 and later
    # py3
    from html import escape as escapecgi
except ImportError:
    # py2
    from cgi import escape as escapecgi

try:
    # Python 2.6+
    import json
except ImportError:
    # from http://code.google.com/p/simplejson
    import simplejson as json

import datetime
import os
import sys


try:
    if os.environ.get('FORCE_DIETCHERRYPY'):
        # disable cherrypy usage
        raise ImportError()
    import cherrypy
    dietcherrypy_wsgi = dietcherrypy = None
except ImportError:
    # Try DietCherryPy - https://hg.sr.ht/~clach04/dietcherrypy/
    try:
        import dietcherrypy_wsgi
        dietcherrypy = cherrypy = dietcherrypy_wsgi
    except ImportError:
        import dietcherrypy
        cherrypy = dietcherrypy
        dietcherrypy_wsgi = None


class Root(object):
    def index(self):
        return '''Nothing to see here, see /commands
        <a href="./commands">/commands</a>
        '''
    index.exposed = True

    def commands(self):
        # See https://github.com/Domi04151309/HomeApp/wiki/SimpleHome-API
        commands_dict = {
            "commands": {
                "example": {
                    "title": "Title of the command",
                    "summary": "Summary of the command",
                    "icon": "display",
                    "mode": "action"
                    # NOTE mode will default to action if omitted
                },
                "mode_missing": {
                    "title": "Mode Missing",
                    "summary": "should default to action",
                    "icon": "display",
                    # NOTE mode will default to action if omitted
                },
                "mode_switch": {
                    "title": "Mode Switch",
                    "summary": "Toggle",
                    "icon": "display",
                    "mode": "switch"
                },
                "mode_input": {
                    "title": "Mode Input",
                    "summary": "Prompt user for input",
                    "icon": "display",
                    "mode": "input"
                },
                "mode_none": {
                    "title": "Mode none",
                    "summary": "DateTime %s" % datetime.datetime.now(),
                    "icon": "display",
                    "mode": "none"
                },
                "mode_none_refresh": {
                    "title": "Mode none refresh",
                    "summary": "DateTime %s" % datetime.datetime.now(),
                    "icon": "display",
                    "mode": "none"
                },
            }
        }
        return json.dumps(commands_dict)  # optionally make pretty for debugging with indent=4
    commands.exposed = True

    def example(self, input=None):
        # from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66062
        this_function_name = sys._getframe().f_code.co_name
        msg = '%s called' % this_function_name
        if input:
            msg += ' - input=%r' % input
        print('%s' % msg)
        return json.dumps({'toast': msg})
    example.exposed = True

    def mode_missing(self, input=None):
        # from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66062
        this_function_name = sys._getframe().f_code.co_name
        msg = '%s called' % this_function_name
        if input:
            msg += ' - input=%r' % input
        print('%s' % msg)
        return json.dumps({'toast': msg})
    mode_missing.exposed = True

    def mode_switch(self, input=None):
        # from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66062
        this_function_name = sys._getframe().f_code.co_name
        msg = '%s called' % this_function_name
        if input:
            msg += ' - input=%r' % input
        print('%s' % msg)
        return json.dumps({'toast': msg})
    mode_switch.exposed = True

    def mode_input(self, input=None):
        # from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66062
        this_function_name = sys._getframe().f_code.co_name
        msg = '%s called' % this_function_name
        if input:
            msg += ' - input=%r' % input
        print('%s' % msg)
        return json.dumps({'toast': msg})
    mode_input.exposed = True

    def mode_none(self, input=None):
        # from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66062
        this_function_name = sys._getframe().f_code.co_name
        msg = '%s called' % this_function_name
        if input:
            msg += ' - input=%r' % input
        msg += ' - now=%r' % str(datetime.datetime.now())
        print('%s' % msg)
        return json.dumps({'toast': msg})
    mode_none.exposed = True

    def mode_none_refresh(self, input=None):
        # from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66062
        this_function_name = sys._getframe().f_code.co_name
        msg = '%s called' % this_function_name
        if input:
            msg += ' - input=%r' % input
        msg += ' - now=%r' %str( datetime.datetime.now())
        print('%s' % msg)
        return json.dumps({'toast': msg, "refresh": True})
    mode_none_refresh.exposed = True


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if not os.getenv('SCRIPT_NAME'):
        # We're NOT running under CGI
        print('Python %s on %s' % (sys.version, sys.platform))
        print('cherrypy.__version__', cherrypy.__version__)

    server_port = int(os.environ.get('HTTP_PORT', 7777))
    socket_host = '0.0.0.0'  # allow access from any client
    print('http://localhost:%d/' % server_port)

    """
    ## cherrypy v3 quickstart (no call backs allowed, need to thread locally)
    #cherrypy.quickstart(Root(form, self._webform_callback))
    
    ### cherrypy 3.0.2 does NOT have server.start_with_callback it is engine..?
    cherrypy.config.update({'server.socketPort':server_port})
    cherrypy.engine.start_with_callback(webbrowser.open, ('http://localhost:%d'%server_port,))
    """
    ### cherrypy 2.?.? (and dietcherrypy)
    #cherrypy.config.update({'server.socketPort': server_port}) # maybe a 3.0 thing?
    cherrypy.config.update({'server.socket_port': server_port, 'server.socket_host': socket_host})  # CherryPy 3.1.2
    mywebapp = Root()

    """
    ## CherryPy version 2.x.x style
    root = SimpleWeb()
    server.start()
    """
    
    ## CherryPy version 3.x style
    cherrypy.quickstart(Root())

    return 0


if __name__ == "__main__":
    sys.exit(main())
