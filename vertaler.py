#!/usr/bin/env python3
"""Gecontroleerde zinsvertaler Nederlands <-> Torelkiva 2.0.

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

SUBJECTS_NL = {'ik': 'mi', 'jij': 'ti', 'je': 'ti', 'wij': 'miva', 'we': 'miva', 'hij': 'ela', 'zij': 'tira'}
SUBJECTS_TK = {'mi':'Ik', 'ti':'Jij', 'miva':'Wij', 'ela':'Hij', 'tira':'Zij'}
OBJECTS_NL = {'mij':'mi', 'me':'mi', 'jou':'ti', 'je':'ti', 'ons':'miva', 'hem':'ela', 'hen':'tira'}
OBJECTS_TK = {'mi':'mij', 'ti':'jou', 'miva':'ons', 'ela':'hem/haar', 'tira':'hen'}

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
PRON = {'mi':0, 'ti':1, 'miva':2, 'ela':1, 'tira':2}
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
        raise UnsupportedSentenceError('Begin met mi, ti, miva, ela of tira.')
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
    return Parsed(subject, verb, obj, adjective, tense, negated, question or mark == '?')


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
            article = ARTICLES.get(p.obj,'een')
            adj = NL_ADJ.get(p.adjective,'')
            if adj:
                # Onbepaald het-woord: een nieuw boek, geen *nieuwe boek*.
                het_woorden = {'viro','sima','lavi','meva','mora','liri','pora'}
                needs_e = article in ('de', 'het') or (article == 'een' and p.obj not in het_woorden)
                if needs_e and not adj.endswith('e'): adj += 'e'
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
        finite = ('wil' if p.subject=='ela' and p.verb=='laki' else (ik,jij,plural)[i])
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
    words, mark = _tokens(text)
    if words in (['hallo'],['tot','ziens']):
        raise UnsupportedSentenceError('Groeten worden afzonderlijk verwerkt.')
    question = mark == '?'
    if question:
        # Nederlandse inversie. Bij 'jij' vervalt de -t in het heden.
        if len(words)<2 or words[1] not in SUBJECTS_NL:
            raise UnsupportedSentenceError('Gebruik voor vragen bijvoorbeeld: "Begrijp jij mij?"')
        verb_word=words.pop(0)
        subject=SUBJECTS_NL[words.pop(0)]
        if verb_word in ('zal','zul','zullen'):
            expected = 'zullen' if subject in ('miva','tira') else ('zul' if subject=='ti' else 'zal')
            if verb_word != expected or not words:
                raise UnsupportedSentenceError('Gebruik de correcte toekomstige vraagvorm.')
            inf=words.pop()
            matches=[k for k,v in VERBS.items() if inf==v[0]]
            if len(matches)!=1:
                raise UnsupportedSentenceError('Toekomstig werkwoord is onbekend.')
            verb=matches[0];tense='sa'
        else:
            matching=[]
            i=PRON[subject]
            for code, forms in VERBS.items():
                present = ('wil' if subject=='ela' and code=='laki' else (forms[1] if subject=='ti' else forms[1+i]))
                if verb_word==present:
                    matching.append((code,''))
                past_form=forms[5] if i==2 else forms[4]
                if verb_word==past_form:
                    matching.append((code,'na'))
            matching=list(set(matching))
            if len(matching)!=1:
                raise UnsupportedSentenceError('Werkwoord van deze vraag niet eenduidig.')
            verb,tense=matching[0]
    else:
        if words[0] not in SUBJECTS_NL:
            raise UnsupportedSentenceError('Gebruik als onderwerp: ik, jij, hij of wij.')
        subject=SUBJECTS_NL[words.pop(0)]
        if not words: raise UnsupportedSentenceError('Een zin heeft een werkwoord nodig.')
        verb_word=words.pop(0)
        tense='sa' if verb_word in ('zal','zult','zullen') else ''
        if tense:
            expected_future='zullen' if subject in ('miva','tira') else ('zult' if subject=='ti' else 'zal')
            if verb_word != expected_future:
                raise UnsupportedSentenceError('Gebruik de correcte vorm: zal, zult of zullen.')
            if not words: raise UnsupportedSentenceError('Een toekomstige zin heeft een infinitief nodig.')
            verb_word=words.pop()
        matching = []
        for code, forms in VERBS.items():
            if tense=='sa' and verb_word==forms[0]: matching.append((code,'sa'))
            if tense!='sa':
                for form, t in [(forms[1],''),(forms[2],''),(forms[3],''),(forms[4],'na'),(forms[5],'na')]:
                    if verb_word==form:matching.append((code,t))
        matching = list(set(matching))
        i = PRON[subject]
        # 'Ik schrijft' en 'wij loopt' mogen niet stilzwijgend worden vertaald.
        matching = [(code,t) for code,t in matching if (
            (tense == 'sa' and verb_word == VERBS[code][0]) or
            (tense != 'sa' and verb_word == (
                 VERBS[code][5 if i == 2 else 4] if t == 'na'
                 else ('wil' if subject=='ela' and code=='laki' else VERBS[code][1+i])
            ))
        )]
        if len(matching)!=1:
            raise UnsupportedSentenceError('Onbekend of dubbelzinnig werkwoord; gebruik een voorbeeldzin uit de gids.')
        verb,tense=matching[0]
    negated = False
    if 'niet' in words:
        words.remove('niet'); negated=True
    if 'geen' in words:
        words.remove('geen');negated=True
    if words and words[0] in ('de','het','een'):
        words.pop(0)
    obj=adjective=None
    if words:
        if len(words)>2:
            raise UnsupportedSentenceError('Slechts één voorwerp met eventueel één bijvoeglijk naamwoord wordt ondersteund.')
        raw=words.pop()
        if raw in OBJECTS_NL:
            obj=OBJECTS_NL[raw]
        elif raw in NOUNS:
            obj=NOUNS[raw]
            if obj == 'Torelkiva': obj='torelkiva'
        else:
            raise UnsupportedSentenceError(f'Geen Torelkiva-woord voor {raw!r}.')
        if words:
            raw=words.pop()
            if raw not in ADJS:
                raise UnsupportedSentenceError(f'Geen Torelkiva-bijvoeglijk naamwoord voor {raw!r}.')
            adjective=ADJS[raw]
    return Parsed(subject,verb,obj,adjective,tense,negated,question)


def to_torelkiva(text: str) -> str:
    words, mark=_tokens(text)
    if words == ['hallo']:return 'Vema!'
    if words == ['tot','ziens']:return 'Savo!'
    p=parse_nederlands(text)
    out=[p.subject]
    if p.adjective: out.append(p.adjective)
    if p.obj: out.append(p.obj+'em')
    if p.tense: out.append(p.tense)
    if p.negated: out.append('vo')
    out.append(p.verb)
    if p.question:out.append('ke')
    return ' '.join(out).capitalize() + ('?' if p.question else '.')


def main(argv: list[str]|None=None) -> int:
    p=argparse.ArgumentParser(description='Gecontroleerde Torelkiva-zinsvertaler 2.0 (beperkt domein)')
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
