# In StudentHelp/context_processors.py
from .models import TransportRequest

def transport_requests_processor(request):
    if request.user.is_authenticated:
        transport_requests = TransportRequest.objects.filter(post__user=request.user)
    else:
        transport_requests = []
    return {'transport_requests': transport_requests}
