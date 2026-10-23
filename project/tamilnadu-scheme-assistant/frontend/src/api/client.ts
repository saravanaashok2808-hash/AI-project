import type { QueryRequest, QueryResponse, Scheme, SchemeEligibility, UserProfile } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://ai-project-792f.onrender.com';

function mapBackendScheme(s: any): Scheme {
  const benefitsList = s.benefits ? Object.values(s.benefits).map(String) : [];
  const officialLink = (s.official_urls && s.official_urls.length > 0) 
    ? s.official_urls[0] 
    : 'https://www.tn.gov.in';
  const lastVerified = (s.source_metadata && s.source_metadata.last_verified) 
    ? s.source_metadata.last_verified 
    : '2026-10-01';

  return {
    id: s.scheme_id || '',
    name_en: s.scheme_name_english || '',
    name_ta: s.scheme_name_tamil || '',
    department: s.department || '',
    benefits_en: benefitsList,
    benefits_ta: benefitsList,
    eligibility_en: s.matched_criteria || [],
    eligibility_ta: s.matched_criteria || [],
    documents_en: s.required_documents || [],
    documents_ta: s.required_documents || [],
    application_steps_en: s.application_steps || [],
    application_steps_ta: s.application_steps || [],
    official_link: officialLink,
    last_verified_date: lastVerified,
  };
}

export class ApiClient {
  static getAuthToken(): string | null {
    return localStorage.getItem('tn_auth_token');
  }

  static setAuthToken(token: string): void {
    localStorage.setItem('tn_auth_token', token);
  }

  static clearAuth(): void {
    localStorage.removeItem('tn_auth_token');
  }

  static getGeminiApiKey(): string | null {
    return localStorage.getItem('tn_gemini_api_key');
  }

  static setGeminiApiKey(key: string): void {
    localStorage.setItem('tn_gemini_api_key', key.trim());
  }

  static clearGeminiApiKey(): void {
    localStorage.removeItem('tn_gemini_api_key');
  }

  static async validateGeminiKey(apiKey: string): Promise<{ valid: boolean; error?: string; model?: string }> {
    const response = await fetch(`${API_BASE_URL}/api/query/validate-gemini`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key: apiKey }),
    });
    if (!response.ok) {
      return { valid: false, error: `Server error: ${response.status}` };
    }
    return await response.json();
  }

  static getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    const token = ApiClient.getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  static async register(payload: {
    name: string;
    password: string;
    phone?: string;
    email?: string;
    age?: number;
    gender?: string;
    district?: string;
    profile_data?: any;
  }): Promise<{ access_token: string; user: any }> {
    const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Registration failed' }));
      throw new Error(err.detail || 'Registration failed');
    }

    const data = await response.json();
    if (data.access_token) {
      ApiClient.setAuthToken(data.access_token);
    }
    return data;
  }

  static async login(identifier: string, password: string): Promise<{ access_token: string; user: any }> {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identifier, password }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Invalid credentials' }));
      throw new Error(err.detail || 'Invalid credentials');
    }

    const data = await response.json();
    if (data.access_token) {
      ApiClient.setAuthToken(data.access_token);
    }
    return data;
  }

  static async getMe(): Promise<{ id: string; name: string; phone?: string; profile: UserProfile }> {
    const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
      method: 'GET',
      headers: ApiClient.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Authentication expired: ${response.status}`);
    }

    return await response.json();
  }

  static async updateProfile(profile: UserProfile): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/auth/profile`, {
      method: 'PUT',
      headers: ApiClient.getAuthHeaders(),
      body: JSON.stringify({ profile_data: profile }),
    });

    if (!response.ok) {
      throw new Error(`Failed to update profile: ${response.status}`);
    }

    return await response.json();
  }

  static async query(request: QueryRequest): Promise<QueryResponse> {
    const isTa = request.language === 'ta';
    
    // Map request to backend model
    const geminiKey = ApiClient.getGeminiApiKey();
    const payload = {
      query: request.query,
      language: request.language === 'ta-en' ? null : request.language,
      session_id: request.session_id,
      gemini_api_key: geminiKey || undefined,
      history: request.history || undefined,
      profile_updates: request.user_profile ? {
        name: request.user_profile.name,
        age: request.user_profile.age,
        gender: request.user_profile.gender,
        district: request.user_profile.district,
        education_level: request.user_profile.education_level,
        employment_status: request.user_profile.employment_status,
        occupation: request.user_profile.occupation,
        annual_income: request.user_profile.income,
        marital_status: request.user_profile.marital_status,
        community: request.user_profile.caste_category,
        is_differently_abled: request.user_profile.disability
      } : null
    };

    const response = await fetch(`${API_BASE_URL}/api/query/`, {
      method: 'POST',
      headers: ApiClient.getAuthHeaders(),
      body: JSON.stringify(payload),
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();

    const schemes: Scheme[] = (data.schemes || []).map(mapBackendScheme);

    const eligibility_checks: SchemeEligibility[] = (data.eligibility_summaries || []).map((e: any) => ({
      scheme_id: e.scheme_id,
      status: e.status,
      reason_en: e.reasoning_english || '',
      reason_ta: e.reasoning_tamil || ''
    }));

    const extracted_profile: UserProfile = {
      ...request.user_profile,
      age: data.extracted_entities?.age ?? request.user_profile?.age,
      gender: data.extracted_entities?.gender ?? request.user_profile?.gender,
      district: data.extracted_entities?.district ?? request.user_profile?.district,
      occupation: data.extracted_entities?.occupation ?? request.user_profile?.occupation,
      employment_status: data.extracted_entities?.employment_status ?? request.user_profile?.employment_status,
      education_level: data.extracted_entities?.education_level ?? request.user_profile?.education_level,
    };

    const answer_text = (data.detected_language === 'ta' || isTa) 
      ? (data.response_text_tamil || data.response_text_english || '') 
      : (data.response_text_english || data.response_text_tamil || '');

    return {
      answer_text,
      language: data.detected_language || 'en',
      schemes,
      eligibility_checks,
      extracted_profile
    };
  }

  static async synthesizeSpeech(text: string, language: string = 'ta', gender: string = 'female'): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/api/voice/tts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, language, gender })
    });
    if (!response.ok) {
      throw new Error(`TTS synthesis error: ${response.status}`);
    }
    const blob = await response.blob();
    return URL.createObjectURL(blob);
  }

  static async getSchemes(): Promise<Scheme[]> {
    const response = await fetch(`${API_BASE_URL}/api/schemes/`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    const list = await response.json();
    return list.map(mapBackendScheme);
  }

  static async getScheme(id: string): Promise<Scheme> {
    const response = await fetch(`${API_BASE_URL}/api/schemes/${id}`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    const item = await response.json();
    return mapBackendScheme(item);
  }

  static async checkEligibility(profile: UserProfile, schemeId: string): Promise<SchemeEligibility> {
    const response = await fetch(`${API_BASE_URL}/api/eligibility/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ profile, scheme_id: schemeId }),
    });
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    const data = await response.json();
    return {
      scheme_id: data.scheme_id,
      status: data.status,
      reason_en: data.reasoning_english,
      reason_ta: data.reasoning_tamil
    };
  }
}
