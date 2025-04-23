# AI Tutor Chatbot

## 🔍 Problem
Many students lack access to 24/7 tutoring support. This chatbot offers instant academic help.

## 🤖 AI Approach
- Uses a pretrained transformer model (`distilbert-base-uncased-distilled-squad`) for question answering.  
- The model processes a static `context` or can be extended to search larger text.

## 🛠 Key Features
- Interactive web-based chat UI.  
- Real NLP-based answers from a pretrained model.  
- Easy to extend context or connect to a document database.

## ⚠️ Limitations
- Limited to the static `context` provided.  
- Not fine-tuned on domain-specific curricula.  
- Cannot handle image or complex multi-step problems yet.

## 🚀 Running Locally
See **Installation & Setup** above.

## 💡 Next Steps
- Load multiple contexts or a CSV/DB of Q&A pairs.  
- Add user authentication and personalized learning paths.  
- Deploy publicly using Heroku, Render, or Docker.