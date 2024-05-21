from django.http import HttpResponse

from model.TrainModel import save_model


def train(request):
    save_model()
    return HttpResponse("ok")