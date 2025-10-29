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
    def insert_member(self, name: str) -> MemberRow:
        mid = self.next_id()
        mr = MemberRow(mid, name, 0)
        self.members[mid] = mr
        return mr


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
        return lr


    def mark_loan_returned(self, loan_id: int):
        if loan_id in self.loans:
            self.loans[loan_id].returned = True

    def find_active_loans_by_member(self, member_id: int) -> List[LoanRow]:
        return [l for l in self.loans.values() if l.member_id == member_id and not l.returned]


    def get_loan(self, loan_id: int) -> Optional[LoanRow]:
        return self.loans.get(loan_id)