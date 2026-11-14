/** Publish the approved B2B series after the legacy Python build. No external dependencies. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
function publishB2B(inputs,articles){
const B="https://mood-agency.com";
const esc=s=>String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");
const json=s=>JSON.stringify(s).replaceAll("<","\\u003c");
const template=inputs["blog/automatizar-seguimiento-comercial/index.html"];
const originalGraph=JSON.parse(template.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1])["@graph"];
const outputs={};
for(const a of articles){
 const url=B+"/blog/"+a.slug+"/", full=a.seo_title+" | Mood Agency",image=B+a.image;
 let html=template.replace(/<title>[\s\S]*?<\/title>/,"<title>"+esc(full)+"</title>");
 const metadata={"description":a.summary,"og:title":full,"og:description":a.summary,"og:url":url,"og:image":image,"og:image:width":a.image_width,"og:image:height":a.image_height,"og:image:alt":a.image_alt,"twitter:title":full,"twitter:description":a.summary,"twitter:image":image,"twitter:image:alt":a.image_alt,"article:published_time":a.datePublished,"article:modified_time":a.dateModified};
 for(const [key,value] of Object.entries(metadata))html=html.replace(new RegExp('<meta (name|property)="'+key+'" content="[^"]*">'),(_,attr)=>`<meta ${attr}="${key}" content="${esc(value)}">`);
 html=html.replace(/<link rel="canonical" href="[^"]*">/,`<link rel="canonical" href="${url}">`);
 const graph=originalGraph.filter(n=>["Organization","WebSite"].includes(n["@type"]));
 graph.push({"@type":"WebPage","@id":url+"#page",url,name:a.title,description:a.summary,inLanguage:"es-MX",isPartOf:{"@id":B+"/#website"},primaryImageOfPage:{"@id":url+"#primaryimage"}});
 graph.push({"@type":"BreadcrumbList",itemListElement:[["Inicio",B+"/"],["Blog",B+"/blog/"],[a.title,url]].map(([name,item],i)=>({"@type":"ListItem",position:i+1,name,item}))});
 graph.push({"@type":"ImageObject","@id":url+"#primaryimage",url:image,contentUrl:image,width:a.image_width,height:a.image_height,caption:a.image_alt});
 graph.push({"@type":"Article","@id":url+"#article",headline:a.title,description:a.summary,inLanguage:"es-MX",datePublished:a.datePublished,dateModified:a.dateModified,mainEntityOfPage:{"@id":url+"#page"},author:{"@id":B+"/#organization"},publisher:{"@id":B+"/#organization"},image:{"@id":url+"#primaryimage"}});
 // FAQ remains visible in the article; no promise of rich-result eligibility.
 html=html.replace(/<script type="application\/ld\+json">[\s\S]*?<\/script>/,`<script type="application/ld+json">${json({"@context":"https://schema.org","@graph":graph})}</script>`);
 const toc=[...a.body.matchAll(/<h2>(.*?)<\/h2>/g)].map((m,i)=>({label:m[1].replace(/<[^>]+>/g,""),id:"seccion-"+(i+1)}));
 let c=0;const articleBody=a.body.replace(/<h2>/g,()=>`<h2 id="seccion-${++c}">`);
 const related=a.related.map(slug=>articles.find(x=>x.slug===slug)).filter(Boolean);
 const dateText=a.slug==="automatizar-seguimiento-comercial"?'Publicado el <time datetime="2026-11-13">13 de noviembre de 2026</time> · Actualizado el <time datetime="2026-11-14">14 de noviembre de 2026</time>':'Publicado el <time datetime="2026-11-14">14 de noviembre de 2026</time>';
 const main=`<main id="contenido"><section class="section"><div class="wrap"><nav class="breadcrumb" aria-label="Ruta de navegación"><a href="/">Inicio</a> / <a href="/blog/">Blog</a></nav><p class="eyebrow">${esc(a.category)}</p><h1 style="font-size:clamp(32px,5.5vw,76px);overflow-wrap:anywhere">${esc(a.title)}</h1><p class="lede">${esc(a.summary)}</p></div></section><section class="section"><div class="wrap"><article class="narrow prose"><p class="muted">Por <a href="/nosotros/">Mood Agency</a> · ${dateText}</p><figure style="margin:24px 0"><img src="${a.image}" width="${a.image_width}" height="${a.image_height}" alt="${esc(a.image_alt)}" loading="eager" fetchpriority="high" decoding="async" style="display:block;width:100%;height:auto;border-radius:20px"><figcaption class="small">Ilustración editorial generada con IA para Mood Agency.</figcaption></figure><details class="service-card"><summary>En esta guía</summary><ul>${toc.map(t=>`<li><a href="#${t.id}">${esc(t.label)}</a></li>`).join("")}</ul></details>${articleBody}${a.sources.length?`<h2>Fuentes y documentación</h2><ul>${a.sources.map(([label,href])=>`<li><a href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(label)}</a></li>`).join("")}</ul>`:""}<p class="note">Los ejemplos y las plantillas son orientativos. Adapta los criterios a tu operación y verifica la información antes de usarla comercialmente.</p><aside><h2>Continúa con estas guías</h2><ul>${related.map(r=>`<li><a href="/blog/${r.slug}/">${esc(r.title)}</a></li>`).join("")}</ul></aside><div class="service-card"><h2>De la idea a tu operación</h2><p>Cuéntanos qué vende tu empresa, a quién atiende y qué quieres mejorar.</p><a href="/contacto/" class="btn" data-cta="article-b2b">Hablemos de tu proyecto</a></div></article></div></section></main>`;
 html=html.replace(/<main id="contenido">[\s\S]*?<\/main>/,main);
 outputs["blog/"+a.slug+"/index.html"]=html;
}
let blog=inputs["blog/index.html"];
for(const a of articles)blog=blog.replace(new RegExp('<a class="card service-card" href="/blog/'+a.slug+'/">[\\s\\S]*?</a>','g'),"");
const cards=articles.map(a=>`<a class="card service-card" href="/blog/${a.slug}/"><img src="${a.image}" alt="${esc(a.image_alt)}" width="${a.image_width}" height="${a.image_height}" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;border-radius:12px;margin-bottom:18px"><p class="eyebrow">${esc(a.category)}</p><h3>${esc(a.title)}</h3><p>${esc(a.summary)}</p><span>Leer guía →</span></a>`).join("");
blog=blog.replace('<div class="grid">','<div class="grid">'+cards);
outputs["blog/index.html"]=blog;
let sitemap=inputs["sitemap.xml"];
for(const a of articles){
 const url=B+"/blog/"+a.slug+"/";
 sitemap=sitemap.replace(new RegExp("<url>\\s*<loc>"+url.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+"<\\/loc>[\\s\\S]*?<\\/url>","g"),"");
 sitemap=sitemap.replace("</urlset>",`<url><loc>${url}</loc><lastmod>2026-11-14</lastmod></url></urlset>`);
}
sitemap=sitemap.replace(/(<loc>https:\/\/mood-agency.com\/blog\/<\/loc><lastmod>)[^<]+/,"$12026-11-14");
outputs["sitemap.xml"]=sitemap;
const section="\n## Guías prácticas B2B publicadas el 14 de noviembre de 2026\n"+articles.map(a=>`- [${a.title}](${B}/blog/${a.slug}/): ${a.summary}`).join("\n")+"\n";
for(const path of ["llms.txt","llms-full.txt"])outputs[path]=inputs[path].replace(/\n## Guías prácticas B2B publicadas el 14 de noviembre de 2026[\s\S]*$/,"")+section;
const old=JSON.parse(inputs["src/articles.json"]);
const merged=old.map(x=>articles.find(a=>a.slug===x.slug)||x);
for(const a of articles)if(!merged.some(x=>x.slug===a.slug))merged.push(a);
outputs["src/articles.json"]=JSON.stringify(merged,null,2)+"\n";
let manifest=JSON.parse(inputs["src/page-manifest.json"]);
for(const a of articles){const p={path:"/blog/"+a.slug+"/",title:a.seo_title,description:a.summary};const i=manifest.findIndex(x=>x.path===p.path);if(i>=0)manifest[i]=p;else manifest.push(p);}
outputs["src/page-manifest.json"]=JSON.stringify(manifest,null,2)+"\n";
return outputs;
}
const inputNames=["blog/automatizar-seguimiento-comercial/index.html","blog/index.html","sitemap.xml","llms.txt","llms-full.txt","src/articles.json","src/page-manifest.json"];
const inputs=Object.fromEntries(inputNames.map(p=>[p,fs.readFileSync(path.join(root,p),'utf8')]));
const articles=JSON.parse(inputs['src/articles.json']).filter(a=>a.b2b);
if(articles.length!==13)throw new Error('Expected the 13 approved B2B articles');
const output=publishB2B(inputs,articles);
for(const [p,content] of Object.entries(output)) {const dest=path.join(root,p);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,content);}
console.log(JSON.stringify({b2bArticles:articles.length,written:Object.keys(output).length}));
