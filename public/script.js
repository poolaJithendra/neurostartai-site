const $ = (q)=>document.querySelector(q);
const grid = $("#grid");
const state = { q:"", cat:"", sort:"score" };

function render(items){
  grid.innerHTML = "";
  items.forEach(d=>{
    const el = document.createElement("div");
    el.className = "card";
    el.innerHTML = `
      <img class="thumb" src="${d.image_url}" alt="${d.title}">
      <div class="pad">
        <div class="title">${d.title}</div>
        <div class="meta">
          <span>₹${parseInt(d.deal_price)} <small>(₹${parseInt(d.original_price)})</small></span>
          <span class="badge">${parseInt(d.discount_percent)}% OFF</span>
        </div>
        <div class="actions">
          <a class="btnlink" target="_blank" rel="nofollow sponsored" href="${d.url}">Buy now</a>
          <a class="btnlink ghost" target="_blank" href="https://twitter.com/intent/tweet?text=${encodeURIComponent(d.title)}&url=${encodeURIComponent(d.url)}">Share</a>
        </div>
      </div>`;
    grid.appendChild(el);
  });
  const ld = items.slice(0,12).map(d=>({
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": d.title,
    "image": d.image_url,
    "offers": {
      "@type": "Offer",
      "priceCurrency": "INR",
      "price": String(d.deal_price),
      "url": d.url,
      "availability": "https://schema.org/InStock"
    }
  }));
  $("#ld").textContent = JSON.stringify(ld);
}

function apply(){
  let items = (typeof DEALS !== "undefined" ? DEALS.slice() : []);
  if(state.q){
    const q = state.q.toLowerCase();
    items = items.filter(d => (d.title||"").toLowerCase().includes(q));
  }
  if(state.cat){
    items = items.filter(d => (d.category||"") === state.cat);
  }
  switch(state.sort){
    case "discount": items.sort((a,b)=>(b.discount_percent)-(a.discount_percent)); break;
    case "price_low": items.sort((a,b)=>a.deal_price-b.deal_price); break;
    case "price_high": items.sort((a,b)=>b.deal_price-a.deal_price); break;
    case "new": items.sort((a,b)=>(b.ts||0)-(a.ts||0)); break;
    default: items.sort((a,b)=>(b.score||0)-(a.score||0));
  }
  render(items);
}

window.addEventListener("DOMContentLoaded", ()=>{
  $("#q").addEventListener("input", e=>{ state.q = e.target.value; apply(); });
  $("#cat").addEventListener("change", e=>{ state.cat = e.target.value; apply(); });
  $("#sort").addEventListener("change", e=>{ state.sort = e.target.value; apply(); });
  $("#dark").addEventListener("click", ()=>{
    document.body.classList.toggle("light");
  });
  try { $("#year").textContent = new Date().getFullYear(); } catch(e){}
  apply();
});
