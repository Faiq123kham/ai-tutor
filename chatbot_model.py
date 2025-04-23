from transformers import pipeline
import wikipedia
from typing import List, Optional

# Load pipelines: QA for definitions, and a text-generation model for chat
qa_pipeline = pipeline(
    'question-answering',
    model='distilbert-base-uncased-distilled-squad'
)
chat_pipeline = pipeline(
    'text-generation',
    model='microsoft/DialoGPT-medium'
)

# Helper: fetch contexts from Wikipedia

def get_contexts(topic: str, top_k: int = 2) -> List[str]:
    pages = wikipedia.search(topic, results=top_k)
    contexts: List[str] = []
    for title in pages:
        try:
            contexts.append(wikipedia.summary(title, sentences=3))
        except Exception:
            continue
    return contexts or ["No context available."]

# Main response function with ML/NLP conversational model

def get_response(question: str, history: Optional[List[dict]] = None) -> str:
    question_clean = question.strip()
    if not question_clean:
        return "Please ask a question."

    lower_q = question_clean.lower()
    definition_triggers = (
        "what is", "define", "who is", "tell me about",
        "explain", "describe"
    )

    # Definition queries: use wiki summary + QA
    for trig in definition_triggers:
        if lower_q.startswith(trig):
            topic = question_clean[len(trig):].strip(' ?') or question_clean
            try:
                return wikipedia.summary(topic, sentences=3)
            except wikipedia.exceptions.DisambiguationError as e:
                options = e.options[:5]
                return f"Your query could refer to: {', '.join(options)}. Please specify."
            except Exception:
                # If summary fails, use QA on fetched contexts
                contexts = get_contexts(topic)
                combined_context = ' '.join(contexts)
                res = qa_pipeline(question=question_clean, context=combined_context)
                return res.get('answer', "I don't know.")

    # Non-definition queries: use text-generation model
    # Build a prompt including recent history
    prompt = ''
    if history:
        for h in history[-5:]:
            prompt += f"User: {h['user']} Bot: {h['bot']}"
    prompt += f"User: {question_clean} Bot:"

    # Generate a reply
    # Ensure the model can generate beyond the prompt by setting pad_token_id
    generated = chat_pipeline(
        prompt,
        max_length=len(prompt.split()) + 50,
        pad_token_id=chat_pipeline.tokenizer.eos_token_id
    )[0]['generated_text']

    # Extract the text after the prompt
    reply = generated[len(prompt):].strip()
    return reply or "I'm not sure about that."
