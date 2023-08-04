import datetime
from django.conf import settings

import uuid

from api.utils import write_to_encrypted_file

class RequestResponseLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate a unique request ID
        request_id = str(uuid.uuid4())

        # Attach the request ID to the request object for future access
        request.request_id = request_id

        user_id = request.user

        if user_id:
            file_path = f"log/{user_id}.log"
        else:
            file_path = f"log/anon.log"
            
        write_to_encrypted_file(file_path, f"[Request ID: {request_id}] Incoming Request: {request.method} {request.path} {request.body}", settings.FERNET_KEY)

        # Get the response from the next middleware or view
        response = self.get_response(request)
        write_to_encrypted_file(file_path, f"[Request ID: {request_id}] Outgoing Response: {response.status_code}", settings.FERNET_KEY)

        return response
    
    

