import json
import re
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from app.core.config import settings
from app.core.prompts import SYSTEM_NARRATIVE_SEGMENTER, USER_SEGMENTATION_PROMPT, FUSION_PROMPT_TEMPLATE

# --- Pydantic Data Models ---

class Character(BaseModel):
    name: str = Field(description="Name of the character")
    visual_features: str = Field(description="Physical and stylistic appearance details")
    pose: str = Field(description="Character bodily posture or physical stance")
    expression: str = Field(description="Facial expression and emotional state")

class Dialogue(BaseModel):
    en: str = Field(description="English narration or character dialogue")
    hi: str = Field(description="Hindi narration or character dialogue (Devanagari)")
    ja: str = Field(description="Japanese narration or character dialogue (Kanji/Kana)")

class Panel(BaseModel):
    panel_id: int = Field(description="Panel sequence number 1 to N")
    scene_description: str = Field(description="Visual description of scene setting and action")
    characters: List[Character] = Field(default_factory=list, description="Characters visible in this panel")
    dialogue: Dialogue = Field(description="Trilingual narration/dialogue for this card")
    stage_notes: str = Field(description="Kamishibai physical stage directions (slide speed, sound effects, pauses)")
    image_prompt: str = Field(description="Optimized diffusion prompt blending styles")
    camera_angle: str = Field(description="Camera angle and perspective")
    cultural_notes: Optional[str] = Field(default=None, description="Folkloric and cross-cultural notes")

class KamishibaiStory(BaseModel):
    story_id: str
    title: str
    title_translations: Dict[str, str]
    source_tradition: str
    indian_style: str
    japanese_style: str
    fusion_style_summary: str
    moral: Dict[str, str]
    panels: List[Panel]

# --- Curated Canonical Panchatantra & Jataka Presets ---

PRESET_STORIES: Dict[str, KamishibaiStory] = {
    "monkey-and-crocodile": KamishibaiStory(
        story_id="monkey-and-crocodile",
        title="The Monkey and the Crocodile",
        title_translations={
            "en": "The Monkey and the Crocodile",
            "hi": "बंदर और मगरमच्छ",
            "ja": "猿とワニの知恵比べ"
        },
        source_tradition="Panchatantra (Mitra-bheda)",
        indian_style="madhubani",
        japanese_style="ukiyoe",
        fusion_style_summary="Intricate Madhubani botanical geometry merged with Edo-period Ukiyo-e woodblock ocean waves and bokashi atmospheric gradients.",
        moral={
            "en": "Presence of mind in moments of peril can conquer any treachery.",
            "hi": "संकट के समय बुद्धि और धैर्य से किसी भी विश्वासघात को जीता जा सकता है।",
            "ja": "危急の時こそ、機知と冷静さが最大の武器となる。"
        },
        panels=[
            Panel(
                panel_id=1,
                scene_description="On the lush sunlit banks of the sacred river Narmada, a clever monkey named Raktamukha perches happily upon a towering Jamun (rose apple) tree laden with deep violet berries.",
                characters=[
                    Character(
                        name="Raktamukha (Monkey)",
                        visual_features="Golden-brown fur adorned with fine Madhubani floral spirals, alert expressive eyes",
                        pose="Perched gracefully on a thick blooming Jamun branch, holding a ripe purple fruit",
                        expression="Warm, radiant, inviting smile"
                    )
                ],
                dialogue=Dialogue(
                    en="Long ago, on the flowering banks of the great river, lived Raktamukha, a monkey of quick wit who feasted daily upon luscious purple rose-apples.",
                    hi="बहुत पुरानी बात है, नर्मदा नदी के सुरम्य तट पर जामुन के एक विशाल वृक्ष पर 'रक्तमुख' नाम का एक बुद्धिमान वानर रहता था।",
                    ja="むかしむかし、大きな川のほとりに、知恵に満ちた猿のラクタームカが、甘い紫の果実を実らせる大木に暮らしていました。"
                ),
                stage_notes="[Sound: Hyoshigi clappers - Chon-chon! Slowly slide card 1 into the Butai frame. Voice: Joyous, gentle cadence.]",
                image_prompt="Masterpiece Kamishibai card. Golden monkey sitting upon a lush blooming Jamun tree with rich purple berries over a flowing river. Madhubani intricate double lines and sacred geometric leaves fused with Edo period Ukiyo-e woodcut waves, delicate washi paper texture, warm sunlight.",
                camera_angle="Wide establishing shot with decorative Indian-Japanese floral border",
                cultural_notes="Panchatantra Book 4: The Jamun tree symbolizes prosperity and natural abundance; the monkey represents pure *buddhi* (intellect)."
            ),
            Panel(
                panel_id=2,
                scene_description="A weary crocodile named Karalamukha crawls out of the glistening water to rest under the shade. The monkey plucks sweetest berries and tosses them down with warm hospitality.",
                characters=[
                    Character(
                        name="Raktamukha (Monkey)",
                        visual_features="Agile, gesturing with open hand from the branches",
                        pose="Leaning down from branch offering glistening fruit",
                        expression="Benevolent and generous"
                    ),
                    Character(
                        name="Karalamukha (Crocodile)",
                        visual_features="Emerald armored scales etched with Ukiyo-e water contours, ancient wisdom in eyes",
                        pose="Basking half-emerged on the sandy riverbank",
                        expression="Delighted and humbled"
                    )
                ],
                dialogue=Dialogue(
                    en="One hot afternoon, Karalamukha the crocodile rested beneath the canopy. The generous monkey dropped sweetest fruits, sparking an enduring brotherhood between water and earth.",
                    hi="एक दिन करालमुख नाम का मगरमच्छ छाया में विश्राम करने आया। दयालु वानर ने अमृत जैसे मीठे जामुन नीचे गिराए, और दोनों में गहरी मित्रता हो गई।",
                    ja="ある暑い日、ワニのカララムカが木陰に休みに来ました。優しい猿は甘い果実を落としてやり、水と陸の深い友情が結ばれたのです。"
                ),
                stage_notes="[Keep card steady. Performer speaks in warm conversational tones, gesturing outward.]",
                image_prompt="Kamishibai painting. Monkey tossing purple berries down to an emerald crocodile resting on a riverbank. Madhubani fine lines and fish motifs combined with Hokusai-style woodblock river currents and bokashi gradient sands, peaceful afternoon glow.",
                camera_angle="Medium eye-level shot capturing the bond between branch and water",
                cultural_notes="In Indian ethics (*Athiti Devo Bhava*), offering food to a stranger establishes sacred guest-friendship."
            ),
            Panel(
                panel_id=3,
                scene_description="Karalamukha returns to his underwater cave carrying rose-apples to his wife. She tastes the nectar-sweet fruit, but a dark covetous gleam appears in her cold serpent-like eyes.",
                characters=[
                    Character(
                        name="Crocodile's Wife",
                        visual_features="Sinuous jagged scales, dark indigo and silver hues with Kabuki-style dark eye markings",
                        pose="Coiled menacingly on underwater river stones",
                        expression="Greedy, manipulative, calculating sneer"
                    ),
                    Character(
                        name="Karalamukha (Crocodile)",
                        visual_features="Submissive posture, holding fruit delicately",
                        pose="Swimming anxiously beside his mate",
                        expression="Conflicted and uneasy"
                    )
                ],
                dialogue=Dialogue(
                    en="When the crocodile's wife tasted the divine nectar, dark greed gripped her heart. 'If the fruits are so sweet,' she hissed, 'imagine how delicious the monkey's heart must be! Bring him to me, or I shall starve!'",
                    hi="जब मगरमच्छ की पत्नी ने वे मीठे जामुन चखे, तो उसके मन में दुष्ट लोभ जाग उठा—'जो रोज़ ऐसे फल खाता है, उसका हृदय कितना मीठा होगा! मुझे उसका हृदय चाहिए!'",
                    ja="その甘美な果実を味わったワニの妻の心に、邪悪な欲望が芽生えました。「これほど美味い実を食す猿の心臓は、さぞ甘かろう。連れてこなければ私は死にます！」"
                ),
                stage_notes="[Sound: Low sinister taiko drum roll - Dronnn... Narrator drops voice to a raspy, theatrical whisper.]",
                image_prompt="Kamishibai dramatic card. Dark underwater cavern illuminated by moonlight. Menacing female crocodile with sharp teeth and greedy glowing eyes whispering to uneasy husband. Madhubani decorative aquatic motifs blended with dark Ukiyo-e ghost print aesthetic, eerie bioluminescent water.",
                camera_angle="Low-angle close-up emphasizing the wife's menacing silhouette",
                cultural_notes="Traditional archetype of the deceptive temptation leading to betrayal of *Mitra-dharma* (duty of friendship)."
            ),
            Panel(
                panel_id=4,
                scene_description="Karalamukha returns with a heavy heart, offering the monkey a ride on his back across the river, claiming his family invites him for a grand royal feast.",
                characters=[
                    Character(
                        name="Raktamukha (Monkey)",
                        visual_features="Vibrant golden, innocent, trusting",
                        pose="Perched courageously upon the crocodile's broad textured back in mid-river",
                        expression="Excited, trusting, joyful"
                    ),
                    Character(
                        name="Karalamukha (Crocodile)",
                        visual_features="Half-submerged in churning foam, solemn eyes",
                        pose="Swimming through deep river currents",
                        expression="Burdened with sorrow and guilt"
                    )
                ],
                dialogue=Dialogue(
                    en="'My dear friend,' lied the heavy-hearted crocodile, 'my wife invites you for a splendid feast! Climb upon my back; I shall ferry you safely.' Trusting his companion, the monkey leaped aboard.",
                    hi="'मित्र!' मगरमच्छ ने भारी मन से झूठ कहा, 'मेरी पत्नी ने तुम्हें दावत पर बुलाया है। मेरी पीठ पर बैठो, मैं तुम्हें पार ले चलूंगा।' वानर ने निश्छल विश्वास से छलांग लगा दी।",
                    ja="「友よ、妻が君をご馳走に招きたいと言っている。背中に乗りなさい」重い嘘をつくワニ。猿は疑うことなく、その広い背に飛び乗りました。"
                ),
                stage_notes="[Slowly slide card 3 out, revealing card 4 moving like a boat floating across waves. Voice is gentle yet carries foreboding undertone.]",
                image_prompt="Theatrical Kamishibai card. Golden monkey riding on the back of an emerald crocodile in the middle of a swirling sacred river. Madhubani geometric water ripples fused with Great Wave of Kanagawa woodblock foam, dramatic mid-stream tension.",
                camera_angle="Dynamic side-tracking angle across rushing water",
                cultural_notes="The peril of venturing into unfamiliar elements where one's natural agility is rendered vulnerable."
            ),
            Panel(
                panel_id=5,
                scene_description="In the deepest, darkest whirlpool of the river, Karalamukha begins to sink. Guilt-ridden, he confesses the terrible truth: his wife demands the monkey's heart.",
                characters=[
                    Character(
                        name="Karalamukha (Crocodile)",
                        visual_features="Jaws parted slightly in confession, water splashing around nostrils",
                        pose="Dipping downward into swirling dark depths",
                        expression="Tormented, sorrowful"
                    ),
                    Character(
                        name="Raktamukha (Monkey)",
                        visual_features="Clinging desperately to spiky crest, mind racing",
                        pose="Balancing precariously amidst crashing waves",
                        expression="Instant shock transformed into sharp, intense cunning"
                    )
                ],
                dialogue=Dialogue(
                    en="In deep water, the crocodile began to sink. 'Forgive me, brother,' he groaned. 'My wife craves your sweet heart!' A chill struck the monkey, yet his brilliant mind remained razor sharp.",
                    hi="गहरे भंवर में मगरमच्छ डूबने लगा—'मुझे क्षमा करना मित्र, मेरी पत्नी तुम्हारा हृदय खाना चाहती है!' वानर का कलेजा कांप उठा, किंतु उसकी बुद्धि बिजली की तरह चमकी।",
                    ja="深みに入り、ワニは沈み始めました。「許せ友よ…妻がお前の心臓を食べたがっているのだ！」凍りつく猿。しかしその瞳に、研ぎ澄まされた知恵の光が宿ります。"
                ),
                stage_notes="[Perform Nukikata: abruptly pull card halfway! Hold it frozen for 2 seconds. Sound: Sudden Hyoshigi CLACK! Voice: Sudden gasp, then calm resolve.]",
                image_prompt="Kamishibai climax card. Monkey clinging to sinking crocodile in a dramatic swirling whirlpool. Ukiyo-e vortex waves and swirling foam with Madhubani intricate cosmic spiral patterns, intense lightning-like splash, suspenseful atmosphere.",
                camera_angle="High dramatic overhead angle plunging into the swirling whirlpool",
                cultural_notes="The turning point (*Ten* in Ki-shō-ten-ketsu). Ancient Indian strategic wisdom: Never panic when cornered; strike with psychological illusion."
            ),
            Panel(
                panel_id=6,
                scene_description="With a calm, laughing composure, the monkey laughs aloud at the crocodile's silly mistake, explaining that monkeys keep their hearts safely hanging in the hollow of the Jamun tree.",
                characters=[
                    Character(
                        name="Raktamukha (Monkey)",
                        visual_features="Chest puffed out, gesturing gracefully toward the distant riverbank",
                        pose="Standing upright on crocodile's head without fear",
                        expression="Charming, amused, theatrical laughter"
                    ),
                    Character(
                        name="Karalamukha (Crocodile)",
                        visual_features="Wide foolish eyes, gullible expression",
                        pose="Halting in mid-swim, turning head awkwardly",
                        expression="Astonished, naive, bewildered"
                    )
                ],
                dialogue=Dialogue(
                    en="'Oh foolish brother!' laughed the monkey warmly. 'Why didn't you say so earlier? We monkeys keep our hearts safely hanging in the hollow of our tree! Turn around at once, and I will gladly fetch it for your queen!'",
                    hi="'अरे मूर्ख मित्र!' वानर खिलखिलाकर हंसा, 'यह पहले क्यों नहीं बताया? हम वानर तो अपना हृदय जामुन के खोखल में सुरक्षित रखते हैं! तुरंत वापस चलो, मैं सहर्ष ले आता हूँ!'",
                    ja="「なーんだ、そんなことか！」猿はからからと笑いました。「私たち猿は、心臓を木の洞に干してあるんだよ！早く戻ろう、奥方のために取ってきてあげるから！」"
                ),
                stage_notes="[Fully slide the card into place. Performer adopts a broad theatrical laugh: 'Ha-ha-ha!' Audience chuckles.]",
                image_prompt="Kamishibai card. Clever monkey laughing confidently atop crocodile's snout, pointing back to the glowing distant riverbank. Madhubani radiant sunburst pattern and Ukiyo-e expressive Kabuki-style comedic faces, whimsical and vibrant.",
                camera_angle="Dynamic two-shot with comedic contrast between cunning monkey and dumbfounded crocodile",
                cultural_notes="The trope of 'the detachable organ' is a famous motif in Buddhist Jatakas and Japanese folklore (*Saru no Iki-gimo* / The Monkey's Liver)."
            ),
            Panel(
                panel_id=7,
                scene_description="The gullible crocodile races back to shore. The instant they touch the bank, the monkey vaults like a lightning bolt into the highest branch, safe among the sweet fruit.",
                characters=[
                    Character(
                        name="Raktamukha (Monkey)",
                        visual_features="Dynamic motion blur, triumphantly holding a branch high in the sky",
                        pose="Perched safely high above, pointing mockingly downward",
                        expression="Victorious, mocking, enlightened"
                    ),
                    Character(
                        name="Karalamukha (Crocodile)",
                        visual_features="Stranded on the mud bank looking up foolishly",
                        pose="Jaws open in disbelief, tail sluggish in the mud",
                        expression="Utter shame and defeat"
                    )
                ],
                dialogue=Dialogue(
                    en="The gullible beast paddled furiously back. The moment scales grazed the sand, Raktamukha leaped to safety high in the branches! 'O traitor,' he declared, 'can any creature live without its heart? Go tell your greedy wife that wit has defeated hunger!'",
                    hi="मूर्ख मगरमच्छ तेज़ी से तट की ओर लौटा। किनारा आते ही वानर ने बिजली की फुर्ती से पेड़ पर छलांग लगा दी! 'अरे विश्वासघाती! क्या कोई हृदय के बिना जीवित रह सकता है? तुम्हारी धूर्तता पर मेरी बुद्धि की विजय हुई!'",
                    ja="愚かなワニは全速力で岸へ戻りました。浅瀬に着いた瞬間、猿は電光石火の如く枝へと飛び移りました！「裏切り者め！心臓のない生き物がどこにいる！お前の悪巧みは知恵に敗れたのだ！」"
                ),
                stage_notes="[Sound: Fast card slide with swoosh sound! Performer's voice resonates with triumphant moral authority.]",
                image_prompt="Triumphant Kamishibai climax. Golden monkey perched victorious high in a magnificent blooming tree, laughing at a sullen green crocodile stranded below. Vibrant Madhubani peacock motifs in the branches with dramatic Ukiyo-e sunburst and rushing river waves, glorious victory.",
                camera_angle="Dramatic high-to-low vertical perspective showing safety above and stranded predator below",
                cultural_notes="The triumph of *Yukti* (cunning intellect) over *Bala* (brute force), fulfilling the primary mandate of the Panchatantra."
            ),
            Panel(
                panel_id=8,
                scene_description="Sunset bathes the river in gold and vermilion. The monkey sits serenely enjoying fruit while the ashamed crocodile sinks into the dark depths alone.",
                characters=[
                    Character(
                        name="Raktamukha (Monkey)",
                        visual_features="Halo-like golden aura, peaceful silhouette",
                        pose="Meditative pose on tree bough against setting sun",
                        expression="Peaceful, wise, contemplative"
                    )
                ],
                dialogue=Dialogue(
                    en="And so, trust broken can never be mended, but wisdom and courage will guide the righteous through the darkest waters. Thus ends our Kamishibai tale.",
                    hi="और इस प्रकार, टूटा हुआ विश्वास कभी नहीं जुड़ता, किंतु साहस और विवेक हर संकट से उबार लेते हैं। यही इस कथा की सीख है।",
                    ja="一度壊れた信頼は二度と戻りません。しかし機知と勇気は、如何なる荒波をも渡る光となるのです。これにて、紙芝居のおしまい。"
                ),
                stage_notes="[Sound: Final ceremonial Hyoshigi clappers: Chon... Chon... Chon! Performer gently bows. Close Butai doors slowly.]",
                image_prompt="Kamishibai closing card. Spectacular sunset over the river Narmada with vermilion and indigo skies. Madhubani sacred lotus flower motifs framing the scene with Japanese Sumi-e silhouetted tree branches and gold leaf washi texture, contemplative and tranquil.",
                camera_angle="Wide scenic sunset panorama with traditional calligraphy seal stamp",
                cultural_notes="The Sanskrit moral: 'उपायेन हि यच्छक्यं न तच्छक्यं पराक्रमैः' (What can be achieved by stratagem cannot be achieved by mere force)."
            )
        ]
    ),
    "turtle-who-could-not-stop-talking": KamishibaiStory(
        story_id="turtle-who-could-not-stop-talking",
        title="The Turtle Who Couldn't Stop Talking",
        title_translations={
            "en": "The Turtle Who Couldn't Stop Talking",
            "hi": "बातूनी कछुआ",
            "ja": "おしゃべりな亀 (ジャータカ物語)"
        },
        source_tradition="Jataka Tales (Kacchapa Jataka)",
        indian_style="warli",
        japanese_style="sumie",
        fusion_style_summary="Minimalist Warli white rice geometric stick figures on terracotta earth harmonized with fluid Sumi-e ink wash skies and zen negative space.",
        moral={
            "en": "A word spoken out of season brings destruction; silence is the jewel of the wise.",
            "hi": "असमय बोला गया शब्द विनाश लाता है; मौन ही बुद्धिमानों का आभूषण है।",
            "ja": "時ならぬ口数は身を滅ぼす。沈黙こそ智者の宝である。"
        },
        panels=[
            Panel(
                panel_id=1,
                scene_description="In a peaceful lake surrounded by ancient hills, a talkative turtle named Kambugriva lives in joyful friendship with two graceful wild geese, Sankha and Vikata.",
                characters=[
                    Character(
                        name="Kambugriva (Turtle)",
                        visual_features="Warli geometric shell with radiating white concentric rings",
                        pose="Swimming happily with head poked out of the pond",
                        expression="Chatty, smiling, eyes wide open"
                    ),
                    Character(
                        name="Two Geese",
                        visual_features="Fluid Sumi-e brushstroke white wings, elegant curved necks",
                        pose="Gliding side-by-side above water",
                        expression="Serene and loyal"
                    )
                ],
                dialogue=Dialogue(
                    en="Deep in the Himalayas, in a lotus-covered lake, lived Kambugriva the turtle and his dearest companions, two noble wild geese. The turtle had a heart of gold, but could never cease his endless chatter.",
                    hi="हिमालय की तलहटी में एक सुंदर सरोवर में कम्बुग्रीव नाम का कछुआ अपने दो हंस मित्रों के साथ रहता था। कछुआ बहुत स्नेही था, पर अपनी बातूनी आदत पर उसका कोई नियंत्रण न था।",
                    ja="昔、蓮の花咲く湖に、おしゃべり好きな亀と二羽の気品ある白鳥が仲良く暮らしていました。亀は心優しかったものの、口を開けば止まりませんでした。"
                ),
                stage_notes="[Sound: Soft wind chime. Slide card 1 smoothly into Butai frame. Voice: Melodic and steady.]",
                image_prompt="Warli and Sumi-e fusion Kamishibai art. Terracotta background with white rice pigment Warli geometric turtle swimming in a lotus pond, two graceful Japanese Sumi-e ink wash geese flying overhead, Zen minimalist balance.",
                camera_angle="Wide scenic view of serene mountain pond",
                cultural_notes="From Jataka Tale No. 215, traditionally used by the Bodhisattva to teach restraint in speech."
            ),
            Panel(
                panel_id=2,
                scene_description="A harsh summer drought dries the lake into cracked terracotta clay. The fish perish, and the three friends must find a way to escape to the distant lake of Manasarovar.",
                characters=[
                    Character(
                        name="Kambugriva (Turtle)",
                        visual_features="Parched mud texture on shell",
                        pose="Struggling upon cracked earth",
                        expression="Despondent, anxious"
                    ),
                    Character(
                        name="Geese",
                        visual_features="Spread wings shielding friend from blazing sun",
                        pose="Hovering protectively",
                        expression="Deep concern and deliberation"
                    )
                ],
                dialogue=Dialogue(
                    en="A fierce drought struck the land; the waters vanished into parched cracked clay. To save their dear friend from perishing, the two geese devised an ingenious plan to carry him across the skies.",
                    hi="भीषण सूखा पड़ा और सरोवर सूखकर दरार भरी मिट्टी में बदल गया। अपने मित्र के प्राण बचाने के लिए दोनों हंसों ने उसे आकाश मार्ग से दूर मानसरोवर ले जाने की अद्भुत युक्ति सोची।",
                    ja="激しい日照りが湖を干上がらせました。友を救うため、白鳥たちは一本の木の棒を使い、亀を空へと運ぶ奇想天外な策を思いつきました。"
                ),
                stage_notes="[Sound: Low hum like heat waves. Narrator adopts a sorrowful yet determined tone.]",
                image_prompt="Kamishibai painting. Cracked terracotta dry earth in Warli style with parched mud cracks, combined with fiery Sumi-e brushstrokes of blazing sun, two white ink birds consulting a stylized turtle.",
                camera_angle="Low-angle view emphasizing parched desert-like terrain",
                cultural_notes="Depiction of seasonal droughts in Indian literature symbolizing existential crises needing solidarity."
            ),
            Panel(
                panel_id=3,
                scene_description="The geese hold a sturdy wooden stick between their beaks, while the turtle clamps his jaws firmly onto the center. The geese give a stern warning: 'Keep your mouth shut, no matter what!'",
                characters=[
                    Character(
                        name="Kambugriva (Turtle)",
                        visual_features="Jaws clamped tight on center of wooden staff",
                        pose="Suspended between the two birds",
                        expression="Nodding vigorously with clenched jaw"
                    ),
                    Character(
                        name="Two Geese",
                        visual_features="Firm beaks holding the two ends of the staff",
                        pose="Flapping powerful wings preparing for lift-off",
                        expression="Stern and focused"
                    )
                ],
                dialogue=Dialogue(
                    en="'Bite the center of this stick with all your might,' warned the geese solemnly. 'If you utter even a single syllable, you will fall to your doom!' The turtle nodded, sealing his lips tight.",
                    hi="'इस लकड़ी को अपने दांतों से कसकर पकड़ लो,' हंसों ने कड़ी चेतावनी दी। 'यदि तुमने एक भी शब्द बोलने के लिए मुंह खोला, तो गिरकर तुम्हारी मृत्यु निश्चित है!' कछुए ने दृढ़ता से सिर हिलाया।",
                    ja="「この木の棒の真ん中を強く噛むのだ」白鳥は厳しく戒めました。「空を飛んでいる間、決して口を開いてはならぬぞ！」亀は固く誓いました。"
                ),
                stage_notes="[Sound: Wooden clapper click - Chon! Voice: Stern, emphatic, dramatic warning.]",
                image_prompt="Kamishibai card. Minimalist Warli stick figures and Sumi-e dynamic brushwork. Turtle biting a wooden stick held by two soaring geese, lifting above hills into a pale ink wash sky.",
                camera_angle="Eye-level dynamic side view of departure",
                cultural_notes="The stick symbolizes the vow of silence (*Mouna Vrata*), an ancient Indian ascetic discipline."
            ),
            Panel(
                panel_id=4,
                scene_description="They soar majestic across the clouds over towns and villages. People below gather, pointing and laughing at the ridiculous spectacle of a flying turtle.",
                characters=[
                    Character(
                        name="Villagers below",
                        visual_features="Warli geometric stick figures in festive circle formation",
                        pose="Pointing fingers upward, clapping and shouting",
                        expression="Mocking and astonished"
                    ),
                    Character(
                        name="Kambugriva (Turtle)",
                        visual_features="Eyes bulging with rising indignation",
                        pose="Gliding high in sky, neck swelling with anger",
                        expression="Infuriated, bursting to retort"
                    )
                ],
                dialogue=Dialogue(
                    en="Up into the azure heavens they soared! But as they passed over a crowded village, people gathered pointing and shouting: 'Look! What an absurd sight—two birds carrying a round foolish creature!'",
                    hi="वे बादलों के पार उड़े! किंतु जैसे ही एक नगर के ऊपर से गुज़रे, लोग नीचे जमा होकर उपहास करने लगे: 'देखो-देखो! क्या हास्यास्पद दृश्य है—दो पक्षी एक मूर्ख कछुए को ढो रहे हैं!'",
                    ja="やがて町の上空を飛ぶと、地上の人々が指をさして騒ぎ始めました。「見ろ見ろ！鳥が滑稽な亀をぶら下げて飛んでいるぞ！なんたる見世物だ！」"
                ),
                stage_notes="[Sound: Hubbub of murmuring voices. Narrator mimics the chattering crowd below, then turns to the turtle's swelling anger.]",
                image_prompt="Warli tribal village below with rhythmic stick figures pointing up at a flying turtle held by two majestic Sumi-e geese against vast open sky, dramatic height and contrast.",
                camera_angle="High bird's-eye view looking down from the heavens to the tiny villagers below",
                cultural_notes="The crowd represents public opinion and mockery, the ultimate test of human ego and equanimity."
            ),
            Panel(
                panel_id=5,
                scene_description="Unable to endure the mockery, Kambugriva loses his temper. He opens his mouth to shout an insult, instantly losing his grip and tumbling from the sky.",
                characters=[
                    Character(
                        name="Kambugriva (Turtle)",
                        visual_features="Mouth wide open screaming, tumbling upside down through empty space",
                        pose="Spinning downwards with limbs flailing",
                        expression="Horror and immediate regret"
                    ),
                    Character(
                        name="Two Geese",
                        visual_features="Looking down in sorrow with wings outstretched",
                        pose="Holding empty stick aloft in clear sky",
                        expression="Heartbroken despair"
                    )
                ],
                dialogue=Dialogue(
                    en="Blinded by wounded pride, the turtle could bear it no longer. 'Eat your own dust!' he bellowed—and in that fateful instant, his jaws slipped, and he plummeted toward the earth.",
                    hi="अपमान से तिलमिलाकर कछुआ अपना धैर्य खो बैठा। 'मेरी धूल चाटो!' जैसे ही उसने चिल्लाने के लिए मुंह खोला, लकड़ी छूट गई और वह तीव्र गति से नीचे गिर पड़ा।",
                    ja="自尊心を傷つけられた亀は、我慢の限界を超えて叫びました。「お前たちこそ泥でも食え！」——その刹那、口から棒が離れ、亀は真っ逆さまに落下していきました。"
                ),
                stage_notes="[Sound: Sudden rapid card pull halfway down! Sound: Piercing shriek followed by Taiko thud - DON! Voice: Sudden crescendo to gasp.]",
                image_prompt="Dramatic Kamishibai card. Spinning Warli-patterned turtle tumbling down through vertical Sumi-e ink streaks, two geese holding empty stick in high empty sky, sense of terrifying freefall.",
                camera_angle="Dynamic steep vertical perspective capturing dizzying downward plunge",
                cultural_notes="The classic tragic flaw of *Krodha* (uncontrolled wrath) annihilating years of friendship and safety."
            ),
            Panel(
                panel_id=6,
                scene_description="The two geese circle the quiet mountainside in silent mourning, while the narrator reflects on the eternal lesson of guarded speech.",
                characters=[
                    Character(
                        name="Two Geese",
                        visual_features="Silhouetted against mountain peaks",
                        pose="Soaring away into the misty horizon",
                        expression="Solemn and sorrowful"
                    )
                ],
                dialogue=Dialogue(
                    en="He who cannot control his tongue, even when saved by loyal friends, brings about his own undoing. Remember this lesson of the turtle, and let your words be few and wise.",
                    hi="जो व्यक्ति सच्चे मित्रों की हितकारी सलाह पर भी अपनी वाणी पर नियंत्रण नहीं रख पाता, वह स्वयं अपना विनाश कर बैठता है। मौन ही सबसे बड़ा विवेक है।",
                    ja="忠告を聞き入れず、舌を制御できぬ者は、自ら身を滅ぼす。言葉は慎み深く、心には静寂を。これにて、紙芝居のおしまい。"
                ),
                stage_notes="[Sound: Final gentle Hyoshigi clappers: Chon... Chon. The storyteller bows quietly.]",
                image_prompt="Kamishibai closing card. Two majestic white geese disappearing into misty Sumi-e mountain peaks at dusk, Warli geometric border of protective tree branches, quiet contemplative atmosphere.",
                camera_angle="Wide panoramic mountain vista with soft twilight tones",
                cultural_notes="The Bodhisattva's verse from the Jataka: 'Truly, the turtle spoke and died; through his own speech he fell.'"
            )
        ]
    )
}

# --- Narrative Segmentation Engine ---

# In-memory storage for active generated custom stories
ACTIVE_STORIES: Dict[str, KamishibaiStory] = {}

class NarrativeSegmenter:
    """Orchestrates story segmentation using LangChain LLM or fallback heuristics."""

    def __init__(self):
        self.llm = None
        self._init_llm()

    def _init_llm(self):
        """Initializes LangChain LLM if credentials are present."""
        if settings.OPENAI_API_KEY:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model="gpt-4o",
                    temperature=0.7,
                    api_key=settings.OPENAI_API_KEY
                )
            except Exception as e:
                print(f"[NarrativeSegmenter] Could not init ChatOpenAI: {e}")
        elif settings.GEMINI_API_KEY:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",
                    temperature=0.7,
                    google_api_key=settings.GEMINI_API_KEY
                )
            except Exception as e:
                print(f"[NarrativeSegmenter] Could not init ChatGoogleGenerativeAI: {e}")

    def get_presets(self) -> List[Dict]:
        """Returns metadata for all available curated stories."""
        return [
            {
                "story_id": s.story_id,
                "title": s.title,
                "title_translations": s.title_translations,
                "source_tradition": s.source_tradition,
                "indian_style": s.indian_style,
                "japanese_style": s.japanese_style,
                "fusion_style_summary": s.fusion_style_summary,
                "moral": s.moral,
                "panel_count": len(s.panels)
            }
            for s in PRESET_STORIES.values()
        ]

    def get_preset_story(self, story_id: str) -> Optional[KamishibaiStory]:
        """Fetches a pre-segmented story by ID from presets or active stories."""
        return PRESET_STORIES.get(story_id) or ACTIVE_STORIES.get(story_id)

    def get_story(self, story_id: str) -> Optional[KamishibaiStory]:
        """Alias for get_preset_story."""
        return self.get_preset_story(story_id)

    def segment_story(
        self,
        story_text: str,
        title: str = "Indian Folk Tale",
        source: str = "Panchatantra",
        indian_style: str = "madhubani",
        japanese_style: str = "ukiyoe"
    ) -> KamishibaiStory:
        """
        Segments a raw story text into structured Kamishibai panels.
        Uses LangChain LLM when available; otherwise generates an intelligent dramatic breakdown.
        """
        # 1. Check if user selected or matched a canonical preset story
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
        for preset_id, preset in PRESET_STORIES.items():
            if preset_id == slug or preset.title.lower() == title.lower():
                ACTIVE_STORIES[preset.story_id] = preset
                return preset

        # 2. Try LLM pipeline if configured
        if self.llm:
            try:
                story = self._segment_with_llm(story_text, title, source, indian_style, japanese_style)
                ACTIVE_STORIES[story.story_id] = story
                return story
            except Exception as e:
                print(f"[NarrativeSegmenter] LLM generation failed, using intelligent rule segmenter: {e}")

        # 3. Fallback: Intelligent algorithmic narrative breakdown
        story = self._heuristic_segment(story_text, title, source, indian_style, japanese_style)
        ACTIVE_STORIES[story.story_id] = story
        return story

    def _segment_with_llm(
        self,
        story_text: str,
        title: str,
        source: str,
        indian_style: str,
        japanese_style: str
    ) -> KamishibaiStory:
        """Executes the LangChain LLM prompt chain."""
        from langchain_core.messages import SystemMessage, HumanMessage
        from langchain_core.output_parsers import PydanticOutputParser

        parser = PydanticOutputParser(pydantic_object=KamishibaiStory)
        
        ind_style_info = settings.INDIAN_STYLES.get(indian_style, settings.INDIAN_STYLES["madhubani"])
        jap_style_info = settings.JAPANESE_STYLES.get(japanese_style, settings.JAPANESE_STYLES["ukiyoe"])

        prompt_text = USER_SEGMENTATION_PROMPT.format(
            title=title,
            source=source,
            indian_style=ind_style_info["name"],
            indian_style_keywords=ind_style_info["keywords"],
            japanese_style=jap_style_info["name"],
            japanese_style_keywords=jap_style_info["keywords"],
            story_text=story_text
        )

        messages = [
            SystemMessage(content=SYSTEM_NARRATIVE_SEGMENTER),
            HumanMessage(content=prompt_text + "\n\n" + parser.get_format_instructions())
        ]

        response = self.llm.invoke(messages)
        parsed = parser.parse(response.content)
        return parsed

    def _heuristic_segment(
        self,
        story_text: str,
        title: str,
        source: str,
        indian_style: str,
        japanese_style: str
    ) -> KamishibaiStory:
        """
        Intelligently decomposes any arbitrary story text into 4 to 6 distinct Kamishibai panels,
        ensuring each scene has a unique setting, character action, and visual prompt.
        """
        raw_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', story_text) if len(s.strip()) > 5]
        if not raw_sentences:
            raw_sentences = [story_text]

        # Determine target scene count (between 4 and 6)
        if len(raw_sentences) >= 6:
            target_panels = 6
        elif len(raw_sentences) >= 4:
            target_panels = len(raw_sentences)
        else:
            target_panels = 4

        # Group sentences into target_panels chunks
        chunks = []
        if len(raw_sentences) <= target_panels:
            for s in raw_sentences:
                chunks.append(s)
            # If fewer than target_panels, pad logically
            while len(chunks) < target_panels:
                chunks.append(chunks[-1])
        else:
            step = len(raw_sentences) / target_panels
            for i in range(target_panels):
                start_idx = int(i * step)
                end_idx = int((i + 1) * step) if i < target_panels - 1 else len(raw_sentences)
                chunks.append(" ".join(raw_sentences[start_idx:end_idx]))

        ind_style_info = settings.INDIAN_STYLES.get(indian_style, settings.INDIAN_STYLES["madhubani"])
        jap_style_info = settings.JAPANESE_STYLES.get(japanese_style, settings.JAPANESE_STYLES["ukiyoe"])

        theatrical_acts = [
            {
                "act": "Act 1: Ki (起) - The World & Introduction",
                "stage": "[Sound: Hyoshigi clappers - Chon-chon! Slowly slide Card 1 into the Butai frame. Voice: Joyous, gentle cadence.]",
                "angle": "Wide panoramic establishing shot with ornamental floral borders",
                "pose": "Peaceful, serene introduction stance in their natural habitat",
                "expression": "Content, curious, and welcoming"
            },
            {
                "act": "Act 2: Shō (承) - The Inciting Incident & Journey",
                "stage": "[Keep card steady. Performer speaks in warm conversational tones, gesturing outward to audience.]",
                "angle": "Medium two-shot capturing the unexpected encounter and new surroundings",
                "pose": "Engaged in active motion, discovering something wondrous or strange",
                "expression": "Intrigued, marveling, beginning of change"
            },
            {
                "act": "Act 3: Shō-Ten (承-転) - Rising Tension & The Dilemma",
                "stage": "[Sound: Low sinister taiko drum roll - Dronnn... Narrator drops voice to a raspy, theatrical whisper.]",
                "angle": "Dynamic side-angle with contrasting light and deep shadows",
                "pose": "Facing a sudden dilemma or rising temptation amidst the gathering crowd",
                "expression": "Uneasy, tempted, conflicted"
            },
            {
                "act": "Act 4: Ten (転) - The Climax & Peril Revealed",
                "stage": "[Perform Nukikata: abruptly pull card halfway! Hold frozen for 2 seconds. Sound: Sudden Hyoshigi CLACK! Voice: Urgent gasp.]",
                "angle": "Dramatic low-angle close-up emphasizing peril and shock",
                "pose": "In mid-action at the peak of danger, truth suddenly laid bare",
                "expression": "Intense shock, panic, then sudden lightning-fast wit"
            },
            {
                "act": "Act 5: Ketsu (結) - The Great Escape & Outsmarting",
                "stage": "[Sound: Fast card slide with swoosh sound! Performer's voice resonates with triumphant energy.]",
                "angle": "Steep dynamic perspective showing swift escape and baffled adversaries",
                "pose": "Leaping or standing victorious, having outwitted the danger",
                "expression": "Triumphant, mocking, relieved"
            },
            {
                "act": "Act 6: Ketsu-Owari (結-終) - The Moral & Philosophical Reflection",
                "stage": "[Sound: Final ceremonial Hyoshigi clappers: Chon... Chon... Chon! Performer gently bows. Close Butai doors slowly.]",
                "angle": "Scenic golden sunset panorama with traditional calligraphy seal stamp",
                "pose": "Tranquil, meditative silhouette overlooking the serene landscape",
                "expression": "Enlightened, peaceful, contemplative"
            }
        ]

        panels = []
        for idx in range(target_panels):
            panel_id = idx + 1
            chunk = chunks[idx]
            act_info = theatrical_acts[min(idx, len(theatrical_acts) - 1)]

            # Construct unique, highly descriptive image prompt for this specific scene
            scene_action_desc = f"Scene from {title}, {act_info['act']}: {chunk[:200]}"
            img_prompt = (
                f"Masterpiece Japanese Kamishibai card illustration. {scene_action_desc}. "
                f"Character posture: {act_info['pose']}, emotion: {act_info['expression']}. "
                f"Visual Style: Authentic fusion of {ind_style_info['keywords']} AND {jap_style_info['keywords']}. "
                f"Composition: {act_info['angle']}, dramatic storytelling lighting, museum quality washi paper texture."
            )

            panels.append(
                Panel(
                    panel_id=panel_id,
                    scene_description=f"{act_info['act']}: {chunk[:220]}",
                    characters=[
                        Character(
                            name="Protagonist",
                            visual_features=f"Stylized in {ind_style_info['name']} and {jap_style_info['name']}",
                            pose=act_info["pose"],
                            expression=act_info["expression"]
                        )
                    ],
                    dialogue=Dialogue(
                        en=chunk[:320],
                        hi=f"कथा भाग {panel_id}: {chunk[:280]}",
                        ja=f"第{panel_id}幕: {chunk[:280]}"
                    ),
                    stage_notes=act_info["stage"],
                    image_prompt=img_prompt,
                    camera_angle=act_info["angle"],
                    cultural_notes=f"Lesson from {source}: Harmonizing cultural storytelling traditions through wisdom."
                )
            )

        slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-') or "kamishibai-story"

        return KamishibaiStory(
            story_id=slug,
            title=title,
            title_translations={
                "en": title,
                "hi": f"{title} (भारतीय लोककथा)",
                "ja": f"{title} (インド昔話)"
            },
            source_tradition=source,
            indian_style=indian_style,
            japanese_style=japanese_style,
            fusion_style_summary=f"Artistic synthesis of {ind_style_info['name']} with {jap_style_info['name']}.",
            moral={
                "en": "True wisdom, courage, and presence of mind conquer every treachery.",
                "hi": "सच्चा विवेक, साहस और बुद्धि प्रत्येक संकट पर विजय दिलाते हैं।",
                "ja": "真の知恵と冷静さこそが、あらゆる試練を乗り越える光となる。"
            },
            panels=panels
        )

narrative_segmenter = NarrativeSegmenter()

