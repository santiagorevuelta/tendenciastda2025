import logging
logger = logging.getLogger(__name__)

class ContadorVisitasMiddleware:
    contador = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ContadorVisitasMiddleware.contador += 1
        logger.info(f"Visita numero: {ContadorVisitasMiddleware.contador}")
        response = self.get_response(request)
        return response