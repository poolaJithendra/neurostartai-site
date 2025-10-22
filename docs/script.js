(function(){
  if (typeof DEALS === "undefined") {
    window.DEALS = [
      { title: "Boat Airdopes 141", category: "Digital & Gadgets", image_url: "https://m.media-amazon.com/images/I/51HBom8xz7L._SL1500_.jpg", deal_price: 1099, original_price: 2999, discount_percent: 63, url: "#", score: 90, ts: Date.now() },
      { title: "Minimalist Sunscreen SPF 50", category: "Beauty", image_url: "https://m.media-amazon.com/images/I/51x2bQ4kHhL._SL1000_.jpg", deal_price: 399, original_price: 599, discount_percent: 33, url: "#", score: 80, ts: Date.now() }
    ];
  }
})();

const $ = (q)=>document.querySelector(q);
const grid = $("#grid");
const search = $("#search");
const catSel = $("#category");
const sortSel = $("#sort");
const compareDrawer = $("#compareDrawer");
const compareGrid = $("#compareGrid");
const closeCompareBtn = $("#closeCompare");
const modal = $("#dealModal");
const yearEl = $("#year");

function fmtINR(n){ try{ return "₹" + parseInt(n).toLocaleString("en-IN"); }catch(e){ return "₹" + n; } }
function pct(n){ return parseInt(n) + "% OFF"; }

const state = {
  q: "",
  cat: "",
  sort: "score",
  likes: new Set(JSON.parse(localStorage.getItem("likes")||"[]")),
  dislikes: new Set(JSON.parse(localStorage.getItem("dislikes")||"[]")),
  saved: new Set(JSON.parse(localStorage.getItem("saved")||"[]")),
  compare: JSON.parse(localStorage.getItem("compare")||"[]"),
  theme: localStorage.getItem("theme") || "light"
};

function persist(){
  localStorage.setItem("likes", JSON.stringify([...state.likes]));
  localStorage.setItem("dislikes", JSON.stringify([...state.dislikes]));
  localStorage.setItem("saved", JSON.stringify([...state.saved]));
  localStorage.setItem("compare", JSON.stringify(state.compare));
  localStorage.setItem("theme", state.theme);
}

function toast(msg){
  const t = document.createElement("div");
  t.className = "fixed bottom-5 left-1/2 -translate-x-1/2 bg-black text-white px-4 py-2 rounded-xl text-sm z-40";
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(()=>{ t.remove(); }, 1500);
}

function render(items){
  if(!grid) return;
  grid.innerHTML = "";
  items.forEach((d, idx)=>{
    const id = d.title;
    const liked = state.likes.has(id);
    const saved = state.saved.has(id);
    const cmpIdx = state.compare.findIndex(x=>x.title===d.title);
    const el = document.createElement("div");
    el.className = "card group";
    el.innerHTML = `
      <div class="relative cursor-pointer" data-open-modal="${idx}">
        <img src="${d.image_url}" alt="${d.title}"/>
        <span class="badge">${parseInt(d.discount_percent)}% OFF</span>
      </div>
      <div class="p-4">
        <div class="font-semibold line-clamp-2">${d.title}</div>
        <div class="mt-1 flex items-center gap-3">
          <span class="price">${fmtINR(d.deal_price)}</span>
          <span class="text-slate-500 line-through text-sm">${fmtINR(d.original_price)}</span>
        </div>
        <div class="actions">
          <button class="btn" data-save="${id}">${saved?"💖 Saved":"❤️ Save"}</button>
          <button class="btn" data-like="${id}">${liked?"👍 Liked":"👍 Like"}</button>
          <button class="btn" data-compare='${JSON.stringify(d)}'>${cmpIdx>-1?"📊 In Compare":"📊 Compare"}</button>
          <a class="btn col-span-3 text-center" target="_blank" rel="nofollow sponsored" href="${d.url}">↗️ Buy Now</a>
        </div>
      </div>
    `;
    grid.appendChild(el);
  });

  grid.querySelectorAll("[data-open-modal]").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      const idx = parseInt(btn.getAttribute("data-open-modal"));
      openModal(items[idx]);
    });
  });
  grid.querySelectorAll("[data-save]").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      const id = btn.getAttribute("data-save");
      if(state.saved.has(id)){ state.saved.delete(id); toast("Removed from Saved"); }
      else{ state.saved.add(id); toast("Saved!"); }
      persist(); apply();
    });
  });
  grid.querySelectorAll("[data-like]").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      const id = btn.getAttribute("data-like");
      if(state.likes.has(id)){ state.likes.delete(id); toast("Removed Like"); }
      else{ state.likes.add(id); state.dislikes.delete(id); toast("Liked"); }
      persist(); apply();
    });
  });
  grid.querySelectorAll("[data-compare]").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      const d = JSON.parse(btn.getAttribute("data-compare"));
      const exists = state.compare.findIndex(x=>x.title===d.title);
      if(exists>-1){ state.compare.splice(exists,1); toast("Removed from Compare"); }
      else{
        if(state.compare.length>=4){ state.compare.shift(); }
        state.compare.push(d); toast("Added to Compare");
      }
      persist(); renderCompare();
    });
  });
}

function filterSort(list){
  let items = list.slice();
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
  return items;
}

function apply(){
  const items = filterSort((typeof DEALS !== "undefined" ? DEALS : []));
  render(items);
}

function openModal(d){
  if(!modal) return;
  modal.classList.remove("hidden"); modal.classList.add("flex");
  document.querySelector("#modalImage").src = d.image_url;
  document.querySelector("#modalTitle").textContent = d.title;
  document.querySelector("#modalDesc").textContent = d.category || "";
  document.querySelector("#modalPriceNow").textContent = fmtINR(d.deal_price);
  document.querySelector("#modalPriceWas").textContent = fmtINR(d.original_price);
  document.querySelector("#modalOff").textContent = parseInt(d.discount_percent) + "% OFF";
  document.querySelector("#btnBuyModal").href = d.url;
  document.querySelector("#btnSaveModal").onclick = ()=>{ const id = d.title; if(state.saved.has(id)){ state.saved.delete(id); toast("Removed from Saved"); } else { state.saved.add(id); toast("Saved!"); } persist(); };
  document.querySelector("#btnLikeModal").onclick = ()=>{ state.likes.add(d.title); state.dislikes.delete(d.title); persist(); toast("Liked"); };
  document.querySelector("#btnDislikeModal").onclick = ()=>{ state.dislikes.add(d.title); state.likes.delete(d.title); persist(); toast("Disliked"); };
  document.querySelector("#btnCompareModal").onclick = ()=>{ const exists = state.compare.findIndex(x=>x.title===d.title); if(exists>-1){ state.compare.splice(exists,1); toast("Removed from Compare"); } else { if(state.compare.length>=4){ state.compare.shift(); } state.compare.push(d); toast("Added to Compare"); } persist(); renderCompare(); };
  modal.querySelector("[data-close-modal]").onclick = ()=>{ modal.classList.add("hidden"); modal.classList.remove("flex"); };
}

function renderCompare(){
  if(!compareGrid) return;
  compareGrid.innerHTML = state.compare.map(c=>`
    <div class="border border-slate-200 rounded-xl p-2">
      <img class="w-full h-28 object-cover rounded-md" src="${c.image_url}" alt="${c.title}">
      <div class="font-semibold text-sm mt-1 line-clamp-2">${c.title}</div>
      <div class="text-blue-700 font-bold text-sm">${fmtINR(c.deal_price)}</div>
    </div>
  `).join("");
  if(state.compare.length>0){
    compareDrawer.style.transform = "translateY(0)";
  }
  closeCompareBtn && closeCompareBtn.addEventListener("click", ()=>{
    compareDrawer.style.transform = "translateY(100%)";
  });
}

function renderSaved(){
  const savedGrid = document.querySelector("#savedGrid");
  if(!savedGrid) return;
  const items = (typeof DEALS !== "undefined" ? DEALS : []).filter(d=>state.saved.has(d.title));
  if(items.length===0){
    savedGrid.innerHTML = "<div class='text-slate-500'>No saved deals yet.</div>";
    return;
  }
  const original = grid;
  window.grid = savedGrid;
  render(items);
  window.grid = original;
}

function renderFeed(){
  const feedGrid = document.querySelector("#feedGrid");
  if(!feedGrid) return;
  const likedCats = new Set();
  (typeof DEALS !== "undefined" ? DEALS : []).forEach(d=>{
    if(state.likes.has(d.title) && d.category) likedCats.add(d.category);
  });
  let items = (typeof DEALS !== "undefined" ? DEALS : []).slice();
  items.sort((a,b)=>{
    const aBoost = likedCats.has(a.category)?1:0;
    const bBoost = likedCats.has(b.category)?1:0;
    return (bBoost - aBoost) || ((b.score||0)-(a.score||0));
  });
  const original = grid;
  window.grid = feedGrid;
  render(items.slice(0,24));
  window.grid = original;
}

search && search.addEventListener("input", e=>{ state.q = e.target.value; apply(); });
catSel && catSel.addEventListener("change", e=>{ state.cat = e.target.value; apply(); });
sortSel && sortSel.addEventListener("change", e=>{ state.sort = e.target.value; apply(); });

const toggleTheme = document.querySelector("#toggleTheme");
if(toggleTheme){
  if(state.theme==="dark"){ document.documentElement.classList.add("dark"); toggleTheme.textContent="☀️ Light"; }
  toggleTheme.addEventListener("click", ()=>{
    document.documentElement.classList.toggle("dark");
    state.theme = document.documentElement.classList.contains("dark") ? "dark" : "light";
    toggleTheme.textContent = state.theme==="dark" ? "☀️ Light" : "🌙 Dark";
    persist();
  });
}

const yearEl = document.querySelector("#year");
if(yearEl) yearEl.textContent = new Date().getFullYear();

renderCompare();
apply();
renderSaved();
renderFeed();
