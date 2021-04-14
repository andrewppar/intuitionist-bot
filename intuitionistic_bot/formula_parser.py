from enum import Enum
from abc import ABC

"""Formula Parser

    This module is for converting formulas generated by mathlogicbot into
    a form that is parseable by the modal logic theorem prover.

    Example:

         parser = FormulaParser()
         parser.parse("¬¬((¬¬¬a⇾a)∨¬a)")
"""

# Formula


class Connective(Enum):
    """An Enum of all the connectives"""

    Negation = "Not"
    Implication = "Implies"
    Conjunction = "And"
    Disjunction = "Or"


    BiImplication = "Equivalent"


class Formula(ABC):
    """This is the super class of all formulas"""

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass

    def __eq__(self, formula) -> bool:
        pass


class Atomic(Formula):
    """The class that of atomic formulas

    Atomic formulas are the base case in the
    recursive definition of what a formula is. As such
    they take a string which serves as their identity
    criterion.

    Attributes:
        repr: This is a string that is a representation of the formula
    """

    def __init__(self, repr: str) -> None:
        super().__init__()
        self.repr = repr

    def __str__(self) -> str:
        return f'(AtomicFormula "{self.repr}")'

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, Atomic):
            return False
        else:
            return self.repr == formula.repr


class Negation(Formula):
    """The class of all negations

    This class contains formulas that are the
    result of adding a negation to a formula, i.e.
    if P is a formula then Negation(P) is a negation.

    Attributes:
        connective: In this case this attribute is the connective Negation
        negatum: The formula that is being negated
    """

    def __init__(self, negatum: Formula) -> None:
        super().__init__()
        self.connective = Connective.Negation
        self.negatum = negatum

    def __str__(self) -> str:
        return f"({self.connective.value} {self.negatum.__str__()})"

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, Negation):
            return False
        else:
            return self.negatum == formula.negatum


class BinaryFormula(Formula):
    """The class of binary formulas

    This class contains all formulas that have
    exactly two subformulas.

    Attributes:
        left: The left subformula
        right: The right subformula
    """

    def __init__(self, left: Formula, right: Formula) -> None:
        super().__init__()
        self.left = left
        self.right = right

    def _str_helper(self, connective: str) -> str:
        """This is template code that subclasses of
        BinaryFormula use to generate their __str__ function."""
        left_string = self.left.__str__()
        right_string = self.right.__str__()
        return f"({connective} [{left_string}, {right_string}])"

    def __str__(self) -> str:
        pass

    def _eq_helper(self, formula):
        """This is template code that subclasses of
        BinaryFormula use to generate their __eq__ function."""
        first_formulas = [self.left, self.right]
        second_formulas = [formula.left, formula.right]
        for formula in first_formulas:
            if formula not in second_formulas:
                return False
        for formula in second_formulas:
            if formula not in first_formulas:
                return False
        return True

    def __eq__(self, formula) -> bool:
        pass


class Implication(BinaryFormula):
    """The class of implications

    This is a subclass of BinaryFormula.
    """

    def __init__(self, antecedent: Formula, consequent: Formula) -> None:
        super().__init__(antecedent, consequent)
        self.connective = Connective.Implication

    def __str__(self) -> str:
        return f"(Implies {self.left} {self.right})"

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, Implication):
            return False
        else:
            first_antecedent = self.left
            second_antecedent = formula.left
            first_consequent = self.right
            second_consequent = formula.right
            ant_equal = first_antecedent == second_antecedent
            con_equal = first_consequent == second_consequent
            return ant_equal and con_equal


class BiImplication(BinaryFormula):
    """The class of bi-implications

    This is a subclass of BinaryFormula.
    Each bi-implication BiImplication(P,Q) is equivalent
    to the formula And(Implies(P,Q), Implies(Q,P))
    """

    def __init__(self, left: Formula, right: Formula) -> None:
        super().__init__(left, right)
        self.connective = Connective.BiImplication

    def __str__(self) -> str:
        return f"(Equivalent {self.left} {self.right})"

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, BiImplication):
            return False
        else:
            return self._eq_helper(formula)


class Disjunction(BinaryFormula):
    """The class of disjunctions

    This is a subclass of BinaryFormula.
    """

    def __init__(self, left: Formula, right: Formula) -> None:
        super().__init__(left, right)
        self.connective = Connective.Disjunction

    def __str__(self) -> str:
        return self._str_helper(self.connective.value)

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, Disjunction):
            return False
        else:
            return self._eq_helper(formula)


class Conjunction(BinaryFormula):
    """The class of conjunctions

       This is a subclass of BinaryFormula.
    """

    def __init__(self, left: Formula, right: Formula) -> None:
        super().__init__(left, right)
        self.connective = Connective.Conjunction

    def __str__(self) -> str:
        return self._str_helper(self.connective.value)

    def __eq__(self, formula) -> bool:
        if not isinstance(formula, Conjunction):
            return False
        else:
            return self._eq_helper(formula)


class FormulaParser:
    """Parses a string into an instance of Formula.

    This is the class that does all the work parsing strings
    into formulas.

    Attributes:
        binary_connective_chars: The characters that are binary connectives
        logical_operator_chars: The characters that are logical operators
        special_parse_chars: Characters ot in the above to classes but are not
            parts of atomic formulas, i.e. ( and )
   """

    def __init__(self) -> None:
        self.binary_connective_chars = ['∨', '⇾', '∧', '⇿']
        self.logical_operator_chars = self.binary_connective_chars + ['¬']
        self.special_parse_chars = self.logical_operator_chars + ['(',
                                                                  ')']

    def _is_atomic_formula(self, formula_string: str) -> bool:
        """An internal function that checks whether a string
        should be parsed as an atomic formula.

        Args:
            formula_string: the string that is going to be checked

        Returns:
            A boolean indicating whether or not formula_string should
                be parsed as an atomic formula.
        """
        result = True
        for char in formula_string:
            if char in self.special_parse_chars:
                return False
        return result

    def parse(self, string: str) -> Formula:
        """This is the main public function of this class
        It takes a string and either returns the formula
        corresponding to that string or an error if the
        string cannot be parsed as a formula.

        Args:
            string: The string that will be attempted to parse

        Returns:
            An instance of Formula

        Raises:
            RuntimeError: An error if the string is not
                parseable into a formula
        """
        if string[0] == '(' and string[-1] == ')':
            string = string[1:-1]
        if self._is_atomic_formula(string):
            return Atomic(string)
        else:
            main_idx = self.get_main_connective_index(string)
        if main_idx == 0:
            subformula = self.parse(string[1:])
            return Negation(subformula)
        else:
            connective = string[main_idx]
            left_string = string[:main_idx]
            right_string = string[(main_idx + 1):]
            left_formula = self.parse(left_string)
            right_formula = self.parse(right_string)
            if connective == '∨':
                return Disjunction(left_formula, right_formula)
            elif connective == '⇾':
                return Implication(left_formula, right_formula)
            elif connective == '∧':
                return Conjunction(left_formula, right_formula)
            elif connective == '⇿':
                return BiImplication(left_formula, right_formula)
            else:
                error = f"{connective} is not a supported connective"
                raise RuntimeError(error)

    def get_main_connective_index(self, formula_string: str) -> int:
        """Returns the index of the main connective in a formula string

        Args:
            formula_string: The string whose main connective is being
                retrieved.

        Returns:
            An int corresponding to the index that the main connective was
            found at.
        """
        paren_depth = 0
        connective_index = 0
        for idx, char in enumerate(formula_string):
            if char in self.binary_connective_chars and paren_depth == 0:
                if connective_index != 0:
                    raise RuntimeError(f"{formula_string} is ambiguous")
                else:
                    connective_index = idx
            elif char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            else:
                continue
        return connective_index


# formulas = ["¬¬((¬¬¬a⇾a)∨¬a)",
#             "¬¬((¬¬¬a⇿¬a)∨a)",
#             "¬¬((¬¬¬a∧¬a)∨a)",
#             "(¬¬¬a∧¬a)∨a",
#             "¬¬¬a∧¬a",
#             ]
#
# parser = FormulaParser()
# for formula in formulas:
#     print(formula)
#     print(parser.parse(formula))
