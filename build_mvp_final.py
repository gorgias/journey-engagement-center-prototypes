from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('file:///sandbox/journey-ec-gorgias/index.html')
    page.wait_for_selector('.app')

    removed = page.evaluate('''() => {
        const removed = [];
        document.querySelectorAll('.navItem').forEach(el => {
            const pg = el.dataset.page;
            if (['opportunities','intelligence','loyalty'].includes(pg)) { removed.push('nav:'+pg); el.remove(); }
        });
        document.querySelectorAll('#page-overview .card').forEach(card => {
            if (card.textContent.includes('How you compare')) { removed.push('overview-benchmark'); card.remove(); }
        });
        ['page-opportunities','page-intelligence','page-loyalty'].forEach(id => {
            const el = document.getElementById(id); if (el) { removed.push(id); el.remove(); }
        });
        document.querySelectorAll('#page-engagements .tabItem').forEach(el => {
            if (el.dataset.tab === 'scenarios') { removed.push('tab:scenarios'); el.remove(); }
        });
        document.querySelectorAll('#page-engagements .tabPanel').forEach(el => {
            if (el.dataset.panelFor === 'scenarios') { removed.push('panel:scenarios'); el.remove(); }
        });
        const acePanel = document.querySelector('#page-engagements .tabPanel[data-panel-for="ace"]');
        if (acePanel) { acePanel.classList.remove('tabPanel'); acePanel.removeAttribute('data-panel-for'); }
        document.querySelectorAll('#page-engagements .tabList').forEach(el => { if (el.children.length === 0) el.remove(); });
        document.querySelectorAll('button[data-panel="new"]').forEach(el => { removed.push('btn:new-engagement'); el.remove(); });
        const engSub = document.querySelector('#page-engagements .pageHeader .ttl p');
        if (engSub) engSub.textContent = 'Everything that reaches out to a shopper: the engagement the AI decides on its own.';
        document.querySelectorAll('#page-campaigns .col.gap-xs').forEach(col => {
            const h2 = col.querySelector('h2');
            if (h2 && h2.textContent.includes('AI opportunities')) { removed.push('campaigns-ai-opportunities'); col.remove(); }
        });
        ['guardrailOpportunities','lifecycleOpportunities','loyaltyOpportunities'].forEach(id => {
            const el = document.getElementById(id); if (el) { removed.push(id); el.remove(); }
        });
        ['askFab','askPanel'].forEach(id => {
            const el = document.getElementById(id); if (el) { removed.push(id); el.remove(); }
        });
        const soonText = document.querySelector('#page-soon .ttl p');
        if (soonText) soonText.textContent = 'This MVP covers Overview, Engagements, Campaigns, Guardrails, Lifecycle, Conversations and Channels.';
        const pendingBtn = document.getElementById('acePendingBtn');
        if (pendingBtn) { removed.push('acePendingBtn'); pendingBtn.remove(); }
        document.querySelectorAll('#aceModeCards .modeBig').forEach(card => {
            if (card.textContent.includes('Manual acceptance')) { removed.push('mode:manual'); card.remove(); }
        });
        const chList = document.getElementById('chList');
        if (chList) { Array.from(chList.children).slice(1).forEach(el => el.remove()); removed.push('channels-non-sms'); }
        document.title = 'Journey Engagement Center — MVP';
        return removed;
    }''')

    print('DOM removed:', removed)
    html = page.content()
    browser.close()

# Replace ACE_DOMAINS with flat engagements in the serialized HTML
old_domains = '''const ACE_DOMAINS=[
  {n:"Replenishment & reorder",d:"Someone is due, or overdue, for something they already buy.",ins:"Customized",on:true,
   plays:[
     {n:"Replenishment due",d:"Past their own reorder rhythm for something they already buy.",trg:"on their learned rhythm, per category",ins:"Customized",reach:1680,gmv:9800,cvr:8.4,opt:0.6},
     {n:"Running low",d:"The usage model says the last one is nearly gone.",trg:"when the usage model says they are low",ins:"Default",reach:540,gmv:3900,cvr:7.8,opt:0.8},
     {n:"Size up the reorder",d:"Buying the same thing often enough that the bigger format is cheaper for them.",trg:"on the third repeat order",ins:"Default",reach:190,gmv:1200,cvr:6.9,opt:1.0}
   ]},
  {n:"Retention & win-back",d:"Going quiet, or already gone, and worth one honest attempt.",ins:"Default",on:true,
   plays:[
     {n:"Win-back",d:"No order in 120 days, one honest attempt.",trg:"after 120 days quiet, again at 180",ins:"Customized",reach:1290,gmv:5600,cvr:3.9,opt:1.9},
     {n:"At-risk save",d:"Already 1.5× past their own rhythm and still quiet.",trg:"at 1.5× their own gap",ins:"Default",reach:490,gmv:2600,cvr:5.2,opt:1.1},
     {n:"Second-order gap",d:"One order, sitting in the window where a second one usually lands.",trg:"between day 48 and 62 after the first order",ins:"Default",reach:200,gmv:900,cvr:5.4,opt:0.9}
   ]},
  {n:"Cross-sell & complements",d:"They own the thing; the companion piece is the obvious next step.",ins:"Customized",on:true,
   plays:[
     {n:"Post-purchase companion",d:"First order landed and the obvious companion is missing.",trg:"1 day after delivery",ins:"Customized",reach:820,gmv:5400,cvr:6.4,opt:0.8},
     {n:"Complete the kit",d:"Owns the base, missing the piece that finishes it.",trg:"14 days after the base item",ins:"Default",reach:560,gmv:4100,cvr:7.5,opt:0.9},
     {n:"Upgrade path",d:"Outgrew the entry model and the step up is worth naming.",trg:"on the usage signal",ins:"Default",reach:260,gmv:1800,cvr:7.1,opt:1.2}
   ]},
  {n:"Service recovery",d:"Something went wrong and the relationship is worth repairing.",ins:"Default",on:true,
   plays:[
     {n:"Post-resolution follow-up",d:"A support ticket closed; check the fix actually held.",trg:"2 days after the ticket closes",ins:"Default",reach:380,gmv:1700,cvr:3.1,opt:0.3},
     {n:"Return without a replacement",d:"Refund processed and nothing bought since.",trg:"5 days after the refund",ins:"Default",reach:140,gmv:700,cvr:3.5,opt:0.7},
     {n:"Delivery exception",d:"Delayed, lost or held in customs.",trg:"on the carrier event",ins:"Default",reach:0,gmv:0,cvr:0,opt:0,
      potReach:620,potGmv:2900,potCvr:2.4,potOpt:0.3,st:"setup",note:"No carrier integration yet"}
   ]},
  {n:"Subscriptions",d:"Renewals, failed payments, pauses worth saving.",ins:"Default",on:true,
   plays:[
     {n:"Renewal reminder",d:"Next charge approaching, no surprises.",trg:"3 days before the charge",ins:"Customized",reach:210,gmv:2900,cvr:11.4,opt:0.2},
     {n:"Card expiring",d:"Payment method expires before the next charge.",trg:"7 days before the card expires",ins:"Default",reach:110,gmv:1600,cvr:13.8,opt:0.3},
     {n:"Payment failed",d:"Dunning, without sounding like a debt collector.",trg:"2h after the failure, again at 48h",ins:"Default",reach:60,gmv:900,cvr:14.2,opt:0.4},
     {n:"Pause or cancel save",d:"They asked to stop; find out whether it's the cadence or the product.",trg:"1 day after the request",ins:"Default",reach:30,gmv:400,cvr:13.1,opt:0.6}
   ]},
  {n:"Loyalty moments",d:"A tier within reach, points about to expire, an anniversary.",ins:"Default",on:true,
   plays:[
     {n:"Points about to expire",d:"A balance worth something, 30 days from being worth nothing.",trg:"30 days before the points expire",ins:"Default",reach:120,gmv:1500,cvr:9.2,opt:0.4},
     {n:"A tier within reach",d:"One order away from the next tier.",trg:"when they cross 80% of the threshold",ins:"Default",reach:95,gmv:1400,cvr:10.6,opt:0.5},
     {n:"Anniversary",d:"A year since the first order, said properly.",trg:"on the anniversary of the first order",ins:"Default",reach:65,gmv:900,cvr:9.7,opt:0.7}
   ]},
  {n:"Consideration & browse",d:"Looking, hesitating, not yet a customer.",ins:"Default",on:false,
   plays:[
     {n:"Cart abandonment",d:"Checkout started, no order.",trg:"45 min after checkout, again at 20h",ins:"Customized",potReach:1180,potGmv:6200,potCvr:4.6,potOpt:1.5},
     {n:"Session abandonment",d:"Left mid-session without ever reaching the cart.",trg:"90 min after the session ends",ins:"Default",potReach:840,potGmv:2900,potCvr:2.7,potOpt:2.1},
     {n:"Browse abandonment",d:"Repeat views of the same product, no cart.",trg:"3h after the third view",ins:"Default",potReach:690,potGmv:2600,potCvr:3.1,potOpt:1.9},
     {n:"Welcome",d:"Opt-in confirmed, no first order yet.",trg:"immediately on consent",ins:"Default",potReach:390,potGmv:1100,potCvr:2.2,potOpt:1.7}
   ]},
  {n:"Seasonal & inventory",d:"A restock, a weather swing, a range that suddenly matters.",ins:"Default",on:false,
   plays:[
     {n:"Back in stock",d:"Something they viewed or waitlisted is available again.",trg:"on the restock event",ins:"Default",potReach:620,potGmv:3100,potCvr:6.2,potOpt:0.9},
     {n:"Price drop on a watched item",d:"Something they looked at twice got cheaper.",trg:"on the price change",ins:"Default",potReach:430,potGmv:1900,potCvr:4.8,potOpt:1.3},
     {n:"Weather swing",d:"A range that suddenly matters where they live.",trg:"on the forecast change",ins:"Default",potReach:400,potGmv:1600,potCvr:3.9,potOpt:1.5}
   ]}
];'''

new_domains = '''const ACE_ENGAGEMENTS=[
  {n:"Someone searched and did not find.",d:"They looked for something specific and came up empty — a signal to suggest the right alternative before they leave.",ins:"Default",on:true, reach:1180,gmv:6200,cvr:4.6,opt:1.5},
  {n:"Someone cannot make up their mind.",d:"They keep comparing variants, reading reviews, returning to the same page — a nudge toward the decision they are already leaning into.",ins:"Default",on:true, reach:840,gmv:2900,cvr:2.7,opt:2.1},
  {n:"Someone keeps coming back to one thing.",d:"Repeat views of the same product without buying — the item is in consideration, and the moment to answer the hesitation is now.",ins:"Default",on:true, reach:690,gmv:2600,cvr:3.1,opt:1.9},
  {n:"Someone is looking at the thing they are about to run out of.",d:"The usage model says the last one is nearly gone — a timely reminder to restock before they need it.",ins:"Default",on:true, reach:540,gmv:3900,cvr:7.8,opt:0.8}
];'''

if old_domains in html:
    html = html.replace(old_domains, new_domains)
    print('Replaced ACE_DOMAINS with ACE_ENGAGEMENTS')
else:
    print('WARNING: ACE_DOMAINS not found')

# Replace helper functions
old_helpers = '''function playReal(p){ return {reach:p.reach||0,gmv:p.gmv||0,cvr:p.cvr||0,opt:p.opt||0} }
function playPot(p){ return {reach:p.potReach??p.reach??0,gmv:p.potGmv??p.gmv??0,
                             cvr:p.potCvr??p.cvr??0,opt:p.potOpt??p.opt??0} }
function playLive(d,p,aceOn){ return aceOn && d.on && p.on!==false && p.st!=="setup" }
/* Never hand-write a theme total: fold the plays. Rates are re-derived from
   the reach they were measured on, never averaged across plays. */
function fold(rows){
  const reach=rows.reduce((a,r)=>a+r.reach,0), gmv=rows.reduce((a,r)=>a+r.gmv,0);
  const w=(k)=>reach?rows.reduce((a,r)=>a+r[k]*r.reach,0)/reach:0;
  return {reach,gmv,cvr:w("cvr"),opt:w("opt")};
}
function domTotals(d,aceOn){
  const live=d.plays.filter(p=>playLive(d,p,aceOn));
  return live.length?fold(live.map(playReal)):null;
}
function domPotential(d){ return fold(d.plays.map(playPot)) }'''

new_helpers = '''function engLive(e,aceOn){ return aceOn && e.on!==false }
function engReal(e){ return {reach:e.reach||0,gmv:e.gmv||0,cvr:e.cvr||0,opt:e.opt||0} }'''

if old_helpers in html:
    html = html.replace(old_helpers, new_helpers)
    print('Replaced helper functions')

# Update updateNavCount
old_navcount = '''function updateNavCount(){
  const on=aceState!=="off";
  const plays=ACE_DOMAINS.reduce((a,d)=>a+d.plays.filter(p=>playLive(d,p,on)).length,0);
  $("#navEngCount").textContent=plays+ENG.filter(r=>r.st==="on").length;
}'''
new_navcount = '''function updateNavCount(){
  const on=aceState!=="off";
  const plays=ACE_ENGAGEMENTS.filter(e=>engLive(e,on)).length;
  $("#navEngCount").textContent=plays;
}'''
if old_navcount in html:
    html = html.replace(old_navcount, new_navcount)
    print('Replaced updateNavCount')

# Inject override script before </body>
override = '''
<script>
(function(){
  window.renderAce = function(){
    const M=ACE_MODES.find(m=>m.k===aceState), on=aceState!=="off";
    const allowed=ACE_ENGAGEMENTS.filter(e=>e.on), off=ACE_ENGAGEMENTS.filter(e=>!e.on);
    const lostGmv=off.reduce((a,e)=>a+e.gmv,0);
    const badge=$("#aceTabBadge"); if(badge){ badge.textContent=M.n; badge.className="tag "+M.tag; }
    $("#aceModeCards").innerHTML=ACE_MODES.map(m=>{
      const sel=m.k===aceState;
      return `<button class="modeBig ${sel?"on":""}" data-acemode="${m.k}">
        <div class="row between">
          <div class="row gap-xs"><span class="h-md">${m.n}</span>${sel?`<span class="tag ${m.tag}">Current</span>`:""}</div>
          <span class="radioRing ${sel?"on":""}"></span>
        </div>
        <span class="t-md med" style="color:${sel?"var(--content-accent-default)":"var(--content-neutral-default)"}">${m.sum}</span>
        <span class="t-sm sec">${m.brief}</span>
        <span class="t-sm acc med" style="margin-top:auto" data-learn="${m.k}">Learn more →</span>
      </button>`}).join("");
    $("#aceDomCount").textContent=allowed.length+" of "+ACE_ENGAGEMENTS.length+" active";
    const pot=$("#aceDomPotential");
    if(off.length&&on){pot.style.display="";pot.textContent=off.length+" off · ≈$"+fmt(lostGmv)+" GMV left on the table"}
    else pot.style.display="none";
    const tb=$("#aceDomainTable tbody"); tb.innerHTML="";
    ACE_ENGAGEMENTS.forEach((e,i)=>{
      const live=engLive(e,on);
      const v=engReal(e);
      const tr=el("tr","domRow");
      tr.innerHTML=`
        <td><div class="row gap-xs" style="align-items:flex-start">
          <div class="col gap-xxxs" style="flex:1">
            <div class="row gap-xs wrap"><span class="t-md med">${e.n}</span></div>
            <span class="t-sm sec">${e.d}</span>
            ${live?"":`<span class="tag tag-purple" style="margin-top:4px;width:fit-content">Off — figures are estimates</span>`}
          </div>
        </div></td>
        <td class="t-md num-t">${fmt(Math.round(v.reach))}</td>
        <td class="t-md num-t">$${fmt(Math.round(v.gmv))}</td>
        <td class="t-md num-t">${rate(v.cvr)}</td>
        <td class="t-md num-t">${rate(v.opt)}</td>
        <td><button class="btn btn-secondary sm" data-dominstr="${i}">
          ${e.ins==="Customized"?`<span class="dot" style="background:var(--purple-500)"></span>Edit skill`
            :`<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 5v14M5 12h14"/></svg>Add skill`}
        </button></td>
        <td><div class="row gap-xs" style="justify-content:flex-end">
          <span class="t-sm ${e.on?"med":"ter"}" style="min-width:24px;text-align:right">${e.on?"On":"Off"}</span>
          <span class="toggle ${e.on?"on":""}" data-eng="${i}" ${on?"":'style="opacity:.5;pointer-events:none"'}></span>
        </div></td>`;
      tb.appendChild(tr);
    });
    updateNavCount();
  };
  
  // Override click handler for engagement toggles
  document.addEventListener('click', function(e){
    const t = e.target.closest('[data-eng]');
    if (t) {
      const i = +t.dataset.eng;
      ACE_ENGAGEMENTS[i].on = !ACE_ENGAGEMENTS[i].on;
      renderAce();
    }
  }, true);
  
  // Override goto to prevent removed pages
  const _goto = window.goto;
  window.goto = function(page, opts){
    if (['opportunities','intelligence','loyalty'].includes(page)) page = 'overview';
    return _goto(page, opts);
  };
  
  // Re-render now
  renderAce();
})();
</script>
'''

html = html.replace('</body>', override + '\n</body>')

# Add dummy elements for removed IDs to prevent original script errors
dummies = '''<div style="display:none !important" aria-hidden="true">
  <select id="oppType"></select>
  <select id="oppStatus"></select>
  <select id="oppSort"></select>
  <button id="oppPrev"></button>
  <button id="oppNext"></button>
  <button id="oppSend"></button>
  <button id="oppVoice"></button>
  <input id="askInput"/>
  <button id="askSend"></button>
  <button id="askFab"></button>
  <aside id="askPanel"></aside>
  <div id="benchWrap"></div>
  <div id="intelList"></div>
</div>
'''
html = html.replace('<body>', '<body>\n' + dummies)

# Update title
html = html.replace('<title>Journey Engagement Center — Axiom prototype</title>',
                    '<title>Journey Engagement Center — MVP</title>')

with open('/sandbox/journey-ec-gorgias/index.html', 'w') as f:
    f.write(html)

print('Wrote index.html, length:', len(html))
