"""
Unified Intelligence System Module

Main orchestrator for the 8D intelligence system.
"""

import numpy as np
from typing import Optional, List, Dict, Any
import json
import time

from ..novelty_engine import NoveltyTensorEngine
from ..pattern_space import PatternSpaceManager, Pattern
from ..dimensions import DimensionalProcessingCore
from ..meta_compass import PerspectiveShiftCore, SelfMonitor
from ..logic_layers import LogicLayersToolkit
from ..utils import (
    generate_id,
    timestamp_now,
    cosine_similarity,
    create_trace,
    log_trace,
)


class UnifiedIntelligenceSystem:
    """
    Main orchestrator for the 8D Unified Intelligence System.
    
    Coordinates all components to process queries through
    the complete intelligence cycle.
    
    Attributes:
        novelty_engine: Novelty detection engine
        pattern_space: Pattern storage manager
        dimensional_core: 8D processing core
        perspective_shift: Perspective shifting engine
        self_monitor: Self-monitoring engine
        logic_toolkit: Logic layers toolkit
    """
    
    def __init__(self):
        """Initialize the unified intelligence system."""
        self.novelty_engine = NoveltyTensorEngine()
        self.pattern_space = PatternSpaceManager()
        self.dimensional_core = DimensionalProcessingCore()
        self.perspective_shift = PerspectiveShiftCore()
        self.self_monitor = SelfMonitor()
        self.logic_toolkit = LogicLayersToolkit()
        
        self._initialized = False
        self._current_trace_id: Optional[str] = None
    
    def initialize(self) -> None:
        """Initialize the system."""
        if not self._initialized:
            self.novelty_engine.initialize()
            self.pattern_space._connect()
            self._initialized = True
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check.
        
        Returns:
            Health status dictionary
        """
        return {
            "status": "healthy",
            "components": {
                "novelty_engine": "active",
                "pattern_space": "active",
                "dimensional_core": "active",
                "perspective_shift": "active",
                "self_monitor": "active",
                "logic_toolkit": "active",
            },
        }
    
    def _create_trace(self, operation: str) -> str:
        """
        Create a trace ID for logging.
        
        Args:
            operation: Operation name
            
        Returns:
            Trace ID string
        """
        self._current_trace_id = generate_id("trace")
        log_trace(create_trace(self._current_trace_id, operation))
        return self._current_trace_id
    
    def _perceive_and_contextualize(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Perceive input and contextualize.
        
        Extracts semantic meaning and prepares query for processing.
        
        Args:
            query: Input query
            context: Additional context
            
        Returns:
            Perception dictionary with query embedding and metadata
        """
        trace_id = self._create_trace("perceive_and_contextualize")
        
        # Handle None or empty query - convert to empty string
        query = query or ""
        
        # Generate query embedding
        embedding = self.novelty_engine.generate_embedding(query)
        
        # Extract query features
        safe_query = query if query else ""
        features = {
            "length": len(safe_query),
            "words": len(safe_query.split()),
            "uppercase_ratio": sum(1 for c in safe_query if c.isupper()) / max(len(safe_query), 1),
            "punctuation_ratio": sum(1 for c in safe_query if c in ".!?,:;") / max(len(safe_query), 1),
        }
        
        # Add context if provided
        full_context = context.copy() if context else {}
        full_context["query"] = safe_query
        full_context["timestamp"] = timestamp_now()
        
        perception = {
            "trace_id": trace_id,
            "query": safe_query,
            "embedding": embedding,
            "features": features,
            "context": full_context,
            "perception_timestamp": timestamp_now(),
        }
        
        log_trace(
            create_trace(trace_id, "perceive_and_contextualize", {"features": features}),
            "debug"
        )
        
        return perception
    
    def _activate_meta_compass(
        self,
        perception: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Activate meta-cognitive oversight.
        
        Engages perspective shifting and self-monitoring.
        
        Args:
            perception: Perceived query data
            
        Returns:
            Meta-compass analysis results
        """
        trace_id = perception.get("trace_id", generate_id("trace"))
        
        # Perspective shift analysis
        perspective_analysis = self.perspective_shift.analyze(perception)
        
        # Self-monitoring check
        self_monitoring = self.self_monitor.check(perception)
        
        # Identify assumptions and blind spots
        assumptions = self.self_monitor.identify_assumptions(perception)
        blind_spots = self.self_monitor.detect_blind_spots(perception)
        
        meta_compass = {
            "trace_id": trace_id,
            "perspective_analysis": perspective_analysis,
            "self_monitoring": self_monitoring,
            "assumptions": assumptions,
            "blind_spots": blind_spots,
            "oversight_score": perspective_analysis.get("oversight_score", 0.0),
            "activation_timestamp": timestamp_now(),
        }
        
        return meta_compass
    
    def _select_logic_layers(
        self,
        perception: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Select appropriate logic layers.
        
        Chooses reasoning frameworks based on query characteristics.
        
        Args:
            perception: Perceived query data
            
        Returns:
            Logic layer selection results
        """
        trace_id = perception.get("trace_id", generate_id("trace"))
        
        # Analyze query features
        features = perception.get("features", {})
        query_length = features.get("length", 0)
        
        # Select logic layers based on query characteristics
        selected_layers = []
        weights = {}
        
        # Always include toolkit
        selected_layers.append("toolkit")
        weights["toolkit"] = 1.0
        
        # Select based on features
        if query_length > 50:
            selected_layers.append("systems_thinking")
            weights["systems_thinking"] = 0.8
        
        # Safely get query text
        query_text = perception.get("query")
        if query_text is None:
            query_text = ""
        query_text = query_text.lower() if query_text else ""
        
        if "why" in query_text:
            selected_layers.append("five_whys")
            weights["five_whys"] = 0.9
        
        if "how" in query_text:
            selected_layers.append("socratic")
            weights["socratic"] = 0.7
        
        # Add logic layer results
        logic_selection = {
            "trace_id": trace_id,
            "selected_layers": selected_layers,
            "weights": weights,
            "selection_criteria": {
                "query_length": query_length,
                "keywords_detected": self._detect_keywords(perception.get("query") or ""),
            },
            "selection_timestamp": timestamp_now(),
        }
        
        return logic_selection
    
    def _detect_keywords(self, query: str) -> List[str]:
        """
        Detect keywords in query.
        
        Args:
            query: Query string
            
        Returns:
            List of detected keywords
        """
        keywords = []
        query_lower = (query or "").lower()
        
        keyword_patterns = {
            "why": "why",
            "how": "how",
            "what": "what",
            "when": "when",
            "where": "where",
            "who": "who",
            "problem": "problem",
            "solution": "solution",
            "cause": "cause",
            "effect": "effect",
            "reason": "reason",
            "impact": "impact",
            "strategy": "strategy",
            "approach": "approach",
            "method": "method",
        }
        
        for keyword, pattern in keyword_patterns.items():
            if pattern in query_lower:
                keywords.append(keyword)
        
        return keywords[:5]  # Limit to 5 keywords
    
    def _branch_and_explore(
        self,
        perception: Dict[str, Any],
        logic_selection: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Branch exploration through logic layers.
        
        Generates multiple reasoning paths.
        
        Args:
            perception: Perceived query data
            logic_selection: Selected logic layers
            
        Returns:
            List of exploration branches
        """
        trace_id = perception.get("trace_id", generate_id("trace"))
        branches = []
        
        # Process through each selected logic layer
        for layer in logic_selection.get("selected_layers", []):
            layer_branch = {
                "trace_id": trace_id,
                "layer": layer,
                "path": [],
                "insights": [],
            }
            
            # Apply logic layer
            if layer == "socratic":
                result = self.logic_toolkit.socratic_decomposition(perception)
            elif layer == "first_principles":
                result = self.logic_toolkit.first_principles_abduction(perception)
            elif layer == "systems_thinking":
                result = self.logic_toolkit.systems_analysis(perception)
            elif layer == "five_whys":
                result = self.logic_toolkit.five_whys_analysis(perception)
            elif layer == "argument_mapping":
                result = self.logic_toolkit.argument_mapping(perception)
            else:
                result = self.logic_toolkit.general_analysis(perception)
            
            # Add to branch
            layer_branch["path"].append(result.get("path", []))
            layer_branch["insights"].append(result.get("insights", []))
            branches.append(layer_branch)
        
        # Merge branches
        merged_branches = self._merge_branches(branches)
        
        return merged_branches
    
    def _merge_branches(self, branches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Merge multiple exploration branches.
        
        Args:
            branches: List of exploration branches
            
        Returns:
            Merged branches
        """
        if not branches:
            return []
        
        # Merge insights from all branches
        all_insights = []
        for branch in branches:
            all_insights.extend(branch.get("insights", []))
        
        # Remove duplicates
        unique_insights = list({json.dumps(i, sort_keys=True): i for i in all_insights}.values())
        
        # Merge paths
        all_paths = []
        for branch in branches:
            all_paths.extend(branch.get("path", []))
        
        return [
            {
                "trace_id": branches[0].get("trace_id"),
                "layer": "merged",
                "path": all_paths,
                "insights": unique_insights,
            }
        ]
    
    def _detect_novelty(
        self,
        branches: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Detect novelty in exploration results.
        
        Compares branches against known patterns.
        
        Args:
            branches: Exploration branches
            
        Returns:
            Novelty detection results
        """
        trace_id = branches[0].get("trace_id", generate_id("trace")) if branches else generate_id("trace")
        
        novelty_results = {
            "trace_id": trace_id,
            "novelty_scores": [],
            "novel_insights": [],
            "confidence": 0.0,
        }
        
        # Process each branch
        for branch in branches:
            # Generate novelty score
            novelty_score = self.novelty_engine.detect_novelty(branch)
            
            novelty_results["novelty_scores"].append({
                "layer": branch.get("layer"),
                "score": novelty_score.get("score", 0.0),
            })
            
            # Extract novel insights
            novel_insights = self.novelty_engine.extract_novelty(branch)
            novelty_results["novel_insights"].extend(novel_insights)
        
        # Calculate average confidence
        if novelty_results["novelty_scores"]:
            novelty_results["confidence"] = np.mean([
                s.get("score", 0.0) for s in novelty_results["novelty_scores"]
            ])
        
        return novelty_results
    
    def _evaluate_and_integrate(
        self,
        novelty_results: Dict[str, Any],
        branches: List[Dict[str, Any]],
        meta_compass: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Evaluate and integrate results.
        
        Synthesizes insights from all sources.
        
        Args:
            novelty_results: Novelty detection results
            branches: Exploration branches
            meta_compass: Meta-compass analysis
            
        Returns:
            Integration results
        """
        trace_id = novelty_results.get("trace_id", generate_id("trace"))
        
        # Evaluate insights
        evaluated_insights = []
        for branch in branches:
            for insight in branch.get("insights", []):
                evaluation = self._evaluate_insight(insight, meta_compass)
                evaluated_insights.append({
                    "insight": insight,
                    "evaluation": evaluation,
                    "source": branch.get("layer"),
                })
        
        # Rank insights by quality
        ranked_insights = sorted(
            evaluated_insights,
            key=lambda x: x.get("evaluation", {}).get("quality_score", 0.0),
            reverse=True,
        )
        
        # Select top insights
        top_insights = ranked_insights[:10]  # Limit to 10
        
        # Integrate with meta-compass
        integrated = {
            "trace_id": trace_id,
            "evaluated_insights": evaluated_insights,
            "top_insights": [i["insight"] for i in top_insights],
            "integration_quality": self._calculate_integration_quality(
                novelty_results, meta_compass
            ),
            "integration_timestamp": timestamp_now(),
        }
        
        return integrated
    
    def _evaluate_insight(
        self,
        insight: Dict[str, Any],
        meta_compass: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Evaluate a single insight.
        
        Args:
            insight: Insight to evaluate
            meta_compass: Meta-compass analysis
            
        Returns:
            Evaluation results
        """
        # Check against blind spots
        blind_spots = meta_compass.get("blind_spots", [])
        is_compromised = False
        for blind_spot in blind_spots:
            if blind_spot.get("term") in str(insight):
                is_compromised = True
                break
        
        # Calculate quality score
        quality_score = 0.9 if not is_compromised else 0.5
        
        return {
            "quality_score": quality_score,
            "is_compromised": is_compromised,
            "confidence": 0.8,
        }
    
    def _calculate_integration_quality(
        self,
        novelty_results: Dict[str, Any],
        meta_compass: Dict[str, Any],
    ) -> float:
        """
        Calculate integration quality score.
        
        Args:
            novelty_results: Novelty detection results
            meta_compass: Meta-compass analysis
            
        Returns:
            Quality score (0.0 to 1.0)
        """
        novelty_score = novelty_results.get("confidence", 0.0)
        oversight_score = meta_compass.get("oversight_score", 0.0)
        
        # Weighted combination
        return 0.6 * novelty_score + 0.4 * oversight_score
    
    def _act_output(
        self,
        integrated: Dict[str, Any],
        novelty_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate action/output.
        
        Creates final response based on integrated insights.
        
        Args:
            integrated: Integration results
            novelty_results: Novelty detection results
            
        Returns:
            Action/output results
        """
        trace_id = integrated.get("trace_id", generate_id("trace"))
        
        # Generate response
        top_insights = integrated.get("top_insights", [])
        novel_insights = novelty_results.get("novel_insights", [])
        
        # Combine insights
        all_insights = top_insights + novel_insights
        
        # Generate response text
        response_text = self._generate_response(all_insights)
        
        # Create output
        output = {
            "trace_id": trace_id,
            "response": response_text,
            "insights_used": len(all_insights),
            "novelty_detected": novelty_results.get("confidence", 0.0) > 0.5,
            "output_timestamp": timestamp_now(),
        }
        
        return output
    
    def _generate_response(self, insights: List[Dict[str, Any]]) -> str:
        """
        Generate response from insights.
        
        Args:
            insights: List of insights
            
        Returns:
            Response text
        """
        if not insights:
            return "No insights generated."
        
        # Format insights
        insight_texts = [json.dumps(i, indent=2) for i in insights[:5]]
        
        return f"Analysis complete. Key insights:\n{chr(10).join(insight_texts)}"
    
    def process_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Process a query through the complete intelligence cycle.
        
        Args:
            query: Input query
            context: Additional context
        
        Returns:
            Processing results
        """
        start_time = time.time()
        
        # Initialize trace
        self._create_trace("process_query")
        
        try:
            # Step 1: Perceive & Contextualize
            perception = self._perceive_and_contextualize(query, context)
            
            # Step 2: Activate Meta-Compass
            meta_compass = self._activate_meta_compass(perception)
            
            # Step 3: Select Logic Layers
            logic_selection = self._select_logic_layers(perception)
            
            # Step 4: Branch & Explore
            branches = self._branch_and_explore(perception, logic_selection)
            
            # Step 5: Novelty Detection
            novelty_results = self._detect_novelty(branches)
            
            # Step 6: Evaluate & Integrate
            integrated = self._evaluate_and_integrate(
                novelty_results, branches, meta_compass
            )
            
            # Step 7: Act / Output
            output = self._act_output(integrated, novelty_results)
            
            # Calculate total time
            total_time = time.time() - start_time
            
            # Compile final results
            results = {
                "trace_id": output.get("trace_id"),
                "response": output.get("response"),
                "processing_time": total_time,
                "insights_count": output.get("insights_used", 0),
                "novelty_detected": output.get("novelty_detected"),
                "meta_compass_score": meta_compass.get("oversight_score", 0.0),
                "novelty_score": novelty_results.get("confidence", 0.0),
                "integration_quality": integrated.get("integration_quality", 0.0),
                "timestamp": timestamp_now(),
                "status": "completed",
            }
            
            log_trace(
                create_trace(output.get("trace_id"), "process_query_complete", results),
                "info"
            )
            
            return results
            
        except Exception as e:
            # Handle errors gracefully
            error_results = {
                "trace_id": self._current_trace_id,
                "response": f"Processing error: {str(e)}",
                "processing_time": time.time() - start_time,
                "status": "error",
                "error_message": str(e),
                "timestamp": timestamp_now(),
            }
            
            log_trace(
                create_trace(self._current_trace_id, "process_query_error", error_results),
                "error"
            )
            
            return error_results
    
    def shutdown(self) -> None:
        """Shutdown the system."""
        self._initialized = False
        self.pattern_space._disconnect()


# Singleton instance for lazy loading
_system_instance: Optional[UnifiedIntelligenceSystem] = None


def get_system() -> UnifiedIntelligenceSystem:
    """
    Get or create the system instance.
    
    Returns:
        UnifiedIntelligenceSystem instance
    """
    global _system_instance
    if _system_instance is None:
        _system_instance = UnifiedIntelligenceSystem()
        _system_instance.initialize()
    return _system_instance
