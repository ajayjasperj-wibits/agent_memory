from fastapi.responses import HTMLResponse


UI_HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agent Memory</title><style>
:root{font:14px system-ui;color:#17202a;background:#f5f7fb}*{box-sizing:border-box}body{margin:0}.top{background:#17202a;color:white;padding:20px 5vw;display:flex;justify-content:space-between;align-items:center}.top h1{margin:0;font-size:20px}.wrap{max-width:1400px;margin:24px auto;padding:0 20px}.bar,.card{background:white;border:1px solid #e4e8ef;border-radius:14px;padding:16px;margin-bottom:16px;box-shadow:0 3px 14px #1822300a}.bar{display:flex;gap:10px;flex-wrap:wrap}.tabs{overflow:auto}.tabs button,button{border:0;border-radius:9px;padding:10px 14px;background:#eef2f7;color:#17202a;cursor:pointer;white-space:nowrap}.tabs button.active,button.primary{background:#2563eb;color:white}.key{flex:1;min-width:220px}input,select{border:1px solid #d7dde7;border-radius:9px;padding:10px;font:inherit}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}.metric strong{display:block;font-size:28px;margin-top:6px}.muted{color:#687386}.table{overflow:auto}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:12px;border-bottom:1px solid #edf0f4;white-space:nowrap}th{color:#687386;font-size:12px;text-transform:uppercase}tbody tr{cursor:pointer}tbody tr:hover{background:#f8f9fb}.error{color:#b42318;background:#fff1f0;padding:12px;border-radius:9px}.empty{padding:30px;text-align:center;color:#687386}.row{display:flex;align-items:center;justify-content:space-between;gap:12px}.detail{width:min(900px,94vw);max-height:85vh;border:0;border-radius:16px;padding:0;box-shadow:0 20px 80px #0003}.detail::backdrop{background:#1118}.detail-head{position:sticky;top:0;background:white;padding:16px 20px;border-bottom:1px solid #edf0f4;display:flex;justify-content:space-between}.detail-body{padding:18px 20px;overflow:auto;max-height:72vh}.json{white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f7fb;border-radius:10px;padding:14px;font:12px ui-monospace,monospace}.event{border-left:3px solid #2563eb;padding:4px 0 12px 14px;margin:0 0 10px 6px}.pager{display:flex;justify-content:flex-end;gap:8px;margin-top:14px}@media(max-width:600px){.top{padding:16px 20px}.wrap{margin-top:16px}}
</style><link href="https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.snow.css" rel="stylesheet"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Geist:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><script src="https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.js"></script><style>
label{display:grid;gap:7px;font-weight:600;margin:12px 0}label input,label select{width:100%;font-weight:400}.quill-editor{background:white;border-radius:0 0 9px 9px}.quill-editor .ql-editor{min-height:220px;font:15px/1.6 system-ui}.drop-zone{border:2px dashed #cbd5e1;border-radius:12px;padding:22px;display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:16px;background:#fafbfc}.drop-zone.dragging{border-color:#2563eb;background:#eff6ff}.task-file{display:flex;justify-content:space-between;gap:12px;padding:8px;border-bottom:1px solid #edf0f4}.pill{display:inline-flex;border-radius:99px;padding:4px 9px;font-size:12px;font-weight:700;background:#eef2f7}.pill.open{color:#1d4ed8;background:#dbeafe}.pill.working{color:#075985;background:#e0f2fe}.pill.done{color:#166534;background:#dcfce7}.priority.urgent{color:#b42318}.priority.high{color:#2563eb}.priority.normal{color:#475569}.priority.low{color:#64748b}.task-body{line-height:1.65;overflow-wrap:anywhere}.task-body pre{white-space:pre-wrap;background:#f5f7fb;padding:12px;border-radius:8px}.task-body img,.task-body iframe{max-width:100%}.task-attachments{display:grid;gap:8px}.path{font:12px ui-monospace,monospace;overflow-wrap:anywhere;color:#475569}

.task-screen{max-width:none;margin:0}.task-heading{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:16px}.task-eyebrow{font-size:11px;font-weight:700;letter-spacing:1.8px;color:#7b8494}.task-heading h2{font-size:24px;letter-spacing:-.5px;margin:4px 0;color:#17202a}.task-heading p{color:#687386;margin:0;line-height:1.6}.task-create{display:flex;align-items:center;gap:8px;padding:12px 18px;font-weight:650;box-shadow:0 3px 8px rgba(37,99,235,0.2)}.task-create span{font-size:21px}.task-panel{background:#fff;border:1px solid #e2e7ee;border-radius:16px;overflow:hidden;box-shadow:0 6px 24px #18223005}.task-toolbar{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:12px 16px;background:#fcfdff;border-bottom:1px solid #edf0f4}.task-filter-group{display:flex;gap:16px;flex-wrap:wrap}.task-filter-group label{margin:0;display:flex;align-items:center;gap:10px;color:#647084;font-size:12px}.task-filter-group select{min-width:130px;background:white;padding:8px 12px;color:#25344b}.task-toggle{display:flex;align-items:center;gap:9px;font-size:12px;color:#526075;margin:0;white-space:nowrap}.task-toggle input{width:16px;height:16px;accent-color:#2563eb}.task-results-line{padding:8px 16px;display:flex;align-items:center;justify-content:space-between;color:#7b8494;font-size:12px}.task-results-line button{background:none;color:#687386;font-size:12px;padding:4px}.task-table th{background:#f8fafc;color:#788396;font-size:10px;letter-spacing:.8px;padding:12px}.task-table td{padding:12px}.task-table tbody tr{cursor:default}.task-title-cell{width:auto;min-width:180px;white-space:normal}.task-title-link{background:none;padding:0;text-align:left;white-space:normal;font-size:14px;font-weight:650;line-height:1.5;color:#25344b}.task-title-link:hover{color:#2563eb;text-decoration:underline}.task-subline{display:flex;align-items:center;gap:10px;flex-wrap:wrap;color:#8892a3;font-size:12px;margin-top:3px}.review-label{color:#2563eb;background:#eff6ff;border:1px solid #dbeafe;border-radius:5px;padding:2px 6px;font-size:10px}.task-table .pill{text-transform:capitalize;font-weight:600;gap:6px;align-items:center;padding:5px 10px}.task-table .pill:before{content:'';width:5px;height:5px;border-radius:50%;background:currentColor}.task-priority{text-transform:capitalize;font-size:12px;color:#677489}.task-priority span{font-size:9px;margin-right:4px}.task-priority.urgent{color:#c13e45}.task-priority.high{color:#2563eb}.task-priority.low{color:#94a0b0}.task-assignee{font-size:12px;color:#647084}.task-date{font-size:12px;color:#526075}.task-date small{display:inline;margin-left:6px;color:#929baa;font-size:11px}.task-footer{padding:0 12px 12px}.task-empty{text-align:center;padding:24px}.task-empty>div{width:48px;height:48px;border-radius:14px;background:#eff6ff;color:#2563eb;display:grid;place-items:center;margin:auto;font-size:24px}.task-empty h3{font-size:18px;margin:20px 0 8px}.task-empty p{color:#7b8494;max-width:330px;margin:0 auto 24px;line-height:1.7}.task-screen button:focus-visible{outline:3px solid #3b82f6;outline-offset:3px}@media(max-width:640px){.task-screen{margin:0}.task-heading{align-items:flex-start;gap:12px}.task-heading h2{font-size:27px}.task-heading p{font-size:12px}.task-create{padding:10px;font-size:12px}.task-toolbar{align-items:flex-start;flex-direction:column;padding:16px;gap:16px}.task-filter-group{width:100%;gap:12px}.task-filter-group label{display:grid;flex:1}.task-filter-group select{min-width:0;width:100%}.task-table td,.task-table th{padding:12px}.task-results-line{padding:14px 16px}.task-title-cell{min-width:180px}}
.task-action-group{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.task-action-group button{font-size:12px;padding:8px 11px}.task-action-group .task-delete{color:#b42318;background:#fff1f0}.task-action-group button:disabled{opacity:.45;cursor:default}#detail-body>.task-action-group{justify-content:flex-end;margin-bottom:18px}#task-editor .detail-head{z-index:5;flex-shrink:0}#task-editor[open]{display:flex;flex-direction:column}#task-editor .detail-body{min-height:0;overflow:auto}#task-submit{font-weight:650}#detail .detail-head{z-index:5;flex-shrink:0;gap:12px}#detail[open]{display:flex;flex-direction:column}#detail .detail-body{min-height:0;overflow:auto}#detail-approve[hidden]{display:none!important}.task-table .member-status-edge{text-align:right;width:1%;white-space:nowrap}.member-status-select{font-size:12px;padding:6px 24px 6px 9px;border:1px solid #d7dde7;border-radius:6px;background-color:#fff;color:#344054;min-width:108px;cursor:pointer}.member-status-select:disabled{opacity:.6}
/* AuraOps Stitch redesign */
:root{font:14px Inter,system-ui,sans-serif;color:#191c1e;background:#f7f9fb;--accent:#2563eb;--accent-dark:#1d4ed8;--ink:#191c1e;--muted:#667085;--line:#e2e7ec;--surface:#fff;--soft:#f1f4f7}body{display:grid;grid-template-columns:240px minmax(0,1fr);grid-template-rows:72px 1fr;min-height:100vh;background:#f7f9fb}.sidebar{grid-row:1/3;background:#f1f4f7;border-right:1px solid #dde3e8;display:flex;flex-direction:column;position:sticky;top:0;height:100vh;z-index:20}.brand{height:72px;display:flex;align-items:center;gap:12px;padding:0 22px;border-bottom:1px solid #dde3e8;font:600 17px Geist}.brand-mark{width:38px;height:38px;border-radius:9px;background:linear-gradient(145deg,#2563eb,#1e40af);color:#fff;display:grid;place-items:center;font-size:20px;box-shadow:inset 0 0 0 1px #fff3}.system-state{padding:16px 22px;color:#52606d;font-size:12px;border-bottom:1px solid #e2e7ec}.live-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#12b76a;margin-right:8px;box-shadow:0 0 0 3px #12b76a18}.tabs{display:grid;gap:4px;padding:16px 12px;overflow:auto}.tabs button{display:flex;align-items:center;gap:12px;width:100%;text-align:left;padding:11px 13px;border-radius:8px;background:transparent;color:#344054;font-weight:500}.tabs button:before{content:attr(data-icon);width:18px;text-align:center;font-size:16px}.tabs button:hover{background:#e7eaed}.tabs button.active{background:var(--ui-accent);color:#fff;box-shadow:0 2px 5px rgba(37,99,235,0.2)}.sidebar-foot{margin-top:auto;border-top:1px solid #dde3e8;padding:16px 20px;font-size:12px;color:#667085;display:flex;justify-content:space-between}.top{grid-column:2;grid-row:1;background:#fff;color:var(--ink);padding:12px 28px;border-bottom:1px solid #e1e6eb;display:flex;align-items:center;gap:14px;position:sticky;top:0;z-index:15}.global-search{position:relative;flex:1;max-width:560px}.global-search:before{content:'⌕';position:absolute;left:14px;top:8px;color:#667085;font-size:20px}.global-search input{width:100%;padding:11px 14px 11px 42px;background:#f5f7f9;border-color:#dce2e7}.key-wrap{display:flex;align-items:center;gap:8px;padding:5px 8px;background:#f6f7f8;border:1px solid #e2e7ec;border-radius:8px}.key-wrap:before{content:'⚿';color:#475467}.key-wrap input{width:130px;border:0;background:transparent;padding:6px}.refresh-btn{background:#fff;border:1px solid #dfe4e8}.user-chip{margin-left:auto;display:flex;align-items:center;gap:10px;padding-left:14px;border-left:1px solid #e2e7ec}.avatar{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:var(--ui-accent);color:#fff;font-weight:700}.user-chip strong{display:block;font-size:12px}.user-chip small{color:var(--ui-accent)}.wrap{grid-column:2;grid-row:2;width:100%;max-width:none;margin:0;padding:32px clamp(20px,3vw,48px)}button{font-family:Inter;border-radius:7px;transition:.16s ease}button:hover{transform:translateY(-1px)}button.primary{background:var(--ui-accent);box-shadow:0 2px 5px rgba(37,99,235,0.15)}button.primary:hover{background:var(--ui-accent-dark)}input,select{border-color:#d9e0e6;background:#fff}.card,.task-panel{border-color:#e0e5ea;border-radius:12px;box-shadow:0 1px 3px #0f172a12}.metric{min-height:150px;padding:24px}.metric span{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#475569}.metric strong{font:600 36px Geist;margin-top:22px}.grid{gap:20px}.table table{font-size:13px}th{background:#f5f7f9;color:#667085;letter-spacing:.06em}th,td{padding:15px 18px}.task-heading h2{font:600 32px Geist}.task-heading{margin-bottom:22px}.task-eyebrow{color:var(--ui-accent)}.task-toolbar{padding:16px 20px}.detail{border-radius:12px}.detail[open]{margin:0 0 0 auto;width:min(640px,96vw);height:100vh;max-height:100vh;border-radius:0;box-shadow:-18px 0 60px #0f172a24}.detail::backdrop{background:#18223066;backdrop-filter:blur(2px)}.detail-head{padding:20px 24px}.detail-body{padding:24px;max-height:none}.approval-banner{padding:20px;border:1px solid #bfdbfe;border-radius:12px;background:linear-gradient(100deg,#dbeafe,#fff);margin-bottom:22px}.approval-banner strong{font:600 18px Geist}.approval-banner p{color:#475569;line-height:1.6}.danger{color:#b42318}.empty{padding:56px 24px}.pager button{border:1px solid #dce2e7;background:#fff}@media(max-width:900px){body{grid-template-columns:74px minmax(0,1fr)}.brand{padding:0 17px}.brand-name,.system-state,.tabs button span,.sidebar-foot span:first-child{display:none}.tabs button{justify-content:center;padding:12px}.top,.wrap{grid-column:2}.user-copy,#updated{display:none}}@media(max-width:640px){body{display:block}.sidebar{position:fixed;left:0;right:0;bottom:0;top:auto;width:100%;height:64px;z-index:40;border:0;border-top:1px solid #dce2e7}.brand,.system-state,.sidebar-foot{display:none}.tabs{display:flex;padding:8px;overflow-x:auto}.tabs button{min-width:54px;padding:10px}.top{position:sticky;height:64px;padding:8px 12px}.key-wrap,.refresh-btn,.user-chip{display:none}.wrap{padding:20px 14px 88px}.metric{min-height:118px}.task-heading h2{font-size:26px}.detail[open]{width:100vw}.task-heading{align-items:center}}
</style></head><body><aside class="sidebar"><div class="brand"><span class="brand-mark">◉</span><span class="brand-name">Agent Memory</span></div><div class="system-state"><span class="live-dot"></span><span id="status">Disconnected</span></div><nav class="tabs" id="sidebar-navigation" aria-label="Main navigation"><div class="nav-group"><div class="nav-group-label">Workspace</div><button class="active" title="Overview" aria-label="Overview" data-tab="overview" data-icon="▦"><span>Overview</span></button><button title="Tasks" aria-label="Tasks" data-tab="tasks" data-icon="✓"><span>Tasks</span></button><button title="Projects" aria-label="Projects" data-tab="projects" data-icon="□"><span>Projects</span></button></div><div class="nav-group"><div class="nav-group-label">Knowledge</div><button title="Memories" aria-label="Memories" data-tab="memories" data-icon="◉"><span>Memories</span></button><button title="Instructions" aria-label="Instructions" data-tab="instructions" data-icon="≡"><span>Instructions</span></button></div><div class="nav-group"><div class="nav-group-label">Administration</div><button title="Agents" aria-label="Agents" data-tab="agents" data-icon="♙"><span>Agents</span></button><button title="Sessions & events" aria-label="Sessions & events" data-tab="sessions" data-icon="◴"><span>Sessions &amp; events</span></button><button title="Audit" aria-label="Audit" data-tab="audit" data-icon="◇"><span>Audit</span></button><button title="Members" aria-label="Members" data-tab="members" data-icon="♧"><span>Members</span></button></div></nav><div class="sidebar-foot" role="status" aria-label="Cluster sync: Healthy" title="Cluster sync: Healthy"><div class="sidebar-sync-icon" aria-hidden="true"><svg class="uicon" viewBox="0 0 24 24" fill="none"><path d="m7 12 3 3 7-7"/></svg></div><div class="sidebar-sync-copy"><strong>Cluster sync</strong><small>Healthy</small></div></div></aside><header class="top"><div class="global-search"><input id="q" placeholder="Global search memories, tasks, agents…" aria-label="Global search"></div><div class="key-wrap"><input id="key" type="password" placeholder="X-API-Key" aria-label="API key"></div><button class="refresh-btn" onclick="load()">Refresh</button><span class="muted" id="updated">Auto-refresh · 5s</span><div class="user-chip"><span class="avatar">AM</span><span class="user-copy"><strong>Workspace Admin</strong><small>Admin role</small></span></div></header><main class="wrap">
<section id="error"></section><section id="app"></section></main><dialog id="detail" class="detail"><div class="detail-head"><strong id="detail-title">Record details</strong><div class="task-action-group"><span id="detail-task-actions" class="task-action-group"></span><button id="detail-approve" class="primary" hidden>Approve task</button><button id="detail-back" type="button" onclick="$('detail').close()">Back</button></div></div><div id="detail-body" class="detail-body"></div></dialog>
<dialog id="task-editor" class="detail"><div class="detail-head"><div><small class="task-eyebrow">AUTONOMOUS TASK INTAKE</small><strong style="display:block;font:600 22px Geist">Create a task</strong></div><div class="task-action-group"><button type="button" onclick="$('task-editor').close()">Cancel</button><button id="task-submit" class="primary" type="submit" form="task-form">Create task</button></div></div><form id="task-form" class="detail-body" onsubmit="saveTask(event)"><label>Task title <span class="muted">(maximum 240 characters)</span><input id="task-title" required maxlength="240" placeholder="Describe the outcome"></label><div class="grid"><label>Project<select id="task-project" required></select><small class="muted">Determines which agents can access this task.</small></label><label>Assign agent<select id="task-agent"><option value="">Unassigned</option></select><small class="muted">The agent receives project context after approval.</small></label></div><label>Execution priority<select id="task-priority"><option value="normal">Normal</option><option value="low">Low</option><option value="high">High</option><option value="urgent">Urgent</option></select></label><label>Description &amp; memory guidelines</label><p class="muted">Suggested sections: Objective · Background &amp; Context · Requirements · Acceptance Criteria · Constraints · References</p><div id="task-description-editor" class="quill-editor"></div><p class="muted">Use headings, lists, links, code, images, video, and rich formatting to give agents clear context.</p><section id="task-upload-section" hidden><div class="task-section-heading"><h3>Attachments</h3><span>Files for this task</span></div><div id="task-existing-files"></div><div id="task-drop" class="drop-zone" tabindex="0"><strong>Drop files here</strong><span>or <button type="button" onclick="$('task-files').click()">browse files</button></span><input id="task-files" type="file" multiple hidden></div><div id="task-file-list" class="muted">No files attached</div><p class="muted">New files are attached when you save. Identical files are skipped automatically.</p></section></form></dialog>
<dialog id="approval-dialog" class="approval-dialog"><form method="dialog"><div class="approval-modal-icon">✓</div><h2>Approve this task?</h2><p>Approving confirms that the requirements are ready and allows the assigned agent to begin work immediately.</p><div id="approval-summary" class="approval-summary"></div><label>Approval note or execution directives (optional)<textarea id="approval-note" rows="4" placeholder="e.g., Proceed with the first node batch; verify cache warm-up before full sweep…"></textarea></label><label class="approval-check"><input type="checkbox" checked disabled> Notify assigned agent immediately via execution bus</label><div class="task-action-group" style="justify-content:flex-end"><button value="cancel">Cancel</button><button id="approval-confirm" value="default" type="button" class="primary">Approve Task &amp; Authorize Agent</button></div></form></dialog>
<style>.approval-dialog{width:min(520px,92vw);border:0;border-top:4px solid #2563eb;border-radius:14px;padding:0;box-shadow:0 24px 80px #10182850}.approval-dialog::backdrop{background:#17202a8c;backdrop-filter:blur(5px)}.approval-dialog form{padding:28px}.approval-dialog h2{font:600 22px Geist;margin:0 0 6px;padding-left:52px}.approval-dialog form>p{color:#667085;line-height:1.55;margin:0 0 22px;padding-left:52px}.approval-modal-icon{position:absolute;width:40px;height:40px;border-radius:10px;background:#e1e9ff;color:#0758b7;display:grid;place-items:center;font-size:20px;font-weight:700}.approval-summary{background:#f1f4f7;border-radius:9px;padding:16px;margin-bottom:18px}.approval-summary strong{display:block;font-size:16px;margin-bottom:6px}.approval-dialog textarea{width:100%;border:1px solid #d0d5dd;border-radius:8px;padding:12px;font:inherit;resize:vertical}.approval-check{display:flex;grid-template-columns:auto 1fr;align-items:flex-start;font-size:12px;font-weight:400}.approval-check input{margin-top:2px}</style>
<style>
html{scroll-behavior:smooth}body{letter-spacing:-.005em}button,input,select,textarea{outline:none}button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,[tabindex]:focus-visible{box-shadow:0 0 0 3px rgba(59,130,246,0.35)!important;border-color:#2563eb!important}.top{box-shadow:0 1px 0 #fff inset}.brand-mark{font-size:0}.brand-mark:after{content:'✦';font-size:20px}.system-state{font-weight:500}.sidebar-foot span:last-child{color:#087a4d;background:#dff7ea;padding:3px 8px;border-radius:99px}.page-hero{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:24px}.page-hero-copy{max-width:720px}.page-kicker{display:flex;align-items:center;gap:8px;color:#2563eb;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}.page-kicker:before{content:'';width:7px;height:7px;border-radius:50%;background:#2563eb}.page-hero h1{font:600 clamp(28px,3vw,38px)/1.15 Geist;margin:8px 0 7px;letter-spacing:-.035em}.page-hero p{margin:0;color:#667085;line-height:1.65}.record-panel{background:#fff;border:1px solid #e0e5ea;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px #0f172a12}.record-toolbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:17px 20px;border-bottom:1px solid #e6eaee;background:#fff}.record-toolbar strong{font:600 16px Geist}.record-count{display:inline-flex;align-items:center;gap:8px;color:#667085;font-size:12px}.record-count:before{content:'';width:7px;height:7px;border-radius:50%;background:#12b76a}.record-panel .pager{padding:14px 18px;margin:0;border-top:1px solid #e8ecef}.record-panel tbody tr{transition:background .15s ease}.record-panel tbody tr:hover{background:#f1f5f9}.record-panel tbody tr td:first-child{font-weight:600;color:#29323a}.record-panel tbody tr td:last-child{color:#667085}.record-panel tbody tr:after{content:'›';display:table-cell;padding:15px;color:#98a2b3}.status-chip{display:inline-flex;align-items:center;gap:6px;padding:5px 9px;border-radius:99px;background:#eef2f6;color:#475467;font-size:11px;font-weight:600}.status-chip:before{content:'';width:6px;height:6px;border-radius:50%;background:currentColor}.members-layout{display:grid;grid-template-columns:minmax(280px,380px) minmax(0,1fr);gap:20px}.form-card,.members-card{background:#fff;border:1px solid #e0e5ea;border-radius:12px;padding:24px;box-shadow:0 1px 3px #0f172a12}.form-card h2,.members-card h2{font:600 20px Geist;margin:0 0 8px}.form-card p{color:#667085;line-height:1.55}.form-card button{width:100%;margin-top:8px}.credential-result{margin-top:16px;padding:14px;border:1px solid #bfdbfe;background:#eff6ff;border-radius:8px;color:#1e3a8a;overflow-wrap:anywhere}.detail-head strong{font:600 17px Geist}.detail-body h3{font:600 16px Geist;margin-top:28px;padding-bottom:10px;border-bottom:1px solid #e8ecef}.task-file{padding:13px 14px;border:1px solid #e1e6eb;border-radius:8px;background:#f8fafb;margin-bottom:8px}.event{border-left-color:#2563eb;background:#fafbfc;border-radius:0 8px 8px 0;padding:12px 14px;margin-bottom:8px}.json{border:1px solid #e2e7ec;background:#f6f8fa}.error{border:1px solid #f5b8b1;box-shadow:0 8px 30px #b4231810;margin-bottom:18px}.toast-stack{position:fixed;right:22px;bottom:22px;z-index:100;display:grid;gap:10px}.toast{min-width:280px;max-width:420px;background:#1d2939;color:#fff;padding:13px 15px;border-radius:9px;box-shadow:0 18px 50px #10182835;animation:toast-in .22s ease}.toast.success{border-left:4px solid #12b76a}.toast.error-toast{border-left:4px solid #f04438}@keyframes toast-in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}.loading-state{display:grid;place-items:center;min-height:280px;color:#667085}.loading-state:before{content:'';width:30px;height:30px;border:3px solid #e4e7ec;border-top-color:#2563eb;border-radius:50%;animation:spin .7s linear infinite;margin-bottom:12px}@keyframes spin{to{transform:rotate(360deg)}}#task-editor[open]{width:min(860px,96vw)}#task-editor .detail-body{background:linear-gradient(180deg,#f8fafc 0,#fff 180px)}#task-editor .ql-toolbar{border-radius:8px 8px 0 0;background:#f7f9fb}#task-editor .quill-editor{border-radius:0 0 8px 8px}.task-create{background:linear-gradient(135deg,#2563eb,#1d4ed8)!important}.task-panel{overflow:clip}.task-results-line{background:#fafbfc;border-bottom:1px solid #edf0f4}.review-label{background:#eff6ff;border-color:#bfdbfe;color:#1d4ed8}.approval-banner{position:relative;overflow:hidden}.approval-banner:after{content:'✦';position:absolute;right:24px;top:13px;font-size:64px;color:rgba(37,99,235,0.06)}.metric{position:relative;overflow:hidden;transition:transform .18s ease,box-shadow .18s ease}.metric:hover{transform:translateY(-3px);box-shadow:0 12px 30px #0f172a10}.metric:after{content:'';position:absolute;width:64px;height:64px;border-radius:18px;right:-18px;top:-18px;background:rgba(37,99,235,0.04)}.metric p{margin-top:12px}.card>h2,.row h2{font-family:Geist}@media(max-width:780px){.page-hero{align-items:flex-start;flex-direction:column}.members-layout{grid-template-columns:1fr}.record-toolbar{align-items:flex-start;flex-direction:column}.record-panel tbody tr:after{display:none}.toast-stack{left:14px;right:14px;bottom:80px}.toast{min-width:0}.task-filter-group{display:grid;grid-template-columns:1fr 1fr}.task-filter-group label{width:100%}}
</style>
<style>.uicon{width:17px;height:17px;flex:0 0 auto;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}.uicon path{vector-effect:non-scaling-stroke}.tabs button:before,.global-search:before,.key-wrap:before{display:none}.tabs button .uicon{width:19px;height:19px}.global-search>.uicon{position:absolute;left:14px;top:12px;color:#667085;z-index:2}.refresh-btn,.task-action-group button,.task-create,.form-card button,.page-hero>button{display:inline-flex;align-items:center;justify-content:center;gap:8px}.brand-mark:after{content:none}.brand-mark:before{content:'';width:20px;height:20px;background:currentColor;mask:radial-gradient(circle at 35% 35%,transparent 0 12%,#000 13% 23%,transparent 24%),linear-gradient(#000 0 0);-webkit-mask:radial-gradient(circle at 35% 35%,transparent 0 12%,#000 13% 23%,transparent 24%),linear-gradient(#000 0 0);opacity:.95}@media(max-width:900px){.tabs button .uicon{margin:0}}</style>
<style>
:root{color-scheme:light;--canvas:#f6f8fa;--panel:#fff;--panel-soft:#f1f4f7;--panel-raised:#fff;--text:#191c1e;--text-soft:#667085;--border:#e0e5ea;--border-strong:#d0d5dd;--shadow:0 1px 3px #0f172a12;--shadow-lg:0 20px 60px #0f172a20;--accent:#2563eb;--accent-hover:#1d4ed8;--accent-soft:#eff6ff}body{background:radial-gradient(circle at 75% -20%,#dbeafe 0,transparent 32%),var(--canvas);color:var(--text);transition:background-color .2s,color .2s}.sidebar{background:color-mix(in srgb,var(--panel-soft) 94%,transparent);border-color:var(--border);backdrop-filter:blur(16px)}.top{background:color-mix(in srgb,var(--panel) 92%,transparent);border-color:var(--border);backdrop-filter:blur(18px)}.card,.task-panel,.record-panel,.form-card,.members-card,.detail-head,.detail-body{background:var(--panel);border-color:var(--border);color:var(--text)}.global-search input,.key-wrap,input,select,textarea,.json,.drop-zone,.task-toolbar,.task-results-line,.task-file,.event{background:var(--panel-soft);border-color:var(--border);color:var(--text)}.theme-toggle{display:inline-flex;align-items:center;gap:8px;height:38px;padding:0 11px;border:1px solid var(--border);background:var(--panel-soft);color:var(--text);border-radius:8px}.theme-toggle-dot{width:16px;height:16px;border-radius:50%;background:linear-gradient(135deg,#60a5fa 50%,#344054 50%);box-shadow:inset 0 0 0 1px #ffffff55}.theme-toggle span:last-child{font-size:12px;font-weight:600}.muted,.page-hero p,.task-heading p{color:var(--text-soft)!important}
body[data-theme="dark"]{color-scheme:dark;--canvas:#0c1017;--panel:#131922;--panel-soft:#19212c;--panel-raised:#1e2733;--text:#f3f5f7;--text-soft:#9ba7b5;--border:#283341;--border-strong:#3a4655;--shadow:0 1px 3px #0005;--shadow-lg:0 24px 70px #0008;--accent:#3b82f6;--accent-hover:#60a5fa;--accent-soft:#172554;background:radial-gradient(circle at 75% -15%,rgba(30,58,138,0.25) 0,transparent 34%),#0c1017}body[data-theme="dark"] .sidebar{background:#101620eF}body[data-theme="dark"] .top{background:#111720eF}body[data-theme="dark"] .brand,body[data-theme="dark"] .system-state,body[data-theme="dark"] .sidebar-foot{border-color:var(--border)}body[data-theme="dark"] .tabs button{color:#b9c3cf}body[data-theme="dark"] .tabs button:hover{background:#1d2733;color:#fff}body[data-theme="dark"] .tabs button.active{background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff}body[data-theme="dark"] .key-wrap,body[data-theme="dark"] .global-search input,body[data-theme="dark"] input,body[data-theme="dark"] select,body[data-theme="dark"] textarea{background:#161e28;border-color:#2b3745;color:#eef2f6}body[data-theme="dark"] input::placeholder,body[data-theme="dark"] textarea::placeholder{color:#778495}body[data-theme="dark"] .card,body[data-theme="dark"] .task-panel,body[data-theme="dark"] .record-panel,body[data-theme="dark"] .form-card,body[data-theme="dark"] .members-card{background:linear-gradient(145deg,#151c26,#111821);border-color:#293543;box-shadow:0 1px 3px #0006}body[data-theme="dark"] .metric:hover{box-shadow:0 16px 36px #0007;border-color:#3b4a5a}body[data-theme="dark"] th{background:#19212c;color:#9eabba;border-color:#293543}body[data-theme="dark"] td{border-color:#252f3b}body[data-theme="dark"] tbody tr:hover{background:#1b2530}body[data-theme="dark"] .record-toolbar,body[data-theme="dark"] .task-toolbar,body[data-theme="dark"] .task-results-line{background:#161e28;border-color:#293543}body[data-theme="dark"] button{background:#202a36;color:#e9edf2}body[data-theme="dark"] button:hover{background:#293644}body[data-theme="dark"] button.primary,body[data-theme="dark"] .task-create{background:linear-gradient(135deg,#3b82f6,#1d4ed8)!important;color:#fff}body[data-theme="dark"] .approval-banner{background:linear-gradient(100deg,#172554,#181d25);border-color:#1e3a8a}body[data-theme="dark"] .approval-banner p{color:#93c5fd}body[data-theme="dark"] .detail,body[data-theme="dark"] .approval-dialog{background:#131922;color:#f3f5f7}body[data-theme="dark"] .detail-head,body[data-theme="dark"] .detail-body{background:#131922;border-color:#293543}body[data-theme="dark"] .detail::backdrop,body[data-theme="dark"] .approval-dialog::backdrop{background:#040609bb}body[data-theme="dark"] .json,body[data-theme="dark"] .event,body[data-theme="dark"] .task-file,body[data-theme="dark"] .drop-zone{background:#19212c;border-color:#2c3846}body[data-theme="dark"] .review-label{background:#172554;border-color:#1e3a8a;color:#93c5fd}body[data-theme="dark"] .pill.open{background:#172554;color:#93c5fd}body[data-theme="dark"] .pill.working{background:#142f42;color:#7cccf8}body[data-theme="dark"] .pill.done{background:#153424;color:#75d89c}body[data-theme="dark"] .error{background:#371c1c;border-color:#713333;color:#ffb4ac}body[data-theme="dark"] .ql-toolbar,body[data-theme="dark"] .ql-container{border-color:#344151!important}body[data-theme="dark"] .ql-toolbar{background:#19212c!important}body[data-theme="dark"] .ql-editor{background:#131922;color:#f0f3f6}body[data-theme="dark"] .ql-stroke:not(.ql-color-label){stroke:#c6d0dc!important}body[data-theme="dark"] .ql-fill:not(.ql-color-label){fill:#c6d0dc!important}body[data-theme="dark"] .theme-toggle-dot{background:radial-gradient(circle at 65% 35%,#dbeafe 0 18%,transparent 20%),#56647a;box-shadow:inset -5px -3px 0 #202838}body[data-theme="dark"] .page-kicker{color:#60a5fa}body[data-theme="dark"] .metric span{color:#93c5fd}body[data-theme="dark"] .avatar{background:#2563eb}body[data-theme="dark"] ::selection{background:#1d4ed8;color:#fff}@media(max-width:900px){.theme-toggle span:last-child{display:none}.theme-toggle{padding:0 10px}}@media(max-width:640px){.theme-toggle{display:inline-flex}.top{gap:8px}}
</style>
<style>
/* Organized Slate + Indigo workspace system */
:root{--accent:#4f46e5;--accent-hover:#4338ca;--accent-soft:#eef2ff;--canvas:#f7f8fc;--panel:#fff;--panel-soft:#f8fafc;--text:#172033;--text-soft:#667085;--border:#e4e7ec;--success:#079455;--danger:#d92d20}body{grid-template-columns:264px minmax(0,1fr);background:var(--canvas);font-size:13px}.sidebar{background:#fff;border-right:1px solid #e4e7ec}.brand{height:76px;padding:0 24px;border-color:#e4e7ec}.brand-mark{background:linear-gradient(145deg,#6366f1,#3730a3);border-radius:10px}.system-state{margin:14px 14px 0;padding:11px 12px;border:1px solid #e4e7ec;border-radius:9px;background:#f8fafc}.tabs{padding:12px 14px;gap:3px}.tabs button{padding:10px 12px;border-radius:7px;color:#475467}.tabs button.active{background:#eef2ff;color:#3730a3;box-shadow:none;font-weight:600}.tabs button.active .uicon{color:#4f46e5}.tabs button:hover{background:#f2f4f7}.sidebar-foot{margin:0 14px 14px;padding:12px;border:1px solid #e4e7ec;border-radius:9px;background:#f8fafc}.top{height:76px;padding:14px 32px;background:#fff;border-color:#e4e7ec;box-shadow:none}.global-search{max-width:620px}.global-search input{height:42px;background:#f8fafc;border-color:#e4e7ec}.key-wrap{height:42px;background:#f8fafc}.refresh-btn{height:42px;background:#fff}.user-chip{padding-left:18px}.avatar{background:linear-gradient(145deg,#6366f1,#4338ca)}.wrap{padding:36px clamp(24px,3vw,48px) 64px}.wrap>#app{max-width:1480px;margin:0 auto}.page-hero{padding-bottom:22px;border-bottom:1px solid #e4e7ec;margin-bottom:28px;align-items:center}.page-hero h1{font-size:32px;color:#172033}.page-kicker,.task-eyebrow{color:#4f46e5}.page-kicker:before{background:#6366f1}.record-panel,.task-panel,.form-card,.members-card{border-radius:10px;border-color:#e4e7ec;box-shadow:0 1px 2px #1018280a}.record-toolbar{padding:18px 20px;background:#fff}.record-toolbar p{margin:5px 0 0;color:#667085}.record-count:before{background:#12b76a}th{padding:12px 18px;background:#f8fafc;font-size:11px;color:#667085}td{padding:15px 18px}.record-panel tbody tr:hover{background:#f8f9ff}button.primary,.task-create{background:#4f46e5!important;box-shadow:0 1px 2px #1018280d}button.primary:hover,.task-create:hover{background:#4338ca!important}.task-heading{padding-bottom:22px;border-bottom:1px solid #e4e7ec}.task-heading h2{color:#172033}.task-toolbar{background:#fff;padding:14px 18px}.task-filter-group select{background:#f8fafc;border-color:#e4e7ec}.review-label{background:#eff6ff;border-color:#bfdbfe;color:#2563eb}.approval-banner{background:#eef2ff;border-color:#c7d2fe}.approval-banner strong{color:#3730a3}.approval-banner p{color:#475467}.detail[open]{width:min(680px,96vw)}.detail-head{border-color:#e4e7ec}.overview-header{display:flex;align-items:flex-end;justify-content:space-between;gap:28px;padding-bottom:28px;border-bottom:1px solid #e4e7ec;margin-bottom:28px}.overview-header h1{font:600 clamp(30px,3vw,40px)/1.15 Geist;margin:8px 0;color:#172033;letter-spacing:-.035em}.overview-header p{margin:0;color:#667085;font-size:15px}.system-health{display:flex;align-items:center;gap:12px;padding:12px 15px;background:#ecfdf3;border:1px solid #abefc6;border-radius:9px;min-width:270px}.system-health>span{width:10px;height:10px;border-radius:50%;background:#17b26a;box-shadow:0 0 0 4px #17b26a1f}.system-health strong,.system-health small{display:block}.system-health strong{color:#067647;font-size:12px}.system-health small{color:#47936d;margin-top:2px}.overview-section{margin-bottom:24px}.section-heading{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:14px}.section-heading h2{font:600 18px Geist;margin:0 0 4px;color:#172033}.section-heading p{margin:0;color:#667085}.section-heading>span{color:#079455;background:#ecfdf3;padding:4px 9px;border-radius:99px;font-size:11px;font-weight:600}.metric-grid-primary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.metric-card{display:flex;align-items:flex-start;gap:15px;background:#fff;border:1px solid #e4e7ec;border-radius:10px;padding:20px;min-height:150px;box-shadow:0 1px 2px #1018280a;transition:.18s ease}.metric-card:hover{transform:translateY(-2px);border-color:#c7d2fe;box-shadow:0 8px 22px #4f46e50d}.metric-icon{width:42px;height:42px;border-radius:9px;background:#eef2ff;color:#4f46e5;display:grid;place-items:center}.metric-icon .uicon{width:21px;height:21px}.metric-card span{color:#667085;font-weight:600}.metric-card strong{display:block;font:600 32px Geist;color:#172033;margin:12px 0 6px}.metric-card p{margin:0;color:#98a2b3;font-size:12px}.metric-strip{display:grid;grid-template-columns:repeat(4,1fr);margin-top:14px;background:#fff;border:1px solid #e4e7ec;border-radius:10px}.metric-strip article{padding:16px 20px;border-right:1px solid #e4e7ec}.metric-strip article:last-child{border-right:0}.metric-strip span,.metric-strip small{display:block;color:#667085}.metric-strip strong{display:block;font:600 20px Geist;color:#344054;margin:5px 0}.overview-recent{margin-top:24px}body[data-theme="dark"]{--accent:#818cf8;--accent-hover:#6366f1;--accent-soft:#252747}body[data-theme="dark"] .sidebar,body[data-theme="dark"] .top{background:#111722}body[data-theme="dark"] .tabs button.active{background:#242747;color:#c7d2fe}body[data-theme="dark"] .tabs button.active .uicon{color:#a5b4fc}body[data-theme="dark"] .system-state,body[data-theme="dark"] .sidebar-foot{background:#171f2a;border-color:#293543}body[data-theme="dark"] .overview-header h1,body[data-theme="dark"] .section-heading h2,body[data-theme="dark"] .page-hero h1,body[data-theme="dark"] .task-heading h2,body[data-theme="dark"] .metric-card strong{color:#f3f5f7}body[data-theme="dark"] .metric-card,body[data-theme="dark"] .metric-strip{background:#131922;border-color:#293543}body[data-theme="dark"] .metric-strip article{border-color:#293543}body[data-theme="dark"] .metric-icon{background:#242747;color:#a5b4fc}body[data-theme="dark"] .system-health{background:#10291e;border-color:#205d3e}body[data-theme="dark"] .system-health strong{color:#75d89c}body[data-theme="dark"] .system-health small{color:#69a985}body[data-theme="dark"] .approval-banner{background:#202442;border-color:#373d70}body[data-theme="dark"] .approval-banner strong{color:#c7d2fe}@media(max-width:1150px){.metric-grid-primary{grid-template-columns:repeat(2,1fr)}}@media(max-width:900px){body{grid-template-columns:78px minmax(0,1fr)}.overview-header{align-items:flex-start;flex-direction:column}.system-health{width:100%}}@media(max-width:700px){.metric-grid-primary,.metric-strip{grid-template-columns:1fr 1fr}.metric-strip article:nth-child(2){border-right:0}.metric-strip article:nth-child(-n+2){border-bottom:1px solid #e4e7ec}}@media(max-width:480px){.metric-grid-primary,.metric-strip{grid-template-columns:1fr}.metric-strip article{border-right:0;border-bottom:1px solid #e4e7ec}.metric-strip article:last-child{border-bottom:0}.overview-header{padding-bottom:20px}.wrap{padding-top:24px}}
</style>
<style>.ql-toolbar .ql-list[value="check"]:after{content:'✓';font-weight:700;font-size:14px;position:absolute;inset:2px;display:grid;place-items:center}.ql-toolbar .ql-list[value="check"] svg{display:none}</style>
<style>.ql-toolbar button.ql-list[value="check"]{position:relative!important;display:inline-grid!important;place-items:center!important;width:28px!important;height:24px!important;color:#444ce7!important;opacity:1!important}.ql-toolbar button.ql-list[value="check"]:after{content:'✓'!important;position:static!important;display:block!important;visibility:visible!important;opacity:1!important;color:currentColor!important;font:700 15px/1 Inter,system-ui,sans-serif!important;transform:none!important}.ql-toolbar button.ql-list[value="check"]:hover,.ql-toolbar button.ql-list[value="check"].ql-active{color:#3730a3!important;background:#eef2ff!important;border-radius:4px}.ql-toolbar button.ql-list[value="check"] svg{display:none!important}body[data-theme="dark"] .ql-toolbar button.ql-list[value="check"]{color:#a5b4fc!important}body[data-theme="dark"] .ql-toolbar button.ql-list[value="check"]:hover,body[data-theme="dark"] .ql-toolbar button.ql-list[value="check"].ql-active{color:#c7d2fe!important;background:#2b315b!important}</style>
<style>.manual-create{display:inline-flex;align-items:center;gap:8px;padding:11px 15px}.manual-entry[open]{width:min(720px,96vw)}.manual-entry .detail-head>div:first-child{display:grid;gap:3px}.manual-entry .detail-body{padding:26px 28px 40px}.manual-entry textarea{width:100%;resize:vertical;line-height:1.5}.manual-entry select[multiple]{min-height:110px;padding:6px}.manual-entry select[multiple] option{padding:8px;border-radius:5px}.manual-entry select[multiple] option:checked{background:#eef2ff;color:#3730a3}.manual-entry label small{font-weight:400;color:#667085}.form-intro{padding:16px 18px;margin-bottom:20px;background:#f8f9ff;border:1px solid #e0e7ff;border-radius:9px}.form-intro strong{font:600 16px Geist;color:#3730a3}.form-intro p{margin:5px 0 0;color:#667085;line-height:1.55}.manual-entry label{margin:17px 0}.manual-entry .grid label{margin:0}body[data-theme="dark"] .form-intro{background:#202442;border-color:#373d70}body[data-theme="dark"] .form-intro strong{color:#c7d2fe}body[data-theme="dark"] .manual-entry select[multiple] option:checked{background:#2b315b;color:#e0e7ff}@media(max-width:640px){.manual-entry .detail-body{padding:20px 18px 90px}.manual-entry .detail-head{align-items:flex-start}.manual-entry .detail-head .task-action-group{position:fixed;left:0;right:0;bottom:0;padding:12px 16px;background:var(--panel);border-top:1px solid var(--border);justify-content:flex-end;z-index:50}}</style>
<style>
/* Final professional system: neutral slate + indigo only */
:root{--ui-bg:#f6f7f9;--ui-surface:#fff;--ui-subtle:#f8f9fb;--ui-muted:#667085;--ui-text:#182230;--ui-border:#e1e5ea;--ui-border-strong:#cfd5dc;--ui-accent:#4f46e5;--ui-accent-dark:#4338ca;--ui-accent-soft:#eef2ff;--ui-danger:#b42318;--ui-radius:8px;--ui-shadow:0 1px 2px rgba(16,24,40,.05)}*{box-sizing:border-box}body{background:var(--ui-bg)!important;color:var(--ui-text)!important;grid-template-columns:256px minmax(0,1fr);font:13px/1.5 Inter,system-ui,sans-serif;letter-spacing:0}.sidebar{background:var(--ui-surface)!important;border-right:1px solid var(--ui-border)!important;backdrop-filter:none!important}.brand{height:72px;padding:0 22px;border-bottom:1px solid var(--ui-border)!important}.brand-mark{width:36px;height:36px;border-radius:8px;background:var(--ui-accent)!important;box-shadow:none}.system-state{margin:12px 12px 4px;padding:10px 11px;border:1px solid var(--ui-border)!important;border-radius:var(--ui-radius);background:var(--ui-subtle)!important;color:var(--ui-muted)!important}.live-dot{width:7px;height:7px;background:var(--ui-accent)!important;box-shadow:none}.tabs{padding:8px 12px;gap:2px}.tabs button{min-height:40px;padding:9px 11px;border-radius:6px!important;color:#475467!important;font-weight:500;background:transparent!important;box-shadow:none!important}.tabs button:hover{background:#f2f4f7!important;color:var(--ui-text)!important;transform:none}.tabs button.active{background:var(--ui-accent-soft)!important;color:#3730a3!important;font-weight:600}.tabs button.active .uicon{color:var(--ui-accent)!important}.sidebar-foot{margin:4px 12px 12px;padding:10px 11px;border:1px solid var(--ui-border)!important;border-radius:var(--ui-radius);background:var(--ui-subtle)!important}.sidebar-foot span:last-child{padding:0;background:transparent!important;color:var(--ui-accent)!important;font-weight:600}.top{height:72px;padding:14px 28px;background:var(--ui-surface)!important;border-bottom:1px solid var(--ui-border)!important;box-shadow:none!important;backdrop-filter:none!important;gap:12px}.global-search{max-width:560px}.global-search input,.key-wrap{height:40px;background:var(--ui-subtle)!important;border:1px solid var(--ui-border)!important;border-radius:var(--ui-radius)!important}.key-wrap input{height:auto!important}.refresh-btn,.theme-toggle{height:40px;background:var(--ui-surface)!important;border:1px solid var(--ui-border)!important;border-radius:var(--ui-radius)!important;color:#344054!important}.theme-toggle-dot{background:var(--ui-accent)!important;box-shadow:none!important;width:14px;height:14px}.user-chip{padding-left:16px;border-color:var(--ui-border)!important}.avatar{width:34px;height:34px;background:var(--ui-accent)!important}.wrap{padding:32px clamp(24px,3vw,44px) 56px}.wrap>#app{max-width:1440px}.page-hero,.task-heading,.overview-header{padding-bottom:22px;margin-bottom:24px;border-bottom:1px solid var(--ui-border)!important}.page-hero h1,.task-heading h2,.overview-header h1{color:var(--ui-text)!important;font-size:30px;line-height:1.2;letter-spacing:-.025em}.page-kicker,.task-eyebrow{color:var(--ui-accent)!important;letter-spacing:.08em}.page-kicker:before{background:var(--ui-accent)!important}.page-hero p,.task-heading p,.overview-header p,.muted{color:var(--ui-muted)!important}.card,.task-panel,.record-panel,.form-card,.members-card,.metric-card,.metric-strip{background:var(--ui-surface)!important;border:1px solid var(--ui-border)!important;border-radius:var(--ui-radius)!important;box-shadow:var(--ui-shadow)!important}.card{padding:20px;margin-bottom:16px}.record-panel,.task-panel{overflow:hidden}.record-toolbar{min-height:66px;padding:16px 20px;background:var(--ui-surface)!important;border-bottom:1px solid var(--ui-border)!important}.record-toolbar strong{font-size:15px;color:var(--ui-text)}.record-toolbar p{margin:3px 0 0}.record-count{color:var(--ui-muted)!important}.record-count:before{background:var(--ui-accent)!important}.table{overflow:auto}table{border-spacing:0}th{height:42px;padding:11px 16px!important;background:var(--ui-subtle)!important;color:var(--ui-muted)!important;border-bottom:1px solid var(--ui-border)!important;font-size:10px;letter-spacing:.065em}td{height:52px;padding:13px 16px!important;border-bottom:1px solid var(--ui-border)!important;color:#344054}tbody tr:last-child td{border-bottom:0}tbody tr:hover{background:#fafaff!important}.record-panel tbody tr td:first-child{color:var(--ui-text)!important}.record-panel tbody tr:after{color:#98a2b3}.record-panel .pager,.task-footer{padding:12px 16px;border-top:1px solid var(--ui-border)!important;background:var(--ui-surface)!important}.pager{gap:6px}.pager button{height:34px;border:1px solid var(--ui-border)!important;background:var(--ui-surface)!important}.metric-grid-primary{gap:12px}.metric-card{padding:18px;min-height:138px;gap:14px}.metric-card:hover{transform:none;border-color:#c7d2fe!important;box-shadow:0 2px 6px rgba(79,70,229,.08)!important}.metric-icon{width:40px;height:40px;border-radius:7px;background:var(--ui-accent-soft)!important;color:var(--ui-accent)!important}.metric-card strong{margin:10px 0 4px;color:var(--ui-text)!important;font-size:30px}.metric-card span,.metric-card p,.metric-strip span,.metric-strip small{color:var(--ui-muted)!important}.metric-strip{margin-top:12px}.metric-strip article{padding:14px 18px;border-right:1px solid var(--ui-border)!important}.metric-strip strong{color:#344054!important}.system-health{min-width:260px;padding:11px 13px;background:var(--ui-accent-soft)!important;border:1px solid #c7d2fe!important;border-radius:var(--ui-radius)}.system-health>span{background:var(--ui-accent)!important;box-shadow:none}.system-health strong{color:#3730a3!important}.system-health small{color:#6366a8!important}.task-toolbar{padding:14px 16px;background:var(--ui-surface)!important;border-bottom:1px solid var(--ui-border)!important}.task-filter-group{gap:10px}.task-filter-group label{gap:6px;color:var(--ui-muted)!important}.task-filter-group select{height:36px;min-width:138px;background:var(--ui-subtle)!important;border:1px solid var(--ui-border)!important;border-radius:6px!important}.task-results-line{padding:9px 16px;background:var(--ui-subtle)!important;border-bottom:1px solid var(--ui-border)!important}.pill,.review-label,.status-chip{border-radius:99px!important;padding:4px 8px!important;border:1px solid #d8defd!important;background:var(--ui-accent-soft)!important;color:#4338ca!important}.pill:before{background:currentColor!important}.pill.open,.pill.working,.pill.done,.pill.reopened{background:var(--ui-accent-soft)!important;color:#4338ca!important}.pill.closed{background:#f2f4f7!important;color:#667085!important;border-color:#e4e7ec!important}.task-priority,.task-priority.urgent,.task-priority.high,.task-priority.normal,.task-priority.low,.priority.urgent,.priority.high,.priority.normal,.priority.low{color:#475467!important}.review-label{background:#f5f3ff!important;color:#5b21b6!important}.approval-banner{padding:18px;background:var(--ui-accent-soft)!important;border:1px solid #c7d2fe!important;border-radius:var(--ui-radius)!important}.approval-banner strong{color:#3730a3!important}.approval-banner p{color:#4f5685!important}.approval-banner:after{display:none}.form-card,.members-card{padding:22px}.form-intro{padding:14px 16px;margin-bottom:18px;background:var(--ui-subtle)!important;border:1px solid var(--ui-border)!important;border-radius:var(--ui-radius)!important}.form-intro strong{color:var(--ui-text)!important}.manual-entry label{margin:15px 0}label{gap:6px}input,select,textarea{border:1px solid var(--ui-border-strong)!important;border-radius:6px!important;background:var(--ui-surface)!important;color:var(--ui-text)!important;padding:9px 11px}input,select{min-height:38px}input:focus,select:focus,textarea:focus{border-color:#818cf8!important;box-shadow:0 0 0 3px rgba(99,102,241,.12)!important}button{min-height:34px;border-radius:6px!important;padding:8px 12px;background:#f2f4f7;color:#344054;box-shadow:none!important}button:hover{transform:none;background:#e9edf2}button.primary,.task-create{background:var(--ui-accent)!important;color:#fff!important;border:1px solid var(--ui-accent)!important}button.primary:hover,.task-create:hover{background:var(--ui-accent-dark)!important}.task-delete{color:var(--ui-danger)!important;background:#fff!important;border:1px solid #fecdca!important}.drop-zone{padding:20px;background:var(--ui-subtle)!important;border:1px dashed var(--ui-border-strong)!important;border-radius:var(--ui-radius)!important}.task-file,.event,.json{background:var(--ui-subtle)!important;border:1px solid var(--ui-border)!important;border-radius:var(--ui-radius)!important}.event{border-left:3px solid var(--ui-accent)!important}.detail,.approval-dialog{border-radius:0!important;background:var(--ui-surface)!important}.detail-head{min-height:68px;padding:15px 20px;background:var(--ui-surface)!important;border-bottom:1px solid var(--ui-border)!important}.detail-body{padding:22px 20px 36px;background:var(--ui-surface)!important}.detail-body h3{margin-top:26px;border-color:var(--ui-border)!important}.ql-toolbar{background:var(--ui-subtle)!important;border-color:var(--ui-border)!important;border-radius:6px 6px 0 0!important}.ql-container{border-color:var(--ui-border)!important;border-radius:0 0 6px 6px!important}.toast{border-radius:var(--ui-radius)!important}.toast.success,.toast.error-toast{border-left-color:var(--ui-accent)!important}body[data-theme="dark"]{--ui-bg:#0f141c;--ui-surface:#151c26;--ui-subtle:#1a2330;--ui-muted:#9aa6b5;--ui-text:#edf1f5;--ui-border:#2a3543;--ui-border-strong:#3a4655;--ui-accent:#818cf8;--ui-accent-dark:#6366f1;--ui-accent-soft:#242947;background:var(--ui-bg)!important}body[data-theme="dark"] .sidebar,body[data-theme="dark"] .top,body[data-theme="dark"] .card,body[data-theme="dark"] .task-panel,body[data-theme="dark"] .record-panel,body[data-theme="dark"] .form-card,body[data-theme="dark"] .members-card,body[data-theme="dark"] .metric-card,body[data-theme="dark"] .metric-strip,body[data-theme="dark"] .detail,body[data-theme="dark"] .detail-head,body[data-theme="dark"] .detail-body{background:var(--ui-surface)!important;border-color:var(--ui-border)!important}body[data-theme="dark"] .tabs button{color:#b1bdca!important}body[data-theme="dark"] .tabs button:hover{background:var(--ui-subtle)!important}body[data-theme="dark"] .tabs button.active{background:var(--ui-accent-soft)!important;color:#c7d2fe!important}body[data-theme="dark"] .global-search input,body[data-theme="dark"] .key-wrap,body[data-theme="dark"] input,body[data-theme="dark"] select,body[data-theme="dark"] textarea,body[data-theme="dark"] .task-toolbar,body[data-theme="dark"] .task-results-line,body[data-theme="dark"] th,body[data-theme="dark"] .drop-zone,body[data-theme="dark"] .task-file,body[data-theme="dark"] .event,body[data-theme="dark"] .json,body[data-theme="dark"] .form-intro{background:var(--ui-subtle)!important;border-color:var(--ui-border)!important;color:var(--ui-text)!important}body[data-theme="dark"] td{border-color:var(--ui-border)!important;color:#c3ccd6}body[data-theme="dark"] tbody tr:hover{background:#1b2533!important}body[data-theme="dark"] .system-health,body[data-theme="dark"] .approval-banner{background:var(--ui-accent-soft)!important;border-color:#3d4679!important}body[data-theme="dark"] .system-health strong,body[data-theme="dark"] .approval-banner strong{color:#c7d2fe!important}body[data-theme="dark"] .system-health small,body[data-theme="dark"] .approval-banner p{color:#a8b0df!important}body[data-theme="dark"] button{background:#202a36;color:#d8e0e8}body[data-theme="dark"] .task-delete{background:transparent!important;border-color:#733a3a!important;color:#fda29b!important}@media(max-width:900px){body{grid-template-columns:76px minmax(0,1fr)}.wrap{padding:28px 22px 48px}}@media(max-width:640px){body{display:block}.top{height:64px;padding:10px 12px}.wrap{padding:22px 14px 82px}.page-hero,.task-heading,.overview-header{padding-bottom:18px;margin-bottom:20px}.card{padding:16px}.task-toolbar{padding:12px}.task-filter-group{grid-template-columns:1fr 1fr}.task-filter-group select{width:100%;min-width:0}.metric-card{min-height:122px}.record-toolbar{padding:14px 16px}}
</style>
<style>
/* Layout corrections and adaptive navigation */
.key-wrap input{border:0!important;box-shadow:none!important;background:transparent!important;min-height:0!important;height:auto!important;padding:5px 7px!important}.key-wrap input:focus{border:0!important;box-shadow:none!important}.task-filter-group{align-items:flex-end}.task-filter-group label{display:flex!important;flex:0 0 auto!important;align-items:center!important;white-space:nowrap!important;margin:0!important}.task-filter-group label select{flex:0 0 auto}.sidebar-foot{margin:auto 12px 12px!important}.tabs button[hidden]{display:none!important}.page-actions{display:flex;align-items:center;justify-content:flex-end;gap:8px;flex:0 0 auto}.page-actions button{margin:0}.required-mark{margin-left:5px;color:var(--ui-accent);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.05em}.user-chip strong{color:var(--ui-text)!important}.user-chip small{color:var(--ui-accent)!important}.wrap,.wrap>#app,.task-screen,.record-panel,.task-panel{min-width:0;width:100%}.table{max-width:100%}.sidebar-toggle{margin-left:auto;width:30px;height:30px;min-height:30px;padding:0!important;display:grid;place-items:center;background:transparent!important;border:1px solid transparent!important}.sidebar-toggle:hover{background:var(--ui-subtle)!important;border-color:var(--ui-border)!important}.sidebar-toggle span{position:relative;width:14px;height:12px;border-left:2px solid currentColor;border-right:2px solid currentColor}.sidebar-toggle span:after{content:'';position:absolute;left:3px;top:5px;width:4px;border-top:2px solid currentColor}.sidebar-collapsed{grid-template-columns:76px minmax(0,1fr)}.sidebar-collapsed .brand{padding:0 18px;justify-content:center}.sidebar-collapsed .brand-name,.sidebar-collapsed .system-state,.sidebar-collapsed .tabs button span,.sidebar-collapsed .sidebar-foot span:first-child{display:none!important}.sidebar-collapsed .brand-mark{display:none}.sidebar-collapsed .sidebar-toggle{margin:0}.sidebar-collapsed .tabs{padding:8px}.sidebar-collapsed .tabs button{justify-content:center;padding:9px}.sidebar-collapsed .tabs button .uicon{margin:0}.sidebar-collapsed .sidebar-foot{justify-content:center;padding:10px 6px}.sidebar-collapsed .sidebar-foot span:last-child{font-size:0}.sidebar-collapsed .sidebar-foot span:last-child:after{content:'';display:block;width:8px;height:8px;border-radius:50%;background:var(--ui-accent)}body[data-theme="dark"] .user-chip strong{color:#edf1f5!important}body[data-theme="dark"] .user-chip small{color:#a5b4fc!important}body[data-theme="dark"] .sidebar-toggle{color:#c7d2dc!important}@media(max-width:1100px){.top{padding-left:20px;padding-right:20px}.wrap{padding-left:24px;padding-right:24px}.task-toolbar{align-items:flex-start;flex-direction:column}.task-filter-group{width:100%;display:flex;flex-wrap:wrap}.task-toggle{align-self:flex-end}}@media(max-width:900px){body:not(.sidebar-collapsed){grid-template-columns:76px minmax(0,1fr)}body:not(.sidebar-collapsed) .brand-name,body:not(.sidebar-collapsed) .system-state,body:not(.sidebar-collapsed) .tabs button span,body:not(.sidebar-collapsed) .sidebar-foot span:first-child{display:none}.brand{padding:0 18px}.brand-mark{display:none}.sidebar-toggle{margin:0}.tabs{padding:8px}.tabs button{justify-content:center}.sidebar-foot{justify-content:center}.page-hero{align-items:flex-start}.page-actions{align-self:flex-start}}@media(max-width:640px){body.sidebar-collapsed{display:block}.sidebar-toggle{display:none}.page-hero{gap:14px}.page-actions{width:100%;justify-content:flex-start;flex-wrap:wrap}.page-actions button{flex:1}.task-filter-group{display:grid!important;grid-template-columns:1fr 1fr!important;gap:10px}.task-filter-group label{display:grid!important;width:100%;align-items:stretch!important}.task-filter-group label select{width:100%}.task-toggle{align-self:flex-start}.user-chip{display:none!important}}
</style>
<style>
/* Authoritative task filter layout */
.task-toolbar{display:grid!important;grid-template-columns:minmax(0,1fr) auto!important;align-items:end!important;gap:16px!important;padding:16px!important;overflow:visible!important}.task-filter-group{display:grid!important;grid-template-columns:repeat(4,minmax(140px,1fr))!important;gap:12px!important;width:100%!important;min-width:0!important;align-items:end!important}.task-filter-group label{display:grid!important;grid-template-columns:minmax(0,1fr)!important;gap:6px!important;width:100%!important;min-width:0!important;margin:0!important;white-space:nowrap!important;align-items:stretch!important}.task-filter-group label select{display:block!important;width:100%!important;min-width:0!important;max-width:none!important;height:38px!important;margin:0!important;padding:8px 30px 8px 10px!important;overflow:hidden!important;text-overflow:ellipsis!important}.task-toggle{display:flex!important;align-items:center!important;align-self:end!important;height:38px!important;margin:0!important;padding:0 4px!important;white-space:nowrap!important}.task-toggle input{width:16px!important;height:16px!important;min-height:0!important;flex:0 0 16px!important;margin:0!important}.task-panel,.task-toolbar,.task-filter-group{box-sizing:border-box!important}.task-results-line{clear:both!important}@media(max-width:1280px){.task-filter-group{grid-template-columns:repeat(2,minmax(160px,1fr))!important}}@media(max-width:760px){.task-toolbar{grid-template-columns:1fr!important;align-items:stretch!important}.task-filter-group{grid-template-columns:repeat(2,minmax(0,1fr))!important}.task-toggle{justify-self:start!important}}@media(max-width:480px){.task-filter-group{grid-template-columns:1fr!important}}
</style>
<style>
.overview-hero{align-items:center}.overview-hero-actions{display:flex;align-items:center;gap:8px}.overview-hero-actions button{display:inline-flex;align-items:center;gap:7px}.overview-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:20px}.overview-kpi{position:relative;display:flex;align-items:center!important;justify-content:flex-start!important;text-align:left;white-space:normal;gap:16px!important;min-height:132px;padding:24px!important;background:var(--ui-surface)!important;border:1px solid var(--ui-border)!important;border-radius:var(--ui-radius)!important;box-shadow:var(--ui-shadow)!important}.overview-kpi:hover{border-color:#c7d2fe!important;background:#fafaff!important}.overview-kpi .metric-icon{flex:0 0 40px}.overview-kpi-copy{display:flex;flex:1;flex-direction:column;gap:6px;min-width:0;overflow-wrap:anywhere}.overview-kpi-copy small,.overview-kpi-copy strong,.overview-kpi-copy em{display:block}.overview-kpi-copy small{color:var(--ui-muted);font-size:12px;line-height:1.4;font-weight:600}.overview-kpi-copy strong{margin:0;font:600 28px/1.15 Geist,system-ui,sans-serif;font-variant-numeric:tabular-nums;color:var(--ui-text)}.overview-kpi-copy em{color:var(--ui-muted);font-size:12px;line-height:1.4;font-style:normal}.overview-kpi-arrow{flex:0 0 12px;align-self:flex-start;margin-left:auto;color:var(--ui-muted);font-size:20px;line-height:1}.overview-dashboard-grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1.1fr) minmax(260px,.8fr);gap:12px;margin-bottom:20px}.dashboard-panel{display:flex;flex-direction:column;min-height:320px;padding:20px;background:var(--ui-surface);border:1px solid var(--ui-border);border-radius:var(--ui-radius);box-shadow:var(--ui-shadow)}.dashboard-panel>header{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:18px}.dashboard-panel h2{margin:0;font:600 15px Geist;color:var(--ui-text)}.dashboard-panel header p{margin:4px 0 0;color:var(--ui-muted);font-size:11px}.dashboard-panel header>strong{color:var(--ui-accent);font-size:12px;white-space:nowrap}.completion-track,.mix-track{height:6px;background:#eef0f3;border-radius:99px;overflow:hidden}.completion-track{margin-bottom:18px}.completion-track span,.mix-track span{display:block;height:100%;background:var(--ui-accent);border-radius:inherit}.workload-list{display:grid;gap:3px}.workload-list>div{display:flex;align-items:center;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--ui-border)}.workload-list>div:last-child{border-bottom:0}.workload-list span{display:flex;align-items:center;gap:8px;color:#475467}.workload-list i{width:7px;height:7px;border-radius:50%;background:var(--ui-accent)}.workload-list strong{font-size:12px}.panel-link{display:flex;align-items:center;justify-content:space-between;width:100%;margin-top:auto;padding:10px 0 0!important;background:transparent!important;border:0!important;border-top:1px solid var(--ui-border)!important;border-radius:0!important;color:var(--ui-accent)!important;font-weight:600}.memory-mix{display:grid;gap:16px}.memory-mix>div>div:first-child{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}.memory-mix span{color:#475467;text-transform:capitalize}.memory-mix strong{font-size:11px}.empty-compact{padding:28px;text-align:center;color:var(--ui-muted)}.inventory-grid{display:grid;grid-template-columns:1fr 1fr;border:1px solid var(--ui-border);border-radius:7px;overflow:hidden}.inventory-grid>div{padding:14px;border-right:1px solid var(--ui-border);border-bottom:1px solid var(--ui-border)}.inventory-grid>div:nth-child(2n){border-right:0}.inventory-grid>div:nth-last-child(-n+2){border-bottom:0}.inventory-grid span,.inventory-grid strong{display:block}.inventory-grid span{color:var(--ui-muted);font-size:11px}.inventory-grid strong{margin-top:4px;font:600 17px Geist}.system-row{display:flex;align-items:center;gap:10px;margin-top:auto;padding:13px;background:var(--ui-accent-soft);border:1px solid #d8defd;border-radius:7px}.system-dot{width:8px;height:8px;border-radius:50%;background:var(--ui-accent)}.system-row strong,.system-row small{display:block}.system-row strong{color:#3730a3;font-size:11px}.system-row small{color:#6366a8;font-size:10px}.overview-table-actions{display:flex;align-items:center;gap:10px}.overview-table-actions button{min-height:30px;padding:5px 9px}body[data-theme="dark"] .overview-kpi,body[data-theme="dark"] .dashboard-panel{background:var(--ui-surface)!important;border-color:var(--ui-border)!important}body[data-theme="dark"] .overview-kpi:hover{background:#1a2330!important;border-color:#4a5285!important}body[data-theme="dark"] .overview-kpi-copy strong,body[data-theme="dark"] .dashboard-panel h2{color:var(--ui-text)}body[data-theme="dark"] .workload-list>div,body[data-theme="dark"] .panel-link{border-color:var(--ui-border)!important}body[data-theme="dark"] .workload-list span,body[data-theme="dark"] .memory-mix span{color:#bdc6d0}body[data-theme="dark"] .completion-track,body[data-theme="dark"] .mix-track{background:#26313e}body[data-theme="dark"] .inventory-grid{border-color:var(--ui-border)}body[data-theme="dark"] .inventory-grid>div{border-color:var(--ui-border)}body[data-theme="dark"] .system-row{background:var(--ui-accent-soft);border-color:#3d4679}body[data-theme="dark"] .system-row strong{color:#c7d2fe}body[data-theme="dark"] .system-row small{color:#a8b0df}@media(max-width:1200px){.overview-kpis{grid-template-columns:repeat(2,1fr)}.overview-dashboard-grid{grid-template-columns:1fr 1fr}.inventory-panel{grid-column:1/-1;min-height:220px}.inventory-grid{grid-template-columns:repeat(4,1fr)}.inventory-grid>div{border-bottom:0}.inventory-grid>div:nth-child(2){border-right:1px solid var(--ui-border)}}@media(max-width:760px){.overview-hero{align-items:flex-start}.overview-hero-actions{width:100%}.overview-hero-actions button{flex:1}.overview-dashboard-grid{grid-template-columns:1fr}.inventory-panel{grid-column:auto}.inventory-grid{grid-template-columns:1fr 1fr}.inventory-grid>div:nth-child(2){border-right:0}.inventory-grid>div:nth-child(-n+2){border-bottom:1px solid var(--ui-border)}}@media(max-width:480px){.overview-kpis{grid-template-columns:1fr}.overview-kpi{min-height:112px;padding:20px!important}.overview-table-actions .record-count{display:none}}
</style>
<style>
/* Full-width adaptive workspace */
body{width:100%;max-width:none;overflow-x:hidden}.top,.wrap{width:auto;min-width:0;max-width:none}.wrap{justify-self:stretch;margin:0!important}.wrap>#app,#app>section,#app>header,.task-screen,.task-panel,.record-panel,.overview-section,.overview-kpis,.overview-dashboard-grid,.overview-recent,.members-layout{width:100%!important;max-width:none!important;min-width:0!important}.card,.form-card,.members-card,.dashboard-panel,.metric-grid-primary,.metric-strip{max-width:none!important;min-width:0}.table{width:100%!important;max-width:100%!important;min-width:0!important}table{width:100%!important;min-width:100%}.sidebar-collapsed .wrap,.sidebar-collapsed .top{width:auto!important;max-width:none!important}.sidebar-collapsed .wrap>#app{width:100%!important;max-width:none!important}@media(min-width:901px){body:not(.sidebar-collapsed) .wrap{padding-left:36px;padding-right:36px}body.sidebar-collapsed .wrap{padding-left:36px;padding-right:36px}}@media(max-width:900px){.wrap{width:100%!important;max-width:none!important;padding-left:22px;padding-right:22px}}@media(max-width:640px){.wrap{padding-left:14px;padding-right:14px}.record-panel,.task-panel{width:100%!important}}

/* Dark Blue Theme, Button, Border, Tag, and Pill Overrides */
:root {
  --ui-bg: #f4f6fa;
  --ui-surface: #ffffff;
  --ui-subtle: #edf2f9;
  --ui-muted: #566479;
  --ui-text: #0f172a;
  --ui-border: #cbd5e1;
  --ui-border-strong: #94a3b8;
  --ui-accent: #1d4ed8;
  --ui-accent-dark: #1e3a8a;
  --ui-accent-soft: #eff6ff;
  --ui-shadow: 0 1px 3px rgba(15,23,42,0.08);
}
body[data-theme="dark"] {
  --ui-bg: #0b111e;
  --ui-surface: #10192a;
  --ui-subtle: #172338;
  --ui-muted: #94a3b8;
  --ui-text: #f1f5f9;
  --ui-border: #233550;
  --ui-border-strong: #334b6e;
  --ui-accent: #3b82f6;
  --ui-accent-dark: #2563eb;
  --ui-accent-soft: #14243d;
  background: #0b111e !important;
  color: #f1f5f9 !important;
}
body[data-theme="dark"] .sidebar {
  background: #0d1524 !important;
  border-right-color: #233550 !important;
}
body[data-theme="dark"] .top {
  background: #0e1726 !important;
  border-bottom-color: #233550 !important;
}
body[data-theme="dark"] .top .refresh-btn,
body[data-theme="dark"] .top .theme-toggle {
  background: #172338 !important;
  border: 1px solid #334b6e !important;
  color: #f1f5f9 !important;
}
body[data-theme="dark"] .top .refresh-btn:hover,
body[data-theme="dark"] .top .theme-toggle:hover {
  background: #1e2f4a !important;
  border-color: #476694 !important;
}
body[data-theme="dark"] .top .refresh-btn .uicon,
body[data-theme="dark"] .top .theme-toggle .uicon {
  color: #93c5fd !important;
}
body[data-theme="dark"] .theme-toggle span {
  color: #f1f5f9 !important;
}
body[data-theme="dark"] button {
  background: #172338 !important;
  border: 1px solid #233550 !important;
  color: #f1f5f9 !important;
}
body[data-theme="dark"] button:hover {
  background: #1e2f4a !important;
  border-color: #3b82f6 !important;
  color: #ffffff !important;
}
body[data-theme="dark"] button.primary,
body[data-theme="dark"] .task-create {
  background: #2563eb !important;
  border-color: #3b82f6 !important;
  color: #ffffff !important;
}
body[data-theme="dark"] button.primary:hover,
body[data-theme="dark"] .task-create:hover {
  background: #1d4ed8 !important;
}
/* Buttons with icons: prevent text overlap */
button {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
}
/* Side menu / navigation tabs: align to start ordered by icons */
.sidebar .tabs button,
.tabs button,
aside.sidebar .tabs button,
body .sidebar .tabs button,
body:not(.sidebar-collapsed) .tabs button {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  text-align: start !important;
}
.sidebar .tabs button > span,
.tabs button > span,
aside.sidebar .tabs button > span {
  text-align: start !important;
  justify-content: flex-start !important;
  margin-left: 0 !important;
  flex: 1 1 auto !important;
}
.sidebar .brand,
aside.sidebar .brand,
body:not(.sidebar-collapsed) .sidebar .brand {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  text-align: start !important;
}
.sidebar .system-state,
aside.sidebar .system-state,
body:not(.sidebar-collapsed) .sidebar .system-state {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  text-align: start !important;
}
.sidebar .sidebar-foot,
aside.sidebar .sidebar-foot,
body:not(.sidebar-collapsed) .sidebar-foot {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  text-align: start !important;
}
body.sidebar-collapsed .tabs button {
  justify-content: center !important;
  text-align: center !important;
}
.sidebar .tabs button .uicon,
button .uicon {
  flex-shrink: 0 !important;
  margin: 0 !important;
}
.page-actions {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
}
.page-actions button {
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
}
/* Tags and Pills in light and dark mode */
.memory-tag,
.tag-pill,
.pill,
.status-chip,
.review-label {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  line-height: 1.4 !important;
  padding: 4px 10px !important;
  border-radius: 99px !important;
  border: 1px solid #bfdbfe !important;
  background: #eff6ff !important;
  color: #1d4ed8 !important;
}
.pill.open, .pill.working, .pill.reopened {
  background: #eff6ff !important;
  border-color: #bfdbfe !important;
  color: #1d4ed8 !important;
}
.pill.done {
  background: #ecfdf5 !important;
  border-color: #a7f3d0 !important;
  color: #065f46 !important;
}
.pill.closed {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #475569 !important;
}
body[data-theme="dark"] .memory-tag,
body[data-theme="dark"] .tag-pill,
body[data-theme="dark"] .pill,
body[data-theme="dark"] .status-chip,
body[data-theme="dark"] .review-label {
  background: #14243d !important;
  border-color: #2a4368 !important;
  color: #93c5fd !important;
}
body[data-theme="dark"] .pill.open,
body[data-theme="dark"] .pill.working,
body[data-theme="dark"] .pill.reopened {
  background: #172c4e !important;
  border-color: #2a4878 !important;
  color: #bfdbfe !important;
}
body[data-theme="dark"] .pill.done {
  background: #0f2e22 !important;
  border-color: #1b533d !important;
  color: #6ee7b7 !important;
}
body[data-theme="dark"] .pill.closed {
  background: #151f30 !important;
  border-color: #233550 !important;
  color: #94a3b8 !important;
}
/* Reorganized Memory Detail View */
.memory-detail-view {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.memory-header-card {
  padding: 18px;
  background: var(--ui-subtle);
  border: 1px solid var(--ui-border);
  border-radius: 10px;
}
.memory-header-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.memory-header-card h2 {
  margin: 0 0 8px;
  font-size: 20px;
  font-weight: 700;
  color: var(--ui-text);
  word-break: break-word;
}
.memory-id-line {
  font-size: 11px;
  color: var(--ui-muted);
}
.memory-id-line code {
  background: var(--ui-surface);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid var(--ui-border);
  font-family: ui-monospace, monospace;
}
.memory-stat-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 10px;
}
.memory-stat-card {
  padding: 12px 14px;
  background: var(--ui-surface);
  border: 1px solid var(--ui-border);
  border-radius: 8px;
}
.memory-stat-card small {
  display: block;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ui-muted);
  margin-bottom: 4px;
}
.memory-stat-card strong {
  font-size: 18px;
  color: var(--ui-accent);
}
.memory-stat-card span {
  font-size: 12px;
  color: var(--ui-text);
  word-break: break-all;
}
.memory-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.memory-section-title {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--ui-muted);
}
.memory-content-box {
  background: var(--ui-subtle);
  border: 1px solid var(--ui-border);
  border-radius: 8px;
  padding: 14px 16px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  color: var(--ui-text);
}
.memory-tags-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}
.memory-meta-box {
  background: var(--ui-subtle);
  border: 1px solid var(--ui-border);
  border-radius: 8px;
  padding: 12px 14px;
}
.memory-meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 10px;
}
.memory-meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 12px;
}
.memory-meta-item strong {
  color: var(--ui-muted);
  font-size: 11px;
}
.memory-meta-item span {
  color: var(--ui-text);
  word-break: break-all;
}
.memory-raw-details {
  margin-top: 8px;
  border: 1px solid var(--ui-border);
  border-radius: 8px;
  padding: 8px 12px;
  background: var(--ui-surface);
}
.memory-raw-details summary {
  cursor: pointer;
  font-weight: 600;
  font-size: 12px;
  color: var(--ui-muted);
}


/* Sidebar layout: one explicit expanded/compact state at every viewport. */
body {grid-template-columns:240px minmax(0,1fr);}
body.sidebar-collapsed {grid-template-columns:72px minmax(0,1fr);}
body .sidebar {min-height:0;height:100dvh;overflow:hidden;}
body .sidebar .brand {height:72px;min-height:72px;padding:0 16px;gap:10px;}
body .sidebar .brand-mark {display:grid;flex:0 0 30px;width:30px;height:30px;}
body .sidebar .brand-name {display:block;font-size:14px;white-space:nowrap;}
body .sidebar .sidebar-toggle {display:inline-flex!important;flex:0 0 32px;width:32px;height:32px;margin-left:auto;}
.sidebar-toggle span {border:0;width:16px;height:16px;}
.sidebar-toggle span:after {width:7px;height:7px;left:6px;top:4px;border:0;border-left:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg);}
body .sidebar .system-state {display:flex!important;flex-shrink:0;padding:12px 18px;font-size:11px;}
body .sidebar .tabs {display:flex;flex:1;min-height:0;flex-direction:column;gap:20px;padding:16px 12px;overflow-y:auto;overflow-x:hidden;}
.nav-group {display:grid;gap:4px;}
.nav-group:not(:has(button:not([hidden]))) {display:none;}
.nav-group-label {padding:0 10px 6px;font-size:10px;line-height:16px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--ui-muted);}
body .sidebar .tabs button {min-width:0;min-height:40px;padding:10px!important;gap:12px!important;white-space:normal;}
body:not(.sidebar-collapsed) .sidebar .tabs button > span {display:block;line-height:1.4;}
body .sidebar .tabs button .uicon {width:18px;height:18px;flex:0 0 18px;}
body .sidebar .sidebar-foot {display:flex!important;align-items:center!important;justify-content:flex-start!important;flex-shrink:0;gap:10px;margin:8px 12px 12px!important;padding:12px!important;border-radius:8px;font-size:12px;}
.sidebar-sync-icon {display:grid;place-items:center;flex:0 0 28px;width:28px;height:28px;border-radius:8px;background:#dcfce7;color:#15803d;}
.sidebar-sync-icon .uicon {width:18px;height:18px;}
.sidebar-sync-copy {display:flex;flex-direction:column;gap:3px;min-width:0;text-align:left;}
.sidebar-sync-copy strong {font-size:12px;line-height:1.4;font-weight:600;color:var(--ui-text);}
.sidebar-sync-copy small {font-size:11px;line-height:1.4;color:var(--ui-muted);}
body[data-theme="dark"] .sidebar-sync-icon {background:#153b2c;color:#86efac;}
body:not(.sidebar-collapsed) .sidebar-foot span:first-child {display:block;}
body.sidebar-collapsed .sidebar .brand {padding:0;justify-content:center!important;}
body.sidebar-collapsed .sidebar .brand-mark,
body.sidebar-collapsed .sidebar .brand-name,
body.sidebar-collapsed .sidebar .system-state,
body.sidebar-collapsed .sidebar .nav-group-label {display:none!important;}
body.sidebar-collapsed .sidebar .sidebar-toggle {margin:0;}
body.sidebar-collapsed .sidebar-toggle span:after {left:2px;transform:rotate(225deg);}
body.sidebar-collapsed .sidebar .tabs {padding:16px 12px;gap:12px;}
body.sidebar-collapsed .nav-group + .nav-group {border-top:1px solid var(--ui-border);padding-top:12px;}
body.sidebar-collapsed .sidebar .tabs button {justify-content:center!important;}
body.sidebar-collapsed .sidebar .sidebar-foot {justify-content:center!important;gap:0;margin:8px 12px 12px!important;padding:9px 0!important;}
body.sidebar-collapsed .sidebar-sync-copy {display:none;}
@media (min-width:641px) and (max-width:900px) {
 body:not(.sidebar-collapsed) {grid-template-columns:240px minmax(0,1fr);}
}
@media (max-width:640px) {
 body,body.sidebar-collapsed {display:grid;grid-template-columns:64px minmax(0,1fr);grid-template-rows:64px 1fr;}
 body .sidebar {position:fixed;top:0;bottom:0;left:0;right:auto;width:240px;border-right:1px solid var(--ui-border);border-top:0;box-shadow:12px 0 30px #10182826;}
 body.sidebar-collapsed .sidebar {width:64px;box-shadow:none;}
 body .sidebar .brand {height:64px;min-height:64px;}
 body.sidebar-collapsed .sidebar .tabs {padding:12px 8px;}
 body.sidebar-collapsed .sidebar .sidebar-foot {margin:8px!important;}
 body .top {grid-column:2;grid-row:1;}
 body .wrap {grid-column:2;grid-row:2;padding:20px 12px 32px;}
}

/* Compact task rows; the title button remains the keyboard entry to details. */
.task-table th,.task-table td {padding:8px 12px;vertical-align:middle;}
.task-table th {font-size:10px;}
.task-table tbody .task-row {cursor:pointer;}
.task-table .task-title-cell {width:auto;min-width:180px;}
.task-table .task-title-link {min-height:0;padding:0!important;background:transparent!important;border:0!important;box-shadow:none!important;font-size:13px;line-height:1.4;text-align:left;justify-content:flex-start!important;}
.task-table .task-subline {margin-top:2px;gap:8px;font-size:11px;line-height:1.4;}
.task-table .task-action-group {flex-wrap:nowrap;gap:4px;}
.task-table .task-actions-cell {width:1%;white-space:nowrap;}
.task-table .task-icon-action {width:30px;height:30px;min-height:30px;flex:0 0 30px;padding:0!important;}
.task-table .task-icon-action .uicon {width:15px;height:15px;}
.task-table .task-date {font-size:11px;}
.task-table .task-date small {margin-left:5px;font-size:10px;}
.task-table .member-status-select {min-height:30px;padding:5px 24px 5px 8px;font-size:11px;}
@media(pointer:coarse) {
 .task-table .task-icon-action {width:40px;height:40px;min-height:40px;flex-basis:40px;}
}
/* Task-only detail layout; other record dialogs retain their layout. */
#detail:has(.task-detail-view) {width:min(820px,100vw);}
#detail:has(.task-detail-view) .detail-head {align-items:flex-start;gap:16px;padding:18px 24px;}
#detail:has(.task-detail-view) #detail-title {font:600 19px/1.4 Geist,system-ui,sans-serif;overflow-wrap:anywhere;min-width:0;flex:1;}
#detail:has(.task-detail-view) .detail-head>.task-action-group {justify-content:flex-end;gap:6px;max-width:50%;}
#detail:has(.task-detail-view) .detail-body {padding:24px;}
.task-detail-view {display:grid;gap:20px;min-width:0;}
.task-detail-intro {display:flex;align-items:center;justify-content:space-between;gap:12px;}
.task-detail-kicker {font-size:10px;font-weight:700;letter-spacing:.12em;color:var(--ui-muted);}
.task-detail-meta {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 24px;margin:0;padding:16px;background:var(--ui-subtle);border:1px solid var(--ui-border);border-radius:8px;}
.task-detail-meta dt {font-size:11px;color:var(--ui-muted);margin-bottom:6px;}
.task-detail-meta dd {margin:0;font-size:13px;font-weight:600;overflow-wrap:anywhere;}
.task-detail-meta>div:nth-child(2) dd {text-transform:capitalize;}
.task-detail-section {padding:18px;border:1px solid var(--ui-border);border-radius:8px;min-width:0;}
.task-section-heading {display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;}
#detail .task-section-heading h3 {margin:0;padding:0;border:0;font-size:14px;}
.task-section-heading>span {font-size:11px;color:var(--ui-muted);text-align:right;}
.task-description {font-size:13px;line-height:1.75;overflow-wrap:anywhere;}
.task-description>:first-child {margin-top:0;}.task-description>:last-child {margin-bottom:0;}
.task-description img,.task-description video,.task-description iframe {max-width:100%;}
.task-description pre {white-space:pre-wrap;overflow-wrap:anywhere;}
.task-progress-fields {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;}
.task-progress-fields label {margin:0;font-size:11px;min-width:0;}
.task-progress-fields select {width:100%;min-width:0;font-size:12px;}
.task-section-actions {display:flex;justify-content:flex-end;margin-top:14px;}
.task-detail-view .task-file {display:flex;align-items:flex-start;justify-content:space-between;gap:12px;padding:12px;margin:0 0 8px;}
.task-file-copy {display:grid;gap:5px;min-width:0;overflow-wrap:anywhere;}
.task-file-copy strong {font-size:12px;}.task-file-copy small,.task-file-paths {font-size:11px;}
.task-file-paths summary {cursor:pointer;color:var(--ui-muted);}.task-file-paths .path {white-space:normal;overflow-wrap:anywhere;margin-top:6px;}
.task-detail-view .drop-zone {margin-top:12px;padding:14px;font-size:12px;}
.task-upload-actions {display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:10px;font-size:11px;}
#detail-file-list {overflow-wrap:anywhere;min-width:0;}
.task-detail-empty {margin:0;padding:12px 0;font-size:12px;color:var(--ui-muted);}
.task-event-heading {display:flex;justify-content:space-between;align-items:flex-start;gap:10px;}
.task-event-heading strong {font-size:12px;text-transform:capitalize;}
.task-event-heading time {font-size:10px;color:var(--ui-muted);flex-shrink:0;}
.task-event-note {white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;line-height:1.6;margin-top:6px;}
.task-note-form {margin-top:16px;}.task-note-form label {font-size:12px;margin:0 0 8px;}
.task-note-form textarea {width:100%;resize:vertical;line-height:1.6;font:inherit;}
.task-console {background:var(--ui-subtle);}
.task-console-toolbar {display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;}
.task-console-toolbar select {min-width:180px;max-width:100%;font-size:12px;}
.console-events {display:grid;gap:8px;max-height:360px;overflow:auto;margin:12px 0;padding-right:4px;}
.console-event {padding:10px 12px;border:1px solid var(--ui-border);border-radius:7px;background:var(--ui-surface);}
.console-event-head {display:flex;justify-content:space-between;gap:10px;color:var(--ui-muted);font-size:10px;text-transform:capitalize;}
.console-event-content {margin-top:5px;white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;line-height:1.55;}
.console-composer {display:grid;gap:8px;margin-top:12px;}
.console-composer textarea {width:100%;resize:vertical;line-height:1.5;font:inherit;}
.console-actions {display:flex;justify-content:flex-end;gap:8px;flex-wrap:wrap;}
.task-detail-dates {display:flex;flex-wrap:wrap;gap:6px 16px;font-size:10px;color:var(--ui-muted);}
@media(max-width:600px){
 #detail:has(.task-detail-view) .detail-head {flex-direction:column;padding:16px;}
 #detail:has(.task-detail-view) .detail-head>.task-action-group {max-width:none;width:100%;justify-content:flex-start;}
 #detail:has(.task-detail-view) .detail-body {padding:16px;}
 .task-detail-view {gap:14px;}.task-detail-section {padding:14px;}
 .task-progress-fields {grid-template-columns:1fr;}.task-event-heading {flex-direction:column;gap:4px;}
 .task-upload-actions {align-items:flex-start;flex-direction:column;}
}

#detail .detail-head .detail-icon-action {width:34px;height:34px;min-height:34px;flex:0 0 34px;padding:0!important;}
#detail .detail-head .detail-icon-action .uicon {width:17px;height:17px;}
#detail:has(.task-detail-view) .detail-head>.task-action-group {max-width:none;flex-shrink:0;flex-wrap:nowrap;}
@media(pointer:coarse){#detail .detail-head .detail-icon-action {width:40px;height:40px;min-height:40px;flex-basis:40px;}}

#task-editor .approval-banner[hidden],#task-upload-section[hidden],#task-drop[hidden] {display:none!important;}
#task-description-editor.ql-container {height:auto;}
#task-description-editor .ql-editor {min-height:140px;max-height:260px;overflow-y:auto;padding:12px 14px;font-size:13px;line-height:1.6;}
#task-description-editor.fallback-editor {min-height:140px;max-height:260px;overflow-y:auto;padding:12px 14px;}
#task-editor .ql-toolbar {padding:6px 8px;}
#task-editor .ql-toolbar .ql-formats {margin-right:10px;margin-bottom:3px;}
/* Quill controls must not inherit the application's full-size button layout. */
#task-editor .ql-toolbar.ql-snow button {display:inline-flex!important;align-items:center!important;justify-content:center!important;width:28px;height:28px;min-height:28px;padding:4px!important;border:0!important;background:transparent!important;color:var(--ui-text)!important;box-shadow:none!important;gap:0!important;}
#task-editor .ql-toolbar.ql-snow button svg {display:block;width:18px;height:18px;flex:0 0 18px;}
#task-editor .ql-toolbar.ql-snow .ql-formats {display:inline-flex;align-items:center;vertical-align:middle;}
#task-editor .ql-toolbar.ql-snow .ql-picker {color:var(--ui-text);height:28px;}
#task-editor .ql-toolbar.ql-snow .ql-picker-label {display:flex;align-items:center;height:28px;border-color:transparent;}
#task-editor .ql-toolbar.ql-snow .ql-picker-options {background:var(--ui-surface);border:1px solid var(--ui-border)!important;border-radius:6px;box-shadow:0 6px 20px #0003;z-index:10;}
#task-editor .ql-toolbar.ql-snow .ql-picker.ql-expanded .ql-picker-label {color:var(--ui-accent);border-color:var(--ui-border);}
body[data-theme="dark"] #task-editor .ql-toolbar.ql-snow .ql-stroke:not(.ql-color-label) {stroke:currentColor!important;}
body[data-theme="dark"] #task-editor .ql-toolbar.ql-snow .ql-fill:not(.ql-color-label) {fill:currentColor!important;}
#task-editor .ql-toolbar.ql-snow button:hover,
#task-editor .ql-toolbar.ql-snow button.ql-active,
#task-editor .ql-toolbar.ql-snow .ql-picker-label:hover,
#task-editor .ql-toolbar.ql-snow .ql-picker-label.ql-active {color:var(--ui-accent)!important;background:var(--ui-accent-soft)!important;border-radius:4px;}
#task-editor .ql-toolbar.ql-snow .ql-picker-item:hover,
#task-editor .ql-toolbar.ql-snow .ql-picker-item.ql-selected {color:var(--ui-accent)!important;}
#task-editor .ql-toolbar.ql-snow .ql-color-picker .ql-picker-item {border:1px solid var(--ui-border-strong);}
#task-editor .ql-toolbar.ql-snow .ql-color-picker .ql-picker-item:hover,
#task-editor .ql-toolbar.ql-snow .ql-color-picker .ql-picker-item.ql-selected {outline:2px solid var(--ui-accent);outline-offset:1px;}
#task-editor .ql-toolbar.ql-snow button:focus-visible,
#task-editor .ql-toolbar.ql-snow .ql-picker-label:focus-visible,
#task-editor .ql-toolbar.ql-snow .ql-picker-item:focus-visible {outline:2px solid var(--ui-accent);outline-offset:2px;}
body[data-theme="dark"] #task-editor .ql-editor.ql-blank:before {color:var(--ui-muted);}
body[data-theme="dark"] #task-editor .ql-tooltip {background:var(--ui-surface);color:var(--ui-text);border-color:var(--ui-border);box-shadow:0 6px 20px #0005;}
body[data-theme="dark"] #task-editor .ql-tooltip a {color:var(--ui-accent);}

#task-upload-section {margin-top:24px;padding-top:20px;border-top:1px solid var(--ui-border);}
#task-upload-section .task-section-heading h3 {margin:0;font-size:14px;}
#task-upload-section>p {font-size:11px;line-height:1.5;margin:12px 0 0;}
#task-existing-files,#task-file-list,#detail-file-list {display:grid;gap:8px;}
#task-existing-files:empty {display:none;}
.attachment-list-label {font-size:11px;font-weight:600;color:var(--ui-muted);margin:12px 0 2px;}
.attachment-row {display:flex;align-items:center;gap:12px;padding:12px;border:1px solid var(--ui-border);border-radius:8px;background:var(--ui-subtle);min-width:0;}
.attachment-file-icon {width:32px;height:36px;flex:0 0 32px;display:grid;place-items:center;border-radius:6px;background:var(--ui-accent-soft);color:var(--ui-accent);}
.attachment-file-copy {display:grid;gap:4px;flex:1;min-width:0;}
.attachment-file-copy strong {font-size:12px;overflow-wrap:anywhere;line-height:1.4;}
.attachment-file-copy small {font-size:11px;color:var(--ui-muted);}
.attachment-row button,.member-actions button {width:34px;height:34px;min-height:34px;padding:0!important;flex:0 0 34px;}
.attachment-empty {font-size:12px;color:var(--ui-muted);padding:10px 0;margin:0;}
.member-table .member-actions {width:1%;text-align:right;white-space:nowrap;}
.member-table tbody tr {cursor:default;}
#task-editor .detail-body>label {margin:16px 0;}
#task-editor .detail-body>p {font-size:12px;line-height:1.5;margin:8px 0 12px;}
/* Render saved Quill content with the same typography as its editor. */
#task-description-editor .ql-editor,
#task-description-editor.fallback-editor,
#detail .task-description.ql-editor {
 font-family:system-ui,sans-serif;font-size:13px;line-height:1.6;letter-spacing:normal;
 padding:12px 14px;text-align:left;white-space:pre-wrap;overflow-wrap:anywhere;
}
#detail .task-description.ql-editor {height:auto;overflow:visible;}
#task-description-editor .ql-editor :is(p,h1,h2,h3,h4,h5,h6),
#detail .task-description.ql-editor :is(p,h1,h2,h3,h4,h5,h6) {
 margin:0;padding:0;border:0;font-family:inherit;line-height:inherit;color:inherit;
}
#task-description-editor .ql-editor :is(h1,h2,h3,h4,h5,h6),
#detail .task-description.ql-editor :is(h1,h2,h3,h4,h5,h6) {font-weight:700;}
#task-description-editor .ql-editor h1,#detail .task-description.ql-editor h1 {font-size:2em;}
#task-description-editor .ql-editor h2,#detail .task-description.ql-editor h2 {font-size:1.5em;}
#task-description-editor .ql-editor h3,#detail .task-description.ql-editor h3 {font-size:1.17em;}
#task-description-editor .ql-editor h4,#detail .task-description.ql-editor h4 {font-size:1em;}
#task-description-editor .ql-editor h5,#detail .task-description.ql-editor h5 {font-size:.83em;}
#task-description-editor .ql-editor h6,#detail .task-description.ql-editor h6 {font-size:.67em;}
#task-description-editor .ql-editor blockquote,#detail .task-description.ql-editor blockquote {margin:5px 0;padding-left:16px;border-left:4px solid var(--ui-border-strong);}
#task-description-editor .ql-editor pre,#detail .task-description.ql-editor pre {margin:5px 0;padding:5px 10px;white-space:pre-wrap;background:var(--ui-subtle);border-radius:3px;}
#detail .task-body.ql-editor li[data-list="checked"],
#detail .task-body.ql-editor li[data-list="unchecked"] {cursor:pointer;}
#detail .task-body.ql-editor li[data-list]:focus-visible {outline:2px solid var(--ui-accent);outline-offset:2px;}
body[data-theme="dark"] #task-description-editor .ql-editor li>.ql-ui,
body[data-theme="dark"] #detail .task-description.ql-editor li>.ql-ui {color:var(--ui-muted);}

.instruction-content {white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;line-height:1.65;}
.instruction-table .instruction-title {padding:0!important;min-height:0;background:transparent!important;text-align:left;white-space:normal;font-weight:600;}
.instruction-table .task-action-group {flex-wrap:nowrap;gap:6px;}
.instruction-table .task-action-group button {width:32px;height:32px;min-height:32px;padding:0!important;}
.instruction-table tbody tr:after {display:none;}
.instruction-table td:last-child {width:1%;}
.instruction-options {display:grid;gap:8px;}
.instruction-option {display:flex;align-items:flex-start;gap:12px;padding:14px;border:1px solid var(--ui-border);border-radius:8px;margin:0;cursor:pointer;}
.instruction-option input {width:16px;min-height:16px;margin:3px 0 0;flex-shrink:0;}
.instruction-option span {display:grid;gap:5px;min-width:0;overflow-wrap:anywhere;}
.instruction-option small,.mapped-instruction small {font-size:11px;color:var(--ui-muted);font-weight:400;}
.mapped-instruction {padding:12px;border:1px solid var(--ui-border);border-radius:6px;margin-top:8px;}
.mapped-instruction summary {font-size:13px;font-weight:600;cursor:pointer;overflow-wrap:anywhere;}
.mapped-instruction .instruction-content {margin-top:10px;}
</style>
<script>
let memberMode=false;let tab='overview',busy=false,searchTimer,cursors=[],cursor=null,hasMore=false,taskQuill=null,taskFiles=[],detailFiles=[],editingTaskId=null,taskStatusFilter='all',taskPriorityFilter='all';const $=id=>document.getElementById(id);const key=()=>$('key').value||'dev-key';const toastStack=document.createElement('div');toastStack.className='toast-stack';document.body.append(toastStack);function toast(message,type='success'){const el=document.createElement('div');el.className='toast '+(type==='error'?'error-toast':'success');el.textContent=message;toastStack.append(el);setTimeout(()=>el.remove(),3200)}
const iconPaths={home:'<path d="M8 17h8M11.018 2.764 4.235 8.039c-.453.353-.68.53-.843.75a2 2 0 0 0-.318.65C3 9.704 3 9.991 3 10.565V17.8c0 1.12 0 1.68.218 2.108a2 2 0 0 0 .874.874C4.52 21 5.08 21 6.2 21h11.6c1.12 0 1.68 0 2.108-.218a2 2 0 0 0 .874-.874C21 19.48 21 18.92 21 17.8v-7.235c0-.574 0-.861-.074-1.126a2 2 0 0 0-.318-.65c-.163-.22-.39-.397-.843-.75l-6.783-5.275c-.351-.273-.527-.41-.72-.462a1 1 0 0 0-.523 0c-.194.052-.37.189-.721.462Z"/>',check:'<path d="m7.5 12 3 3 6-6M7.8 21h8.4c1.68 0 2.52 0 3.162-.327a3 3 0 0 0 1.311-1.311C21 18.72 21 17.88 21 16.2V7.8c0-1.68 0-2.52-.327-3.162a3 3 0 0 0-1.311-1.311C18.72 3 17.88 3 16.2 3H7.8c-1.68 0-2.52 0-3.162.327a3 3 0 0 0-1.311 1.311C3 5.28 3 6.12 3 7.8v8.4c0 1.68 0 2.52.327 3.162a3 3 0 0 0 1.311 1.311C5.28 21 6.12 21 7.8 21Z"/>',folder:'<path d="m13 7-1.116-2.231c-.32-.642-.481-.963-.72-1.198a2 2 0 0 0-.748-.462C10.1 3 9.74 3 9.022 3H5.2c-1.12 0-1.68 0-2.108.218a2 2 0 0 0-.874.874C2 4.52 2 5.08 2 6.2V7m0 0h15.2c1.68 0 2.52 0 3.162.327a3 3 0 0 1 1.311 1.311C22 9.28 22 10.12 22 11.8v4.4c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C19.72 21 18.88 21 17.2 21H6.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C2 18.72 2 17.88 2 16.2V7Z"/>',database:'<path d="M14 20a2 2 0 1 1-4 0m4 0a2 2 0 0 0-2-2m2 2h7m-11 0a2 2 0 0 1 2-2m-2 2H3m9-2v-4m9-9c0 1.657-4.03 3-9 3S3 6.657 3 5m18 0c0-1.657-4.03-3-9-3S3 3.343 3 5m18 0v6c0 1.66-4 3-9 3M3 5v6c0 1.66 4 3 9 3"/>',user:'<path d="M20 21c0-1.396 0-2.093-.172-2.661a4 4 0 0 0-2.667-2.667c-.568-.172-1.265-.172-2.661-.172h-5c-1.396 0-2.093 0-2.661.172a4 4 0 0 0-2.667 2.667C4 18.907 4 19.604 4 21M16.5 7.5a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0Z"/>',clock:'<path d="m22.7 13.5-2-2-2 2M21 12a9 9 0 1 1-1.245-4.57M12 7v5l3 2"/>',list:'<path d="M21 12H9m12-6H9m12 12H9m-4-6a1 1 0 1 1-2 0 1 1 0 0 1 2 0Zm0-6a1 1 0 1 1-2 0 1 1 0 0 1 2 0Zm0 12a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"/>',shield:'<path d="M11.302 21.615c.221.129.332.194.488.227.122.026.298.026.42 0 .156-.034.267-.098.488-.227C14.646 20.478 20 16.908 20 12V7.217c0-.799 0-1.199-.13-1.542a2 2 0 0 0-.548-.79c-.275-.243-.65-.383-1.398-.664l-5.362-2.01c-.208-.078-.312-.117-.419-.133a1 1 0 0 0-.286 0c-.107.016-.21.055-.419.133L6.076 4.22c-.748.28-1.122.421-1.398.664a2 2 0 0 0-.547.79C4 6.018 4 6.418 4 7.217V12c0 4.908 5.354 8.478 7.302 9.615Z"/>',search:'<path d="m21 21-6-6m2-5a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z"/>',refresh:'<path d="M2 14s.121.85 3.636 4.364A9 9 0 0 0 20.776 14M2 14v6m0-6h6m14-4s-.121-.85-3.636-4.364A9 9 0 0 0 3.224 10M22 10V4m0 6h-6"/>',plus:'<path d="M12 5v14m-7-7h14"/>',edit:'<path d="M2.876 18.116c.046-.414.069-.62.131-.814a2 2 0 0 1 .234-.485c.111-.17.259-.317.553-.61L17 3a2.828 2.828 0 1 1 4 4L7.794 20.206c-.294.294-.442.442-.611.553a2 2 0 0 1-.485.233c-.193.063-.4.086-.814.132L2.5 21.5l.376-3.384Z"/>',trash:'<path d="M9 3h6M3 6h18m-2 0-.701 10.52c-.105 1.578-.158 2.367-.499 2.965a3 3 0 0 1-1.298 1.215c-.62.3-1.41.3-2.993.3h-3.018c-1.582 0-2.373 0-2.993-.3A3 3 0 0 1 6.2 19.485c-.34-.598-.394-1.387-.499-2.966L5 6m5 4.5v5m4-5v5"/>',download:'<path d="M21 15v1.2c0 1.68 0 2.52-.327 3.162a3 3 0 0 1-1.311 1.311C18.72 21 17.88 21 16.2 21H7.8c-1.68 0-2.52 0-3.162-.327a3 3 0 0 1-1.311-1.311C3 18.72 3 17.88 3 16.2V15m14-5-5 5m0 0-5-5m5 5V3"/>',close:'<path d="M17 7 7 17M7 7l10 10"/>',filter:'<path d="M6 12h12M3 6h18M9 18h6"/>'};
function icon(name,label=''){return '<svg class="uicon" viewBox="0 0 24 24" fill="none" aria-hidden="'+(label?'false':'true')+'"'+(label?' aria-label="'+esc(label)+'"':'')+'>'+iconPaths[name]+'</svg>'}function decorateIcons(root=document){const nav={overview:'home',tasks:'check',projects:'folder',memories:'database',agents:'user',sessions:'clock',instructions:'list',audit:'shield',members:'user'};root.querySelectorAll('[data-tab]').forEach(b=>{if(!b.querySelector('.uicon'))b.insertAdjacentHTML('afterbegin',icon(nav[b.dataset.tab]))});const rules=[['New task','plus'],['Create task','plus'],['Add member','plus'],['Refresh','refresh'],['Edit','edit'],['Delete','trash'],['Download','download'],['Close','close'],['Reset filters','filter']];root.querySelectorAll('button').forEach(b=>{const text=b.textContent.trim();const hit=rules.find(([match])=>text.includes(match));if(hit&&!b.querySelector('.uicon')&&!b.querySelector('svg'))b.insertAdjacentHTML('afterbegin',icon(hit[1]))});const search=document.querySelector('.global-search');if(search&&!search.querySelector('.uicon'))search.insertAdjacentHTML('afterbegin',icon('search','Search'))}
function removeLegacyGlyphs(root=document){root.querySelectorAll('.task-create>span[aria-hidden]').forEach(el=>el.remove());root.querySelectorAll('button').forEach(button=>{for(const node of button.childNodes){if(node.nodeType===Node.TEXT_NODE){node.textContent=node.textContent.replace(/^[\s＋+↻]+\s*/,'');}}})}
function applyNavigationPermissions(allowedTabs=[],identity=null){const allowed=new Set(allowedTabs);const nav=document.querySelector('.tabs');nav.dataset.authorized=allowed.size?'true':'false';document.querySelectorAll('[data-tab]').forEach(button=>button.hidden=!allowed.has(button.dataset.tab));const current=document.querySelector('[data-tab].active');if(!current||current.hidden){const first=document.querySelector('[data-tab]:not([hidden])');if(first){tab=first.dataset.tab;document.querySelectorAll('[data-tab]').forEach(button=>button.classList.toggle('active',button===first))}}const copy=document.querySelector('.user-copy');if(copy&&identity){copy.querySelector('strong').textContent=identity.role==='dev'?'Workspace Admin':'Workspace Member';copy.querySelector('small').textContent=identity.role==='dev'?'Administrator':'Member access'}}applyNavigationPermissions([]);
function preferredTheme(){const saved=localStorage.getItem('agent-memory-theme');if(saved==='light'||saved==='dark')return saved;return matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}function applyTheme(theme){document.body.dataset.theme=theme;const button=$('theme-toggle');if(button){button.setAttribute('aria-label','Switch to '+(theme==='dark'?'light':'dark')+' theme');button.setAttribute('aria-pressed',String(theme==='dark'));button.querySelector('span:last-child').textContent=theme==='dark'?'Dark':'Light'}}function toggleTheme(){const next=document.body.dataset.theme==='dark'?'light':'dark';localStorage.setItem('agent-memory-theme',next);applyTheme(next)}function setupTheme(){const user=document.querySelector('.user-chip');if(!$('theme-toggle')){const button=document.createElement('button');button.id='theme-toggle';button.className='theme-toggle';button.type='button';button.onclick=toggleTheme;button.innerHTML='<span class="theme-toggle-dot" aria-hidden="true"></span><span>Theme</span>';user.before(button)}applyTheme(preferredTheme())}setupTheme();
function applySidebarState(collapsed){document.body.classList.toggle('sidebar-collapsed',collapsed);const button=$('sidebar-toggle');if(button){button.setAttribute('aria-expanded',String(!collapsed));button.setAttribute('aria-label',collapsed?'Expand navigation':'Collapse navigation');button.title=collapsed?'Expand navigation':'Collapse navigation'}}function setupSidebarToggle(){const brand=document.querySelector('.brand');if(!$('sidebar-toggle')){const button=document.createElement('button');button.id='sidebar-toggle';button.className='sidebar-toggle';button.type='button';button.setAttribute('aria-controls','sidebar-navigation');button.innerHTML='<span aria-hidden="true"></span>';button.onclick=()=>{const collapsed=!document.body.classList.contains('sidebar-collapsed');localStorage.setItem('agent-memory-sidebar',collapsed?'collapsed':'expanded');applySidebarState(collapsed)};brand.append(button)}const saved=localStorage.getItem('agent-memory-sidebar');applySidebarState(saved?saved==='collapsed':matchMedia('(max-width:900px)').matches)}setupSidebarToggle();
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&matchMedia('(max-width:640px)').matches)applySidebarState(true)});
document.querySelector('.tabs').addEventListener('click',event=>{if(event.target.closest('[data-tab]')&&matchMedia('(max-width:640px)').matches)applySidebarState(true)});
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{tab=b.dataset.tab;cursor=null;cursors=[];document.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active',x===b));load()});
// Query the HTTP API directly and keep the visible view current while this tab is open.
$('q').addEventListener('input',()=>{clearTimeout(searchTimer);searchTimer=setTimeout(load,250)});
$('key').addEventListener('input',()=>{applyNavigationPermissions([]);$('app').innerHTML='';clearTimeout(searchTimer);searchTimer=setTimeout(load,400)});
async function api(path,options={}){if(memberMode&&path.startsWith('/v1/agents')&&!options.method)return {items:[]};let r=await fetch(path,{...options,headers:{'X-API-Key':key(),...(options.headers||{})}});let d=await r.json();if(!r.ok)throw Error(d.error?.message||d.detail||r.status);return d}
function esc(v){return String(v??'').replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]))}
function table(items,cols,onrow){if(!items?.length)return '<div class="empty">No records found</div>';return '<div class="table"><table><thead><tr>'+cols.map(x=>'<th>'+x[0]+'</th>').join('')+'</tr></thead><tbody>'+items.map((i,n)=>'<tr data-row="'+n+'">'+cols.map(x=>'<td>'+esc(typeof x[1]==='function'?x[1](i):i[x[1]])+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>'}
async function load(){if(busy||($('member-result')?.textContent&&tab==='members'))return;busy=true;$('error').innerHTML='';$('status').textContent='Validating key…';try{const identity=await api('/v1/me');memberMode=identity.role!=='dev';applyNavigationPermissions(identity.allowed_tabs||[],identity);document.querySelectorAll('[data-tab]').forEach(b=>b.classList.toggle('active',b.dataset.tab===tab));if(tab==='members')await membersView();else if(tab==='overview')await overview();else await records();addManualEntryAction();const now=new Date();$('status').textContent='Live · '+now.toLocaleTimeString();$('updated').textContent='Updated '+now.toLocaleTimeString()+' · auto refresh 5s'}catch(e){applyNavigationPermissions([]);$('app').innerHTML='';$('status').textContent=e.message==='Invalid API key'?'Key required':'Access unavailable';$('error').innerHTML='<div class="error">'+esc(e.message)+'</div>'}finally{removeLegacyGlyphs();decorateIcons();busy=false}}
function pager(){return '<div class="pager"><button onclick="previousPage()" '+(cursors.length?'':'disabled')+'>Previous</button><button onclick="nextPage()" '+(hasMore?'':'disabled')+'>Next</button></div>'}
function nextPage(){if(!hasMore)return;cursors.push(cursor);cursor=window.nextCursor;load()}function previousPage(){if(!cursors.length)return;cursor=cursors.pop()||null;load()}
function showDetail(title,obj){$('detail-approve').hidden=true;$('detail-task-actions').replaceChildren();$('detail-title').textContent=title;$('detail-body').innerHTML='<pre class="json">'+esc(JSON.stringify(obj,null,2))+'</pre>';const d=$('detail');if(!d.open)d.showModal()}
function showMemory(m){
  $('detail-approve').hidden=true;
  $('detail-task-actions').replaceChildren();
  $('detail-title').textContent='Memory Details';
  const tagsHtml=(m.tags||[]).length
    ? m.tags.map(t=>`<span class="memory-tag">${esc(t)}</span>`).join('')
    : '<span class="muted">No tags attached</span>';
  const metaEntries=Object.entries(m.metadata||{});
  const metaHtml=metaEntries.length
    ? `<div class="memory-meta-grid">${metaEntries.map(([k,v])=>`<div class="memory-meta-item"><strong>${esc(k)}</strong><span>${esc(typeof v==='object'?JSON.stringify(v):v)}</span></div>`).join('')}</div>`
    : '<p class="muted" style="margin:0;font-size:12px">No structured metadata available</p>';
  $('detail-body').innerHTML=`<div class="memory-detail-view">
    <div class="memory-header-card">
      <div class="memory-header-meta">
        <span class="pill ${esc(m.type||"general")}">${esc(m.type||"memory")}</span>
        <span class="pill ${esc(m.status||"active")}">${esc(m.status||"active")}</span>
      </div>
      <h2>${esc(m.title||m.id)}</h2>
      <div class="memory-id-line">ID: <code>${esc(m.id)}</code></div>
    </div>
    <div class="memory-stat-row">
      <div class="memory-stat-card"><small>Scope</small><strong>${esc(m.scope||"global")}</strong></div>
      <div class="memory-stat-card"><small>Importance</small><strong>${esc(m.importance??0)}</strong></div>
      <div class="memory-stat-card"><small>Project ID</small><span>${esc(m.project_id||"Global (None)")}</span></div>
      <div class="memory-stat-card"><small>Created</small><span>${m.created_at?new Date(m.created_at).toLocaleString():"Unknown"}</span></div>
    </div>
    <div class="memory-section">
      <div class="memory-section-title">Memory Content</div>
      <div class="memory-content-box">${esc(m.content||"(Empty content)")}</div>
    </div>
    <div class="memory-section">
      <div class="memory-section-title">Tags</div>
      <div class="memory-tags-wrap">${tagsHtml}</div>
    </div>
    <div class="memory-section">
      <div class="memory-section-title">Structured Metadata</div>
      <div class="memory-meta-box">${metaHtml}</div>
    </div>
    <details class="memory-raw-details">
      <summary>View raw JSON</summary>
      <pre class="json">${esc(JSON.stringify(m,null,2))}</pre>
    </details>
  </div>`;
  const d=$('detail');
  if(!d.open)d.showModal();
}
function safeRich(html){const parsed=new DOMParser().parseFromString(String(html||''),'text/html');const allowed=new Set(['P','BR','H1','H2','H3','H4','BLOCKQUOTE','PRE','CODE','OL','UL','LI','STRONG','B','EM','I','U','S','DEL','SUB','SUP','SPAN','A','IMG','IFRAME']);function clean(node){if(node.nodeType===Node.TEXT_NODE)return document.createTextNode(node.textContent||'');if(node.nodeType!==Node.ELEMENT_NODE)return document.createDocumentFragment();const tag=node.tagName;if(!allowed.has(tag))return tag==='SCRIPT'||tag==='STYLE'||tag==='OBJECT'||tag==='EMBED'?document.createDocumentFragment():Array.from(node.childNodes).reduce((fragment,child)=>(fragment.append(clean(child)),fragment),document.createDocumentFragment());const out=document.createElement(tag.toLowerCase());const qlClasses=Array.from(node.classList||[]).filter(c=>/^ql-(align-(center|right|justify)|direction-rtl|size-(small|large|huge)|font-(serif|monospace)|indent-[1-8]|syntax|ui)$/.test(c));if(qlClasses.length)out.className=qlClasses.join(' ');if(tag==='LI'&&['ordered','bullet','checked','unchecked'].includes(node.getAttribute('data-list')))out.setAttribute('data-list',node.getAttribute('data-list'));if(tag==='A'){try{const u=new URL(node.getAttribute('href')||'',location.href);if(['http:','https:','mailto:'].includes(u.protocol)){out.href=u.href;out.target='_blank';out.rel='noopener noreferrer'}}catch(_){}}if(tag==='IMG'){const src=node.getAttribute('src')||'';if(/^https?:\/\//i.test(src)||/^data:image\/(png|jpeg|gif|webp);base64,/i.test(src)){out.src=src;out.alt=node.getAttribute('alt')||'';out.loading='lazy'}}if(tag==='IFRAME'){try{const u=new URL(node.getAttribute('src')||'');if(u.protocol==='https:'&&['youtube.com','www.youtube.com','youtube-nocookie.com','player.vimeo.com'].includes(u.hostname)){out.src=u.href;out.title=node.getAttribute('title')||'Embedded video';out.loading='lazy';out.setAttribute('allowfullscreen','')}}catch(_){}}if(node.hasAttribute('style')){const style=node.getAttribute('style')||'';const color=style.match(/(?:^|;)\s*color:\s*(#[0-9a-f]{3,8}|[a-z]+|rgb\([\d, %]+\))/i);const bg=style.match(/(?:^|;)\s*background-color:\s*(#[0-9a-f]{3,8}|[a-z]+|rgb\([\d, %]+\))/i);const align=style.match(/(?:^|;)\s*text-align:\s*(left|right|center|justify)/i);if(color)out.style.color=color[1];if(bg)out.style.backgroundColor=bg[1];if(align)out.style.textAlign=align[1]}for(const child of node.childNodes)out.append(clean(child));return out}const wrapper=document.createElement('div');for(const child of parsed.body.childNodes)wrapper.append(clean(child));return wrapper.innerHTML}
function initTaskEditor(){if(taskQuill)return;if(window.Quill){taskQuill=new Quill('#task-description-editor',{theme:'snow',placeholder:'Describe the work, acceptance criteria, and useful context…',modules:{toolbar:[[{font:[]}],[{size:['small',false,'large','huge']}],[{header:[1,2,3,4,false]}],['bold','italic','underline','strike','blockquote','code-block'],[{color:[]},{background:[]}],[{script:'sub'},{script:'super'}],[{list:'ordered'},{list:'bullet'},{list:'check'},{indent:'-1'},{indent:'+1'}],[{direction:'rtl'},{align:[]}],['link','image','video'],['clean']]}})}else{$('task-description-editor').contentEditable='true';$('task-description-editor').classList.add('fallback-editor')}}
function descriptionHtml(){return safeRich(taskQuill?taskQuill.root.innerHTML:$('task-description-editor').innerHTML)}
async function projectOptions(selected=''){const data=await api('/v1/projects?limit=100');$('task-project').innerHTML=data.items.map(p=>'<option value="'+esc(p.id)+'">'+esc(p.name)+'</option>').join('');if(selected)$('task-project').value=selected;await agentOptions($('task-project').value)}
async function agentOptions(projectId,selected=''){const data=await api('/v1/agents?limit=100'+(projectId?'&project_id='+encodeURIComponent(projectId):''));$('task-agent').innerHTML='<option value="">Unassigned</option>'+data.items.map(a=>'<option value="'+esc(a.id)+'">'+esc(a.name)+'</option>').join('');if(selected)$('task-agent').value=selected}
async function openTaskComposer(taskId=null){editingTaskId=taskId;taskFiles=[];$('task-project').disabled=!!taskId;$('task-upload-section').hidden=memberMode;$('task-files').disabled=memberMode;$('task-agent').closest('label').hidden=memberMode;$('task-form').reset();$('task-existing-files').replaceChildren();renderStagedFiles();$('task-editor').querySelector('.detail-head strong').textContent=taskId?'Edit task':'Create a task';$('task-submit').textContent=taskId?'Save task':'Create task';initTaskEditor();if(taskQuill)taskQuill.setText('');else $('task-description-editor').innerHTML='';let existing=null;if(taskId)existing=await api('/v1/tasks/'+taskId);await projectOptions(existing?.project_id||'');if(existing){if(!memberMode)$('task-existing-files').innerHTML=existing.attachments?.length?'<div class="attachment-list-label">Attached · '+existing.attachments.length+'</div>'+existing.attachments.map(a=>attachmentRow(a.name,a.size_bytes,`<button type="button" title="Download file" aria-label="Download file" onclick="downloadTaskFile('${esc(existing.id)}','${esc(a.id)}')">${icon('download')}</button>`)).join(''):'';$('task-title').value=existing.title;$('task-priority').value=existing.priority;await agentOptions(existing.project_id,existing.agent_id||'');if(taskQuill)taskQuill.clipboard.dangerouslyPasteHTML(safeRich(existing.description||''));else $('task-description-editor').innerHTML=safeRich(existing.description||'')}if(!$('task-editor').open)$('task-editor').showModal()}
function attachmentRow(name,size,action){return `<div class="attachment-row"><div class="attachment-file-icon">${icon('list')}</div><div class="attachment-file-copy"><strong>${esc(name)}</strong><small>${size<1024?size+' B':size<1048576?(size/1024).toFixed(1)+' KB':(size/1048576).toFixed(1)+' MB'}</small></div>${action}</div>`}
function queuedAttachments(files,removeHandler){return files.length?'<div class="attachment-list-label">Ready to upload · '+files.length+'</div>'+files.map((f,i)=>attachmentRow(f.webkitRelativePath||f.name,f.size,`<button type="button" title="Remove selected file" aria-label="Remove selected file" onclick="${removeHandler}(${i})">${icon('close')}</button>`)).join(''):'<p class="attachment-empty">No new files selected</p>'}
function renderStagedFiles(){$('task-file-list').innerHTML=queuedAttachments(taskFiles,'removeTaskFile')}
function appendUniqueFiles(queue,files){let skipped=0;for(const file of files){if(queue.some(x=>x.name===file.name&&x.size===file.size&&x.lastModified===file.lastModified))skipped++;else queue.push(file)}if(skipped)toast(skipped+' already-selected file(s) skipped')}
function stageTaskFiles(files){if(memberMode)return;appendUniqueFiles(taskFiles,files);renderStagedFiles()}
function removeTaskFile(index){taskFiles.splice(index,1);renderStagedFiles()}
async function saveTask(event){event.preventDefault();const button=$('task-submit');button.disabled=true;const wasEditing=!!editingTaskId;try{const payload={project_id:$('task-project').value,title:$('task-title').value.trim(),description:descriptionHtml(),priority:$('task-priority').value,agent_id:$('task-agent').value||null};if(editingTaskId)delete payload.project_id;if(memberMode)delete payload.agent_id;const task=editingTaskId?await api('/v1/tasks/'+editingTaskId,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}):await api('/v1/tasks',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});if(!memberMode&&taskFiles.length)await uploadFiles(task.id,taskFiles);taskFiles=[];$('task-editor').close();await load();await showTask(task.id);toast(wasEditing?'Task updated successfully':'Task created and queued for approval')}catch(e){toast('Could not save task: '+e.message,'error')}finally{button.disabled=false}}
function statusPill(status){return '<span class="pill '+esc(status)+'">'+esc(status)+'</span>'}
let hideClosed=true,taskMemberFilter='all',taskProjectFilter='all';
function taskFilter(name,value){if(name==='status')taskStatusFilter=value;else if(name==='priority')taskPriorityFilter=value;else if(name==='member')taskMemberFilter=value;else if(name==='project')taskProjectFilter=value;else hideClosed=value;cursor=null;cursors=[];load()}
function resetTaskFilters(){taskMemberFilter='all';taskProjectFilter='all';taskStatusFilter='all';taskPriorityFilter='all';hideClosed=true;$('q').value='';cursor=null;cursors=[];load()}
async function tasks(){
 const filters=new URLSearchParams({limit:'100',hide_closed:String(hideClosed)});
 if(cursor)filters.set('cursor',cursor);
 if($('q').value.trim())filters.set('q',$('q').value.trim());
 if(taskStatusFilter!=='all')filters.set('status',taskStatusFilter);
 if(taskPriorityFilter!=='all')filters.set('priority',taskPriorityFilter);
 if(taskProjectFilter!=='all')filters.set('project_id',taskProjectFilter);
 if(!memberMode&&taskMemberFilter!=='all')filters.set('creator_id',taskMemberFilter);
 const members=memberMode?{items:[]}:await api('/v1/members');
 const [data,projects,agents]=await Promise.all([api('/v1/tasks?'+filters),api('/v1/projects?limit=100'),api('/v1/agents?limit=100')]);
 const names=Object.fromEntries(projects.items.map(p=>[p.id,p.name]));
 const agentNames=Object.fromEntries(agents.items.map(a=>[a.id,a.name]));
 hasMore=data.has_more;window.nextCursor=data.next_cursor;
 const options=(values,current)=>values.map(v=>`<option value="${v}" ${current===v?'selected':''}>${v==='all'?'All':v[0].toUpperCase()+v.slice(1)}</option>`).join('');
 const rows=data.items.map(t=>`<tr class="task-row" data-task-id="${esc(t.id)}">
  <td class="task-title-cell"><button class="task-title-link" onclick="showTask('${esc(t.id)}')">${esc(t.title)}</button><div class="task-subline"><span>${esc(names[t.project_id]||'Project')}</span>${!t.approved?'<span class="review-label">Awaiting approval</span>':''}</div></td>
  ${memberMode?'':`<td>${statusPill(t.status)}</td>`}
  <td><span class="task-priority ${esc(t.priority)}"><span aria-hidden="true">●</span> ${esc(t.priority)}</span></td>
  ${memberMode?'':`<td><span class="task-assignee">${esc(agentNames[t.agent_id]||'Unassigned')}</span></td>`}
  <td class="task-date">${esc(new Date(t.updated_at).toLocaleDateString(undefined,{month:'short',day:'numeric'}))}<small>${esc(new Date(t.updated_at).toLocaleTimeString(undefined,{hour:'2-digit',minute:'2-digit'}))}</small></td>
 <td class="task-actions-cell">${taskActions(t,false,true)}</td>${memberMode?`<td class="member-status-edge">${memberStatusSelect(t)}</td>`:''}
 </tr>`).join('');
 $('app').innerHTML=`<section class="task-screen">
 <div class="task-heading"><div><span class="task-eyebrow">WORKSPACE / TASKS</span><h2>${memberMode?'My tasks':'Tasks'}</h2><p>${memberMode?'Follow your submissions from review to completion.':'Review requests, coordinate work, and track progress.'}</p></div><button class="primary task-create" onclick="openTaskComposer()"><span aria-hidden="true">＋</span> New task</button></div>
 <div class="task-panel"><div class="task-toolbar"><div class="task-filter-group"><label>Project<select onchange="taskFilter('project',this.value)"><option value="all">All projects</option>${projects.items.map(project=>`<option value="${esc(project.id)}" ${taskProjectFilter===project.id?'selected':''}>${esc(project.name)}</option>`).join('')}</select></label><label>Status<select onchange="taskFilter('status',this.value)">${options(['all','open','working','done','reopened','closed'],taskStatusFilter)}</select></label><label>Priority<select onchange="taskFilter('priority',this.value)">${options(['all','urgent','high','normal','low'],taskPriorityFilter)}</select></label>${memberMode?'':`<label>Created by<select onchange="taskFilter('member',this.value)"><option value="all">All creators</option>${[{id:'dev',name:'dev-key (Administrator)'},{id:'builtin-test',name:'test-key (Tester)'},...members.items].map(m=>`<option value="${esc(m.id)}" ${taskMemberFilter===m.id?'selected':''}>${esc(m.name)}</option>`).join('')}</select></label>`}</div><label class="task-toggle"><input type="checkbox" ${hideClosed?'checked':''} onchange="taskFilter('closed',this.checked)">Hide closed</label></div>
 <div class="task-results-line"><span>${data.items.length} task${data.items.length===1?'':'s'} on this page</span><button onclick="resetTaskFilters()">Reset filters</button></div>
 <div class="table task-table">${rows?`<table><thead><tr><th>Task / project</th>${memberMode?'':'<th>Status</th>'}<th>Priority</th>${memberMode?'':'<th>Assigned to</th>'}<th>Updated</th><th class="task-actions-cell">Actions</th>${memberMode?'<th class="member-status-edge">Status</th>':''}</tr></thead><tbody>${rows}</tbody></table>`:`<div class="task-empty"><div aria-hidden="true">✓</div><h3>No tasks to show</h3><p>Create a task to get started, or adjust your filters to find existing work.</p><button class="primary" onclick="openTaskComposer()">Create a task</button></div>`}</div><div class="task-footer">${pager()}</div></div></section>`;
}
async function editOwnTask(id){try{await openTaskComposer(id);if($('detail').open)$('detail').close()}catch(e){alert('Could not open task: '+e.message)}}
function memberStatusSelect(task){const allowed=['open','closed','reopened'];const values=allowed.includes(task.status)?allowed:[task.status,...allowed];return `<select class="member-status-select" data-current="${esc(task.status)}" aria-label="Task status" onchange="setMemberTaskStatus('${esc(task.id)}',this)">${values.map(status=>`<option value="${esc(status)}" ${status===task.status?'selected':''} ${allowed.includes(status)?'':'disabled'}>${esc(status[0].toUpperCase()+status.slice(1))}</option>`).join('')}</select>`}
function taskActions(task,includeStatus=true,compact=false){
 const action=(label,glyph,handler,danger=false,disabled=false)=>`<button type="button" class="${danger?'task-delete ':''}${compact?'task-icon-action':''}" title="${label}" aria-label="${label}" ${disabled?'disabled':''} onclick="${handler}">${compact?icon(glyph):label}</button>`;
 const id=esc(task.id);
 return `<div class="task-action-group">${compact&&!memberMode?action('Map instructions','list',`openTaskInstructions('${id}')`):''}${compact&&!memberMode&&!task.approved?action('Approve task','check',`approveTask('${id}')`):''}${memberMode?action('Edit task','edit',`editOwnTask('${id}')`):action('Close task','close',`closeTask('${id}',this)`,false,task.status==='closed')}${action('Delete task','trash',`deleteTask('${id}',this)`,true)}${memberMode&&includeStatus?memberStatusSelect(task):''}</div>`;
}
// Keep row navigation separate from inline buttons and status controls.
function openTaskRow(event){
 const row=event.target.closest('.task-row');
 if(!row||event.target.closest('button,a,input,select,textarea,label'))return;
 if(window.getSelection()?.toString())return;
 showTask(row.dataset.taskId);
}
$('app').addEventListener('click',openTaskRow);

async function setMemberTaskStatus(id,select){const previous=select.dataset.current;if(select.value===previous)return;select.disabled=true;try{const task=await api('/v1/tasks/'+id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:select.value})});select.dataset.current=task.status;select.value=task.status;if($('detail').open)await showTask(id);await load()}catch(e){select.value=select.dataset.current;alert(e.message)}finally{select.disabled=false}}
async function closeTask(id,button){button.disabled=true;try{await api('/v1/tasks/'+id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:'closed'})});if($('detail').open)await showTask(id);await load()}catch(e){alert('Could not close task: '+e.message)}finally{button.disabled=false}}
async function deleteTask(id,button){if(!confirm('Permanently delete this task, its updates and attached files? This cannot be undone.'))return;button.disabled=true;try{await api('/v1/tasks/'+id,{method:'DELETE'});if($('detail').open)$('detail').close();await load()}catch(e){alert('Could not delete task: '+e.message)}finally{button.disabled=false}}
function setTaskHeaderActions(task){
 const group=$('detail-task-actions');group.replaceChildren();
 const close=document.createElement('button');close.type='button';close.innerHTML=icon('close');close.className='detail-icon-action';close.title='Close task';close.setAttribute('aria-label','Close task');close.disabled=task.status==='closed';close.onclick=()=>closeTask(task.id,close);
 const remove=document.createElement('button');remove.type='button';remove.innerHTML=icon('trash');remove.title='Delete task';remove.setAttribute('aria-label','Delete task');remove.className='task-delete detail-icon-action';remove.onclick=()=>deleteTask(task.id,remove);
 group.append(close,remove);
 const approve=$('detail-approve');approve.innerHTML=icon('check');approve.classList.add('detail-icon-action');approve.title='Approve task';approve.setAttribute('aria-label','Approve task');
}

function isDetailBackdrop(event){
 const dialog=$('detail');
 if(event.target!==dialog||!dialog.querySelector('.task-detail-view'))return false;
 const rect=dialog.getBoundingClientRect();
 return event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom;
}
let detailBackdropPressed=false;
$('detail').addEventListener('pointerdown',event=>{detailBackdropPressed=isDetailBackdrop(event)});
$('detail').addEventListener('pointercancel',()=>{detailBackdropPressed=false});
$('detail').addEventListener('click',event=>{
 const dismiss=detailBackdropPressed&&isDetailBackdrop(event);detailBackdropPressed=false;
 if(dismiss)$('detail').close();
});
$('detail').addEventListener('close',()=>{detailBackdropPressed=false});
const taskEditorDialog=$('task-editor');let editorBackdropPressed=false;
function isEditorBackdrop(event){if(event.target!==taskEditorDialog)return false;const rect=taskEditorDialog.getBoundingClientRect();return event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom}
taskEditorDialog.addEventListener('pointerdown',event=>{editorBackdropPressed=isEditorBackdrop(event)});
taskEditorDialog.addEventListener('pointercancel',()=>{editorBackdropPressed=false});
taskEditorDialog.addEventListener('click',event=>{const dismiss=editorBackdropPressed&&isEditorBackdrop(event);editorBackdropPressed=false;if(dismiss)taskEditorDialog.close()});
taskEditorDialog.addEventListener('close',()=>{editorBackdropPressed=false});
function taskDetailActions(task){if(!memberMode)return '';const holder=document.createElement('div');holder.innerHTML=taskActions(task);holder.querySelector('.task-delete')?.remove();return holder.innerHTML}
function taskDetailSummary(task,projectName,agentName){
 const field=(label,value)=>`<div><dt>${label}</dt><dd>${value}</dd></div>`;
 return `<div class="task-detail-intro"><span class="task-detail-kicker">TASK DETAILS</span><span class="status-chip">${task.approved?'Approved':'Awaiting approval'}</span></div><dl class="task-detail-meta">${field('Status',statusPill(task.status))}${field('Priority',esc(task.priority))}${projectName?field('Project',esc(projectName)):''}${agentName?field('Assigned to',esc(agentName)):''}</dl>`;
}
function taskDetailDates(task){return `<footer class="task-detail-dates"><span>Created ${esc(new Date(task.created_at).toLocaleString())}</span><span>Updated ${esc(new Date(task.updated_at).toLocaleString())}</span>${task.completed_at?`<span>Completed ${esc(new Date(task.completed_at).toLocaleString())}</span>`:''}</footer>`}
async function showTask(taskId){
 $('detail-approve').hidden=true;$('detail-task-actions').replaceChildren();
 if(memberMode){
  const task=await api('/v1/tasks/'+taskId);$('detail-title').textContent=task.title;setTaskHeaderActions(task);
  $('detail-body').innerHTML=`<div class="task-detail-view">${taskDetailSummary(task)}<section class="task-detail-section"><div class="task-section-heading"><h3>Manage task</h3></div>${taskDetailActions(task)}</section><section class="task-detail-section ql-snow"><div class="task-section-heading"><h3>Description</h3></div><div class="task-description ql-editor">${safeRich(task.description||'<p class="muted">No description added yet.</p>')}</div></section>${taskInstructionSection(task)}${taskDetailDates(task)}</div>`;
  if(!$('detail').open)$('detail').showModal();return;
 }
 const [task,events,projects,agents,sessions]=await Promise.all([api('/v1/tasks/'+taskId),api('/v1/tasks/'+taskId+'/events?limit=100'),api('/v1/projects?limit=100'),api('/v1/agents?limit=100'),api('/v1/tasks/'+taskId+'/sessions?limit=20')]);
 const id=esc(task.id),agentNames=Object.fromEntries(agents.items.map(a=>[a.id,a.name])),project=projects.items.find(p=>p.id===task.project_id);
 $('detail-title').textContent=task.title;setTaskHeaderActions(task);$('detail-approve').hidden=!!task.approved;$('detail-approve').onclick=()=>approveTask(task.id);
 const options=(values,current)=>values.map(value=>`<option value="${esc(value)}" ${value===current?'selected':''}>${esc(value[0].toUpperCase()+value.slice(1))}</option>`).join('');
 const attachments=task.attachments||[];
 const attachmentHtml=attachments.map(a=>`<article class="task-file"><div class="task-file-copy"><strong>${esc(a.name)}</strong><small class="muted">${(a.size_bytes/1024).toFixed(1)} KB</small><details class="task-file-paths"><summary>File locations</summary><div class="path">Source: ${esc(a.source_path||a.name)}</div><div class="path">Server: ${esc(a.path)}</div></details></div><button title="Download file" aria-label="Download ${esc(a.name)}" onclick="downloadTaskFile('${id}','${esc(a.id)}')">${icon('download')}</button></article>`).join('')||'<p class="task-detail-empty">No files attached yet.</p>';
 const eventHtml=events.items.map(e=>`<article class="event"><div class="task-event-heading"><strong>${esc(e.action.replaceAll('_',' '))}${e.actor_agent_id?' · '+esc(agentNames[e.actor_agent_id]||'Agent'):''}</strong><time>${esc(new Date(e.created_at).toLocaleString())}</time></div><div class="task-event-note">${esc(e.note||((e.from_status||'')+' → '+(e.to_status||'')))}</div></article>`).join('')||'<p class="task-detail-empty">No updates yet. Add a note to keep the team informed.</p>';
 const sessionOptions=sessions.items.map(s=>`<option value="${esc(s.id)}">${esc(s.title||s.task||s.id)} · ${esc(s.status)}</option>`).join('');
 $('detail-body').innerHTML=`<div class="task-detail-view">
 ${taskDetailSummary(task,project?.name||task.project_id,agentNames[task.agent_id]||'Unassigned')}
 <section class="task-detail-section ql-snow"><div class="task-section-heading"><h3>Description</h3><button title="Edit task" aria-label="Edit task" onclick="openTaskComposer('${id}');$('detail').close()">${icon('edit')}</button></div><div class="task-body task-description ql-editor">${safeRich(task.description||'<p class="muted">No description added yet.</p>')}</div></section>
 <section class="task-detail-section"><div class="task-section-heading"><h3>Progress</h3><span>Manage status and ownership</span></div><div class="task-progress-fields"><label>Status<select id="task-status">${options(['open','working','done','reopened','closed'],task.status)}</select></label><label>Priority<select id="task-detail-priority">${options(['urgent','high','normal','low'],task.priority)}</select></label><label>Assigned agent<select id="task-detail-agent"><option value="">Unassigned</option>${agents.items.map(a=>`<option value="${esc(a.id)}" ${task.agent_id===a.id?'selected':''}>${esc(a.name)}</option>`).join('')}</select></label></div><div class="task-section-actions"><button class="primary" onclick="saveTaskProgress('${id}')">Save changes</button></div></section>
 <section class="task-detail-section"><div class="task-section-heading"><h3>Attachments</h3><span>${attachments.length} file${attachments.length===1?'':'s'}</span></div><div class="task-attachments">${attachmentHtml}</div><div class="drop-zone" id="detail-drop" tabindex="0">Drop files here or <button onclick="$('detail-files').click()">Browse files</button><input id="detail-files" type="file" multiple hidden></div><div id="detail-file-list"></div><div class="task-section-actions"><button id="detail-upload-button" disabled onclick="uploadDetailFiles('${id}')">Upload files</button></div></section>
 <section class="task-detail-section"><div class="task-section-heading"><h3>Activity</h3><span>${events.items.length} update${events.items.length===1?'':'s'}</span></div><div class="task-activity">${eventHtml}</div><div class="task-note-form"><label for="task-note">Add a team update</label><textarea id="task-note" rows="3" placeholder="Share progress, decisions, or blockers…"></textarea><div class="task-section-actions"><button class="primary" onclick="addTaskNote('${id}')">Post update</button></div></div></section>
 <section class="task-detail-section task-console"><div class="task-section-heading"><div><h3>Agent console</h3><span>Discuss with the CLI agent in a task-linked session</span></div><button onclick="createTaskConsoleSession('${id}')">New session</button></div><div class="task-console-toolbar"><select id="console-session" onchange="loadTaskConsole('${id}')"><option value="">Select a session</option>${sessionOptions}</select><span id="console-state" class="muted" role="status">Select a session</span><button class="primary" ${task.approved?'':'disabled'} onclick="runTaskAgent('${id}')">Run CLI agent</button></div><div id="console-events" class="console-events"><p class="task-detail-empty">Select or create a session to view its updates.</p></div><div class="console-composer"><textarea id="console-message" rows="3" placeholder="Send an update or instruction to this session…"></textarea><div class="console-actions"><button class="primary" onclick="sendConsoleMessage('${id}')">Send message</button></div></div></section>
 ${taskInstructionSection(task)}${taskDetailDates(task)}</div>`;
 if(!$('detail').open)$('detail').showModal();wireDetailDrop(task.id);if(sessions.items[0]&&$('console-session')){$('console-session').value=sessions.items[0].id;loadTaskConsole(task.id)}
}
let activeTaskId=null,checklistSaving=false;const renderTaskDetail=showTask;showTask=async function(taskId){activeTaskId=taskId;return renderTaskDetail(taskId)};$('detail-body').addEventListener('click',async event=>{const item=event.target.closest('.task-body li[data-list="checked"],.task-body li[data-list="unchecked"]');if(!item||!activeTaskId||checklistSaving)return;const previous=item.dataset.list;const next=previous==='checked'?'unchecked':'checked';item.dataset.list=next;item.setAttribute('aria-checked',String(next==='checked'));checklistSaving=true;try{const body=item.closest('.task-body');await api('/v1/tasks/'+activeTaskId,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({description:safeRich(body.innerHTML)})});toast(next==='checked'?'Checklist item completed':'Checklist item reopened')}catch(error){item.dataset.list=previous;item.setAttribute('aria-checked',String(previous==='checked'));toast('Could not update checklist: '+error.message,'error')}finally{checklistSaving=false}});$('detail-body').addEventListener('keydown',event=>{if((event.key==='Enter'||event.key===' ')&&event.target.matches('.task-body li[data-list="checked"],.task-body li[data-list="unchecked"]')){event.preventDefault();event.target.click()}});new MutationObserver(()=>{$('detail-body').querySelectorAll('.task-body li[data-list="checked"],.task-body li[data-list="unchecked"]').forEach(item=>{item.tabIndex=0;item.setAttribute('role','checkbox');item.setAttribute('aria-checked',String(item.dataset.list==='checked'));item.title='Click to mark '+(item.dataset.list==='checked'?'incomplete':'complete')})}).observe($('detail-body'),{childList:true,subtree:true});
function memberTable(items){return items.length?'<div class="table member-table"><table><thead><tr><th>Name</th><th class="member-actions">Actions</th></tr></thead><tbody>'+items.map(m=>`<tr><td>${esc(m.name)}</td><td class="member-actions"><button type="button" class="task-delete" title="Remove member" aria-label="Remove ${esc(m.name)}" onclick="deleteMember('${esc(m.id)}',this)">${icon('trash')}</button></td></tr>`).join('')+'</tbody></table></div>':'<p class="attachment-empty">No members added yet.</p>'}
async function deleteMember(id,button){if(!confirm('Remove this member? Their API key will stop working. Existing tasks will be kept.'))return;button.disabled=true;try{await api('/v1/members/'+id,{method:'DELETE'});await membersView();toast('Member removed')}catch(e){toast('Could not remove member: '+e.message,'error')}finally{button.disabled=false}}
async function instructionsView(){
 const params=new URLSearchParams({limit:'25'});if(cursor)params.set('cursor',cursor);if($('q').value.trim())params.set('q',$('q').value.trim());
 const data=await api('/v1/instructions?'+params);hasMore=data.has_more;window.nextCursor=data.next_cursor;
 $('app').innerHTML=`<header class="page-hero"><div><span class="page-kicker">INSTRUCTIONS</span><h1>Instructions</h1><p>Manage reusable guidance and map it to tasks.</p></div></header><section class="record-panel"><div class="record-toolbar"><strong>Instruction library</strong><span class="record-count">${data.items.length} records</span></div><div class="table instruction-table"><table><thead><tr><th>Title</th><th>Scope</th><th>Priority</th><th>Status</th><th>Actions</th></tr></thead><tbody>${data.items.map(item=>`<tr data-instruction-id="${esc(item.id)}"><td><button class="instruction-title" onclick="showInstruction('${esc(item.id)}')">${esc(item.title)}</button></td><td>${esc(item.scope)}</td><td>${esc(item.priority)}</td><td>${esc(item.status)}</td><td><div class="task-action-group"><button title="Edit instruction" aria-label="Edit instruction" onclick="editInstruction('${esc(item.id)}')">${icon('edit')}</button><button class="task-delete" title="Delete instruction" aria-label="Delete instruction" onclick="deleteInstruction('${esc(item.id)}',this)">${icon('trash')}</button></div></td></tr>`).join('')}</tbody></table></div>${data.items.length?'':'<p class="attachment-empty">No instructions found.</p>'}${pager()}</section>`;
 document.querySelectorAll('[data-instruction-id]').forEach(row=>row.onclick=event=>{if(!event.target.closest('button,a,input,select'))showInstruction(row.dataset.instructionId)});
}
async function showInstruction(id){const item=await api('/v1/instructions/'+id);showDetail(item.title,item);$('detail-body').innerHTML=`<div class="task-action-group"><button onclick="editInstruction('${esc(id)}')">${icon('edit')} Edit</button><button class="task-delete" onclick="deleteInstruction('${esc(id)}',this)">${icon('trash')} Delete</button></div><p class="muted">${esc(item.scope)} · ${esc(item.status)} · Priority ${esc(item.priority)}</p><div class="instruction-content">${esc(item.content)}</div>`;}
async function editInstruction(id){
 const item=await api('/v1/instructions/'+id);const dialog=ensureManualDialog();$('manual-title').textContent='Edit instruction';$('manual-submit').textContent='Save changes';
 $('manual-form').innerHTML=`<p class="muted">${esc(item.scope)} instruction · ${esc(item.status)}</p><label>Title<input id="instruction-title" required maxlength="500" value="${esc(item.title)}"></label><label>Content<textarea id="instruction-content" rows="8" required>${esc(item.content)}</textarea></label><label>Priority<input id="instruction-priority" type="number" min="0" max="100" required value="${esc(item.priority)}"></label><label>Status<select id="instruction-status"><option value="draft" ${item.status==='draft'?'selected':''}>Draft</option><option value="approved" ${item.status==='approved'?'selected':''}>Approved</option><option value="revoked" ${item.status==='revoked'?'selected':''}>Revoked</option></select></label><label>Tags<input id="instruction-tags" value="${esc((item.tags||[]).join(', '))}" placeholder="Comma separated"></label>`;
 $('manual-form').onsubmit=async event=>{event.preventDefault();const button=$('manual-submit');button.disabled=true;try{await api('/v1/instructions/'+id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:$('instruction-title').value.trim(),content:$('instruction-content').value.trim(),priority:Number($('instruction-priority').value),status:$('instruction-status').value,tags:$('instruction-tags').value.split(',').map(x=>x.trim()).filter(Boolean)})});dialog.close();if($('detail').open)$('detail').close();await load();toast('Instruction updated')}catch(e){toast(e.message,'error')}finally{button.disabled=false}};
 if(!dialog.open)dialog.showModal();
}
async function deleteInstruction(id,button){if(!confirm('Delete this instruction? It will also be removed from mapped tasks.'))return;button.disabled=true;try{await api('/v1/instructions/'+id,{method:'DELETE'});if($('detail').open)$('detail').close();await load();toast('Instruction deleted')}catch(e){toast(e.message,'error')}finally{button.disabled=false}}
function taskInstructionSection(task){return `<section class="task-detail-section"><div class="task-section-heading"><h3>Instructions</h3>${memberMode?'':`<button title="Map instructions" aria-label="Map instructions" onclick="openTaskInstructions('${esc(task.id)}')">${icon('list')}</button>`}</div>${task.instructions?.length?task.instructions.map(item=>`<details class="mapped-instruction"><summary>${esc(item.title)} <small>${esc(item.status)}</small></summary><div class="instruction-content">${esc(item.content)}</div></details>`).join(''):'<p class="task-detail-empty">No instructions mapped.</p>'}</section>`}
async function openTaskInstructions(id){
 if(memberMode)return;
 try{
  const task=await api('/v1/tasks/'+id);let items=[],next=null;do{const page=await api('/v1/instructions?limit=100'+(next?'&cursor='+encodeURIComponent(next):''));items.push(...page.items.filter(item=>item.status==='approved'));next=page.has_more?page.next_cursor:null;}while(next);
  let dialog=$('task-instruction-dialog');if(!dialog){dialog=document.createElement('dialog');dialog.id='task-instruction-dialog';dialog.className='detail';document.body.append(dialog)}
  dialog.innerHTML=`<div class="detail-head"><strong>Map instructions</strong><button onclick="$('task-instruction-dialog').close()">Back</button></div><form id="task-instruction-form" class="detail-body"><p class="muted">Select guidance for <strong>${esc(task.title)}</strong>.</p><div class="instruction-options">${items.length?items.map(item=>`<label class="instruction-option"><input type="checkbox" name="instruction" value="${esc(item.id)}" ${(task.instruction_ids||[]).includes(item.id)?'checked':''}><span><strong>${esc(item.title)}</strong><small>${esc(item.scope)} · ${esc(item.status)}</small></span></label>`).join(''):'<p>No instructions available. Create one in Instructions first.</p>'}</div><div class="task-section-actions"><button id="save-task-instructions" class="primary" type="submit">Save mapping</button></div></form>`;
  $('task-instruction-form').onsubmit=async event=>{event.preventDefault();const button=$('save-task-instructions');button.disabled=true;try{const instruction_ids=Array.from(dialog.querySelectorAll('input[name="instruction"]:checked'),input=>input.value);await api('/v1/tasks/'+id+'/instructions',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({instruction_ids})});dialog.close();if($('detail').open)await showTask(id);await load();toast('Task instructions updated')}catch(e){toast(e.message,'error')}finally{button.disabled=false}};
  if(!dialog.open)dialog.showModal();
 }catch(e){toast('Could not load instructions: '+e.message,'error')}
}
async function membersView(){const data=await api('/v1/members');if($('member-name')){const list=$('member-list');if(list)list.innerHTML=memberTable(data.items);if($('member-count'))$('member-count').textContent=data.items.length+' active';return;}$('app').innerHTML='<header class="page-hero"><div class="page-hero-copy"><span class="page-kicker">ACCESS CONTROL</span><h1>Members</h1><p>Issue scoped workspace credentials and review who can submit and manage tasks.</p></div></header><div class="members-layout"><section class="form-card"><h2>Add a member</h2><p>Create a named workspace identity with a private API key of at least 16 characters.</p><form onsubmit="createMember(event)"><label>Member name<input id="member-name" required placeholder="e.g. Platform operations"></label><label>API key <span class="required-mark">Required</span><input id="member-key" type="password" required minlength="16" autocomplete="new-password" placeholder="Minimum 16 characters"></label><button class="primary" type="submit">＋ Add member</button></form><div id="member-result"></div></section><section class="members-card"><div class="row"><h2>Workspace members</h2><span id="member-count" class="record-count">'+data.items.length+' active</span></div><div id="member-list">'+memberTable(data.items)+'</div></section></div>'}
async function createMember(event){event.preventDefault();try{const member=await api('/v1/members',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:$('member-name').value,api_key:$('member-key').value||null})});$('member-key').value='';$('member-result').className='credential-result';$('member-result').innerHTML='<strong>Copy this key now</strong><br><span>'+esc(member.api_key)+'</span><br><small>It will not be shown again.</small>';toast('Member added successfully')}catch(e){toast(e.message,'error')}}
async function approveTask(id){const task=await api('/v1/tasks/'+id);if(task.approved||memberMode){$('detail-approve').hidden=true;if($('approval-dialog').open)$('approval-dialog').close();return;}$('approval-summary').innerHTML='<strong>'+esc(task.title)+'</strong><span class="muted">Priority: '+esc(task.priority)+' · Assigned: '+esc(task.agent_id||'Unassigned')+'</span>';$('approval-note').value='';$('approval-confirm').onclick=()=>confirmTaskApproval(id);$('approval-dialog').showModal()}
async function confirmTaskApproval(id){const button=$('approval-confirm');button.disabled=true;try{const current=await api('/v1/tasks/'+id);if(current.approved||memberMode){$('approval-dialog').close();await showTask(id);return;}await api('/v1/tasks/'+id+'/approve',{method:'POST'});$('approval-dialog').close();await showTask(id);await load();toast('Task approved and agent authorized')}catch(e){toast('Could not approve task: '+e.message,'error')}finally{button.disabled=false}}
async function saveTaskProgress(id){try{await api('/v1/tasks/'+id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:$('task-status').value,priority:$('task-detail-priority').value,agent_id:$('task-detail-agent').value||null})});await load();await showTask(id);toast('Task progress saved')}catch(e){toast('Could not update task: '+e.message,'error')}}
async function addTaskNote(id){const note=$('task-note').value.trim();if(!note)return;try{await api('/v1/tasks/'+id+'/events',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({note})});await showTask(id);toast('Team update posted')}catch(e){toast('Could not post update: '+e.message,'error')}}
async function createTaskConsoleSession(taskId){try{const session=await api('/v1/tasks/'+taskId+'/sessions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({})});await showTask(taskId);if($('console-session')){$('console-session').value=session.id;await loadTaskConsole(taskId)}toast('Console session created')}catch(e){toast('Could not create session: '+e.message,'error')}}
let consolePollTimer=null;
function stopConsolePolling(){if(consolePollTimer){clearTimeout(consolePollTimer);consolePollTimer=null}}
function consoleStateLabel(session){const state=session?.metadata?.agent_state||((session?.status==='active')?'online':'offline');return state==='typing'?'● typing…':state==='online'?'● online':'○ offline'}
async function refreshTaskConsole(taskId){const sessionId=$('console-session')?.value;const target=$('console-events');if(!target||!sessionId){stopConsolePolling();if(target)target.innerHTML='<p class="task-detail-empty">Select or create a session to view its updates.</p>';if($('console-state'))$('console-state').textContent='Select a session';return}try{const [session,events]=await Promise.all([api('/v1/sessions/'+sessionId),api('/v1/sessions/'+sessionId+'/events?limit=100&order=asc')]);const state=session.metadata?.agent_state||((session.status==='active')?'online':'offline');if($('console-state'))$('console-state').textContent=consoleStateLabel(session)+(state==='typing'?' The agent is processing your message.':'');target.innerHTML=events.items.length?events.items.map(e=>`<article class="console-event"><div class="console-event-head"><strong>${esc(e.role)} · ${esc(e.kind)}</strong><time>${esc(new Date(e.created_at||Date.now()).toLocaleString())}</time></div><div class="console-event-content">${esc(e.content)}</div></article>`).join(''):'<p class="task-detail-empty">No session updates yet.</p>';target.scrollTop=target.scrollHeight;stopConsolePolling();if(state==='typing'||session.status==='active')consolePollTimer=setTimeout(()=>refreshTaskConsole(taskId),1500)}catch(e){target.innerHTML='<p class="task-detail-empty">Could not load session updates: '+esc(e.message)+'</p>';stopConsolePolling()}}
async function loadTaskConsole(taskId){return refreshTaskConsole(taskId)}
async function sendConsoleMessage(taskId){const sessionId=$('console-session')?.value;const input=$('console-message');const message=input?.value.trim();if(!sessionId){toast('Select a console session first','error');return}if(!message)return;try{const session=await api('/v1/sessions/'+sessionId);if(session.metadata?.agent_state==='typing'){toast('The agent is still responding; your message is saved for the next run','error')}await api('/v1/sessions/'+sessionId+'/events',{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':crypto.randomUUID()},body:JSON.stringify({role:'user',kind:'message',content:message,metadata:{task_id:taskId}})});input.value='';if(session.metadata?.agent_state!=='typing')await runTaskAgent(taskId);await refreshTaskConsole(taskId);toast('Message sent')}catch(e){toast('Could not send message: '+e.message,'error')}}
async function runTaskAgent(taskId){let sessionId=$('console-session')?.value;if(!sessionId){await createTaskConsoleSession(taskId);sessionId=$('console-session')?.value}if(!sessionId)return;try{await api('/v1/tasks/'+taskId+'/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:sessionId})});await refreshTaskConsole(taskId);toast('CLI agent started')}catch(e){toast('Could not start CLI agent: '+e.message,'error')}}
async function downloadTaskFile(taskId,fileId){try{const response=await fetch('/v1/tasks/'+taskId+'/attachments/'+fileId+'/download',{headers:{'X-API-Key':key()}});if(!response.ok)throw Error('Download failed');const blob=await response.blob();const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='attachment';link.click();URL.revokeObjectURL(link.href)}catch(e){alert(e.message)}}
async function uploadFiles(taskId,files){if(memberMode)throw new Error('Only the dev-key administrator can attach files');if(!files.length)return;const form=new FormData();for(const file of files){form.append('files',file,file.name);form.append('source_paths',file.webkitRelativePath||file.name)}const result=await api('/v1/tasks/'+taskId+'/attachments',{method:'POST',body:form});if(result.skipped_duplicates?.length)toast(result.skipped_duplicates.length+' duplicate file(s) skipped');return result}
async function uploadDetailFiles(taskId){const button=$('detail-upload-button');if(button.disabled||!detailFiles.length)return;button.disabled=true;try{await uploadFiles(taskId,detailFiles);detailFiles=[];await showTask(taskId)}catch(e){alert('Could not upload files: '+e.message)}finally{if($('detail-upload-button'))$('detail-upload-button').disabled=!detailFiles.length}}
function renderDetailFiles(){$('detail-file-list').innerHTML=queuedAttachments(detailFiles,'removeDetailFile');$('detail-upload-button').disabled=!detailFiles.length}
function removeDetailFile(index){detailFiles.splice(index,1);renderDetailFiles()}
function wireDetailDrop(taskId){const zone=$('detail-drop');if(!zone)return;const input=$('detail-files');detailFiles=[];renderDetailFiles();const stage=files=>{if(memberMode)return;appendUniqueFiles(detailFiles,files);renderDetailFiles()};zone.ondragover=e=>{e.preventDefault();zone.classList.add('dragging')};zone.ondragleave=()=>zone.classList.remove('dragging');zone.ondrop=e=>{e.preventDefault();zone.classList.remove('dragging');stage(e.dataTransfer.files)};input.onchange=()=>{stage(input.files);input.value=''}}
function goToTab(name){document.querySelector('[data-tab="'+name+'"]')?.click()}
async function overview(){let [p,m,a,s,stats,tasksData]=await Promise.all([api('/v1/projects?limit=100'),api('/v1/memories?limit=100'),api('/v1/agents?limit=100'),api('/v1/sessions?limit=100'),api('/v1/stats'),api('/v1/tasks?limit=100')]);const taskCounts={open:0,working:0,done:0,reopened:0,closed:0};tasksData.items.forEach(task=>taskCounts[task.status]=(taskCounts[task.status]||0)+1);const activeTasks=taskCounts.open+taskCounts.working+taskCounts.reopened;const completed=taskCounts.done+taskCounts.closed;const completion=tasksData.items.length?Math.round(completed/tasksData.items.length*100):0;const memoryTypes={};m.items.forEach(memory=>memoryTypes[memory.type]=(memoryTypes[memory.type]||0)+1);const topTypes=Object.entries(memoryTypes).sort((x,y)=>y[1]-x[1]).slice(0,4);const maxType=Math.max(1,...topTypes.map(x=>x[1]));const primary=[['Projects',p.items.length,'Active workspaces','folder','projects'],['Active tasks',activeTasks,tasksData.items.length+' total tasks','check','tasks'],['Memories',stats.memories,'Indexed knowledge','database','memories'],['Agents',a.items.length,a.items.filter(x=>x.status==='active').length+' active','user','agents']];$('app').innerHTML='<header class="overview-header overview-hero"><div><span class="page-kicker">OPERATIONS DASHBOARD</span><h1>Workspace overview</h1><p>Live visibility into work, knowledge, agents, and system activity.</p></div><div class="overview-hero-actions"><button onclick="goToTab(\'tasks\')">View tasks</button><button class="primary" onclick="openTaskComposer()">New task</button></div></header><section class="overview-kpis">'+primary.map(item=>'<button class="overview-kpi" onclick="goToTab(\''+item[4]+'\')"><span class="metric-icon">'+icon(item[3])+'</span><span class="overview-kpi-copy"><small>'+item[0]+'</small><strong>'+item[1]+'</strong><em>'+item[2]+'</em></span><span class="overview-kpi-arrow">›</span></button>').join('')+'</section><section class="overview-dashboard-grid"><article class="dashboard-panel work-panel"><header><div><h2>Task workload</h2><p>Current distribution across the work queue.</p></div><strong>'+completion+'% complete</strong></header><div class="completion-track"><span style="width:'+completion+'%"></span></div><div class="workload-list">'+[['Open',taskCounts.open],['Working',taskCounts.working],['Done',taskCounts.done],['Reopened',taskCounts.reopened],['Closed',taskCounts.closed]].map(item=>'<div><span><i></i>'+item[0]+'</span><strong>'+item[1]+'</strong></div>').join('')+'</div><button class="panel-link" onclick="goToTab(\'tasks\')">Open task workspace <span>→</span></button></article><article class="dashboard-panel memory-panel"><header><div><h2>Memory composition</h2><p>Most common memory types in the current index.</p></div><strong>'+stats.memories+' total</strong></header><div class="memory-mix">'+(topTypes.length?topTypes.map(item=>'<div><div><span>'+esc(item[0])+'</span><strong>'+item[1]+'</strong></div><div class="mix-track"><span style="width:'+(item[1]/maxType*100)+'%"></span></div></div>').join(''):'<div class="empty-compact">No memories indexed yet.</div>')+'</div><button class="panel-link" onclick="goToTab(\'memories\')">Browse memory index <span>→</span></button></article><article class="dashboard-panel inventory-panel"><header><div><h2>System inventory</h2><p>Stored operational resources.</p></div></header><div class="inventory-grid">'+[['Sessions',stats.sessions],['Events',stats.events],['Instructions',stats.instructions],['Database',(stats.storage_bytes/1024).toFixed(1)+' KB']].map(item=>'<div><span>'+item[0]+'</span><strong>'+item[1]+'</strong></div>').join('')+'</div><div class="system-row"><span class="system-dot"></span><div><strong>System healthy</strong><small>API and memory database responding</small></div></div></article></section><section class="record-panel overview-recent"><div class="record-toolbar"><div><strong>Recent memories</strong><p>Latest knowledge added to the workspace.</p></div><div class="overview-table-actions"><span class="record-count">'+Math.min(m.items.length,8)+' records</span><button onclick="goToTab(\'memories\')">View all</button></div></div>'+table(m.items.slice(0,8),[['Title','title'],['Type','type'],['Scope','scope'],['Importance','importance'],['Status','status'],['Created',i=>new Date(i.created_at).toLocaleString()]])+'</section>';document.querySelectorAll('#app tbody tr').forEach((tr,n)=>tr.onclick=()=>showMemory(m.items[n]));removeLegacyGlyphs();decorateIcons()}
async function records(){if(tab==='tasks')return tasks();if(tab==='instructions')return instructionsView();const meta={projects:['PROJECT REGISTRY','Projects','Organize memory, agents, and work into governed operational spaces.'],memories:['KNOWLEDGE INDEX','Memories','Inspect semantic knowledge, episodic records, and retained agent context.'],agents:['AGENT FLEET','Agents','Monitor connected models, project access, and execution readiness.'],sessions:['EXECUTION TRACE','Sessions & Events','Follow agent context windows and the events produced during execution.'],instructions:['CONTROL PLANE','Instructions','Review scoped rules that shape agent behavior and operational policy.'],audit:['SECURITY LOG','Audit','Trace administrative actions and changes across the workspace.']}[tab];let base=tab==='projects'?'/v1/projects':tab==='memories'?'/v1/memories':tab==='agents'?'/v1/agents':tab==='sessions'?'/v1/sessions':tab==='instructions'?'/v1/instructions':'/v1/audit';let url=base+'?limit=25'+(cursor?'&cursor='+encodeURIComponent(cursor):'');let d=await api(url);let items=d.items||[];hasMore=d.has_more;window.nextCursor=d.next_cursor;let q=$('q').value.toLowerCase();if(q)items=items.filter(i=>JSON.stringify(i).toLowerCase().includes(q));let cols=tab==='projects'?[['Name','name'],['Slug','slug'],['Status','status'],['Description','description'],['Updated',i=>new Date(i.updated_at).toLocaleString()]]:tab==='memories'?[['Title','title'],['Type','type'],['Scope','scope'],['Importance','importance'],['Pinned','pinned'],['Status','status'],['Tags',i=>(i.tags||[]).join(', ')],['Created',i=>new Date(i.created_at).toLocaleString()]]:tab==='agents'?[['Name','name'],['Provider','provider'],['Model','model'],['Projects',i=>(i.project_ids||[]).length],['Status','status'],['Created',i=>new Date(i.created_at).toLocaleString()]]:tab==='sessions'?[['Task','task'],['Project','project_id'],['Agent','agent_id'],['Status','status'],['Created',i=>new Date(i.created_at).toLocaleString()]]:tab==='instructions'?[['Title','title'],['Scope','scope'],['Priority','priority'],['Status','status'],['Source','source'],['Updated',i=>new Date(i.updated_at).toLocaleString()]]:[['Action','action'],['Resource','resource'],['Resource ID','resource_id'],['Project','project_id'],['When',i=>new Date(i.created_at).toLocaleString()]];$('app').innerHTML='<header class="page-hero"><div class="page-hero-copy"><span class="page-kicker">'+meta[0]+'</span><h1>'+meta[1]+'</h1><p>'+meta[2]+'</p></div><button onclick="load()">Refresh data</button></header><section class="record-panel"><div class="record-toolbar"><strong>'+meta[1]+' directory</strong><span class="record-count">'+items.length+' records on this page · select a row for details</span></div>'+table(items,cols)+pager()+'</section>';document.querySelectorAll('#app tbody tr').forEach((tr,n)=>tr.onclick=()=>tab==='sessions'?showSession(items[n]):tab==='memories'?showMemory(items[n]):showDetail(items[n].title||items[n].name||items[n].action||tab,items[n]))}
async function showSession(session){$('detail-approve').hidden=true;$('detail-task-actions').replaceChildren();let [full,events,summary]=await Promise.all([api('/v1/sessions/'+session.id),api('/v1/sessions/'+session.id+'/events?limit=100&order=asc').catch(()=>({items:[]})),api('/v1/sessions/'+session.id+'/summary').catch(()=>null)]);$('detail-title').textContent='Session · '+(session.task||session.id);$('detail-body').innerHTML='<h3>Session record</h3><pre class="json">'+esc(JSON.stringify(full,null,2))+'</pre>'+(summary?'<h3>Summary</h3><pre class="json">'+esc(JSON.stringify(summary,null,2))+'</pre>':'')+'<h3>Events ('+events.items.length+')</h3>'+(events.items.length?events.items.map(e=>'<article class="event"><strong>'+esc(e.role)+' · '+esc(e.kind)+'</strong><div class="muted">'+esc(e.created_at||'')+'</div><div>'+esc(e.content)+'</div></article>').join(''):'<div class="empty">No events recorded</div>');$('detail').showModal()}
function addManualEntryAction(){if(memberMode||!['projects','agents','instructions'].includes(tab))return;const hero=$('app').querySelector('.page-hero');if(!hero||hero.querySelector('.manual-create'))return;let actions=hero.querySelector('.page-actions');if(!actions){actions=document.createElement('div');actions.className='page-actions';const existing=hero.querySelector(':scope > button');if(existing)actions.append(existing);hero.append(actions)}const labels={projects:'New project',agents:'New agent',instructions:'New instruction'};const button=document.createElement('button');button.className='primary manual-create';button.textContent=labels[tab];button.onclick=()=>openManualEntry(tab);actions.append(button)}
function ensureManualDialog(){if($('manual-entry'))return $('manual-entry');const dialog=document.createElement('dialog');dialog.id='manual-entry';dialog.className='detail manual-entry';dialog.innerHTML='<div class="detail-head"><div><small class="task-eyebrow">MANUAL ENTRY</small><strong id="manual-title">Create record</strong></div><div class="task-action-group"><button type="button" onclick="$(\'manual-entry\').close()">Cancel</button><button id="manual-submit" class="primary" type="submit" form="manual-form">Create</button></div></div><form id="manual-form" class="detail-body"></form>';document.body.append(dialog);let outsidePressed=false;const outside=event=>{if(event.target!==dialog)return false;const rect=dialog.getBoundingClientRect();return event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom};dialog.addEventListener('pointerdown',event=>{outsidePressed=outside(event)});dialog.addEventListener('pointercancel',()=>{outsidePressed=false});dialog.addEventListener('click',event=>{const dismiss=outsidePressed&&outside(event);outsidePressed=false;if(dismiss)dialog.close()});dialog.addEventListener('close',()=>{outsidePressed=false});return dialog}
function jsonValue(id){const raw=$(id)?.value.trim();if(!raw)return {};try{const value=JSON.parse(raw);if(!value||Array.isArray(value)||typeof value!=='object')throw Error();return value}catch(_){throw Error('Metadata must be a valid JSON object')}}
async function openManualEntry(kind){const dialog=ensureManualDialog();const form=$('manual-form');$('manual-title').textContent={projects:'Create project',agents:'Register agent',instructions:'Create instruction'}[kind];$('manual-submit').textContent={projects:'Create project',agents:'Register agent',instructions:'Create instruction'}[kind];if(kind==='projects')form.innerHTML='<div class="form-intro"><strong>New workspace project</strong><p>Projects group tasks, memories, and agents under one operational context.</p></div><label>Project name<input id="manual-name" required maxlength="200" placeholder="e.g. Atlas Core"></label><label>Slug<input id="manual-slug" required maxlength="100" pattern="[a-z0-9][a-z0-9-]*" placeholder="atlas-core"><small>Lowercase letters, numbers, and hyphens only.</small></label><label>Description<textarea id="manual-description" rows="4" placeholder="Describe the project purpose and scope"></textarea></label><label>Metadata <span class="muted">optional JSON</span><textarea id="manual-metadata" rows="4" placeholder=\'{"owner":"platform"}\'></textarea></label>';if(kind==='agents'){const projects=await api('/v1/projects?limit=100');form.innerHTML='<div class="form-intro"><strong>Register an agent</strong><p>Describe the model and connect it to the projects it can access.</p></div><label>Agent name<input id="manual-name" required maxlength="200" placeholder="e.g. Research Agent"></label><div class="grid"><label>Provider<input id="manual-provider" placeholder="OpenAI, Anthropic, local…"></label><label>Model<input id="manual-model" placeholder="Model identifier"></label></div><label>Description<textarea id="manual-description" rows="4" placeholder="Agent role, capabilities, and operating constraints"></textarea></label><label>Project access<select id="manual-projects" multiple size="'+Math.min(6,Math.max(3,projects.items.length))+'">'+projects.items.map(project=>'<option value="'+esc(project.id)+'">'+esc(project.name)+'</option>').join('')+'</select><small>Use Ctrl/Cmd to select multiple projects.</small></label><label>Metadata <span class="muted">optional JSON</span><textarea id="manual-metadata" rows="4" placeholder=\'{"team":"automation"}\'></textarea></label>'}if(kind==='instructions'){form.innerHTML='<label>Title<input id="instruction-title" required maxlength="500" placeholder="Instruction title"></label><label>Content<textarea id="instruction-content" rows="8" required placeholder="Write the instruction…"></textarea></label><label>Priority<input id="instruction-priority" type="number" min="0" max="100" required value="100"></label><label>Status<select id="instruction-status"><option value="draft" selected>Draft</option><option value="approved">Approved</option><option value="revoked">Revoked</option></select></label><label>Tags<input id="instruction-tags" placeholder="Comma separated"></label>';form.onsubmit=event=>saveManualEntry(event,kind);dialog.showModal();decorateIcons(dialog);return}if(kind==='instructions-old'){const [projects,agents]=await Promise.all([api('/v1/projects?limit=100'),api('/v1/agents?limit=100')]);form.innerHTML='<div class="form-intro"><strong>New operating instruction</strong><p>Instructions become reusable policy context for agents and projects.</p></div><label>Title<input id="manual-title-field" required maxlength="300" placeholder="e.g. Production data handling"></label><label>Instruction content<textarea id="manual-content" required rows="8" placeholder="Write the rule or operational guidance clearly…"></textarea></label><div class="grid"><label>Scope<select id="manual-scope" onchange="updateInstructionTarget()"><option value="global">Global</option><option value="project">Project</option><option value="agent">Agent</option></select></label><label>Priority<input id="manual-priority" type="number" min="0" max="100" value="50" required></label><label>Status<select id="manual-status"><option value="draft">Draft</option><option value="approved">Approved</option></select></label></div><label id="manual-target-wrap" hidden>Scope target<select id="manual-target"></select></label><label>Source<input id="manual-source" required value="manual" placeholder="manual"></label><label>Tags <span class="muted">comma separated</span><input id="manual-tags" placeholder="security, production"></label>';form.dataset.projects=JSON.stringify(projects.items.map(x=>({id:x.id,name:x.name})));form.dataset.agents=JSON.stringify(agents.items.map(x=>({id:x.id,name:x.name})))}form.onsubmit=event=>saveManualEntry(event,kind);dialog.showModal();decorateIcons(dialog)}
function updateInstructionTarget(){const form=$('manual-form'),scope=$('manual-scope').value,wrap=$('manual-target-wrap'),target=$('manual-target');wrap.hidden=scope==='global';if(scope==='global'){target.innerHTML='';return}const items=JSON.parse(form.dataset[scope==='project'?'projects':'agents']||'[]');target.innerHTML=items.map(item=>'<option value="'+esc(item.id)+'">'+esc(item.name)+'</option>').join('')}
async function saveManualEntry(event,kind){event.preventDefault();const button=$('manual-submit');button.disabled=true;try{let path,payload;if(kind==='projects'){path='/v1/projects';payload={name:$('manual-name').value.trim(),slug:$('manual-slug').value.trim(),description:$('manual-description').value.trim()||null,metadata:jsonValue('manual-metadata')}}else if(kind==='agents'){path='/v1/agents';payload={name:$('manual-name').value.trim(),provider:$('manual-provider').value.trim()||null,model:$('manual-model').value.trim()||null,description:$('manual-description').value.trim()||null,project_ids:Array.from($('manual-projects').selectedOptions,x=>x.value),metadata:jsonValue('manual-metadata')}}else{path='/v1/instructions';payload={title:$('instruction-title').value.trim(),content:$('instruction-content').value.trim(),scope:'global',priority:Number($('instruction-priority').value),source:'manual',status:'draft',tags:$('instruction-tags').value.split(',').map(x=>x.trim()).filter(Boolean)}}await api(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});$('manual-entry').close();toast({projects:'Project created',agents:'Agent registered',instructions:'Instruction created'}[kind]);await load()}catch(error){toast('Could not create record: '+error.message,'error')}finally{button.disabled=false}}
$('task-project').addEventListener('change',()=>agentOptions($('task-project').value));$('task-files').addEventListener('change',e=>{stageTaskFiles(e.target.files);e.target.value=''});const taskDrop=$('task-drop');taskDrop.addEventListener('dragover',e=>{e.preventDefault();taskDrop.classList.add('dragging')});taskDrop.addEventListener('dragleave',()=>taskDrop.classList.remove('dragging'));taskDrop.addEventListener('drop',e=>{e.preventDefault();taskDrop.classList.remove('dragging');stageTaskFiles(e.dataTransfer.files)});load();
function backgroundRefresh(){
  const editing=document.activeElement?.matches('input,textarea,select,[contenteditable="true"],.ql-editor');
  if(document.visibilityState!=='visible')return;
  if(tab==='members'||document.querySelector('dialog[open]')||editing){
    $('updated').textContent='Auto refresh paused while editing';
    return;
  }
  load();
}
setInterval(backgroundRefresh,5000);
document.addEventListener('visibilitychange',backgroundRefresh);
</script></body></html>'''


def ui_response() -> HTMLResponse:
    return HTMLResponse(UI_HTML)
