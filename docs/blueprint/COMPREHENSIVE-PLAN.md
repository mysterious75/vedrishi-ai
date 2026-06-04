# VEDRISHI AI - COMPREHENSIVE PLAN
> Security-first, zero-error, perfect system

---

## 📊 CURRENT STATUS

### Datasets Downloaded: 40+ | Size: 9.58 GB | Files: 45,036

| Category | Count | Status |
|----------|-------|--------|
| Scripture Texts | 15 | ✅ |
| Sanskrit NLP Data | 10 | ✅ |
| Competitor Projects | 8 | ✅ |
| Academic Corpora | 4 | ✅ |
| Linguistic Tools | 5 | ✅ |

### Issues Found:
1. **Encoding Issues**: Some Sanskrit text shows as `?` characters
2. **Empty Files**: 131 empty `__init__.py` files (normal for Python projects)

---

## 🎯 PHASE-WISE PLAN

### PHASE 1: DATA CLEANING & PREPARATION (Week 1)
**Goal**: Convert raw data to training-ready format

#### Step 1.1: Fix Encoding Issues
```bash
# Read files with correct encoding (UTF-8 with proper Sanskrit handling)
# Convert all JSON to JSONL with normalized Unicode
```

#### Step 1.2: Merge Datasets
- Combine all Gita sources (DharmicData + bhagavad-gita-dataset + gita)
- Combine all Ramayana sources
- Combine all Mahabharata sources
- Remove duplicates

#### Step 1.3: Clean Content
- Remove verses with encoding issues
- Remove duplicate verses
- Standardize format (Sanskrit + Hindi + English)
- Add metadata (chapter, verse number, theme tags)

#### Step 1.4: Generate Instruction Pairs
- Create 50,000+ Q&A pairs
- Format: `{"instruction": "...", "input": "...", "output": "..."}`
- Include tone tags (compassionate, practical, non-dogmatic)

#### Step 1.5: Quality Filter
- Remove toxic content
- Remove biased content (caste, gender)
- Remove fake verses
- Verify verse accuracy against sources

**Output**: `vedrishi_train.jsonl` (50K+ clean pairs)

---

### PHASE 2: MODEL TRAINING (Week 2)
**Goal**: Fine-tune Qwen 2.5 7B with spiritual knowledge

#### Step 2.1: Setup Training Environment
- Create Unsloth Cloud account
- Configure QLoRA parameters
- Set up system prompt for Ved Rishi persona

#### Step 2.2: Upload Dataset
- Upload `vedrishi_train.jsonl` to platform
- Verify data integrity
- Set train/validation split (90/10)

#### Step 2.3: Launch Training
- QLoRA fine-tuning (2-6 hours)
- Monitor loss metrics
- Save checkpoints

#### Step 2.4: Evaluate Model
- Test 100 queries for accuracy
- Check tone consistency (≥85%)
- Verify verse citations (≥92%)
- Safety compliance (100%)

**Output**: Fine-tuned VedRishi model

---

### PHASE 3: RAG SETUP (Week 2-3)
**Goal**: Ensure factual accuracy with verse retrieval

#### Step 3.1: Setup Vector Database
- Pinecone (free tier) or ChromaDB (self-hosted)
- Index all verses with embeddings

#### Step 3.2: Create Embeddings
- Use `paraphrase-multilingual-MiniLM-L12-v2`
- Embed all 300K+ verses
- Store with metadata

#### Step 3.3: Build Retrieval Pipeline
- User query → Embed → Search → Get top 5 verses → Generate response
- LangChain/LlamaIndex integration

#### Step 3.4: Test Accuracy
- Query: "गीता में कर्मयोग क्या है?"
- Expected: Correct chapter/verse citation
- Fail if: Wrong citation, hallucination

**Output**: RAG-enabled VedRishi model

---

### PHASE 4: SAFETY & GUARDRAILS (Week 3)
**Goal**: Zero harmful content, zero false information

#### Step 4.1: Content Guardrails
```
SYSTEM PROMPT:
तुम 'वेद ऋषि' हो। तुम्हारे नियम:
1. केवल सत्य ज्ञान दो - कभी झूठ मत बोलो
2. अगर श्लोक याद न आए, तो paraphrase करो और source बताओ
3. कभी भी चिकित्सा, कानूनी, या वित्तीय सलाह मत दो
4. आत्महत्या/हिंसा की बात पर तुरंत हेल्पलाइन दो
5. अंधविश्वास मत फैलाओ
6. हर उत्तर में disclaimer दो
```

#### Step 4.2: Technical Guardrails
- **NeMo Guardrails**: NVIDIA's safety framework
- **Input Validation**: Sanitize all user inputs
- **Output Validation**: Check for harmful content before sending
- **Rate Limiting**: Prevent abuse (3 queries/day free)

#### Step 4.3: Legal Compliance
- **Disclaimer on every page**: "AI spiritual assistant, not a real guru"
- **Disclaimer in every response**: "Yeh ek AI guide hai"
- **Privacy Policy**: GDPR compliant
- **Terms of Service**: Clear usage terms

#### Step 4.4: Crisis Handling
```
IF user mentions self-harm/suicide:
  → Show empathy
  → Provide helpline numbers
  → Do NOT give advice
  → Recommend professional help

IF user asks for medical/legal/financial advice:
  → Redirect to qualified professional
  → Do NOT give specific advice
```

**Output**: Safe, compliant VedRishi system

---

### PHASE 5: MVP BUILD (Week 3-4)
**Goal**: Launch basic product for testing

#### Step 5.1: Backend API
- FastAPI server
- JWT authentication
- Rate limiting
- Error handling
- Logging (no PII)

#### Step 5.2: Frontend (Web)
- Next.js/React
- Chat interface
- Daily shloka display
- Mobile responsive

#### Step 5.3: WhatsApp Bot (Optional)
- Twilio integration
- Basic Q&A flow

#### Step 5.4: Payment Integration
- Razorpay (India)
- Stripe (Global)
- Digital Dakshina button

**Output**: Working MVP (Web + API)

---

### PHASE 6: TESTING & QA (Week 4-5)
**Goal**: Zero bugs, zero security issues

#### Step 6.1: Security Testing
- SQL injection tests
- XSS prevention
- CSRF protection
- Input sanitization
- API key security

#### Step 6.2: Content Testing
- 500+ test queries
- Verse accuracy verification
- Tone consistency check
- Safety compliance check

#### Step 6.3: Load Testing
- Concurrent user simulation
- Response time monitoring
- Error rate tracking

#### Step 6.4: User Testing
- 50 beta users
- Feedback collection
- Bug fixes
- Iteration

**Output**: Production-ready MVP

---

### PHASE 7: LAUNCH (Week 5-6)
**Goal**: Public launch with marketing

#### Step 7.1: Pre-Launch
- Social media accounts setup
- Content creation (Reels, posts)
- Landing page

#### Step 7.2: Beta Launch
- 100 beta users
- Monitor metrics
- Collect feedback

#### Step 7.3: Full Launch
- Instagram Reels
- YouTube Shorts
- Reddit posts
- Hindu community groups

#### Step 7.4: Post-Launch
- User support
- Bug fixes
- Feature iteration

**Output**: Live product with users

---

### PHASE 8: MONETIZATION (Week 6-8)
**Goal**: Start earning revenue

#### Step 8.1: Subscription System
- Free tier: 3 questions/day
- Premium ₹199/month: Unlimited
- Premium ₹299/month: Family plan

#### Step 8.2: Digital Dakshina
- Micro-donation button (₹11-101)
- After helpful responses

#### Step 8.3: E-Commerce
- Rudraksha, pooja samagri
- Affiliate links (Amazon/Flipkart)
- 5-15% commission

#### Step 8.4: Kundali (Premium)
- Basic Kundali: ₹99
- Detailed Kundali: ₹299

**Output**: Revenue-generating product

---

## 🔒 SECURITY PLAN

### Data Security
| Measure | Implementation |
|---------|----------------|
| **Encryption at Rest** | AES-256 for all stored data |
| **Encryption in Transit** | TLS 1.3 for all API calls |
| **API Keys** | Environment variables, never in code |
| **Database** | Row-level security, no SQL injection |
| **User Data** | Anonymized logs, no PII |
| **Backups** | Daily encrypted backups |

### Application Security
| Measure | Implementation |
|---------|----------------|
| **Input Validation** | Sanitize all user inputs |
| **Output Validation** | Check AI responses before sending |
| **Rate Limiting** | Prevent abuse (3/day free, unlimited premium) |
| **Authentication** | JWT + refresh tokens |
| **CORS** | Strict origin restrictions |
| **Headers** | Security headers (CSP, X-Frame-Options) |

### AI Security
| Measure | Implementation |
|---------|----------------|
| **Hallucination Prevention** | RAG + verse verification |
| **Content Guardrails** | NeMo Guardrails framework |
| **Toxicity Filter** | Remove harmful content |
| **False Information** | Verify against source texts |
| **Disclaimer** | Every response includes AI disclaimer |

### Legal Security
| Measure | Implementation |
|---------|----------------|
| **Privacy Policy** | GDPR compliant |
| **Terms of Service** | Clear usage terms |
| **AI Disclosure** | "This is AI, not a real guru" |
| **Crisis Handling** | Helpline redirect for self-harm |
| **Content Restrictions** | No medical/legal/financial advice |

---

## 📊 SUCCESS METRICS

### Technical Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Verse Citation Accuracy | ≥92% | Manual audit vs source texts |
| Response Relevance | ≥88% | Embedding similarity |
| Safety Compliance | 100% | Automated + manual review |
| Response Latency | <6 sec | Cloud benchmarking |
| Uptime | 99.9% | Monitoring tools |

### Business Metrics
| Metric | Target | Timeline |
|--------|--------|----------|
| Beta Users | 100 | Week 5 |
| Monthly Active Users | 1,000 | Month 3 |
| Premium Conversion | 8% | Month 3 |
| Monthly Revenue | ₹50,000 | Month 6 |
| User Satisfaction | ≥4.2/5 | Ongoing |

---

## 💰 BUDGET

### One-Time Costs
| Item | Cost |
|------|------|
| Dataset (Free APIs) | ₹0 |
| Training (QLoRA) | ₹5,000-20,000 |
| Domain Name | ₹500-1,000 |
| **Total One-Time** | **₹5,500-21,000** |

### Monthly Costs
| Item | Cost |
|------|------|
| Hosting (Vercel/Railway) | ₹0-5,000 |
| Voice (ElevenLabs) | ₹0-2,000 |
| Payment Gateway | 2% per transaction |
| Monitoring | ₹0-1,000 |
| **Total Monthly** | **₹0-8,000** |

---

## 📅 TIMELINE

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1 | Data Cleaning | `vedrishi_train.jsonl` |
| 2 | Model Training | Fine-tuned model |
| 2-3 | RAG Setup | RAG-enabled model |
| 3 | Safety | Guardrails active |
| 3-4 | MVP Build | Working web app |
| 4-5 | Testing | Production-ready |
| 5-6 | Launch | Public beta |
| 6-8 | Monetization | Revenue started |

---

## ⚠️ RISKS & MITIGATION

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hallucination | High | RAG mandatory, verse verification |
| Legal Issues | High | Strict guardrails, disclaimers |
| Low Quality | Medium | Evaluation framework, human review |
| Cost Overrun | Medium | Free tiers, monitor usage |
| Competition | Low | Unique value (Hindi+comprehensive) |

---

## 🎯 IMMEDIATE NEXT STEPS

1. **Fix encoding issues** in downloaded datasets
2. **Merge and clean** all Gita sources
3. **Generate instruction pairs** (50K+)
4. **Quality filter** all content
5. **Start training** when ready

Kya main Phase 1 (Data Cleaning) shuru karun? 🚀
