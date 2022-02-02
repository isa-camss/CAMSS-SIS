import re
import com.nttdata.dgi.util.io as io
from com.nttdata.dgi.nlp.langmodels import LangModel


def _has_special_chars(phrase: str) -> bool:
    c = re.compile('[a-zA-Z0-9\\s]+$')
    return False if c.match(phrase) else True


def simple_clean(text: str) -> str:
    """
    Lower the text and replace "’" with "'". this is particularly important for correct lemmatization
    in French. Other tailored replacements may be further needed.
    :param text: the initial text to be prepared
    :return text: prepared initial string
    """
    text = text.lower()
    text = re.sub(r'’', '\'', text)
    return text


def _remove_trailing_inner_blank(p: str) -> str:
    # sl = '.!-,?:\/"\'@#$%&=¿*^_<>|;'
    sl = '.'
    lp = len(p)
    return [p[:lp - 2] + p[lp - 1:lp] if p[lp - 2:lp - 1] == ' ' and p[lp - 1:lp] in sl else p][0]


def _compress_blanks_(phrase: str, compress: bool) -> str:
    if not compress:
        return phrase
    phrase = phrase.replace(' - ', '-')  # If not, 'at-risk' results in 'at - risk'
    # phrase = _remove_trailing_inner_blank(phrase)  # If not, 'a.i.' results in 'a.i .'
    return phrase


def lemmatize(phrase: str,
              nlp: LangModel,
              lang: str,
              with_symbols: bool = False,
              compress_blanks=True) -> str:
    """
    DEPRECATE with_symbols, it's a source of troubles.
    1. Lowers and splits the term by ' ',
    2. Returns if the term contains special chars, otherwise strings like AB-CDE are lemmatized into AB
    3. Lemmatizes each word inside the term, and
    4. Re-joins the lemmas.
    :param phrase: the term containing the words to lemmatize
    :param nlp: the language models
    :param lang: the lang to use
    :param with_symbols: if True, skips phrases containing non-alpha or non-digits
    :param compress_blanks: if True, hyphens are compressed since the lemmatizer separates hyphend words. This is
    important if one is interested in removing stopwords: in cases like at-risk, the lemmatizer returns 'at - risk'.
    If after this lemmatization one removes stopwords at risk becomes -risk.
    :return: the term containing lemmatized words
    """
    # If symbols are not to be remove the phrase is not lemmatized. However,...
    # It is very important to lowerize it because, if stored and searched, it
    # would not be found since the searcher lemmatizes (and therefore lowerizes)
    # the searched entry.
    if with_symbols and _has_special_chars(phrase):
        return phrase.lower()
    # If only newlines are coming the lemmatization is skipped
    if len(io.nnl(phrase)) == 0:
        return phrase
    try:
        model = nlp.get_model(lang)
    except Exception:
        io.log(f"Model {lang} not found. Going on with English.")
        model = nlp.get_model('en')
    # Need to simply clean the phrase to remove special characters so the lemmatizer from spacy works well
    # (in particular in French).

    clean_phrase = simple_clean(phrase)
    ret = ' '.join(list(token.lemma_ for token in model(clean_phrase)))
    ret = _compress_blanks_(ret, compress_blanks)

    return ret.strip()
