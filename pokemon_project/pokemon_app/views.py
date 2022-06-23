import random
import re
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests as HTTP_Client
import pprint

pp = pprint.PrettyPrinter(indent=2, depth=2)

randomNumber=random.randint(1,875)


def get_name_and_image(url):
    response = HTTP_Client.get(url).json()
    name=response["forms"][0]["name"]       
    imageURL= response["sprites"]["front_default"]
    return [name,imageURL]


def index(request):
    number = request.GET.get('number') or (randomNumber)
    endpoint = f"https://pokeapi.co/api/v2/pokemon/{number}"
    
    #gets first pokemon
    API_response = HTTP_Client.get(endpoint)
    responseJSON = API_response.json()
    name=responseJSON["forms"][0]["name"]       
    imageURL= responseJSON["sprites"]["front_default"]

    pokemon_team_type= responseJSON["types"][0]["type"]["url"]
    available_teammates=HTTP_Client.get(pokemon_team_type).json()["pokemon"]
    # availble_teammates= list of all pokemon objects of the same type

    #teammates is a list of 5 urls of pokemon of the same type
    teammates=[]        
    while len(teammates) < 5:
        i= random.randint(0,len(available_teammates)-1)
        if available_teammates[i] not in teammates:
            teammates.append(available_teammates[i]["pokemon"]["url"])
    
    urls_and_names=[]
    for url in teammates:
        urls_and_names.append(get_name_and_image(url))


    # print(API_response.content)
    # print(responseJSON)
    # pp.pprint(responseJSON)
    response = render(request, 'pokemon/index.html', {'name': name, "imageURL": imageURL, "teammates": teammates, "urls_and_names": urls_and_names})
    return response


