-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Trips table
create table public.trips (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users(id) on delete cascade,
    request jsonb not null,
    result text,
    status text not null default 'pending' check (status in ('pending', 'planning', 'complete', 'error')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- Itineraries table
create table public.itineraries (
    id uuid primary key default uuid_generate_v4(),
    trip_id uuid references public.trips(id) on delete cascade,
    title text not null,
    data jsonb not null,
    total_cost numeric(10, 2) not null default 0,
    currency text not null default 'USD',
    created_at timestamptz not null default now()
);

-- Row Level Security
alter table public.trips enable row level security;
alter table public.itineraries enable row level security;

create policy "Users can view own trips"
    on public.trips for select
    using (auth.uid() = user_id);

create policy "Users can insert own trips"
    on public.trips for insert
    with check (auth.uid() = user_id);

create policy "Users can update own trips"
    on public.trips for update
    using (auth.uid() = user_id);

create policy "Users can view own itineraries"
    on public.itineraries for select
    using (trip_id in (select id from public.trips where user_id = auth.uid()));

-- Updated_at trigger
create or replace function public.update_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

create trigger trips_updated_at
    before update on public.trips
    for each row execute function public.update_updated_at();

-- Indexes
create index idx_trips_user_id on public.trips(user_id);
create index idx_trips_status on public.trips(status);
create index idx_itineraries_trip_id on public.itineraries(trip_id);
