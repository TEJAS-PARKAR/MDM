import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { 
  Sparkles, Play, BookOpen, Layers, Compass, 
  Volume2, Globe, ArrowRight, ShieldCheck, Palette
} from 'lucide-react';
import StoryForm from '../components/StoryForm';

export default function Home() {
  const router = useRouter();

  const handleSelectPreset = (preset) => {
    router.push({
      pathname: '/stage',
      query: { story_id: preset.id }
    });
  };

  const handleStoryGenerated = (storyData) => {
    sessionStorage.setItem('current_custom_story', JSON.stringify(storyData));
    router.push({
      pathname: '/stage',
      query: { story_id: storyData.story_id, custom: 'true' }
    });
  };

  return (
    <div className="min-h-screen flex flex-col justify-between selection:bg-amber-600 selection:text-white">
      <Head>
        <title>AI Kamishibai (紙芝居) • Indo-Japanese Storytelling</title>
      </Head>

      {/* TOP NAVIGATION BAR */}
      <header className="w-full border-b border-amber-900/40 bg-[#120906]/90 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl brass-bracket flex items-center justify-center text-amber-950 font-bold text-xl shadow-lg border border-amber-800">
              🎭
            </div>
            <div>
              <span className="font-serif font-black text-base md:text-lg text-amber-200 tracking-wide">
                AI KAMISHIBAI
              </span>
              <span className="hidden sm:inline-block ml-2 text-[11px] font-sans px-2 py-0.5 rounded-full bg-amber-950/80 border border-amber-800/60 text-amber-400">
                伝統紙芝居 × インド民話
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/stage?story_id=monkey-and-crocodile"
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-500 hover:to-amber-600 text-white text-xs md:text-sm font-semibold shadow-lg shadow-amber-950/60 transition-all border border-amber-400/40"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>Launch Butai Stage</span>
            </Link>
          </div>
        </div>
      </header>

      {/* MAIN HERO & STUDIO SECTION */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-12 flex-1">
        
        {/* HERO TITLE & CULTURAL BADGES */}
        <div className="text-center space-y-4 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-950/60 border border-amber-700/50 text-amber-300 text-xs font-medium backdrop-blur-sm">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>Indo-Japanese Cross-Cultural Generative AI Pipeline</span>
          </div>

          <h1 className="text-3xl sm:text-5xl md:text-6xl font-serif font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-amber-100 via-amber-200 to-amber-400 leading-tight drop-shadow-md">
            Where Indian Folklore Meets Japanese Street Theater
          </h1>

          <p className="text-sm md:text-base text-amber-200/80 font-sans leading-relaxed">
            Adapting ancient Indian tales from the <em>Panchatantra</em> and <em>Jataka Tales</em> into the traditional Japanese 
            <strong> Kamishibai (紙芝居)</strong> picture-card format with authentic 3D wooden theater animation and trilingual neural narration.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
            <span className="px-3 py-1 rounded-lg bg-[#1c100a] border border-amber-800/40 text-xs text-amber-300 flex items-center gap-1.5">
              <span>🇬🇧</span> English Narration
            </span>
            <span className="px-3 py-1 rounded-lg bg-[#1c100a] border border-amber-800/40 text-xs text-amber-300 flex items-center gap-1.5">
              <span>🇮🇳</span> हिन्दी (कथावाचन)
            </span>
            <span className="px-3 py-1 rounded-lg bg-[#1c100a] border border-amber-800/40 text-xs text-amber-300 flex items-center gap-1.5">
              <span>🇯🇵</span> 日本語 (街頭紙芝居)
            </span>
          </div>
        </div>

        {/* QUICK LAUNCH BANNER */}
        <div className="relative overflow-hidden rounded-2xl border-2 border-amber-700/50 bg-gradient-to-r from-[#2a170e] via-[#1a0e08] to-[#2a170e] p-6 md:p-8 shadow-2xl">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
            <div className="space-y-2 text-center md:text-left">
              <span className="text-[11px] font-bold uppercase tracking-widest text-amber-400 bg-amber-950/80 px-2.5 py-1 rounded border border-amber-800/50">
                Featured Flagship Tale
              </span>
              <h2 className="text-xl md:text-2xl font-serif font-bold text-amber-100">
                The Monkey and the Crocodile (बंदर और मगरमच्छ • 猿とワニ)
              </h2>
              <p className="text-xs md:text-sm text-amber-200/80 max-w-xl">
                Experience the classic Panchatantra moral fable synthesized in Madhubani botanical geometry and Edo Ukiyo-e woodblock waves.
              </p>
            </div>
            
            <Link
              href="/stage?story_id=monkey-and-crocodile"
              className="flex-shrink-0 flex items-center gap-3 px-6 py-3.5 rounded-xl brass-bracket text-amber-950 font-bold text-sm tracking-wide shadow-xl hover:scale-105 active:scale-95 transition-all"
            >
              <span>ENTER THE BUTAI STAGE</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* STORY STUDIO / FORM */}
        <div className="pt-4">
          <StoryForm 
            onSelectPreset={handleSelectPreset}
            onStoryGenerated={handleStoryGenerated}
          />
        </div>

        {/* TRADITIONS & STYLES SPOTLIGHT */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6">
          <div className="p-5 rounded-2xl bg-[#170e09] border border-amber-900/50 space-y-3">
            <div className="w-9 h-9 rounded-lg bg-red-950/60 border border-red-800/60 flex items-center justify-center text-red-400">
              <Palette className="w-5 h-5" />
            </div>
            <h3 className="font-serif font-bold text-amber-200 text-base">
              Indo-Japanese Fusion Art
            </h3>
            <p className="text-xs text-amber-300/70 leading-relaxed">
              Synthesizing Madhubani lines, Warli tribal figures, and Pattachitra scrolls with Japanese Ukiyo-e woodcuts, Sumi-e ink wash, and 90s cel anime.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-[#170e09] border border-amber-900/50 space-y-3">
            <div className="w-9 h-9 rounded-lg bg-amber-950/60 border border-amber-800/60 flex items-center justify-center text-amber-400">
              <Compass className="w-5 h-5" />
            </div>
            <h3 className="font-serif font-bold text-amber-200 text-base">
              Digital Butai & Nukikata
            </h3>
            <p className="text-xs text-amber-300/70 leading-relaxed">
              Authentic wooden theater with folding doors, ceremonial Hyoshigi clappers sound, smooth horizontal card sliding, and half-pull suspense cues.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-[#170e09] border border-amber-900/50 space-y-3">
            <div className="w-9 h-9 rounded-lg bg-blue-950/60 border border-blue-800/60 flex items-center justify-center text-blue-400">
              <Volume2 className="w-5 h-5" />
            </div>
            <h3 className="font-serif font-bold text-amber-200 text-base">
              Trilingual Neural TTS
            </h3>
            <p className="text-xs text-amber-300/70 leading-relaxed">
              Real-time trilingual speech synthesis in English, expressive Hindi Katha-vachak cadence, and traditional Japanese Kamishibai storyteller inflection.
            </p>
          </div>
        </div>

      </main>

      {/* FOOTER */}
      <footer className="w-full border-t border-amber-900/40 bg-[#0e0705] py-6 text-center text-xs text-amber-400/60 space-y-1">
        <p>AI Kamishibai • Indo-Japanese Cross-Cultural Storytelling Platform</p>
        <p className="font-serif text-[11px] text-amber-500/50">伝統紙芝居 × パンチャタントラ • 2026</p>
      </footer>
    </div>
  );
}
