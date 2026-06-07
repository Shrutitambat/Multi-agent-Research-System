import streamlit as st

st.set_page_config(
    page_title="ResearchMind — AI Multi-Agent Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Auth ──────────────────────────────────────────────────────────────────────
auth_url = "#"
try:
    from auth import is_authenticated, handle_callback, get_auth_url
    if is_authenticated():
        st.switch_page("pages/app.py")
    if handle_callback():
        st.switch_page("pages/app.py")
    try:
        auth_url = get_auth_url()
    except Exception:
        auth_url = "#"
        st.warning("Google OAuth not configured. Fill in `.streamlit/secrets.toml`.", icon="🔑")
except ImportError:
    pass

def H(s): st.markdown(s, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CSS — exact same palette as app.py
# ══════════════════════════════════════════════════════════════════════════════
H("""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:      #03050f;
  --bg2:     #060916;
  --surf:    rgba(255,255,255,.04);
  --surf2:   rgba(255,255,255,.07);
  --border:  rgba(255,255,255,.07);
  --bhi:     rgba(99,102,241,.4);
  --p:       #6366f1;
  --p2:      #818cf8;
  --cyan:    #22d3ee;
  --emerald: #10b981;
  --rose:    #f43f5e;
  --text:    #f1f5f9;
  --muted:   #64748b;
  --muted2:  #94a3b8;
  --dp:      'Plus Jakarta Sans', sans-serif;
  --body:    'Space Grotesk', sans-serif;
  --mono:    'JetBrains Mono', monospace;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
html, body, [class*="css"], .main, .block-container {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--body) !important;
}
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,.35); border-radius: 2px; }

/* ════ STREAMLIT GRID FIX ════ */
/* Streamlit wraps markdown in stMarkdown > div > p structure.
   We need hero-section to be a real CSS grid. 
   The key is that hero-section is the grid, 
   and hero-left / hero-right must be direct grid children.
   Since they're all in ONE H() call, they ARE direct children. */

/* Remove Streamlit's default block wrapper interference */
.stMarkdown { display: contents !important; }
.element-container:has(.hero-section) { display: contents !important; }

/* ════ NAVBAR ════ */
.nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 6vw; height: 64px;
  background: rgba(3,5,15,.9);
  backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--border);
}
.nav-logo {
  font-family: var(--dp); font-size: 1.22rem; font-weight: 800;
  letter-spacing: -.04em; color: #fff;
}
.nav-logo span { color: var(--p2); }
.nav-links { display: flex; gap: 2.2rem; list-style: none; }
.nav-links a {
  font-size: .82rem; font-weight: 500; color: var(--muted);
  text-decoration: none; transition: color .2s;
}
.nav-links a:hover { color: var(--text); }
.nav-cta {
  display: inline-flex; align-items: center; gap: .45rem;
  background: linear-gradient(135deg, var(--p), #4338ca);
  color: #fff; border: none; border-radius: 8px;
  font-family: var(--body); font-size: .8rem; font-weight: 600;
  padding: .5rem 1.15rem; cursor: pointer; text-decoration: none;
  box-shadow: 0 0 18px rgba(99,102,241,.28);
  transition: transform .2s, box-shadow .2s, opacity .2s;
}
.nav-cta:hover { transform: translateY(-1px); box-shadow: 0 4px 22px rgba(99,102,241,.5); opacity: .92; }

/* ════ HERO ════ */
.hero-section {
  min-height: 100vh;
  display: grid !important;
  grid-template-columns: 55% 45%;
  align-items: center;
  padding: 80px 6vw 60px;
  position: relative;
  overflow: hidden;
  gap: 2rem;
}
/* ensure Streamlit wrapper doesn't break grid */
.hero-section > .hero-mesh,
.hero-section > .hero-dots {
  display: none; /* handled as absolute positioning */
}
.hero-mesh {
  display: block !important;
  position: absolute;
}
.hero-dots {
  display: block !important;
  position: absolute;
}

/* background layers */
.hero-mesh {
  position: absolute; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 60% 55% at 65% 44%, rgba(99,102,241,.14) 0%, transparent 65%),
    radial-gradient(ellipse 40% 42% at 14% 72%, rgba(34,211,238,.08) 0%, transparent 55%),
    radial-gradient(ellipse 48% 36% at 82% 12%, rgba(244,63,94,.06) 0%, transparent 50%);
}
.hero-dots {
  position: absolute; inset: 0; z-index: 0; pointer-events: none;
  background-image: radial-gradient(circle, rgba(255,255,255,.055) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: radial-gradient(ellipse 88% 88% at 50% 50%, black 20%, transparent 80%);
  animation: dots-drift 24s ease-in-out infinite alternate;
}
@keyframes dots-drift {
  from { background-position: 0 0; }
  to   { background-position: 42px 42px; }
}

/* ── LEFT COLUMN ── */
.hero-left {
  position: relative; z-index: 2;
  display: flex; flex-direction: column; align-items: flex-start;
}

.eyebrow {
  display: inline-flex; align-items: center; gap: .5rem;
  font-family: var(--mono); font-size: .62rem; letter-spacing: .18em;
  color: var(--cyan);
  border: 1px solid rgba(34,211,238,.22);
  background: rgba(34,211,238,.06);
  border-radius: 100px; padding: 5px 14px;
  margin-bottom: 1.75rem; width: fit-content;
  animation: fade-up .5s ease both;
}
.eyebrow-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--cyan);
  animation: blink-dot 2s ease infinite; flex-shrink: 0;
}
@keyframes blink-dot { 0%,100%{opacity:1;} 50%{opacity:.15;} }

.hero-h1 {
  font-family: var(--dp) !important;
  font-size: clamp(2.6rem, 3.8vw, 3.8rem) !important;
  font-weight: 800 !important;
  line-height: 1.06 !important;
  letter-spacing: -.05em !important;
  color: #fff !important;
  margin-bottom: 1.4rem !important;
  animation: fade-up .5s .07s ease both;
}
.hero-grad {
  background: linear-gradient(90deg, var(--p2) 0%, var(--cyan) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}

.hero-sub {
  font-size: .97rem; line-height: 1.8; color: var(--muted2);
  max-width: 460px; margin-bottom: 2.2rem;
  animation: fade-up .5s .14s ease both;
}

.hero-btns {
  display: flex; gap: .85rem; flex-wrap: wrap;
  margin-bottom: 2.6rem;
  animation: fade-up .5s .21s ease both;
}
.btn-primary {
  display: inline-flex; align-items: center; gap: .55rem;
  background: linear-gradient(135deg, var(--p), #4338ca);
  color: #fff; border: none; border-radius: 10px;
  font-family: var(--body); font-size: .9rem; font-weight: 600;
  padding: .78rem 1.75rem; cursor: pointer; text-decoration: none;
  box-shadow: 0 4px 22px rgba(99,102,241,.4);
  transition: transform .2s, box-shadow .2s;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 32px rgba(99,102,241,.55); }
.btn-ghost {
  display: inline-flex; align-items: center; gap: .5rem;
  background: transparent; color: var(--text);
  border: 1px solid rgba(99,102,241,.38); border-radius: 10px;
  font-family: var(--body); font-size: .9rem; font-weight: 500;
  padding: .78rem 1.75rem; cursor: pointer; text-decoration: none;
  transition: background .2s, border-color .2s, transform .15s;
}
.btn-ghost:hover { background: rgba(99,102,241,.08); border-color: var(--p2); transform: translateY(-1px); }

/* stats strip — identical to app.py surface style */
.stats-strip {
  display: flex; border: 1px solid var(--border);
  border-radius: 12px; overflow: hidden;
  animation: fade-up .5s .28s ease both;
  background: var(--surf);
  backdrop-filter: blur(14px);
}
.stat-cell {
  flex: 1; padding: 1.15rem .9rem;
  border-right: 1px solid var(--border); text-align: center;
}
.stat-cell:last-child { border-right: none; }
.stat-val {
  font-family: var(--dp); font-size: 1.65rem; font-weight: 800;
  letter-spacing: -.04em;
  background: linear-gradient(135deg, #fff, var(--p2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-lbl { font-size: .6rem; color: var(--muted); margin-top: 3px; font-family: var(--mono); letter-spacing: .1em; }

/* ── RIGHT COLUMN: diagram ── */
.hero-right {
  position: relative; z-index: 2;
  display: flex; align-items: center; justify-content: center;
  height: 500px;
  animation: fade-in .8s .15s ease both;
}
@keyframes fade-in { from{opacity:0;} to{opacity:1;} }

/* diagram container */
.diagram {
  position: relative;
  width: 420px; height: 420px;
}

/* glow blobs */
.gblob {
  position: absolute; border-radius: 50%;
  filter: blur(65px); pointer-events: none;
}
.gb1 { width: 260px; height: 260px; background: rgba(99,102,241,.2);  top: 8%;  left: 4%; }
.gb2 { width: 180px; height: 180px; background: rgba(34,211,238,.13); bottom: 8%; right: 2%; }
.gb3 { width: 130px; height: 130px; background: rgba(244,63,94,.1);   top: 28%; right: 1%; }

/* orbit rings */
.ring {
  position: absolute; top: 50%; left: 50%;
  border-radius: 50%;
  transform: translate(-50%, -50%);
}
.r1 { width: 158px; height: 158px; border: 1px solid rgba(99,102,241,.28); animation: spin 13s linear infinite; }
.r2 { width: 272px; height: 272px; border: 1px dashed rgba(255,255,255,.07); animation: spin 21s linear infinite reverse; }
.r3 { width: 388px; height: 388px; border: 1px solid rgba(255,255,255,.04); animation: spin 34s linear infinite; }
@keyframes spin {
  from { transform: translate(-50%,-50%) rotate(0deg); }
  to   { transform: translate(-50%,-50%) rotate(360deg); }
}

/* center node */
.cnode {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 74px; height: 74px; border-radius: 20px;
  background: linear-gradient(135deg, var(--p), #4338ca);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.7rem; z-index: 5;
  box-shadow: 0 0 48px rgba(99,102,241,.6), 0 0 96px rgba(99,102,241,.22);
  animation: glow-beat 3s ease-in-out infinite;
}
@keyframes glow-beat {
  0%,100% { box-shadow: 0 0 48px rgba(99,102,241,.6), 0 0 96px rgba(99,102,241,.22); }
  50%      { box-shadow: 0 0 68px rgba(99,102,241,.88), 0 0 124px rgba(99,102,241,.4); }
}

/* agent nodes — 6 evenly spaced on a circle (60deg apart) */
.anode {
  position: absolute;
  width: 54px; height: 54px; border-radius: 13px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  font-size: 1.22rem; z-index: 6;
  background: rgba(255,255,255,.055);
  border: 1px solid rgba(255,255,255,.11);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 18px rgba(0,0,0,.5);
  transition: transform .3s, box-shadow .3s;
  cursor: default;
}
.anode:hover { transform: scale(1.18) !important; box-shadow: 0 8px 28px rgba(99,102,241,.4); }
.albl { font-family: var(--mono); font-size: .37rem; color: var(--muted); margin-top: 1px; letter-spacing: .06em; }

/*
  6 agents on radius=140px circle, spaced 60deg apart.
  0deg=top, going clockwise.
  center = 210px,210px (half of 420px)
  r = 140
  pos(deg) => left = 210 + 140*sin(deg) - 27, top = 210 - 140*cos(deg) - 27
*/
.a0 { left: 183px; top:  43px; } /* 0deg   — top center     */
.a1 { left: 304px; top: 113px; } /* 60deg  — top right      */
.a2 { left: 304px; top: 253px; } /* 120deg — bottom right   */
.a3 { left: 183px; top: 323px; } /* 180deg — bottom center  */
.a4 { left:  62px; top: 253px; } /* 240deg — bottom left    */
.a5 { left:  62px; top: 113px; } /* 300deg — top left       */

/* animated data packets */
.pkt {
  position: absolute; width: 7px; height: 7px; border-radius: 50%; z-index: 7;
}
.pk1 { background: var(--cyan);    box-shadow: 0 0 10px var(--cyan);    animation: pmove1 2.8s ease-in-out infinite; }
.pk2 { background: var(--p2);     box-shadow: 0 0 10px var(--p2);     animation: pmove2 3.4s ease-in-out .6s infinite; }
.pk3 { background: var(--emerald);box-shadow: 0 0 10px var(--emerald);animation: pmove3 2.5s ease-in-out 1.3s infinite; }
.pk4 { background: var(--rose);   box-shadow: 0 0 10px var(--rose);   animation: pmove4 3.1s ease-in-out 2s infinite; }

/* packets travel from center outward to each agent */
@keyframes pmove1 { 0%{top:207px;left:207px;opacity:0;} 15%{opacity:1;} 100%{top:57px;left:193px;opacity:0;} }
@keyframes pmove2 { 0%{top:207px;left:207px;opacity:0;} 15%{opacity:1;} 100%{top:127px;left:311px;opacity:0;} }
@keyframes pmove3 { 0%{top:207px;left:207px;opacity:0;} 15%{opacity:1;} 100%{top:336px;left:193px;opacity:0;} }
@keyframes pmove4 { 0%{top:207px;left:207px;opacity:0;} 15%{opacity:1;} 100%{top:267px;left: 68px;opacity:0;} }

/* ════ ANIMATIONS ════ */
@keyframes fade-up {
  from { opacity:0; transform: translateY(18px); }
  to   { opacity:1; transform: translateY(0); }
}

/* ════ SECTIONS — same surface/border as app.py cards ════ */
.section { padding: 88px 6vw; position: relative; }
.section-alt { background: rgba(255,255,255,.016); }

.section-tag {
  font-family: var(--mono); font-size: .62rem; letter-spacing: .2em;
  text-transform: uppercase; color: var(--p2);
  display: block; margin-bottom: .7rem;
}
.section-title {
  font-family: var(--dp) !important;
  font-size: clamp(1.8rem, 3vw, 2.65rem) !important;
  font-weight: 800 !important; letter-spacing: -.04em !important;
  color: #fff !important; line-height: 1.1 !important;
  margin-bottom: .85rem !important;
}
.section-sub {
  font-size: .93rem; line-height: 1.78; color: var(--muted2);
  max-width: 560px; margin-bottom: 3rem;
}
.centered { text-align: center; }
.centered .section-sub { margin-left: auto; margin-right: auto; }

/* two-col */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 4.5rem; align-items: center; }

/* ════ FEATURE CARDS — same style as result-wrap in app.py ════ */
.fgrid   { display: grid; grid-template-columns: repeat(auto-fit, minmax(255px,1fr)); gap: 1.2rem; }
.fgrid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }

.fcard {
  background: var(--surf); border: 1px solid var(--border);
  border-radius: 14px; padding: 1.6rem;
  position: relative; overflow: hidden;
  backdrop-filter: blur(14px);
  transition: border-color .3s, transform .3s, box-shadow .3s;
}
.fcard::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--p), transparent);
  opacity: 0; transition: opacity .3s;
}
.fcard:hover { border-color: rgba(99,102,241,.32); transform: translateY(-4px); box-shadow: 0 14px 42px rgba(0,0,0,.5); }
.fcard:hover::before { opacity: 1; }
.fcard-icon {
  width: 42px; height: 42px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem; margin-bottom: 1rem;
  background: linear-gradient(135deg, rgba(99,102,241,.2), rgba(34,211,238,.08));
  border: 1px solid rgba(99,102,241,.18);
}
.fcard-title { font-family: var(--dp); font-size: .92rem; font-weight: 700; color: #fff; margin-bottom: .4rem; letter-spacing: -.02em; }
.fcard-desc  { font-size: .8rem; line-height: 1.65; color: var(--muted2); }

/* ════ WORKFLOW ════ */
.workflow { max-width: 640px; margin: 0 auto; }
.wstep { display: flex; gap: 1.4rem; align-items: flex-start; padding: 1.15rem 0; position: relative; }
.wstep-line { position: absolute; left: 21px; top: 52px; bottom: -10px; width: 2px; background: linear-gradient(to bottom, var(--p), transparent); }
.wstep:last-child .wstep-line { display: none; }
.wstep-num {
  width: 44px; height: 44px; border-radius: 11px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--mono); font-size: .78rem; font-weight: 600; color: #fff;
  background: linear-gradient(135deg, var(--p), #4338ca);
  box-shadow: 0 4px 16px rgba(99,102,241,.32); position: relative; z-index: 1;
}
.wstep-body { padding-top: .3rem; }
.wstep-title { font-family: var(--dp); font-size: .92rem; font-weight: 700; color: #fff; margin-bottom: .26rem; letter-spacing: -.02em; }
.wstep-desc  { font-size: .8rem; line-height: 1.65; color: var(--muted2); }

/* ════ BENEFIT CARDS ════ */
.bgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(215px,1fr)); gap: 1rem; }
.bcard {
  background: var(--surf); border: 1px solid var(--border);
  border-radius: 13px; padding: 1.3rem 1.4rem;
  display: flex; align-items: flex-start; gap: .85rem;
  backdrop-filter: blur(10px); transition: border-color .25s, transform .25s;
}
.bcard:hover { border-color: rgba(99,102,241,.3); transform: translateY(-3px); }
.bcard-icon  { font-size: 1.22rem; flex-shrink: 0; margin-top: 1px; }
.bcard-title { font-family: var(--dp); font-size: .87rem; font-weight: 700; color: #fff; margin-bottom: .22rem; letter-spacing: -.02em; }
.bcard-desc  { font-size: .76rem; line-height: 1.6; color: var(--muted2); }

/* ════ USE CASE CARDS ════ */
.ugrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(215px,1fr)); gap: 1.2rem; }
.ucard {
  background: var(--surf); border: 1px solid var(--border);
  border-radius: 14px; padding: 1.65rem 1.5rem;
  position: relative; overflow: hidden;
  backdrop-filter: blur(10px); transition: border-color .3s, transform .3s;
}
.ucard::after {
  content: ''; position: absolute; bottom: -22px; right: -22px;
  width: 80px; height: 80px; border-radius: 50%;
  background: radial-gradient(circle, rgba(99,102,241,.13), transparent 70%);
  pointer-events: none;
}
.ucard:hover { border-color: rgba(99,102,241,.32); transform: translateY(-4px); }
.ucard-icon  { font-size: 1.6rem; margin-bottom: .82rem; }
.ucard-title { font-family: var(--dp); font-size: .9rem; font-weight: 700; color: #fff; margin-bottom: .38rem; letter-spacing: -.02em; }
.ucard-desc  { font-size: .78rem; line-height: 1.65; color: var(--muted2); }

/* ════ CTA ════ */
.cta-wrap { padding: 106px 6vw; text-align: center; position: relative; overflow: hidden; }
.cta-glow {
  position: absolute; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 62% 62% at 50% 50%, rgba(99,102,241,.12) 0%, transparent 65%),
    radial-gradient(ellipse 36% 42% at 18% 22%, rgba(34,211,238,.07) 0%, transparent 55%);
}
.cta-wrap > * { position: relative; z-index: 1; }
.cta-title {
  font-family: var(--dp) !important;
  font-size: clamp(2rem, 3.8vw, 3.1rem) !important;
  font-weight: 800 !important; letter-spacing: -.05em !important;
  color: #fff !important; line-height: 1.08 !important;
  margin-bottom: 1.15rem !important;
}
.cta-sub { font-size: .93rem; line-height: 1.75; color: var(--muted2); max-width: 455px; margin: 0 auto 2.3rem; }

/* ════ FOOTER ════ */
.footer {
  padding: 1.6rem 6vw; border-top: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 1rem; font-size: .72rem; color: var(--muted);
}
.footer-brand { font-family: var(--dp); font-weight: 800; font-size: .9rem; color: #fff; letter-spacing: -.02em; }

/* ════ PARTICLES ════ */
.particles { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.pt {
  position: absolute; border-radius: 50%;
  animation: pfloat linear infinite;
}
@keyframes pfloat {
  0%   { transform: translateY(105vh) scale(0); opacity: 0; }
  8%   { opacity: 1; }
  92%  { opacity: 1; }
  100% { transform: translateY(-8vh) scale(1); opacity: 0; }
}
</style>""")

# ── PARTICLES ──
H("""<div class="particles">
  <div class="pt" style="width:3px;height:3px;left:7%;background:#6366f1;animation-duration:21s;animation-delay:0s;opacity:.18;"></div>
  <div class="pt" style="width:4px;height:4px;left:21%;background:#22d3ee;animation-duration:27s;animation-delay:5s;opacity:.13;"></div>
  <div class="pt" style="width:3px;height:3px;left:42%;background:#818cf8;animation-duration:19s;animation-delay:9s;opacity:.17;"></div>
  <div class="pt" style="width:5px;height:5px;left:61%;background:#6366f1;animation-duration:24s;animation-delay:2s;opacity:.11;"></div>
  <div class="pt" style="width:3px;height:3px;left:79%;background:#22d3ee;animation-duration:29s;animation-delay:12s;opacity:.15;"></div>
  <div class="pt" style="width:4px;height:4px;left:91%;background:#f43f5e;animation-duration:22s;animation-delay:7s;opacity:.11;"></div>
</div>""")

# ── NAVBAR ──
H(f"""<nav class="nav">
  <div class="nav-logo">Research<span>Mind</span></div>
  <ul class="nav-links">
    <li><a href="#features">Features</a></li>
    <li><a href="#workflow">Workflow</a></li>
    <li><a href="#benefits">Benefits</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
  <a href="{auth_url}" class="nav-cta">&#128272; Sign in with Google</a>
</nav>""")

# ── HERO — single call (both columns in one markdown to keep flex layout intact) ──
H(f"""<section class="hero-section" id="home">
  <div class="hero-mesh"></div>
  <div class="hero-dots"></div>

  <!-- LEFT COLUMN -->
  <div class="hero-left">
    <div class="eyebrow"><span class="eyebrow-dot"></span>MULTI-AGENT AI RESEARCH PLATFORM</div>
    <h1 class="hero-h1">
      AI-Powered<br>
      <span class="hero-grad">Multi-Agent</span><br>
      Research Platform
    </h1>
    <p class="hero-sub">
      ResearchMind automates complex research workflows using specialized AI agents
      working in concert &#8212; collecting insights, validating sources, analyzing
      findings, and generating professional reports in minutes, not hours.
    </p>
    <div class="hero-btns">
      <a href="{auth_url}" class="btn-primary">&#128272; Continue with Google</a>
      <a href="#features" class="btn-ghost">Explore Features &#8595;</a>
    </div>
    <div class="stats-strip">
      <div class="stat-cell"><div class="stat-val">4&#215;</div><div class="stat-lbl">FASTER</div></div>
      <div class="stat-cell"><div class="stat-val">6</div><div class="stat-lbl">AGENTS</div></div>
      <div class="stat-cell"><div class="stat-val">99%</div><div class="stat-lbl">ACCURACY</div></div>
      <div class="stat-cell"><div class="stat-val">&#8734;</div><div class="stat-lbl">TOPICS</div></div>
    </div>
  </div>

  <!-- RIGHT COLUMN: diagram -->
  <div class="hero-right">
    <div class="diagram">
      <div class="gblob gb1"></div>
      <div class="gblob gb2"></div>
      <div class="gblob gb3"></div>
      <div class="ring r1"></div>
      <div class="ring r2"></div>
      <div class="ring r3"></div>
      <div class="cnode">&#128302;</div>
      <div class="anode a0">&#128269;<span class="albl">SEARCH</span></div>
      <div class="anode a1">&#128196;<span class="albl">READER</span></div>
      <div class="anode a2">&#129518;<span class="albl">ANALYST</span></div>
      <div class="anode a3">&#128202;<span class="albl">REPORT</span></div>
      <div class="anode a4">&#9989;<span class="albl">VERIFY</span></div>
      <div class="anode a5">&#9997;&#65039;<span class="albl">WRITER</span></div>
      <div class="pkt pk1"></div>
      <div class="pkt pk2"></div>
      <div class="pkt pk3"></div>
      <div class="pkt pk4"></div>
    </div>
  </div>
</section>
<script>
<script>
(function()
  function fixGrid(){{
    var hero = document.querySelector(".hero-section");
    if(!hero){{ setTimeout(fixGrid,150); return; }}

    var node = hero.parentElement;

    for(var i=0;i<8;i++){{

      if(!node || node.tagName==="BODY") break;
      if(node.classList.contains("block-container")) break;

      node.style.display="contents";
      node = node.parentElement;
    }}
  }}

</script>""")

# ════ SECTION 2 — WHY ════
H("""<section class="section section-alt" id="features">
  <div class="two-col">
    <div>
      <span class="section-tag">WHY RESEARCHMIND</span>
      <h2 class="section-title">Professional AI Research Automation</h2>
      <p class="section-sub" style="margin-bottom:0;">
        A multi-agent architecture where specialized AI agents collaborate to conduct
        research, validate information, analyze findings, and produce comprehensive
        reports &#8212; no manual hours required.
      </p>
    </div>
    <div class="fgrid-2">
      <div class="fcard"><div class="fcard-icon">&#129309;</div><div class="fcard-title">Multi-Agent Collaboration</div><div class="fcard-desc">Specialized agents work in parallel, each handling a distinct stage of the research pipeline.</div></div>
      <div class="fcard"><div class="fcard-icon">&#9889;</div><div class="fcard-title">Real-Time Research</div><div class="fcard-desc">Live web search and scraping delivers up-to-date, relevant information instantly.</div></div>
      <div class="fcard"><div class="fcard-icon">&#128221;</div><div class="fcard-title">Automated Reports</div><div class="fcard-desc">Structured, professional reports generated automatically from validated insights.</div></div>
      <div class="fcard"><div class="fcard-icon">&#128737;&#65039;</div><div class="fcard-title">Source Verification</div><div class="fcard-desc">Every source is cross-checked for credibility before inclusion in the final report.</div></div>
      <div class="fcard"><div class="fcard-icon">&#129504;</div><div class="fcard-title">Smart Summarization</div><div class="fcard-desc">Key insights distilled into concise executive summaries for fast decision-making.</div></div>
      <div class="fcard"><div class="fcard-icon">&#128228;</div><div class="fcard-title">Export to PDF</div><div class="fcard-desc">Download polished, shareable reports in PDF and plain text with one click.</div></div>
    </div>
  </div>
</section>""")

# ════ SECTION 3 — WORKFLOW ════
H("""<section class="section" id="workflow">
  <div class="centered">
    <span class="section-tag">HOW IT WORKS</span>
    <h2 class="section-title">Five Stages to Insight</h2>
    <p class="section-sub">From raw topic to polished, validated research report &#8212; fully automated.</p>
  </div>
  <div class="workflow">
    <div class="wstep"><div class="wstep-line"></div><div class="wstep-num">01</div><div class="wstep-body"><div class="wstep-title">Enter Research Topic</div><div class="wstep-desc">Provide a topic, question, or area of investigation. ResearchMind handles the rest.</div></div></div>
    <div class="wstep"><div class="wstep-line"></div><div class="wstep-num">02</div><div class="wstep-body"><div class="wstep-title">AI Agents Collect Information</div><div class="wstep-desc">Agents gather information from multiple web sources simultaneously, scraping the most relevant content for deep analysis.</div></div></div>
    <div class="wstep"><div class="wstep-line"></div><div class="wstep-num">03</div><div class="wstep-body"><div class="wstep-title">Validation &amp; Analysis</div><div class="wstep-desc">Findings are verified, filtered, and analyzed. Only credible content advances to the report stage.</div></div></div>
    <div class="wstep"><div class="wstep-line"></div><div class="wstep-num">04</div><div class="wstep-body"><div class="wstep-title">Report Generation</div><div class="wstep-desc">Writer and Critic agents collaborate to produce a structured, professionally written report.</div></div></div>
    <div class="wstep"><div class="wstep-num">05</div><div class="wstep-body"><div class="wstep-title">Export &amp; Share</div><div class="wstep-desc">Download in PDF or text format and share with your team instantly.</div></div></div>
  </div>
</section>""")

# ════ SECTION 4 — AGENTS ════
H("""<section class="section section-alt">
  <div class="centered">
    <span class="section-tag">AGENT ARCHITECTURE</span>
    <h2 class="section-title">Six Specialized AI Agents</h2>
    <p class="section-sub">Each agent is purpose-built for one stage, working in concert to deliver results no single model could achieve alone.</p>
  </div>
  <div class="fgrid">
    <div class="fcard"><div class="fcard-icon">&#128269;</div><div class="fcard-title">Research Agent</div><div class="fcard-desc">Deep web research and information gathering from diverse, authoritative sources.</div></div>
    <div class="fcard"><div class="fcard-icon">&#129518;</div><div class="fcard-title">Analysis Agent</div><div class="fcard-desc">Processes information, identifies patterns, and extracts meaningful actionable insights.</div></div>
    <div class="fcard"><div class="fcard-icon">&#9989;</div><div class="fcard-title">Verification Agent</div><div class="fcard-desc">Cross-checks facts and validates source credibility &#8212; every claim is trustworthy.</div></div>
    <div class="fcard"><div class="fcard-icon">&#128202;</div><div class="fcard-title">Report Agent</div><div class="fcard-desc">Builds structured, professional-quality reports with clear sections and summaries.</div></div>
    <div class="fcard"><div class="fcard-icon">&#9986;&#65039;</div><div class="fcard-title">Summarization Agent</div><div class="fcard-desc">Creates concise executive summaries and key takeaways for decision-makers.</div></div>
    <div class="fcard"><div class="fcard-icon">&#128228;</div><div class="fcard-title">Export System</div><div class="fcard-desc">Exports polished reports in PDF and professional formats, ready to share.</div></div>
  </div>
</section>""")

# ════ SECTION 5 — BENEFITS ════
H("""<section class="section" id="benefits">
  <div class="centered">
    <span class="section-tag">BENEFITS</span>
    <h2 class="section-title">Why Teams Choose ResearchMind</h2>
    <p class="section-sub">From solo researchers to enterprise teams &#8212; measurable advantages at every scale.</p>
  </div>
  <div class="bgrid">
    <div class="bcard"><div class="bcard-icon">&#9201;&#65039;</div><div><div class="bcard-title">Save Hours of Research</div><div class="bcard-desc">Automated pipelines compress days of manual research into minutes.</div></div></div>
    <div class="bcard"><div class="bcard-icon">&#127919;</div><div><div class="bcard-title">Improve Accuracy</div><div class="bcard-desc">Multi-agent verification catches errors single-pass research routinely misses.</div></div></div>
    <div class="bcard"><div class="bcard-icon">&#128221;</div><div><div class="bcard-title">Auto-Generate Reports</div><div class="bcard-desc">No formatting from scratch &#8212; ResearchMind delivers publish-ready output.</div></div></div>
    <div class="bcard"><div class="bcard-icon">&#128200;</div><div><div class="bcard-title">Scale Efficiently</div><div class="bcard-desc">Run multiple pipelines simultaneously without adding headcount.</div></div></div>
    <div class="bcard"><div class="bcard-icon">&#129302;</div><div><div class="bcard-title">AI Specialist Team</div><div class="bcard-desc">Each agent brings domain expertise &#8212; never left to a generalist alone.</div></div></div>
    <div class="bcard"><div class="bcard-icon">&#128194;</div><div><div class="bcard-title">Centralize Workflows</div><div class="bcard-desc">One platform for all research &#8212; no more juggling tabs and fragmented notes.</div></div></div>
  </div>
</section>""")

# ════ SECTION 6 — USE CASES ════
H("""<section class="section section-alt">
  <div class="centered">
    <span class="section-tag">USE CASES</span>
    <h2 class="section-title">Built For Modern Research</h2>
    <p class="section-sub">Academia, business, content creation &#8212; ResearchMind adapts to your workflow.</p>
  </div>
  <div class="ugrid">
    <div class="ucard"><div class="ucard-icon">&#127891;</div><div class="ucard-title">Academic Research</div><div class="ucard-desc">Comprehensive literature reviews and topic research with verified sources.</div></div>
    <div class="ucard"><div class="ucard-icon">&#128201;</div><div class="ucard-title">Business Intelligence</div><div class="ucard-desc">Analyze markets, competitors, and trends with AI-validated insights.</div></div>
    <div class="ucard"><div class="ucard-icon">&#9997;&#65039;</div><div class="ucard-title">Content Research</div><div class="ucard-desc">Gather verified information for articles, blog posts, and professional reports.</div></div>
    <div class="ucard"><div class="ucard-icon">&#9822;&#65039;</div><div class="ucard-title">Strategic Planning</div><div class="ucard-desc">Informed decisions backed by comprehensive, cross-validated research intelligence.</div></div>
  </div>
</section>""")

# ════ CTA + FOOTER ════
H(f"""<section class="cta-wrap" id="contact">
  <div class="cta-glow"></div>
  <span class="section-tag" style="justify-content:center;display:block;">GET STARTED</span>
  <h2 class="cta-title">Ready to Transform<br>Your Research?</h2>
  <p class="cta-sub">Join researchers, analysts, students, and professionals accelerating knowledge discovery with ResearchMind.</p>
  <a href="{auth_url}" class="btn-primary" style="display:inline-flex;margin:0 auto;font-size:.95rem;padding:.85rem 2.1rem;">
    &#128272; Continue with Google &#8212; It&#39;s Free
  </a>
</section>

<footer class="footer">
  <div class="footer-brand">ResearchMind</div>
  <div>&#169; 2025 ResearchMind &middot; AI-Powered Research Automation</div>
  <div style="font-family:var(--mono);font-size:.62rem;color:var(--muted);">LangChain + Streamlit</div>
</footer>""")