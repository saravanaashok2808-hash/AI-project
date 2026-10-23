import { useState, useEffect } from 'react';
import { AuthPage } from './components/AuthPage';
import { ProfileOnboarding } from './components/ProfileOnboarding';
import { AssistantPage } from './components/AssistantPage';
import { ApiClient } from './api/client';
import type { UserProfile } from './types';

type AppState = 'auth' | 'onboarding' | 'assistant';

function App() {
  const [appState, setAppState] = useState<AppState>('auth');
  const [previousState, setPreviousState] = useState<AppState>('auth');
  const [language, setLanguage] = useState<'ta' | 'en'>('ta');
  const [currentCitizen, setCurrentCitizen] = useState<UserProfile>({});
  const [onboardingInitialProfile, setOnboardingInitialProfile] = useState<UserProfile>({});

  // Check for saved citizen session on startup and verify token with backend
  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = ApiClient.getAuthToken();
        if (token) {
          const user = await ApiClient.getMe();
          if (user && user.profile) {
            setCurrentCitizen(user.profile);
            return;
          }
        }
      } catch {
        ApiClient.clearAuth();
      }

      try {
        const saved = localStorage.getItem('tn_current_citizen');
        if (saved) {
          const parsed = JSON.parse(saved);
          if (parsed && parsed.name) {
            setCurrentCitizen(parsed);
          }
        }
      } catch {
        // Ignore parse errors
      }
    };

    initAuth();
  }, []);

  // Stop all voice synthesis whenever leaving the assistant page
  useEffect(() => {
    if (appState !== 'assistant' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }, [appState]);

  const handleAuthLogin = (profile: UserProfile) => {
    setCurrentCitizen(profile);
    localStorage.setItem('tn_current_citizen', JSON.stringify(profile));
    setAppState('assistant');
  };

  const handleAuthSignUp = (initialProfile: UserProfile) => {
    setPreviousState('auth');
    setOnboardingInitialProfile(initialProfile);
    setAppState('onboarding');
  };

  const handleOnboardingComplete = async (profile: UserProfile) => {
    setCurrentCitizen(profile);
    localStorage.setItem('tn_current_citizen', JSON.stringify(profile));

    // If authenticated, sync profile updates to backend database
    try {
      if (ApiClient.getAuthToken()) {
        await ApiClient.updateProfile(profile);
      }
    } catch (e) {
      console.warn('Could not sync profile to backend:', e);
    }

    // Also update saved citizens list
    try {
      const existingStr = localStorage.getItem('tn_saved_citizens');
      const existing: UserProfile[] = existingStr ? JSON.parse(existingStr) : [];
      const filtered = existing.filter(c => c.name?.toLowerCase() !== profile.name?.toLowerCase());
      filtered.unshift(profile);
      localStorage.setItem('tn_saved_citizens', JSON.stringify(filtered.slice(0, 10)));
    } catch {
      // Ignore error
    }

    setAppState('assistant');
  };

  const handleEditProfile = () => {
    setPreviousState('assistant');
    setOnboardingInitialProfile(currentCitizen);
    setAppState('onboarding');
  };

  const handleLogout = () => {
    ApiClient.clearAuth();
    localStorage.removeItem('tn_current_citizen');
    setCurrentCitizen({});
    setAppState('auth');
  };

  const handleHome = () => {
    setAppState('auth');
  };

  return (
    <>
      {appState === 'auth' && (
        <AuthPage 
          language={language}
          onLanguageChange={setLanguage}
          onLogin={handleAuthLogin}
          onSignUp={handleAuthSignUp}
        />
      )}

      {appState === 'onboarding' && (
        <ProfileOnboarding 
          language={language}
          initialProfile={onboardingInitialProfile}
          onComplete={handleOnboardingComplete}
          onBack={() => setAppState(previousState)}
        />
      )}

      {appState === 'assistant' && (
        <AssistantPage 
          language={language}
          initialProfile={currentCitizen}
          onHome={handleHome}
          onEditProfile={handleEditProfile}
          onLogout={handleLogout}
        />
      )}
    </>
  );
}

export default App;
