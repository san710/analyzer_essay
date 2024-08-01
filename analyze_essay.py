import language_tool_python
import gensim
from gensim import corpora
from collections import defaultdict
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

# List of common abbreviations to ignore
abbreviations = {"e.g.", "i.e.", "etc.", "Mr.", "Mrs.", "Dr.", "Prof."}

def check_grammar(text):
    try:
        tool_gb = language_tool_python.LanguageToolPublicAPI('en-GB')
        tool_us = language_tool_python.LanguageToolPublicAPI('en-US')
    except language_tool_python.LanguageToolError:
        return [{"message": "LanguageTool server error", "offset": 0, "length": 0, "context": "", "replacements": []}]

    matches_gb = tool_gb.check(text)
    matches_us = tool_us.check(text)

    errors = []

    # Convert matches to a set of error spans
    errors_gb = {match.context[match.offset:match.offset + match.errorLength] for match in matches_gb if match.context[match.offset:match.offset + match.errorLength] not in abbreviations}
    errors_us = {match.context[match.offset:match.offset + match.errorLength] for match in matches_us if match.context[match.offset:match.offset + match.errorLength] not in abbreviations}

    # Consider errors only if they appear in both GB and US lists
    common_errors = errors_gb & errors_us

    # Add common errors to the error list
    for match in matches_gb + matches_us:
        error_span = match.context[match.offset:match.offset + match.errorLength]
        if error_span in common_errors:
            error_message = match.message
            if match.replacements:
                error_message += f" '{error_span}' should be '{match.replacements[0]}'"
            error = {
                "message": error_message,
                "offset": match.offset,
                "length": match.errorLength,
                "context": match.context,
                "replacements": match.replacements
            }
            if not any(e['offset'] == error['offset'] and e['length'] == error['length'] for e in errors):
                errors.append(error)

    return errors

def identify_redundant_phrases(text):
    doc = nlp(text)
    errors = []
    matcher = Matcher(nlp.vocab)

    # Define redundant phrase patterns
    redundant_patterns = [
        [{"LOWER": "for"}, {"LOWER": "instance"}, {"TEXT": {"REGEX": ",? e.g\\."}}],
        [{"LOWER": "in"}, {"LOWER": "addition"}, {"TEXT": {"REGEX": ",? i.e\\."}}],
        [{"LOWER": "for"}, {"LOWER": "example"}, {"TEXT": {"REGEX": ",? e.g\\."}}],
        [{"LOWER": "that"}, {"LOWER": "is"}, {"TEXT": {"REGEX": ",? i.e\\."}}],
        [{"LOWER": "in"}, {"LOWER": "conclusion"}, {"TEXT": {"REGEX": ",? to conclude"}}],
        [{"LOWER": "firstly"}, {"LOWER": "first"}],
        [{"LOWER": "secondly"}, {"LOWER": "second"}]
    ]

    for pattern in redundant_patterns:
        matcher.add("REDUNDANT_PHRASE", [pattern])

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        errors.append({
            "message": f"Redundant phrase detected: '{span.text}'. Consider revising.",
            "offset": span.start_char,
            "length": len(span.text),
            "context": text[max(0, span.start_char-30):min(len(text), span.end_char+30)],
            "replacements": [span.text]
        })

    return errors

def identify_topics(text):
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in [text]]
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    # Avoid filtering out all words
    texts = [[token for token in text if frequency[token] > 1 or frequency[token] == 1] for text in texts]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    if len(corpus[0]) == 0:
        return [("No topics identified", 0.0)]
    lda = gensim.models.ldamodel.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=15)
    topics = lda.print_topics(num_words=4)
    return topics

def score_essay(text, errors):
    score = 20  # start with a perfect score
    error_penalty = len(errors) * 0.5  # penalize 0.5 points per error
    final_score = max(0, score - error_penalty)
    return final_score

def score_relevance(text, context):
    doc1 = nlp(context)
    doc2 = nlp(text)
    relevance_score = doc1.similarity(doc2) * 10  # Scale similarity to 10
    return round(relevance_score, 2)

def analyze_essay(text, context):
    grammar_errors = check_grammar(text)
    phrase_errors = identify_redundant_phrases(text)
    errors = grammar_errors + phrase_errors
    topics = identify_topics(text)
    grammar_score = score_essay(text, errors)
    relevance_score = score_relevance(text, context)

    # Calculate total score with a penalty if word count is below 300
    word_count = len(text.split())
    total_score = grammar_score + relevance_score
    if word_count < 300:
        total_score -= 10  # Apply a 10 marks penalty

    return {
        "original_text": text,
        "errors": errors,
        "topics": topics,
        "grammar_score": grammar_score,
        "relevance_score": relevance_score,
        "total_score": total_score,
    }