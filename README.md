# Concurrence

Le(s) projet(s) pour la discipline de Gestion de la Concurrence l'année 2019/20

## Déplacement d'une Foule

Le programme modélise le déplacement d'une foule sur un terrain avec des obstacles. Une instance est modelisé par:

1. La taille du terrain
2. Les points de sortie
3. Les obstacles, parametrizer par sont point plus en haut et à gauche et son point plus en bas et à droite
4. Les personnes, chacqu'une à une position sur le terrain

### Éxécution

Le programme peut être éxécuté avec `python main.py -p <nombre de personnes> -t <scénario de création de threads> [-m]`, où:

- Le numéro donné `p` varie de 0 a 9, et le nombre de personnes sera 2<sup>p</sup>
- Il-y-a 3 scénarios possibles pour `t`:
	- `-t 0`: Le programme utilisera une seule thread
	- `-t 1`: Le programme utilisera une thread pour chacque personne
	- `-t 2`: Le terrain sera partagé en 4 parties dont chacqune aura une thread
- Si la flag `-m` est utilisé le programme fara la mesure du temps d'exécution et la consommation du CPU. En ce cas le programme n'affichera rien au console. La mesure resultant sera la moyenne des 3 valeurs intermédiaires après 5 exécutions
