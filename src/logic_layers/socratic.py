"""
Socratic Decomposition Module

Implements Socratic questioning and decomposition.
"""

from typing import Optional, Dict, Any, List


class SocraticDecomposition:
    """
    Socratic decomposition engine.
    
    Uses Socratic questioning to break down complex ideas,
    challenge assumptions, and deepen understanding.
    
    Attributes:
        question_types: Available question types
    """
    
    def __init__(self):
        """Initialize the Socratic decomposition."""
        self.question_types = {
            "clarification": [
                "Can you explain that in different words?",
                "Could you give me an example?",
                "What do you mean by {term}?",
            ],
            "probing": [
                "What evidence supports that?",
                "How did you arrive at that conclusion?",
                "What assumptions are you making?",
            ],
            "assumption": [
                "Why must that be true?",
                "What if the opposite were true?",
                "Are there any alternative explanations?",
            ],
            "implication": [
                "What are the implications of that?",
                "How does that relate to {related_concept}?",
                "What follows from that statement?",
            ],
            "viewpoint": [
                "How would someone with a different perspective see this?",
                "What would a critic say about that?",
                "Is there another way to interpret this?",
            ],
        }
    
    def decompose_question(
        self,
        question: str,
        depth: int = 3,
    ) -> Dict[str, Any]:
        """
        Decompose a question using Socratic method.
        
        Args:
            question: Original question
            depth: Decomposition depth
        
        Returns:
            Dictionary with decomposition path and insights
        """
        decomposition = []
        current_level = [{"question": question}]
        
        for level in range(depth):
            next_level = []
            
            for q in current_level:
                # Generate follow-up questions
                follow_ups = self._generate_follow_ups(q["question"])
                next_level.extend(follow_ups)
            
            decomposition.append({
                "level": level + 1,
                "questions": next_level,
            })
            
            current_level = next_level
        
        # Build path (list of lists)
        path = []
        for level_data in decomposition:
            path.append(level_data.get("questions", []))
        
        # Build insights (key insights from the decomposition)
        insights = []
        for level_data in decomposition:
            for q_data in level_data.get("questions", []):
                insights.append({
                    "path": f"level_{level_data['level']}_{q_data.get('category', 'unknown')}",
                    "question": q_data.get("question", ""),
                    "category": q_data.get("category", ""),
                })
        
        return {
            "path": path,
            "insights": insights,
            "original_question": question,
        }
    
    def _generate_follow_ups(
        self,
        question: str,
    ) -> List[Dict[str, str]]:
        """
        Generate follow-up questions.
        
        Args:
            question: Original question
        
        Returns:
            List of follow-up questions
        """
        follow_ups = []
        
        # Extract key term from question
        key_term = self._extract_key_term(question)
        
        # Generate questions from each category
        for category, templates in self.question_types.items():
            for template in templates:
                # Replace placeholder if present
                if "{term}" in template:
                    template = template.replace("{term}", key_term)
                
                # Skip if question already asked
                if template.lower() in question.lower():
                    continue
                
                follow_ups.append({
                    "category": category,
                    "question": template,
                    "parent": question,
                })
        
        # Limit to 3 follow-ups
        return follow_ups[:3]
    
    def _extract_key_term(
        self,
        question: str,
    ) -> str:
        """
        Extract key term from question.
        
        Args:
            question: Question text
        
        Returns:
            Key term or default
        """
        # Simple extraction (placeholder)
        words = question.split()
        if len(words) >= 2:
            return words[-2]  # Second-to-last word
        return "the question"
    
    def chain_questions(
        self,
        starting_question: str,
        max_chain: int = 5,
    ) -> List[str]:
        """
        Create a chain of related questions.
        
        Args:
            starting_question: Starting question
            max_chain: Maximum chain length
        
        Returns:
            List of questions in chain
        """
        chain = [starting_question]
        current = starting_question
        
        for _ in range(max_chain):
            follow_ups = self._generate_follow_ups(current)
            if follow_ups:
                current = follow_ups[0]["question"]
                chain.append(current)
            else:
                break
        
        return chain
    
    def analyze_question_depth(
        self,
        question: str,
    ) -> Dict[str, Any]:
        """
        Analyze the depth and complexity of a question.
        
        Args:
            question: Question to analyze
        
        Returns:
            Analysis results
        """
        # Placeholder analysis
        return {
            "question": question,
            "estimated_depth": 2,
            "requires_follow_up": True,
        }
    
    def __repr__(self) -> str:
        return "SocraticDecomposition(question_types={})".format(len(self.question_types))
    
    def __str__(self) -> str:
        return self.__repr__()
