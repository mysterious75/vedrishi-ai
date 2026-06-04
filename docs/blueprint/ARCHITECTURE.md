# VEDRISHI AI - TECHNICAL ARCHITECTURE

## SYSTEM OVERVIEW
```
User Input → API Gateway → Fine-tuned Model (Qwen 2.5 7B)
                              ↓
                         RAG System (Pinecone/ChromaDB)
                              ↓
                         Guardrails Filter
                              ↓
                    Response + Disclaimer
```

## COMPONENTS

### 1. AI Model Layer
- **Base Model**: Qwen 2.5 7B Instruct
- **Fine-Tuning**: QLoRA (4-bit quantization)
- **Training Data**: 15k-25k instruction pairs from scriptures
- **Platform**: Unsloth Cloud / Together AI (free tier)

### 2. RAG (Retrieval-Augmented Generation)
- **Vector DB**: Pinecone (free tier) or ChromaDB (self-hosted)
- **Embedding**: paraphrase-multilingual-MiniLM-L12-v2
- **Data**: Bhagavad Gita, Upanishads, Ramayana verses
- **Purpose**: Verse citation accuracy 92%+

### 3. Guardrails Layer
- **Safety Filter**: Block self-harm, violence, fraud queries
- **Tone Filter**: Ensure compassionate, non-prescriptive responses
- **Caste/Gender Filter**: Remove discriminatory content
- **Disclaimer**: Every response mein AI disclaimer

### 4. API Layer
- **Backend**: Python FastAPI (free, fast, secure)
- **Auth**: JWT tokens for user sessions
- **Rate Limiting**: Free users - 3 queries/day
- **Database**: PostgreSQL (user data, conversations)

### 5. Frontend
- **Web**: React.js / Next.js
- **Mobile**: React Native (cross-platform)
- **WhatsApp Bot**: Twilio API (free tier)

### 6. Voice Integration
- **TTS**: ElevenLabs API (Hindi voice)
- **STT**: OpenAI Whisper (free, self-hosted)
- **Avatar**: Static Rishi image (Midjourney generated)

### 7. Payment
- **India**: Razorpay
- **Global**: Stripe
- **Micro-donations**: In-app purchase

## SECURITY MEASURES
1. **Data Encryption**: AES-256 at rest, TLS 1.3 in transit
2. **Input Validation**: Sanitize all user inputs
3. **Rate Limiting**: Prevent abuse
4. **Authentication**: JWT + refresh tokens
5. **Database**: Row-level security, no SQL injection
6. **API Keys**: Environment variables, never in code
7. **Logs**: No PII in logs, anonymized user data
8. **Compliance**: GDPR (global users), India IT Act

## DEPLOYMENT
- **Model**: HuggingFace Inference / Together AI
- **Backend**: Railway / Render (free tier)
- **Frontend**: Vercel (free tier)
- **Database**: Supabase (free tier)
- **CDN**: Cloudflare (free tier)

## MONITORING
- **Uptime**: UptimeRobot (free)
- **Errors**: Sentry (free tier)
- **Analytics**: Plausible (privacy-friendly)
- **Feedback**: In-app rating system
