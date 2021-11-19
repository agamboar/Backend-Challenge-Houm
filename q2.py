import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

#funcion para obtener un pokemon, dada una url

def get_pokemon(url):
    pokemon = requests.get(url)
    return pokemon

#funcion para obtener los pokemon con los que se puede aparear Raichu
#es decir, que tengan el mismo tipo de egg group

def get_egg_groups():

    url = 'https://pokeapi.co/api/v2/pokemon-species/'

    raichu = get_pokemon('https://pokeapi.co/api/v2/pokemon-species/raichu/')

    raichu_egg_groups = raichu.json()['egg_groups']

    egg_groups = []

    for i in range(len(raichu_egg_groups)):
        egg_groups.append(raichu_egg_groups[i]['name'])

    req = requests.get(url)

    n_pokemon = req.json()['count']
    args = {"limit": n_pokemon}

    r = requests.get(url, params=args)

    pokemon = r.json()

    processes = []
    list_pokemon = []

    #debido que son 898 pokemon, se necesitan 898 request para obtener los datos de cada uno
    #es por esto que se usa multithread para que los request tarden menos tiempo
    #originalmente tardaba aprox 90 segundos en obtener el resultado
    #con multithread tarda entre 10 y 12 segundos, lo cual puede ser mejorado aún más

    with ThreadPoolExecutor(max_workers=10) as executor:

        for j in range(len(pokemon['results'])):
    
            pok_name = pokemon['results'][j]['name']
            url_pok = url + pok_name
            processes.append(executor.submit(get_pokemon, url_pok))

        for task in as_completed(processes):

            egg_groups_pos = task.result().json()['egg_groups']

            if len(egg_groups_pos) > 1:
                for k in range(len(egg_groups_pos)):

                    if egg_groups_pos[k]['name'] in egg_groups:
                        list_pokemon.append(pok_name)
                        break
    
            elif len(egg_groups_pos) == 1:
                if egg_groups_pos[0]['name'] in egg_groups:
                    list_pokemon.append(pok_name)
            else:
                continue

    return(len(list_pokemon))

if __name__ == "__main__":

    print(get_egg_groups())

 
