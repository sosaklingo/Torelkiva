#!/usr/bin/env python3
"""Gecontroleerde zinsvertaler Nederlands <-> Torelkiva 2.2.

Beperkt grammaticaal domein. Onbekende vormen geven een fout; de vertaler
verzint nooit onbekende woorden of een schijnbaar correcte betekenis.
"""
from __future__ import annotations
import argparse
import re
from dataclasses import dataclass
from taal import woorden

class UnsupportedSentenceError(ValueError):
    """Zin valt buiten de gepubliceerde gecontroleerde grammatica."""

SUBJECTS_NL = {'ik': 'mi', 'jij': 'ti', 'je': 'ti', 'wij': 'miva', 'we': 'miva', 'hij': 'ela', 'zij': 'eli'}
SUBJECTS_TK = {'mi':'Ik', 'ti':'Jij', 'miva':'Wij', 'ela':'Hij', 'eli':'Zij', 'tira':'Zij'}
OBJECTS_NL = {'mij':'mi', 'me':'mi', 'jou':'ti', 'je':'ti', 'ons':'miva', 'hem':'ela', 'haar':'eli', 'hen':'tira'}
OBJECTS_TK = {'mi':'mij', 'ti':'jou', 'miva':'ons', 'ela':'hem', 'eli':'haar', 'tira':'hen'}

# infinitief, ik-vorm, jij-vorm, wij-vorm, verleden enkelvoud, verleden meervoud
VERBS = {
 'vara': ('spreken','spreek','spreekt','spreken','sprak','spraken'),
 'nela': ('begrijpen','begrijp','begrijpt','begrijpen','begreep','begrepen'),
 'sila': ('verbergen','verberg','verbergt','verbergen','verborg','verborgen'),
 'kiri': ('beschermen','bescherm','beschermt','beschermen','beschermde','beschermden'),
 'fira': ('zien','zie','ziet','zien','zag','zagen'),
 'mero': ('schrijven','schrijf','schrijft','schrijven','schreef','schreven'),
 'lona': ('lezen','lees','leest','lezen','las','lazen'),
 'gala': ('gaan','ga','gaat','gaan','ging','gingen'),
 'dara': ('komen','kom','komt','komen','kwam','kwamen'),
 'sema': ('weten','weet','weet','weten','wist','wisten'),
 'tala': ('denken','denk','denkt','denken','dacht','dachten'),
 'voro': ('vragen','vraag','vraagt','vragen','vroeg','vroegen'),
 'riva': ('antwoorden','antwoord','antwoordt','antwoorden','antwoordde','antwoordden'),
 'rala': ('leren','leer','leert','leren','leerde','leerden'),
 'meki': ('maken','maak','maakt','maken','maakte','maakten'),
 'tanu': ('geven','geef','geeft','geven','gaf','gaven'),
 'sumi': ('nemen','neem','neemt','nemen','nam','namen'),
 'kori': ('vinden','vind','vindt','vinden','vond','vonden'),
 'navo': ('openen','open','opent','openen','opende','openden'),
 'kavo': ('sluiten','sluit','sluit','sluiten','sloot','sloten'),
 'deki': ('helpen','help','helpt','helpen','hielp','hielpen'),
 'laki': ('willen','wil','wilt','willen','wilde','wilden'),
 'hira': ('lachen','lach','lacht','lachen','lachte','lachten'),
 'naki': ('wachten','wacht','wacht','wachten','wachtte','wachtten'),
 'dari': ('werken','werk','werkt','werken','werkte','werkten'),
 'rano': ('spelen','speel','speelt','spelen','speelde','speelden'),
 'suri': ('slapen','slaap','slaapt','slapen','sliep','sliepen'),
 'meli': ('eten','eet','eet','eten','at','aten'),
 'pelo': ('drinken','drink','drinkt','drinken','dronk','dronken'),
 'piri': ('voelen','voel','voelt','voelen','voelde','voelden'),
 'dali': ('lopen','loop','loopt','lopen','liep','liepen'),
 'sira': ('luisteren','luister','luistert','luisteren','luisterde','luisterden'),
 'somo': ('horen','hoor','hoort','horen','hoorde','hoorden'),
}
PRON = {'mi':0, 'ti':1, 'miva':2, 'ela':1, 'eli':1, 'tira':2}
# Werkwoorden waarbij een direct voorwerp in de gecontroleerde Nederlandse
# zinsbouw niet mogelijk is. Voorzetselvoorwerpen ('naar muziek luisteren')
# zijn nog geen onderdeel van dit beperkte vertaalmodel.
NO_DIRECT_OBJECT = frozenset({'gala','dara','hira','naki','dari','rano',
                             'suri','dali','sira','tala','riva','sema'})


def _check_valency(verb: str, obj: str | None) -> None:
    if obj is not None and verb in NO_DIRECT_OBJECT:
        raise UnsupportedSentenceError(
            'Dit werkwoord kan in deze vertaler geen direct voorwerp hebben. '
            'Een eventuele voorzetselconstructie is nog niet ondersteund.')


# Veelgebruikte zelfstandige naamwoorden, met artikel voor een leesbare weergave.
ARTICLES = {'viro':'een', 'meva':'een','ravo':'de','sima':'het','lavi':'een','luma':'een',
            'mora':'een','liri':'een','taro':'een','dova':'een', 'sona':'de',
            'lovo':'de','pora':'het','tora':'een', 'nema':'de'}
# Exacte genormeerde woorden voor het gecontroleerde vertaaldomein.
NOUNS = {'bericht':'viro','taal':'ravo','geheim':'sima','boek':'lavi','woord':'meva',
         'vriend':'luma','huis':'mora','kind':'liri','computer':'taro','telefoon':'dova',
         'familie':'sona','liefde':'lovo','water':'pora','sleutel':'tora','wereld':'nema',
         'torelkiva':'Torelkiva'}
ADJS = {'nieuw':'nori','nieuwe':'nori','geheim':'sima','geheime':'sima','mooi':'mavi','mooie':'mavi',
        'goed':'kavi','goede':'kavi','groot':'vala','grote':'vala', 'klein':'niva','kleine':'niva',
        'veilig':'velo','veilige':'velo'}
GENDER_ARTICLE = {'viro':'het','meva':'het','ravo':'de','sima':'het','lavi':'het',
                  'luma':'de','mora':'het','liri':'het','taro':'de','dova':'de',
                  'sona':'de','lovo':'de','pora':'het','tora':'de','nema':'de'}
NL_NOUN = {value: key for key, value in NOUNS.items()}
NL_NOUN['torelkiva']='Torelkiva'
NL_ADJ = {'nori':'nieuw','sima':'geheim','mavi':'mooi','kavi':'goed','vala':'groot','niva':'klein','velo':'veilig'}

@dataclass(frozen=True)
class Parsed:
    subject: str
    verb: str
    obj: str|None = None
    adjective: str|None = None
    tense: str = ''
    negated: bool = False
    question: bool = False
    article_token: str = ''  # leeg=2.1-weergave; da=de/het; en=een


def _tokens(text: str) -> tuple[list[str], str]:
    clean = re.sub(r'\s+', ' ', text.strip())
    if not clean:
        raise UnsupportedSentenceError('Voer eerst een zin in.')
    if '\n' in text.strip():
        raise UnsupportedSentenceError('Vertaal één zin tegelijk; meerdere regels zijn niet ondersteund.')
    if not re.fullmatch(r"[\w\- ]+[.!?]?", clean, flags=re.UNICODE):
        raise UnsupportedSentenceError('Gebruik één eenvoudige zin zonder komma’s of aanhalingstekens.')
    mark = clean[-1] if clean[-1] in '.!?' else '.'
    words = (clean[:-1] if clean[-1] in '.!?' else clean).split(' ')
    return [w.casefold() for w in words], mark


def parse_torel(text: str) -> Parsed:
    words, mark = _tokens(text)
    if words in (['vema'], ['savo']):
        raise UnsupportedSentenceError('Groeten worden afzonderlijk verwerkt.')
    question = words[-1] == 'ke'
    if (mark == '?') != question:
        raise UnsupportedSentenceError("Een Torelkiva-vraag eindigt op 'ke?'; een mededeling op een punt.")
    if question:
        words.pop()
    if not words or words[0] not in SUBJECTS_TK:
        raise UnsupportedSentenceError('Begin met mi, ti, miva, ela, eli of tira.')
    subject = words.pop(0)
    if not words or words[-1] not in VERBS:
        raise UnsupportedSentenceError('De zin moet eindigen op een bekend Torelkiva-werkwoord.')
    verb = words.pop()
    negated = False
    if words and words[-1] == 'vo':
        words.pop(); negated = True
    tense = ''
    if words and words[-1] in ('na','sa'):
        tense = words.pop()
    if words and words[-1] == 'vo':
        raise UnsupportedSentenceError('Gebruik de vaste volgorde: ... na/sa vo werkwoord.')
    obj = adjective = None
    article_token = ''
    if words and words[0] in ('da','en'):
        article_token = words.pop(0)
    if words:
        if len(words) > 2:
            raise UnsupportedSentenceError('Deze vertaler ondersteunt maximaal één bijvoeglijk naamwoord en één voorwerp.')
        raw = words.pop()
        if not raw.endswith('em'):
            raise UnsupportedSentenceError('Een lijdend voorwerp eindigt op -em.')
        obj = raw[:-2]
        if obj.endswith('in'):
            raise UnsupportedSentenceError('Meervoudsvoorwerpen worden nog niet automatisch vertaald.')
        if obj not in NL_NOUN and obj not in OBJECTS_TK:
            raise UnsupportedSentenceError(f'Geen Nederlandse vertaalvorm voor {obj!r}.')
        if words:
            adjective = words.pop()
            if adjective not in NL_ADJ:
                raise UnsupportedSentenceError(f'Onbekend bijvoeglijk naamwoord: {adjective!r}.')
            if obj in OBJECTS_TK or obj == 'torelkiva':
                raise UnsupportedSentenceError('Een bijvoeglijk naamwoord kan hier niet bij een voornaamwoord of eigennaam staan.')
    if article_token and (not obj or obj in OBJECTS_TK or obj == 'torelkiva' or negated):
        raise UnsupportedSentenceError('da/en mogen alleen vóór een niet-ontkend zelfstandig naamwoord staan.')
    _check_valency(verb, obj)
    return Parsed(subject, verb, obj, adjective, tense, negated, question or mark == '?', article_token)


def to_nederlands(text: str) -> str:
    words, mark = _tokens(text)
    if words == ['vema']: return 'Hallo!'
    if words == ['savo']: return 'Tot ziens!'
    p = parse_torel(text)
    inf, ik, jij, plural, past, past_pl = VERBS[p.verb]
    i = PRON[p.subject]
    subject = SUBJECTS_TK[p.subject]
    pronoun_obj = p.obj in OBJECTS_TK
    obj = ''
    if p.obj:
        if pronoun_obj:
            obj = OBJECTS_TK[p.obj]
        else:
            noun = NL_NOUN[p.obj]
            article = (GENDER_ARTICLE[p.obj] if p.article_token == 'da' else 'een' if p.article_token == 'en' else ARTICLES.get(p.obj,'een'))
            adj = NL_ADJ.get(p.adjective,'')
            if adj:
                # Onbepaald het-woord: een nieuw boek, geen *nieuwe boek*.
                het_woorden = {'viro','sima','lavi','meva','mora','liri','pora'}
                effective_article = 'een' if p.negated else article
                needs_e = effective_article in ('de', 'het') or (effective_article == 'een' and p.obj not in het_woorden)
                if needs_e:
                    # Groot -> grote, niet 'groote'; spelling is geen simpele -e bij alle stammen.
                    adj = {'groot': 'grote'}.get(adj, adj if adj.endswith('e') else adj+'e')
                obj = f'{article} {adj} {noun}'
            else:
                obj = f'{article} {noun}' if p.obj!='torelkiva' else 'Torelkiva'
    if p.negated and p.obj and not pronoun_obj and p.obj != 'torelkiva':
        # 'Geen bericht' is idiomatischer dan 'een bericht niet'.
        if obj.startswith(('een ', 'het ', 'de ')):
            obj = 'geen ' + obj.split(' ', 1)[1]
        neg_word = ''
    else:
        neg_word = 'niet ' if p.negated else ''
    if p.tense == 'sa':
        finite = 'zullen' if i == 2 else ('zult' if p.subject == 'ti' else 'zal')
        predicate = f'{finite} {obj} {neg_word}{inf}'.strip()
    elif p.tense == 'na':
        finite = past_pl if i == 2 else past
        predicate = f'{finite} {obj} {neg_word}'.strip()
    else:
        finite = ('wil' if p.subject in ('ela','eli') and p.verb=='laki' else (ik,jij,plural)[i])
        predicate = f'{finite} {obj} {neg_word}'.strip()
    if p.question:
        # Nederlandse inversie: "Begrijp jij mij?", niet "Begrijpt jij mij?".
        if p.tense == 'sa':
            finite_q = 'zullen' if i==2 else ('zul' if p.subject=='ti' else 'zal')
            sentence = f'{finite_q.capitalize()} {subject.lower()} {obj} {neg_word}{inf}?'
        else:
            if p.tense == 'na':
                finite_q = past_pl if i==2 else past
            else:
                finite_q = ik if p.subject == 'ti' else finite
            sentence = f'{finite_q.capitalize()} {subject.lower()} {obj} {neg_word}?'
        return re.sub(r'\s+\?', '?', re.sub(r'\s+', ' ', sentence))
    return re.sub(r'\s+', ' ', f'{subject} {predicate}.')


def parse_nederlands(text: str) -> Parsed:
    """Herken alleen de gedocumenteerde, gecontroleerde zinsbouw.

    Volgorde: [persoonsvorm] onderwerp [geen/een/de/het + adj + object]
              [niet] [infinitief bij toekomst].
    Leid geen vertaling af van een zin met tegengestelde ontkenningen of
    een bijvoeglijk naamwoord bij een voornaamwoord.
    """
    words, mark = _tokens(text)
    if words in (['hallo'], ['tot', 'ziens']):
        raise UnsupportedSentenceError('Groeten worden afzonderlijk verwerkt.')
    question = mark == '?'
    singular_she = False
    if question:
        if len(words) < 2 or words[1] not in SUBJECTS_NL:
            raise UnsupportedSentenceError('Gebruik voor vragen bijvoorbeeld: "Begrijp jij mij?"')
        finite = words.pop(0)
        subject_word = words.pop(0)
        subject = SUBJECTS_NL[subject_word]
    else:
        if words[0] not in SUBJECTS_NL:
            raise UnsupportedSentenceError('Gebruik als onderwerp: ik, jij, hij, zij of wij.')
        subject_word = words.pop(0)
        subject = SUBJECTS_NL[subject_word]
        if not words:
            raise UnsupportedSentenceError('Een zin heeft een werkwoord nodig.')
        finite = words.pop(0)
    # Nederlandse 'zij' is enkelvoud of meervoud afhankelijk van de persoonsvorm.
    # 'zij gaan' en 'zij zullen' zijn meervoud; 'zij gaat' en 'zij zal' enkelvoud.
    if subject_word == 'zij':
        plural_forms = {'zullen'} | {forms[3] for forms in VERBS.values()} | {forms[5] for forms in VERBS.values()}
        singular_forms = {'zal','wil'} | {forms[2] for forms in VERBS.values()} | {forms[4] for forms in VERBS.values()}
        if finite in plural_forms and finite not in singular_forms:
            subject = 'tira'
        elif finite in singular_forms and finite not in plural_forms:
            subject = 'eli'
        elif finite in plural_forms and finite in singular_forms:
            raise UnsupportedSentenceError("'Zij' is hier dubbelzinnig. Gebruik voor een enkelvoudige vrouw 'zij zal' of een andere ondubbelzinnige persoonsvorm.")
        else:
            raise UnsupportedSentenceError('Onbekende of onjuiste persoonsvorm bij zij.')

    person = PRON[subject]
    future = finite in {'zal','zul','zult','zullen'}
    if future:
        if question:
            expected = 'zullen' if person==2 else ('zul' if subject=='ti' else 'zal')
        else:
            expected = 'zullen' if person==2 else ('zult' if subject=='ti' else 'zal')
        if finite != expected:
            raise UnsupportedSentenceError('Gebruik de correcte toekomstige persoonsvorm.')
        if not words:
            raise UnsupportedSentenceError('Een toekomstige zin heeft een infinitief nodig.')
        infinitive = words.pop()  # Het hele werkwoord staat aan het einde: ik zal een boek lezen.
        matches = [code for code, forms in VERBS.items() if forms[0] == infinitive]
        if len(matches) != 1:
            raise UnsupportedSentenceError('Onbekend toekomstig werkwoord.')
        verb, tense = matches[0], 'sa'
    else:
        matches = []
        for code, forms in VERBS.items():
            # Nederlandse inversie bij jij: "Begrijp jij", niet "Begrijpt jij".
            if question and subject == 'ti':
                present = forms[1]
            else:
                present = 'wil' if code == 'laki' and subject in ('ela','eli') else forms[1 + person]
            past = forms[5] if person == 2 else forms[4]
            if finite == present:
                matches.append((code, ''))
            if finite == past:
                matches.append((code, 'na'))
        matches = list(dict.fromkeys(matches))
        if len(matches) != 1:
            raise UnsupportedSentenceError('Onbekend of dubbelzinnig werkwoord; gebruik een voorbeeldzin uit de gids.')
        verb, tense = matches[0]

    # Alleen twee canonieke soorten ontkenning: "niet" aan het einde van
    # de zinskern of "geen" vóór een gewoon zelfstandig naamwoord.
    if words.count('niet') > 1 or words.count('geen') > 1 or ('niet' in words and 'geen' in words):
        raise UnsupportedSentenceError('Gebruik één ontkenning: niet of geen, niet allebei.')
    negated = False
    if words and words[-1] == 'niet':
        words.pop()
        negated = True
    elif 'niet' in words:
        raise UnsupportedSentenceError("'Niet' hoort in deze eenvoudige zinnen aan het einde van de zinsdelen.")
    no_article = False
    if words and words[0] == 'geen':
        words.pop(0)
        negated = True
        no_article = True
    elif 'geen' in words:
        raise UnsupportedSentenceError("'Geen' hoort direct vóór het voorwerp.")

    article = None
    if words and words[0] in ('de','het','een'):
        article = words.pop(0)
    if no_article and article:
        raise UnsupportedSentenceError("Gebruik geen lidwoord na 'geen'.")
    obj = adjective = None
    if words:
        if len(words) > 2:
            raise UnsupportedSentenceError('Slechts één voorwerp met eventueel één bijvoeglijk naamwoord wordt ondersteund.')
        raw = words.pop()
        if raw in OBJECTS_NL:
            obj = OBJECTS_NL[raw]
        elif raw in NOUNS:
            obj = NOUNS[raw]
            if obj == 'Torelkiva':
                obj = 'torelkiva'
        else:
            raise UnsupportedSentenceError(f'Geen Torelkiva-woord voor {raw!r}.')
        if words:
            attr = words.pop()
            if attr not in ADJS:
                raise UnsupportedSentenceError(f'Geen Torelkiva-bijvoeglijk naamwoord voor {attr!r}.')
            adjective = ADJS[attr]
        if article in ('de','het') and obj not in OBJECTS_TK and obj != 'torelkiva' and article != GENDER_ARTICLE.get(obj):
            raise UnsupportedSentenceError(f"Onjuist lidwoord: gebruik {GENDER_ARTICLE.get(obj)!r} in plaats van {article!r}.")
        if (article or no_article) and (obj in OBJECTS_TK or obj == 'torelkiva'):
            raise UnsupportedSentenceError('Gebruik geen lidwoord of geen bij een voornaamwoord of eigennaam.')
        if adjective and (obj in OBJECTS_TK or obj == 'torelkiva'):
            raise UnsupportedSentenceError('Gebruik geen bijvoeglijk naamwoord bij een voornaamwoord of eigennaam.')
        if (article or no_article) and adjective:
            # Foute verbuigingen worden niet stilzwijgend vertaald.
            stem = NL_ADJ[adjective]
            needs_e = article in ('de','het') or ((article=='een' or no_article) and obj not in {'viro','sima','lavi','meva','mora','liri','pora'})
            expected = {'groot':'grote'}.get(stem, stem if stem.endswith('e') else stem+'e') if needs_e else stem
            if attr != expected:
                raise UnsupportedSentenceError(f'Onjuiste bijvoeglijke vorm: gebruik {expected!r}.')
    elif article or no_article:
        raise UnsupportedSentenceError('Na een lidwoord of geen moet een voorwerp staan.')

    if obj and obj not in OBJECTS_TK and obj != 'torelkiva' and not (article or no_article):
        raise UnsupportedSentenceError(
            'Gebruik bij zelfstandige naamwoorden de, het, een of geen. '
            'Zonder lidwoord is deze eenvoudige Nederlandse zin niet ondersteund.')

    if negated and obj and obj not in OBJECTS_TK and obj != 'torelkiva':
        if not no_article:
            # In de gecontroleerde taal worden ontkende zelfstandige naamwoorden
            # uitgedrukt met "geen", niet met "een/de/het ... niet".
            raise UnsupportedSentenceError("Gebruik 'geen [voorwerp]' bij een ontkend zelfstandig naamwoord.")
    if no_article and not obj:
        raise UnsupportedSentenceError("'Geen' vereist een voorwerp.")
    # 2.2: bewaar expliciete bepaaldheid wanneer die niet gelijk is aan de oude canon.
    # Dit laat 2.1-zinnen zonder da/en volledig bruikbaar.
    article_token = ''
    if article and obj not in OBJECTS_TK and obj != 'torelkiva':
        legacy = ARTICLES.get(obj, 'een')
        if article != legacy:
            article_token = 'en' if article == 'een' else 'da'
    _check_valency(verb, obj)
    return Parsed(subject,verb,obj,adjective,tense,negated,question,article_token)


def to_torelkiva(text: str) -> str:
    words, mark=_tokens(text)
    if words == ['hallo']:return 'Vema!'
    if words == ['tot','ziens']:return 'Savo!'
    p=parse_nederlands(text)
    out=[p.subject]
    if p.article_token: out.append(p.article_token)
    if p.adjective: out.append(p.adjective)
    if p.obj: out.append(p.obj+'em')
    if p.tense: out.append(p.tense)
    if p.negated: out.append('vo')
    out.append(p.verb)
    if p.question:out.append('ke')
    return ' '.join(out).capitalize() + ('?' if p.question else '.')


def main(argv: list[str]|None=None) -> int:
    p=argparse.ArgumentParser(description='Gecontroleerde Torelkiva-zinsvertaler 2.2 (beperkt domein)')
    p.add_argument('--van', choices=['nl','tk'], required=True)
    p.add_argument('zin', help='Vertaal één eenvoudige zin. Onbekende zinnen worden geweigerd.')
    args=p.parse_args(argv)
    try:
        print(to_torelkiva(args.zin) if args.van=='nl' else to_nederlands(args.zin))
        return 0
    except UnsupportedSentenceError as exc:
        p.exit(2, f'Niet ondersteund: {exc}\n')

if __name__=='__main__':
    raise SystemExit(main())
