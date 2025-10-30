"""Repositorio en memoria simulado - actúa como "base de datos" para pruebas
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import itertools

@dataclass
class BookRow:
    id: int
    title: str
    copies: int


@dataclass
class MemberRow:
    id: int
    name: str
    active_loans: int = 0


@dataclass
class LoanRow:
    id: int
    member_id: int
    book_id: int
    returned: bool = False


class InMemoryDB:
    _id_counter = itertools.count(1)

    def __init__(self):
        self.books: Dict[int, BookRow] = {}
        self.members: Dict[int, MemberRow] = {}
        self._next_member_id = 1
        self.loans: Dict[int, LoanRow] = {}


    def next_id(self) -> int:
        return next(self._id_counter)


    # book
    def insert_book(self, title: str, copies: int) -> BookRow:
        bid = self.next_id()
        br = BookRow(bid, title, copies)
        self.books[bid] = br
        return br


    def get_book(self, book_id: int) -> Optional[BookRow]:
        return self.books.get(book_id)


    def update_book_copies(self, book_id: int, copies: int):
        if book_id in self.books:
            self.books[book_id].copies = copies


    # member
    def create_member(self, nombre):
        from dominio.socio import Socio
        # Socio parece requerir (id, nombre) en su constructor
        m = Socio(self._next_member_id, nombre)
        # asegurar atributos por si Constructor ya los estableció o no
        if not hasattr(m, 'id') or m.id is None:
            m.id = self._next_member_id
        if not hasattr(m, 'active_loans'):
            m.active_loans = 0
        self.members[m.id] = m
        self._next_member_id += 1
        return m.id


    def get_member(self, member_id: int) -> Optional[MemberRow]:
        return self.members.get(member_id)


    def update_member_loans(self, member_id: int, loans: int):
        if member_id in self.members:
            self.members[member_id].active_loans = loans


    # loan
    def insert_loan(self, member_id: int, book_id: int) -> LoanRow:
        lid = self.next_id()
        lr = LoanRow(lid, member_id, book_id, False)
        self.loans[lid] = lr
        # incrementar contador de préstamos activos del socio si existe
        member = self.members.get(member_id)
        if member is not None and hasattr(member, 'active_loans'):
            member.active_loans += 1
        return lr


    def get_loan(self, loan_id):
        print(f"[DEBUG InMemoryDB] get_loan({loan_id})")
        return self.loans.get(loan_id)

    def close_loan(self, loan_id):

        print(f"[DEBUG InMemoryDB] close_loan({loan_id})")
        loan = self.loans.get(loan_id)
        if not loan:
            return False
        # en LoanRow el campo es 'returned'
        if getattr(loan, 'returned', False):
            return False
        loan.returned = True
        # decrementar préstamos activos del socio asociado si existe
        member = self.members.get(loan.member_id)
        if member is not None and hasattr(member, 'active_loans'):
            member.active_loans = max(0, member.active_loans - 1)
        return True


    def increment_copies(self, book_id):
        print(f"[DEBUG InMemoryDB] increment_copies({book_id})")
        book = self.books.get(book_id)
        if not book:
            return False
        book.copies += 1
        return True

    def decrement_copies(self, book_id):
        print(f"[DEBUG InMemoryDB] decrement_copies({book_id})")
        book = self.books.get(book_id)
        if not book:
            return False
        if book.copies <= 0:
            return False
        book.copies -= 1
        return True