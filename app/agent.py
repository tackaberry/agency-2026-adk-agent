# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import McpToolset
from mcp import StdioServerParameters
from google.genai import types

from .spotlight_tools import spotlight_tools

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

bigquery_project = os.environ.get("BIGQUERY_PROJECT")

# Initialize the MCP Toolset for Conversational Analytics
mcp_toolset = McpToolset(
    connection_params=StdioServerParameters(
        command="./toolbox",
        args=["--prebuilt", "bigquery", "--stdio"],
        env={**os.environ, "BIGQUERY_PROJECT": bigquery_project} if bigquery_project else os.environ,
    )
)

root_agent = Agent(
    name="conversational_analytics_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        # System instructions for the agent
        "You are a sophisticated Conversational Analytics Agent and investigative researcher. "
        "Your goal is to help users analyze data by accessing data sources through your tools. "
        "Use the BigQuery tools provided via the MCP toolset to query and analyze financial/government data. "
        
        # The datasets you have access to include:
        "CRITICAL DATA DICTIONARY - ALWAYS REFER TO THIS:"
        "- `fed` dataset: Federal Grants & Contributions. (Tables: `grants_contributions`, `agreement_type_lookup`, `recipient_type_lookup`)."
        "- `ab` dataset: Alberta Open Data (Tables: `ab_grants`, `ab_contracts`, `ab_sole_source`, `ab_non_profit`)."
        "- `entity_golden_records` table: Canonical entity records mapping aliases and BNs to per-dataset profiles."
        "DATABASE RULES:"
        "1. NEVER guess table schemas. Always use the MCP tools to list tables and get schema definitions before writing SQL."
        "2. When joining across datasets, always use `entity_golden_records` as the authoritative cross-reference bridge." 
        "3. Always always check the table schema before sql queries, and ensure your SQL is compatible with the schema. If you get an error, check the schema again and adjust your SQL accordingly."
        
        # Spotlight Tools:
        "When investigating suspicious entities, charities, or grants, use the Spotlight tools "
        "(search_news_archives and load_web_page) to cross-reference data with real-world news, "
        "websites, and media presence. "

        # Emphasize that a lack of web presence or news mentions can be a red flag for shell entities, while a strong web presence can help validate legitimacy.
        "Always prioritize accuracy and provide clear explanations of your findings, highlighting "
        "if an entity lacks a web presence or has a controversial history."
    ),
    tools=[mcp_toolset, *spotlight_tools],
)

app = App(
    root_agent=root_agent,
    name="app",
)
