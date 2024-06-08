from django.http import JsonResponse

class CustomUnauthorizedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 401:
            return JsonResponse({'detail': 'Vous devez être authentifié pour accéder à cette ressource.'}, status=401)
        elif response.status_code == 403:
            return JsonResponse({'detail': 'Vous n\'avez pas les permissions nécessaires pour accéder à cette ressource.'}, status=403)
        elif response.status_code == 404:
            return JsonResponse({'detail': 'La ressource demandée n\'a pas été trouvée.'}, status=404)
        return response
