(() => { 'use strict';
 const dialog=document.getElementById('md-lightbox');if(!dialog)return;
 let trigger;
 document.querySelectorAll('.md-zoom').forEach(button=>button.addEventListener('click',()=>{const image=button.querySelector('img');trigger=button;const large=dialog.querySelector('img');large.src=button.dataset.full;large.alt=image.alt;dialog.querySelector('p').textContent=image.alt;dialog.showModal();}));
 dialog.querySelector('.md-close').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('click',event=>{if(event.target===dialog){const box=dialog.getBoundingClientRect();if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)dialog.close();}});
 dialog.addEventListener('close',()=>trigger?.focus());
})();
