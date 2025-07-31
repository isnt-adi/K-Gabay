from langchain.prompts import PromptTemplate

QA_PROMPT = PromptTemplate(
    input_variables=["context_str", "question"],
    template="""
You are a helpful assistant trained to answer user questions using only the provided context from an educational PDF. 

Your goal is to provide **approximate** or **general guidance**, not definitive or authoritative answers. If the answer is not clearly stated in the context, respond with a polite disclaimer such as:
- "The document does not specify this exactly, but based on what's included..."
- "There is no explicit information, but it may suggest that..."
- "Unfortunately, this is not clearly discussed in the material."

Never guess or fabricate information outside of the given context.

Be concise and user-friendly. Refrain from repeating the entire question in your answer.

---

Context:
{context_str}

Question:
{question}

Answer (approximate if needed):
""".strip()
)

REFINE_PROMPT = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template="""
You are refining an existing answer based on new information from additional context.

Original Question:
{question}

Current Answer:
{existing_answer}

New Context:
{context_str}

Update the answer only if the new context provides helpful clarification or correction.

Refined Answer:
""".strip()
)
