function fillQ(text){const q=document.getElementById("question"); if(q){q.value=text;q.focus();}}
document.addEventListener("DOMContentLoaded",()=>{document.querySelectorAll(".poster").forEach((p,i)=>{p.style.setProperty("--hue",(i*47+30)%360);});});
