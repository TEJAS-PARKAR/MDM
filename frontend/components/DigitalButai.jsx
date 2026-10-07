import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, Pause, SkipForward, SkipBack, RotateCcw, 
  Maximize, Minimize, Sliders, Volume2, Sparkles, MoveRight, Eye
} from 'lucide-react';
import LanguageSelector from './LanguageSelector';

export default function DigitalButai({
  story,
  currentPanelIndex,
  onPanelChange,
  currentLanguage,
  onLanguageChange,
  onToggleNarratorView,
  isNarratorOpen
}) {
  const [doorsOpen, setDoorsOpen] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [autoPlay, setAutoPlay] = useState(true);
  const [isSliding, setIsSliding] = useState(false);
  const [isNukikata, setIsNukikata] = useState(false); // Kamishibai half-pull suspense
  const [slidingDirection, setSlidingDirection] = useState('next');
  const [showSubtitles, setShowSubtitles] = useState(true);
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
  const [isMuted, setIsMuted] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [audioProgress, setAudioProgress] = useState(0);

  const audioRef = useRef(null);
  const sfxRef = useRef(null);
  const stageContainerRef = useRef(null);

  const panels = story?.panels || [];
  const currentPanel = panels[currentPanelIndex] || null;
  const nextPanel = panels[currentPanelIndex + 1] || null;

  // Sound effects player
  const playSfx = (sfxName) => {
    try {
      const sfx = new Audio(`/audio/${sfxName}.wav`);
      sfx.volume = 0.7;
      sfx.play().catch(() => {});
    } catch (e) {}
  };

  // Open / Close Stage Doors
  const toggleDoors = () => {
    if (!doorsOpen) {
      playSfx('hyoshigi'); // Traditional wooden clapper on stage opening
    }
    setDoorsOpen(!doorsOpen);
  };

  // Construct audio URL for current panel and language
  const getAudioUrl = (panelId, lang) => {
    if (!story) return '';
    return `/audio/${story.story_id}_panel_${panelId}_${lang}.mp3`;
  };

  // Construct image URL for a panel
  const getImageUrl = (panelId) => {
    if (!story) return '';
    return `/panels/${story.story_id}_panel_${panelId}.jpg`;
  };

  // Update audio source when panel or language changes
  useEffect(() => {
    if (!audioRef.current || !currentPanel) return;

    const audioUrl = getAudioUrl(currentPanel.panel_id, currentLanguage);
    const wasPlaying = isPlaying;

    audioRef.current.src = audioUrl;
    audioRef.current.playbackRate = playbackSpeed;
    audioRef.current.muted = isMuted;

    if (wasPlaying && doorsOpen) {
      audioRef.current.play().catch((e) => {
        console.warn("Audio autoplay blocked by browser policy:", e);
      });
    }
  }, [currentPanelIndex, currentLanguage, story?.story_id]);

  // Handle Play/Pause
  const togglePlayPause = () => {
    if (!doorsOpen) {
      toggleDoors();
    }

    if (!audioRef.current) return;

    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play().then(() => {
        setIsPlaying(true);
      }).catch((e) => {
        console.warn("Audio play prevented:", e);
        setIsPlaying(true);
      });
    }
  };

  // Audio event listeners
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleEnded = () => {
      setIsPlaying(false);
      setAudioProgress(100);

      // Auto-advance if AutoPlay enabled
      if (autoPlay && currentPanelIndex < panels.length - 1) {
        setTimeout(() => {
          advancePanel();
        }, 1200);
      }
    };

    const handleTimeUpdate = () => {
      if (audio.duration) {
        setAudioProgress((audio.currentTime / audio.duration) * 100);
      }
    };

    audio.addEventListener('ended', handleEnded);
    audio.addEventListener('timeupdate', handleTimeUpdate);

    return () => {
      audio.removeEventListener('ended', handleEnded);
      audio.removeEventListener('timeupdate', handleTimeUpdate);
    };
  }, [autoPlay, currentPanelIndex, panels.length]);

  // Physical Card Sliding to Next Panel
  const advancePanel = () => {
    if (currentPanelIndex >= panels.length - 1 || isSliding) return;

    playSfx('paper_slide');
    setIsSliding(true);
    setSlidingDirection('next');
    setIsNukikata(false);

    setTimeout(() => {
      onPanelChange(currentPanelIndex + 1);
      setIsSliding(false);
    }, 650);
  };

  // Slide Back to Previous Panel
  const previousPanel = () => {
    if (currentPanelIndex <= 0 || isSliding) return;

    playSfx('paper_slide');
    setIsSliding(true);
    setSlidingDirection('prev');
    setIsNukikata(false);

    setTimeout(() => {
      onPanelChange(currentPanelIndex - 1);
      setIsSliding(false);
    }, 650);
  };

  // Theatrical "Nukikata" Half-Pull Suspense Trigger
  const triggerNukikata = () => {
    playSfx('paper_slide');
    setIsNukikata(!isNukikata);
  };

  // Fullscreen toggle
  const toggleFullscreen = () => {
    if (!stageContainerRef.current) return;
    if (!document.fullscreenElement) {
      stageContainerRef.current.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      document.exitFullscreen().catch(() => {});
      setIsFullscreen(false);
    }
  };

  // Speed toggle
  const cyclePlaybackSpeed = () => {
    const speeds = [0.8, 1.0, 1.25];
    const nextIdx = (speeds.indexOf(playbackSpeed) + 1) % speeds.length;
    const nextSpeed = speeds[nextIdx];
    setPlaybackSpeed(nextSpeed);
    if (audioRef.current) {
      audioRef.current.playbackRate = nextSpeed;
    }
  };

  // Get current dialogue in selected language
  const getCurrentDialogueText = () => {
    if (!currentPanel?.dialogue) return "";
    return currentPanel.dialogue[currentLanguage] || currentPanel.dialogue.en || "";
  };

  return (
    <div ref={stageContainerRef} className="flex flex-col items-center w-full max-w-5xl mx-auto select-none">
      {/* Hidden Audio Player */}
      <audio ref={audioRef} preload="auto" />

      {/* TOP CONTROLS & LANGUAGE SWITCHER */}
      <div className="w-full mb-3">
        <LanguageSelector
          currentLanguage={currentLanguage}
          onLanguageChange={onLanguageChange}
          showSubtitles={showSubtitles}
          onToggleSubtitles={() => setShowSubtitles(!showSubtitles)}
          isMuted={isMuted}
          onToggleMute={() => {
            const next = !isMuted;
            setIsMuted(next);
            if (audioRef.current) audioRef.current.muted = next;
          }}
          isPlayingAudio={isPlaying}
        />
      </div>

      {/* THE DIGITAL BUTAI (WOODEN KAMISHIBAI STAGE) */}
      <div className="relative w-full aspect-[4/3] max-h-[640px] rounded-2xl p-4 md:p-6 butai-frame butai-wood-grain shadow-stage transition-all">
        
        {/* Brass Ornamental Corner Brackets */}
        <div className="absolute top-2 left-2 w-8 h-8 md:w-12 md:h-12 brass-bracket rounded-tl-lg pointer-events-none" />
        <div className="absolute top-2 right-2 w-8 h-8 md:w-12 md:h-12 brass-bracket rounded-tr-lg pointer-events-none" />
        <div className="absolute bottom-2 left-2 w-8 h-8 md:w-12 md:h-12 brass-bracket rounded-bl-lg pointer-events-none" />
        <div className="absolute bottom-2 right-2 w-8 h-8 md:w-12 md:h-12 brass-bracket rounded-br-lg pointer-events-none" />

        {/* Top Header Plate with Calligraphy */}
        <div className="absolute top-2 left-1/2 -translate-x-1/2 px-4 py-0.5 rounded-full bg-[#1e110b] border border-amber-600/50 text-[11px] font-serif tracking-widest text-amber-300/90 shadow-inner flex items-center gap-2">
          <span>◆</span>
          <span>伝統紙芝居 舞台 • DIGITAL BUTAI</span>
          <span>◆</span>
        </div>

        {/* INNER CARD VIEWPORT (Where the paper cards slide) */}
        <div className="relative w-full h-full rounded-xl overflow-hidden bg-[#0c0806] border-4 border-[#2b170e] shadow-2xl flex items-center justify-center">
          
          {/* UNDERNEATH CARD (Next card visible during slide-out) */}
          {nextPanel && (
            <div className="absolute inset-0 w-full h-full card-next-underneath">
              <img
                src={getImageUrl(nextPanel.panel_id)}
                alt={`Panel ${nextPanel.panel_id}`}
                className="w-full h-full object-cover brightness-95"
              />
            </div>
          )}

          {/* ACTIVE CURRENT KAMISHIBAI CARD */}
          {currentPanel ? (
            <div
              className={`absolute inset-0 w-full h-full kamishibai-card ${
                isSliding && slidingDirection === 'next'
                  ? 'card-slide-out-right'
                  : isNukikata
                  ? 'card-nukikata-half'
                  : 'card-current'
              }`}
            >
              <img
                src={getImageUrl(currentPanel.panel_id)}
                alt={`Panel ${currentPanel.panel_id}`}
                className="w-full h-full object-cover"
              />

              {/* Subtitles Overlay */}
              {showSubtitles && (
                <div className="absolute bottom-3 left-3 right-3 p-3.5 bg-black/85 backdrop-blur-md border border-amber-900/60 rounded-xl shadow-2xl transition-all">
                  <p className="text-sm md:text-base font-serif text-amber-100 text-center leading-relaxed">
                    {getCurrentDialogueText()}
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="text-amber-300 font-serif text-center p-6">
              <p className="text-lg">Select a Kamishibai story to place cards inside the Butai.</p>
            </div>
          )}

          {/* TRADITIONAL FOLDING WOODEN DOORS (TOBIRA) OVERLAY */}
          <div className={`absolute inset-0 flex stage-doors-overlay ${doorsOpen ? 'doors-open pointer-events-none' : 'doors-closed'}`}>
            {/* Left Door */}
            <div className="w-1/2 h-full butai-wood-grain border-r-2 border-amber-900/80 shadow-2xl flex flex-col items-end justify-center pr-6 stage-door-left relative">
              <div className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-24 brass-bracket rounded-l" />
              <div className="w-12 h-12 rounded-full brass-bracket flex items-center justify-center text-amber-950 font-bold shadow-lg mr-2 border border-amber-900">
                開
              </div>
            </div>

            {/* Right Door */}
            <div className="w-1/2 h-full butai-wood-grain border-l-2 border-amber-900/80 shadow-2xl flex flex-col items-start justify-center pl-6 stage-door-right relative">
              <div className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-24 brass-bracket rounded-r" />
              <div className="w-12 h-12 rounded-full brass-bracket flex items-center justify-center text-amber-950 font-bold shadow-lg ml-2 border border-amber-900">
                幕
              </div>
            </div>

            {/* Center Latch Button when doors are closed */}
            {!doorsOpen && (
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-auto bg-black/20">
                <button
                  onClick={toggleDoors}
                  className="group px-7 py-3 rounded-full brass-bracket text-amber-950 font-bold text-sm tracking-wider shadow-2xl hover:scale-105 transition-transform flex items-center gap-2 border-2 border-amber-800"
                >
                  <Sparkles className="w-4 h-4 text-amber-900 group-hover:rotate-45 transition-transform" />
                  <span>OPEN BUTAI DOORS (拍子木)</span>
                </button>
                <p className="text-xs text-amber-300/80 font-serif mt-3 drop-shadow">
                  Click to open the traditional stage doors and commence the story
                </p>
              </div>
            )}
          </div>
        </div>

        {/* BOTTOM STAGE SLOT (Slide Slot Details) */}
        <div className="absolute bottom-1 left-8 right-8 h-2 bg-[#120a06] rounded-full border-t border-amber-900/40 shadow-inner" />
      </div>

      {/* STAGE CONTROLS BAR */}
      <div className="w-full mt-3 p-3 bg-[#180e08]/95 border border-amber-900/60 rounded-xl shadow-xl flex flex-wrap items-center justify-between gap-3">
        
        {/* Left: Previous / Play / Next */}
        <div className="flex items-center gap-2">
          {/* Previous Card */}
          <button
            onClick={previousPanel}
            disabled={currentPanelIndex <= 0 || isSliding}
            className="p-2.5 rounded-lg bg-amber-950/40 border border-amber-800/40 text-amber-300 hover:text-white hover:bg-amber-900/50 disabled:opacity-30 disabled:pointer-events-none transition-all"
            title="Previous Card (←)"
          >
            <SkipBack className="w-4 h-4" />
          </button>

          {/* Play / Pause */}
          <button
            onClick={togglePlayPause}
            className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-500 hover:to-amber-600 text-white font-semibold text-sm shadow-lg shadow-amber-950/60 scale-100 active:scale-95 transition-all border border-amber-400/50"
            title={isPlaying ? "Pause Narration (Space)" : "Play Narration (Space)"}
          >
            {isPlaying ? (
              <>
                <Pause className="w-4 h-4 fill-current" />
                <span>Pause</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current ml-0.5" />
                <span>Play</span>
              </>
            )}
          </button>

          {/* Next Card (Slide Card) */}
          <button
            onClick={advancePanel}
            disabled={currentPanelIndex >= panels.length - 1 || isSliding}
            className="flex items-center gap-1.5 px-3 py-2.5 rounded-lg bg-amber-950/40 border border-amber-800/40 text-amber-200 hover:text-white hover:bg-amber-900/50 disabled:opacity-30 disabled:pointer-events-none transition-all"
            title="Slide Out Next Card (→)"
          >
            <span className="text-xs font-medium hidden sm:inline">Next Card</span>
            <SkipForward className="w-4 h-4" />
          </button>

          {/* Nukikata (Half-Pull Suspense) Button */}
          <button
            onClick={triggerNukikata}
            className={`flex items-center gap-1.5 px-3 py-2 rounded-lg border text-xs font-medium transition-all ${
              isNukikata
                ? 'bg-amber-500 text-amber-950 font-bold border-amber-300 shadow-md'
                : 'bg-black/30 border-amber-900/50 text-amber-300 hover:bg-amber-950/40'
            }`}
            title="Traditional Kamishibai half-pull to tease audience suspense"
          >
            <MoveRight className="w-3.5 h-3.5" />
            <span className="hidden md:inline">Half-Pull (抜き方)</span>
          </button>
        </div>

        {/* Center: Card Indicator & Timeline Progress */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-3 py-1 bg-black/40 border border-amber-900/40 rounded-full text-xs font-serif text-amber-300">
            <span>Card</span>
            <strong className="text-white">{currentPanelIndex + 1}</strong>
            <span className="text-amber-500">/</span>
            <span>{panels.length || 0}</span>
          </div>

          {/* Autoplay toggle */}
          <button
            onClick={() => setAutoPlay(!autoPlay)}
            className={`px-2.5 py-1 rounded-full text-xs border transition-colors ${
              autoPlay
                ? 'bg-amber-900/60 border-amber-600 text-amber-200'
                : 'bg-black/30 border-amber-950 text-amber-500/50 hover:text-amber-400'
            }`}
            title="Auto-slide to next card when narration ends"
          >
            Auto-Play: <strong>{autoPlay ? 'ON' : 'OFF'}</strong>
          </button>
        </div>

        {/* Right: Stage Speed, Behind-the-Butai Narrator, Fullscreen */}
        <div className="flex items-center gap-2">
          {/* Speed Toggle */}
          <button
            onClick={cyclePlaybackSpeed}
            className="px-2.5 py-1.5 rounded-lg bg-black/30 border border-amber-900/40 text-xs font-medium text-amber-300 hover:bg-amber-900/30 transition-colors"
            title="Narration Speed"
          >
            {playbackSpeed}x
          </button>

          {/* Behind the Butai (Narrator View) */}
          <button
            onClick={onToggleNarratorView}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium transition-all ${
              isNarratorOpen
                ? 'bg-amber-700/80 border-amber-400 text-white shadow-md'
                : 'bg-black/30 border-amber-900/50 text-amber-300 hover:bg-amber-900/30'
            }`}
            title="Toggle Narrator Rear View with stage directions and trilingual text"
          >
            <Eye className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Behind Butai (裏舞台)</span>
          </button>

          {/* Door Toggle Button */}
          <button
            onClick={toggleDoors}
            className="p-2 rounded-lg bg-black/30 border border-amber-900/40 text-amber-300 hover:text-white hover:bg-amber-900/30 transition-colors"
            title={doorsOpen ? "Close Doors (閉幕)" : "Open Doors (開幕)"}
          >
            <span className="text-xs font-serif">{doorsOpen ? '閉幕' : '開幕'}</span>
          </button>

          {/* Fullscreen */}
          <button
            onClick={toggleFullscreen}
            className="p-2 rounded-lg bg-black/30 border border-amber-900/40 text-amber-300 hover:text-white hover:bg-amber-900/30 transition-colors"
            title="Fullscreen Theatrical Mode"
          >
            {isFullscreen ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* AUDIO PROGRESS BAR (Scrubber) */}
      <div className="w-full mt-2 h-1.5 bg-black/40 rounded-full overflow-hidden border border-amber-900/30">
        <div
          className="h-full bg-gradient-to-r from-amber-600 to-amber-400 transition-all duration-150"
          style={{ width: `${audioProgress}%` }}
        />
      </div>

      {/* PANEL THUMBNAIL REEL */}
      <div className="flex items-center gap-2 overflow-x-auto w-full mt-3 py-2 px-1 scrollbar-thin">
        {panels.map((p, idx) => {
          const isCurrent = idx === currentPanelIndex;
          return (
            <button
              key={p.panel_id}
              onClick={() => {
                if (idx !== currentPanelIndex) {
                  playSfx('paper_slide');
                  onPanelChange(idx);
                }
              }}
              className={`flex-shrink-0 relative w-20 md:w-24 aspect-[4/3] rounded-lg overflow-hidden border-2 transition-all ${
                isCurrent
                  ? 'border-amber-400 scale-105 shadow-md shadow-amber-900/50 brightness-105'
                  : 'border-amber-900/40 opacity-60 hover:opacity-100 hover:border-amber-600'
              }`}
            >
              <img
                src={getImageUrl(p.panel_id)}
                alt={`Thumbnail ${p.panel_id}`}
                className="w-full h-full object-cover"
              />
              <span className="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-black/80 text-[10px] font-bold text-amber-200">
                #{p.panel_id}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
