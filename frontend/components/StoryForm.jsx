import React, { useState } from 'react';
import { 
  Sparkles, Palette, BookOpen, Layers, Wand2, 
  ArrowRight, CheckCircle2, Loader2, RefreshCw 
} from 'lucide-react';

export default function StoryForm({ onStoryGenerated, onSelectPreset }) {
  const [activeTab, setActiveTab] = useState('preset'); // 'preset' or 'custom'
  
  // Custom Story State
  const [title, setTitle] = useState('');
  const [source, setSource] = useState('Panchatantra');
  const [storyText, setStoryText] = useState('');
  const [indianStyle, setIndianStyle] = useState('madhubani');
  const [japaneseStyle, setJapaneseStyle] = useState('ukiyoe');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationStep, setGenerationStep] = useState('');

  const indianStyles = [
    {
      id: 'madhubani',
      name: 'Madhubani (Mithila)',
      region: 'Bihar, India',
      desc: 'Intricate fine double lines, geometric motifs, and vibrant natural pigments.',
      badgeColor: 'border-red-600/60 bg-red-950/40 text-red-200'
    },
    {
      id: 'warli',
      name: 'Warli Tribal Art',
      region: 'Maharashtra, India',
      desc: 'Rhythmic white-rice geometric stick figures on terracotta red clay.',
      badgeColor: 'border-amber-600/60 bg-amber-950/40 text-amber-200'
    },
    {
      id: 'pattachitra',
      name: 'Pattachitra Scroll',
      region: 'Odisha, India',
      desc: 'Ornate scroll paintings with bold contour lines and mythological borders.',
      badgeColor: 'border-blue-600/60 bg-blue-950/40 text-blue-200'
    }
  ];

  const japaneseStyles = [
    {
      id: 'ukiyoe',
      name: 'Ukiyo-e Woodblock',
      era: 'Edo Period',
      desc: 'Hokusai & Hiroshige woodcut contours, wave foam, and subtle bokashi gradients.',
      badgeColor: 'border-cyan-600/60 bg-cyan-950/40 text-cyan-200'
    },
    {
      id: 'sumie',
      name: 'Sumi-e Ink Wash',
      era: 'Muromachi Period',
      desc: 'Dynamic Zen calligraphy brushwork, splashing haboku ink, and negative space.',
      badgeColor: 'border-slate-500/60 bg-slate-900/60 text-slate-200'
    },
    {
      id: 'anime90s',
      name: '90s Retro Cel Anime',
      era: 'Showa/Heisei Era',
      desc: 'Hand-painted cel shading, 35mm grain, expressive character eyes, and nostalgic warmth.',
      badgeColor: 'border-purple-600/60 bg-purple-950/40 text-purple-200'
    }
  ];

  const presetStories = [
    {
      id: 'monkey-and-crocodile',
      title: 'The Monkey and the Crocodile',
      titleNative: 'बंदर और मगरमच्छ • 猿とワニ',
      tradition: 'Panchatantra (Mitra-bheda)',
      indianStyle: 'madhubani',
      japaneseStyle: 'ukiyoe',
      fusion: 'Madhubani Floral Geometry × Edo Ukiyo-e Woodblock Waves',
      desc: 'A clever monkey outsmarts a treacherous crocodile by claiming his heart is safely stored in a rose-apple tree.',
      moral: 'Presence of mind conquers any betrayal.',
      panels: 8
    },
    {
      id: 'turtle-who-could-not-stop-talking',
      title: "The Turtle Who Couldn't Stop Talking",
      titleNative: 'बातूनी कछुआ • おしゃべりな亀',
      tradition: 'Jataka Tales (Kacchapa Jataka)',
      indianStyle: 'warli',
      japaneseStyle: 'sumie',
      fusion: 'Warli Terracotta Tribal × Zen Sumi-e Ink Wash Skies',
      desc: 'Two loyal geese carry a talkative turtle across the sky on a stick, but mockery from villagers tempts him into fatal speech.',
      moral: 'Silence is the jewel of the wise.',
      panels: 6
    }
  ];

  const handleGenerateCustom = async (e) => {
    e.preventDefault();
    if (!storyText.trim()) return;

    setIsGenerating(true);
    setGenerationStep('Decomposing narrative into Kamishibai theatrical panels...');

    try {
      const response = await fetch('/api/narrative/segment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: title || 'Indian Folk Tale',
          source: source,
          story_text: storyText,
          indian_style: indianStyle,
          japanese_style: japaneseStyle
        })
      });

      if (!response.ok) {
        throw new Error('Failed to segment story');
      }

      setGenerationStep('Synthesizing Indo-Japanese fusion card artwork & multilingual audio...');
      const storyData = await response.json();

      // Trigger batch image & audio pre-synthesis with full story data
      await fetch('/api/image/batch-generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ story_id: storyData.story_id, story_data: storyData })
      }).catch(() => {});

      await fetch('/api/audio/batch-synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ story_id: storyData.story_id, story_data: storyData })
      }).catch(() => {});

      setGenerationStep('Preparing Digital Butai stage...');
      setTimeout(() => {
        setIsGenerating(false);
        if (onStoryGenerated) onStoryGenerated(storyData);
      }, 1000);

    } catch (err) {
      console.error(err);
      setIsGenerating(false);
      alert('Error orchestrating story: ' + err.message);
    }
  };

  const loadSampleStory = () => {
    setTitle('The Loyal Mongoose');
    setSource('Panchatantra');
    setIndianStyle('pattachitra');
    setJapaneseStyle('anime90s');
    setStoryText(
      `In a quiet village lived a farmer and his wife who raised a loyal mongoose like their own child alongside their infant son. One day, while the mother went to draw water from the well, a venomous black cobra crept into the cradle. With courageous fury, the faithful mongoose fought the serpent and tore it to pieces to save the sleeping baby. When the mother returned, she saw the mongoose's mouth drenched in blood. Blinded by hasty grief and suspecting the worst, she hurled a heavy water jar upon the innocent protector. But stepping inside the nursery, she saw the dead cobra beside her laughing, unharmed child. Wailing in agony, she realized that thoughtless haste creates wounds that tears can never heal.`
    );
  };

  return (
    <div className="w-full max-w-4xl mx-auto bg-[#1a0f0a] border border-amber-900/60 rounded-2xl p-6 md:p-8 shadow-2xl">
      
      {/* Header Tabs */}
      <div className="flex items-center justify-between border-b border-amber-900/50 pb-5 mb-6">
        <div>
          <h2 className="text-xl md:text-2xl font-serif font-bold text-amber-200 flex items-center gap-2.5">
            <Palette className="w-6 h-6 text-amber-400" />
            <span>Kamishibai Story Studio (紙芝居スタジオ)</span>
          </h2>
          <p className="text-xs md:text-sm text-amber-300/70 font-sans mt-0.5">
            Choose a canonical Panchatantra tale or input your own Indian folklore for cross-cultural adaptation
          </p>
        </div>

        {/* Tab switch */}
        <div className="flex items-center p-1 bg-black/40 border border-amber-900/40 rounded-xl">
          <button
            onClick={() => setActiveTab('preset')}
            className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'preset'
                ? 'bg-amber-600 text-white shadow-md'
                : 'text-amber-300/70 hover:text-amber-200'
            }`}
          >
            Curated Classics
          </button>
          <button
            onClick={() => setActiveTab('custom')}
            className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'custom'
                ? 'bg-amber-600 text-white shadow-md'
                : 'text-amber-300/70 hover:text-amber-200'
            }`}
          >
            Create Custom Story
          </button>
        </div>
      </div>

      {/* TAB 1: CURATED CLASSICS PRESETS */}
      {activeTab === 'preset' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {presetStories.map((story) => (
            <div
              key={story.id}
              className="p-5 rounded-xl bg-gradient-to-br from-[#24150e] to-[#160c07] border-2 border-amber-900/50 hover:border-amber-500/80 transition-all duration-300 flex flex-col justify-between group shadow-lg"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-semibold text-amber-400/90 tracking-wider uppercase bg-amber-950/80 px-2.5 py-0.5 rounded-full border border-amber-800/50">
                    {story.tradition}
                  </span>
                  <span className="text-xs text-amber-300/70 font-mono">
                    {story.panels} Panels
                  </span>
                </div>

                <h3 className="text-lg font-serif font-bold text-amber-100 group-hover:text-amber-300 transition-colors">
                  {story.title}
                </h3>
                <p className="text-xs text-amber-400/80 font-serif mb-3">
                  {story.titleNative}
                </p>

                <p className="text-xs text-amber-200/80 leading-relaxed mb-4">
                  {story.desc}
                </p>

                {/* Style Fusion Badge */}
                <div className="p-2.5 rounded-lg bg-black/40 border border-amber-900/40 mb-4">
                  <div className="flex items-center gap-1.5 text-[11px] font-semibold text-amber-300 mb-1">
                    <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                    <span>Visual Fusion:</span>
                  </div>
                  <p className="text-[11px] font-serif text-amber-200/90">
                    {story.fusion}
                  </p>
                </div>
              </div>

              <button
                onClick={() => onSelectPreset(story.id)}
                className="w-full mt-2 py-2.5 px-4 rounded-lg bg-amber-700 hover:bg-amber-600 text-white text-xs font-bold tracking-wider uppercase transition-colors shadow-md flex items-center justify-center gap-2 group-hover:shadow-amber-900/50"
              >
                <span>Load in Digital Butai</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* TAB 2: CREATE CUSTOM STORY */}
      {activeTab === 'custom' && (
        <form onSubmit={handleGenerateCustom} className="space-y-6">
          
          {/* Title and Source */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-amber-300 mb-1.5">
                Story Title
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. The Loyal Mongoose"
                required
                className="w-full px-3.5 py-2.5 bg-black/40 border border-amber-900/60 rounded-lg text-sm text-amber-100 placeholder-amber-700 focus:outline-none focus:border-amber-400"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-amber-300 mb-1.5">
                Folklore Tradition / Source
              </label>
              <select
                value={source}
                onChange={(e) => setSource(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-black/40 border border-amber-900/60 rounded-lg text-sm text-amber-100 focus:outline-none focus:border-amber-400"
              >
                <option value="Panchatantra">Panchatantra (Mitra-bheda / Mitra-prapti)</option>
                <option value="Jataka Tales">Jataka Tales (Buddhist Folklore)</option>
                <option value="Hitopadesha">Hitopadesha (Wise Counsel)</option>
                <option value="Indian Regional Folklore">Indian Regional Folklore</option>
              </select>
            </div>
          </div>

          {/* TWO-WAY VISUAL STYLE MATRIX SELECTOR */}
          <div className="space-y-4">
            <label className="block text-xs font-bold text-amber-200 uppercase tracking-wider flex items-center gap-2">
              <Layers className="w-4 h-4 text-amber-400" />
              <span>Indo-Japanese Cross-Cultural Style Synthesis Matrix</span>
            </label>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              
              {/* Indian Folk Style Selection */}
              <div className="p-4 rounded-xl bg-black/30 border border-amber-900/50">
                <span className="text-xs font-bold text-amber-400 block mb-2">
                  1. Indian Folk Art Tradition
                </span>
                <div className="space-y-2">
                  {indianStyles.map((style) => (
                    <label
                      key={style.id}
                      onClick={() => setIndianStyle(style.id)}
                      className={`flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-all ${
                        indianStyle === style.id
                          ? 'border-amber-400 bg-amber-950/60 shadow-md ring-1 ring-amber-400/40'
                          : 'border-amber-900/40 bg-black/20 hover:border-amber-700/60'
                      }`}
                    >
                      <input
                        type="radio"
                        name="indianStyle"
                        checked={indianStyle === style.id}
                        onChange={() => setIndianStyle(style.id)}
                        className="mt-1 accent-amber-500"
                      />
                      <div>
                        <div className="flex items-center gap-2">
                          <strong className="text-xs text-amber-100 font-semibold">{style.name}</strong>
                          <span className="text-[10px] text-amber-400/70">({style.region})</span>
                        </div>
                        <p className="text-[11px] text-amber-300/70 mt-0.5 leading-snug">{style.desc}</p>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              {/* Japanese Traditional Style Selection */}
              <div className="p-4 rounded-xl bg-black/30 border border-amber-900/50">
                <span className="text-xs font-bold text-amber-400 block mb-2">
                  2. Japanese Traditional Art Tradition
                </span>
                <div className="space-y-2">
                  {japaneseStyles.map((style) => (
                    <label
                      key={style.id}
                      onClick={() => setJapaneseStyle(style.id)}
                      className={`flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-all ${
                        japaneseStyle === style.id
                          ? 'border-amber-400 bg-amber-950/60 shadow-md ring-1 ring-amber-400/40'
                          : 'border-amber-900/40 bg-black/20 hover:border-amber-700/60'
                      }`}
                    >
                      <input
                        type="radio"
                        name="japaneseStyle"
                        checked={japaneseStyle === style.id}
                        onChange={() => setJapaneseStyle(style.id)}
                        className="mt-1 accent-amber-500"
                      />
                      <div>
                        <div className="flex items-center gap-2">
                          <strong className="text-xs text-amber-100 font-semibold">{style.name}</strong>
                          <span className="text-[10px] text-amber-400/70">({style.era})</span>
                        </div>
                        <p className="text-[11px] text-amber-300/70 mt-0.5 leading-snug">{style.desc}</p>
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            {/* LIVE FUSION BADGE PREVIEW */}
            <div className="p-3 rounded-xl bg-amber-950/40 border border-amber-600/40 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-400" />
                <span className="text-xs text-amber-300">Active Blend:</span>
                <span className="text-xs font-serif font-bold text-amber-100">
                  {indianStyles.find(s => s.id === indianStyle)?.name} × {japaneseStyles.find(s => s.id === japaneseStyle)?.name}
                </span>
              </div>
              <span className="text-[11px] text-amber-400/80 font-mono">1024×768 Kamishibai Ratio</span>
            </div>
          </div>

          {/* Story Textarea */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-semibold text-amber-300">
                Story Text (Indian Folk Narrative)
              </label>
              <button
                type="button"
                onClick={loadSampleStory}
                className="text-[11px] text-amber-400 hover:text-amber-200 underline flex items-center gap-1"
              >
                <RefreshCw className="w-3 h-3" />
                Load Sample Story (The Loyal Mongoose)
              </button>
            </div>
            <textarea
              rows={5}
              value={storyText}
              onChange={(e) => setStoryText(e.target.value)}
              placeholder="Paste raw narrative of the Indian story here..."
              required
              className="w-full p-3.5 bg-black/40 border border-amber-900/60 rounded-xl text-xs md:text-sm text-amber-100 placeholder-amber-700/80 focus:outline-none focus:border-amber-400 leading-relaxed font-serif"
            />
          </div>

          {/* Submit Button */}
          <div className="pt-2">
            <button
              type="submit"
              disabled={isGenerating || !storyText.trim()}
              className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-500 hover:to-amber-600 text-white font-bold text-sm tracking-wider uppercase transition-all shadow-xl shadow-amber-950/80 disabled:opacity-50 disabled:pointer-events-none flex items-center justify-center gap-2.5 border border-amber-400/50"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>{generationStep}</span>
                </>
              ) : (
                <>
                  <Wand2 className="w-5 h-5" />
                  <span>Transform into Kamishibai Theatrical Panels</span>
                </>
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
