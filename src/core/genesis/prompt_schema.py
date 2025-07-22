from dataclasses import dataclass, field
from typing import List

@dataclass
class Metadata:
    instance_name: str
    prompt_schema_version: float

@dataclass
class MarketAnalysis:
    sector: str
    target_customer: str
    key_competitors: List[str]
    market_trends: List[str]

@dataclass
class InitialStrategy:
    business_model: str
    go_to_market: str
    brand_positioning: str



@dataclass
class InitialResources:
    virtual_capital: int
    agent_workforce_template: str

@dataclass
class SelfImprovementParameters:
    primary_directive: str
    evolution_aggressiveness: float
    learning_scope: List[str]
    feedback_loops: List[str]

@dataclass
class PromptSeminal:
    metadata: Metadata
    mission_statement: str
    market_analysis: MarketAnalysis
    initial_strategy: InitialStrategy
    ethical_charter: List[str] # Changed to List[str] to directly map YAML list
    initial_resources: InitialResources
    self_improvement_parameters: SelfImprovementParameters
