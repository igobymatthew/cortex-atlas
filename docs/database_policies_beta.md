1) Supabase schema sketch for Cortex Atlas (Postgres)

This is a sane baseline for: users → orgs → projects → documents → analysis runs → results. Plus billing/audit hooks later.

Core entities

orgs
	•	id uuid pk
	•	name text
	•	slug text unique
	•	created_at timestamptz

org_members
	•	org_id uuid fk orgs
	•	user_id uuid fk auth.users
	•	role text check in ('owner','admin','member','viewer')
	•	created_at timestamptz
	•	PK (org_id, user_id)

projects
	•	id uuid pk
	•	org_id uuid fk orgs
	•	name text
	•	created_by uuid fk auth.users
	•	created_at timestamptz

project_members (optional; if you want per-project membership)
	•	project_id uuid fk projects
	•	user_id uuid fk auth.users
	•	role text check in ('admin','editor','viewer')
	•	PK (project_id, user_id)

Documents + artifacts

documents
	•	id uuid pk
	•	project_id uuid fk projects
	•	source_type text (e.g. upload, url, paste, integration)
	•	title text
	•	mime_type text
	•	storage_path text (Supabase Storage path)
	•	checksum text
	•	status text check in ('ingesting','ready','failed')
	•	created_by uuid fk auth.users
	•	created_at timestamptz

document_chunks (if you do your own chunking; otherwise keep chunks in a vector store)
	•	id uuid pk
	•	document_id uuid fk documents
	•	chunk_index int
	•	content text
	•	token_count int
	•	created_at timestamptz

artifacts
	•	id uuid pk
	•	project_id uuid fk projects
	•	kind text (e.g. report_pdf, json, csv, image)
	•	storage_path text
	•	meta jsonb
	•	created_by uuid fk auth.users
	•	created_at timestamptz

Analysis execution

analysis_runs
	•	id uuid pk
	•	project_id uuid fk projects
	•	created_by uuid fk auth.users
	•	status text check in ('queued','running','succeeded','failed','canceled')
	•	input jsonb (prompt params, selected docs, filters, etc.)
	•	model text
	•	started_at timestamptz
	•	finished_at timestamptz
	•	created_at timestamptz

analysis_results
	•	id uuid pk
	•	run_id uuid fk analysis_runs
	•	kind text (e.g. summary, qa, extraction, timeline)
	•	content jsonb (structured outputs; keep big text in text column if preferred)
	•	created_at timestamptz

Operational / audit

api_keys (optional if you want user-created API keys for Cortex Atlas, separate from Supabase keys)
	•	id uuid pk
	•	org_id uuid fk orgs
	•	label text
	•	hash text (store hashed token)
	•	created_by uuid fk auth.users
	•	revoked_at timestamptz
	•	created_at timestamptz

audit_events
	•	id uuid pk
	•	org_id uuid
	•	actor_user_id uuid
	•	action text
	•	target_type text
	•	target_id uuid
	•	meta jsonb
	•	created_at timestamptz

Indexes you will want early:
	•	org_members(user_id), projects(org_id), documents(project_id,status), analysis_runs(project_id,status,created_at)

⸻

2) Example RLS policies (copy/paste SQL patterns)

Helper: “is org member?”

Create a helper function so policies stay readable:

create or replace function public.is_org_member(_org_id uuid)
returns boolean
language sql
stable
as $$
  select exists (
    select 1
    from public.org_members m
    where m.org_id = _org_id
      and m.user_id = auth.uid()
  );
$$;

If you do project_members, add:

create or replace function public.is_project_member(_project_id uuid)
returns boolean
language sql
stable
as $$
  select exists (
    select 1
    from public.project_members pm
    where pm.project_id = _project_id
      and pm.user_id = auth.uid()
  );
$$;

Enable RLS

alter table public.orgs enable row level security;
alter table public.org_members enable row level security;
alter table public.projects enable row level security;
alter table public.documents enable row level security;
alter table public.analysis_runs enable row level security;
alter table public.analysis_results enable row level security;
alter table public.artifacts enable row level security;

orgs: members can read, owners/admin can update

create policy "orgs_read_if_member"
on public.orgs for select
using (public.is_org_member(id));

create policy "orgs_update_if_admin"
on public.orgs for update
using (
  exists (
    select 1 from public.org_members m
    where m.org_id = id
      and m.user_id = auth.uid()
      and m.role in ('owner','admin')
  )
);

org_members: members can view membership; only owners/admin manage

create policy "org_members_read_if_member"
on public.org_members for select
using (public.is_org_member(org_id));

create policy "org_members_insert_if_admin"
on public.org_members for insert
with check (
  exists (
    select 1 from public.org_members m
    where m.org_id = org_id
      and m.user_id = auth.uid()
      and m.role in ('owner','admin')
  )
);

create policy "org_members_update_delete_if_owner"
on public.org_members for update, delete
using (
  exists (
    select 1 from public.org_members m
    where m.org_id = org_id
      and m.user_id = auth.uid()
      and m.role = 'owner'
  )
);

projects: readable by org members; writable by org admin (or project roles)

create policy "projects_read_if_org_member"
on public.projects for select
using (public.is_org_member(org_id));

create policy "projects_insert_if_org_member"
on public.projects for insert
with check (public.is_org_member(org_id));

create policy "projects_update_if_org_admin"
on public.projects for update
using (
  exists (
    select 1 from public.org_members m
    where m.org_id = org_id
      and m.user_id = auth.uid()
      and m.role in ('owner','admin')
  )
);

documents: access via project’s org

create policy "documents_read_if_org_member"
on public.documents for select
using (
  exists (
    select 1
    from public.projects p
    where p.id = documents.project_id
      and public.is_org_member(p.org_id)
  )
);

create policy "documents_insert_if_org_member"
on public.documents for insert
with check (
  exists (
    select 1
    from public.projects p
    where p.id = documents.project_id
      and public.is_org_member(p.org_id)
  )
);

analysis_runs & results: access controlled by project membership

create policy "runs_read_if_org_member"
on public.analysis_runs for select
using (
  exists (
    select 1
    from public.projects p
    where p.id = analysis_runs.project_id
      and public.is_org_member(p.org_id)
  )
);

create policy "runs_insert_if_org_member"
on public.analysis_runs for insert
with check (
  exists (
    select 1
    from public.projects p
    where p.id = analysis_runs.project_id
      and public.is_org_member(p.org_id)
  )
);

create policy "results_read_if_org_member"
on public.analysis_results for select
using (
  exists (
    select 1
    from public.analysis_runs r
    join public.projects p on p.id = r.project_id
    where r.id = analysis_results.run_id
      and public.is_org_member(p.org_id)
  )
);

Important operational note

Your worker (FastAPI / job runner) should use the service role key to bypass RLS when it needs to read/write across orgs. Do not ship the service role key to the client.

⸻

3) FastAPI + Supabase coexistence map

You have three clean patterns; you can mix them.

Pattern A: Client ↔ Supabase directly (most CRUD)

Use Supabase client SDK in the frontend:
	•	list projects
	•	upload documents metadata
	•	view runs/results
	•	read only what RLS allows

Pros: fastest, least backend code
Cons: you must get RLS right (but you should anyway)

Pattern B: FastAPI as “compute + privileged orchestrator”

FastAPI does:
	•	ingestion pipeline (parse files, chunk, embed)
	•	run analysis jobs (LLM calls, multi-step flows)
	•	write results back to Postgres
	•	generate signed URLs for artifacts
	•	enforce rate limits / quotas / cost controls

It uses:
	•	Supabase service role key (server-side only)
	•	Optionally verifies end-user JWT when user hits FastAPI endpoints

Pros: real control over compute and cost; keeps secrets server-side
Cons: more code, but it’s the code you actually want

Pattern C: Hybrid “thin API”

Frontend still does normal reads/writes with RLS, but anything sensitive goes through FastAPI:
	•	“start_run” endpoint that validates inputs, sets queued, enqueues job
	•	“cancel_run”
	•	“download_report” that returns signed URL
	•	“admin” endpoints

This is usually the sweet spot for Cortex Atlas.

JWT verification for user-facing FastAPI endpoints

If FastAPI needs to know who is calling:
	•	Verify the Supabase JWT (from Authorization: Bearer ...)
	•	Use the sub claim as user id (auth.users.id)

Then either:
	•	Use anon key + RLS and “act as user”, or
	•	Use service role and enforce your own checks (I prefer this for compute endpoints)

Realtime / status updates
	•	Use Supabase Realtime to subscribe to analysis_runs changes
	•	Worker updates run status in Postgres
	•	UI updates instantly without polling

⸻

4) Where Supabase will hit limits later (and what to do)

Limit 1: Heavy compute + long-running jobs

Supabase is not your job system.
	•	Fix: keep FastAPI + a queue (Redis/RQ, Celery, Dramatiq, or a managed queue). Supabase remains the system of record + realtime feed.

Limit 2: Vector search at scale (pgvector)

pgvector is great until it isn’t:
	•	large corpora, high QPS similarity search, heavy filtering + reranking can get expensive
	•	Fix options:
	•	Start with pgvector for MVP
	•	Graduate to a dedicated vector DB (Pinecone/Weaviate/Qdrant) or hybrid (Postgres metadata + vector store)

Limit 3: Multi-region / global latency

Supabase projects are region-based.
	•	Fix: put compute near DB; use caching; eventually split read replicas / edge caching; if you need true global active-active, you’re in custom infra land.

Limit 4: Fine-grained RBAC complexity

RLS can get gnarly when you have:
	•	org roles + project roles + resource-level ACLs
	•	Fix: keep the model simple (org membership + optional project membership) and avoid per-row ACL tables unless you must.

Limit 5: Storage + egress costs / large artifacts

Reports, embeddings, and big exports add up.
	•	Fix: lifecycle policies, compression, “cold storage” bucket, and signed URLs (never proxy large downloads through FastAPI unless needed).

Limit 6: Migration discipline

Fast iteration + multiple environments can turn schema into sludge.
	•	Fix: use proper migrations (Supabase CLI), treat DB schema like code, add CI checks for migrations.

Limit 7: “Service role everywhere” foot-guns

If you overuse service role, you silently bypass RLS and can create data leaks via bugs.
	•	Fix: Only use service role in workers/admin paths; keep user-facing reads/writes RLS-backed.

⸻

If you want the fastest next step

Say whether Cortex Atlas is:
	•	single-tenant per user, or
	•	org/project multi-tenant (my assumption above)

Either way, I can output a single SQL migration that creates the tables + indexes + RLS policies in one shot.