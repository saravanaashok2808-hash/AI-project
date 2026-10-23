# 01 — Problem Definition

## The Information Gap

### Core Problem
Millions of people in Tamil Nadu are potentially eligible for government welfare schemes but **do not know about them, cannot find clear information, or struggle to understand eligibility criteria**.

### Specific Problems

#### 1. Information Fragmentation
- Government scheme information is scattered across **dozens of department websites**
- No single portal provides comprehensive, searchable Tamil Nadu scheme data
- Information exists in PDFs, HTML pages, government orders, and circulars
- Different departments use different formats and update schedules

#### 2. Language Barrier
- Most digital tools are English-first
- Tamil-speaking users, especially in rural areas, find English interfaces inaccessible
- Tanglish (Tamil-English mix) is the natural communication mode for millions but is not supported by any government tool
- Even Tamil content on government sites uses formal/literary Tamil that may be unfamiliar to conversational speakers

#### 3. Digital Literacy Gap
- Many potential beneficiaries are unfamiliar with web portals and search engines
- Text-heavy government websites are not designed for voice-first interaction
- Elderly users, rural users, and users with limited education face significant access barriers

#### 4. Eligibility Confusion
- Eligibility criteria are often complex with multiple conditions
- Users cannot easily determine if they qualify
- No existing system explains *why* someone does or does not meet criteria
- Users often discover only one scheme when they may qualify for several

#### 5. Outdated Information
- Scheme details change with budget announcements, policy updates, and government orders
- Information on unofficial websites may be months or years out of date
- No system tracks source freshness or flags potentially outdated information

#### 6. Trust Deficit
- Users encounter conflicting information from different sources
- AI chatbots may hallucinate scheme details that don't exist
- No existing system provides source citations with verification dates

---

## Existing Solutions and Their Limitations

### MyScheme (myscheme.gov.in)
| Aspect | Assessment |
|--------|-----------|
| **Strengths** | Comprehensive, government-maintained, eligibility logic built-in |
| **Weaknesses** | English-heavy, no voice support, no Tanglish, no conversational interface |
| **Tamil support** | Limited — some scheme names in Tamil but interface is English |
| **Voice** | None |
| **Tanglish** | None |
| **Explainability** | Shows eligible/not eligible but limited explanation |

### Tamil Nadu e-Sevai (tnesevai.tn.gov.in)
| Aspect | Assessment |
|--------|-----------|
| **Strengths** | Official TN portal, application submission |
| **Weaknesses** | Not a scheme discovery tool, complex navigation |
| **Tamil support** | Yes, but formal Tamil |
| **Voice** | None |
| **Explanation** | None — it's an application portal, not a guidance system |

### CM Helpline (cmhelpline.tn.gov.in)
| Aspect | Assessment |
|--------|-----------|
| **Strengths** | Integrated complaint/tracking system |
| **Weaknesses** | Grievance-focused, not scheme discovery |
| **Tamil support** | Yes |
| **Voice** | Phone-based only |

### Generic AI Chatbots (ChatGPT, etc.)
| Aspect | Assessment |
|--------|-----------|
| **Strengths** | Natural language, multilingual |
| **Weaknesses** | **Hallucinate scheme details**, no verified data, no source citations, require paid API |
| **Tamil** | Variable quality |
| **Trust** | Cannot be trusted for factual scheme information |
| **Cost** | Paid APIs |

---

## Our Proposed Solution

A **Tamil-first, voice-enabled, RAG-grounded government scheme assistant** that:

1. **Speaks Tamil** — Natural Tamil voice interaction, not just translated English
2. **Understands Tanglish** — "farmer-ku enna scheme?" is a valid query
3. **Grounds in verified data** — Every scheme fact comes from official sources
4. **Explains eligibility** — Shows matched, failed, and missing criteria
5. **Identifies missing info** — Asks only the minimum necessary follow-up
6. **Provides sources** — Every recommendation links to official pages
7. **Tracks freshness** — Shows when information was last verified
8. **Runs free** — ₹0 core cost, works on a student laptop
9. **Respects privacy** — No permanent personal data storage

---

## Target Population

### Tamil Nadu Demographics (Relevant Context)
- **Population**: ~80 million
- **Languages**: Tamil (official), English (widely used in education/business)
- **Rural population**: ~51%
- **Internet users**: Growing rapidly, mobile-first
- **Smartphone penetration**: Significant and increasing

### Primary Target Users

#### Persona 1: Rural Tamil Speaker
- **Age**: 45-65
- **Language**: Tamil only, some spoken Tanglish
- **Digital literacy**: Low
- **Need**: Discover pension, agricultural, welfare schemes
- **Challenge**: Cannot navigate English websites

#### Persona 2: Young Job Seeker
- **Age**: 18-25
- **Language**: Tanglish, English
- **Digital literacy**: High
- **Need**: Education, employment, skill development schemes
- **Challenge**: Doesn't know which schemes exist

#### Persona 3: Working Woman
- **Age**: 25-40
- **Language**: Tamil, some English
- **Digital literacy**: Medium
- **Need**: Women's welfare schemes, health insurance, family benefits
- **Challenge**: Time-constrained, prefers voice interaction

#### Persona 4: Farmer
- **Age**: 30-55
- **Language**: Tamil
- **Digital literacy**: Low-Medium
- **Need**: Agricultural subsidies, crop insurance, farmer welfare
- **Challenge**: Seasonal urgency, complex eligibility

#### Persona 5: Senior Citizen
- **Age**: 60+
- **Language**: Tamil
- **Digital literacy**: Very low
- **Need**: Pension, health, disability schemes
- **Challenge**: Physical and digital accessibility

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Scheme retrieval accuracy (Recall@5) | ≥ 80% |
| Eligibility assessment accuracy | ≥ 85% |
| Tamil ASR accuracy (WER) | ≤ 25% |
| English ASR accuracy (WER) | ≤ 15% |
| Response time (text query → response) | ≤ 10 seconds |
| Source citation rate | 100% (every scheme fact cited) |
| Hallucination rate | ≤ 5% |
| Core cost | ₹0 |
