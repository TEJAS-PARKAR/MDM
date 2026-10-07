import React from 'react';
import { Volume2, VolumeX, Subtitles, Globe, Sparkles } from 'lucide-react';

export default function LanguageSelector({
  currentLanguage,
  onLanguageChange,
  showSubtitles,
  onToggleSubtitles,
  isMuted,
  onToggleMute,
  isPlayingAudio
}) {
  const languages = [
    {
      code: 'en',
      label: 'English',
      native: 'English',
      flag: '🇬🇧',
      voiceName: 'Christopher Neural',
      accentColor: 'border-blue-500/80 bg-blue-950/40 text-blue-200'
    },
    {
      code: 'hi',
      label: 'Hindi',
      native: 'हिन्दी',
      flag: '🇮🇳',
      voiceName: 'Madhur (कथावाचक)',
      accentColor: 'border-orange-500/80 bg-orange-950/40 text-orange-200'
    },
    {
      code: 'ja',
      label: 'Japanese',
      native: '日本語',
      flag: '🇯🇵',
      voiceName: 'Nanami (紙芝居師)',
      accentColor: 'border-red-500/80 bg-red-950/40 text-red-200'
    }
  ];

  const activeLang = languages.find(l => l.code === currentLanguage) || languages[0];

  return (
    <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-2.5 bg-[#1a0f0a]/90 border border-amber-900/50 rounded-xl backdrop-blur-md shadow-lg">
      {/* Language Pills */}
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1.5 text-xs text-amber-300/80 font-medium mr-1 uppercase tracking-wider">
          <Globe className="w-3.5 h-3.5 text-amber-400" />
          <span>Narration:</span>
        </div>

        <div className="flex items-center p-1 bg-[#120a06] border border-amber-900/40 rounded-lg gap-1">
          {languages.map((lang) => {
            const isActive = currentLanguage === lang.code;
            return (
              <button
                key={lang.code}
                onClick={() => onLanguageChange(lang.code)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-amber-600/90 text-white shadow-md shadow-amber-950/50 scale-[1.02] border border-amber-400/50'
                    : 'text-amber-200/70 hover:text-amber-100 hover:bg-amber-950/30'
                }`}
                title={`Switch to ${lang.label} narration`}
              >
                <span className="text-sm">{lang.flag}</span>
                <span className="font-semibold">{lang.native}</span>
                {isActive && (
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 animate-pulse" />
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Voice Badge & Audio Controls */}
      <div className="flex items-center gap-3">
        {/* Active Neural Voice Indicator */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 bg-amber-950/40 border border-amber-800/40 rounded-full text-[11px] text-amber-300/90">
          <Sparkles className="w-3 h-3 text-amber-400 animate-spin" style={{ animationDuration: '6s' }} />
          <span>Voice: <strong className="font-semibold text-amber-200">{activeLang.voiceName}</strong></span>
          {isPlayingAudio && (
            <span className="inline-flex gap-0.5 items-end h-3 ml-1">
              <span className="w-0.5 h-2 bg-amber-400 animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-0.5 h-3 bg-amber-400 animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-0.5 h-1.5 bg-amber-400 animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </span>
          )}
        </div>

        {/* Subtitle toggle */}
        <button
          onClick={onToggleSubtitles}
          className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border text-xs font-medium transition-colors ${
            showSubtitles
              ? 'bg-amber-800/50 border-amber-500 text-amber-200'
              : 'bg-black/30 border-amber-900/40 text-amber-400/50 hover:text-amber-300'
          }`}
          title={showSubtitles ? "Hide Subtitles" : "Show Subtitles"}
        >
          <Subtitles className="w-3.5 h-3.5" />
          <span className="hidden md:inline">{showSubtitles ? 'Captions ON' : 'Captions'}</span>
        </button>

        {/* Audio Mute / Unmute */}
        <button
          onClick={onToggleMute}
          className="p-1.5 rounded-lg bg-black/30 border border-amber-900/40 text-amber-300 hover:text-amber-100 hover:bg-amber-900/30 transition-colors"
          title={isMuted ? "Unmute Audio" : "Mute Audio"}
        >
          {isMuted ? (
            <VolumeX className="w-4 h-4 text-red-400" />
          ) : (
            <Volume2 className="w-4 h-4 text-amber-300" />
          )}
        </button>
      </div>
    </div>
  );
}
