import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { 
  ArrowLeft, BookOpen, Layers, Sparkles, RefreshCw, 
  ChevronDown, HelpCircle, Volume2, Info, Eye
} from 'lucide-react';
import DigitalButai from '../components/DigitalButai';
import NarratorPanel from '../components/NarratorPanel';

export default function StagePage() {
  const router = useRouter();
  const { story_id, custom } = router.query;

  const [story, setStory] = useState(null);
  const [currentPanelIndex, setCurrentPanelIndex] = useState(0);
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [isNarratorOpen, setIsNarratorOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [storyList, setStoryList] = useState([]);

  // Load available presets list
  useEffect(() => {
    fetch('/api/narrative/presets')
      .then((res) => res.json())
      .then((data) => setStoryList(data))
      .catch((err) => console.error("Error loading presets list:", err));
  }, []);

  // Load selected story
  useEffect(() => {
    const activeId = story_id || 'monkey-and-crocodile';
    setIsLoading(true);
    setError(null);
    setCurrentPanelIndex(0);

    if (custom === 'true') {
      try {
        const stored = sessionStorage.getItem('current_custom_story');
        if (stored) {
          const parsed = JSON.parse(stored);
          setStory(parsed);
          setIsLoading(false);
          return;
        }
      } catch (e) {
        console.warn("Could not load custom story from session:", e);
      }
    }

    // Fetch preset from backend
    fetch(`/api/narrative/presets/${activeId}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Could not load story '${activeId}'`);
        return res.json();
      })
      .then((data) => {
        setStory(data);
        setIsLoading(false);
      })
      .catch((err) => {
        console.error("Fetch story error:", err);
        setError(err.message);
        setIsLoading(false);
      });
  }, [story_id, custom]);

  // Keyboard shortcut listener
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Don't trigger if user is in an input or textarea
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;

      if (e.key === 'u' || e.key === 'U' || e.key === 'n' || e.key === 'N') {
        setIsNarratorOpen((prev) => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleSwitchStory = (newId) => {
    router.push({
      pathname: '/stage',
      query: { story_id: newId }
    });
  };

  return (
    <div className="min-h-screen flex flex-col justify-between selection:bg-amber-600 selection:text-white">
      <Head>
        <title>
          {story ? `${story.title} • Digital Butai Stage` : 'Digital Butai • AI Kamishibai'}
        </title>
      </Head>

      {/* STAGE HEADER BAR */}
      <header className="w-full border-b border-amber-900/40 bg-[#120906]/90 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link
              href="/"
              className="p-2 rounded-lg bg-black/40 hover:bg-black/60 border border-amber-900/50 text-amber-300 hover:text-white transition-colors"
              title="Back to Story Studio"
            >
              <ArrowLeft className="w-4 h-4" />
            </Link>

            <div className="w-9 h-9 rounded-xl brass-bracket flex items-center justify-center text-amber-950 font-bold text-lg shadow border border-amber-800">
              舞台
            </div>

            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-serif font-bold text-sm sm:text-base text-amber-100 line-clamp-1">
                  {story ? story.title : 'Loading Kamishibai...'}
                </h1>
                {story?.source_tradition && (
                  <span className="hidden md:inline-block text-[10px] font-sans px-2 py-0.5 rounded bg-amber-950/80 border border-amber-800/60 text-amber-300">
                    {story.source_tradition}
                  </span>
                )}
              </div>
              <p className="text-[11px] text-amber-400/70 font-serif line-clamp-1">
                {story?.title_translations?.[currentLanguage] || story?.title_translations?.hi || ''}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            {/* Story Switcher Dropdown */}
            {storyList.length > 0 && (
              <div className="relative">
                <select
                  value={story?.story_id || ''}
                  onChange={(e) => handleSwitchStory(e.target.value)}
                  className="px-3 py-1.5 bg-[#1e100a] border border-amber-900/60 rounded-lg text-xs font-medium text-amber-200 focus:outline-none focus:border-amber-400 cursor-pointer pr-7 appearance-none"
                >
                  {storyList.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.title}
                    </option>
                  ))}
                </select>
                <ChevronDown className="w-3.5 h-3.5 text-amber-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>
            )}

            {/* Behind the Butai Toggle Button */}
            <button
              onClick={() => setIsNarratorOpen(!isNarratorOpen)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                isNarratorOpen
                  ? 'bg-amber-600 text-white border-amber-400 shadow-md'
                  : 'bg-black/40 border-amber-900/50 text-amber-300 hover:bg-amber-950/50 hover:text-white'
              }`}
              title="Toggle Storyteller's Script & Stage Notes (Shortcut: U)"
            >
              <BookOpen className="w-4 h-4" />
              <span className="hidden sm:inline">Behind the Butai (裏舞台)</span>
            </button>
          </div>
        </div>
      </header>

      {/* MAIN STAGE PLAYSPACE */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 flex flex-col justify-center">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-24 space-y-4">
            <div className="w-12 h-12 rounded-full border-4 border-amber-600 border-t-transparent animate-spin" />
            <p className="text-amber-200 font-serif text-sm">Preparing Digital Butai stage cards...</p>
          </div>
        ) : error ? (
          <div className="max-w-md mx-auto text-center py-16 p-6 rounded-2xl bg-[#1c0f0a] border border-red-900/60 space-y-4">
            <p className="text-red-300 text-sm">{error}</p>
            <button
              onClick={() => handleSwitchStory('monkey-and-crocodile')}
              className="px-4 py-2 rounded-lg bg-amber-700 hover:bg-amber-600 text-white text-xs font-bold"
            >
              Load Flagship Tale
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            
            {/* DIGITAL BUTAI STAGE COMPONENT */}
            <DigitalButai
              story={story}
              currentPanelIndex={currentPanelIndex}
              onPanelChange={setCurrentPanelIndex}
              currentLanguage={currentLanguage}
              onLanguageChange={setCurrentLanguage}
              onToggleNarratorView={() => setIsNarratorOpen(!isNarratorOpen)}
              isNarratorOpen={isNarratorOpen}
            />

            {/* FUSION STYLE & MORAL BANNER */}
            <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Art Fusion Info */}
              <div className="p-4 rounded-xl bg-[#150c07] border border-amber-900/40 flex items-start gap-3">
                <Sparkles className="w-4 h-4 text-amber-400 mt-0.5 flex-shrink-0" />
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-amber-200 uppercase tracking-wider">
                      Fusion Art Matrix:
                    </span>
                    <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-amber-950 border border-amber-800/40 text-amber-300">
                      {story?.indian_style} × {story?.japanese_style}
                    </span>
                  </div>
                  <p className="text-xs text-amber-300/70 font-serif leading-relaxed">
                    {story?.fusion_style_summary}
                  </p>
                </div>
              </div>

              {/* Story Moral / Philosophy */}
              <div className="p-4 rounded-xl bg-[#150c07] border border-amber-900/40 flex items-start gap-3">
                <BookOpen className="w-4 h-4 text-amber-400 mt-0.5 flex-shrink-0" />
                <div className="space-y-1">
                  <span className="text-xs font-bold text-amber-200 uppercase tracking-wider">
                    Core Folkloric Moral (教訓):
                  </span>
                  <p className="text-xs text-amber-200/90 font-serif italic leading-relaxed">
                    "{story?.moral?.[currentLanguage] || story?.moral?.en || ''}"
                  </p>
                </div>
              </div>
            </div>

            {/* NARRATOR PANEL (BEHIND THE BUTAI - URA-BUTAI) */}
            {isNarratorOpen && (
              <div className="max-w-5xl mx-auto pt-2 animate-in fade-in slide-in-from-bottom-4 duration-300">
                <NarratorPanel
                  story={story}
                  currentPanelIndex={currentPanelIndex}
                  currentLanguage={currentLanguage}
                  onClose={() => setIsNarratorOpen(false)}
                />
              </div>
            )}

          </div>
        )}
      </main>

      {/* FOOTER */}
      <footer className="w-full border-t border-amber-900/30 bg-[#0e0705] py-4 text-center text-[11px] text-amber-500/60">
        <p>Press [Space] for Narration • [← / →] for Cards • [U] for Behind the Butai • AI Kamishibai 2026</p>
      </footer>
    </div>
  );
}
