from django.http import JsonResponse

def getRoutes(request):
    routes = [
        'GET /api'
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    # safe=False let's routes turn into JSON data
    return JsonResponse(routes, safe=False)