import React from 'react';
import { 
  BookOpen, Sparkles, Volume2, Info, Compass, 
  MessageSquare, FileText, ChevronRight, X
} from 'lucide-react';

export default function NarratorPanel({
  story,
  currentPanelIndex,
  currentLanguage,
  onClose
}) {
  const panel = story?.panels?.[currentPanelIndex];

  const playSfx = (sfxName) => {
    try {
      const sfx = new Audio(`/audio/${sfxName}.wav`);
      sfx.volume = 0.8;
      sfx.play().catch(() => {});
    } catch (e) {}
  };

  if (!panel) return null;

  return (
    <div className="w-full bg-[#18110c] border border-amber-900/60 rounded-2xl shadow-2xl overflow-hidden washi-paper">
      
      {/* HEADER: Behind the Butai */}
      <div className="flex items-center justify-between px-5 py-3.5 bg-[#25150e] border-b border-amber-900/60 text-amber-200">
        <div className="flex items-center gap-2.5">
          <BookOpen className="w-5 h-5 text-amber-400" />
          <div>
            <h3 className="font-serif font-bold text-sm tracking-wide flex items-center gap-2">
              <span>BEHIND THE BUTAI (裏舞台 • URA-BUTAI)</span>
              <span className="px-2 py-0.5 rounded bg-amber-950/80 border border-amber-800/60 text-[11px] text-amber-300">
                Card #{panel.panel_id} Back
              </span>
            </h3>
            <p className="text-[11px] text-amber-300/70 font-sans">
              Storyteller's script, physical stage manipulation notes, and cultural annotations
            </p>
          </div>
        </div>

        {onClose && (
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg bg-black/30 hover:bg-black/60 text-amber-400 hover:text-white transition-colors"
            title="Close Narrator View"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      <div className="p-5 space-y-5">
        
        {/* SECTION 1: STAGE DIRECTIONS (ENSHUTSU 演出) */}
        <div className="p-4 rounded-xl bg-amber-900/15 border-2 border-amber-800/50 shadow-inner">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-amber-800 mb-2">
            <Compass className="w-4 h-4 text-amber-700" />
            <span>Stage Direction & Card Manipulation (演出ノート)</span>
          </div>
          <p className="text-sm font-serif italic text-amber-950 leading-relaxed bg-white/70 p-3 rounded-lg border border-amber-200">
            {panel.stage_notes}
          </p>
        </div>

        {/* SECTION 2: INTERACTIVE SOUND EFFECTS SOUNDBOARD */}
        <div className="p-3.5 rounded-xl bg-[#2a1b14] text-amber-100 border border-amber-900/50">
          <div className="flex items-center justify-between mb-2.5">
            <div className="flex items-center gap-2 text-xs font-semibold text-amber-300 uppercase tracking-wider">
              <Volume2 className="w-4 h-4 text-amber-400" />
              <span>Storyteller's Soundboard (効果音)</span>
            </div>
            <span className="text-[11px] text-amber-400/70">Click to trigger live sound effect</span>
          </div>

          <div className="grid grid-cols-3 gap-2.5">
            <button
              onClick={() => playSfx('hyoshigi')}
              className="flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg bg-amber-950/80 hover:bg-amber-900 border border-amber-600/40 text-amber-200 text-xs font-medium transition-transform active:scale-95 shadow"
            >
              <span>🪵</span>
              <span>Hyoshigi (拍子木)</span>
            </button>

            <button
              onClick={() => playSfx('taiko')}
              className="flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg bg-amber-950/80 hover:bg-amber-900 border border-amber-600/40 text-amber-200 text-xs font-medium transition-transform active:scale-95 shadow"
            >
              <span>🥁</span>
              <span>Taiko (太鼓)</span>
            </button>

            <button
              onClick={() => playSfx('paper_slide')}
              className="flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg bg-amber-950/80 hover:bg-amber-900 border border-amber-600/40 text-amber-200 text-xs font-medium transition-transform active:scale-95 shadow"
            >
              <span>📜</span>
              <span>Paper Slide (紙引き)</span>
            </button>
          </div>
        </div>

        {/* SECTION 3: MULTILINGUAL SCRIPT SIDE-BY-SIDE */}
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-amber-900">
            <MessageSquare className="w-4 h-4 text-amber-700" />
            <span>Multilingual Narration Script (三言語台本)</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            
            {/* English Card */}
            <div className={`p-3.5 rounded-xl border transition-all ${
              currentLanguage === 'en'
                ? 'bg-blue-50/90 border-blue-400 shadow-md ring-2 ring-blue-400/30'
                : 'bg-white/60 border-amber-200/80 opacity-80'
            }`}>
              <div className="flex items-center justify-between text-xs font-bold text-blue-900 mb-1.5">
                <span className="flex items-center gap-1.5">
                  <span>🇬🇧</span> English Narration
                </span>
                {currentLanguage === 'en' && (
                  <span className="px-1.5 py-0.5 rounded bg-blue-200 text-[10px] text-blue-900 font-semibold">Active</span>
                )}
              </div>
              <p className="text-xs font-serif text-slate-800 leading-relaxed">
                {panel.dialogue.en}
              </p>
            </div>

            {/* Hindi Card */}
            <div className={`p-3.5 rounded-xl border transition-all ${
              currentLanguage === 'hi'
                ? 'bg-orange-50/90 border-orange-400 shadow-md ring-2 ring-orange-400/30'
                : 'bg-white/60 border-amber-200/80 opacity-80'
            }`}>
              <div className="flex items-center justify-between text-xs font-bold text-orange-900 mb-1.5">
                <span className="flex items-center gap-1.5">
                  <span>🇮🇳</span> हिन्दी (कथावाचन)
                </span>
                {currentLanguage === 'hi' && (
                  <span className="px-1.5 py-0.5 rounded bg-orange-200 text-[10px] text-orange-900 font-semibold">Active</span>
                )}
              </div>
              <p className="text-xs font-serif text-slate-900 leading-relaxed">
                {panel.dialogue.hi}
              </p>
            </div>

            {/* Japanese Card */}
            <div className={`p-3.5 rounded-xl border transition-all ${
              currentLanguage === 'ja'
                ? 'bg-red-50/90 border-red-400 shadow-md ring-2 ring-red-400/30'
                : 'bg-white/60 border-amber-200/80 opacity-80'
            }`}>
              <div className="flex items-center justify-between text-xs font-bold text-red-900 mb-1.5">
                <span className="flex items-center gap-1.5">
                  <span>🇯🇵</span> 日本語 (語り)
                </span>
                {currentLanguage === 'ja' && (
                  <span className="px-1.5 py-0.5 rounded bg-red-200 text-[10px] text-red-900 font-semibold">Active</span>
                )}
              </div>
              <p className="text-xs font-serif text-slate-900 leading-relaxed">
                {panel.dialogue.ja}
              </p>
            </div>
          </div>
        </div>

        {/* SECTION 4: CROSS-CULTURAL BRIDGE & EDUCATIONAL ANNOTATIONS */}
        {panel.cultural_notes && (
          <div className="p-3.5 rounded-xl bg-amber-100/60 border border-amber-300 flex items-start gap-3">
            <Info className="w-5 h-5 text-amber-800 flex-shrink-0 mt-0.5" />
            <div className="text-xs leading-relaxed text-amber-950 font-serif">
              <strong className="font-sans font-bold text-amber-900 block mb-0.5">
                Cross-Cultural Folkloric Bridge (文化の架け橋):
              </strong>
              {panel.cultural_notes}
            </div>
          </div>
        )}

        {/* SECTION 5: VISUAL DIFFUSION PROMPT METADATA */}
        <div className="p-3 rounded-lg bg-black/10 border border-amber-900/20 text-[11px] text-amber-900/80 font-mono">
          <span className="font-bold text-amber-950 font-sans">Diffusion Style Prompt: </span>
          {panel.image_prompt}
        </div>
      </div>
    </div>
  );
}
