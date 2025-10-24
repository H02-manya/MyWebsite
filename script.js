// utils
function safePad(n){ return String(n).padStart(2,'0'); }

let keys = [], currentIndex = 0, renderByIndex;

// 初始化阅读器
function initReader(CHAPTERS, chapKey, mangaKey){
  const viewer = document.getElementById('viewer');
  const chapterTitle = document.getElementById('chapterTitle');
  const backBtn = document.getElementById('backBtn');
  const prevBtn = document.getElementById('prevChapter');
  const nextBtn = document.getElementById('nextChapter');
  const fsBtn = document.getElementById('fsBtn');
  const tocBtn = document.getElementById('tocBtn');

  // 构建章节索引
  keys = Object.keys(CHAPTERS).sort((a,b)=> parseInt(a,10)-parseInt(b,10));
  if(keys.length === 0){
    viewer.innerHTML = '<div class="muted">未找到章节数据。</div>';
    return;
  }

  currentIndex = keys.indexOf(chapKey);
  if(currentIndex < 0) currentIndex = 0;

  // 渲染章节
  renderByIndex = function(i){
    if(i<0 || i>=keys.length) return;
    const key = keys[i];
    const ch = CHAPTERS[key];
    chapterTitle.textContent = ch.title || `第${safePad(key)}话`;
    viewer.innerHTML = '';

    const pages = (ch.pages||[]).slice();

    pages.forEach(p=>{
      const img = document.createElement('img');
      img.src = p;  // ✅ 现在每页图片路径在 chapters 文件中已包含完整路径
      img.alt = p;
      img.className = 'manga';
      img.loading = 'lazy';
      viewer.appendChild(img);
    });

    currentIndex = i;
    viewer.scrollTo({top:0, behavior:'instant'});
    updateFirstImageMargin();
  };

  renderByIndex(currentIndex);

  // 按钮事件
  prevBtn.addEventListener('click', ()=>{ if(currentIndex>0){ currentIndex--; renderByIndex(currentIndex); }});
  nextBtn.addEventListener('click', ()=>{ if(currentIndex<keys.length-1){ currentIndex++; renderByIndex(currentIndex); }});
  backBtn.addEventListener('click', ()=> location.href='index.html');
  fsBtn.addEventListener('click', async ()=>{
    if(!document.fullscreenElement) await document.documentElement.requestFullscreen().catch(()=>{});
    else await document.exitFullscreen().catch(()=>{});
  });

  // 自动隐藏 header
  const header = document.querySelector('.reader-header');
  let lastScroll = 0;
  viewer.addEventListener('scroll', ()=>{
    const currentScroll = viewer.scrollTop;
    if(currentScroll > lastScroll && currentScroll > 50){
      header.style.transform='translateY(-100%)';
    } else {
      header.style.transform='translateY(0)';
    }
    lastScroll = currentScroll;
    updateFirstImageMargin();
  });

  tocBtn.addEventListener('click', () => {
    // 从 URL 参数中取 manga 名称
    const params = new URLSearchParams(location.search);
    const mangaName = params.get('manga');
    if (mangaName) {
      location.href = `${mangaName}.html`;
    } else {
      location.href = 'index.html'; // fallback
    }
  });

}

function updateFirstImageMargin(){
  const header = document.querySelector('.reader-header');
  const viewerEl = document.getElementById('viewer');
  const firstImg = viewerEl.querySelector('img');
  if(!firstImg) return;
  if(header.style.transform==='translateY(0)' || header.style.transform===''){
    firstImg.style.marginTop = header.offsetHeight + 'px';
  } else {
    firstImg.style.marginTop = '0px';
  }
}
