import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square } from 'lucide-react';

interface AudioRecorderProps {
  onTranscription: (text: string) => void;
  language?: 'ta-IN' | 'en-IN';
  onStart?: () => void;
  onError?: (errorMessage: string) => void;
  onRecordingStateChange?: (isRecording: boolean) => void;
  disabled?: boolean;
}

declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

export const AudioRecorder: React.FC<AudioRecorderProps> = ({
  onTranscription,
  language = 'ta-IN',
  onStart,
  onError,
  onRecordingStateChange,
  disabled = false
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    onRecordingStateChange?.(isRecording);
  }, [isRecording, onRecordingStateChange]);

  const cleanupRecognition = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.onresult = null;
        recognitionRef.current.onerror = null;
        recognitionRef.current.onend = null;
        recognitionRef.current.onstart = null;
        recognitionRef.current.abort();
      } catch (e) {
        // Ignore cleanup errors
      }
      recognitionRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      cleanupRecognition();
    };
  }, []);

  const startListening = () => {
    if (disabled || isRecording) return;

    // 1. Verify Browser Support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      const errorMsg = 'குரல் உள்ளீடு இந்த உலாவியில் கிடைக்கவில்லை. Chrome அல்லது Edge உலாவியைப் பயன்படுத்தவும். (Speech recognition is not supported in this browser. Please use Chrome or Edge.)';
      onError?.(errorMsg);
      return;
    }

    // 2. Initialize Clean SpeechRecognition
    cleanupRecognition();

    try {
      const recognition = new SpeechRecognition();
      recognitionRef.current = recognition;

      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.maxAlternatives = 1;
      recognition.lang = language;

      recognition.onstart = () => {
        setIsRecording(true);
        onStart?.();
      };

      recognition.onresult = (event: any) => {
        let fullTranscript = '';
        for (let i = 0; i < event.results.length; ++i) {
          const item = event.results[i];
          if (item && item[0]) {
            fullTranscript += item[0].transcript;
          }
        }

        const candidateText = fullTranscript.trim();
        if (candidateText) {
          onTranscription(candidateText);
        }
      };

      recognition.onerror = (event: any) => {
        console.warn('Speech recognition error event:', event.error);
        setIsRecording(false);

        if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
          onError?.('மைக்ரோஃபோன் அனுமதி மறுக்கப்பட்டுள்ளது. முகவரிப் பட்டியில் உள்ள லாக்/மைக் ஐகானைக் கிளிக் செய்து அனுமதிக்கவும். (Microphone permission was denied. Please allow microphone access in your browser address bar.)');
        } else if (event.error === 'audio-capture') {
          onError?.('மைக்ரோஃபோன் சாதனம் கிடைக்கவில்லை. (Microphone hardware not available.)');
        } else if (event.error === 'network') {
          onError?.('இணைய தொடர்பு அல்லது குரல் சேவை கிடைக்கவில்லை. (Network error or voice service unavailable.)');
        } else if (event.error !== 'aborted' && event.error !== 'no-speech') {
          onError?.(`குரல் அறிதல் பிழை: ${event.error}`);
        }
      };

      recognition.onend = () => {
        setIsRecording(false);
      };

      recognition.start();
      setIsRecording(true);
    } catch (e: any) {
      console.error('Failed to start speech recognition:', e);
      setIsRecording(false);
      onError?.(`குரல் பதிவை தொடங்க முடியவில்லை: ${e.message || e}`);
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (e) {
        // Ignore
      }
    }
    setIsRecording(false);
  };

  const toggleRecording = (e: React.MouseEvent) => {
    e.preventDefault();
    if (isRecording) {
      stopListening();
    } else {
      startListening();
    }
  };

  return (
    <button
      type="button"
      onClick={toggleRecording}
      disabled={disabled}
      className={`p-3 rounded-2xl flex items-center justify-center transition-all cursor-pointer relative shadow-sm ${
        disabled
          ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
          : isRecording
          ? 'bg-rose-600 text-white animate-pulse ring-4 ring-rose-200 scale-105'
          : 'bg-emerald-700 hover:bg-emerald-800 text-white active:scale-95 shadow-md shadow-emerald-950/15'
      }`}
      aria-label={isRecording ? 'Stop voice input' : 'Start voice input'}
      title={isRecording ? 'பேசுவதை நிறுத்த கிளிக் செய்யவும் (Click to stop)' : 'குரல் மூலம் பேச கிளிக் செய்யவும் (Click to speak)'}
    >
      {isRecording ? (
        <Square size={18} className="fill-current" />
      ) : (
        <Mic size={19} />
      )}
    </button>
  );
};
