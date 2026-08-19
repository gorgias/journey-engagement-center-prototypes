from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('file:///sandbox/journey-ec-gorgias/index.html')
    page.wait_for_selector('.app')

    result = page.evaluate('''() => {
        const log = [];
        
        // 1. Replace ACE_DOMAINS with flat engagements in JS
        window.ACE_ENGAGEMENTS = [
          {n:"Someone searched and did not find.",d:"They looked for something specific and came up empty — a signal to suggest the right alternative before they leave.",ins:"Default",on:true, reach:1180,gmv:6200,cvr:4.6,opt:1.5},
          {n:"Someone cannot make up their mind.",d:"They keep comparing variants, reading reviews, returning to the same page — a nudge toward the decision they are already leaning into.",ins:"Default",on:true, reach:840,gmv:2900,cvr:2.7,opt:2.1},
          {n:"Someone keeps coming back to one thing.",d:"Repeat views of the same product without buying — the item is in consideration, and the moment to answer the hesitation is now.",ins:"Default",on:true, reach:690,gmv:2600,cvr:3.1,opt:1.9},
          {n:"Someone is looking at the thing they are about to run out of.",d:"The usage model says the last one is nearly gone — a timely reminder to restock before they need it.",ins:"Default",on:true, reach:540,gmv:3900,cvr:7.8,opt:0.8}
        ];
        delete window.ACE_DOMAINS;
        log.push('replaced ACE_DOMAINS');
        
        // 2. Replace helper functions
        window.engLive = function(e,aceOn){ return aceOn && e.on!==false; };
        window.engReal = function(e){ return {reach:e.reach||0,gmv:e.gmv||0,cvr:e.cvr||0,opt:e.opt||0}; };
        
        // 3. Replace updateNavCount
        window.updateNavCount = function(){
          const on=aceState!=="off";
          const plays=ACE_ENGAGEMENTS.filter(e=>engLive(e,on)).length;
          $("#navEngCount").textContent=plays;
        };
        
        // 4. Replace renderAce
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
        
        // 5. Remove nav items
        document.querySelectorAll('.navItem').forEach(el => {
            const pg = el.dataset.page;
            if (['opportunities','intelligence','loyalty'].includes(pg)) { log.push('nav:'+pg); el.remove(); }
        });
        
        // 6. Remove Overview benchmark
        document.querySelectorAll('#page-overview .card').forEach(card => {
            if (card.textContent.includes('How you compare')) { log.push('overview-benchmark'); card.remove(); }
        });
        
        // 7. Remove entire pages
        ['page-opportunities','page-intelligence','page-loyalty'].forEach(id => {
            const el = document.getElementById(id);
            if (el) { log.push(id); el.remove(); }
        });
        
        // 8. Remove Custom engagement tab and panel
        document.querySelectorAll('#page-engagements .tabItem').forEach(el => {
            if (el.dataset.tab === 'scenarios') { log.push('tab:scenarios'); el.remove(); }
        });
        document.querySelectorAll('#page-engagements .tabPanel').forEach(el => {
            if (el.dataset.panelFor === 'scenarios') { log.push('panel:scenarios'); el.remove(); }
        });
        const acePanel = document.querySelector('#page-engagements .tabPanel[data-panel-for="ace"]');
        if (acePanel) { acePanel.classList.remove('tabPanel'); acePanel.removeAttribute('data-panel-for'); }
        document.querySelectorAll('#page-engagements .tabList').forEach(el => { if (el.children.length === 0) el.remove(); });
        
        // 9. Remove New engagement button
        document.querySelectorAll('button[data-panel="new"]').forEach(el => { log.push('btn:new-engagement'); el.remove(); });
        
        // 10. Update engagements subtitle
        const engSub = document.querySelector('#page-engagements .pageHeader .ttl p');
        if (engSub) engSub.textContent = 'Everything that reaches out to a shopper: the engagement the AI decides on its own.';
        
        // 11. Remove Campaigns AI opportunities
        document.querySelectorAll('#page-campaigns .col.gap-xs').forEach(col => {
            const h2 = col.querySelector('h2');
            if (h2 && h2.textContent.includes('AI opportunities')) { log.push('campaigns-ai-opportunities'); col.remove(); }
        });
        
        // 12. Remove opportunity sections
        ['guardrailOpportunities','lifecycleOpportunities','loyaltyOpportunities'].forEach(id => {
            const el = document.getElementById(id);
            if (el) { log.push(id); el.remove(); }
        });
        
        // 13. Remove askFab/askPanel
        ['askFab','askPanel'].forEach(id => {
            const el = document.getElementById(id);
            if (el) { log.push(id); el.remove(); }
        });
        
        // 14. Update placeholder text
        const soonText = document.querySelector('#page-soon .ttl p');
        if (soonText) soonText.textContent = 'This MVP covers Overview, Engagements, Campaigns, Guardrails, Lifecycle, Conversations and Channels.';
        
        // 15. Remove pending button
        const pendingBtn = document.getElementById('acePendingBtn');
        if (pendingBtn) { log.push('acePendingBtn'); pendingBtn.remove(); }
        
        // 16. Remove Manual acceptance mode card
        document.querySelectorAll('#aceModeCards .modeBig').forEach(card => {
            if (card.textContent.includes('Manual acceptance')) { log.push('mode:manual'); card.remove(); }
        });
        
        // 17. Channels: keep only SMS in list
        const chList = document.getElementById('chList');
        if (chList) { Array.from(chList.children).slice(1).forEach(el => el.remove()); log.push('channels-non-sms'); }
        
        // 18. Update title
        document.title = 'Journey Engagement Center — MVP';
        
        // 19. Update CHANNELS data
        window.CHANNELS = window.CHANNELS.filter(ch => ch.n === 'SMS');
        window.chSel = 0;
        
        // 20. Update ACE modes data
        window.ACE_MODES = [
          {k:"off",n:"Off",tag:"tag-grey", sum:"ACE stops looking entirely.", brief:"Nothing is deleted. Turn it back on and it resumes.", det:"Your own engagements and campaigns carry on exactly as before. ACE stops watching your data, stops proposing and stops sending. Anything it had queued is dropped rather than held, so nothing goes out days late when you switch back on.", see:"Nothing new in Conversations from ACE. History stays.", who:"Pick this if you want the machine out of the loop while you sort something else out."},
          {k:"auto",n:"On",tag:"tag-purple", sum:"ACE sends on its own, inside your guardrails.", brief:"Same work, no waiting. You review after, not before.", det:"ACE sends on its own. The guardrails still run last and can stop anything the agents decided — frequency, quiet hours, exclusions and discount ceilings are not negotiable. Every message is logged in Conversations with the reasoning that produced it, so nothing is unaccountable; the difference is that you read it after rather than before. You can turn ACE off at any time, and anything in flight finishes cleanly.", see:"Everything in Conversations as it happens, with the reasoning attached.", who:"Pick this once you've read a few dozen and you trust what it's doing."}
        ];
        
        // 21. Remove loyalty from conversations
        if (window.CONV) {
            window.CONV.forEach(c => {
                delete c.tier;
                if (c.domain === 'Loyalty moments') c.domain = 'Lifecycle';
                if (c.src === 'Custom') c.src = 'ACE';
                if (c.reason) c.reason = c.reason.filter(r => r[0] !== 'Loyalty');
            });
        }
        
        // 22. Remove Custom from SRC
        if (window.SRC && window.SRC.Custom) delete window.SRC.Custom;
        
        // 23. Remove tier from DIMS
        if (window.DIMS && window.DIMS.tier) delete window.DIMS.tier;
        
        // 24. Remove loyalty from DISCOUNTS and LEVERS
        if (window.DISCOUNTS) window.DISCOUNTS = window.DISCOUNTS.filter(d => d !== "Loyalty points instead of money");
        if (window.LEVERS) window.LEVERS = window.LEVERS.filter(l => l !== "Points boost" && l !== "Tier fast-track");
        
        // 25. Re-render engagements
        renderAce();
        
        return log;
    }''')

    print('DOM changes:', result)
    
    # Serialize the modified page
    html = page.content()
    browser.close()
    
    with open('/sandbox/journey-ec-gorgias/index.html', 'w') as f:
        f.write(html)
    
    print('Wrote index.html, length:', len(html))
