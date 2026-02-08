#!/usr/bin/env python3
"""
quiz.py - prosty quiz konsolowy
Uruchom: python quiz.py
"""

def ask(question, options, correct_index):
    """
    Zadaje pytanie, pokazuje opcje, zwraca True jeśli odpowiedź poprawna.
    question: str
    options: list[str]
    correct_index: int (0-based)
    """
    print()
    print(question)
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")
    while True:
        ans = input("Wybierz numer odpowiedzi: ").strip()
        if not ans.isdigit():
            print("Wpisz numer (np. 1).")
            continue
        num = int(ans)
        if 1 <= num <= len(options):
            return (num - 1) == correct_index
        print(f"Wybierz numer od 1 do {len(options)}.")

def main():
    print("=== Krótki quiz — dzień 1 ===")
    score = 0
    total = 3

    if ask("1) Jaki typ danych w Pythonie służy do przechowywania wielu wartości niemutowalnych?", 
           ["list", "tuple", "dict", "set"], 1):
        print("✔️ Poprawnie!")
        score += 1
    else:
        print("❌ Niepoprawnie. Poprawna odpowiedź: tuple")

    if ask("2) Która instrukcja służy do warunkowego wykonania bloku kodu?", 
           ["for", "while", "if", "def"], 2):
        print("✔️ Poprawnie!")
        score += 1
    else:
        print("❌ Niepoprawnie. Poprawna odpowiedź: if")

    if ask("3) Jak zdefiniujesz funkcję w Pythonie?", 
           ["function():", "def name():", "func name():", "define name():"], 1):
        print("✔️ Poprawnie!")
        score += 1
    else:
        print("❌ Niepoprawnie. Poprawna odpowiedź: def name():")

    print()
    print(f"Twój wynik: {score}/{total}")
    if score == total:
        print("Brawo — świetny start! 🎉")
    elif score >= total // 2:
        print("Dobrze — masz solidne podstawy.")
    else:
        print("Spoko — powtórka kilku zagadnień przyda się.")
    print("Koniec quizu.")

if __name__ == "__main__":
    main()
