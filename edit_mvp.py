import re

with open('index.html') as f:
    src = f.read()

print('Original length:', len(src))

# 1. Remove nav items: opportunities, intelligence, loyalty
src = re.sub(r'    <button class="navItem" data-page="opportunities">\n      <svg[^>]*>.*?</svg>\n      Opportunities <span class="count" id="navOppCount">7</span></button>\n', '', src, flags=re.S)
src = re.sub(r'    <button class="navItem" data-page="intelligence">\n      <svg[^>]*>.*?</svg>\n      Intelligence Hub</button>\n', '', src, flags=re.S)
src = re.sub(r'    <button class="navItem" data-page="loyalty">\n      <svg[^>]*>.*?</svg>\n      Loyalty <span class="count">4</span></button>\n', '', src, flags=re.S)

# 2. Remove Overview benchmark card
src = re.sub(r'          <!-- benchmark -->\n          <div class="card pad">.*?</div>\n\n', '', src, flags=re.S)

# 3. Remove Intelligence Core section
src = re.sub(r'      <!-- ======== INTELLIGENCE CORE · the model\'s read of the business ======== -->\n      <section class="page hidden" id="page-intelligence">.*?</section>\n\n', '', src, flags=re.S)

# 4. Remove Opportunities section
src = re.sub(r'      <!-- ======== OPPORTUNITIES · conversational action inbox ======== -->\n      <section class="page hidden" id="page-opportunities">.*?</section>\n\n', '', src, flags=re.S)

# 5. Remove Loyalty section
src = re.sub(r'      <!-- ======== LOYALTY · overview \+ configuration ======== -->\n      <section class="page hidden" id="page-loyalty">.*?</section>\n\n', '', src, flags=re.S)

# 6. Remove Campaigns AI opportunities block
src = re.sub(r'          <div class="col gap-xs">\n            <div class="row between wrap gap-xs">\n              <div class="col gap-xxxs"><h2 class="h-lg">AI opportunities</h2>\n                <p class="t-sm sec">Engage found timely stories in your catalogue and customer data.</p></div>\n              <span class="tag tag-purple">3 new</span>\n            </div>\n            <div class="grid g-3">.*?</div>\n          </div>\n\n', '', src, flags=re.S)

# 7. Remove Custom engagement tab
src = re.sub(r'          <button class="tabItem" data-tab="scenarios">Custom engagement <span class="tag tag-grey" id="scnBadge">18</span></button>\n', '', src)

# 8. Remove Custom engagement panel (scenarios tab)
src = re.sub(r'        <!-- ---------- TAB: SCENARIOS ---------- -->\n        <div class="zone top tabPanel hidden" data-panel-for="scenarios">.*?</div>\n      </section>\n\n', '      </section>\n\n', src, flags=re.S)

# 9. Convert ACE panel to regular zone (remove tabPanel wrapper)
src = src.replace('        <!-- ---------- TAB: ACE ---------- -->\n        <div class="zone top tabPanel" data-panel-for="ace">', '        <div class="zone top">')

# 10. Remove New engagement button
src = src.replace('            <button class="btn btn-primary" data-panel="new">New engagement</button>\n', '')

# 11. Update engagements subtitle
src = src.replace('Everything that reaches out to a shopper: the engagement the AI decides on its own, and the engagement you define.',
                  'Everything that reaches out to a shopper: the engagement the AI decides on its own.')

# 12. Update placeholder text
src = src.replace('This prototype covers Reporting, Engagements, Campaigns, Guardrails, Lifecycle, Conversations and Loyalty. Brand profile lives in your global account configuration, outside AI Journey.',
                  'This MVP covers Overview, Engagements, Campaigns, Guardrails, Lifecycle, Conversations and Channels.')

# 13. Remove opportunity sections in guardrails/lifecycle
src = src.replace('<div class="opportunitySection" id="guardrailOpportunities"></div>\n', '')
src = src.replace('<div class="opportunitySection" id="lifecycleOpportunities"></div>\n', '')
src = src.replace('<div class="opportunitySection" id="loyaltyOpportunities"></div>\n', '')

# 14. Remove askFab and askPanel
src = re.sub(r'<button class="askFab" id="askFab".*?</button>\n', '', src, flags=re.S)
src = re.sub(r'<aside class="askPanel" id="askPanel">.*?</aside>\n', '', src, flags=re.S)

# 15. Remove BENCH data
src = re.sub(r'const BENCH=\[.*?\];\n', '', src, flags=re.S)

# 16. Remove WHEN_EVENTS, WHEN_DELAYS, ENG (custom engagement data)
src = re.sub(r'const WHEN_EVENTS=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'const WHEN_DELAYS=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'const ENG=\[.*?\];\n', '', src, flags=re.S)

# 17. Remove PRODUCT_OPPORTUNITIES and OPPORTUNITIES
src = re.sub(r'const PRODUCT_OPPORTUNITIES=\{.*?\};\n', '', src, flags=re.S)
src = re.sub(r'const OPPORTUNITIES=\[.*?\];\n', '', src, flags=re.S)

# 18. Remove TIERS, EARN, REWARDS
src = re.sub(r'const TIERS=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'const EARN=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'const REWARDS=\[.*?\];\n', '', src, flags=re.S)

# 19. Update ACE modes: remove Manual acceptance
src = src.replace('''const ACE_MODES=[
  {k:"off",n:"Off",tag:"tag-grey",
   sum:"ACE stops looking entirely.",
   brief:"Nothing is deleted. Turn it back on and it resumes.",
   det:"Your own engagements and campaigns carry on exactly as before. ACE stops watching your data, stops proposing and stops sending. Anything it had queued is dropped rather than held, so nothing goes out days late when you switch back on.",
   see:"Nothing new in Conversations from ACE. History stays.",
   who:"Pick this if you want the machine out of the loop while you sort something else out."},
  {k:"manual",n:"Manual acceptance",tag:"tag-blue",
   sum:"It prepares everything. You press send.",
   brief:"It does all the work, then waits for you.",
   det:"ACE finds the moment, picks the person, writes the message and runs every guardrail — then stops. Nothing sends without you. Each one lands in Conversations with the full reasoning attached: the lifecycle stage, the loyalty state, the timing it chose and the lever it picked. You approve, edit or reject. Anything you leave untouched for 48 hours expires rather than going out stale.",
   see:"A queue in Conversations, each with its reasoning and a sample message.",
   who:"Pick this for the first few weeks, or on any theme where you want a human in the loop for good."},
  {k:"auto",n:"Automatic",tag:"tag-purple",
   sum:"It sends on its own, inside your guardrails.",
   brief:"Same work, no waiting. You review after, not before.",
   det:"ACE sends on its own. The guardrails still run last and can stop anything the agents decided — frequency, quiet hours, exclusions and discount ceilings are not negotiable. Every message is logged in Conversations with the reasoning that produced it, so nothing is unaccountable; the difference is that you read it after rather than before. You can drop back to manual at any time, and anything in flight finishes cleanly.",
   see:"Everything in Conversations as it happens, with the reasoning attached.",
   who:"Pick this once you've read a few dozen and you trust what it's doing."}
];''', '''const ACE_MODES=[
  {k:"off",n:"Off",tag:"tag-grey",
   sum:"ACE stops looking entirely.",
   brief:"Nothing is deleted. Turn it back on and it resumes.",
   det:"Your own engagements and campaigns carry on exactly as before. ACE stops watching your data, stops proposing and stops sending. Anything it had queued is dropped rather than held, so nothing goes out days late when you switch back on.",
   see:"Nothing new in Conversations from ACE. History stays.",
   who:"Pick this if you want the machine out of the loop while you sort something else out."},
  {k:"auto",n:"On",tag:"tag-purple",
   sum:"ACE sends on its own, inside your guardrails.",
   brief:"Same work, no waiting. You review after, not before.",
   det:"ACE sends on its own. The guardrails still run last and can stop anything the agents decided — frequency, quiet hours, exclusions and discount ceilings are not negotiable. Every message is logged in Conversations with the reasoning that produced it, so nothing is unaccountable; the difference is that you read it after rather than before. You can turn ACE off at any time, and anything in flight finishes cleanly.",
   see:"Everything in Conversations as it happens, with the reasoning attached.",
   who:"Pick this once you've read a few dozen and you trust what it's doing."}
];''')

# 20. Update CHANNELS to only SMS
src = src.replace('''const CHANNELS=[
  {n:"SMS",c:"var(--blue-200)",d:"Text-only. Works everywhere and is the fallback for every other channel.",on:true,locked:true,
   sends:["SampleStore · short code 78-2001","+1 415 555 0134 · long code"],status:"Verified",tag:"tag-green"},
  {n:"RCS",c:"var(--teal-200)",d:"Rich media, buttons and read receipts, where the carrier and device support it. Falls back to SMS automatically when it isn't.",on:true,
   sends:["Sample Store Co. · verified brand agent"],status:"Verified",tag:"tag-green"},
  {n:"Email",c:"var(--green-300)",d:"Best for longer or receipt-style sends — a different medium, not a shorter SMS.",on:true,
   sends:["hello@samplestore.example.com"],status:"Domain verification pending",tag:"tag-orange",
   extra:[["Exempt from quiet hours","An inbox doesn't buzz in someone's pocket the way a text does — let Email send on the engine's normal schedule instead of waiting for the SMS/RCS window in Guardrails → Timing.",false],
          ["Always include an unsubscribe link","Legal requirement, separate from the SMS/RCS opt-out line in Guardrails → Content.",true,true]]},
  {n:"Instagram",c:"var(--coral-400)",d:"DMs to shoppers who've messaged the account or opted in from an ad. Short, casual, image-friendly.",on:false,
   sends:["@samplestoreco"],status:"Not connected",tag:"tag-grey"},
  {n:"Messenger",c:"var(--purple-200)",d:"Facebook DMs — the same audience shape as Instagram, a different app.",on:false,
   sends:["Sample Store Co."],status:"Not connected",tag:"tag-grey"},
  {n:"TikTok",c:"var(--grey-300)",d:"DMs to shoppers who follow or have engaged with the account.",on:false,
   sends:["@samplestoreco"],status:"Not connected",tag:"tag-grey"},
  {n:"TikTok Shop",c:"var(--orange-300)",d:"Order and shipping updates tied to a TikTok Shop purchase.",on:false,
   sends:["Sample Store Co. Shop"],status:"Not connected",tag:"tag-grey",
   note:"Transactional only — TikTok Shop's own policy restricts this channel to order and shipping updates, so it never carries marketing content regardless of the skill."}
];''', '''const CHANNELS=[
  {n:"SMS",c:"var(--blue-200)",d:"Text-only. Works everywhere and is the fallback for every other channel.",on:true,locked:true,
   sends:["SampleStore · short code 78-2001","+1 415 555 0134 · long code"],status:"Verified",tag:"tag-green"}
];''')

# 21. Replace ACE_DOMAINS with 4 plain engagements
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
  {n:"Someone searched and did not find.",d:"They looked for something specific and came up empty — a signal to suggest the right alternative before they leave.",ins:"Default",on:true,
   reach:1180,gmv:6200,cvr:4.6,opt:1.5},
  {n:"Someone cannot make up their mind.",d:"They keep comparing variants, reading reviews, returning to the same page — a nudge toward the decision they are already leaning into.",ins:"Default",on:true,
   reach:840,gmv:2900,cvr:2.7,opt:2.1},
  {n:"Someone keeps coming back to one thing.",d:"Repeat views of the same product without buying — the item is in consideration, and the moment to answer the hesitation is now.",ins:"Default",on:true,
   reach:690,gmv:2600,cvr:3.1,opt:1.9},
  {n:"Someone is looking at the thing they are about to run out of.",d:"The usage model says the last one is nearly gone — a timely reminder to restock before they need it.",ins:"Default",on:true,
   reach:540,gmv:3900,cvr:7.8,opt:0.8}
];'''

if old_domains in src:
    src = src.replace(old_domains, new_domains)
else:
    print('WARNING: Could not find ACE_DOMAINS block')

# 22. Update helper functions for flat engagements
src = src.replace('''function playReal(p){ return {reach:p.reach||0,gmv:p.gmv||0,cvr:p.cvr||0,opt:p.opt||0} }
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
function domPotential(d){ return fold(d.plays.map(playPot)) }''', '''function engLive(e,aceOn){ return aceOn && e.on!==false }
function engReal(e){ return {reach:e.reach||0,gmv:e.gmv||0,cvr:e.cvr||0,opt:e.opt||0} }''')

# 23. Update updateNavCount
src = src.replace('''function updateNavCount(){
  const on=aceState!=="off";
  const plays=ACE_DOMAINS.reduce((a,d)=>a+d.plays.filter(p=>playLive(d,p,on)).length,0);
  $("#navEngCount").textContent=plays+ENG.filter(r=>r.st==="on").length;
}''', '''function updateNavCount(){
  const on=aceState!=="off";
  const plays=ACE_ENGAGEMENTS.filter(e=>engLive(e,on)).length;
  $("#navEngCount").textContent=plays;
}''')

# 24. Replace renderAce with a simpler version for flat engagements
old_renderAce = '''function renderAce(){
  const M=ACE_MODES.find(m=>m.k===aceState), on=aceState!=="off";
  const allowed=ACE_DOMAINS.filter(d=>d.on), off=ACE_DOMAINS.filter(d=>!d.on);
  const lostGmv=off.reduce((a,d)=>a+domPotential(d).gmv,0);

  $("#acePendingBtn").style.display = aceState==="manual" ? "" : "none";
  const badge=$("#aceTabBadge"); badge.textContent=M.n; badge.className="tag "+M.tag;

  /* mode cards */
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

  /* domains, and the plays underneath them */
  $("#aceDomCount").textContent=allowed.length+" of "+ACE_DOMAINS.length+" allowed";
  const pot=$("#aceDomPotential");
  if(off.length&&on){pot.style.display="";pot.textContent=off.length+" off · ≈$"+fmt(lostGmv)+" GMV left on the table"}
  else pot.style.display="none";
  $("#aceExpandAll").textContent = aceOpen.size ? "Collapse all" : "Expand all";

  const tb=$("#aceDomainTable tbody"); tb.innerHTML="";
  ACE_DOMAINS.forEach((d,i)=>{
    const live=d.on&&on, open=aceOpen.has(i);
    const t=live?domTotals(d,on):null, p=domPotential(d);
    const nPlays=d.plays.length, nSetup=d.plays.filter(x=>x.st==="setup").length;
    const cell=(real,potential)=>t
      ? `<td class="t-md num-t">${real}</td>`
      : `<td class="t-md num-t" style="color:var(--content-accent-default);font-style:italic">${potential}</td>`;

    const tr=el("tr","domRow");
    tr.setAttribute("data-domopen",i);
    tr.style.cursor="pointer";
    tr.innerHTML=`
      <td><div class="row gap-xs" style="align-items:flex-start">
        <button class="twistie ${open?"open":""}" tabindex="-1" aria-hidden="true">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6"><path d="m9 5 7 7-7 7"/></svg>
        </button>
        <div class="col gap-xxxs" style="flex:1">
          <div class="row gap-xs wrap"><span class="t-md med">${d.n}</span>
            <span class="tag tag-grey">${nPlays} play${nPlays===1?"":"s"}</span>
            ${nSetup&&live?`<span class="tag tag-orange">${nSetup} needs setup</span>`:""}</div>
          <span class="t-sm sec">${d.d}</span>
          ${live?"":`<span class="tag tag-purple" style="margin-top:4px;width:fit-content">Not allowed — figures are estimates</span>`}
        </div>
      </div></td>
      ${cell(fmt(Math.round(t?t.reach:0)),"≈"+fmt(Math.round(p.reach)))}
      ${cell("$"+fmt(Math.round(t?t.gmv:0)),"≈$"+fmt(Math.round(p.gmv)))}
      ${cell(rate(t?t.cvr:0),"≈"+rate(p.cvr))}
      ${cell(rate(t?t.opt:0),"≈"+rate(p.opt))}
      <td><button class="btn btn-secondary sm" data-dominstr="${i}">
        ${d.ins==="Customized"?`<span class="dot" style="background:var(--purple-500)"></span>Edit skill`
          :`<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 5v14M5 12h14"/></svg>Add skill`}
      </button></td>
      <td><div class="row gap-xs" style="justify-content:flex-end">
        <span class="t-sm ${d.on?"med":"ter"}" style="min-width:24px;text-align:right">${d.on?"Yes":"No"}</span>
        <span class="toggle ${d.on?"on":""}" data-dom="${i}" ${on?"":'style="opacity:.5;pointer-events:none"'}></span>
      </div></td>`;
    tb.appendChild(tr);
    if(!open) return;

    d.plays.forEach((pl,j)=>{
      const pLive=playLive(d,pl,on), v=pLive?playReal(pl):playPot(pl), pOn=pl.on!==false;
      const pInteractive=on&&pl.st!=="setup";
      const pStatus=pl.st==="setup"?"Blocked":pLive?"Running":!on?"ACE is off":!d.on?"Off with the theme":"Off";
      const pc=(real,potential)=>pLive
        ? `<td class="t-md num-t">${real}</td>`
        : `<td class="t-md num-t" style="color:var(--content-accent-default);font-style:italic">${potential}</td>`;
      const ptr=el("tr","playRow");
      ptr.innerHTML=`
        <td><div class="playName">
          <span class="playRail ${pLive?"live":""}"></span>
          <div class="col gap-xxxs" style="flex:1">
            <div class="row gap-xs wrap"><span class="t-md med">${pl.n}</span>
              ${pl.st==="setup"?`<span class="tag tag-orange">${pl.note}</span>`:""}</div>
            <span class="t-sm sec">${pl.d}</span>
            <span class="t-xs ter">Fires ${pl.trg}</span>
          </div>
        </div></td>
        ${pc(fmt(v.reach),"≈"+fmt(v.reach))}
        ${pc("$"+fmt(v.gmv),"≈$"+fmt(v.gmv))}
        ${pc(rate(v.cvr),"≈"+rate(v.cvr))}
        ${pc(rate(v.opt),"≈"+rate(v.opt))}
        <td><button class="btn btn-tertiary sm" data-playinstr="${i}.${j}">
          ${pl.ins==="Customized"?`<span class="dot" style="background:var(--purple-500)"></span>Edit skill`
            :`<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 5v14M5 12h14"/></svg>Add skill`}
        </button></td>
        <td><div class="row gap-xs" style="justify-content:flex-end">
          <span class="t-xs ter" style="text-align:right">${pStatus}</span>
          <span class="toggle ${pOn?"on":""}" data-play="${i}.${j}" ${pInteractive?"":'style="opacity:.5;pointer-events:none"'}></span>
        </div></td>`;
      tb.appendChild(ptr);
    });
  });

  updateNavCount();
}'''

new_renderAce = '''function renderAce(){
  const M=ACE_MODES.find(m=>m.k===aceState), on=aceState!=="off";
  const allowed=ACE_ENGAGEMENTS.filter(e=>e.on), off=ACE_ENGAGEMENTS.filter(e=>!e.on);
  const lostGmv=off.reduce((a,e)=>a+e.gmv,0);

  const badge=$("#aceTabBadge"); badge.textContent=M.n; badge.className="tag "+M.tag;

  /* mode cards */
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

  /* engagements table */
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
}'''

if old_renderAce in src:
    src = src.replace(old_renderAce, new_renderAce)
else:
    print('WARNING: Could not find renderAce function')

# 25. Remove renderBench function
src = re.sub(r'function renderBench\(\)\{.*?\n\}\n', '', src, flags=re.S)

# 26. Remove opportunity functions
src = re.sub(r'function visibleOpportunities\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function renderOpportunities\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function renderOpportunityDetail\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function addOpportunityExchange\(user,assistant\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function applyOpportunityAction\(act\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function sendOpportunityMessage\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function renderProductOpportunities\(surface,hostId\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function removeProductOpportunity\(surface,k\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function findProductOpportunity\(k\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function openProductOpportunity\(k\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function applyProductOpportunity\(k\)\{.*?\n\}\n', '', src, flags=re.S)

# 27. Remove custom engagement functions
src = re.sub(r'function whenLine\(w\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function renderEng\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'const ENG_DEFAULT_TEXT=.*?\n', '', src)
src = re.sub(r'function instructionText\(r\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function openEngagement\(i\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function studioForEng\(i\)\{.*?\n\}\n', '', src, flags=re.S)

# 28. Remove loyalty functions
src = re.sub(r'function renderLoyalty\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function renderEarn\(\)\{.*?\n\}\n', '', src, flags=re.S)

# 29. Remove intelligence functions
src = re.sub(r'function renderIntelligence\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function drawIntelRead\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function drawIntelGraph\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function intelInspect\(k\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function drawIntelDecay\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function intelReadout\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function drawMarkets\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function tickMarkets\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function drawPlays\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function drawSegments\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function drawRevisions\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function pushDecision\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function startStream\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function drawBlind\(\)\{.*?\n\}\n', '', src, flags=re.S)

# 30. Remove ASK functions
src = re.sub(r'function buildAsk\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function sendAsk\(\)\{.*?\n\}\n', '', src, flags=re.S)
src = re.sub(r'function renderAsk\(\)\{.*?\n\}\n', '', src, flags=re.S)

# 31. Remove intelligence data arrays
src = re.sub(r'const iFmt=.*?\n', '', src)
src = re.sub(r'const iMoney=.*?\n', '', src)
src = re.sub(r'const iPct=.*?\n', '', src)
src = re.sub(r'const NS=.*?\n', '', src)
src = re.sub(r'const svgEl=.*?\n', '', src)
src = re.sub(r'const IRAMP=.*?\n', '', src)
src = re.sub(r'const I_PRODUCTS=\{.*?\};\n', '', src, flags=re.S)
src = re.sub(r'const I_EDGES=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'const I_COHORT=.*?\n', '', src)
src = re.sub(r'const I_ROLE_C=.*?\n', '', src)
src = re.sub(r'const I_ROLE_N=.*?\n', '', src)
src = re.sub(r'const iOut=.*?\n', '', src)
src = re.sub(r'const iInc=.*?\n', '', src)
src = re.sub(r'const iDown=.*?\n', '', src)
src = re.sub(r'const iStake=.*?\n', '', src)
src = re.sub(r'const iStartValue=.*?\n', '', src)
src = re.sub(r'const HERO_MULT=.*?\n', '', src)
src = re.sub(r'const I_P0=.*?\n', '', src)
src = re.sub(r'const I_HALF=.*?\n', '', src)
src = re.sub(r'const pAt=.*?\n', '', src)
src = re.sub(r'const cohortAt=.*?\n', '', src)
src = re.sub(r'const PEAK_D=.*?\n', '', src)
src = re.sub(r'const peakP=.*?\n', '', src)
src = re.sub(r'const WINDOW=.*?\n', '', src)
src = re.sub(r'const I_SECTIONS=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'let intelSel=.*?\n', '', src)
src = re.sub(r'const I_COLX=.*?\n', '', src)
src = re.sub(r'let gMode=.*?\n', '', src)
src = re.sub(r'let gSel=.*?\n', '', src)
src = re.sub(r'let iRaf=.*?\n', '', src)
src = re.sub(r'const I_MONTHS=.*?\n', '', src)
src = re.sub(r'const I_MONTH_FULL=.*?\n', '', src)
src = re.sub(r'const NORTH=.*?\n', '', src)
src = re.sub(r'const rot=.*?\n', '', src)
src = re.sub(r'const MARKETS=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'const rampIdx=.*?\n', '', src)
src = re.sub(r'let mkMonth=.*?\n', '', src)
src = re.sub(r'let mkPlaying=.*?\n', '', src)
src = re.sub(r'let mkTimer=.*?\n', '', src)
src = re.sub(r'const PLAYS=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'let playMode=.*?\n', '', src)
src = re.sub(r'const SEGMENTS=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'const REVISIONS=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'const I_NAMES=.*?\n', '', src)
src = re.sub(r'const I_ACTS=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'let streamOn=.*?\n', '', src)
src = re.sub(r'let iSi=.*?\n', '', src)
src = re.sub(r'let streamTimer=.*?\n', '', src)
src = re.sub(r'const BELIEFS=\[.*?\];\n', '', src, flags=re.S)
src = re.sub(r'const FEEDS=\[.*?\];\n', '', src, flags=re.S)

# 32. Remove opportunity variables
src = re.sub(r'let oppSel=.*?\n', '', src)
src = re.sub(r'const oppExchanges=.*?\n', '', src)
src = re.sub(r'const oppStatusMeta=.*?\n', '', src)
src = re.sub(r'const safeText=.*?\n', '', src)

# 33. Remove loyalty variables
src = re.sub(r'let loySel=.*?\n', '', src)

# 34. Update goto function
src = src.replace('''  if(page==="campaign-new") resetWizard();
  if(page==="intelligence"){ renderIntelligence(); buildAsk(); }
  /* the Ask shortcut belongs to the Intelligence Core — it answers from that
     page's model objects, so it should not float over unrelated screens */
  const fab=$("#askFab"), askP=$("#askPanel");
  if(fab) fab.style.display = (page==="intelligence" && !askOpen) ? "" : "none";
  if(askP && page!=="intelligence"){ askP.classList.remove("on"); askOpen=false; }''', '''  if(page==="campaign-new") resetWizard();''')

# 35. Update bottom render calls
src = src.replace('''renderReport(); renderBench();
renderEng(); renderAce(); renderCampaigns(); renderOpportunities(); renderRules(); renderVariants();
renderGuardrails(); renderExclusions(); renderLifecycle(); renderChannels();
renderConv(); renderWiz(); renderLoyalty();
renderProductOpportunities("guardrails","guardrailOpportunities");
renderProductOpportunities("lifecycle","lifecycleOpportunities");
renderProductOpportunities("loyalty","loyaltyOpportunities");''', '''renderReport();
renderAce(); renderCampaigns(); renderRules(); renderVariants();
renderGuardrails(); renderExclusions(); renderLifecycle(); renderChannels();
renderConv(); renderWiz();''')

# 36. Remove opportunity event listeners
src = re.sub(r'\$\("#oppType"\)\.addEventListener\("change",.*?\);\n', '', src)
src = re.sub(r'\$\("#oppStatus"\)\.addEventListener\("change",.*?\);\n', '', src)
src = re.sub(r'\$\("#oppSort"\)\.addEventListener\("change",.*?\);\n', '', src)
src = re.sub(r'\$\("#oppPrev"\)\.addEventListener\("click",.*?\}\);\n', '', src)
src = re.sub(r'\$\("#oppNext"\)\.addEventListener\("click",.*?\}\);\n', '', src)
src = re.sub(r'\$\("#oppSend"\)\.addEventListener\("click",.*?\}\);\n', '', src)
src = re.sub(r'\$\("#oppVoice"\)\.addEventListener\("click",.*?\}\);\n', '', src)

# 37. Remove delegated handlers for removed features
src = re.sub(r'if\(opportunitySelect\)\{oppSel=opportunitySelect\.dataset\.oppSelect;renderOpportunities\(\);return\}\n', '', src)
src = re.sub(r'if\(loyaltyApply\)\{.*?renderLoyalty\(\); return;\}\n', '', src, flags=re.S)
src = re.sub(r'if\(tierNew\)\{.*?renderLoyalty\(\); return;\}\n', '', src, flags=re.S)
src = re.sub(r'if\(panelNew\)\{.*?closePanel\(\); return;\}\n', '', src, flags=re.S)

# 38. Update click handler for domains -> engagements
src = src.replace('if(domOpen!==null){aceOpen.toggle(+domOpen);renderAce();return}', 'if(domOpen!==null){renderAce();return}')
src = src.replace('if(playToggle){const[i,j]=playToggle.dataset.play.split(".");', 'if(playToggle){return} // plays removed in MVP\n  if(false){const[i,j]=playToggle.dataset.play.split(".");')
src = src.replace('const domToggle=e.target.closest("[data-dom]")', 'const domToggle=e.target.closest("[data-eng]")')
src = src.replace('if(domToggle){const i=+domToggle.dataset.dom;ACE_DOMAINS[i].on=!ACE_DOMAINS[i].on;renderAce();return}',
                  'if(domToggle){const i=+domToggle.dataset.eng;ACE_ENGAGEMENTS[i].on=!ACE_ENGAGEMENTS[i].on;renderAce();return}')

# 39. Remove conversation loyalty references
src = src.replace('["Loyalty","Member · 340 points, 60 short of a free-shipping reward"],\n              ', '')
src = src.replace('["Loyalty","Gold · early access is available, so no discount needed"],\n              ', '')
src = src.replace('["Loyalty","Silver · free returns already included, used as the reassurance"],\n              ', '')
src = src.replace('["Loyalty","Silver · earned 80 points on this order"],\n              ', '')
src = src.replace('["Loyalty","Summit · concierge sizing offered instead of a discount"],\n              ', '')
src = src.replace('["Loyalty","Silver · 1.25 points per dollar mentioned at close"],\n              ', '')
src = src.replace('["Loyalty","Member · 900 points, enough for free shipping"],\n              ', '')
src = src.replace('["Loyalty","Gold → Summit within reach; expiring points are the hook"],\n              ', '')

# 40. Remove tier field from conversations
src = re.sub(r',tier:"[^"]+"', '', src)

# 41. Remove loyalty domain
src = src.replace('domain:"Loyalty moments",', 'domain:"Lifecycle",')

# 42. Remove loyalty-related campaign data
src = src.replace('aud:"Summit + Gold loyalty tiers",', 'aud:"Summit tier members",')
src = src.replace('win:"Points boost",', 'win:"Answer the objection",')

# 43. Remove loyalty references in conversation text
src = src.replace('No offer; loyalty reward held in reserve', 'No offer')
src = src.replace('Gold tier makes early access available as a lever, ahead of any discount.', 'Early access is available as a lever, ahead of any discount.')
src = src.replace('Silver tier includes free returns, so the risk of trying again is already covered — used as reassurance instead of a discount.', 'Free returns are included, so the risk of trying again is already covered — used as reassurance instead of a discount.')
src = src.replace('Summit tier gets concierge sizing instead of a discount, which answers the actual blocker.', 'Concierge sizing is available instead of a discount, which answers the actual blocker.')
src = src.replace('900 points is enough for free shipping, so that\'s offered before any discount.', 'Free shipping is available, so that\'s offered before any discount.')
src = src.replace('120 points from Summit, and 1,400 points expire at the end of the month.', 'A tier milestone is close, and a reward expires at the end of the month.')
src = src.replace('120 points from crossing into Summit — close enough that naming it is worth doing.', 'Close to a tier milestone — close enough that naming it is worth doing.')
src = src.replace('1,400 points expire at the end of the month if unused.', 'A reward expires at the end of the month if unused.')
src = src.replace('Ingrid — you\'re 120 points from Summit, and 1,400 of yours expire on the 31st. Want me to show you what they\'d cover?', 'Ingrid — you\'re close to a tier milestone, and a reward expires on the 31st. Want me to show you what it covers?')

# 44. Remove tier tag rendering in conversations
src = re.sub(r'      <span class="tag \$\{c\.tier==="Gold"\|\|c\.tier==="Summit"\?"tag-yellow":"tag-blue"\}\">\$\{c\.tier\}</span>\n', '', src)
src = re.sub(r'      <span class="tag tag-blue">\$\{c\.tier\}</span>\n', '', src)

# 45. Remove tier from conversation filter and display
src = src.replace('&&(!convQ||(c.who+" "+c.domain+" "+c.why+" "+c.tier).toLowerCase().includes(convQ))',
                  '&&(!convQ||(c.who+" "+c.domain+" "+c.why).toLowerCase().includes(convQ))')
src = src.replace('${c.id} · ${c.stage} · ${c.tier}', '${c.id} · ${c.stage}')

# 46. Remove PREV_TIER
src = re.sub(r'const PREV_TIER=\[.*?\];\n', '', src)
src = re.sub(r'const tier=PREV_TIER\[\(i\*11\)%PREV_TIER\.length\];\n', '', src)

# 47. Remove loyalty from STAGES conditions
src = re.sub(r'cond:\[\["Loyalty sign-up","=","yes"\]\],', 'cond:[["Orders","≥","1"]],', src)

# 48. Remove loyalty from rule builder options
src = src.replace('<option>Loyalty tier</option>', '')

# 49. Remove loyalty from guardrails summary
src = src.replace('Discount is the last lever, not the first — Loyalty gives it cheaper ones.', 'Discount is the last lever, not the first.')

# 50. Remove loyalty from DISCOUNTS and LEVERS
src = src.replace('"Loyalty points instead of money",', '')
src = src.replace('"Points boost",', '')
src = src.replace('"Tier fast-track",', '')

# 51. Remove SRC Custom
src = src.replace('''const SRC={ACE:{c:"var(--dv-ace)",tag:"tag-purple"},Custom:{c:"var(--dv-custom)",tag:"tag-coral"},
           Campaign:{c:"var(--dv-campaign)",tag:"tag-teal"}};''',
                  '''const SRC={ACE:{c:"var(--dv-ace)",tag:"tag-purple"},
           Campaign:{c:"var(--dv-campaign)",tag:"tag-teal"}};''')

# 52. Remove Custom source references in conversations
src = src.replace('src:"Custom",', 'src:"ACE",')

# 53. Remove tier source from DIMS
src = re.sub(r'  tier:\{label:"Loyalty tier", head:"Tier", members:\[\n    \{n:"Member",base:6900,g:\.008,reply:\.079,click:\.054,cvr:\.038,opt:\.010,aov:116\},\n    \{n:"Silver",base:4200,g:\.012,reply:\.091,click:\.064,cvr:\.049,opt:\.007,aov:128\},\n    \{n:"Gold",base:2800,g:\.015,reply:\.103,click:\.074,cvr:\.058,opt:\.005,aov:142\},\n    \{n:"Summit",base:900,g:\.018,reply:\.118,click:\.087,cvr:\.071,opt:\.003,aov:168\}\n  \]\},\n', '', src)

# 54. Remove loyalty from campaign wizard thread
src = re.sub(r'\["Loyalty","[^"]+"\],\n              ', '', src)

# 55. Remove remaining loyalty text
src = src.replace('Loyalty threshold crossed', 'Tier threshold crossed')

# 56. Remove Intelligence Core CSS block
src = re.sub(r'/\* ============ INTELLIGENCE CORE ============ \*/.*?/\* ============ MOBILE ============ \*/', '/\* ============ MOBILE ============ */', src, flags=re.S)

# 57. Remove opportunity CSS block
src = re.sub(r'/\* opportunities inbox \*/.*?/\* lever object rows \*/', '', src, flags=re.S)

# 58. Remove custom engagement CSS
src = re.sub(r'/\* shopper rows in the drawer \*/.*?/\* the conversations inbox needs its own height \*/', '', src, flags=re.S)

# 59. Remove loyalty CSS
src = re.sub(r'/\* loyalty tier ramp \*/.*?/\* ============ MOBILE ============ \*/', '/\* ============ MOBILE ============ */', src, flags=re.S)

# 60. Remove remaining CSS rules
src = re.sub(r'\.intel[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.i-[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.opp[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.scn[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.engRow[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.whenLine[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.loy[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.tier[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.reward[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.ask[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.market[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.playBar[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.seg[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.revItem[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.decision[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.belief[A-Za-z0-9_-]*[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.opportunitySection[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'\.opportunityHead[^\{]*\{[^}]*\}\n', '', src)
src = re.sub(r'#page-intelligence\{[^}]+\}\n', '', src)
src = re.sub(r'#page-conversations,#page-opportunities\{[^}]+\}\n', '#page-conversations{display:flex;flex-direction:column;height:100%}\n', src)

# 61. Remove ACE_CHAIN if no longer used
src = re.sub(r'const ACE_CHAIN=\[.*?\];\n', '', src, flags=re.S)

# 62. Remove aceOpen variable since no longer needed
src = re.sub(r'let aceOpen=new Set\(\);\n', '', src)

# 63. Remove aceExpandAll references
src = re.sub(r'\$\("#aceExpandAll"\)\.textContent = aceOpen\.size \? "Collapse all" : "Expand all";\n', '', src)

# 64. Update title
src = src.replace('<title>Journey Engagement Center — Axiom prototype</title>',
                  '<title>Journey Engagement Center — MVP</title>')

# Clean up excessive blank lines
src = re.sub(r'\n{3,}', '\n\n', src)

with open('index.html', 'w') as f:
    f.write(src)

print('Final length:', len(src))
