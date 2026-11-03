// Reusable quiz widget. Markup: <div class="q" data-answer="N" data-explain="why">
// <p>Question</p><button>option 0</button>... </div>. data-answer is the 0-based correct index.
document.querySelectorAll('.q').forEach(q=>{
  const btns=[...q.querySelectorAll('button')];
  const fb=document.createElement('div');fb.className='fb';q.appendChild(fb);
  btns.forEach((b,i)=>b.addEventListener('click',()=>{
    const ok=i===+q.dataset.answer;
    b.classList.add(ok?'right':'wrong');
    if(ok){btns.forEach(x=>x.disabled=true);fb.textContent='Correct. '+q.dataset.explain}
    else{b.disabled=true;fb.textContent='Not quite. Try again.'}
  }));
});
