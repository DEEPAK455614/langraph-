import os
import time
from flask import Flask, jsonify, request, Response
from workflow import ask_question

app = Flask(__name__)
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

PAGE = r'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GraphMind — LangGraph × Gemini</title><style>
:root{--bg:#06101b;--panel:#0b1524;--line:#1a2a40;--text:#f7fbff;--muted:#8fa0b8;--a:#7c3aed;--b:#4f46e5;--ok:#34d399}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at top left,#141a3a 0,transparent 38%),radial-gradient(circle at top right,#063c45 0,transparent 35%),var(--bg);color:var(--text);font-family:Inter,system-ui,sans-serif;min-height:100vh}.wrap{max-width:1120px;margin:auto;padding:18px}.top,.card{border:1px solid var(--line);background:rgba(8,16,30,.88);backdrop-filter:blur(20px);border-radius:24px}.top{padding:20px 24px;display:flex;justify-content:space-between;align-items:center}.brand{font-size:25px;font-weight:800}.sub{font-size:11px;letter-spacing:.16em;color:var(--muted)}.status{color:#bff5df;font-size:14px;display:flex;gap:8px;align-items:center}.dot{width:9px;height:9px;background:var(--ok);border-radius:50%;box-shadow:0 0 15px var(--ok)}.grid{display:grid;grid-template-columns:310px 1fr;gap:16px;margin-top:16px}.side{padding:22px}.side h2{font-size:28px;line-height:1.05;margin:8px 0}.side p{color:var(--muted);line-height:1.6;font-size:13px}.node{border:1px solid var(--line);padding:12px;border-radius:14px;margin:7px 0;background:#0d1726}.arr{text-align:center;color:#62748f}.tag{display:inline-block;margin:4px 4px 0 0;padding:6px 8px;border:1px solid var(--line);border-radius:9px;color:#aebbd0;font-size:11px}.chat{min-height:720px;display:flex;flex-direction:column;overflow:hidden}.head{padding:20px 24px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between}.head b{font-size:18px}.head span{display:block;color:var(--muted);font-size:12px;margin-top:4px}.btn{border:1px solid var(--line);background:#101b2c;color:#dbe6f5;padding:10px 14px;border-radius:12px}.messages{flex:1;padding:26px;overflow:auto}.welcome{text-align:center;max-width:600px;margin:12vh auto}.welcome h1{font-size:38px;margin-bottom:10px}.welcome p{color:var(--muted);line-height:1.6}.row{display:flex;margin:16px 0}.user{justify-content:flex-end}.bubble{max-width:82%;padding:14px 16px;border-radius:18px;line-height:1.6;white-space:pre-wrap;word-break:break-word}.user .bubble{background:linear-gradient(135deg,var(--a),var(--b))}.assistant .bubble{background:#111b2b;border:1px solid var(--line)}.meta{font-size:10px;color:#6e8099;margin-top:5px}.composer{padding:16px;border-top:1px solid var(--line);display:flex;gap:10px}.composer textarea{flex:1;background:#0b1423;color:#fff;border:1px solid var(--line);border-radius:16px;padding:15px;resize:none;outline:none;font:inherit}.send{width:52px;border:0;border-radius:16px;color:white;background:linear-gradient(135deg,var(--a),#5b6df8);font-size:20px}.error .bubble{border-color:#7f1d1d;color:#fecaca;background:#211014}@media(max-width:860px){.grid{grid-template-columns:1fr}.side{display:none}.chat{min-height:calc(100vh - 120px)}.wrap{padding:10px}.top{border-radius:18px}.status span:last-child{display:none}.messages{padding:18px}.welcome{margin-top:10vh}.welcome h1{font-size:30px}.bubble{max-width:92%}}</style></head><body><div class="wrap"><div class="top"><div><div class="brand">GraphMind</div><div class="sub">LANGGRAPH × GEMINI</div></div><div class="status"><i class="dot"></i><span id="model">Gemini 3.6 Flash</span></div></div><div class="grid"><aside class="card side"><div class="sub">REAL WORKFLOW</div><h2>User Question → Gemini → Answer</h2><p>This demo uses the original LangGraph workflow and calls Gemini on the server. The API key never reaches the browser.</p><div class="node">START</div><div class="arr">↓</div><div class="node">User Question</div><div class="arr">↓</div><div class="node">Gemini LLM Node</div><div class="arr">↓</div><div class="node">Answer</div><div class="arr">↓</div><div class="node">END</div><div style="margin-top:16px"><span class="tag">LangGraph</span><span class="tag">LangChain</span><span class="tag">Gemini API</span><span class="tag">Flask</span><span class="tag">Render</span></div></aside><section class="card chat"><div class="head"><div><b>Gemini Assistant</b><span>Real LangGraph execution</span></div><button class="btn" onclick="newChat()">New chat</button></div><div class="messages" id="messages"><div class="welcome" id="welcome"><h1>Ask Gemini anything.</h1><p>Every message goes through the deployed LangGraph StateGraph and returns the real Gemini response.</p></div></div><div class="composer"><textarea id="input" rows="2" placeholder="Message GraphMind..."></textarea><button class="send" id="send">↑</button></div></section></div></div><script>
const m=document.getElementById('messages'),i=document.getElementById('input'),s=document.getElementById('send');let hist=[];function esc(x){return String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}function add(role,text,meta=''){document.getElementById('welcome')?.remove();const r=document.createElement('div');r.className='row '+role;r.innerHTML='<div><div class="bubble">'+esc(text)+'</div>'+(meta?'<div class="meta">'+esc(meta)+'</div>':'')+'</div>';m.appendChild(r);m.scrollTop=m.scrollHeight}function newChat(){hist=[];m.innerHTML='<div class="welcome" id="welcome"><h1>New conversation</h1><p>Ask your next question.</p></div>';i.focus()}async function send(){const q=i.value.trim();if(!q||s.disabled)return;add('user',q);i.value='';s.disabled=true;const start=performance.now();try{const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q,history:hist.slice(-10)})});const raw=await r.text();let data;try{data=JSON.parse(raw)}catch{throw new Error(raw.slice(0,240)||('HTTP '+r.status))}if(!r.ok)throw new Error(data.error||('HTTP '+r.status));add('assistant',data.answer,'LangGraph → '+data.model+' • '+Math.round(performance.now()-start)+' ms');hist.push({role:'user',content:q},{role:'assistant',content:data.answer})}catch(e){const r=document.createElement('div');r.className='row assistant error';r.innerHTML='<div><div class="bubble">'+esc('Backend error: '+e.message)+'</div><div class="meta">Request failed</div></div>';m.appendChild(r);m.scrollTop=m.scrollHeight}finally{s.disabled=false;i.focus()}}s.onclick=send;i.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send()}});fetch('/health').then(r=>r.json()).then(x=>document.getElementById('model').textContent=x.model).catch(()=>{});
</script></body></html>'''

@app.get("/")
def index():
    return Response(PAGE, mimetype="text/html")

@app.get("/health")
def health():
    return jsonify({"status":"ok","service":"graphmind","model":MODEL,"api_key_configured":bool(os.getenv("GOOGLE_API_KEY"))})

@app.get("/verify")
def verify():
    started=time.perf_counter()
    try:
        answer=ask_question("Reply with exactly: GRAPHMIND_OK")
        return jsonify({"ok":True,"model":MODEL,"answer":answer,"latency_ms":round((time.perf_counter()-started)*1000)})
    except Exception as e:
        app.logger.exception("verify failed")
        return jsonify({"ok":False,"model":MODEL,"error":str(e)}),500

@app.post("/api/chat")
def chat():
    payload=request.get_json(silent=True) or {}
    message=str(payload.get("message","")).strip()
    history=payload.get("history",[])
    if not message:return jsonify({"error":"Message is required."}),400
    if len(message)>12000:return jsonify({"error":"Message is too long."}),400
    try:
        answer=ask_question(message,history if isinstance(history,list) else [])
        return jsonify({"answer":answer,"model":MODEL})
    except Exception as e:
        app.logger.exception("chat failed")
        return jsonify({"error":str(e),"model":MODEL}),500
