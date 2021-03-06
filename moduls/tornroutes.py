import tornado.web

class route(object):
    """
    decorates RequestHandlers and builds up a list of routables handlers

    Tech Notes (or "What the *@# is really happening here?")
    --------------------------------------------------------

    Everytime @route('...') is called, we instantiate a new route object which
    saves off the passed in URI.  Then, since it's a decorator, the function is
    passed to the route.__call__ method as an argument.  We save a reference to
    that handler with our uri in our class level routes list then return that
    class to be instantiated as normal.

    Later, we can call the classmethod route.get_routes to return that list of
    tuples which can be handed directly to the tornado.web.Application
    instantiation.

    Example
    -------

    ```python
    @route('/some/path')
    class SomeRequestHandler(RequestHandler):
        def get(self):
            goto = self.reverse_url('other')
            self.redirect(goto)

    # so you can do myapp.reverse_url('other')
    @route('/some/other/path', name='other')
    class SomeOtherRequestHandler(RequestHandler):
        def get(self):
            goto = self.reverse_url('SomeRequestHandler')
            self.redirect(goto)

    # for passing uri parameters
    @route(r'/some/(?P<parameterized>\w+)/path')
    class SomeParameterizedRequestHandler(RequestHandler):
        def get(self, parameterized):
            goto = self.reverse_url(parameterized)
            self.redirect(goto)

    my_routes = route.get_routes()
    ```

    Credit
    -------
    Jeremy Kelley - initial work
    Peter Bengtsson - redirects, named routes and improved comments
    Ben Darnell - general awesomeness
    """
    

    _routes = []

    def __init__(self, uri, name=None, kwargs={}):
        #print("__init__")
        self._uri = uri
        self.name = name
        self.kwargs = kwargs

    def __call__(self, _handler):
        """gets called when we class decorate"""
        #print("__call__")
        name = self.name or _handler.__name__
        self._routes.append(tornado.web.url(self._uri, _handler, self.kwargs, name=name))
        return _handler

    @classmethod
    def get_routes(cls):
        #print("get_routes")
        return cls._routes

# route_redirect provided by Peter Bengtsson via the Tornado mailing list
# and then improved by Ben Darnell.
# Use it as follows to redirect other paths into your decorated handler.
#
#   from routes import route, route_redirect
#   route_redirect('/smartphone$', '/smartphone/')
#   route_redirect('/iphone/$', '/smartphone/iphone/', name='iphone_shortcut')
#   @route('/smartphone/$')
#   class SmartphoneHandler(RequestHandler):
#        def get(self):
#            ...


def route_redirect(from_, to, name=None):
    print("route_redirect")
    route._routes.append(tornado.web.url(
        from_,
        tornado.web.RedirectHandler,
        dict(url=to),
        name=name ))

# maps a template to a route.
def generic_route(uri, template, handler = None):
    print("Generic route")
    h_ = handler or tornado.web.RequestHandler
    @route(uri, name=uri)
    class generic_handler(h_):
        _template = template
        def get(self):
            return self.render(self._template)
    return generic_handler

def authed_generic_route(uri, template, handler):
    print("authed_generic_route")
    """
    Provides authenticated mapping of template render to route.

    :param: uri: the route path
    :param: template: the template path to render
    :param: handler: a subclass of tornado.web.RequestHandler that provides all
        the necessary methods for resolving current_user
    """
    @route(uri, name=uri)
    class authed_handler(handler):
        print("prvni")
        _template = template
        @tornado.web.authenticated
        def get(self):
            print("druhy")
            return self.render(self._template)
    return authed_handler
