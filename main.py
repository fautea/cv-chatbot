from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Chargement du CV au démarrage
def load_cv():
    try:
        with open("cv.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "CV non trouvé. Veuillez créer un fichier cv.txt."

CV_CONTENT = load_cv()

SYSTEM_PROMPT = f"""
Tu es un assistant personnel et professionnel représentant le propriétaire de ce CV.
Tu réponds aux questions des recruteurs et visiteurs de manière chaleureuse, concise et professionnelle.

Règles importantes :
- Base-toi UNIQUEMENT sur les informations du CV ci-dessous
- Si une information n'est pas dans le CV, dis-le honnêtement sans inventer
- Réponds toujours en français sauf si on te parle dans une autre langue
- Sois enthousiaste et mets en valeur les points forts du candidat
- Reste concis (3-5 phrases maximum par réponse)

=== CV ===
{CV_CONTENT}
==========
"""

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Stockage des conversations par session (en mémoire)
conversations: dict = {}

class MessageRequest(BaseModel):
    session_id: str
    message: str

class MessageResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message vide")

    # Initialiser l'historique si nouvelle session
    if request.session_id not in conversations:
        conversations[request.session_id] = []

    history = conversations[request.session_id]

    # Ajouter le message utilisateur
    history.append({
        "role": "user",
        "content": request.message
    })

    # Appel à l'API Claude
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=history
    )

    assistant_message = response.content[0].text

    # Sauvegarder la réponse
    history.append({
        "role": "assistant",
        "content": assistant_message
    })

    # Limiter l'historique à 20 messages pour éviter les dépassements
    if len(history) > 20:
        conversations[request.session_id] = history[-20:]

    return MessageResponse(response=assistant_message)

@app.delete("/api/chat/{session_id}")
async def clear_conversation(session_id: str):
    if session_id in conversations:
        del conversations[session_id]
    return {"status": "cleared"}

# Servir les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")
