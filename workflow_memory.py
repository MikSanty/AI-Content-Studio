"""Workflow Memory - Cross-stage learning and context management."""
import os
import json
from datetime import datetime
from collections import defaultdict
from utils import ensure_dir


class WorkflowMemory:
    """Manages persistent memory across workflow stages and sessions."""
    
    def __init__(self, memory_dir='memory'):
        """
        Initialize workflow memory.
        
        Args:
            memory_dir: Directory to store memory files
        """
        self.memory_dir = memory_dir
        ensure_dir(memory_dir)
        
        self.user_preferences = {}
        self.feedback_history = []
        self.rejection_patterns = defaultdict(list)
        self.session_stats = defaultdict(int)
        
        # Load existing memory
        self._load_memory()
    
    def add_feedback(self, stage, feedback, approved=True, content_snippet=None):
        """
        Add feedback from a workflow stage.
        
        Args:
            stage: Agent stage (writer, llmon, editor)
            feedback: User feedback text
            approved: Whether content was approved
            content_snippet: Optional snippet of content (first 200 chars)
        """
        feedback_entry = {
            'stage': stage,
            'feedback': feedback,
            'approved': approved,
            'timestamp': datetime.now().isoformat(),
            'content_snippet': content_snippet[:200] if content_snippet else None
        }
        
        self.feedback_history.append(feedback_entry)
        
        # Track rejection patterns
        if not approved:
            self.rejection_patterns[stage].append(feedback)
        
        # Update session stats
        self.session_stats[f'{stage}_feedback_count'] += 1
        if approved:
            self.session_stats[f'{stage}_approvals'] += 1
        else:
            self.session_stats[f'{stage}_rejections'] += 1
        
        # Auto-save after each feedback
        self._save_memory()
    
    def add_approval(self, stage, quality_scores=None):
        """
        Record an approval at a stage.
        
        Args:
            stage: Agent stage
            quality_scores: Optional quality scores for the approved content
        """
        approval_entry = {
            'stage': stage,
            'approved': True,
            'timestamp': datetime.now().isoformat(),
            'quality_scores': quality_scores
        }
        
        self.feedback_history.append(approval_entry)
        self.session_stats[f'{stage}_approvals'] += 1
        self._save_memory()
    
    def extract_preferences(self):
        """
        Extract user preferences from feedback history.
        
        Returns:
            Dictionary of detected preferences
        """
        # Analyze rejection patterns
        common_rejections = {}
        for stage, feedbacks in self.rejection_patterns.items():
            if feedbacks:
                # Find most common words in rejections (simple analysis)
                all_words = ' '.join(feedbacks).lower().split()
                word_freq = defaultdict(int)
                for word in all_words:
                    if len(word) > 4:  # Skip short words
                        word_freq[word] += 1
                
                # Get top issues
                top_issues = sorted(
                    word_freq.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:5]
                common_rejections[stage] = [word for word, _ in top_issues]
        
        self.user_preferences['common_rejections'] = common_rejections
        
        # Analyze approval patterns
        approved_feedback = [
            f['feedback'] for f in self.feedback_history 
            if f.get('approved') and f.get('feedback')
        ]
        
        if approved_feedback:
            # Extract positive indicators
            positive_words = []
            for feedback in approved_feedback:
                words = feedback.lower().split()
                positive_words.extend([w for w in words if len(w) > 4])
            
            word_freq = defaultdict(int)
            for word in positive_words:
                word_freq[word] += 1
            
            top_positives = sorted(
                word_freq.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            self.user_preferences['approved_elements'] = [word for word, _ in top_positives]
        
        self._save_memory()
        return self.user_preferences
    
    def get_context_for_agent(self, agent_name):
        """
        Compile relevant historical context for an agent.
        
        Args:
            agent_name: Name of agent (writer, llmon, editor)
        
        Returns:
            Context string with relevant feedback and preferences
        """
        context_parts = []
        
        # Get recent feedback for this agent
        agent_feedback = [
            f for f in self.feedback_history[-10:]  # Last 10 items
            if f.get('stage') == agent_name and f.get('feedback')
        ]
        
        if agent_feedback:
            context_parts.append(f"# Recent Feedback for {agent_name.title()} Agent")
            context_parts.append("")
            
            for i, entry in enumerate(agent_feedback[-5:], 1):  # Last 5
                status = "[OK] Approved" if entry.get('approved') else "[REJECTED] Rejected"
                context_parts.append(f"{i}. {status} {entry['feedback']}")
            
            context_parts.append("")
        
        # Add common rejection patterns
        if agent_name in self.rejection_patterns:
            rejections = self.rejection_patterns[agent_name]
            if rejections:
                context_parts.append(f"# Common Issues to Avoid ({agent_name.title()})")
                context_parts.append("")
                for i, rejection in enumerate(rejections[-3:], 1):  # Last 3
                    context_parts.append(f"{i}. {rejection}")
                context_parts.append("")
        
        # Add extracted preferences
        if self.user_preferences:
            context_parts.append("# User Preferences")
            context_parts.append("")
            
            if 'common_rejections' in self.user_preferences:
                stage_rejections = self.user_preferences['common_rejections'].get(agent_name, [])
                if stage_rejections:
                    context_parts.append(f"Avoid: {', '.join(stage_rejections[:5])}")
            
            if 'approved_elements' in self.user_preferences:
                context_parts.append(f"User likes: {', '.join(self.user_preferences['approved_elements'][:5])}")
            
            context_parts.append("")
        
        return '\n'.join(context_parts) if context_parts else ""
    
    def get_session_summary(self):
        """
        Get summary of current session.
        
        Returns:
            Dictionary with session statistics
        """
        return dict(self.session_stats)
    
    def _save_memory(self):
        """Save memory to disk."""
        memory_data = {
            'last_updated': datetime.now().isoformat(),
            'user_preferences': self.user_preferences,
            'feedback_history': self.feedback_history[-50:],  # Keep last 50
            'rejection_patterns': {
                k: v[-20:] for k, v in self.rejection_patterns.items()  # Keep last 20 per stage
            },
            'session_stats': dict(self.session_stats)
        }
        
        memory_file = os.path.join(self.memory_dir, 'workflow_memory.json')
        
        try:
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Failed to save memory: {e}")
    
    def _load_memory(self):
        """Load memory from disk."""
        memory_file = os.path.join(self.memory_dir, 'workflow_memory.json')
        
        if not os.path.exists(memory_file):
            return
        
        try:
            with open(memory_file, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            self.user_preferences = memory_data.get('user_preferences', {})
            self.feedback_history = memory_data.get('feedback_history', [])
            self.session_stats = defaultdict(int, memory_data.get('session_stats', {}))
            
            # Convert rejection_patterns back to defaultdict
            rejection_data = memory_data.get('rejection_patterns', {})
            self.rejection_patterns = defaultdict(list, rejection_data)
            
        except Exception as e:
            print(f"Warning: Failed to load memory: {e}")
    
    def clear_session(self):
        """Clear current session data (keeps historical learning)."""
        self.session_stats = defaultdict(int)
        self._save_memory()
    
    def reset_all(self):
        """Reset all memory (use with caution)."""
        self.user_preferences = {}
        self.feedback_history = []
        self.rejection_patterns = defaultdict(list)
        self.session_stats = defaultdict(int)
        self._save_memory()

