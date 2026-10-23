import React from 'react';
import type { UserProfile } from '../types';
import { User, X, ShieldCheck, MapPin, Briefcase, GraduationCap, IndianRupee, Heart, Award, Trash2 } from 'lucide-react';

interface ProfileSidebarProps {
  profile: UserProfile;
  isOpen: boolean;
  onClose: () => void;
  onClearSession: () => void;
  language: 'ta' | 'en';
}

export const ProfileSidebar: React.FC<ProfileSidebarProps> = ({ profile, isOpen, onClose, onClearSession, language }) => {
  const isTa = language === 'ta';

  if (!isOpen) return null;

  return (
    <>
      {/* Blurred Backdrop */}
      <div 
        className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-40 transition-opacity animate-in fade-in duration-200" 
        onClick={onClose} 
      />
      
      {/* Drawer */}
      <div className="fixed inset-y-0 right-0 max-w-sm w-full bg-white/95 backdrop-blur-2xl shadow-2xl z-50 transform transition-transform overflow-y-auto flex flex-col border-l border-white/80 animate-in slide-in-from-right duration-300">
        
        {/* Header */}
        <div className="p-5 bg-gradient-to-r from-emerald-800 via-emerald-700 to-teal-800 text-white flex justify-between items-center relative overflow-hidden shadow-md">
          <div className="absolute -right-6 -bottom-6 w-24 h-24 bg-white/10 rounded-full blur-xl pointer-events-none" />
          
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-white/15 backdrop-blur-md border border-white/20 flex items-center justify-center text-[#FFD700] shadow-inner font-bold text-lg">
              {profile.name ? profile.name.charAt(0).toUpperCase() : 'கு'}
            </div>
            <div>
              <h2 className="text-base font-bold leading-tight flex items-center gap-1.5">
                <span>{profile.name || (isTa ? 'குடிமக்கள்' : 'Citizen Profile')}</span>
              </h2>
              <span className="text-[11px] text-emerald-200 flex items-center gap-1">
                <ShieldCheck size={12} className="text-[#FFD700]" />
                {isTa ? 'சரிபார்க்கப்பட்ட சுயவிவரம்' : 'Verified Welfare Profile'}
              </span>
            </div>
          </div>

          <button 
            type="button"
            onClick={onClose} 
            className="p-1.5 hover:bg-white/20 active:scale-95 rounded-full transition-all text-white/90 hover:text-white cursor-pointer"
            aria-label="Close"
          >
            <X size={20} />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-5 flex-1 space-y-4">
          <div className="p-3 bg-emerald-50/70 rounded-2xl border border-emerald-100/70 text-xs text-emerald-900 leading-relaxed flex items-start gap-2">
            <span className="text-base">🎯</span>
            <p>
              {isTa 
                ? 'உங்கள் விவரங்களின் அடிப்படையில் AI தானாகவே தகுதியான அரசு நலத்திட்டங்களை பரிந்துரைக்கிறது.' 
                : 'SchemeVoice AI analyzes these parameters to accurately match eligible welfare schemes for you.'}
            </p>
          </div>

          {/* Profile Details Grid */}
          <div className="space-y-2.5">
            <ProfileField 
              icon={<User size={15} className="text-emerald-600" />}
              label={isTa ? 'வயது மற்றும் பாலினம்' : 'Age & Gender'} 
              value={`${profile.age || 24} ${isTa ? 'வயது' : 'Years'}, ${
                profile.gender === 'Female' ? (isTa ? 'பெண்' : 'Female') :
                profile.gender === 'Male' ? (isTa ? 'ஆண்' : 'Male') :
                (isTa ? 'மற்றவை' : 'Others')
              }`} 
            />

            <ProfileField 
              icon={<MapPin size={15} className="text-emerald-600" />}
              label={isTa ? 'மாவட்டம்' : 'District'} 
              value={profile.district || (isTa ? 'தமிழ்நாடு' : 'Tamil Nadu')} 
            />

            <ProfileField 
              icon={<GraduationCap size={15} className="text-emerald-600" />}
              label={isTa ? 'கல்வித் தகுதி' : 'Education'} 
              value={profile.education_level || (isTa ? 'பட்டதாரி' : 'Graduate')} 
            />

            <ProfileField 
              icon={<Briefcase size={15} className="text-emerald-600" />}
              label={isTa ? 'வேலை மற்றும் பணி' : 'Occupation / Employment'} 
              value={`${profile.employment_status || (isTa ? 'வேலை தேடுபவர்' : 'Unemployed')} • ${profile.occupation || (isTa ? 'விவசாயி' : 'Farmer')}`} 
            />

            <ProfileField 
              icon={<IndianRupee size={15} className="text-emerald-600" />}
              label={isTa ? 'ஆண்டு வருமானம்' : 'Annual Income'} 
              value={profile.income ? `₹${profile.income.toLocaleString('en-IN')}` : '₹60,000'} 
            />

            <ProfileField 
              icon={<Award size={15} className="text-emerald-600" />}
              label={isTa ? 'இடஒதுக்கீடு பிரிவு' : 'Social Category'} 
              value={profile.caste_category || 'BC / General'} 
            />

            <ProfileField 
              icon={<Heart size={15} className="text-emerald-600" />}
              label={isTa ? 'திருமண நிலை' : 'Marital Status'} 
              value={profile.marital_status || (isTa ? 'திருமணம் ஆகாதவர்' : 'Single')} 
            />

            {profile.disability && (
              <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-900 font-semibold flex items-center gap-2">
                <span>♿</span>
                <span>{isTa ? 'மாற்றுத்திறனாளி சிறப்பு நலத்திட்டங்கள் பொருந்தும்' : 'Eligible for Special Disability Welfare'}</span>
              </div>
            )}
          </div>
        </div>

        {/* Footer Area */}
        <div className="p-4 border-t border-slate-100 bg-slate-50/80 space-y-3">
          <div className="flex items-center gap-2 text-[11px] text-slate-500">
            <ShieldCheck size={14} className="text-emerald-600 shrink-0" />
            <span>{isTa ? 'அனைத்து தரவுகளும் உங்கள் உலாவியில் மட்டுமே பாதுகாப்பாக சேமிக்கப்படுகின்றன.' : 'Your data is processed securely on your browser device.'}</span>
          </div>

          <button
            type="button"
            onClick={onClearSession}
            className="w-full py-2.5 px-4 bg-white hover:bg-rose-50 border border-slate-200 hover:border-rose-200 text-slate-600 hover:text-rose-600 rounded-xl text-xs font-bold transition-all shadow-xs flex items-center justify-center gap-1.5 cursor-pointer active:scale-98"
          >
            <Trash2 size={14} />
            <span>{isTa ? 'சுயவிவரத்தை மீட்டமை (Reset Profile)' : 'Reset Profile & Clear Data'}</span>
          </button>
        </div>
      </div>
    </>
  );
};

const ProfileField = ({ icon, label, value }: { icon: React.ReactNode; label: string; value?: string }) => {
  return (
    <div className="p-3 bg-slate-50/90 rounded-xl border border-slate-200/70 hover:border-emerald-200 transition-colors">
      <div className="flex items-center gap-1.5 text-[11px] font-semibold text-slate-500 mb-0.5">
        {icon}
        <span>{label}</span>
      </div>
      <div className="text-xs sm:text-sm font-bold text-slate-800 pl-5">
        {value || <span className="text-slate-400 font-normal italic">Not specified</span>}
      </div>
    </div>
  );
};
