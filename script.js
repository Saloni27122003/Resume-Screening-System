let skills = [];

function addSkill(){
    let val = document.getElementById("skillInput").value;
    if(!val) return;

    skills.push(val);

    let tag = document.createElement("span");
    tag.className="tag";
    tag.innerText=val;

    document.getElementById("skills").appendChild(tag);
}

async function upload(){
    let file = document.getElementById("fileInput").files[0];
    if(!file){ alert("Select file"); return;}

    let formData = new FormData();
    formData.append("file", file);

    await fetch("http://127.0.0.1:5000/upload",{
        method:"POST",
        body:formData
    });

    alert("Uploaded!");
}

async function analyze(){
    document.getElementById("loader").classList.remove("hidden");

    let res = await fetch("http://127.0.0.1:5000/analyze",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({skills})
    });

    let data = await res.json();

    let out = document.getElementById("results");
    out.innerHTML="";

    data.forEach(r=>{
        let div=document.createElement("div");
        div.className="card";

        div.innerHTML=`
        <h3>${r.name}</h3>
        <p>Score: ${r.score}</p>
        <p>Match: ${r.match}%</p>
        <p>Matched: ${r.matched.join(", ")}</p>
        `;

        out.appendChild(div);
    });

    document.getElementById("loader").classList.add("hidden");
}