# NASCAR Pit Box AI Assistant

Voice-driven AI assistant for NASCAR pit box operations, featuring LangGraph agents, FastAPI simulator, and comprehensive evaluation.

## Architecture

```
app/
├── graphs/              # LangGraph agent definitions
│   ├── simple_pitbox.py   # Basic Q&A agent
│   └── analytics_agent.py # Advanced analytics with evaluation loop
├── tools/               # Tool implementations
│   ├── simulator_api.py   # FastAPI simulator tools
│   └── rag_knowledge.py   # Knowledge base RAG tools
├── simulator/           # FastAPI NASCAR data simulator
└── knowledge/           # RAG knowledge base
    ├── trackhouse_team.txt    # Trackhouse Racing team info
    ├── nascar_glossary.txt    # NASCAR terminology and rules
    └── nascar_tracks.txt      # Track information and history

evaluation/              # Evaluation and testing
├── golden_dataset.json   # Q&A pairs for validation
└── eval_harness.py       # Automated evaluation

tests/                   # Test suite
└── test_rag_knowledge.py  # RAG system tests

web_client/              # Demo interface (TODO: Next.js)
```