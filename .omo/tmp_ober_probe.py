import fitz, re, pathlib
p = pathlib.Path(r'W:/books references etc/!master list astro/midpoints - Aren Ober - Midpoint Interpretation.pdf')
d = fitz.open(p)
terms = ['Table of Contents','SUN/MOON','Sun/Moon','Midpoint Structures','MIDPOINT INTERPRETATION','Cosmogram','Jupiter','Venus']
for i in range(len(d)):
    t = d[i].get_text('text')
    if any(term in t for term in terms):
        clean = re.sub(r'\s+', ' ', t).strip()
        print('PAGE', i+1, clean[:1800].encode('ascii','replace').decode())
