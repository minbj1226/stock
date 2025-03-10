import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import dashboard.routing  # dashboard 앱의 웹소켓 라우팅 추가

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "joljak.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(dashboard.routing.websocket_urlpatterns)
        ),
    }
)
