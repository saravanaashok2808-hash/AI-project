import React, { useState, useRef, useEffect, useMemo } from 'react';
import { 
  Send, Menu, Loader2, Home, Volume2, VolumeX, User, LogOut, Edit3, Sparkles, 
  CheckCircle2, AlertCircle, X, Bot, Columns2, Maximize2, Search, 
  Filter, GraduationCap, Briefcase, Heart, Sprout, Building2, Layers
} from 'lucide-react';
import { ApiClient } from '../api/client';
import type { QueryRequest, UserProfile, Scheme } from '../types';
import { SchemeCard } from './SchemeCard';
import { AudioRecorder } from './AudioRecorder';
import { ProfileSidebar } from './ProfileSidebar';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  schemes?: Scheme[];
  eligibilityData?: any;
}

interface AssistantPageProps {
  language: 'ta' | 'en';
  initialProfile: UserProfile;
  onHome: () => void;
  onEditProfile: () => void;
  onLogout: () => void;
}

type CategoryFilter = 'all' | 'eligible' | 'education' | 'women' | 'business' | 'agriculture' | 'health';

export const AssistantPage: React.FC<AssistantPageProps> = ({
  language: initialLang,
  initialProfile,
  onHome,
  onEditProfile,
  onLogout
}) => {
  const [language, setLanguage] = useState<'ta' | 'en'>(initialLang);
  const [userProfile, setUserProfile] = useState<UserProfile>(initialProfile);
  const [voiceGender, setVoiceGender] = useState<'female' | 'male'>(initialProfile.voice_gender || 'female');
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const citizenName = userProfile.name || (initialLang === 'ta' ? 'அன்பரே' : 'Citizen');

  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'assistant',
      text: initialLang === 'ta' 
        ? `வணக்கம் ${citizenName}! நான் உங்கள் 'அரசு நண்பன்' (AI நலத்திட்ட வழிகாட்டி). உங்கள் சுயவிவரத்தின்படி (வயது: ${userProfile.age || 24}, கல்வி: ${userProfile.education_level || 'பட்டதாரி'}, மாவட்டம்: ${userProfile.district || 'தமிழ்நாடு'}) உங்களுக்குப் பொருத்தமான அரசு நலத்திட்டங்களை ஆய்வு செய்து வலதுபுறப் பலகையில் கொடுத்துள்ளேன். உங்களுக்கு என்ன உதவி தேவை என்பதை தாராளமாக கேட்கலாம்!`
        : `Welcome ${citizenName}! I am 'Arasu Nanban', your Government Scheme AI Guide. Based on your profile (Age: ${userProfile.age || 24}, Education: ${userProfile.education_level || 'Graduate'}, District: ${userProfile.district || 'Tamil Nadu'}), I have evaluated verified welfare schemes for you on the right side hub. Feel free to speak or ask anything!`,
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const baseInputRef = useRef<string>('');
  const requestIdRef = useRef<number>(0);
  const [micStatus, setMicStatus] = useState<string | null>(null);

  // Landscape & Hub State
  const [activeSchemes, setActiveSchemes] = useState<Scheme[]>([]);
  const [activeEligibilityData, setActiveEligibilityData] = useState<any[]>([]);
  const [isSplitLayout, setIsSplitLayout] = useState(true);
  const [mobileTab, setMobileTab] = useState<'chat' | 'schemes'>('chat');
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>('all');
  const [searchFilter, setSearchFilter] = useState('');

  // Google Gemini AI Key configuration modal state
  const [showGeminiModal, setShowGeminiModal] = useState(false);
  const [geminiKeyInput, setGeminiKeyInput] = useState(() => ApiClient.getGeminiApiKey() || '');
  const [hasGeminiKey, setHasGeminiKey] = useState(() => !!ApiClient.getGeminiApiKey());
  const [isValidatingGemini, setIsValidatingGemini] = useState(false);
  const [geminiStatusMsg, setGeminiStatusMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleSaveGeminiKey = async () => {
    const trimmed = geminiKeyInput.trim();
    if (!trimmed) {
      ApiClient.clearGeminiApiKey();
      setHasGeminiKey(false);
      setGeminiStatusMsg({ type: 'success', text: isTa ? 'API சாவி நீக்கப்பட்டது' : 'API Key removed' });
      return;
    }
    setIsValidatingGemini(true);
    setGeminiStatusMsg(null);
    try {
      const result = await ApiClient.validateGeminiKey(trimmed);
      if (result.valid) {
        ApiClient.setGeminiApiKey(trimmed);
        setHasGeminiKey(true);
        setGeminiStatusMsg({
          type: 'success',
          text: isTa ? 'கூகிள் ஜெமினி AI வெற்றிகரமாக இணைக்கப்பட்டது!' : 'Google Gemini AI successfully connected!'
        });
        setTimeout(() => {
          setShowGeminiModal(false);
          setGeminiStatusMsg(null);
        }, 1200);
      } else {
        setGeminiStatusMsg({
          type: 'error',
          text: result.error || (isTa ? 'செல்லுபடியாகாத சாவி' : 'Invalid API Key')
        });
      }
    } catch (err: any) {
      setGeminiStatusMsg({
        type: 'error',
        text: err.message || (isTa ? 'சரிபார்ப்பு தோல்வியடைந்தது' : 'Validation failed')
      });
    } finally {
      setIsValidatingGemini(false);
    }
  };

  const [fetchError, setFetchError] = useState(false);
  const [sessionId] = useState(() => Math.random().toString(36).substring(7));
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [autoSpeak, setAutoSpeak] = useState(true);
  const [isVoiceRecording, setIsVoiceRecording] = useState(false);
  const [voiceLang, setVoiceLang] = useState<'ta-IN' | 'en-IN'>(language === 'ta' ? 'ta-IN' : 'en-IN');

  useEffect(() => {
    setVoiceLang(language === 'ta' ? 'ta-IN' : 'en-IN');
  }, [language]);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const isTa = language === 'ta';
  const hasInitializedRef = useRef(false);
  const currentSpeechIdRef = useRef(0);

  // Stop any playing audio
  const stopAllAudio = () => {
    currentSpeechIdRef.current++;
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current = null;
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsPlayingAudio(false);
  };

  // Fallback to browser synthesis
  const fallbackSpeech = (text: string, lang: 'ta' | 'en') => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang === 'ta' ? 'ta-IN' : 'en-IN';
      utterance.rate = 0.95;
      utterance.onend = () => setIsPlayingAudio(false);
      utterance.onerror = () => setIsPlayingAudio(false);
      setIsPlayingAudio(true);
      window.speechSynthesis.speak(utterance);
    }
  };

  // High-Quality Studio Neural Human TTS
  const speakText = async (text: string, lang?: 'ta' | 'en') => {
    const thisSpeechId = ++currentSpeechIdRef.current;
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }

    setIsPlayingAudio(true);
    const targetLang = (lang || language) === 'ta' ? 'ta' : 'en';

    try {
      const audioUrl = await ApiClient.synthesizeSpeech(text, targetLang, voiceGender);
      if (currentSpeechIdRef.current !== thisSpeechId) return;

      const audio = new Audio(audioUrl);
      audioRef.current = audio;
      audio.onended = () => {
        if (currentSpeechIdRef.current === thisSpeechId) {
          setIsPlayingAudio(false);
        }
      };
      audio.onerror = () => {
        if (currentSpeechIdRef.current === thisSpeechId) {
          setIsPlayingAudio(false);
          fallbackSpeech(text, targetLang);
        }
      };
      await audio.play();
    } catch (err) {
      if (currentSpeechIdRef.current !== thisSpeechId) return;
      console.warn('Backend neural TTS unavailable, using browser speech synthesis:', err);
      fallbackSpeech(text, targetLang);
    }
  };

  // Initial load: Fetch customized schemes automatically
  const fetchInitialSchemes = async () => {
    setIsLoading(true);
    setFetchError(false);
    try {
      const queryText = isTa 
        ? `என் வயது ${userProfile.age || 24}, ${userProfile.education_level || 'பட்டதாரி'}, ${userProfile.employment_status || 'வேலை தேடுபவர்'}. எனக்கு ஏற்ற திட்டங்கள் எவை?`
        : `Schemes suitable for my profile: age ${userProfile.age || 24}, ${userProfile.education_level || 'graduate'}, ${userProfile.employment_status || 'unemployed'}`;

      const req: QueryRequest = {
        query: queryText,
        language: isTa ? 'ta' : 'en',
        session_id: sessionId,
        user_profile: userProfile
      };

      const response = await ApiClient.query(req);

      setMessages([
        {
          id: '1',
          sender: 'assistant',
          text: response.answer_text || (isTa 
            ? `வணக்கம் ${citizenName}! உங்கள் சுயவிவரத்தின்படி (${userProfile.age ? `வயது: ${userProfile.age}, ` : ''}${userProfile.education_level ? `கல்வி: ${userProfile.education_level}, ` : ''}${userProfile.district ? `மாவட்டம்: ${userProfile.district}` : ''}) தகுதியான அரசு நலத்திட்டங்கள் மதிப்பீடு செய்யப்பட்டு வலதுபுற பலகையில் கொடுக்கப்பட்டுள்ளன:`
            : `Welcome ${citizenName}! Based on your profile (${userProfile.age ? `Age: ${userProfile.age}, ` : ''}${userProfile.education_level ? `Education: ${userProfile.education_level}, ` : ''}${userProfile.district ? `District: ${userProfile.district}` : ''}), here are the welfare schemes evaluated for you in the side panel:`),
          schemes: response.schemes,
          eligibilityData: response.eligibility_checks
        }
      ]);

      if (response.schemes && response.schemes.length > 0) {
        setActiveSchemes(response.schemes);
        setActiveEligibilityData(response.eligibility_checks || []);
      }

      if (autoSpeak && response.answer_text) {
        speakText(response.answer_text, response.language as 'ta' | 'en');
      }
    } catch (e) {
      console.error('Initial scheme fetch failed:', e);
      setFetchError(true);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!hasInitializedRef.current) {
      hasInitializedRef.current = true;
      fetchInitialSchemes();
    }

    return () => {
      stopAllAudio();
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleVoiceStart = () => {
    baseInputRef.current = input.trim();
    setMicStatus(null);
  };

  const handleVoiceTranscription = (transcript: string) => {
    if (!transcript) return;
    const base = baseInputRef.current;
    setInput(base ? `${base} ${transcript}` : transcript);
    setMicStatus(null);
    inputRef.current?.focus();
  };

  const handleSend = async (customText?: string) => {
    if (isLoading) return;
    const textToSend = (typeof customText === 'string' ? customText : input).trim();
    if (!textToSend) return;

    // Switch mobile view back to chat when user sends
    setMobileTab('chat');

    // Build multi-turn history from current messages
    const historyPayload = messages
      .filter(m => m.text && m.text.trim())
      .slice(-8)
      .map(m => ({
        role: (m.sender === 'user' ? 'user' : 'assistant') as 'user' | 'assistant',
        content: m.text
      }));

    const userMessage: Message = { id: Date.now().toString(), sender: 'user', text: textToSend };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setMicStatus(null);

    const thisRequestId = ++requestIdRef.current;

    try {
      const req: QueryRequest = {
        query: textToSend,
        language: 'ta-en',
        session_id: sessionId,
        user_profile: userProfile,
        history: historyPayload
      };

      const response = await ApiClient.query(req);

      if (thisRequestId !== requestIdRef.current) return;

      if (response.extracted_profile) {
        setUserProfile(response.extracted_profile);
      }
      
      if (response.language === 'ta' || response.language === 'en') {
        setLanguage(response.language as 'ta' | 'en');
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: response.answer_text,
        schemes: response.schemes,
        eligibilityData: response.eligibility_checks
      };

      setMessages(prev => [...prev, assistantMessage]);

      if (response.schemes && response.schemes.length > 0) {
        setActiveSchemes(response.schemes);
        setActiveEligibilityData(response.eligibility_checks || []);
      }

      if (autoSpeak && response.answer_text) {
        speakText(response.answer_text, response.language as 'ta' | 'en');
      }

    } catch (error) {
      if (thisRequestId !== requestIdRef.current) return;
      console.error(error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: isTa ? 'மன்னிக்கவும், பிழை ஏற்பட்டுள்ளது. மீண்டும் முயற்சிக்கவும்.' : 'Sorry, an error occurred. Please try again.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      if (thisRequestId === requestIdRef.current) {
        setIsLoading(false);
      }
    }
  };

  const handleClearSession = () => {
    setUserProfile({});
    setActiveSchemes([]);
    setActiveEligibilityData([]);
    setMessages([
      {
        id: Date.now().toString(),
        sender: 'assistant',
        text: isTa ? 'உங்கள் தரவுகள் அழிக்கப்பட்டன. புதிதாக தொடங்குவோம்.' : 'Your data has been cleared. Let\'s start fresh.',
      }
    ]);
    setSidebarOpen(false);
  };

  // Filter schemes in the landscape hub
  const filteredSchemes = useMemo(() => {
    return activeSchemes.filter(s => {
      // 1. Text search filter
      if (searchFilter.trim()) {
        const query = searchFilter.toLowerCase().trim();
        const matchesName = (s.name_en || '').toLowerCase().includes(query) || (s.name_ta || '').toLowerCase().includes(query);
        const matchesDept = (s.department || '').toLowerCase().includes(query);
        const matchesBenefits = (s.benefits_en || []).some(b => b.toLowerCase().includes(query)) || (s.benefits_ta || []).some(b => b.toLowerCase().includes(query));
        if (!matchesName && !matchesDept && !matchesBenefits) {
          return false;
        }
      }

      // 2. Category pill filter
      if (categoryFilter === 'all') return true;

      const elig = activeEligibilityData.find((e: any) => e.scheme_id === s.id);
      if (categoryFilter === 'eligible') {
        return elig?.status === 'ELIGIBLE';
      }

      const combined = `${s.name_en} ${s.name_ta} ${s.department} ${(s.benefits_en || []).join(' ')}`.toLowerCase();

      if (categoryFilter === 'education') {
        return combined.includes('kalvi') || combined.includes('கல்வி') || combined.includes('school') || combined.includes('college') || combined.includes('student') || combined.includes('scholarship') || combined.includes('முதல்வன்') || combined.includes('பட்டதாரி');
      }
      if (categoryFilter === 'women') {
        return combined.includes('women') || combined.includes('மகளிர்') || combined.includes('பெண்') || combined.includes('maternity') || combined.includes('urimai') || combined.includes('விதவை');
      }
      if (categoryFilter === 'business') {
        return combined.includes('business') || combined.includes('loan') || combined.includes('subsidy') || combined.includes('கடன்') || combined.includes('மானியம்') || combined.includes('தொழில்') || combined.includes('uyegp') || combined.includes('needs');
      }
      if (categoryFilter === 'agriculture') {
        return combined.includes('farmer') || combined.includes('agriculture') || combined.includes('விவசாய') || combined.includes('உழவர்') || combined.includes('பயிர்') || combined.includes('pmfby');
      }
      if (categoryFilter === 'health') {
        return combined.includes('health') || combined.includes('medical') || combined.includes('மருத்துவ') || combined.includes('காப்பீடு') || combined.includes('cmchis') || combined.includes('மருந்து');
      }

      return true;
    });
  }, [activeSchemes, activeEligibilityData, categoryFilter, searchFilter]);

  // Quick prompt chips
  const quickChips = isTa ? [
    { label: '🎓 கல்லூரி மாணவர் உதவித்தொகை', query: 'கல்லூரி மாணவர்களுக்கான அரசு உதவித்தொகை திட்டங்கள் எவை?' },
    { label: '💼 மகளிர் உரிமைத் தொகை', query: 'கலைஞர் மகளிர் உரிமைத் திட்டத்திற்கு எப்படி விண்ணப்பிப்பது?' },
    { label: '🌾 விவசாயிகள் நலத்திட்டம்', query: 'விவசாயிகளுக்கான மானியம் மற்றும் கடன் திட்டங்கள் என்னென்ன?' },
    { label: '🚀 சுயதொழில் கடன்', query: 'சுயதொழில் மற்றும் புதிய வணிகம் தொடங்க அரசு மானியம் உண்டா?' },
  ] : [
    { label: '🎓 Student Scholarships', query: 'What scholarships are available for college students?' },
    { label: '💼 Women Rights Scheme', query: 'How to apply for Kalaignar Magalir Urimai Thogai?' },
    { label: '🌾 Farmers Welfare', query: 'What agricultural loan and subsidy schemes exist?' },
    { label: '🚀 Self-Employment Loan', query: 'Government subsidy schemes for starting a small business?' },
  ];

  return (
    <div className="flex flex-col h-screen bg-[#f8fafc] text-slate-800 relative overflow-hidden font-sans">
      
      {/* Ambient background glows */}
      <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-teal-500/5 rounded-full blur-3xl pointer-events-none" />

      {/* Top Glassmorphic Navigation Header */}
      <header className="bg-white/85 backdrop-blur-xl border-b border-white/80 px-3.5 sm:px-6 py-2.5 sm:py-3 shadow-xs flex justify-between items-center z-30 shrink-0">
        
        {/* Left: Brand Emblem & Citizen Pill */}
        <div className="flex items-center gap-3">
          <button 
            type="button"
            onClick={onHome} 
            className="p-2 hover:bg-slate-100/80 active:scale-95 rounded-2xl transition-all text-slate-600 hover:text-slate-900 cursor-pointer"
            title={isTa ? 'முகப்பு' : 'Home'}
          >
            <Home size={19} />
          </button>

          <div className="w-9 h-9 rounded-full overflow-hidden flex items-center justify-center shrink-0 shadow-md shadow-emerald-900/10 ring-2 ring-emerald-600/20 bg-white">
            <img src="/tn-logo.png" alt="Tamil Nadu Government SchemeVoice" className="w-full h-full object-cover" />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-extrabold text-sm sm:text-base text-slate-900 leading-tight">
                {isTa ? 'தமிழ்நாடு அரசுத் திட்ட வழிகாட்டி' : 'SchemeVoice AI'}
              </h1>
              <span className="text-[10px] bg-emerald-100/90 text-emerald-800 font-bold px-2 py-0.5 rounded-full border border-emerald-200/80">
                Landscape AI
              </span>
            </div>
            <div className="hidden sm:flex items-center gap-1.5 text-[11px] text-emerald-800 font-semibold mt-0.5">
              <User size={11} className="text-emerald-600" />
              <span>{userProfile.name || (isTa ? 'குடிமக்கள்' : 'Citizen')}, {userProfile.age || 24}y • {userProfile.district || (isTa ? 'தமிழ்நாடு' : 'Tamil Nadu')}</span>
            </div>
          </div>
        </div>
        
        {/* Right: Controls & Preferences */}
        <div className="flex items-center gap-1.5 sm:gap-2">

          {/* Desktop Landscape Dual-Pane Mode Switcher */}
          <button
            type="button"
            onClick={() => setIsSplitLayout(!isSplitLayout)}
            className={`hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-2xl text-xs font-bold border transition-all cursor-pointer active:scale-95 ${
              isSplitLayout
                ? 'bg-emerald-50 text-emerald-900 border-emerald-300 shadow-xs ring-1 ring-emerald-500/15'
                : 'bg-white/80 hover:bg-white text-slate-700 border-slate-200 shadow-xs'
            }`}
            title={isSplitLayout ? (isTa ? 'அரட்டை மட்டும் காட்டுக' : 'Switch to Focused View') : (isTa ? 'பக்கவாட்டு இரு-பலகை காட்சி (Landscape)' : 'Switch to Split Landscape View')}
          >
            {isSplitLayout ? <Columns2 size={14} className="text-emerald-700" /> : <Maximize2 size={14} className="text-slate-500" />}
            <span>{isSplitLayout ? (isTa ? 'பக்கவாட்டு பலகை' : 'Split View') : (isTa ? 'முழு அரட்டை' : 'Full Chat')}</span>
          </button>
          
          {/* Gemini AI Status Pill */}
          <button
            type="button"
            onClick={() => setShowGeminiModal(true)}
            className={`px-2.5 sm:px-3 py-1.5 rounded-2xl transition-all flex items-center gap-1.5 text-xs font-bold border cursor-pointer active:scale-95 ${
              hasGeminiKey
                ? 'bg-emerald-50 text-emerald-800 border-emerald-300 shadow-xs ring-1 ring-emerald-500/10'
                : 'bg-white/80 hover:bg-white text-slate-700 border-slate-200/80 shadow-xs'
            }`}
            title={hasGeminiKey ? (isTa ? 'ஜெமினி AI இணைக்கப்பட்டுள்ளது' : 'Google Gemini AI Connected') : (isTa ? 'AI அமைப்புகள் (விருப்பத்தேர்வு)' : 'AI Settings (Optional)')}
          >
            <Sparkles size={13} className={hasGeminiKey ? 'text-amber-500 animate-pulse' : 'text-slate-400'} />
            <span className="hidden sm:inline">
              {hasGeminiKey ? 'Gemini AI' : (isTa ? 'AI அமைப்புகள்' : 'AI Settings')}
            </span>
          </button>

          {/* Voice Persona Pill */}
          <button
            type="button"
            onClick={() => setVoiceGender(voiceGender === 'female' ? 'male' : 'female')}
            className="text-xs font-bold bg-white/80 hover:bg-white text-slate-700 px-2.5 sm:px-3 py-1.5 rounded-2xl transition-all flex items-center gap-1 border border-slate-200/80 shadow-xs cursor-pointer active:scale-95"
            title={isTa ? 'மனிதக் குரல் மாற்றவும்' : 'Switch Human Voice Persona'}
          >
            <span>{voiceGender === 'female' ? '👩 பல்லவி' : '👨 வள்ளுவர்'}</span>
          </button>

          {/* Voice Narration ON/OFF with live audio equalizer */}
          <button 
            type="button"
            onClick={() => {
              if (audioRef.current) {
                audioRef.current.pause();
              }
              if (autoSpeak && 'speechSynthesis' in window) {
                window.speechSynthesis.cancel();
              }
              setAutoSpeak(!autoSpeak);
            }}
            className={`px-2.5 sm:px-3 py-1.5 rounded-2xl transition-all flex items-center gap-1.5 text-xs font-bold border cursor-pointer active:scale-95 ${
              autoSpeak 
                ? 'bg-emerald-50 text-emerald-800 border-emerald-300 shadow-xs' 
                : 'bg-slate-100 text-slate-500 border-slate-200'
            }`}
            title={autoSpeak ? (isTa ? 'குரல் வாசிப்பு ஆன்' : 'Voice Narration ON') : (isTa ? 'குரல் வாசிப்பு ஆஃப்' : 'Voice Narration OFF')}
          >
            {isPlayingAudio ? (
              <span className="flex items-center gap-0.5">
                <span className="w-1 h-3 bg-emerald-600 animate-pulse" />
                <span className="w-1 h-4 bg-emerald-600 animate-pulse delay-75" />
                <span className="w-1 h-2 bg-emerald-600 animate-pulse delay-150" />
              </span>
            ) : (
              autoSpeak ? <Volume2 size={15} className="text-emerald-700" /> : <VolumeX size={15} />
            )}
            <span className="hidden xl:inline">{autoSpeak ? (isTa ? 'குரல் ஆன்' : 'Voice ON') : (isTa ? 'குரல் ஆஃப்' : 'Voice OFF')}</span>
          </button>

          {/* Language Toggle Pill */}
          <button
            type="button"
            onClick={() => setLanguage(isTa ? 'en' : 'ta')}
            className="text-xs font-bold bg-white/80 hover:bg-white text-slate-700 px-3 py-1.5 rounded-2xl transition-all border border-slate-200/80 shadow-xs cursor-pointer active:scale-95 hidden sm:inline-flex"
            title={isTa ? 'Switch to English' : 'தமிழுக்கு மாறவும்'}
          >
            <span>{isTa ? 'தமிழ் ⇄ Eng' : 'Eng ⇄ தமிழ்'}</span>
          </button>

          {/* Edit Profile Button */}
          <button
            type="button"
            onClick={() => {
              stopAllAudio();
              onEditProfile();
            }}
            className="p-2 hover:bg-slate-100 rounded-2xl transition-all text-slate-600 hover:text-slate-900 cursor-pointer active:scale-95"
            title={isTa ? 'சுயவிவரம் மாற்ற' : 'Edit Citizen Profile'}
          >
            <Edit3 size={18} />
          </button>

          {/* Sidebar Drawer Button */}
          <button 
            type="button"
            onClick={() => setSidebarOpen(true)}
            className="p-2 hover:bg-slate-100 rounded-2xl transition-all text-slate-600 hover:text-slate-900 relative cursor-pointer active:scale-95"
            aria-label="Profile Details"
            title={isTa ? 'முழு விவரங்கள்' : 'Profile Details'}
          >
            <Menu size={19} />
            {Object.keys(userProfile).length > 0 && (
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-emerald-500 rounded-full ring-2 ring-white" />
            )}
          </button>

          {/* Sign Out Button */}
          <button
            type="button"
            onClick={() => {
              stopAllAudio();
              onLogout();
            }}
            className="p-2 hover:bg-rose-50 text-slate-500 hover:text-rose-600 rounded-2xl transition-all cursor-pointer active:scale-95"
            title={isTa ? 'வெளியேறு' : 'Sign Out'}
          >
            <LogOut size={18} />
          </button>
        </div>
      </header>

      {/* Mobile/Tablet Screen Segmented Tab Switcher (< lg) */}
      <div className="lg:hidden bg-white/90 border-b border-slate-200/80 px-4 py-2 flex items-center justify-center gap-2 z-20 shrink-0">
        <button
          type="button"
          onClick={() => setMobileTab('chat')}
          className={`flex-1 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
            mobileTab === 'chat'
              ? 'bg-emerald-700 text-white shadow-xs'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Bot size={14} />
          <span>{isTa ? 'அரசு நண்பன் அரட்டை' : 'AI Assistant'}</span>
        </button>

        <button
          type="button"
          onClick={() => setMobileTab('schemes')}
          className={`flex-1 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
            mobileTab === 'schemes'
              ? 'bg-emerald-700 text-white shadow-xs'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Building2 size={14} />
          <span>{isTa ? `நலத்திட்டங்கள் (${activeSchemes.length})` : `Schemes Hub (${activeSchemes.length})`}</span>
        </button>
      </div>

      {/* Main Dual-Pane Landscape Container */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden relative z-10 w-full max-w-[1900px] mx-auto">
        
        {/* ======================================================== */}
        {/* LEFT PANE: AI Chat Studio & Voice Conversation Stream   */}
        {/* ======================================================== */}
        <section 
          className={`flex flex-col h-full bg-white/40 backdrop-blur-md relative border-r border-slate-200/70 transition-all ${
            isSplitLayout ? 'w-full lg:w-[42%] xl:w-[38%] 2xl:w-[35%]' : 'w-full max-w-4xl mx-auto'
          } ${mobileTab === 'chat' ? 'flex' : 'hidden lg:flex'}`}
        >
          {/* Sub-header inside Chat Studio */}
          <div className="px-4 py-2 bg-white/60 border-b border-slate-100 flex items-center justify-between shrink-0">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-700">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>{isTa ? 'உரையாடல் அரங்கம்' : 'AI Conversation Studio'}</span>
            </div>
            <span className="text-[11px] text-slate-400 font-semibold">
              {isTa ? 'குரல் & தட்டச்சு வழி வழிகாட்டி' : 'Voice & Text Powered'}
            </span>
          </div>

          {/* Messages Stream Area */}
          <div className="flex-1 overflow-y-auto px-3.5 sm:px-5 py-4 space-y-4 pb-32">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in duration-200`}>
                <div className={`max-w-[90%] sm:max-w-[85%] ${
                  msg.sender === 'user' 
                    ? 'bg-gradient-to-r from-emerald-700 to-teal-700 text-white rounded-3xl rounded-tr-sm shadow-md shadow-emerald-950/15 p-3.5 sm:p-4' 
                    : 'bg-white/95 backdrop-blur-xl border border-slate-200/80 text-slate-800 rounded-3xl rounded-tl-sm shadow-md shadow-emerald-950/5 p-3.5 sm:p-4'
                }`}>
                  
                  {/* Assistant Header */}
                  {msg.sender === 'assistant' && (
                    <div className="flex items-center justify-between gap-2 mb-2.5 pb-2 border-b border-slate-100">
                      <div className="flex items-center gap-1.5">
                        <div className="w-5 h-5 rounded-md bg-emerald-100 text-emerald-800 flex items-center justify-center">
                          <Bot size={12} className="text-emerald-700" />
                        </div>
                        <span className="text-[11px] font-bold text-emerald-900 tracking-wide uppercase">
                          {isTa ? 'அரசு நண்பன்' : 'Arasu Nanban'}
                        </span>
                      </div>

                      <button
                        type="button"
                        onClick={() => speakText(msg.text, isTa ? 'ta' : 'en')}
                        className="px-2 py-0.5 rounded-lg bg-slate-50 hover:bg-emerald-50 text-slate-600 hover:text-emerald-800 border border-slate-200/70 hover:border-emerald-200 transition-all flex items-center gap-1 text-[11px] font-semibold cursor-pointer active:scale-95"
                        title={isTa ? 'குரலில் கேட்கவும்' : 'Listen with voice narration'}
                      >
                        <Volume2 size={12} className="text-emerald-600" />
                        <span>{isTa ? 'கேட்க' : 'Listen'}</span>
                      </button>
                    </div>
                  )}

                  {/* Text Content */}
                  <div className="whitespace-pre-wrap leading-relaxed text-xs sm:text-sm font-normal">
                    {msg.text}
                  </div>

                  {/* Schemes Notification Chip if in landscape mode */}
                  {msg.schemes && msg.schemes.length > 0 && isSplitLayout && (
                    <div className="mt-3 p-2 bg-emerald-50/80 border border-emerald-200/80 rounded-xl flex items-center justify-between text-xs text-emerald-900">
                      <div className="flex items-center gap-1.5 font-bold">
                        <Sparkles size={13} className="text-amber-500" />
                        <span>{isTa ? `வலது பலகையில் ${msg.schemes.length} திட்டங்கள் உள்ளன` : `${msg.schemes.length} schemes updated in side panel`}</span>
                      </div>
                      <button
                        type="button"
                        onClick={() => {
                          setMobileTab('schemes');
                        }}
                        className="lg:hidden text-[11px] font-bold underline text-emerald-800"
                      >
                        {isTa ? 'காண்க' : 'View'}
                      </button>
                    </div>
                  )}

                  {/* Inline Scheme Cards (Shown only when single column mode is active) */}
                  {!isSplitLayout && msg.schemes && msg.schemes.length > 0 && (
                    <div className="mt-4 space-y-3">
                      {msg.schemes.map(scheme => {
                        const elig = msg.eligibilityData?.find((e: any) => e.scheme_id === scheme.id);
                        return (
                          <SchemeCard 
                            key={scheme.id} 
                            scheme={scheme} 
                            eligibilityStatus={elig?.status}
                            eligibilityReason={isTa ? elig?.reason_ta : elig?.reason_en}
                            language={language}
                            onAskAbout={(q) => handleSend(q)}
                          />
                        );
                      })}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* Generating response indicator */}
            {isLoading && (
              <div className="flex justify-start animate-in fade-in duration-200">
                <div className="bg-white/95 backdrop-blur-xl border border-slate-200/80 rounded-2xl rounded-tl-sm p-3.5 shadow-xs flex items-center gap-2.5 text-slate-600 text-xs">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-bounce" />
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-bounce [animation-delay:0.15s]" />
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-bounce [animation-delay:0.3s]" />
                  </div>
                  <span className="font-medium">{isTa ? 'அரசு நண்பன் பதிலளிக்கிறார்...' : 'Arasu Nanban is evaluating...'}</span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Floating Action & Input Station inside Chat Panel */}
          <div className="absolute bottom-2 inset-x-2 sm:inset-x-3 z-20">
            
            {/* Error capsule */}
            {micStatus && (
              <div className="mb-2 p-2.5 bg-amber-50/95 backdrop-blur-md border border-amber-200 rounded-2xl flex items-center justify-between text-xs text-amber-900 shadow-md">
                <div className="flex items-center gap-2">
                  <AlertCircle size={15} className="text-amber-600 shrink-0" />
                  <span>{micStatus}</span>
                </div>
                <button
                  type="button"
                  onClick={() => setMicStatus(null)}
                  className="p-1 hover:bg-amber-100 rounded-full text-amber-700 cursor-pointer"
                >
                  <X size={13} />
                </button>
              </div>
            )}

            {/* Live voice recording capsule */}
            {isVoiceRecording && (
              <div className="mb-2 px-3.5 py-2 bg-gradient-to-r from-rose-50 via-red-50 to-amber-50 backdrop-blur-md border border-red-200 rounded-2xl flex items-center justify-between shadow-lg">
                <div className="flex items-center gap-2">
                  <span className="relative flex h-2.5 w-2.5">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-600"></span>
                  </span>
                  <span className="text-xs font-bold text-red-950">
                    {isTa ? '🔴 பேசவும்...' : '🔴 Listening...'}
                  </span>
                </div>
                <span className="text-[10px] text-slate-500 font-semibold">
                  {isTa ? 'முடிந்ததும் மைக்கை அழுத்தவும்' : 'Click mic when done'}
                </span>
              </div>
            )}

            {/* Quick Suggestion Chips */}
            {!input.trim() && !isLoading && (
              <div className="flex items-center gap-1.5 overflow-x-auto pb-1.5 scrollbar-none">
                {quickChips.map((chip, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSend(chip.query)}
                    className="whitespace-nowrap px-2.5 py-1 rounded-full bg-white/95 backdrop-blur-md border border-slate-200 hover:border-emerald-300 text-[11px] font-bold text-slate-700 hover:text-emerald-900 hover:bg-emerald-50 shadow-xs transition-all active:scale-95 cursor-pointer shrink-0"
                  >
                    {chip.label}
                  </button>
                ))}
              </div>
            )}

            {/* Glass Input Capsule */}
            <div className="bg-white/95 backdrop-blur-2xl border border-white/80 shadow-xl shadow-emerald-950/10 rounded-2xl p-1.5 flex items-end gap-1.5 ring-1 ring-slate-900/5">
              
              <div className="flex-1 flex items-center pl-2.5">
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      if (!isLoading && input.trim()) {
                        handleSend();
                      }
                    }
                  }}
                  placeholder={
                    isVoiceRecording
                      ? (isTa ? 'மைக்ரோஃபோன் கேட்கிறது... பேசுங்கள்...' : 'Microphone is listening... Speak now...')
                      : (isTa ? 'கேள்வி கேட்கவும் அல்லது மைக்கை அழுத்தவும்...' : 'Ask question or use microphone...')
                  }
                  className="w-full max-h-24 min-h-[38px] bg-transparent border-none focus:ring-0 resize-none py-2 outline-none text-xs sm:text-sm text-slate-800 placeholder-slate-400"
                  rows={1}
                />
              </div>

              {/* Action buttons */}
              <div className="flex shrink-0 gap-1 items-center pr-1 pb-0.5">
                <AudioRecorder
                  onTranscription={handleVoiceTranscription}
                  onError={(err) => setMicStatus(err)}
                  language={voiceLang}
                  onRecordingStateChange={setIsVoiceRecording}
                  onStart={handleVoiceStart}
                />

                <button
                  type="button"
                  onClick={() => handleSend()}
                  disabled={isLoading || !input.trim()}
                  className={`w-9 h-9 rounded-xl flex items-center justify-center transition-all ${
                    input.trim() && !isLoading
                      ? 'bg-gradient-to-r from-emerald-700 to-teal-700 text-white shadow-md active:scale-95 cursor-pointer hover:shadow-lg'
                      : 'bg-slate-100 text-slate-400 cursor-not-allowed'
                  }`}
                  title={isTa ? 'அனுப்பவும்' : 'Send'}
                >
                  <Send size={15} />
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* ======================================================== */}
        {/* RIGHT PANE: Live Welfare Schemes Landscape Dashboard     */}
        {/* ======================================================== */}
        {isSplitLayout && (
          <section className={`flex-1 flex flex-col h-full bg-[#f8fafc] overflow-hidden ${mobileTab === 'schemes' ? 'flex' : 'hidden lg:flex'}`}>
            
            {/* Hub Header & Landscape Toolbar */}
            <div className="p-3.5 sm:p-4 bg-white/80 backdrop-blur-md border-b border-slate-200/80 shrink-0 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2.5">
                <div className="flex items-center gap-2">
                  <div className="w-7 h-7 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center">
                    <Building2 size={16} className="text-emerald-700" />
                  </div>
                  <div>
                    <h2 className="text-sm sm:text-base font-extrabold text-slate-900 leading-tight">
                      {isTa ? 'அரசு நலத்திட்டங்கள் பலகை' : 'Live Government Schemes Hub'}
                    </h2>
                    <p className="text-[11px] text-slate-500 font-medium">
                      {isTa ? 'உங்கள் சுயவிவரத்திற்கு ஏற்ப சரிபார்க்கப்பட்ட அரசு உதவிகள்' : 'Verified Welfare Schemes Evaluated for Your Profile'}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="px-3 py-1 rounded-full text-xs font-extrabold bg-emerald-100/80 text-emerald-900 border border-emerald-200">
                    {filteredSchemes.length} {isTa ? 'திட்டங்கள்' : 'Schemes'}
                  </span>

                  {/* Search within schemes */}
                  <div className="relative w-44 sm:w-56">
                    <Search size={13} className="absolute left-2.5 top-2.5 text-slate-400" />
                    <input
                      type="text"
                      value={searchFilter}
                      onChange={(e) => setSearchFilter(e.target.value)}
                      placeholder={isTa ? 'திட்டங்களை வடிகட்டுக...' : 'Filter schemes...'}
                      className="w-full pl-8 pr-2.5 py-1 text-xs rounded-xl bg-slate-50 border border-slate-200 focus:bg-white focus:border-emerald-500 outline-none transition-all"
                    />
                    {searchFilter && (
                      <button
                        type="button"
                        onClick={() => setSearchFilter('')}
                        className="absolute right-2 top-2 text-slate-400 hover:text-slate-600"
                      >
                        <X size={12} />
                      </button>
                    )}
                  </div>
                </div>
              </div>

              {/* Landscape Category Filter Pills */}
              <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">
                {[
                  { key: 'all' as CategoryFilter, label: isTa ? 'அனைத்தும்' : 'All', icon: <Layers size={12} /> },
                  { key: 'eligible' as CategoryFilter, label: isTa ? 'தகுதியானது' : 'Eligible', icon: <CheckCircle2 size={12} /> },
                  { key: 'education' as CategoryFilter, label: isTa ? 'கல்வி & மாணவர்' : 'Education', icon: <GraduationCap size={12} /> },
                  { key: 'women' as CategoryFilter, label: isTa ? 'மகளிர் நலம்' : 'Women', icon: <Heart size={12} /> },
                  { key: 'business' as CategoryFilter, label: isTa ? 'தொழில் & கடன்' : 'Loans & Business', icon: <Briefcase size={12} /> },
                  { key: 'agriculture' as CategoryFilter, label: isTa ? 'வேளாண்மை' : 'Agriculture', icon: <Sprout size={12} /> },
                  { key: 'health' as CategoryFilter, label: isTa ? 'மருத்துவம்' : 'Healthcare', icon: <Building2 size={12} /> },
                ].map(pill => (
                  <button
                    key={pill.key}
                    type="button"
                    onClick={() => setCategoryFilter(pill.key)}
                    className={`px-3 py-1 rounded-xl font-bold flex items-center gap-1.5 transition-all shrink-0 cursor-pointer active:scale-95 ${
                      categoryFilter === pill.key
                        ? 'bg-emerald-700 text-white shadow-xs'
                        : 'bg-white/80 hover:bg-white text-slate-700 border border-slate-200/70 hover:border-emerald-300'
                    }`}
                  >
                    {pill.icon}
                    <span>{pill.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Scheme Cards Canvas */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-5">
              
              {/* Fetch Error State */}
              {fetchError && (
                <div className="mb-4 p-4 bg-rose-50 border border-rose-200 rounded-2xl flex items-center justify-between text-xs text-rose-900 shadow-xs">
                  <span>{isTa ? 'திட்டங்களை ஏற்றுவதில் சிக்கல் ஏற்பட்டது.' : 'Failed to retrieve government schemes.'}</span>
                  <button
                    type="button"
                    onClick={fetchInitialSchemes}
                    className="px-3.5 py-1.5 bg-emerald-700 text-white rounded-xl font-bold hover:bg-emerald-800 transition-all cursor-pointer"
                  >
                    {isTa ? 'மீண்டும் முயற்சி' : 'Retry'}
                  </button>
                </div>
              )}

              {/* Initial Loading State */}
              {isLoading && activeSchemes.length === 0 && (
                <div className="h-64 flex flex-col items-center justify-center text-center p-6 bg-white/70 rounded-3xl border border-slate-200">
                  <Loader2 size={32} className="animate-spin text-emerald-700 mb-3" />
                  <h3 className="font-bold text-slate-800 text-sm">
                    {isTa ? 'அரசு நலத்திட்டங்கள் மதிப்பீடு செய்யப்படுகின்றன...' : 'Evaluating Government Welfare Schemes...'}
                  </h3>
                  <p className="text-xs text-slate-500 mt-1 max-w-sm">
                    {isTa ? 'உங்கள் கல்வி, வயது மற்றும் தகுதிகளை ஆய்வு செய்கிறோம்' : 'Checking eligibility criteria against official government database'}
                  </p>
                </div>
              )}

              {/* Empty schemes state */}
              {!isLoading && filteredSchemes.length === 0 && (
                <div className="h-64 flex flex-col items-center justify-center text-center p-6 bg-white/70 rounded-3xl border border-slate-200">
                  <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center mb-3">
                    <Filter size={20} />
                  </div>
                  <h3 className="font-bold text-slate-800 text-sm">
                    {isTa ? 'பொருத்தமான திட்டங்கள் எதுவும் இல்லை' : 'No Matching Schemes Found'}
                  </h3>
                  <p className="text-xs text-slate-500 mt-1 max-w-sm">
                    {isTa ? 'வேறு வகைப்பிரிவைத் தேர்வு செய்யவும் அல்லது அரட்டையில் உங்கள் தேவையை கேட்கவும்.' : 'Try selecting another category or ask the assistant for specific schemes.'}
                  </p>
                  <button
                    type="button"
                    onClick={() => {
                      setCategoryFilter('all');
                      setSearchFilter('');
                    }}
                    className="mt-3 px-3 py-1.5 bg-emerald-700 text-white rounded-xl text-xs font-bold hover:bg-emerald-800 transition-all cursor-pointer"
                  >
                    {isTa ? 'அனைத்து திட்டங்களையும் காட்டுக' : 'View All Schemes'}
                  </button>
                </div>
              )}

              {/* Schemes Grid in Landscape (1 or 2 Columns) */}
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                {filteredSchemes.map(scheme => {
                  const elig = activeEligibilityData.find((e: any) => e.scheme_id === scheme.id);
                  return (
                    <SchemeCard 
                      key={scheme.id} 
                      scheme={scheme} 
                      eligibilityStatus={elig?.status}
                      eligibilityReason={isTa ? elig?.reason_ta : elig?.reason_en}
                      language={language}
                      onAskAbout={(q) => handleSend(q)}
                    />
                  );
                })}
              </div>
            </div>
          </section>
        )}
      </div>

      {/* Profile Sidebar Drawer */}
      <ProfileSidebar 
        profile={userProfile}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onClearSession={handleClearSession}
        language={language}
      />

      {/* Gemini AI API Key Modal */}
      {showGeminiModal && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-200">
          <div className="bg-white rounded-3xl p-6 max-w-md w-full shadow-2xl border border-white/80 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
                  <Sparkles size={16} />
                </div>
                <h3 className="font-extrabold text-base text-slate-900">
                  {isTa ? 'Google Gemini AI அமைப்புகள்' : 'Google Gemini AI Settings'}
                </h3>
              </div>
              <button 
                type="button"
                onClick={() => {
                  setShowGeminiModal(false);
                  setGeminiStatusMsg(null);
                }}
                className="p-1.5 hover:bg-slate-100 rounded-full text-slate-500 hover:text-slate-800 cursor-pointer"
              >
                <X size={18} />
              </button>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              {isTa 
                ? 'உங்கள் தனிப்பட்ட Gemini API சாவியை இணைத்தால், கூடுதல் நுண்ணறிவு மற்றும் நிகழ்நேர உரையாடல் பதில்களைப் பெறலாம். (சாவி இல்லாவிட்டாலும் உள்ளூர் அறிவார்ந்த வழிகாட்டி துல்லியமாக செயல்படும்).'
                : 'Connect your personal Google Gemini API key to activate deep conversational reasoning. (The system also functions fully with our built-in local knowledge engine).'}
            </p>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1.5">
                {isTa ? 'Gemini API சாவி (API Key)' : 'Gemini API Key'}
              </label>
              <input 
                type="password"
                value={geminiKeyInput}
                onChange={(e) => setGeminiKeyInput(e.target.value)}
                placeholder="AIzaSy..."
                className="w-full px-3.5 py-2.5 rounded-2xl border border-slate-200 bg-slate-50/50 text-slate-800 text-xs sm:text-sm focus:border-emerald-500 focus:bg-white outline-none font-mono"
              />
            </div>

            {geminiStatusMsg && (
              <div className={`p-3 rounded-2xl text-xs font-semibold flex items-center gap-2 ${
                geminiStatusMsg.type === 'success' 
                  ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' 
                  : 'bg-rose-50 text-rose-800 border border-rose-200'
              }`}>
                {geminiStatusMsg.type === 'success' ? <CheckCircle2 size={15} /> : <AlertCircle size={15} />}
                <span>{geminiStatusMsg.text}</span>
              </div>
            )}

            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => {
                  setShowGeminiModal(false);
                  setGeminiStatusMsg(null);
                }}
                className="px-4 py-2 rounded-xl text-xs font-bold text-slate-600 hover:bg-slate-100 transition-all cursor-pointer"
              >
                {isTa ? 'மூடு' : 'Cancel'}
              </button>
              <button
                type="button"
                onClick={handleSaveGeminiKey}
                disabled={isValidatingGemini}
                className="px-5 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-emerald-700 to-teal-700 hover:from-emerald-800 hover:to-teal-800 shadow-md shadow-emerald-950/15 flex items-center gap-2 cursor-pointer disabled:opacity-50"
              >
                {isValidatingGemini && <Loader2 size={14} className="animate-spin" />}
                <span>{isTa ? 'சேமித்து சரிபார்' : 'Save & Validate'}</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};