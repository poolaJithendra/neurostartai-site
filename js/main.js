(async function(){
  const grid = document.getElementById('dealGrid');
  const note = document.getElementById('dealNote');
  if(!grid || !note) return;

  try{
    const res = await fetch('./deals.json', {cache:'no-store'});
    if(!res.ok) throw new Error('No deals.json yet');
    const deals = await res.json();
    if(!Array.isArray(deals) || deals.length === 0){
      note.textContent = 'Auto-refresh is live. New deals will appear after the next run.';
      return;
    }
    grid.innerHTML = deals.slice(0,12).map(d => `
      <div class="card">
        <div class="shot" style="aspect-ratio:1/1;margin-bottom:10px">
          <img src="${d.image||''}" alt="${(d.title||'').replace(/"/g,'&quot;')}" />
        </div>
        <h3 style="margin:6px 0 6px;font-size:16px">${d.title||'Item'}</h3>
        <p class="mini" style="margin:0 0 10px">${d.price||''} ${d.discount?`· ${d.discount}`:''}</p>
        <a class="btn" href="${d.url||'#'}" target="_blank" rel="nofollow noopener">Buy</a>
      </div>
    `).join('');
    note.textContent = 'Prices and availability may change on the retailer site.';
  }catch(e){
    console.warn(e);
    note.textContent = 'Deals will load once the refresh workflow completes.';
  }
})();
