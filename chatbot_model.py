from transformers import pipeline
import wikipedia

# Load a pretrained QA pipeline (DistilBERT fine-tuned on SQuAD)
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert-base-uncased-distilled-squad"
)

def get_response(question: str) -> str:
    question_clean = question.strip()
    if not question_clean:
        return "Please ask a question."

    # Definition-style queries: return summary directly
    lower_q = question_clean.lower()
    if lower_q.startswith(("what is", "define", "who is", "tell me about")):
        # Extract topic
        tokens = question_clean.split()
        if lower_q.startswith(("what is", "who is")) and len(tokens) > 2:
            topic = " ".join(tokens[2:])
        elif lower_q.startswith(("define", "tell me about")) and len(tokens) > 1:
            topic = " ".join(tokens[1:])
        else:
            topic = question_clean
        try:
            summary = wikipedia.summary(topic, sentences=2)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            # Pick the first disambiguated option
            try:
                return wikipedia.summary(e.options[0], sentences=2)
            except:
                return "I found multiple topics. Please be more specific."
        except Exception:
            return "Sorry, I couldn't find information on that topic."

    # For other questions: use QA pipeline with dynamic context
    try:
        context = wikipedia.summary(question_clean, sentences=5)
    except Exception:
        # Fallback context
        context = (
            "Photosynthesis is the process by which green plants use sunlight to synthesize food "
            "from carbon dioxide and water. It involves the green pigment chlorophyll "
            "and generates oxygen as a by-product."
        )

    result = qa_pipeline(question=question_clean, context=context)
    answer = result.get("answer", "")
    return answer or "I'm not sure about that."
