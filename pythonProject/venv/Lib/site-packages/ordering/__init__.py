from collections import Counter
from fractions import Fraction
from functools import total_ordering
from typing import Collection, Dict, Generic, Iterable, Iterator, List, Mapping, TypeVar, Union

__all__ = ('Ordering', 'OrderingItem')


class _Sentinel:
    def __set_name__(self, owner, name) -> None:
        self.owner = owner
        self.name = name

    def __repr__(self) -> str:
        return '{}.{}'.format(self.owner.__qualname__, self.name)


T = TypeVar('T')
_T = Union[T, _Sentinel]


class Ordering(Mapping[T, 'OrderingItem[T]']):
    _start = _Sentinel()
    _end = _Sentinel()

    def __init__(self, iterable: Iterable[T] = ()) -> None:
        self._labels: Dict[_T, Fraction] = {}
        self._successors: Dict[_T, _T] = {}
        self._predecessors: Dict[_T, _T] = {}

        items: List[_T] = [self._start, *iterable, self._end]
        self.assert_unique_items(items)

        for n, (a, b) in enumerate(zip(items, items[1:])):
            self._labels[a] = Fraction(n, len(items) - 1)
            self._successors[a] = b
            self._predecessors[b] = a

        self._labels[self._end] = Fraction(1)

    def _insert_after(self, existing_item: _T, new_item: T) -> 'OrderingItem[T]':
        self.assert_new_item(new_item)

        self._labels[new_item] = (self._labels[existing_item] + self._labels[self._successors[existing_item]]) / 2
        self._successors[new_item] = self._successors[existing_item]
        self._predecessors[new_item] = existing_item

        self._predecessors[self._successors[existing_item]] = new_item
        self._successors[existing_item] = new_item

        return OrderingItem(self, new_item)

    def insert_after(self, existing_item: T, new_item: T) -> 'OrderingItem[T]':
        self._assert_contains(existing_item)
        return self._insert_after(existing_item, new_item)

    def _insert_before(self, existing_item: _T, new_item: T) -> 'OrderingItem[T]':
        return self._insert_after(self._predecessors[existing_item], new_item)

    def insert_before(self, existing_item: T, new_item: T) -> 'OrderingItem[T]':
        self._assert_contains(existing_item)
        return self._insert_after(self._predecessors[existing_item], new_item)

    def insert_start(self, new_item: T) -> 'OrderingItem[T]':
        return self._insert_after(self._start, new_item)

    def insert_end(self, new_item: T) -> 'OrderingItem[T]':
        return self._insert_after(self._predecessors[self._end], new_item)

    def swap(self, item: T, other: T) -> None:
        lower, upper = (item, other) if self.compare(item, other) else (other, item)
        if lower == upper:
            return

        upper_successor = self._successors[upper]
        lower_predecessor = self._predecessors[lower]
        del self[lower], self[upper]

        self._insert_after(lower_predecessor, upper)
        self._insert_before(upper_successor, lower)

    def replace(self, existing_item: T, new_item: T) -> None:
        self.assert_contains(existing_item)

        previous_item = self._predecessors[existing_item]
        del self[existing_item]

        self.assert_new_item(new_item)

        self._insert_after(previous_item, new_item)

    def clear(self) -> None:
        self._labels.clear()
        self._labels.update({self._start: Fraction(0), self._end: Fraction(1)})

        self._successors.clear()
        self._successors.update({self._start: self._end})

        self._predecessors.clear()
        self._predecessors.update({self._end: self._start})

    def compare(self, left_item: T, right_item: T) -> bool:
        self._assert_contains(left_item)
        self._assert_contains(right_item)

        return self._labels[left_item] < self._labels[right_item]

    def __contains__(self, item: object) -> bool:
        if isinstance(item, OrderingItem):
            return item.item in self._labels

        return item in self._labels

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Ordering):
            return NotImplemented  # type: ignore # https://github.com/python/mypy/issues/363
        if len(self) != len(other):
            return False
        return all(a == b for a, b in zip(self, other))

    def __iter__(self) -> Iterator[T]:
        item = self._successors[self._start]

        while not isinstance(item, _Sentinel):
            yield item
            item = self._successors[item]

    def __len__(self) -> int:
        return len(self._labels) - 2

    def __getitem__(self, item: T) -> 'OrderingItem[T]':
        return OrderingItem(self, item)

    # Doing this so that we can write sorted([...], key=ordering)
    __call__ = __getitem__

    def __delitem__(self, item: T) -> None:
        self._assert_contains(item)

        self._successors[self._predecessors[item]] = self._successors[item]
        self._predecessors[self._successors[item]] = self._predecessors[item]

        del self._labels[item]
        del self._successors[item]
        del self._predecessors[item]

    remove = __delitem__

    def _assert_contains(self, item: _T) -> None:
        if item not in self:
            raise KeyError("Ordering {} does not contain {}".format(self, item))

    def assert_contains(self, item: T) -> None:
        self._assert_contains(item)

    def assert_new_item(self, item: T) -> None:
        if item in self:
            raise KeyError("Ordering {} already contains {}".format(self, item))

    @classmethod
    def assert_unique_items(cls, items: Collection[_T]) -> None:
        item_counts = Counter(items)

        if len(items) == len(item_counts):
            return

        duplicates = [item for item, count in item_counts.items() if count > 1]
        raise ValueError("{} found duplicate items: {}".format(cls.__name__, repr(duplicates)[1:-1]))

    def __repr__(self) -> str:
        return '{}({})'.format(type(self).__name__, list(self))


@total_ordering
class OrderingItem(Generic[T]):
    def __init__(self, ordering: Ordering[T], item: T) -> None:
        ordering._assert_contains(item)

        self.ordering = ordering
        self.item = item

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderingItem):
            return self.item == other
        return self.item == other.item and self.ordering == other.ordering

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, OrderingItem):
            return NotImplemented
        return self.ordering.compare(self.item, other.item)

    def insert_before(self, item: T) -> 'OrderingItem[T]':
        return self.ordering.insert_before(self.item, item)

    def insert_after(self, item: T) -> 'OrderingItem[T]':
        return self.ordering.insert_after(self.item, item)

    def __repr__(self) -> str:
        return '<{}: {!r}>'.format(type(self).__name__, self.item)
