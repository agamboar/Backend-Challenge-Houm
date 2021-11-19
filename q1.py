import requests

def getA():

    url = 'https://pokeapi.co/api/v2/pokemon-species'

    req = requests.get(url)
    n_pokemon = req.json()['count']
    args = {"limit": n_pokemon}

    r = requests.get(url, params=args)

    pokemon = r.json()

    list_pokemon = []

    for i in range(len(pokemon['results'])):
    
        name = pokemon['results'][i]['name']
        
        if 'at' in name and name.count('a') == 2:
            list_pokemon.append(name)
        else:
            continue

    return len(list_pokemon)


if __name__ == "__main__":

    print(getA())