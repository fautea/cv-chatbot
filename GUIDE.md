# 🤖 Guide complet — Chatbot CV avec IA

## Architecture du projet

```
cv-chatbot/
├── main.py           ← Serveur FastAPI (backend)
├── cv.txt            ← Ton CV (à personnaliser !)
├── requirements.txt  ← Dépendances Python
├── .env.example      ← Modèle pour la clé API
├── .env              ← Ta vraie clé API (ne jamais committer !)
└── static/
    └── index.html    ← Interface web moderne
```

---

## ÉTAPE 1 — Prérequis

### 1.1 Installer Python
Vérifie que Python 3.10+ est installé :
```bash
python --version
```
Si non installé : https://www.python.org/downloads/

### 1.2 Obtenir une clé API Anthropic
1. Va sur https://console.anthropic.com
2. Crée un compte (ou connecte-toi)
3. Va dans **API Keys** → **Create Key**
4. Copie la clé (elle commence par `sk-ant-...`)
5. Note : Anthropic offre des crédits gratuits au démarrage (~$5)

---

## ÉTAPE 2 — Installation en local

### 2.1 Créer le dossier du projet
```bash
mkdir cv-chatbot
cd cv-chatbot
```

### 2.2 Créer un environnement virtuel
```bash
python -m venv venv

# Sur Mac/Linux :
source venv/bin/activate

# Sur Windows :
venv\Scripts\activate
```

### 2.3 Créer les fichiers
Copie tous les fichiers fournis dans le dossier (main.py, cv.txt, requirements.txt, static/index.html).

```bash
mkdir static  # Créer le dossier pour l'interface web
```

### 2.4 Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2.5 Configurer la clé API
```bash
# Copier le fichier exemple
cp .env.example .env

# Ouvrir .env et remplacer "ta_clé_api_ici" par ta vraie clé
# Exemple : ANTHROPIC_API_KEY=sk-ant-api03-xxxxx...
```

### 2.6 Personnaliser ton CV
Ouvre `cv.txt` et **remplace tout le contenu** par ton vrai CV.
Plus tu mets d'informations, meilleures seront les réponses !

**Astuce :** Structure bien ton cv.txt avec des sections claires :
```
=== EXPÉRIENCES ===
...
=== COMPÉTENCES ===
...
=== FORMATION ===
...
=== DISPONIBILITÉ & PRÉTENTIONS ===
...
```

---

## ÉTAPE 3 — Lancer en local

```bash
uvicorn main:app --reload --port 8000
```

Ouvre ton navigateur sur : **http://localhost:8000**

✅ Tu devrais voir l'interface du chatbot !

Pour tester, pose des questions comme :
- "Quelles sont tes compétences ?"
- "Parle-moi de ton expérience chez TechCorp"
- "Est-il disponible immédiatement ?"

---

## ÉTAPE 4 — Déploiement gratuit sur Render

### 4.1 Préparer Git
```bash
# Initialiser un dépôt Git
git init

# Créer un .gitignore pour ne pas exposer ta clé API
echo ".env" > .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore

# Ajouter tous les fichiers
git add .
git commit -m "Initial commit — CV Chatbot"
```

### 4.2 Pousser sur GitHub
1. Va sur https://github.com → **New repository**
2. Nomme-le `cv-chatbot` → **Create repository**
3. Suis les instructions GitHub pour lier ton dépôt local :
```bash
git remote add origin https://github.com/TON_USERNAME/cv-chatbot.git
git branch -M main
git push -u origin main
```

### 4.3 Déployer sur Render (gratuit)
1. Va sur https://render.com → **Sign Up** (gratuit)
2. Clique sur **New** → **Web Service**
3. Connecte ton compte GitHub et sélectionne `cv-chatbot`
4. Configure le service :
   - **Name** : `mon-cv-chatbot`
   - **Runtime** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type** : `Free`
5. Dans **Environment Variables**, ajoute :
   - Key : `ANTHROPIC_API_KEY`
   - Value : ta clé API (celle qui commence par `sk-ant-...`)
6. Clique **Create Web Service**

⏳ Le déploiement prend 2-3 minutes. Tu recevras une URL du type :
**https://mon-cv-chatbot.onrender.com**

---

## ÉTAPE 5 — Personnalisation avancée (optionnel)

### Changer le nom affiché
Dans `static/index.html`, cherche et remplace :
```html
<h1>Mon Assistant CV</h1>
```
par :
```html
<h1>Assistant de Jean Dupont</h1>
```

### Modifier les questions suggérées
Dans `static/index.html`, modifie les `.suggestion-chip` :
```html
<span class="suggestion-chip" onclick="sendSuggestion(this)">
  💼 Ta question personnalisée ?
</span>
```

### Enrichir le prompt système
Dans `main.py`, tu peux ajouter des règles dans `SYSTEM_PROMPT` :
```python
SYSTEM_PROMPT = f"""
...
- Si un recruteur demande à te contacter, fournis l'email : jean@email.com
- Si on parle anglais, réponds en anglais
- Mets toujours en avant les 3 forces principales : Python, React, et l'IA
...
"""
```

---

## Résolution des problèmes fréquents

**❌ "ModuleNotFoundError"**
→ Vérifie que l'environnement virtuel est activé (`source venv/bin/activate`)

**❌ "AuthenticationError"**
→ Ta clé API est invalide ou manquante dans le fichier `.env`

**❌ "FileNotFoundError: cv.txt"**
→ Assure-toi que `cv.txt` est à la racine du projet (pas dans `static/`)

**❌ Sur Render, le service s'endort**
→ Le plan gratuit de Render met le service en veille après 15min d'inactivité.
   La première requête prendra ~30 secondes à se réveiller. C'est normal !

---

## Coût estimé

| Usage | Coût Claude API |
|-------|----------------|
| 100 conversations/mois | ~$0.50 |
| 500 conversations/mois | ~$2.50 |
| Usage normal d'un portfolio | < $5/mois |

Render est entièrement **gratuit** pour ce type d'usage.

---

## Récapitulatif des commandes

```bash
# Installation
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Lancement local
uvicorn main:app --reload --port 8000

# Git & déploiement
git add . && git commit -m "update" && git push
```
