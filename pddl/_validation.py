#
# Copyright 2021-2023 WhiteMech
#
# ------------------------------
#
# This file is part of pddl.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#

"""This module defines validation functions for PDDL data structures."""
from typing import Collection, Optional, Set, Tuple

from pddl.custom_types import name, namelike, to_names  # noqa: F401
from pddl.exceptions import PDDLValidationError
from pddl.helpers.base import ensure_set
from pddl.logic import Constant, Predicate
from pddl.logic.terms import Term
from pddl.parser.symbols import ALL_SYMBOLS


def _find_inconsistencies_in_typed_terms(
    terms: Optional[Collection[Term]], all_types: Set[name]
) -> Optional[Tuple[Term, name]]:
    """
    Check that the terms in input all have legal types according to the list of available types.

    :param terms: the terms to check
    :param all_types: all available types
    :return: the type tag that raised the error, None otherwise
    """
    if terms is None:
        return None
    for term in terms:
        for type_tag in sorted(term.type_tags):
            if type_tag is not None and type_tag not in all_types:
                return term, type_tag
    return None


def _check_constant_types(
    constants: Optional[Collection[Constant]], all_types: Set[name]
) -> None:
    check_result = _find_inconsistencies_in_typed_terms(constants, all_types)
    if check_result is not None:
        constant, type_tag = check_result
        raise PDDLValidationError(
            f"type {repr(type_tag)} of constant {repr(constant)} is not in available types {all_types}"
        )


def _check_types_in_has_terms_objects(
    has_terms_objects: Optional[Collection[Predicate]],
    all_types: Set[name],
) -> None:
    """Check that the terms in the set of predicates all have legal types."""
    if has_terms_objects is None:
        return

    for has_terms in has_terms_objects:
        check_result = _find_inconsistencies_in_typed_terms(has_terms.terms, all_types)
        if check_result is not None:
            term, type_tag = check_result
            raise PDDLValidationError(
                f"type {repr(type_tag)} of term {repr(term)} in atomic expression "
                f"{repr(has_terms)} is not in available types {all_types}"
            )


def _is_a_keyword(word: str, ignore: Optional[Set[str]] = None) -> bool:
    """Check that the word is not a keyword."""
    ignore_set = ensure_set(ignore)
    return word not in ignore_set and word in ALL_SYMBOLS
