/* Explicit language choice. No forced redirects or automatic translation. */
(()=>{document.querySelectorAll('.language-switch a').forEach(a=>{const target=new URL(a.href);target.search=location.search;target.hash=location.hash;a.href=target.pathname+target.search+target.hash;});})();
