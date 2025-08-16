import re
from typing import Dict, List, Tuple
from collections import Counter
import json

# Try to import TextBlob, but provide fallback if it fails
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("TextBlob not available. Some analysis features will be limited.")

class DreamAnalyzer:
    def __init__(self):
        # Common dream themes and their keywords
        self.theme_keywords = {
            'flying': ['fly', 'flying', 'soar', 'float', 'levitate', 'airborne', 'wings'],
            'falling': ['fall', 'falling', 'drop', 'plummet', 'tumble', 'slip'],
            'chase': ['chase', 'chased', 'run', 'running', 'escape', 'pursue', 'hunt'],
            'water': ['water', 'ocean', 'sea', 'river', 'lake', 'pool', 'swim', 'drown', 'flood'],
            'death': ['death', 'die', 'dead', 'dying', 'funeral', 'grave', 'cemetery'],
            'animals': ['dog', 'cat', 'bird', 'snake', 'spider', 'lion', 'tiger', 'bear', 'wolf'],
            'school': ['school', 'classroom', 'teacher', 'student', 'exam', 'test', 'homework'],
            'work': ['work', 'office', 'boss', 'colleague', 'meeting', 'job', 'career'],
            'family': ['mother', 'father', 'mom', 'dad', 'sister', 'brother', 'family', 'parent'],
            'friends': ['friend', 'friends', 'buddy', 'pal', 'companion'],
            'love': ['love', 'romance', 'kiss', 'hug', 'relationship', 'partner', 'boyfriend', 'girlfriend'],
            'house': ['house', 'home', 'room', 'bedroom', 'kitchen', 'bathroom', 'door', 'window'],
            'travel': ['travel', 'trip', 'journey', 'vacation', 'car', 'plane', 'train', 'bus'],
            'food': ['food', 'eat', 'eating', 'hungry', 'meal', 'restaurant', 'cook', 'cooking'],
            'money': ['money', 'rich', 'poor', 'buy', 'sell', 'expensive', 'cheap', 'bank'],
            'nature': ['tree', 'forest', 'mountain', 'sky', 'sun', 'moon', 'star', 'flower', 'garden'],
            'technology': ['phone', 'computer', 'internet', 'email', 'text', 'social media', 'app'],
            'supernatural': ['ghost', 'spirit', 'magic', 'witch', 'demon', 'angel', 'supernatural', 'paranormal']
        }
        
        # Emotion keywords for sentiment analysis
        self.emotion_keywords = {
            'fear': ['afraid', 'scared', 'terrified', 'frightened', 'anxious', 'worried', 'panic', 'horror'],
            'joy': ['happy', 'joyful', 'excited', 'cheerful', 'delighted', 'pleased', 'glad', 'elated'],
            'sadness': ['sad', 'depressed', 'melancholy', 'gloomy', 'sorrowful', 'grief', 'crying', 'tears'],
            'anger': ['angry', 'mad', 'furious', 'rage', 'irritated', 'annoyed', 'frustrated', 'hostile'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned', 'bewildered'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'sickened', 'nauseated'],
            'love': ['love', 'affection', 'adoration', 'fondness', 'caring', 'tender'],
            'confusion': ['confused', 'puzzled', 'perplexed', 'bewildered', 'lost', 'uncertain'],
            'peace': ['peaceful', 'calm', 'serene', 'tranquil', 'relaxed', 'content'],
            'excitement': ['excited', 'thrilled', 'energetic', 'enthusiastic', 'eager']
        }
        
        # Color keywords
        self.color_keywords = [
            'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'black', 'white',
            'gray', 'grey', 'brown', 'violet', 'indigo', 'turquoise', 'gold', 'silver',
            'crimson', 'scarlet', 'azure', 'emerald', 'amber', 'magenta', 'cyan'
        ]
        
        # People keywords
        self.people_keywords = [
            'person', 'people', 'man', 'woman', 'child', 'baby', 'stranger', 'crowd',
            'mother', 'father', 'mom', 'dad', 'sister', 'brother', 'friend', 'teacher',
            'doctor', 'police', 'celebrity', 'boss', 'colleague', 'neighbor'
        ]
        
        # Location keywords
        self.location_keywords = [
            'house', 'home', 'school', 'office', 'hospital', 'store', 'restaurant',
            'park', 'beach', 'mountain', 'forest', 'city', 'town', 'village',
            'street', 'road', 'bridge', 'building', 'room', 'bedroom', 'kitchen',
            'bathroom', 'garden', 'yard', 'basement', 'attic'
        ]

    def analyze_dream(self, dream_content: str, dream_title: str = "") -> Dict:
        """Perform comprehensive analysis of dream content"""
        full_text = f"{dream_title} {dream_content}".lower()
        
        analysis = {
            'sentiment_analysis': self._analyze_sentiment(full_text),
            'emotion_analysis': self._analyze_emotions(full_text),
            'theme_analysis': self._analyze_themes(full_text),
            'entity_extraction': self._extract_entities(full_text),
            'word_frequency': self._get_word_frequency(full_text),
            'dream_characteristics': self._analyze_characteristics(full_text),
            'complexity_score': self._calculate_complexity(dream_content)
        }
        
        return analysis

    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze overall sentiment of the dream"""
        # Use fallback sentiment analysis for reliability
        return self._fallback_sentiment_analysis(text)
    
    def _fallback_sentiment_analysis(self, text: str) -> Dict:
        """Fallback sentiment analysis using keyword matching"""
        positive_words = ['happy', 'joy', 'love', 'beautiful', 'amazing', 'wonderful', 'peaceful', 'excited', 'good', 'great']
        negative_words = ['sad', 'fear', 'scary', 'terrible', 'awful', 'bad', 'horrible', 'nightmare', 'terrified', 'angry']
        
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            polarity = 0.0
            sentiment_label = "Neutral"
        else:
            polarity = (positive_count - negative_count) / len(words)
            if polarity > 0.05:
                sentiment_label = "Positive"
            elif polarity < -0.05:
                sentiment_label = "Negative"
            else:
                sentiment_label = "Neutral"
        
        return {
            'polarity': round(polarity, 3),
            'subjectivity': 0.5,  # Default subjectivity
            'label': sentiment_label,
            'confidence': abs(polarity)
        }

    def _analyze_emotions(self, text: str) -> Dict:
        """Detect emotions present in the dream"""
        emotion_scores = {}
        words = text.split()
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            matches = []
            for keyword in keywords:
                count = text.count(keyword)
                if count > 0:
                    score += count
                    matches.extend([keyword] * count)
            
            if score > 0:
                emotion_scores[emotion] = {
                    'score': score,
                    'intensity': min(score / len(words) * 100, 10),  # Normalize to 0-10
                    'keywords_found': list(set(matches))
                }
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores.keys(), key=lambda x: emotion_scores[x]['score']) if emotion_scores else None
        
        return {
            'emotions_detected': emotion_scores,
            'dominant_emotion': dominant_emotion,
            'emotional_complexity': len(emotion_scores)
        }

    def _analyze_themes(self, text: str) -> Dict:
        """Identify themes present in the dream"""
        theme_scores = {}
        
        for theme, keywords in self.theme_keywords.items():
            score = 0
            matches = []
            for keyword in keywords:
                count = text.count(keyword)
                if count > 0:
                    score += count
                    matches.extend([keyword] * count)
            
            if score > 0:
                theme_scores[theme] = {
                    'score': score,
                    'keywords_found': list(set(matches)),
                    'relevance': min(score * 2, 10)  # Scale to 0-10
                }
        
        # Sort themes by relevance
        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        return {
            'themes_detected': theme_scores,
            'primary_themes': [theme for theme, data in sorted_themes[:3]],
            'theme_diversity': len(theme_scores)
        }

    def _extract_entities(self, text: str) -> Dict:
        """Extract people, places, colors, and objects from dream"""
        entities = {
            'colors': [],
            'people': [],
            'locations': [],
            'objects': []
        }
        
        # Extract colors
        for color in self.color_keywords:
            if color in text:
                entities['colors'].append(color)
        
        # Extract people
        for person in self.people_keywords:
            if person in text:
                entities['people'].append(person)
        
        # Extract locations
        for location in self.location_keywords:
            if location in text:
                entities['locations'].append(location)
        
        # Extract objects using fallback method for reliability
        entities['objects'] = self._fallback_object_extraction(text, entities)
        
        return entities
    
    def _fallback_object_extraction(self, text: str, entities: Dict) -> List[str]:
        """Fallback object extraction using common nouns"""
        common_objects = [
            'car', 'house', 'door', 'window', 'phone', 'computer', 'book', 'table', 'chair',
            'bed', 'mirror', 'key', 'bag', 'clothes', 'shoes', 'food', 'water', 'fire',
            'light', 'shadow', 'stairs', 'elevator', 'bridge', 'tree', 'flower', 'animal'
        ]
        
        found_objects = []
        all_entity_words = set(entities['colors'] + entities['people'] + entities['locations'])
        
        for obj in common_objects:
            if obj in text and obj not in all_entity_words:
                found_objects.append(obj)
        
        return found_objects[:10]

    def _get_word_frequency(self, text: str) -> Dict:
        """Get frequency of significant words"""
        # Remove common stop words
        stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
            'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
            'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once'
        }
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        filtered_words = [word for word in words if word not in stop_words]
        
        word_freq = Counter(filtered_words)
        return dict(word_freq.most_common(20))

    def _analyze_characteristics(self, text: str) -> Dict:
        """Analyze dream characteristics like lucidity indicators, nightmare elements"""
        characteristics = {
            'lucidity_indicators': 0,
            'nightmare_indicators': 0,
            'recurring_indicators': 0,
            'symbolic_content': 0
        }
        
        # Lucidity indicators
        lucid_keywords = ['realize', 'realized', 'aware', 'control', 'lucid', 'conscious', 'know i was dreaming']
        for keyword in lucid_keywords:
            if keyword in text:
                characteristics['lucidity_indicators'] += text.count(keyword)
        
        # Nightmare indicators
        nightmare_keywords = ['nightmare', 'terrifying', 'scary', 'frightening', 'horror', 'panic', 'scream']
        for keyword in nightmare_keywords:
            if keyword in text:
                characteristics['nightmare_indicators'] += text.count(keyword)
        
        # Recurring indicators
        recurring_keywords = ['again', 'same', 'recurring', 'repeat', 'familiar', 'before']
        for keyword in recurring_keywords:
            if keyword in text:
                characteristics['recurring_indicators'] += text.count(keyword)
        
        # Symbolic content (abstract concepts)
        symbolic_keywords = ['symbol', 'meaning', 'represent', 'metaphor', 'spiritual', 'mystical']
        for keyword in symbolic_keywords:
            if keyword in text:
                characteristics['symbolic_content'] += text.count(keyword)
        
        return characteristics

    def _calculate_complexity(self, text: str) -> Dict:
        """Calculate dream complexity based on various factors"""
        words = text.split()
        word_count = len(words)
        
        # Simple sentence counting using punctuation
        sentence_count = len(re.findall(r'[.!?]+', text))
        sentence_count = max(sentence_count, 1)  # Avoid division by zero
        avg_sentence_length = word_count / sentence_count
        
        # Vocabulary diversity (unique words / total words)
        unique_words = len(set(word.lower() for word in words))
        vocabulary_diversity = unique_words / word_count if word_count > 0 else 0
        
        # Calculate overall complexity score (0-10)
        complexity_factors = [
            min(word_count / 100, 3),  # Length factor (max 3 points)
            min(vocabulary_diversity * 10, 3),  # Diversity factor (max 3 points)
            min(avg_sentence_length / 10, 2),  # Sentence complexity (max 2 points)
            min(len(self._extract_entities(text.lower())['objects']) / 5, 2)  # Entity richness (max 2 points)
        ]
        
        complexity_score = sum(complexity_factors)
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': round(avg_sentence_length, 2),
            'vocabulary_diversity': round(vocabulary_diversity, 3),
            'complexity_score': round(complexity_score, 2),
            'complexity_level': self._get_complexity_level(complexity_score)
        }

    def _get_complexity_level(self, score: float) -> str:
        """Convert complexity score to descriptive level"""
        if score >= 8:
            return "Very Complex"
        elif score >= 6:
            return "Complex"
        elif score >= 4:
            return "Moderate"
        elif score >= 2:
            return "Simple"
        else:
            return "Very Simple"

    def generate_insights(self, analysis: Dict) -> List[str]:
        """Generate human-readable insights from analysis"""
        insights = []
        
        # Sentiment insights
        sentiment = analysis['sentiment_analysis']
        if sentiment['label'] == 'Positive':
            insights.append(f"This dream has a positive emotional tone (polarity: {sentiment['polarity']})")
        elif sentiment['label'] == 'Negative':
            insights.append(f"This dream has a negative emotional tone (polarity: {sentiment['polarity']})")
        
        # Emotion insights
        emotions = analysis['emotion_analysis']
        if emotions['dominant_emotion']:
            insights.append(f"The dominant emotion in this dream is {emotions['dominant_emotion']}")
        
        if emotions['emotional_complexity'] > 3:
            insights.append("This dream shows high emotional complexity with multiple emotions present")
        
        # Theme insights
        themes = analysis['theme_analysis']
        if themes['primary_themes']:
            primary_theme = themes['primary_themes'][0]
            insights.append(f"The primary theme of this dream is '{primary_theme}'")
        
        # Complexity insights
        complexity = analysis['complexity_score']
        insights.append(f"Dream complexity level: {complexity['complexity_level']}")
        
        # Characteristic insights
        chars = analysis['dream_characteristics']
        if chars['lucidity_indicators'] > 0:
            insights.append("This dream shows signs of lucidity or self-awareness")
        
        if chars['nightmare_indicators'] > 2:
            insights.append("This dream contains nightmare elements")
        
        if chars['recurring_indicators'] > 1:
            insights.append("This dream may be part of a recurring pattern")
        
        return insights

    def compare_dreams(self, dream1_analysis: Dict, dream2_analysis: Dict) -> Dict:
        """Compare two dream analyses"""
        comparison = {
            'sentiment_similarity': 0,
            'theme_overlap': [],
            'emotion_overlap': [],
            'complexity_difference': 0,
            'similarity_score': 0
        }
        
        # Sentiment similarity
        sent1 = dream1_analysis['sentiment_analysis']['polarity']
        sent2 = dream2_analysis['sentiment_analysis']['polarity']
        comparison['sentiment_similarity'] = 1 - abs(sent1 - sent2) / 2
        
        # Theme overlap
        themes1 = set(dream1_analysis['theme_analysis']['themes_detected'].keys())
        themes2 = set(dream2_analysis['theme_analysis']['themes_detected'].keys())
        comparison['theme_overlap'] = list(themes1.intersection(themes2))
        
        # Emotion overlap
        emotions1 = set(dream1_analysis['emotion_analysis']['emotions_detected'].keys())
        emotions2 = set(dream2_analysis['emotion_analysis']['emotions_detected'].keys())
        comparison['emotion_overlap'] = list(emotions1.intersection(emotions2))
        
        # Complexity difference
        comp1 = dream1_analysis['complexity_score']['complexity_score']
        comp2 = dream2_analysis['complexity_score']['complexity_score']
        comparison['complexity_difference'] = abs(comp1 - comp2)
        
        # Overall similarity score
        theme_sim = len(comparison['theme_overlap']) / max(len(themes1.union(themes2)), 1)
        emotion_sim = len(comparison['emotion_overlap']) / max(len(emotions1.union(emotions2)), 1)
        complexity_sim = 1 - comparison['complexity_difference'] / 10
        
        comparison['similarity_score'] = (
            comparison['sentiment_similarity'] * 0.3 +
            theme_sim * 0.4 +
            emotion_sim * 0.2 +
            complexity_sim * 0.1
        )
        
        return comparison