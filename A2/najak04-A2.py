import sys
#Einlesen
def read_instance(f):
    line = f.readline().strip()
    #Exceptionhandling
    if not line:
        raise ValueError("empty file")
#splitten 
    parts = line.split()
    n = int(parts[0])
    cost_limit = int(parts[1])

    cities = f.readline().split()
    if len(cities) != n:
        raise ValueError("number of city names does not match n")
#Kostenmatrix
    costs = []
    for _ in range(n):
        parts = f.readline().split()
        if len(parts) != n:
            raise ValueError("row length does not match n")

        row = []
        for x in parts:
            if x == "-":
                row.append(0)
            else:
                row.append(int(x))
        costs.append(row)

    return n, cost_limit, cities, costs



def cost_of_pairing(pairing, cities, costs):
    """
    Input parameter
    pairing: Liste von Tupeln(Paare), z.B. [("B", "E"), ("G", "I"), ...]
    cities:  Liste aller Städtenamen in Reihenfolge aus der Eingabe, wird nummeriert
    costs:   Kostenmatrix (Liste von Listen)
    """
    name_to_index = {name: i for i, name in enumerate(cities)}
    total = 0
    for a, b in pairing:
        i = name_to_index[a]
        j = name_to_index[b]
        total += costs[i][j]
    return total

def generate_pairings(cities):
    """
    Input parameter
    cities: Liste der STädtenamen 
    Erzeugt alle möglichen Aufteilungen der Städte in Paare.
    cities: Liste wie ["B","E","G","I","K","L","P","S"]
    Return: Liste von Paarlisten
      [[("B","E"),("G","I"),("K","L"),("P","S")], ...]
    """
    if not cities:
        return [[]]  # eine leere Paarung falls keine

    first = cities[0]
    rest = cities[1:]
    pairings = []
    # first mit jedem der restlichen paaren einmal, rek
    for i, other in enumerate(rest):
        pair = (first, other)
        remaining = rest[:i] + rest[i+1:]
        for sub in generate_pairings(remaining):
            pairings.append([pair] + sub)
    return pairings


def main():
    # Dateiname aus der Kommandozeile lesen für in
    #hier zweites arg prüfen
    if len(sys.argv) < 2:
        print("Usage: python a2.py <inputfile>")
        sys.exit(1)

    infile = sys.argv[1]
    with open(infile) as f:
        n, cost_limit, cities, costs = read_instance(f)

    # Zum Teste ein mal ausgeben, alle Paarungen erzeugen
    pairings = generate_pairings(cities)

    for pairing in pairings:
        total_cost = cost_of_pairing(pairing, cities, costs)
        if total_cost <= cost_limit:
            # Ausgabe wie test.out: nur die Paare, ohne Klammern/Kommas
            pairs_as_strings = ["".join(p) for p in pairing]
            print(" ".join(pairs_as_strings))

#Aufruf bei direkt Aufruf
    
if __name__ == "__main__":
    main()
