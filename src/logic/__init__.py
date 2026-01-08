"""
Logic package initialization for RK-OS
"""

__version__ = "1.0.0"
__author__ = "RK-OS Team"

# Import logic components at package level if needed
from .propositional import PropositionalLogicEngine, LogicError
from .predicate import PredicateLogicEngine, predicate_engine  
from .truth_tables import TruthTableGenerator, truth_table_generator
from .tautology import TautologyDetector, tautology_detector
from .equivalence import EquivalenceChecker, equivalence_checker

__all__ = [
    'PropositionalLogicEngine',
    'LogicError',
    'PredicateLogicEngine', 
    'predicate_engine',
    'TruthTableGenerator',
    'truth_table_generator',
    'TautologyDetector',
    'tautology_detector',
    'EquivalenceChecker',
    'equivalence_checker'
]
