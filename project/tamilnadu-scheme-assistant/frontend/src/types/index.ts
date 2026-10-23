export interface Scheme {
  id: string;
  name_en: string;
  name_ta: string;
  department: string;
  benefits_en: string[];
  benefits_ta: string[];
  eligibility_en: string[];
  eligibility_ta: string[];
  documents_en: string[];
  documents_ta: string[];
  application_steps_en: string[];
  application_steps_ta: string[];
  official_link: string;
  last_verified_date: string;
}

export type EligibilityStatus = 'ELIGIBLE' | 'POTENTIALLY_ELIGIBLE' | 'NOT_APPEARING_ELIGIBLE' | 'INSUFFICIENT';

export interface SchemeEligibility {
  scheme_id: string;
  status: EligibilityStatus;
  reason_en: string;
  reason_ta: string;
}

export interface UserProfile {
  name?: string;
  phone?: string;
  email?: string;
  age?: number;
  gender?: string;
  district?: string;
  education_level?: string;
  employment_status?: string;
  occupation?: string;
  income?: number;
  marital_status?: string;
  caste_category?: string;
  disability?: boolean;
  voice_gender?: 'female' | 'male';
}

export interface QueryRequest {
  query: string;
  language: 'ta' | 'en' | 'ta-en'; // auto detected ideally
  session_id?: string;
  user_profile?: UserProfile;
  history?: Array<{ role: 'user' | 'assistant'; content: string }>;
}

export interface QueryResponse {
  answer_text: string;
  language: string;
  schemes: Scheme[];
  eligibility_checks: SchemeEligibility[];
  extracted_profile: UserProfile;
}

export const TN_DISTRICTS = [
  'Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri',
  'Dindigul', 'Erode', 'Kallakurichi', 'Kancheepuram', 'Kanyakumari', 'Karur',
  'Krishnagiri', 'Madurai', 'Mayiladuthurai', 'Nagapattinam', 'Namakkal', 'Nilgiris',
  'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga',
  'Tenkasi', 'Thanjavur', 'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli',
  'Tirupathur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore',
  'Viluppuram', 'Virudhunagar'
];
