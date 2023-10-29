import sys
from itertools import combinations
from collections import namedtuple, defaultdict

# Define data structures for support and relation records
SupportRecord = namedtuple('SupportRecord', ('items', 'support'))
RelationRecord = namedtuple('RelationRecord', SupportRecord._fields + ('ordered_statistics',))
OrderedStatistic = namedtuple('OrderedStatistic', ('items_base', 'items_add', 'confidence', 'lift',))


class TransactionManager:
    """Manage transaction data and compute support for items."""
    
    def __init__(self, transactions):
        self.__transactions = list(transactions)
        self.__num_transaction = len(self.__transactions)

    def calc_support(self, items):
        """Calculate support for items."""
        count = sum(1 for trans in self.__transactions if all(item in trans for item in items))
        return float(count) / self.__num_transaction

    @property
    def num_transaction(self):
        return self.__num_transaction


def generate_candidates(prev_candidates, length):
    """Generate candidate sets for the next iteration."""
    items = sorted(set(item for candidates in prev_candidates for item in candidates))
    return [frozenset(c) for c in combinations(items, length)]


def apriori(transactions, min_support=0.1):
    """The main Apriori algorithm. Returns frequent itemsets and their support."""
    
    # Initialize
    transaction_manager = TransactionManager(transactions)
    candidates = [frozenset([item]) for item in set(item for transaction in transactions for item in transaction)]
    k = 2
    frequent_itemsets = []

    while candidates:
        frequent_candidates = []
        for candidate in candidates:
            support = transaction_manager.calc_support(candidate)
            if support >= min_support:
                frequent_itemsets.append((candidate, support))
                frequent_candidates.append(candidate)
        candidates = generate_candidates(frequent_candidates, k)
        k += 1

    # Transform into a support record format
    support_records = [SupportRecord(itemset, support) for itemset, support in frequent_itemsets]
    return support_records


if __name__ == '__main__':
    transactions = [['A', 'B'], ['B', 'C'], ['A', 'B', 'C'], ['C', 'D']]
    min_support = 0.5
    result = apriori(transactions, min_support)
    for record in result:
        print(record)
