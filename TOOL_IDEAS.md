# Tool Ideas & Agent Capabilities

## Overview
This document outlines brainstorming and ideation for specialized agents and MCP (Model Context Protocol) tools. These concepts are designed to extend the core "Conversational Analytics Agent" to enhance its investigative capabilities, detect fraud typologies, and provide high-impact demonstrations for the AI For Accountability Hackathon.

## 1. The "Web Weaver" (Graph/Network Analysis Agent)
**Concept:** An agent specialized in finding loops, connections, and conflicts of interest.
**Hackathon Value:** Visualizing complex corporate shells or circular charity gifting loops is a highly demo-able feature that judges love.

**Suggested MCP Tools:**
* `generate_network_graph`: Takes relationship data (CRA gift flows, shared board directors, grant distributions) and outputs Python NetworkX graphs, Mermaid.js diagrams, or Gephi files.
* `find_shortest_path`: Interrogates the system to "find the connection between Charity A and Federal Grant B," traversing the `entity_golden_records` and alias tables to find hidden linkages via board members or corporate aliases.

## 2. The "Auditor" (Red-Flag & Anomaly Detection Agent)
**Concept:** A specialized agent that proactively scans for fraud typologies rather than waiting for user questions.
**Hackathon Value:** The agent shifts from reactive (answering questions) to proactive (reporting, "I scanned the new datasets and found 14 entities that look like high-risk shell corporations").

**Suggested MCP Tools:**
* `run_anomaly_scan`: Tools using statistical libraries (like PyOD or Pandas-profiling) to flag statistical outliers in the data.
* `check_double_dipping`: Queries the Golden Record table to find entities that received Federal Grants and Alberta grants for the *exact same* program descriptions in the same year.

## 3. The "Policy Whisperer" (RAG/Compliance Agent)
**Concept:** Data is only suspicious if you understand the rules. This agent answers *why* a data point is illegal or non-compliant.
**Workflow:** The BigQuery agent finds a $5M sole-source contract. It passes the context to the Policy Agent, which responds: "Under TBS rules, sole-source contracts over $25k are only permitted under national security exemptions or extreme urgency. This warrants investigation."

**Suggested MCP Tools:**
* A vector search tool (`agent_platform_vector_search`) loaded with:
  * CRA guidelines for registered charities (T3010 reporting requirements).
  * Treasury Board of Canada Secretariat (TBS) rules on sole-source contracts.

## 4. The "Spotlight" (Web & Media Verification Tool)
**Concept:** Connecting raw data to real-world impact.
**Hackathon Value:** If the BigQuery agent flags an Alberta non-profit receiving $10M, the agent can automatically trigger the Spotlight tool to check if the non-profit actually has a functional website or any news presence. If it has a $10M budget but zero web footprint, the agent flags it as a high-confidence shell entity.

**Suggested MCP Tools:**
* `search_news_archives`: Integration with Tavily, News API, or Google Search.
* `fetch_website_summary`: A tool that scrapes a charity's domain.

## 5. "The Lobbyist Link" (External API Tool)
**Concept:** Cross-referencing financial flows with political influence.
**Workflow:** If the BigQuery agent finds an Alberta company sweeping up sole-source contracts, it can pass the directors' names (from the Golden Record) to the Lobbyist tool to see if they recently registered to lobby the minister who approved the contracts.

**Suggested MCP Tools:**
* API access to the **Federal Registry of Lobbyists** or **Elections Canada Political Contributions** databases.