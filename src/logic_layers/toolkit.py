"""
Logic Layers Toolkit Module

Main toolkit for logic layer operations.
"""

from typing import Optional, Dict, Any, List
from .socratic import SocraticDecomposition
from .first_principles import FirstPrinciplesAbduction
from .systems_thinking import SystemsThinking
from .five_whys import FiveWhysRootCause
from .argument_mapping import ArgumentMapping


class LogicLayersToolkit:
    """
    Toolkit for logic layer operations.
    
    Provides access to all logic layer components
    and coordinates their use.
    
    Attributes:
        socratic: Socratic decomposition instance
        first_principles: First principles instance
        systems_thinking: Systems thinking instance
        five_whys: 5 Whys instance
        argument_mapping: Argument mapping instance
    """
    
    def __init__(self):
        """Initialize the logic layers toolkit."""
        self.socratic = SocraticDecomposition()
        self.first_principles = FirstPrinciplesAbduction()
        self.systems_thinking = SystemsThinking()
        self.five_whys = FiveWhysRootCause()
        self.argument_mapping = ArgumentMapping()
    
    def socratic_decomposition(
        self,
        perception: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Perform Socratic decomposition.
        
        Args:
            perception: Perception data
        
        Returns:
            Decomposition results
        """
        problem = perception.get("query") or ""
        return self.socratic.decompose_question(problem)
    
    def first_principles_abduction(
        self,
        perception: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Perform first principles abduction.
        
        Args:
            perception: Perception data
        
        Returns:
            Abduction results
        """
        problem = perception.get("query") or ""
        return self.first_principles.decompose_to_principles(problem)
    
    def systems_analysis(
        self,
        perception: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Perform systems thinking analysis.
        
        Args:
            perception: Perception data
        
        Returns:
            Systems analysis results
        """
        problem = perception.get("query") or ""
        return self.systems_thinking.analyze_system(problem)
    
    def five_whys_analysis(
        self,
        perception: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Perform 5 Whys analysis.
        
        Args:
            perception: Perception data
        
        Returns:
            Root cause analysis results
        """
        problem = perception.get("query") or ""
        return self.five_whys.analyze_root_cause(problem)
    
    def argument_mapping(
        self,
        perception: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Perform argument mapping.
        
        Args:
            perception: Perception data
        
        Returns:
            Argument mapping results
        """
        problem = perception.get("query") or ""
        return self.argument_mapping.map_arguments(problem, "support")
    
    def general_analysis(
        self,
        perception: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Perform general analysis on perception.
        
        Args:
            perception: Perception data
        
        Returns:
            General analysis results
        """
        problem = perception.get("query") or ""
        
        if not problem:
            return {"error": "No problem provided"}
        
        # Perform comprehensive analysis
        results = self.analyze_problem(problem)
        
        return {
            "problem": problem,
            "analysis": results,
            "methods_used": self.get_available_methods(),
        }
    
    def analyze_problem(
        self,
        problem: str,
        methods: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a problem using multiple methods.
        
        Args:
            problem: Problem statement
            methods: List of methods to use
        
        Returns:
            Analysis results
        """
        effective_methods = methods or [
            "socratic",
            "first_principles",
            "systems_thinking",
            "five_whys",
            "argument_mapping",
        ]
        
        results = {}
        
        if "socratic" in effective_methods:
            results["socratic"] = self.socratic.decompose_question(problem)
        
        if "first_principles" in effective_methods:
            results["first_principles"] = self.first_principles.decompose_to_principles(problem)
        
        if "systems_thinking" in effective_methods:
            results["systems_thinking"] = self.systems_thinking.analyze_system(problem)
        
        if "five_whys" in effective_methods:
            results["five_whys"] = self.five_whys.analyze_root_cause(problem)
        
        if "argument_mapping" in effective_methods:
            results["argument_mapping"] = self.argument_mapping.map_arguments(problem, "support")
        
        return results
    
    def get_available_methods(self) -> List[str]:
        """
        Get available analysis methods.
        
        Returns:
            List of method names
        """
        return [
            "socratic",
            "first_principles",
            "systems_thinking",
            "five_whys",
            "argument_mapping",
        ]
    
    def __repr__(self) -> str:
        return "LogicLayersToolkit(methods={})".format(len(self.get_available_methods()))
    
    def __str__(self) -> str:
        return self.__repr__()
