# Fravel

A multi-agent AI travel planner that builds complete trip itineraries. CrewAI agents handle flights, venues, scheduling, and budgeting — all streamed in real-time to a React dashboard.

**Live:** [fravel-frontend.vercel.app](https://fravel-frontend.vercel.app)

## What it does

- Multi-agent orchestration with CrewAI for trip planning
- Real-time SSE streaming of agent progress to the UI
- Flight search via Aviationstack API
- Venue discovery via Foursquare API
- PDF export of finalized trip itineraries
- Drag-and-drop itinerary editing

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | React 19, TypeScript, Tailwind CSS |
| Backend | FastAPI, CrewAI, LiteLLM |
| Database | Supabase |
| APIs | Aviationstack, Foursquare |
| Streaming | Server-Sent Events (SSE) |
| Hosting | Vercel (frontend), HuggingFace Spaces (backend) |

## Architecture

```
backend/
  app/
    agents/    — CrewAI agent definitions (flight, venue, scheduler, budget)
    routes/    — FastAPI endpoints + SSE streams
    services/  — External API integrations
    main.py    — App entrypoint
    config.py  — Environment and model config
frontend/
  src/
    components/ — React UI components
    pages/      — Route pages
    App.tsx     — Root component
supabase/       — Schema and migrations
```

Each planning request spawns a crew of specialized agents that collaborate to produce a complete itinerary. Progress is streamed to the frontend in real-time via SSE, so users see each agent's work as it happens.
