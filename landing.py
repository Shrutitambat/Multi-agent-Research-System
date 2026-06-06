"""
landing.py — ResearchMind Landing Page
Fixes applied:
  1. CSS injected inline (no file dependency)
  2. Auth URL built safely — no crash if secrets missing
  3. HTML split into small st.markdown() chunks (Streamlit limit fix)
  4. SVG icons replaced with emoji (no giant logo rendering)
  5. auth.py imported safely with try/except
"""

import streamlit as st

st.set_page_config(
    page_title="ResearchMind — AI Multi-Agent Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Auth ─────────────────────────────────────────────────────────────────────
auth_url = "#"

try:
    from auth import is_authenticated, handle_callback, get_auth_url

    # If already logged in → go directly to app
    if is_authenticated():
        st.switch_page("pages/app.py")

    # Google just redirected back with ?code= → exchange for tokens
    if handle_callback():
        st.switch_page("pages/app.py")

    # Build the Google login URL for buttons
    try:
        auth_url = get_auth_url()
    except Exception:
        auth_url = "#"
        st.warning("⚠️ Google OAuth not configured. Fill in `.streamlit/secrets.toml`.", icon="🔑")

except ImportError:
    pass

# ══════════════════════════════════════════════════════════════════════════════
#  INLINE CSS  (no file dependency — always works)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root{
  --bg:#040711; --surface:rgba(255,255,255,0.04); --border:rgba(255,255,255,0.08);
  --border-hi:rgba(120,100,255,0.4); --accent:#7b5cff; --accent2:#00c8ff;
  --text:#e8eaf6; --muted:#7b82a0; --success:#00e5b0;
  --display:'Bricolage Grotesque',sans-serif; --body:'DM Sans',sans-serif;
  --mono:'JetBrains Mono',monospace;
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"],.main,.block-container{
  background-color:var(--bg)!important; color:var(--text)!important;
  font-family:var(--body)!important;
}
#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"]{
  visibility:hidden!important; height:0!important;
}
.block-container{padding:0!important; max-width:100%!important;}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:rgba(123,92,255,.4);border-radius:3px;}

/* ── NAV ── */
.rm-nav{
  position:fixed;top:0;left:0;right:0;z-index:999;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 5vw; height:68px;
  background:rgba(4,7,17,.75); backdrop-filter:blur(18px) saturate(160%);
  border-bottom:1px solid var(--border);
}
.rm-logo{
  font-family:var(--display);font-size:1.4rem;font-weight:800;letter-spacing:-.04em;
  background:linear-gradient(90deg,#fff 30%,var(--accent));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.rm-logo span{color:var(--accent);-webkit-text-fill-color:var(--accent);}
.rm-nav-links{display:flex;gap:2.5rem;list-style:none;}
.rm-nav-links a{
  font-size:.88rem;font-weight:500;color:var(--muted);
  text-decoration:none;transition:color .2s;
}
.rm-nav-links a:hover{color:var(--text);}
.rm-btn-nav{
  display:inline-flex;align-items:center;gap:.5rem;
  background:linear-gradient(135deg,var(--accent),#4f3ecf);
  color:#fff;border:none;border-radius:8px;
  font-family:var(--body);font-size:.85rem;font-weight:600;
  padding:.55rem 1.3rem;cursor:pointer;text-decoration:none;
  box-shadow:0 4px 20px rgba(123,92,255,.3);
  transition:opacity .2s,transform .15s,box-shadow .2s;
}
.rm-btn-nav:hover{opacity:.88;transform:translateY(-1px);box-shadow:0 8px 28px rgba(123,92,255,.45);}

/* ── BUTTONS ── */
.rm-btn-primary{
  display:inline-flex;align-items:center;gap:.6rem;
  background:linear-gradient(135deg,var(--accent),#4f3ecf);
  color:#fff;border:none;border-radius:10px;
  font-family:var(--body);font-size:.95rem;font-weight:600;
  padding:.85rem 2rem;cursor:pointer;text-decoration:none;
  box-shadow:0 6px 30px rgba(123,92,255,.4);
  transition:transform .2s,box-shadow .2s;
}
.rm-btn-primary:hover{transform:translateY(-2px);box-shadow:0 12px 40px rgba(123,92,255,.55);}
.rm-btn-secondary{
  display:inline-flex;align-items:center;gap:.5rem;
  background:transparent;color:var(--text);
  border:1px solid var(--border-hi);border-radius:10px;
  font-family:var(--body);font-size:.95rem;font-weight:500;
  padding:.85rem 2rem;cursor:pointer;text-decoration:none;
  transition:background .2s,border-color .2s,transform .15s;
}
.rm-btn-secondary:hover{background:rgba(123,92,255,.08);border-color:var(--accent);transform:translateY(-1px);}

/* ── HERO ── */
.rm-hero{
  min-height:100vh;display:flex;align-items:center;
  padding:100px 5vw 80px;position:relative;overflow:hidden;
}
.rm-hero-bg{
  position:absolute;inset:0;pointer-events:none;z-index:0;
  background:
    radial-gradient(ellipse 80% 60% at 60% 40%,rgba(123,92,255,.13) 0%,transparent 70%),
    radial-gradient(ellipse 50% 50% at 20% 80%,rgba(0,200,255,.07) 0%,transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 10%,rgba(255,92,168,.05) 0%,transparent 60%);
}
.rm-hero-bg::after{
  content:'';position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);
  background-size:60px 60px;
  mask-image:radial-gradient(ellipse 80% 80% at 50% 50%,black 30%,transparent 80%);
}
.rm-hero-left{flex:1;position:relative;z-index:1;max-width:580px;}
.rm-hero-right{flex:1;position:relative;z-index:1;display:flex;justify-content:center;align-items:center;min-height:460px;}

.rm-badge{
  display:inline-flex;align-items:center;gap:.5rem;
  font-family:var(--mono);font-size:.68rem;letter-spacing:.15em;
  color:var(--accent2);border:1px solid rgba(0,200,255,.25);
  background:rgba(0,200,255,.06);border-radius:100px;
  padding:6px 14px;margin-bottom:1.5rem;
}
.rm-badge::before{content:'●';font-size:.45rem;animation:pdot 2s ease infinite;}
@keyframes pdot{0%,100%{opacity:1;}50%{opacity:.25;}}

.rm-hero h1{
  font-family:var(--display);
  font-size:clamp(2.6rem,5vw,3.8rem);
  font-weight:800;line-height:1.08;letter-spacing:-.04em;
  color:#fff;margin-bottom:1.4rem;
}
.rm-grad{
  background:linear-gradient(90deg,var(--accent),var(--accent2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.rm-hero-sub{
  font-size:1.02rem;line-height:1.75;color:var(--muted);
  margin-bottom:2.2rem;max-width:500px;
}
.rm-hero-btns{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:2.5rem;}

/* ── STATS ── */
.rm-stats{
  display:flex;gap:0;flex-wrap:wrap;
  border:1px solid var(--border);border-radius:14px;overflow:hidden;
}
.rm-stat{
  flex:1;min-width:120px;padding:1.5rem 1rem;
  border-right:1px solid var(--border);text-align:center;
}
.rm-stat:last-child{border-right:none;}
.rm-stat-val{
  font-family:var(--display);font-size:1.9rem;font-weight:800;
  letter-spacing:-.04em;
  background:linear-gradient(90deg,#fff,var(--accent));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.rm-stat-lbl{font-size:.72rem;color:var(--muted);margin-top:3px;font-family:var(--mono);}

/* ── AGENT DIAGRAM ── */
.rm-diagram{position:relative;width:400px;height:400px;}
.rm-orb{
  position:absolute;border-radius:50%;filter:blur(55px);pointer-events:none;
}
.rm-orb-1{width:320px;height:320px;background:rgba(123,92,255,.17);top:5%;left:0%;}
.rm-orb-2{width:200px;height:200px;background:rgba(0,200,255,.12);bottom:5%;right:5%;}
.rm-center{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:82px;height:82px;border-radius:50%;
  background:linear-gradient(135deg,var(--accent),#4f3ecf);
  box-shadow:0 0 48px rgba(123,92,255,.6),0 0 96px rgba(123,92,255,.25);
  display:flex;align-items:center;justify-content:center;
  font-size:1.9rem;z-index:3;
  animation:cpulse 3s ease-in-out infinite;
}
@keyframes cpulse{
  0%,100%{box-shadow:0 0 48px rgba(123,92,255,.6),0 0 96px rgba(123,92,255,.25);}
  50%{box-shadow:0 0 68px rgba(123,92,255,.8),0 0 120px rgba(123,92,255,.4);}
}
.rm-ring{
  position:absolute;top:50%;left:50%;border-radius:50%;
  border:1px dashed rgba(255,255,255,.1);transform:translate(-50%,-50%);
}
.rm-ring-1{width:188px;height:188px;animation:rspin 12s linear infinite;}
.rm-ring-2{width:300px;height:300px;animation:rspin 20s linear infinite reverse;}
.rm-ring-3{width:390px;height:390px;animation:rspin 30s linear infinite;}
@keyframes rspin{from{transform:translate(-50%,-50%) rotate(0deg);}to{transform:translate(-50%,-50%) rotate(360deg);}}
.rm-node{
  position:absolute;width:52px;height:52px;border-radius:11px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-size:1.25rem;border:1px solid var(--border-hi);
  background:rgba(255,255,255,.05);backdrop-filter:blur(10px);
  box-shadow:0 4px 18px rgba(0,0,0,.4);z-index:4;
  transition:transform .3s;cursor:default;
}
.rm-node:hover{transform:scale(1.15);}
.rm-node span{font-family:var(--mono);font-size:.42rem;color:var(--muted);margin-top:1px;letter-spacing:.05em;}
.n-a{top:1%;left:43%;}
.n-b{top:23%;left:87%;}
.n-c{top:70%;left:84%;}
.n-d{top:86%;left:41%;}
.n-e{top:66%;left:0%;}
.n-f{top:20%;left:2%;}

.rm-dot{position:absolute;width:6px;height:6px;border-radius:50%;
  background:var(--accent2);box-shadow:0 0 8px var(--accent2);z-index:5;}
.rd1{animation:rf1 3s ease-in-out infinite;}
.rd2{animation:rf2 3.5s ease-in-out .8s infinite;}
.rd3{animation:rf3 2.8s ease-in-out 1.5s infinite;}
@keyframes rf1{0%{top:46%;left:50%;opacity:0;}20%{opacity:1;}100%{top:1%;left:46%;opacity:0;}}
@keyframes rf2{0%{top:50%;left:54%;opacity:0;}20%{opacity:1;}100%{top:24%;left:89%;opacity:0;}}
@keyframes rf3{0%{top:54%;left:48%;opacity:0;}20%{opacity:1;}100%{top:86%;left:43%;opacity:0;}}

/* ── SECTIONS ── */
.rm-section{padding:90px 5vw;position:relative;}
.rm-section-alt{background:rgba(255,255,255,.018);}
.rm-tag{
  font-family:var(--mono);font-size:.68rem;letter-spacing:.2em;
  text-transform:uppercase;color:var(--accent);
  margin-bottom:.7rem;display:block;
}
.rm-title{
  font-family:var(--display);font-size:clamp(1.8rem,3.5vw,2.7rem);
  font-weight:800;letter-spacing:-.03em;color:#fff;
  line-height:1.12;margin-bottom:.9rem;
}
.rm-sub{font-size:.98rem;line-height:1.75;color:var(--muted);max-width:600px;margin-bottom:3rem;}
.rm-center-text{text-align:center;}
.rm-center-text .rm-sub{margin-left:auto;margin-right:auto;}
.rm-two-col{display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:center;}

/* ── CARDS ── */
.rm-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:1.4rem;}
.rm-grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:1.2rem;}
.rm-card{
  background:var(--surface);border:1px solid var(--border);border-radius:15px;
  padding:1.8rem;position:relative;overflow:hidden;
  backdrop-filter:blur(12px);
  transition:border-color .3s,transform .3s,box-shadow .3s;
}
.rm-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--accent),transparent);
  opacity:0;transition:opacity .3s;
}
.rm-card:hover{
  border-color:var(--border-hi);transform:translateY(-4px);
  box-shadow:0 20px 50px rgba(0,0,0,.4),0 0 0 1px rgba(123,92,255,.1);
}
.rm-card:hover::before{opacity:1;}
.rm-card-icon{
  width:46px;height:46px;border-radius:11px;
  display:flex;align-items:center;justify-content:center;
  font-size:1.3rem;margin-bottom:1.1rem;
  background:linear-gradient(135deg,rgba(123,92,255,.2),rgba(0,200,255,.1));
  border:1px solid rgba(123,92,255,.2);
}
.rm-card-title{font-family:var(--display);font-size:1rem;font-weight:700;color:#fff;margin-bottom:.5rem;letter-spacing:-.02em;}
.rm-card-desc{font-size:.85rem;line-height:1.65;color:var(--muted);}

/* ── BENEFIT CARDS ── */
.rm-bcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1.2rem;}
.rm-bcard{
  background:var(--surface);border:1px solid var(--border);border-radius:13px;
  padding:1.4rem 1.6rem;display:flex;align-items:flex-start;gap:1rem;
  backdrop-filter:blur(10px);transition:border-color .25s,transform .25s;
}
.rm-bcard:hover{border-color:var(--border-hi);transform:translateY(-3px);}
.rm-bcard-icon{font-size:1.35rem;flex-shrink:0;margin-top:2px;}
.rm-bcard h4{font-family:var(--display);font-size:.93rem;font-weight:700;color:#fff;margin-bottom:.3rem;letter-spacing:-.02em;}
.rm-bcard p{font-size:.8rem;line-height:1.6;color:var(--muted);}

/* ── WORKFLOW ── */
.rm-workflow{display:flex;flex-direction:column;max-width:680px;margin:0 auto;}
.rm-step{display:flex;gap:1.5rem;align-items:flex-start;padding:1.4rem 0;position:relative;}
.rm-step-line{position:absolute;left:23px;top:56px;bottom:-10px;width:2px;background:linear-gradient(to bottom,var(--accent),transparent);}
.rm-step:last-child .rm-step-line{display:none;}
.rm-step-num{
  width:48px;height:48px;border-radius:11px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-family:var(--mono);font-size:.82rem;font-weight:600;
  background:linear-gradient(135deg,var(--accent),#4f3ecf);
  box-shadow:0 4px 18px rgba(123,92,255,.35);color:#fff;position:relative;z-index:1;
}
.rm-step h4{font-family:var(--display);font-size:1rem;font-weight:700;color:#fff;margin-bottom:.35rem;letter-spacing:-.02em;}
.rm-step p{font-size:.86rem;line-height:1.65;color:var(--muted);}
.rm-step-body{padding-top:.4rem;}

/* ── USE CASES ── */
.rm-ucards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1.4rem;}
.rm-ucard{
  background:var(--surface);border:1px solid var(--border);border-radius:15px;
  padding:1.8rem 1.6rem;position:relative;overflow:hidden;
  backdrop-filter:blur(10px);transition:border-color .3s,transform .3s;
}
.rm-ucard::after{
  content:'';position:absolute;bottom:-30px;right:-30px;
  width:100px;height:100px;border-radius:50%;
  background:radial-gradient(circle,rgba(123,92,255,.12),transparent 70%);
  pointer-events:none;
}
.rm-ucard:hover{border-color:var(--border-hi);transform:translateY(-4px);}
.rm-ucard-icon{font-size:1.8rem;margin-bottom:.9rem;}
.rm-ucard h4{font-family:var(--display);font-size:.98rem;font-weight:700;color:#fff;margin-bottom:.45rem;letter-spacing:-.02em;}
.rm-ucard p{font-size:.83rem;line-height:1.65;color:var(--muted);}

/* ── CTA ── */
.rm-cta{
  padding:110px 5vw;text-align:center;position:relative;overflow:hidden;
}
.rm-cta-bg{
  position:absolute;inset:0;z-index:0;pointer-events:none;
  background:
    radial-gradient(ellipse 70% 70% at 50% 50%,rgba(123,92,255,.12) 0%,transparent 70%),
    radial-gradient(ellipse 40% 50% at 20% 30%,rgba(0,200,255,.07) 0%,transparent 60%);
}
.rm-cta>*{position:relative;z-index:1;}
.rm-cta h2{
  font-family:var(--display);font-size:clamp(2rem,4vw,3.1rem);
  font-weight:800;letter-spacing:-.04em;color:#fff;
  line-height:1.1;margin-bottom:1.2rem;
}
.rm-cta>p{font-size:1rem;line-height:1.75;color:var(--muted);max-width:500px;margin:0 auto 2.4rem;}
.rm-cta-btns{display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;}

/* ── FOOTER ── */
.rm-footer{
  padding:1.8rem 5vw;border-top:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  font-size:.78rem;color:var(--muted);flex-wrap:wrap;gap:1rem;
}
.rm-footer-logo{
  font-family:var(--display);font-weight:700;font-size:.95rem;
  background:linear-gradient(90deg,#fff 30%,var(--accent));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}

/* ── PARTICLES ── */
.rm-particles{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden;}
.rm-particle{
  position:absolute;border-radius:50%;background:var(--accent);opacity:.15;
  animation:pfloat linear infinite;
}
@keyframes pfloat{
  0%{transform:translateY(100vh) scale(0);opacity:0;}
  10%{opacity:.15;}90%{opacity:.15;}100%{transform:translateY(-10vh) scale(1);opacity:0;}
}

/* ── ANIMATIONS ── */
@keyframes fade-up{from{opacity:0;transform:translateY(22px);}to{opacity:1;transform:translateY(0);}}
.au1{animation:fade-up .6s ease both;}
.au2{animation:fade-up .6s .1s ease both;}
.au3{animation:fade-up .6s .2s ease both;}
.au4{animation:fade-up .6s .3s ease both;}
.au5{animation:fade-up .6s .4s ease both;}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a block of HTML safely ─────────────────────────────────────
def html(content: str):
    st.markdown(content, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PARTICLES + NAVBAR
# ══════════════════════════════════════════════════════════════════════════════
html(f"""
<div class="rm-particles" aria-hidden="true">
  <div class="rm-particle" style="width:4px;height:4px;left:10%;animation-duration:18s;animation-delay:0s;"></div>
  <div class="rm-particle" style="width:3px;height:3px;left:25%;animation-duration:22s;animation-delay:3s;"></div>
  <div class="rm-particle" style="width:5px;height:5px;left:45%;animation-duration:16s;animation-delay:6s;background:#00c8ff;"></div>
  <div class="rm-particle" style="width:3px;height:3px;left:65%;animation-duration:25s;animation-delay:1s;"></div>
  <div class="rm-particle" style="width:4px;height:4px;left:82%;animation-duration:20s;animation-delay:8s;"></div>
</div>

<nav class="rm-nav">
  <div class="rm-logo">Research<span>Mind</span></div>
  <ul class="rm-nav-links">
    <li><a href="#features">Features</a></li>
    <li><a href="#workflow">Workflow</a></li>
    <li><a href="#benefits">Benefits</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
  <a href="{auth_url}" class="rm-btn-nav">🔐 Sign in with Google</a>
</nav>
""")

# ══════════════════════════════════════════════════════════════════════════════
#  HERO — left side
# ══════════════════════════════════════════════════════════════════════════════
html(f"""
<section class="rm-hero" id="home">
  <div class="rm-hero-bg"></div>
  <div class="rm-hero-left">
    <div class="rm-badge au1">MULTI-AGENT AI RESEARCH PLATFORM</div>
    <h1 class="au2">
      AI-Powered<br>
      <span class="rm-grad">Multi-Agent</span><br>
      Research Platform
    </h1>
    <p class="rm-hero-sub au3">
      ResearchMind automates complex research workflows using multiple AI agents
      working together. Collect insights, validate sources, analyze information,
      and generate professional reports in minutes instead of hours.
    </p>
    <div class="rm-hero-btns au4">
      <a href="{auth_url}" class="rm-btn-primary">🔐 Continue with Google</a>
      <a href="#features" class="rm-btn-secondary">Explore Features ↓</a>
    </div>
    <div class="rm-stats au5">
      <div class="rm-stat">
        <div class="rm-stat-val">4×</div>
        <div class="rm-stat-lbl">Faster Research</div>
      </div>
      <div class="rm-stat">
        <div class="rm-stat-val">6</div>
        <div class="rm-stat-lbl">AI Agents</div>
      </div>
      <div class="rm-stat">
        <div class="rm-stat-val">99%</div>
        <div class="rm-stat-lbl">Source Accuracy</div>
      </div>
      <div class="rm-stat">
        <div class="rm-stat-val">∞</div>
        <div class="rm-stat-lbl">Topics</div>
      </div>
    </div>
  </div>
""")

# ── Hero — right side (agent diagram) — separate chunk ───────────────────────
html("""
  <div class="rm-hero-right">
    <div class="rm-orb rm-orb-1"></div>
    <div class="rm-orb rm-orb-2"></div>
    <div class="rm-diagram">
      <div class="rm-ring rm-ring-1"></div>
      <div class="rm-ring rm-ring-2"></div>
      <div class="rm-ring rm-ring-3"></div>
      <div class="rm-center">🔬</div>
      <div class="rm-node n-a">🔍<span>SEARCH</span></div>
      <div class="rm-node n-b">📄<span>READER</span></div>
      <div class="rm-node n-c">🧮<span>ANALYST</span></div>
      <div class="rm-node n-d">📊<span>REPORT</span></div>
      <div class="rm-node n-e">✅<span>VERIFY</span></div>
      <div class="rm-node n-f">✍️<span>WRITER</span></div>
      <div class="rm-dot rd1"></div>
      <div class="rm-dot rd2"></div>
      <div class="rm-dot rd3"></div>
    </div>
  </div>
</section>
""")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — WHY RESEARCHMIND
# ══════════════════════════════════════════════════════════════════════════════
html("""
<section class="rm-section rm-section-alt" id="features">
  <div class="rm-two-col">
    <div>
      <span class="rm-tag">WHY RESEARCHMIND</span>
      <h2 class="rm-title">Professional AI Research Automation</h2>
      <p class="rm-sub" style="margin-bottom:0;">
        ResearchMind uses a multi-agent architecture where specialized AI agents
        collaborate to conduct research, validate information, analyze findings,
        and produce comprehensive research reports. No more manual hours —
        let agents do the heavy lifting.
      </p>
    </div>
    <div class="rm-grid-2">
      <div class="rm-card"><div class="rm-card-icon">🤝</div><div class="rm-card-title">Multi-Agent Collaboration</div><div class="rm-card-desc">Specialized agents work in parallel, each handling a distinct part of the research pipeline.</div></div>
      <div class="rm-card"><div class="rm-card-icon">⚡</div><div class="rm-card-title">Real-Time Research</div><div class="rm-card-desc">Live web search and scraping delivers up-to-date, relevant information instantly.</div></div>
      <div class="rm-card"><div class="rm-card-icon">📝</div><div class="rm-card-title">Automated Reports</div><div class="rm-card-desc">Structured, professional reports generated automatically from validated insights.</div></div>
      <div class="rm-card"><div class="rm-card-icon">🛡️</div><div class="rm-card-title">Source Verification</div><div class="rm-card-desc">Every source is cross-checked for credibility before inclusion in the final report.</div></div>
      <div class="rm-card"><div class="rm-card-icon">🧠</div><div class="rm-card-title">Intelligent Summarization</div><div class="rm-card-desc">Key insights distilled into concise executive summaries for quick decision-making.</div></div>
      <div class="rm-card"><div class="rm-card-icon">📤</div><div class="rm-card-title">Export to PDF</div><div class="rm-card-desc">Download polished, shareable reports in PDF and plain text with one click.</div></div>
    </div>
  </div>
</section>
""")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — WORKFLOW
# ══════════════════════════════════════════════════════════════════════════════
html("""
<section class="rm-section" id="workflow">
  <div class="rm-center-text">
    <span class="rm-tag">HOW IT WORKS</span>
    <h2 class="rm-title">How ResearchMind Works</h2>
    <p class="rm-sub">Five streamlined stages take you from a raw topic to a polished, validated research report.</p>
  </div>
  <div class="rm-workflow">
    <div class="rm-step">
      <div class="rm-step-line"></div>
      <div class="rm-step-num">01</div>
      <div class="rm-step-body"><h4>Enter Research Topic</h4><p>Provide a topic, question, or area of investigation. ResearchMind handles everything from there.</p></div>
    </div>
    <div class="rm-step">
      <div class="rm-step-line"></div>
      <div class="rm-step-num">02</div>
      <div class="rm-step-body"><h4>AI Agents Collect Information</h4><p>Specialized agents gather information from multiple web sources simultaneously, scraping the most relevant URLs for deep content.</p></div>
    </div>
    <div class="rm-step">
      <div class="rm-step-line"></div>
      <div class="rm-step-num">03</div>
      <div class="rm-step-body"><h4>Validation &amp; Analysis</h4><p>Research findings are verified, filtered, and analyzed. Only credible, relevant content advances to the report stage.</p></div>
    </div>
    <div class="rm-step">
      <div class="rm-step-line"></div>
      <div class="rm-step-num">04</div>
      <div class="rm-step-body"><h4>Report Generation</h4><p>Writer and Critic agents collaborate to produce a structured, professionally written report with expert feedback.</p></div>
    </div>
    <div class="rm-step">
      <div class="rm-step-num">05</div>
      <div class="rm-step-body"><h4>Export &amp; Share</h4><p>Download professional reports in PDF or text format and share results with your team instantly.</p></div>
    </div>
  </div>
</section>
""")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — AGENT CARDS
# ══════════════════════════════════════════════════════════════════════════════
html("""
<section class="rm-section rm-section-alt">
  <div class="rm-center-text">
    <span class="rm-tag">AGENT ARCHITECTURE</span>
    <h2 class="rm-title">Six Specialized AI Agents</h2>
    <p class="rm-sub">Each agent is purpose-built for a specific stage, working in concert to deliver results no single model could achieve alone.</p>
  </div>
  <div class="rm-grid">
    <div class="rm-card"><div class="rm-card-icon">🔍</div><div class="rm-card-title">Research Agent</div><div class="rm-card-desc">Performs deep web research and information gathering from diverse, authoritative sources across the internet.</div></div>
    <div class="rm-card"><div class="rm-card-icon">🧮</div><div class="rm-card-title">Analysis Agent</div><div class="rm-card-desc">Processes collected information, identifies patterns, and extracts meaningful, actionable insights.</div></div>
    <div class="rm-card"><div class="rm-card-icon">✅</div><div class="rm-card-title">Verification Agent</div><div class="rm-card-desc">Cross-checks facts and validates source credibility to ensure every claim is trustworthy.</div></div>
    <div class="rm-card"><div class="rm-card-icon">📊</div><div class="rm-card-title">Report Agent</div><div class="rm-card-desc">Builds structured, professional-quality research reports with clear sections, citations, and summaries.</div></div>
    <div class="rm-card"><div class="rm-card-icon">✂️</div><div class="rm-card-title">Summarization Agent</div><div class="rm-card-desc">Creates concise executive summaries and key takeaways tailored for decision-makers.</div></div>
    <div class="rm-card"><div class="rm-card-icon">📤</div><div class="rm-card-title">Export System</div><div class="rm-card-desc">Exports polished reports in PDF and other professional formats, ready to share with stakeholders.</div></div>
  </div>
</section>
""")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — BENEFITS
# ══════════════════════════════════════════════════════════════════════════════
html("""
<section class="rm-section" id="benefits">
  <div class="rm-center-text">
    <span class="rm-tag">BENEFITS</span>
    <h2 class="rm-title">Why Teams Choose ResearchMind</h2>
    <p class="rm-sub">From solo researchers to enterprise teams, ResearchMind delivers measurable advantages at every scale.</p>
  </div>
  <div class="rm-bcards">
    <div class="rm-bcard"><div class="rm-bcard-icon">⏱️</div><div><h4>Save Hours of Research Time</h4><p>Automated pipelines compress days of manual research into minutes, freeing your team for higher-value work.</p></div></div>
    <div class="rm-bcard"><div class="rm-bcard-icon">🎯</div><div><h4>Improve Information Accuracy</h4><p>Multi-agent verification catches errors and biases that single-pass research routinely misses.</p></div></div>
    <div class="rm-bcard"><div class="rm-bcard-icon">📝</div><div><h4>Generate Reports Automatically</h4><p>No more formatting or writing from scratch — ResearchMind delivers publish-ready reports.</p></div></div>
    <div class="rm-bcard"><div class="rm-bcard-icon">📈</div><div><h4>Scale Research Efficiently</h4><p>Run multiple research pipelines simultaneously without adding headcount or infrastructure.</p></div></div>
    <div class="rm-bcard"><div class="rm-bcard-icon">🤖</div><div><h4>Collaborate with AI Specialists</h4><p>Each agent brings domain-specific expertise — your research is never left to a generalist alone.</p></div></div>
    <div class="rm-bcard"><div class="rm-bcard-icon">🗂️</div><div><h4>Centralize Research Workflows</h4><p>One platform for all your research — no more juggling tabs, docs, and fragmented notes.</p></div></div>
  </div>
</section>
""")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — USE CASES
# ══════════════════════════════════════════════════════════════════════════════
html("""
<section class="rm-section rm-section-alt">
  <div class="rm-center-text">
    <span class="rm-tag">USE CASES</span>
    <h2 class="rm-title">Built For Modern Research</h2>
    <p class="rm-sub">Whether you're in academia, business, or content creation — ResearchMind adapts to your workflow.</p>
  </div>
  <div class="rm-ucards">
    <div class="rm-ucard"><div class="rm-ucard-icon">🎓</div><h4>Academic Research</h4><p>Conduct comprehensive literature reviews and topic research with verified academic and web sources.</p></div>
    <div class="rm-ucard"><div class="rm-ucard-icon">📉</div><h4>Business Intelligence</h4><p>Analyze markets, competitors, and industry trends with up-to-date, AI-validated insights.</p></div>
    <div class="rm-ucard"><div class="rm-ucard-icon">✍️</div><h4>Content Research</h4><p>Gather verified, well-structured information for articles, blog posts, and professional reports.</p></div>
    <div class="rm-ucard"><div class="rm-ucard-icon">♟️</div><h4>Strategic Planning</h4><p>Make informed strategic decisions backed by comprehensive, cross-validated research intelligence.</p></div>
  </div>
</section>
""")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 7 — CTA + FOOTER
# ══════════════════════════════════════════════════════════════════════════════
html(f"""
<section class="rm-cta" id="contact">
  <div class="rm-cta-bg"></div>
  <h2>Ready to Transform<br>Your Research Process?</h2>
  <p>Join researchers, analysts, students, and professionals using ResearchMind
     to accelerate knowledge discovery and generate insights at unprecedented speed.</p>
  <div class="rm-cta-btns">
    <a href="{auth_url}" class="rm-btn-primary" style="font-size:1.05rem;padding:.95rem 2.2rem;">
      🔐 Continue with Google — It's Free
    </a>
  </div>
</section>

<footer class="rm-footer">
  <div class="rm-footer-logo">ResearchMind</div>
  <div>© 2025 ResearchMind. AI-Powered Research Automation.</div>
  <div style="font-family:var(--mono);font-size:.7rem;color:var(--muted);">
    Built with LangChain + Streamlit
  </div>
</footer>
""")