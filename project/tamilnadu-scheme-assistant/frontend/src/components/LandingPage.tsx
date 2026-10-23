import React from 'react';
import { Sparkles, ArrowRight, LogIn, UserPlus } from 'lucide-react';

interface LandingPageProps {
  onSignIn: (language: 'ta' | 'en') => void;
  onSignUp: (language: 'ta' | 'en') => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onSignIn, onSignUp }) => {
  const [lang, setLang] = React.useState<'ta' | 'en'>('ta');
  const isTa = lang === 'ta';

  React.useEffect(() => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-950 via-slate-900 to-teal-950 flex flex-col items-center justify-center p-4 sm:p-6 text-center relative overflow-hidden">
      
      {/* Ambient background glow orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-xl w-full bg-white/95 backdrop-blur-2xl rounded-3xl shadow-2xl shadow-black/30 p-6 sm:p-10 border border-white/60 my-6 relative z-10 animate-in fade-in zoom-in-95 duration-200">
        
        {/* Language selector in top right */}
        <div className="flex justify-end mb-2">
          <button
            type="button"
            onClick={() => setLang(isTa ? 'en' : 'ta')}
            className="text-xs bg-white/80 hover:bg-white text-slate-700 border border-slate-200/80 px-3 py-1 rounded-full font-bold shadow-xs transition-all active:scale-95 cursor-pointer"
          >
            {isTa ? '🌐 English' : '🇮🇳 தமிழ்'}
          </button>
        </div>

        <div className="w-24 h-24 rounded-full overflow-hidden mx-auto mb-4 flex items-center justify-center shadow-xl shadow-black/20 ring-4 ring-white bg-white">
          <img src="/tn-logo.png" alt="Tamil Nadu Government SchemeVoice" className="w-full h-full object-cover" />
        </div>

        <div className="inline-flex items-center gap-1.5 bg-emerald-50 border border-emerald-200/80 text-emerald-800 px-3 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider mb-2">
          <Sparkles size={12} className="text-amber-500" />
          <span>SchemeVoice AI</span>
        </div>

        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-1 leading-tight">
          {isTa ? 'தமிழ்நாடு அரசுத் திட்ட வழிகாட்டி' : 'TN Government Scheme Assistant'}
        </h1>
        <h2 className="text-sm sm:text-base font-semibold text-emerald-800 mb-4">
          {isTa ? 'அரசு நண்பன் - குடிமக்கள் குரல் வழிகாட்டி' : 'Arasu Nanban - Multilingual Voice Guide'}
        </h2>

        <p className="text-slate-600 text-xs sm:text-sm mb-6 max-w-md mx-auto leading-relaxed">
          {isTa 
            ? 'உங்கள் வயது, படிப்பு மற்றும் தொழில் விவரங்களை உள்ளிட்டு, உங்களுக்குத் தகுதியான 59+ தமிழ்நாடு அரசு நலத்திட்டங்களை உடனே கண்டறியுங்கள். குரல் மூலமாகவும் உரையாடலாம்.' 
            : 'Enter your profile details to instantly discover verified welfare schemes matched to your eligibility. Complete with natural human voice interaction.'}
        </p>

        {/* Action Buttons */}
        <div className="space-y-3">
          <button
            type="button"
            onClick={() => onSignUp(lang)}
            className="w-full py-3.5 bg-gradient-to-r from-emerald-700 to-teal-700 hover:from-emerald-800 hover:to-teal-800 text-white font-bold rounded-2xl text-sm transition-all shadow-md shadow-emerald-950/20 hover:scale-[1.01] active:scale-[0.99] flex items-center justify-center gap-2 cursor-pointer"
          >
            <UserPlus size={16} />
            <span>{isTa ? 'புதிய பதிவு & சுயவிவரம் (Sign Up / Register)' : 'Sign Up & Setup Profile'}</span>
            <ArrowRight size={16} />
          </button>

          <button
            type="button"
            onClick={() => onSignIn(lang)}
            className="w-full py-3 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 font-bold rounded-2xl text-sm transition-colors shadow-xs flex items-center justify-center gap-2 cursor-pointer active:scale-[0.99]"
          >
            <LogIn size={16} />
            <span>{isTa ? 'உள்நுழைக (Sign In)' : 'Sign In'}</span>
          </button>
        </div>

        <div className="mt-8 pt-4 border-t border-slate-100 text-[11px] text-slate-400">
          {isTa ? 'தமிழ்நாடு அரசு நலத்திட்ட வழிகாட்டி • 100% இலவசம் & பாதுகாப்பானது' : 'Tamil Nadu Welfare Scheme Assistant • ₹0 Cost Open Source'}
        </div>
      </div>
    </div>
  );
};
