from src.data.repositorios_prueba import InMemoryDB
from src.presentacion.vista import Vista


def main():
    db = InMemoryDB()
    vista = Vista(db)
    vista.menu_simple()


    if __name__ == "__main__":
        main()