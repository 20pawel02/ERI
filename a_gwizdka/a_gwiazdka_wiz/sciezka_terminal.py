import math  # dla funkcji matematycznych
import numpy as np  # dla operacji na macierzach


# Funkcja obliczająca odległość euklidesową między dwoma punktami (heurystyka)
def wzor_mat(pozycja, cel):
    """
    Funkcja obliczająca odległość euklidesową między dwoma punktami.
    Używana jako heurystyka w algorytmie A*.
    """
    return math.sqrt((pozycja[0] - cel[0]) ** 2 + (pozycja[1] - cel[1]) ** 2)


# Funkcja wczytująca mapę z pliku tekstowego
def wczytaj_grid(nazwa_pliku):
    """
    Wczytuje mapę z pliku tekstowego.
    Format pliku:
    0 0 5 0 1
    0 5 0 5 1
    1 1 1 1 1
    gdzie: 
    0 - wolne pole
    5 - przeszkoda
    1 - ścieżka
    """
    try:
        with open(nazwa_pliku, 'r') as plik:
            lines = plik.readlines()
            grid = []
            for line in lines:
                # Konwertuje każdą linię na listę liczb całkowitych
                row = [int(x) for x in line.split(' ')]
                grid.append(row)
            return np.array(grid)
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {nazwa_pliku}")
        return None
    except ValueError:
        print("Błąd w formacie pliku. Upewnij się, że zawiera tylko 0 i 1.")
        return None


# Implementacja algorytmu A* do znajdowania najkrótszej ścieżki
def a_gwiazdka(grid, start, cel):
    """
    Algorytm A* znajdujący najkrótszą ścieżkę między punktami start i cel.
    Używa heurystyki odległości euklidesowej.
    """
    wiersze, kolumny = grid.shape
    lista = []  # lista otwarta - kolejka priorytetowa
    lista.append((0, start))  # dodajemy start do listy otwartej
    pola = {}  # słownik przechowujący informację o poprzednich polach
    g_wynik = {start: 0}  # koszt dojścia do danego pola
    f_wynik = {start: wzor_mat(start, cel)}  # przewidywany całkowity koszt

    # Definiujemy możliwe ruchy (góra, dół, lewo, prawo)
    ruchy = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while lista:
        # Znajdujemy element z najniższym priorytetem (ostatnie minimalne oszacowanie)
        lista.sort(key=lambda x: x[0], reverse=True)
        _, obecny = lista.pop()

        if obecny == cel:
            # Znaleziono cel - odtwarzamy ścieżkę
            sciezka = []
            while obecny in pola:
                sciezka.append(obecny)
                obecny = pola[obecny]
            sciezka.append(start)
            sciezka.reverse()

            # Zaznaczamy ścieżkę na gridzie
            for x, y in sciezka:
                grid[x, y] = 1
            return sciezka

        # Sprawdzamy wszystkie możliwe ruchy
        for dx, dy in ruchy:
            x_new, y_new = obecny[0] + dx, obecny[1] + dy
            sasiad = (x_new, y_new)

            # Sprawdzamy czy ruch jest dozwolony (w granicach i nie ma przeszkody)
            if (0 <= x_new < wiersze and 0 <= y_new < kolumny and grid[x_new, y_new] == 0):
                g_new = g_wynik[obecny] + wzor_mat(obecny, sasiad)

                # Aktualizujemy ścieżkę jeśli znaleziono lepszą
                if sasiad not in g_wynik or g_new < g_wynik[sasiad]:
                    pola[sasiad] = obecny
                    g_wynik[sasiad] = g_new
                    f_wynik[sasiad] = g_new + wzor_mat(sasiad, cel)
                    lista.append((f_wynik[sasiad], sasiad))

    return None  # Nie znaleziono ścieżki


def save_grid_with_path(grid, output_file):
    """
    Zapisuje siatkę z zaznaczoną ścieżką do pliku tekstowego.
    """
    with open(output_file, 'w') as f:
        for row in grid:
            f.write(' '.join(map(str, row)) + '\n')


def komunikat_o_zakonczeniu_programu():
    if sciezka:
        print("Znaleziono ścieżke")
        # Zapisujemy grid ze ścieżką do nowego pliku
        save_grid_with_path(grid_sciezka,
                            'pliki/grid_with_path.txt')  # utworzenie nowego pliku grid z zaznaczona sciezka (dla bezpieczenstwa)
        print(grid_sciezka)  # wyprintowanie grid z zaznaczona sciezka
    else:
        print("Nie znaleziono ścieżki")


# Główna część programu
if __name__ == "__main__":
    # Wczytujemy mapę z pliku
    grid = wczytaj_grid('pliki/grid.txt')

    if grid is not None:
        # Tworzymy kopię gridu dla ścieżki
        grid_sciezka = np.copy(grid)

        # Definiujemy punkty start i cel
        start = (19, 0)  # punkt startowy, lewy dolny rog
        cel = (0, 19)  # punkt końcowy, prawy gorny rog

        # Szukamy ścieżki użytkując algorytm A*
        sciezka = a_gwiazdka(grid_sciezka, start, cel)

        # Wyświetlamy wynik
        komunikat_o_zakonczeniu_programu()