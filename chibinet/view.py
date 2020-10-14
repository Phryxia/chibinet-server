from django.http import HttpResponse
from django.shortcuts import render
import torch
from torchvision import transforms
import os
import json
from json import JSONDecodeError


def index(request):
    context = {
        'variables': None
    }
    return render(request, 'chibinet/index.html', context)


def image(request):
    # Load generator model
    try:
        G = torch.load(os.getcwd() + '\\netG.pt')
        G.cpu()
    except FileNotFoundError:
        print('Error: netG.pt is not found')
        G = None

    # Load z-value from POST data
    if request.method == 'GET':
        z = torch.rand((1, 128))
    else:
        try:
            jsondata = json.loads(request.body.decode('utf-8'))
            z = jsondata['data']
            z = torch.tensor(z).reshape(1, 128)
        except KeyError:
            with torch.no_grad():
                z = torch.rand((1, 128))

    # Generate image

    with torch.no_grad():
        if G is not None:
            tensor = G(z).reshape(3, 128, 128)
            tensor = torch.transpose(tensor, 1, 2)
        else:
            tensor = torch.rand((3, 128, 128))

        T = transforms.ToPILImage()
        img = T(tensor)

    # Pack image
    response = HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response