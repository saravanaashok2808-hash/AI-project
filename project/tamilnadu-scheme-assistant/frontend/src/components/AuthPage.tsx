import React, { useState, useEffect } from 'react';
import type { UserProfile } from '../types';
import { TN_DISTRICTS } from '../types';
import { ApiClient } from '../api/client';
import { User, LogIn, UserPlus, ArrowRight, ArrowLeft, Lock, Eye, EyeOff, AlertCircle, Loader2, Sparkles, MapPin, Calendar } from 'lucide-react';

interface AuthPageProps {
  language: 'ta' | 'en';
  onLanguageChange?: (lang: 'ta' | 'en') => void;
  onLogin: (profile: UserProfile) => void;
  onSignUp: (initialProfile: UserProfile) => void;
  onBack?: () => void;
}

export const AuthPage: React.FC<AuthPageProps> = ({ language, onLanguageChange, onLogin, onSignUp, onBack }) => {
  const isTa = language === 'ta';
  const [mode, setMode] = useState<'signin' | 'signup'>('signin');
  const [showPassword, setShowPassword] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Stop any playing audio
  useEffect(() => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }, []);

  // Clear errors when switching modes
  useEffect(() => {
    setAuthError(null);
  }, [mode]);

  // Sign in state
  const [loginIdentifier, setLoginIdentifier] = useState('');
  const [loginPassword, setLoginPassword] = useState('');

  // Sign up state
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [signupPassword, setSignupPassword] = useState('');
  const [district, setDistrict] = useState('Chennai');
  const [age, setAge] = useState<number>(24);
  const [gender, setGender] = useState('Female');

  // Existing saved accounts
  const savedCitizens: UserProfile[] = (() => {
    try {
      const data = localStorage.getItem('tn_saved_citizens');
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  })();

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!loginIdentifier.trim() || !loginPassword.trim()) {
      setAuthError(isTa ? 'பெயர் மற்றும் கடவுச்சொல்லை உள்ளிடவும்' : 'Please enter your identifier and password');
      return;
    }

    setAuthError(null);
    setIsSubmitting(true);

    try {
      const authData = await ApiClient.login(loginIdentifier, loginPassword);
      const userProfile: UserProfile = {
        name: authData.user.name,
        phone: authData.user.phone,
        ...(authData.user.profile || {})
      };
      onLogin(userProfile);
    } catch (err: any) {
      setAuthError(err.message || (isTa ? 'உள்நுழைவு தோல்வியடைந்தது' : 'Authentication failed'));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setAuthError(isTa ? 'உங்கள் பெயரை உள்ளிடவும்' : 'Please enter your name');
      return;
    }
    if (!signupPassword || signupPassword.length < 4) {
      setAuthError(isTa ? 'கடவுச்சொல் குறைந்தது 4 எழுத்துக்களாக இருக்க வேண்டும்' : 'Password must be at least 4 characters');
      return;
    }

    setAuthError(null);
    setIsSubmitting(true);

    try {
      const initialProfile: UserProfile = {
        name,
        phone: phone.trim() || undefined,
        district,
        age,
        gender,
      };

      const authData = await ApiClient.register({
        name,
        password: signupPassword,
        phone: phone.trim() || undefined,
        district,
        age,
        gender,
        profile_data: initialProfile
      });

      const userProfile: UserProfile = {
        name: authData.user.name,
        phone: authData.user.phone,
        ...(authData.user.profile || initialProfile)
      };

      onSignUp(userProfile);
    } catch (err: any) {
      setAuthError(err.message || (isTa ? 'பதிவு தோல்வியடைந்தது' : 'Registration failed'));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-950 via-slate-900 to-teal-950 p-4 sm:p-6 flex items-center justify-center relative overflow-hidden">
      
      {/* Ambient background glow orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-md w-full bg-white/90 backdrop-blur-2xl rounded-3xl shadow-2xl shadow-black/40 overflow-hidden border border-white/40 my-8 relative z-10 animate-in fade-in zoom-in-95 duration-200">
        
        {/* Top Header */}
        <div className="bg-gradient-to-r from-emerald-800 via-emerald-700 to-teal-800 text-white p-6 sm:p-8 text-center relative overflow-hidden">
          <div className="absolute -top-10 -right-10 w-32 h-32 bg-white/10 rounded-full blur-xl pointer-events-none" />
          
          <div className="flex items-center justify-between mb-4">
            {onBack ? (
              <button
                type="button"
                onClick={onBack}
                className="p-2 bg-white/10 hover:bg-white/20 active:scale-95 rounded-full transition-all text-white flex items-center justify-center cursor-pointer border border-white/20 shadow-sm"
                title={isTa ? 'பின்னே செல்ல' : 'Go back'}
                aria-label="Back"
              >
                <ArrowLeft size={18} />
              </button>
            ) : <div />}

            {onLanguageChange && (
              <button
                type="button"
                onClick={() => onLanguageChange(isTa ? 'en' : 'ta')}
                className="text-xs bg-white/15 hover:bg-white/25 active:scale-95 text-white border border-white/30 px-3 py-1 rounded-full font-semibold transition-all cursor-pointer shadow-sm flex items-center gap-1.5"
                title={isTa ? 'Switch to English' : 'தமிழுக்கு மாறுக'}
              >
                <span>{isTa ? '🌐 English' : '🇮🇳 தமிழ்'}</span>
              </button>
            )}
          </div>

          <div className="w-20 h-20 rounded-full overflow-hidden mx-auto mb-3 flex items-center justify-center shadow-xl shadow-black/30 ring-4 ring-white/20 bg-white">
            <img src="/tn-logo.png" alt="Tamil Nadu Government SchemeVoice" className="w-full h-full object-cover" />
          </div>

          <div className="inline-flex items-center gap-1.5 bg-emerald-900/60 backdrop-blur-sm border border-emerald-400/30 text-[#FFD700] px-3 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider mb-2">
            <Sparkles size={11} />
            <span>SchemeVoice AI</span>
          </div>

          <h1 className="text-xl sm:text-2xl font-bold tracking-tight">
            {isTa ? 'தமிழ்நாடு அரசுத் திட்ட வழிகாட்டி' : 'TN Scheme Assistant'}
          </h1>
          <p className="text-emerald-100/90 text-xs mt-1 font-medium">
            {isTa ? 'அரசு நண்பன் - பாதுகாப்பான குடிமக்கள் போர்டல்' : 'Secure Citizen Welfare Portal'}
          </p>

          {/* Segmented Mode Switcher */}
          <div className="flex bg-black/25 backdrop-blur-md p-1 rounded-2xl mt-6 border border-white/10 shadow-inner">
            <button
              type="button"
              onClick={() => setMode('signin')}
              className={`flex-1 py-2 text-xs font-bold rounded-xl transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
                mode === 'signin' ? 'bg-white text-emerald-900 shadow-md' : 'text-white/80 hover:text-white'
              }`}
            >
              <LogIn size={14} />
              <span>{isTa ? 'உள்நுழைக' : 'Sign In'}</span>
            </button>
            <button
              type="button"
              onClick={() => setMode('signup')}
              className={`flex-1 py-2 text-xs font-bold rounded-xl transition-all flex items-center justify-center gap-1.5 cursor-pointer ${
                mode === 'signup' ? 'bg-white text-emerald-900 shadow-md' : 'text-white/80 hover:text-white'
              }`}
            >
              <UserPlus size={14} />
              <span>{isTa ? 'புதிய பதிவு' : 'Sign Up'}</span>
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 sm:p-8">
          {authError && (
            <div className="mb-4 p-3 bg-rose-50 border border-rose-200 rounded-2xl text-xs text-rose-700 flex items-center gap-2 animate-in fade-in duration-150">
              <AlertCircle size={16} className="shrink-0 text-rose-600" />
              <span>{authError}</span>
            </div>
          )}

          {mode === 'signin' ? (
            <form onSubmit={handleSignIn} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  {isTa ? 'பெயர் அல்லது மொபைல் எண்' : 'Name or Mobile Number'} *
                </label>
                <div className="relative">
                  <User size={18} className="absolute left-3.5 top-3 text-slate-400" />
                  <input
                    type="text"
                    required
                    value={loginIdentifier}
                    onChange={(e) => setLoginIdentifier(e.target.value)}
                    placeholder={isTa ? 'எ.கா: கார்த்திக் அல்லது 9876543210' : 'e.g. Priya or 9876543210'}
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-50/80 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 focus:bg-white outline-none transition-all"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  {isTa ? 'கடவுச்சொல் (Password / PIN)' : 'Password / PIN'} *
                </label>
                <div className="relative">
                  <Lock size={18} className="absolute left-3.5 top-3 text-slate-400" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-10 pr-10 py-2.5 bg-slate-50/80 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 focus:bg-white outline-none transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-3 text-slate-400 hover:text-slate-600 cursor-pointer"
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>

              {/* Quick citizen shortcuts */}
              {savedCitizens.length > 0 && (
                <div className="pt-1">
                  <p className="text-[11px] font-bold text-slate-500 mb-2">
                    {isTa ? 'முன்பு உள்நுழைந்த பயனர்கள்:' : 'Saved Citizens on this device:'}
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {savedCitizens.map((c, i) => (
                      <button
                        key={i}
                        type="button"
                        onClick={() => {
                          setLoginIdentifier(c.phone || c.name || '');
                        }}
                        className="px-3 py-1.5 bg-emerald-50 text-emerald-800 border border-emerald-200/80 rounded-xl text-xs font-semibold hover:bg-emerald-100 flex items-center gap-1.5 cursor-pointer transition-all active:scale-95 shadow-xs"
                      >
                        <User size={12} className="text-emerald-600" />
                        <span>{c.name}</span>
                        {c.age && <span className="text-[10px] text-slate-500">({c.age}y)</span>}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full mt-4 py-3 bg-gradient-to-r from-emerald-700 to-teal-700 hover:from-emerald-800 hover:to-teal-800 text-white font-bold rounded-xl text-sm transition-all shadow-md shadow-emerald-950/20 flex items-center justify-center gap-2 cursor-pointer active:scale-98 disabled:opacity-60"
              >
                {isSubmitting ? (
                  <Loader2 size={16} className="animate-spin" />
                ) : (
                  <>
                    <span>{isTa ? 'பாதுகாப்பாக உள்நுழைக' : 'Secure Sign In'}</span>
                    <ArrowRight size={16} />
                  </>
                )}
              </button>
            </form>
          ) : (
            <form onSubmit={handleSignUp} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  {isTa ? 'உங்கள் பெயர்' : 'Full Name'} *
                </label>
                <div className="relative">
                  <User size={18} className="absolute left-3.5 top-3 text-slate-400" />
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder={isTa ? 'எ.கா: கார்த்திகேயன் / பிரியா' : 'e.g. Karthikeyan / Priya'}
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-50/80 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 focus:bg-white outline-none transition-all"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  {isTa ? 'கடவுச்சொல் / பின் (Password / PIN)' : 'Password / PIN'} *
                </label>
                <div className="relative">
                  <Lock size={18} className="absolute left-3.5 top-3 text-slate-400" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={signupPassword}
                    onChange={(e) => setSignupPassword(e.target.value)}
                    placeholder="குறைந்தது 4 எழுத்துக்கள் (Min 4 characters)"
                    className="w-full pl-10 pr-10 py-2.5 bg-slate-50/80 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 focus:bg-white outline-none transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-3 text-slate-400 hover:text-slate-600 cursor-pointer"
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1.5">
                    {isTa ? 'வயது' : 'Age'} *
                  </label>
                  <div className="relative">
                    <Calendar size={16} className="absolute left-3 top-3 text-slate-400" />
                    <input
                      type="number"
                      min={1}
                      max={120}
                      required
                      value={age}
                      onChange={(e) => setAge(parseInt(e.target.value) || 24)}
                      className="w-full pl-9 pr-3 py-2.5 bg-slate-50/80 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 focus:bg-white outline-none"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1.5">
                    {isTa ? 'பாலினம்' : 'Gender'}
                  </label>
                  <select
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    className="w-full px-3 py-2.5 bg-slate-50/80 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 focus:bg-white outline-none"
                  >
                    <option value="Female">{isTa ? 'பெண் (Female)' : 'Female'}</option>
                    <option value="Male">{isTa ? 'ஆண் (Male)' : 'Male'}</option>
                    <option value="Others">{isTa ? 'மற்றவை (Others)' : 'Others'}</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  {isTa ? 'மாவட்டம் (District)' : 'District'}
                </label>
                <div className="relative">
                  <MapPin size={18} className="absolute left-3.5 top-3 text-slate-400" />
                  <select
                    value={district}
                    onChange={(e) => setDistrict(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-50/80 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 focus:bg-white outline-none"
                  >
                    {TN_DISTRICTS.map((dist) => (
                      <option key={dist} value={dist}>{dist}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">
                  {isTa ? 'தொலைபேசி எண் (விருப்பத்தேர்வு)' : 'Phone (Optional)'}
                </label>
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="9876543210"
                  className="w-full px-3.5 py-2.5 bg-slate-50/80 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 focus:bg-white outline-none"
                />
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full mt-4 py-3 bg-gradient-to-r from-emerald-700 to-teal-700 hover:from-emerald-800 hover:to-teal-800 text-white font-bold rounded-xl text-sm transition-all shadow-md shadow-emerald-950/20 flex items-center justify-center gap-2 cursor-pointer active:scale-98 disabled:opacity-60"
              >
                {isSubmitting ? (
                  <Loader2 size={16} className="animate-spin" />
                ) : (
                  <>
                    <span>{isTa ? 'பதிவு செய்து தொடரவும்' : 'Register & Continue'}</span>
                    <ArrowRight size={16} />
                  </>
                )}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
