<script>
import { onMount, createEventDispatcher } from 'svelte';
const dispatch = createEventDispatcher();

function closeLanding() {
    dispatch('close');
}

onMount(() => {
    /* ─── STARS ─────────────────────────────────────────────── */
    const starsEl = document.getElementById('stars');
    if (starsEl) {
        for (let i = 0; i < 130; i++) {
            const s = document.createElement('div');
            const sz = Math.random() * 1.8 + .4;
            s.className = 'star';
            Object.assign(s.style, {
                left: Math.random() * 100 + '%',
                top: Math.random() * 100 + '%',
                width: sz + 'px', height: sz + 'px',
                '--dur': (2.5 + Math.random() * 4) + 's',
                '--lo': (0.04 + Math.random() * .1) + '',
                '--hi': (0.35 + Math.random() * .55) + '',
                animationDelay: (Math.random() * 6) + 's',
            });
            starsEl.appendChild(s);
        }
    }

    /* ─── MODEL DATA ─────────────────────────────────────────── */
    const OUTER = [
        { name: 'GPT-4o', letters: 'GP', color: '#10a37f', bg: 'rgba(16,163,127,.15)' },
        { name: 'Claude 4', letters: 'CL', color: '#e8722a', bg: 'rgba(232,114,42,.15)' },
        { name: 'Gemini Pro', letters: 'GM', color: '#4285f4', bg: 'rgba(66,133,244,.15)' },
        { name: 'DeepSeek', letters: 'DS', color: '#7c3aed', bg: 'rgba(124,58,237,.15)' },
        { name: 'Llama 4', letters: 'LL', color: '#0ea5e9', bg: 'rgba(14,165,233,.15)' },
        { name: 'Qwen3', letters: 'QW', color: '#f43f5e', bg: 'rgba(244,63,94,.15)' },
        { name: 'Grok 3', letters: 'GK', color: '#cbd5e1', bg: 'rgba(203,213,225,.12)' },
        { name: 'Mistral', letters: 'MS', color: '#f97316', bg: 'rgba(249,115,22,.15)' },
        { name: 'DALL·E 3', letters: 'DA', color: '#a78bfa', bg: 'rgba(167,139,250,.15)' },
        { name: 'Midjourney', letters: 'MJ', color: '#fbbf24', bg: 'rgba(251,191,36,.15)' },
        { name: 'Flux Pro', letters: 'FX', color: '#34d399', bg: 'rgba(52,211,153,.15)' },
        { name: 'Perplexity', letters: 'PX', color: '#22d3ee', bg: 'rgba(34,211,238,.15)' },
    ];
    const INNER = [
        { name: 'o3', letters: 'O3', color: '#10a37f', bg: 'rgba(16,163,127,.15)' },
        { name: 'Sonnet 4.6', letters: 'SN', color: '#e8722a', bg: 'rgba(232,114,42,.15)' },
        { name: 'Flash 2.5', letters: 'FL', color: '#4285f4', bg: 'rgba(66,133,244,.15)' },
        { name: 'DS V3', letters: 'DV', color: '#7c3aed', bg: 'rgba(124,58,237,.15)' },
        { name: 'Llama 3.3', letters: 'L3', color: '#0ea5e9', bg: 'rgba(14,165,233,.15)' },
        { name: 'Runway', letters: 'RW', color: '#ec4899', bg: 'rgba(236,72,153,.15)' },
        { name: 'SD 3.5', letters: 'SD', color: '#8b5cf6', bg: 'rgba(139,92,246,.15)' },
        { name: 'Qwen 2.5', letters: 'Q2', color: '#f43f5e', bg: 'rgba(244,63,94,.15)' },
    ];

    /* ─── BUILD ITEMS ────────────────────────────────────────── */
    const scene = document.getElementById('scene');
    if (!scene) return;

    function makeItems(list, size) {
        return list.map(m => {
            const wrap = document.createElement('div');
            wrap.className = 'model-item';
            wrap.title = m.name;

            const icon = document.createElement('div');
            icon.className = 'model-icon';
            Object.assign(icon.style, {
                width: size + 'px', height: size + 'px',
                borderRadius: Math.round(size * .27) + 'px',
                background: m.bg,
                borderColor: m.color + '44',
                color: m.color,
                fontSize: Math.round(size * .28) + 'px',
            });
            icon.textContent = m.letters;

            const lbl = document.createElement('div');
            lbl.className = 'model-label';
            lbl.textContent = m.name;
            lbl.style.fontSize = Math.round(size * .135) + 'px';

            wrap.appendChild(icon);
            wrap.appendChild(lbl);
            scene.appendChild(wrap);
            return { el: wrap, m };
        });
    }

    const outerItems = makeItems(OUTER, 52);
    const innerItems = makeItems(INNER, 38);

    /* ─── ORBITAL ANIMATION ──────────────────────────────────── */
    let aO = 0, aI = Math.PI * .4; // start offset
    const R_OUT = 292, R_IN = 198;
    let animationId;

    function animate() {
        aO += .004;
        aI -= .006;

        outerItems.forEach(({ el }, i) => {
            const n = outerItems.length;
            const a = (2 * Math.PI / n) * i + aO;
            const x = Math.cos(a) * R_OUT, y = Math.sin(a) * R_OUT;
            const depth = (Math.sin(a) + 1) * .5; // 0=back 1=front
            el.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
            el.style.opacity = .38 + depth * .62;
            el.style.zIndex = Math.round(depth * 9) + 1;
            el.querySelector('.model-icon').style.transform = `scale(${.88 + depth * .14})`;
        });

        innerItems.forEach(({ el }, i) => {
            const n = innerItems.length;
            const a = (2 * Math.PI / n) * i + aI;
            const x = Math.cos(a) * R_IN, y = Math.sin(a) * R_IN;
            const depth = (Math.sin(a) + 1) * .5;
            el.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
            el.style.opacity = .3 + depth * .6;
            el.style.zIndex = Math.round(depth * 9) + 1;
        });

        animationId = requestAnimationFrame(animate);
    }
    animate();

    /* ─── TICKER ─────────────────────────────────────────────── */
    const tickerEl = document.getElementById('ticker');
    if (tickerEl) {
        const names = ['GPT-4o', 'Claude Opus 4.8', 'Gemini 2.5 Pro', 'DeepSeek R2', 'Llama 4 Scout',
            'Qwen3-235B', 'Grok 3', 'Mistral Large', 'DALL·E 3', 'Midjourney', 'Flux Pro', 'Perplexity'];
        [...names, ...names].forEach(n => {
            const el = document.createElement('span');
            el.className = 't-item';
            el.innerHTML = `<span class="t-sep">✦</span>${n}`;
            tickerEl.appendChild(el);
        });
    }

    return () => {
        cancelAnimationFrame(animationId);
    };
});
</script>

<svelte:head>
  <link rel="stylesheet" href="/landing.css" />
</svelte:head>

<div class="landing-page-wrapper">
  <!-- ─── NAV ─────────────────────────────────────────────────────── -->
  <nav>
    <div class="nav-inner glass">
      <a href="/" class="logo">
        <img src="/lingrai-logo.png" alt="Lingrai logo"
             onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="logo-fallback" style="display:none">L</div>
        Lingrai
      </a>
      <ul class="nav-links">
        <li><a href="/" class="active">首页</a></li>
        <li><a href="#features">控制台</a></li>
        <li><a href="#models">模型广场</a></li>
        <li><a href="#pricing">代理加盟</a></li>
        <li><a href="#contact">联系我们</a></li>
      </ul>
      <div class="nav-right">
        <button on:click={closeLanding} class="btn btn-ghost">登录</button>
        <button on:click={closeLanding} class="btn btn-solid glass">注册</button>
      </div>
    </div>
  </nav>

  <!-- ─── HERO ─────────────────────────────────────────────────────── -->
  <section class="hero">
    <video class="hero-video" autoplay loop muted playsinline>
      <source src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260314_131748_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4" type="video/mp4">
    </video>
    <div class="hero-overlay"></div>
    <div id="stars"></div>

    <div class="scene-wrap">
      <div class="orbital-scene" id="scene">
        <!-- Ring guides -->
        <div class="ring-guide" style="width:630px;height:630px;animation-delay:0s"></div>
        <div class="ring-guide" style="width:440px;height:440px;animation-delay:1.6s"></div>
        <div class="ring-guide" style="width:240px;height:240px;animation-delay:3.2s;border-color:rgba(255,255,255,.06)"></div>
        <div class="core-glow"></div>

        <!-- Center text -->
        <div class="orbit-center">
          <div class="eyebrow fr">500+ Models · One Gateway</div>
          <h1 class="hero-h1 fr1">
            One key,<br>
            <em>every intelligent</em><br>
            mind.
          </h1>
          <p class="hero-sub fr2">
            一个统一接口，接入全球所有主流 AI 大模型。<br>
            按量付费，无限并发，即充即用。
          </p>
          <button on:click={closeLanding} class="btn btn-solid hero-cta glass fr3">立即接入 →</button>
        </div>
      </div>
    </div>
  </section>

  <!-- ─── TICKER ────────────────────────────────────────────────────── -->
  <div class="ticker-wrap">
    <div class="ticker" id="ticker"></div>
  </div>

  <!-- ─── STATS ─────────────────────────────────────────────────────── -->
  <div style="padding:60px 5%">
    <div class="stats-row">
      <div class="stat-cell"><div class="stat-n">500+</div><div class="stat-d">已接入大模型</div></div>
      <div class="stat-cell"><div class="stat-n">40万+</div><div class="stat-d">全球服务用户</div></div>
      <div class="stat-cell"><div class="stat-n">70+</div><div class="stat-d">授权代理商</div></div>
      <div class="stat-cell"><div class="stat-n">99.9%</div><div class="stat-d">服务可用性</div></div>
      <div class="stat-cell"><div class="stat-n">3年+</div><div class="stat-d">稳定运营</div></div>
    </div>
  </div>

  <!-- ─── FEATURES ──────────────────────────────────────────────────── -->
  <section id="features" class="section" style="padding-top:20px">
    <div class="section-header">
      <h2>为什么选择 Lingrai</h2>
      <p>企业级 AI 接入基础设施，驱动真实业务增长</p>
    </div>
    <div class="feat-grid">
      <div class="feat-card">
        <div class="feat-ic">🔌</div>
        <h3>官方企业级通道</h3>
        <p>三年稳定运营护航，全球多点部署，持续为 40 万+ 用户提供高可用服务。</p>
      </div>
      <div class="feat-card">
        <div class="feat-ic">⚡</div>
        <h3>OpenAI 协议兼容</h3>
        <p>完全兼容 OpenAI API，无缝对接所有主流 AI 工具，零改造成本即可接入 500+ 模型。</p>
      </div>
      <div class="feat-card">
        <div class="feat-ic">💳</div>
        <h3>弹性按量计费</h3>
        <p>无额度过期限制，智能负载均衡不限速，按 Token 精确计量，资源按需使用。</p>
      </div>
      <div class="feat-card">
        <div class="feat-ic">🌐</div>
        <h3>全球加速节点</h3>
        <p>多地域服务器集群，自动就近路由，全球用户均可享受毫秒级低延迟响应。</p>
      </div>
      <div class="feat-card">
        <div class="feat-ic">🛡️</div>
        <h3>7×24 运维保障</h3>
        <p>全天候实时监控，故障快速定位与恢复，SLA 保障您的业务永续在线。</p>
      </div>
      <div class="feat-card">
        <div class="feat-ic">📊</div>
        <h3>透明计费体系</h3>
        <p>与官方倍率同步，公开透明无隐藏，已有 70+ 代理商选择 Lingrai 作为源头合作伙伴。</p>
      </div>
    </div>
  </section>

  <!-- ─── MODELS ────────────────────────────────────────────────────── -->
  <section id="models" class="section models-section">
    <div class="section-header">
      <h2>模型广场</h2>
      <p>一站式接入主流 AI 大模型，紧跟前沿能力同步更新</p>
    </div>
    <div class="model-tags">
      <div class="model-tag"><span class="dot" style="background:#10a37f"></span>GPT-4o</div>
      <div class="model-tag"><span class="dot" style="background:#10a37f"></span>GPT-4.1</div>
      <div class="model-tag"><span class="dot" style="background:#10a37f"></span>o3</div>
      <div class="model-tag"><span class="dot" style="background:#e8722a"></span>Claude Opus 4.8</div>
      <div class="model-tag"><span class="dot" style="background:#e8722a"></span>Claude Sonnet 4.6</div>
      <div class="model-tag"><span class="dot" style="background:#4285f4"></span>Gemini 2.5 Pro</div>
      <div class="model-tag"><span class="dot" style="background:#4285f4"></span>Gemini 2.5 Flash</div>
      <div class="model-tag"><span class="dot" style="background:#7c3aed"></span>DeepSeek R2</div>
      <div class="model-tag"><span class="dot" style="background:#7c3aed"></span>DeepSeek V3</div>
      <div class="model-tag"><span class="dot" style="background:#0ea5e9"></span>Llama 4 Scout</div>
      <div class="model-tag"><span class="dot" style="background:#dc2626"></span>Qwen3-235B</div>
      <div class="model-tag"><span class="dot" style="background:#dc2626"></span>Qwen2.5</div>
      <div class="model-tag"><span class="dot" style="background:#e2e8f0"></span>Grok 3</div>
      <div class="model-tag"><span class="dot" style="background:#f97316"></span>Mistral Large</div>
      <div class="model-tag"><span class="dot" style="background:#a78bfa"></span>DALL·E 3</div>
      <div class="model-tag"><span class="dot" style="background:#fbbf24"></span>Midjourney</div>
      <div class="model-tag"><span class="dot" style="background:#34d399"></span>Flux Pro</div>
      <div class="model-tag"><span class="dot" style="background:#ec4899"></span>Runway Gen-4</div>
      <div class="model-tag"><span class="dot" style="background:#22d3ee"></span>Perplexity</div>
      <div class="model-tag"><span class="dot" style="background:#64748b"></span>500+ 更多…</div>
    </div>
  </section>

  <!-- ─── CODE ──────────────────────────────────────────────────────── -->
  <section class="section code-section">
    <div class="section-header">
      <h2>三行代码，接入一切</h2>
      <p>完全兼容 OpenAI SDK，仅需替换 base_url 即可访问 500+ 模型</p>
    </div>
    <div class="code-box">
      <div class="code-bar">
        <div class="cd cd-r"></div><div class="cd cd-y"></div><div class="cd cd-g"></div>
        <span class="code-fn">quickstart.py — Lingrai API</span>
      </div>
      <div class="code-body"><span class="cc"># pip install openai</span>
<span class="ck">from</span> <span class="cv">openai</span> <span class="ck">import</span> <span class="cv">OpenAI</span>

<span class="cv">client</span> = <span class="cv">OpenAI</span>(
    <span class="cv">base_url</span>=<span class="cs">"https://api.lingrai.ai/v1"</span>,
    <span class="cv">api_key</span>=<span class="cs">"sk-lingrai-your-key"</span>,
)

<span class="cv">response</span> = <span class="cv">client</span>.<span class="cfn">chat</span>.<span class="cfn">completions</span>.<span class="cfn">create</span>(
    <span class="cv">model</span>=<span class="cs">"gpt-4o"</span>,  <span class="cc"># swap to any of 500+ models</span>
    <span class="cv">messages</span>=[{<span class="cs">"role"</span>: <span class="cs">"user"</span>, <span class="cs">"content"</span>: <span class="cs">"Hello, Lingrai!"</span>}],
)

<span class="cfn">print</span>(<span class="cv">response</span>.<span class="cfn">choices</span>[<span class="cv">0</span>].<span class="cfn">message</span>.<span class="cfn">content</span>)</div>
    </div>
  </section>

  <!-- ─── PRICING ───────────────────────────────────────────────────── -->
  <section id="pricing" class="section">
    <div class="section-header">
      <h2>简单透明的定价</h2>
      <p>按量付费，无月租，无隐藏费用，充值即用</p>
    </div>
    <div class="price-grid">
      <div class="price-card">
        <h3>开发者版</h3>
        <div class="price-val">按量计费</div>
        <div class="price-sub-label">充多少用多少，永不过期</div>
        <ul class="price-list">
          <li><span class="chk">✓</span>500+ 模型全覆盖</li>
          <li><span class="chk">✓</span>OpenAI 协议兼容</li>
          <li><span class="chk">✓</span>实时 Token 计量</li>
          <li><span class="chk">✓</span>在线客服支持</li>
        </ul>
        <button on:click={closeLanding} class="btn btn-ghost" style="width:100%">立即注册</button>
      </div>
      <div class="price-card hot">
        <div class="hot-badge">最受欢迎</div>
        <h3>企业版</h3>
        <div class="price-val">官方同步倍率</div>
        <div class="price-sub-label">性价比最高的 API 源头</div>
        <ul class="price-list">
          <li><span class="chk">✓</span>全部开发者版功能</li>
          <li><span class="chk">✓</span>高并发不限速</li>
          <li><span class="chk">✓</span>专属客服通道</li>
          <li><span class="chk">✓</span>SLA 99.9% 保障</li>
          <li><span class="chk">✓</span>发票与合同支持</li>
        </ul>
        <button class="btn btn-solid" style="width:100%">联系我们</button>
      </div>
      <div class="price-card">
        <h3>代理加盟</h3>
        <div class="price-val">分润合作</div>
        <div class="price-sub-label">成为 Lingrai 授权代理商</div>
        <ul class="price-list">
          <li><span class="chk">✓</span>专属折扣价格</li>
          <li><span class="chk">✓</span>二级代理支持</li>
          <li><span class="chk">✓</span>专属管理控制台</li>
          <li><span class="chk">✓</span>优先技术响应</li>
        </ul>
        <button class="btn btn-ghost" style="width:100%">申请加盟</button>
      </div>
    </div>
  </section>

  <!-- ─── FOOTER ────────────────────────────────────────────────────── -->
  <footer>
    <div class="foot-grid">
      <div class="foot-brand">
        <a href="/" class="logo" style="font-size:1.3rem">
          <img src="/lingrai-logo.png" alt="Lingrai"
               onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
          <div class="logo-fallback" style="display:none">L</div>
          Lingrai
        </a>
        <p>致力于为开发者提供快速、便捷的 AI 模型接口调用服务，一站式集成全球几乎所有主流 AI 大模型。</p>
      </div>
      <div>
        <h4>产品</h4>
        <ul>
          <li><a href="/">首页</a></li>
          <li><a href="#models">模型广场</a></li>
          <li><a href="#features">控制台</a></li>
          <li><a href="#">API 文档</a></li>
        </ul>
      </div>
      <div>
        <h4>合作</h4>
        <ul>
          <li><a href="#pricing">代理加盟</a></li>
          <li><a href="#">企业合作</a></li>
          <li><a href="#">OpenClaw 部署</a></li>
        </ul>
      </div>
      <div>
        <h4>支持</h4>
        <ul>
          <li><a href="#contact">联系我们</a></li>
          <li><a href="#">服务条款</a></li>
          <li><a href="#">隐私政策</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">© 2026 Lingrai · All rights reserved · Powered by intelligence</div>
  </footer>
</div>

<style>
  .landing-page-wrapper {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      z-index: 1000;
      background: var(--bg, #020c16);
      color: var(--fg, #ffffff);
      font-family: var(--font-body, 'Inter', sans-serif);
      overflow-y: auto;
      overflow-x: hidden;
  }
</style>
