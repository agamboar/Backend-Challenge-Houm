import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

#funcion para obtener un pokemon, dada una url

def get_pokemon(url):

    pokemon = requests.get(url)
    return pokemon

#funcion para obtener todos los tipos de pokemon tipo pelea de la primera generación
#y obtener los pesos máximos y mínimos

def get_fighting():

    url = 'https://pokeapi.co/api/v2/pokemon/'

    args = {"limit": 151}   #primera generacion son 151 pokemon

    req = requests.get(url, params=args)

    pokemon = req.json()

    pok_fighting_weight = []
    processes = []
    max_min_weight = []

    #nuevamente se usa multithread para acelerar el proceso de obtencion de datos
    #de la API mediante las requests
    
    with ThreadPoolExecutor(max_workers=10) as executor:

        for i in range(len(pokemon['results'])):

            pok_name = pokemon['results'][i]['name']

            url_pok = url + pok_name
            processes.append(executor.submit(get_pokemon, url_pok))

        for task in as_completed(processes):

            types = task.result().json()['types']
    
            if len(types) > 1:

                for j in range(len(types)):

                    if types[j]['type']['name'] == 'fighting':

                        pok_fighting_weight.append(task.result().json()['weight'])
                        break

            if types[0]['type']['name'] == 'fighting':

                pok_fighting_weight.append(task.result().json()['weight'])

        max_min_weight.append(max(pok_fighting_weight))
        max_min_weight.append(min(pok_fighting_weight))

    return(max_min_weight)


if __name__ == "__main__":

    print(get_fighting())

 