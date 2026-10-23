# User Flows

## 1. First-time Tamil voice user seeking schemes (e.g., Lakshmi)
1. **Entry:** User opens the app.
2. **Action:** User taps the prominent Microphone icon and speaks: "மகளிர் உரிமை தொகை எப்படி வாங்குவது?"
3. **Processing:**
   - ASR captures audio and transcodes to Tamil text.
   - Classifier detects Intent = "Scheme Information".
   - System queries Vector DB (RAG) for "Kalaignar Magalir Urimai Thogai".
   - LLM generates a simple Tamil response.
4. **Output:** System reads the response aloud using TTS and displays large text.
5. **Next Step:** System asks a follow-up: "உங்களுக்கு வேறு ஏதேனும் சந்தேகம் உள்ளதா?" (Do you have any other doubts?).

## 2. English text user checking eligibility (e.g., Meena)
1. **Entry:** User opens the app and selects Text input.
2. **Action:** User types: "Am I eligible for Pudhumai Penn scheme?"
3. **Processing:**
   - LLM recognizes missing context (no profile data).
4. **Output:** "To check your eligibility for the Pudhumai Penn scheme, could you tell me if you studied in a Government School in Tamil Nadu from classes 6 to 12, and are currently pursuing a UG degree?"
5. **Action:** User replies: "Yes, I studied in a Govt school and doing B.Sc."
6. **Processing:** LLM extracts profile data -> Updates Session State -> Evaluates Rules.
7. **Output:** "Yes, you are eligible! You will receive ₹1,000 per month. Here is the application link: [link] and the required documents: Aadhar, Bank Passbook, 12th Marksheet."

## 3. Tanglish user discovering farmer schemes (e.g., Karthik)
1. **Entry:** User types: "farmer ku enna scheme iruku"
2. **Processing:**
   - Language detection flags "Tanglish" / Latin script.
   - Vector search maps query to Agricultural schemes.
   - LLM processes retrieved context.
3. **Output:** LLM replies in a mix of English/Tanglish or plain English depending on preference, listing top 3 schemes (e.g., Uzhavar Pathukappu Thittam, PM-KISAN).
4. **Action:** User clicks on "Uzhavar Pathukappu Thittam" to see details.

## 4. Follow-up questions flow
1. **Context:** User just asked about CMCHIS (Health Insurance).
2. **Action:** User asks: "How long does it take to get the card?"
3. **Processing:** LLM uses conversational memory to understand "the card" refers to the CMCHIS card.
4. **Output:** System provides the timeframe based on RAG context for CMCHIS.

## 5. Missing information flow
1. **Action:** User asks: "Can I get free housing?"
2. **Processing:** System retrieves Housing schemes but sees criteria: Income limit, marital status, land ownership.
3. **Output:** "There are a few housing schemes like the Chief Minister's Solar Powered Green House Scheme. To see which one fits, what is your annual family income and do you currently own any concrete house?"

## 6. Error recovery flows
*   **ASR Failure:**
    *   *Trigger:* User speaks but background noise ruins transcription.
    *   *Output:* "மன்னிக்கவும், நீங்கள் சொன்னது தெளிவாக கேட்கவில்லை. மீண்டும் கூற முடியுமா?" (Sorry, I couldn't hear clearly. Can you say that again?)
*   **No schemes found:**
    *   *Trigger:* User asks for a scheme that doesn't exist (e.g., "Free cars for students").
    *   *Output:* "Sorry, I couldn't find any official Tamil Nadu government scheme providing free cars for students. However, there are schemes for free bicycles and laptops. Would you like to know about those?"
*   **Ambiguous query:**
    *   *Trigger:* User just says "Money".
    *   *Output:* "Could you please tell me what kind of financial assistance you are looking for? For example, are you looking for student scholarships, farmer assistance, or old age pension?"

## 7. Language switching flow
1. **Action:** User asks a question in Tamil text, then switches to English in the next turn.
2. **Processing:** System detects language change automatically on the backend using `lingua-py` or Unicode detection.
3. **Output:** System seamlessly responds in English for the new turn, maintaining session context.

## 8. Profile update flow
1. **Action:** User says "I am 65 years old now."
2. **Processing:** LLM extracts age = 65, updates session memory.
3. **Output:** System acknowledges: "I've noted that you are 65 years old. This makes you eligible for Senior Citizen benefits. Would you like to see schemes for seniors?"
