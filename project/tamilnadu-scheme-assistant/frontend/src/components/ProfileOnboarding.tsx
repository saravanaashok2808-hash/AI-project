import React, { useState, useEffect } from 'react';
import type { UserProfile } from '../types';
import { TN_DISTRICTS } from '../types';
import { Sparkles, ArrowRight, ArrowLeft } from 'lucide-react';

interface ProfileOnboardingProps {
  initialProfile?: UserProfile;
  language: 'ta' | 'en';
  onComplete: (profile: UserProfile) => void;
  onBack?: () => void;
}

export const ProfileOnboarding: React.FC<ProfileOnboardingProps> = ({
  initialProfile = {},
  language,
  onComplete,
  onBack
}) => {
  const isTa = language === 'ta';

  useEffect(() => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }, []);

  const [formData, setFormData] = useState<UserProfile>({
    name: initialProfile.name || '',
    phone: initialProfile.phone || '',
    age: initialProfile.age || 24,
    gender: initialProfile.gender || 'Female',
    district: initialProfile.district || 'Chennai',
    education_level: initialProfile.education_level || 'Graduate',
    employment_status: initialProfile.employment_status || 'Unemployed',
    occupation: initialProfile.occupation || 'Farmer',
    income: initialProfile.income || 60000,
    caste_category: initialProfile.caste_category || 'BC',
    marital_status: initialProfile.marital_status || 'Single',
    disability: initialProfile.disability || false,
    voice_gender: initialProfile.voice_gender || 'female'
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onComplete(formData);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-950 via-slate-900 to-teal-950 p-4 sm:p-6 flex items-center justify-center relative overflow-hidden">
      
      {/* Ambient decorative glowing orbs */}
      <div className="absolute top-1/6 left-1/6 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/6 right-1/6 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-2xl w-full bg-white/95 backdrop-blur-2xl rounded-3xl shadow-2xl shadow-black/30 overflow-hidden border border-white/60 my-8 relative z-10 animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header Banner */}
        <div className="bg-gradient-to-r from-emerald-800 via-emerald-700 to-teal-800 text-white p-6 sm:p-8 relative overflow-hidden">
          <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/10 rounded-full blur-2xl pointer-events-none" />

          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              {onBack && (
                <button
                  type="button"
                  onClick={onBack}
                  className="p-1.5 -ml-1 bg-white/10 hover:bg-white/20 active:scale-95 rounded-full transition-all text-white flex items-center justify-center cursor-pointer border border-white/20 shadow-sm"
                  title={isTa ? 'பின்னே செல்ல' : 'Go back'}
                  aria-label="Back"
                >
                  <ArrowLeft size={18} />
                </button>
              )}
              <div className="flex items-center gap-1.5 bg-emerald-900/60 backdrop-blur-sm border border-emerald-400/30 text-[#FFD700] px-3 py-1 rounded-full text-xs font-bold tracking-wide uppercase">
                <Sparkles size={13} />
                <span>{isTa ? 'தனிப்பயனாக்கப்பட்ட அரசு உதவி' : 'Personalized Scheme Discovery'}</span>
              </div>
            </div>
          </div>

          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">
            {isTa ? 'உங்கள் குடிமக்கள் விவரக்குறிப்பு' : 'Complete Your Citizen Profile'}
          </h1>
          <p className="text-emerald-100 text-xs sm:text-sm mt-1.5 leading-relaxed">
            {isTa 
              ? 'உங்கள் வயது, கல்வி மற்றும் வேலை விவரங்களைக் குறிப்பிட்டால், உங்களுக்குப் பொருந்தும் 59+ அரசு நலத்திட்டங்களை துல்லியமாக கண்டறிய முடியும்.' 
              : 'Tell us a few details about yourself so our AI can accurately evaluate and recommend verified Tamil Nadu Government schemes.'}
          </p>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 sm:p-8 space-y-6">

          {/* Section 1: Basic Information */}
          <div className="p-4 sm:p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80 shadow-xs">
            <h2 className="text-xs font-bold text-emerald-900 uppercase tracking-wider mb-3.5 flex items-center gap-2">
              <span className="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center text-xs">1</span>
              <span>{isTa ? 'அடிப்படை விவரங்கள்' : 'Basic Information'}</span>
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'உங்கள் பெயர்' : 'Full Name'} *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name || ''}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder={isTa ? 'எ.கா: கார்த்திக் / பிரியா' : 'e.g., Karthik / Priya'}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none transition-all"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'வயது (Age)' : 'Age (Years)'} *
                </label>
                <input
                  type="number"
                  min={1}
                  max={120}
                  required
                  value={formData.age || ''}
                  onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) || 0 })}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none transition-all"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'பாலினம்' : 'Gender'}
                </label>
                <select
                  value={formData.gender || 'Female'}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none transition-all"
                >
                  <option value="Female">{isTa ? 'பெண் (Female)' : 'Female'}</option>
                  <option value="Male">{isTa ? 'ஆண் (Male)' : 'Male'}</option>
                  <option value="Others">{isTa ? 'மற்றவை (Others)' : 'Others'}</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'மாவட்டம்' : 'District'}
                </label>
                <select
                  value={formData.district || 'Chennai'}
                  onChange={(e) => setFormData({ ...formData, district: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none transition-all"
                >
                  {TN_DISTRICTS.map((dist) => (
                    <option key={dist} value={dist}>{dist}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Section 2: Education & Employment */}
          <div className="p-4 sm:p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80 shadow-xs">
            <h2 className="text-xs font-bold text-emerald-900 uppercase tracking-wider mb-3.5 flex items-center gap-2">
              <span className="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center text-xs">2</span>
              <span>{isTa ? 'கல்வி மற்றும் தொழில் நிலை' : 'Education & Employment'}</span>
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'கல்வித் தகுதி' : 'Education Level'}
                </label>
                <select
                  value={formData.education_level || 'Graduate'}
                  onChange={(e) => setFormData({ ...formData, education_level: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none"
                >
                  <option value="None">{isTa ? 'பள்ளிக்கல்வி இல்லை (No Formal)' : 'No Formal Schooling'}</option>
                  <option value="School">{isTa ? 'பள்ளிக்கல்வி (10th / 12th)' : 'School (10th/12th)'}</option>
                  <option value="ITI_Diploma">{isTa ? 'டிப்ளமோ / ITI (Diploma / ITI)' : 'Diploma / ITI'}</option>
                  <option value="College">{isTa ? 'கல்லூரி மாணவர் (College Student)' : 'College Student'}</option>
                  <option value="Graduate">{isTa ? 'பட்டதாரி (Graduate / Post-Graduate)' : 'Graduate / Post-Graduate'}</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'வேலைவாய்ப்பு நிலை' : 'Employment Status'}
                </label>
                <select
                  value={formData.employment_status || 'Unemployed'}
                  onChange={(e) => setFormData({ ...formData, employment_status: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none"
                >
                  <option value="Student">{isTa ? 'மாணவர் (Student)' : 'Student'}</option>
                  <option value="Unemployed">{isTa ? 'வேலை தேடுபவர் (Unemployed)' : 'Job Seeker / Unemployed'}</option>
                  <option value="Employed">{isTa ? 'வேலை செய்பவர் (Employed)' : 'Employed'}</option>
                  <option value="Self-Employed">{isTa ? 'சுயதொழில் / வணிகம் (Self-Employed)' : 'Self-Employed'}</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'முதன்மைத் தொழில்' : 'Primary Occupation'}
                </label>
                <select
                  value={formData.occupation || 'Farmer'}
                  onChange={(e) => setFormData({ ...formData, occupation: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none"
                >
                  <option value="Student">{isTa ? 'மாணவர் (Student)' : 'Student'}</option>
                  <option value="Farmer">{isTa ? 'விவசாயி (Farmer / Agri Worker)' : 'Farmer / Agri Worker'}</option>
                  <option value="Weaver">{isTa ? 'நெசவாளர் (Weaver / Handloom)' : 'Weaver / Handloom'}</option>
                  <option value="Construction">{isTa ? 'கட்டுமானத் தொழிலாளி (Construction Worker)' : 'Construction Worker'}</option>
                  <option value="Driver">{isTa ? 'ஓட்டுநர் (Driver)' : 'Driver'}</option>
                  <option value="Small Business">{isTa ? 'சிறு வணிகர் (Small Business Owner)' : 'Small Business Owner'}</option>
                  <option value="Others">{isTa ? 'பிற தொழில்கள் (Other)' : 'Other'}</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'குடும்ப ஆண்டு வருமானம் (₹)' : 'Family Annual Income (₹)'}
                </label>
                <input
                  type="number"
                  min={0}
                  step={10000}
                  value={formData.income || 60000}
                  onChange={(e) => setFormData({ ...formData, income: parseInt(e.target.value) || 0 })}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none"
                />
              </div>
            </div>
          </div>

          {/* Section 3: Social Category & Preferences */}
          <div className="p-4 sm:p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80 shadow-xs">
            <h2 className="text-xs font-bold text-emerald-900 uppercase tracking-wider mb-3.5 flex items-center gap-2">
              <span className="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center text-xs">3</span>
              <span>{isTa ? 'சமூக விவரங்கள் & விருப்பங்கள்' : 'Category & Voice Settings'}</span>
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'இடஒதுக்கீடு பிரிவு' : 'Social Category'}
                </label>
                <select
                  value={formData.caste_category || 'BC'}
                  onChange={(e) => setFormData({ ...formData, caste_category: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none"
                >
                  <option value="SC">{isTa ? 'பட்டியலினத்தவர் (SC)' : 'Scheduled Caste (SC)'}</option>
                  <option value="ST">{isTa ? 'பழங்குடியினர் (ST)' : 'Scheduled Tribe (ST)'}</option>
                  <option value="MBC">{isTa ? 'மிகவும் பிற்படுத்தப்பட்டோர் (MBC / DNC)' : 'Most Backward Class (MBC/DNC)'}</option>
                  <option value="BC">{isTa ? 'பிற்படுத்தப்பட்டோர் (BC)' : 'Backward Class (BC)'}</option>
                  <option value="General">{isTa ? 'பொதுப் பிரிவு (General / OC)' : 'General / OC'}</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'திருமண நிலை' : 'Marital Status'}
                </label>
                <select
                  value={formData.marital_status || 'Single'}
                  onChange={(e) => setFormData({ ...formData, marital_status: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none"
                >
                  <option value="Single">{isTa ? 'திருமணம் ஆகாதவர் (Single / Unmarried)' : 'Single / Unmarried'}</option>
                  <option value="Married">{isTa ? 'திருமணமானவர் (Married)' : 'Married'}</option>
                  <option value="Widowed">{isTa ? 'விதவை (Widowed)' : 'Widowed'}</option>
                  <option value="Destitute">{isTa ? 'ஆதரவற்ற பெண் (Destitute)' : 'Destitute'}</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  {isTa ? 'AI குரல் தேர்வு (Voice Persona)' : 'AI Voice Persona'}
                </label>
                <select
                  value={formData.voice_gender || 'female'}
                  onChange={(e) => setFormData({ ...formData, voice_gender: e.target.value as 'female' | 'male' })}
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-emerald-600 outline-none"
                >
                  <option value="female">{isTa ? '👩 பல்லவி (பெண் குரல் / Female)' : '👩 Pallavi (Female)'}</option>
                  <option value="male">{isTa ? '👨 வள்ளுவர் (ஆண் குரல் / Male)' : '👨 Valluvar (Male)'}</option>
                </select>
              </div>

              <div className="flex items-center pt-6">
                <label className="flex items-center gap-3 cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={formData.disability || false}
                    onChange={(e) => setFormData({ ...formData, disability: e.target.checked })}
                    className="w-5 h-5 rounded-lg text-emerald-600 focus:ring-emerald-500 border-slate-300 cursor-pointer"
                  />
                  <span className="text-xs font-bold text-slate-700">
                    {isTa ? 'மாற்றுத்திறனாளி (Person with Disability)' : 'Person with Disability (PwD)'}
                  </span>
                </label>
              </div>
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-3.5 bg-gradient-to-r from-emerald-700 to-teal-700 hover:from-emerald-800 hover:to-teal-800 text-white font-bold rounded-2xl text-sm sm:text-base transition-all shadow-lg shadow-emerald-950/20 flex items-center justify-center gap-2 cursor-pointer active:scale-98"
          >
            <span>{isTa ? 'சுயவிவரத்தை சேமித்து திட்டங்களை காண்க' : 'Save Profile & Explore Eligible Schemes'}</span>
            <ArrowRight size={18} />
          </button>
        </form>
      </div>
    </div>
  );
};
