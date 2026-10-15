# Hook 3 Verification Evidence: Markdown/prose corruption repair

Recorded at UTC: 2026-06-20T13:39:43Z
Workspace: W:\Stellar Influences

## Lint before rebuild

Invocation: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`
Exit code: 0
Output:
```text
Lint passed
```

## Rebuild index

Invocation: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py`
Exit code: 0
Output:
```text
```

## Rebuild query manifest

Invocation: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/query_manifest.py`
Exit code: 0
Output:
```text
```

## Lint after rebuild

Invocation: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`
Exit code: 0
Output:
```text
Lint passed
```

## Changed wiki files

Invocation: `git diff --name-only -- wiki`
Exit code: 0
Output:
```text
warning: in the working copy of 'wiki/axes/jupiter-neptune.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'wiki/axes/mercury-asc.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'wiki/axes/sun-moon.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'wiki/axes/venus-node.md', LF will be replaced by CRLF the next time Git touches it
wiki/axes/jupiter-neptune.md
wiki/axes/mars-jupiter.md
wiki/axes/mars-uranus.md
wiki/axes/mercury-asc.md
wiki/axes/moon-jupiter.md
wiki/axes/sun-moon.md
wiki/axes/sun-saturn.md
wiki/axes/venus-node.md
```

## Truncated fragment absence check

Invocation: `rg -n "exaltation of$|Moon Trine$|The Sun was with$|but with Sun and$|A child with the$|Sun Squared by$" wiki/axes/moon-jupiter.md wiki/axes/mars-jupiter.md wiki/axes/mars-uranus.md wiki/axes/sun-moon.md wiki/axes/sun-saturn.md`
Exit code: 1
Output:
```text
```

## Schema heading placement check

Invocation: `rg -n "^## Comparative Schema" scoped axis files`
Exit code: 0
Output:
```text
wiki/axes/mercury-asc.md:175:## Comparative Schema
wiki/axes/venus-node.md:173:## Comparative Schema
wiki/axes/jupiter-neptune.md:241:## Comparative Schema
wiki/axes/sun-saturn.md:231:## Comparative Schema
wiki/axes/sun-moon.md:294:## Comparative Schema
wiki/axes/mars-jupiter.md:233:## Comparative Schema
wiki/axes/mars-uranus.md:231:## Comparative Schema
wiki/axes/moon-jupiter.md:233:## Comparative Schema
```

## Embedded schema heading absence check

Invocation: `rg -n ".+## Comparative Schema" scoped heading-repair files`
Exit code: 1
Output:
```text
```

## Repaired snippet inspection

Invocation: `Get-Content line windows for eight repaired files`
Exit code: 0
Output:
```text
--- wiki/axes/moon-jupiter.md:123 ---
   123: ### Charles Carter - The Astrological Aspects
   124: 
   125: #### Harmonious Aspects
   126: 
   127: The Moon and Jupiter form an excellent combination, since they are assimilated by the exaltation of Jupiter in Cancer.
   128: 
   129: In regard to character and temperament, they cause the native to be good-natured, friendly, helpful and sympathetic, particularly with the unfortunate and helpless. There is usually much affection for animal pets. There is often a certain amount of shrewdness and business ability.
   130: 
   131: It is extremely favourable for matters of the 9th and 12th houses, such as sport, religion, drama, journalism, films, criticism and travel. Although there is no particular inclination to travel (unless this arises from something else in the map), it ensures fortunate circumstances should journeys in foreign countries be undertaken. In many cases, the "journeys" are of a mental and imaginary character, such as those of writers of fiction, or the speculation of philosophers, such as Swedenborg. It is excellent for residence abroad.
   132: 
   133: In the case of males it often appears to bring benefits through the wife, but, contrary to expectation, I do not find that men with this configuration always marry women of a Jovian character, unless there is a direct application to Jupiter. On the other hand, women with these aspects do seem to be attracted towards men of a religious or otherwise a Jupiter type. In my own family I know of three cases wherein women with the Moon in aspect to Jupiter have married men with that planet in the 1st house.
   134: 
   135: Its effects on the health are beneficial. It tends to good spirits, contentment and cheerful energy. The emotional nature is usually active, lively and inclined to optimism.
   136: 
   137: As with all contacts with Jupiter (even Inharmonious ones), the native will be brought into touch with wealth, even if he is not personally wealthy.
   138: 
   139: For some reason which I do not understand Moon Trine Jupiter in Air is common in the maps of violent criminals. Perhaps it aids the criminal to disguise his proclivities.
   140: 
   141: #### The Conjunction
   142: 
   143: This aspect, like the Harmonious contacts, confers great sympathy and protectiveness, as well as success in similar ways.
--- wiki/axes/mars-jupiter.md:139 ---
   139: In a congenial sign there may be a great love of fun and amusement, often with a satirical tendency. In more repressive signs (such as those ruled by Saturn or in Scorpio) it may give dissatisfaction and rebelliousness.
   140: 
   141: The native usually has an active and even a belligerent or disputative life, being either controversial or the object of controversy; or perhaps he is engaged in financial operations that bear resemblance to military maneuvers and conflicts. In any case he will prove a redoubtable opponent, with considerable resource and energy.
   142: 
   143: A good example of this combination is the natus of Martin Luther, the great Reformer and disputant, who had Venus, Mars and Jupiter conjoined in Libra, in Sextile to Uranus in Sagittary. The Sun was with Saturn in Scorpio, reducing the power of the triple conjunction to produce material comfort, although, even so, the native did abandon monastic life, and married.
   144: 
   145: It inclines to daring undertakings and feats of prowess and courage.
--- wiki/axes/mars-uranus.md:129 ---
   129: They greatly add to the energy, vigour, decision and will-power of the native, who is very rarely of a milk-and-water or nondescript character. He will as a rule know his own mind excellently well, and much will depend on the rest of the map, for, unless this shows sense and judgment, the strength of Mars-Uranus may lead to disaster because of its very strength and courage.
   130: 
   131: It tends to give physical robustness, the ability to stand hard conditions, and the capacity for hard work, but even thus, cross aspects from other bodies may result in high nervous tension and an overwrought condition, the will, as it were, tearing the body asunder.
   132: 
   133: In one case known to me there is a Trine between Mars (Taurus) and Uranus (Virgo) with a cross aspect to the latter from the Sun (Sagittarius). Here the heart has suffered, as the outcome of nervous strain, and the native is almost an invalid. In another case, with the same Trine from the same signs, but with Sun and Saturn in Square to Uranus from Gemini, there is indomitable courage, but it is spent in an uphill fight with poverty and sickness. In the former case the Sun, having the Trine of Saturn, indicated affluent conditions, but for which the native would probably have collapsed altogether.
   134: 
   135: It may be said that any ill aspect to this combination will occasion a greater or less degree of nerve-tension.
--- wiki/axes/sun-moon.md:146 ---
   146: But, it may be repeated that the Sun must be considered above all else in judging the active life. Its aspects indicate the measure of success that will be attained, in what direction, and with what facility or tribulation. It represents the work to be done, due attention being paid to the sign, house and aspects involved.
   147: 
   148: The Moon is more important in relation to ordinary character, and this is particularly so in early life before the Sun's influence makes itself felt. A child with the Moon in Square to Mars but Sun in Trine to Saturn will be hot-tempered or impulsive, but will become, as the years pass, prudent and controlled, at least in action. Habits, morals and temperament are all shown to a large extent by the Moon, the Ascendant being even less self-conscious and rising little above the sensations and instincts, important though these are in their spheres.
   149: 
   150: The mutual aspects are of a general and diffused character rather than particular and focused - the particularization lies with the planets. Hence their effects are not always easily traced unless life and character can be viewed in perspective.
--- wiki/axes/sun-saturn.md:149 ---
   149: The Opposition seems not altogether bad, probably because the two bodies rule opposite signs and therefore there is some kinship between the Opposition aspect and this mutual relation. It is not incompatible with considerable worldly success, if other aspects favour, though such success will be won only by sheer hard work and may be retained with difficulty. Often the early life is very hard and the father is of no use to the native; real sympathy between them is rare. He may be hard or unsuccessful or a reprobate. A case in point is that of the ex-Kaiser, whose father ruled only for a short time, died of cancer and was never intimate with his son. I have a case of a man with Sun Square Saturn who as a child was obliged to fetch his father from the public-house regularly - he grew up a person of staunch moral character, worked extremely hard all his life, and, after severe checks, accumulated a moderate fortune. Here the native's life was embittered because, though fairly successful, he did not attain his ambitions, which were considerable. In other cases known to me the Sun-Saturn native has achieved a great deal in terms of social status, but not in actual tangible cash. Again, the inhibition is sometimes largely physical (cf. the ex-Kaiser's withered arm).
   150: 
   151: We may distinguish three types: the ambitious but incompetent man who "fails," the man who is not ambitious or interested in material affairs, but has to spend his life with them, and the competent and ambitious man who is confronted with obstacles and illluck. Often it seems as if this third class does not suffer much discontent from the fact that he has to work hard for comparatively little emolument; in a word, he accepts the Saturnian destiny philosophically and becomes a willing, if not a cheerful, captive of the planet's regime, finding a sort of satisfaction in the fact that he earns every penny he gets, and sometimes a good deal more. But this will depend upon the general tenor of the map, and especially upon the nature of the Ascendant. In a case of the Sun Squared by Saturn in Aquarius I have found the native very cheerful in poverty, bearing it in an idealistic spirit.
   152: 
   153: The difficulty is always, at heart, one of self-expression. Either proper expression is denied or delayed until it is almost too late to serve its purpose, or else the native tries "to force the issue" and blunders disastrously. Sometimes the issue is shirked and there is shyness or timidity, which may be hidden behind blatant boastfulness.
--- wiki/axes/jupiter-neptune.md:236 ---
   236: - comparison: Development Dissolution Faith Vision Religion Spirituality Dogmatic Mystic
   237: - general: Highest happiness or apparent luck . Being guided on trips . The hypocrite . Trusting one's guardian angel .
   238: - harmony: The Dancing Dervish. Finding the meaning of life in a mystic experience or being found by meaning. Kindness and compassion. Genuine altruism, highest ideals, true spirituality, harmonious connection of faith and inspiration, good visionary gifts. Trance and illumination. Fine sense for happiness.
   239: - discord: The Religious Crackpot. Feels oneself to be the chosen one, illuminated and wise. Seduces others or becomes the victim of peculiar sects, strange ideologies, and crackpot views of the world. Religious delusions. Victim of own dream images and yearnings. Intoxication.
   240: 
   241: ## Comparative Schema
   242: 
--- wiki/axes/mercury-asc.md:170 ---
   170: #### Banzhaf/Haebler Aspect Keywords
   171: 
   172: - harmony: The Nimble Individual. Skillful and nimble in behavior. Enjoys contacts and communication. Diplomatic and entertaining. Intellectual touch.
   173: - discord: The Cunning Person. Difficulties, insincerity, and slyness in communication with the surrounding world. Deceives, outsmarts, and slanders other people. Also becomes a victim. Many misunderstandings, exaggerated criticism, and gossip. Untiring spirit of contradiction.
   174: 
   175: ## Comparative Schema
   176: 
--- wiki/axes/venus-node.md:168 ---
   168: #### Banzhaf/Haebler Aspect Keywords
   169: 
   170: - harmony: Love, liking, grace, eroticism, affection, solidarity with another person, as well as a sense of beauty, appreciation of art, and good taste unite in harmony with the priority in life and are helpful on life's path. Feminine aura as valuable potential that should be recognized and developed.
   171: - discord: Lasting difficulties in finding inner peace because love life has an inhibiting and disruptive effect on the actual direction in life. Feelings of being unfulfilled and great needs for affection that are difficult to satisfy.
   172: 
   173: ## Comparative Schema
   174: 
```

## Judgment

PASS: Fresh hook-3 verification reran lint/rebuild/query/lint, confirmed only the eight scoped wiki files changed, confirmed old truncated fragments and embedded schema headings are absent, and inspected repaired snippets.