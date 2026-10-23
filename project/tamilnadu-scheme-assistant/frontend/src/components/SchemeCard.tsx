import React, { useState } from 'react';
import { ExternalLink, ChevronDown, ChevronUp, FileText, CheckCircle2, AlertTriangle, XCircle, HelpCircle, Building2, Sparkles, Calendar } from 'lucide-react';
import type { Scheme, EligibilityStatus } from '../types';

interface SchemeCardProps {
  scheme: Scheme;
  eligibilityStatus?: EligibilityStatus;
  eligibilityReason?: string;
  language: 'ta' | 'en';
  onAskAbout?: (question: string) => void;
}

const getEligibilityConfig = (status?: EligibilityStatus) => {
  switch (status) {
    case 'ELIGIBLE':
      return {
        badgeClass: 'bg-emerald-50 text-emerald-800 border-emerald-200/80 shadow-xs ring-1 ring-emerald-500/10',
        icon: <CheckCircle2 size={14} className="text-emerald-600" />,
        labelEn: 'Eligible for You',
        labelTa: 'உங்களுக்கு தகுதியானது'
      };
    case 'POTENTIALLY_ELIGIBLE':
      return {
        badgeClass: 'bg-amber-50 text-amber-800 border-amber-200/80 shadow-xs ring-1 ring-amber-500/10',
        icon: <AlertTriangle size={14} className="text-amber-600" />,
        labelEn: 'Potentially Eligible',
        labelTa: 'தகுதி பெற வாய்ப்புள்ளது'
      };
    case 'NOT_APPEARING_ELIGIBLE':
      return {
        badgeClass: 'bg-rose-50 text-rose-800 border-rose-200/80 shadow-xs',
        icon: <XCircle size={14} className="text-rose-500" />,
        labelEn: 'Not Eligible',
        labelTa: 'தகுதியற்றவர்'
      };
    case 'INSUFFICIENT':
      return {
        badgeClass: 'bg-slate-50 text-slate-700 border-slate-200/80 shadow-xs',
        icon: <HelpCircle size={14} className="text-slate-500" />,
        labelEn: 'More Info Needed',
        labelTa: 'கூடுதல் தகவல் தேவை'
      };
    default:
      return null;
  }
};

export const SchemeCard: React.FC<SchemeCardProps> = ({ scheme, eligibilityStatus, eligibilityReason, language, onAskAbout }) => {
  const [expandedSection, setExpandedSection] = useState<'docs' | 'steps' | null>(null);
  
  const isTa = language === 'ta';
  const name = isTa ? scheme.name_ta : scheme.name_en;
  const secondaryName = isTa ? scheme.name_en : scheme.name_ta;
  const benefits = isTa ? scheme.benefits_ta : scheme.benefits_en;
  const documents = isTa ? scheme.documents_ta : scheme.documents_en;
  const steps = isTa ? scheme.application_steps_ta : scheme.application_steps_en;
  
  const eligConfig = getEligibilityConfig(eligibilityStatus);

  const toggleSection = (section: 'docs' | 'steps') => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  return (
    <div className="bg-white/95 backdrop-blur-md rounded-2xl sm:rounded-3xl border border-slate-200/80 shadow-lg shadow-emerald-950/5 hover:shadow-xl hover:shadow-emerald-950/8 transition-all duration-300 overflow-hidden mb-4 group">
      
      {/* Top Department & Status Bar */}
      <div className="p-4 sm:p-5 border-b border-slate-100">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-800 text-xs font-semibold border border-emerald-100/80">
            <Building2 size={12} className="text-emerald-600" />
            <span className="truncate max-w-[240px] sm:max-w-none">{scheme.department}</span>
          </div>

          {eligConfig && (
            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${eligConfig.badgeClass}`}>
              {eligConfig.icon}
              {isTa ? eligConfig.labelTa : eligConfig.labelEn}
            </span>
          )}
        </div>

        {/* Scheme Title */}
        <h3 className="text-base sm:text-lg font-bold text-slate-900 group-hover:text-emerald-900 transition-colors leading-snug">
          {name}
        </h3>
        {secondaryName && (
          <p className="text-xs text-slate-500 font-medium mt-0.5">
            {secondaryName}
          </p>
        )}

        {/* Eligibility Contextual Explanation */}
        {eligibilityReason && (
          <div className="mt-3 text-xs sm:text-sm p-3 rounded-xl bg-gradient-to-r from-emerald-50/70 via-teal-50/50 to-slate-50 border border-emerald-100/70 text-slate-700 leading-relaxed">
            <span className="font-semibold text-emerald-900 mr-1.5">
              {isTa ? '💡 தகுதி விவரம்:' : '💡 Match Reason:'}
            </span>
            {eligibilityReason}
          </div>
        )}

        {/* Key Benefits */}
        <div className="mt-4">
          <div className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <Sparkles size={13} className="text-amber-500" />
            <span>{isTa ? 'முக்கிய பயன்கள்' : 'Key Benefits'}</span>
          </div>
          <div className="space-y-1.5">
            {benefits.map((benefit, idx) => (
              <div key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-slate-600">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-2 shrink-0" />
                <span className="leading-relaxed">{benefit}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Accordion Buttons */}
      <div className="bg-slate-50/80 p-2 border-b border-slate-100 flex flex-col sm:flex-row gap-1.5">
        <button
          type="button"
          onClick={() => toggleSection('docs')}
          className={`flex-1 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold flex items-center justify-between transition-all cursor-pointer ${
            expandedSection === 'docs'
              ? 'bg-white text-emerald-800 shadow-sm border border-emerald-100'
              : 'text-slate-600 hover:bg-white/60 hover:text-slate-900'
          }`}
        >
          <span className="flex items-center gap-2">
            <FileText size={15} className={expandedSection === 'docs' ? 'text-emerald-600' : 'text-slate-400'} />
            <span>{isTa ? 'தேவையான ஆவணங்கள்' : 'Required Documents'}</span>
            <span className="text-[10px] bg-slate-200/80 text-slate-700 px-1.5 py-0.5 rounded-full font-bold">
              {documents.length}
            </span>
          </span>
          {expandedSection === 'docs' ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
        </button>

        <button
          type="button"
          onClick={() => toggleSection('steps')}
          className={`flex-1 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold flex items-center justify-between transition-all cursor-pointer ${
            expandedSection === 'steps'
              ? 'bg-white text-emerald-800 shadow-sm border border-emerald-100'
              : 'text-slate-600 hover:bg-white/60 hover:text-slate-900'
          }`}
        >
          <span className="flex items-center gap-2">
            <CheckCircle2 size={15} className={expandedSection === 'steps' ? 'text-emerald-600' : 'text-slate-400'} />
            <span>{isTa ? 'விண்ணப்பிக்கும் முறை' : 'How to Apply'}</span>
            <span className="text-[10px] bg-slate-200/80 text-slate-700 px-1.5 py-0.5 rounded-full font-bold">
              {steps.length}
            </span>
          </span>
          {expandedSection === 'steps' ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
        </button>
      </div>

      {/* Expanded Documents Pane */}
      {expandedSection === 'docs' && (
        <div className="p-4 bg-white/90 text-xs sm:text-sm text-slate-600 border-b border-slate-100 animate-in fade-in duration-200">
          <ul className="space-y-2">
            {documents.map((doc, idx) => (
              <li key={idx} className="flex items-start gap-2.5">
                <span className="w-5 h-5 rounded-lg bg-emerald-50 text-emerald-700 text-xs font-bold flex items-center justify-center shrink-0 border border-emerald-100">
                  {idx + 1}
                </span>
                <span className="leading-relaxed">{doc}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Expanded Steps Pane */}
      {expandedSection === 'steps' && (
        <div className="p-4 bg-white/90 text-xs sm:text-sm text-slate-600 border-b border-slate-100 animate-in fade-in duration-200">
          <ol className="space-y-2.5">
            {steps.map((step, idx) => (
              <li key={idx} className="flex items-start gap-2.5">
                <span className="w-5 h-5 rounded-full bg-emerald-600 text-white text-[11px] font-bold flex items-center justify-center shrink-0 shadow-xs">
                  {idx + 1}
                </span>
                <span className="leading-relaxed">{step}</span>
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* Footer Info & Official Portal Button */}
      <div className="p-3.5 sm:p-4 bg-white/60 flex flex-wrap justify-between items-center gap-3">
        <div className="text-[11px] text-slate-400 flex items-center gap-1">
          <Calendar size={12} />
          <span>
            {isTa ? 'சரிபார்க்கப்பட்டது:' : 'Verified:'} {new Date(scheme.last_verified_date).toLocaleDateString()}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {onAskAbout && (
            <button
              type="button"
              onClick={() => onAskAbout(isTa ? `${name} திட்டத்தின் முழு விவரங்கள் என்ன?` : `Tell me all details about ${name}`)}
              className="inline-flex items-center gap-1 px-3 py-1.5 rounded-xl text-xs font-bold text-emerald-800 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 transition-all active:scale-95 cursor-pointer"
              title={isTa ? 'இத்திட்டம் குறித்து AI-யிடம் கேட்க' : 'Ask AI Assistant about this scheme'}
            >
              <Sparkles size={12} className="text-emerald-700" />
              <span>{isTa ? 'AI-யிடம் கேட்க' : 'Ask AI'}</span>
            </button>
          )}

          <a
            href={scheme.official_link}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-emerald-700 to-teal-700 hover:from-emerald-800 hover:to-teal-800 shadow-sm transition-all active:scale-95 group/btn"
          >
            <span>{isTa ? 'அதிகாரப்பூர்வ தளம்' : 'Official Portal'}</span>
            <ExternalLink size={12} className="transition-transform group-hover/btn:translate-x-0.5 group-hover/btn:-translate-y-0.5" />
          </a>
        </div>
      </div>
    </div>
  );
};
