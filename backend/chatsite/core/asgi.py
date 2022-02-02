"""
This root routing configuration specifies that when a connection
is made to the Channels development server,
the ProtocolTypeRouter will first inspect the type of connection.
If it is a WebSocket connection (ws:// or wss://),
the connection will be given to the AuthMiddlewareStack.

The AuthMiddlewareStack will populate the connection’s
scope with a reference to the currently authenticated user,
similar to how Django’s AuthenticationMiddleware populates
the request object of a view function with the currently authenticated user.

The URLRouter will examine the HTTP path of the connection
to route it to a particular consumer,
based on the provided url patterns
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# configure app protocols
application = ProtocolTypeRouter({
    "http": get_asgi_application(), # for http requests
    "websocket": AuthMiddlewareStack(   # for websocket
        URLRouter(
            chat.routing.websocket_urlpatterns # add app routes
        )
    ),
})
