# -*- coding: utf-8 -*-
from postal.text import _normalize
from postal.text.tokenize import tokenize_raw
from postal.text.token_types import token_types

from postal.text.encoding import safe_decode

DEFAULT_STRING_OPTIONS = _normalize.NORMALIZE_STRING_LATIN_ASCII |  \
    _normalize.NORMALIZE_STRING_DECOMPOSE | \
    _normalize.NORMALIZE_STRING_TRIM | \
    _normalize.NORMALIZE_STRING_REPLACE_HYPHENS | \
    _normalize.NORMALIZE_STRING_STRIP_ACCENTS | \
    _normalize.NORMALIZE_STRING_LOWERCASE

DEFAULT_TOKEN_OPTIONS = _normalize.NORMALIZE_TOKEN_REPLACE_HYPHENS | \
    _normalize.NORMALIZE_TOKEN_DELETE_FINAL_PERIOD | \
    _normalize.NORMALIZE_TOKEN_DELETE_ACRONYM_PERIODS | \
    _normalize.NORMALIZE_TOKEN_DROP_ENGLISH_POSSESSIVES | \
    _normalize.NORMALIZE_TOKEN_DELETE_OTHER_APOSTROPHE | \
    _normalize.NORMALIZE_TOKEN_REPLACE_DIGITS


def normalized_tokens(s, string_options=DEFAULT_STRING_OPTIONS,
                      token_options=DEFAULT_TOKEN_OPTIONS):
    '''
    Normalizes a string, tokenizes, and normalizes each token
    with string and token-level options.

    This version only uses libpostal's deterministic normalizations
    i.e. methods with a single output. The string tree version will
    return multiple normalized strings, each with tokens.

    Usage:
        normalized_tokens(u'St.-Barthélemy')
    '''
    s = safe_decode(s)
    if string_options & _normalize.NORMALIZE_STRING_LATIN_ASCII:
        normalized = _normalize.normalize_string_latin(s, string_options)
    else:
        normalized = _normalize.normalize_string_utf8(s, string_options)

    # Tuples of (offset, len, type)
    tokens = tokenize_raw(normalized)
    return [(_normalize.normalize_token(normalized, t, token_options), token_types.from_id(t[-1])) for t in tokens]
