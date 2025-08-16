import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DreamDatabase:
    def __init__(self, db_path: str = "dreams.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create dreams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dreams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                date_recorded DATE NOT NULL,
                dream_date DATE,
                mood_before INTEGER,
                mood_after INTEGER,
                sleep_quality INTEGER,
                lucid_dream BOOLEAN DEFAULT FALSE,
                nightmare BOOLEAN DEFAULT FALSE,
                recurring BOOLEAN DEFAULT FALSE,
                tags TEXT,
                emotions TEXT,
                themes TEXT,
                people TEXT,
                locations TEXT,
                objects TEXT,
                colors TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create dream_analysis table for storing analysis results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dream_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dream_id INTEGER,
                sentiment_score REAL,
                emotion_scores TEXT,
                key_themes TEXT,
                word_frequency TEXT,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dream_id) REFERENCES dreams (id)
            )
        ''')
        
        # Create dream_statistics table for tracking patterns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dream_statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT DEFAULT 'default',
                total_dreams INTEGER DEFAULT 0,
                lucid_dreams INTEGER DEFAULT 0,
                nightmares INTEGER DEFAULT 0,
                recurring_dreams INTEGER DEFAULT 0,
                avg_mood_before REAL DEFAULT 0,
                avg_mood_after REAL DEFAULT 0,
                avg_sleep_quality REAL DEFAULT 0,
                most_common_themes TEXT,
                most_common_emotions TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_dream(self, dream_data: Dict) -> int:
        """Add a new dream entry to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO dreams (
                title, content, date_recorded, dream_date, mood_before, mood_after,
                sleep_quality, lucid_dream, nightmare, recurring, tags, emotions,
                themes, people, locations, objects, colors
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dream_data.get('title', ''),
            dream_data.get('content', ''),
            dream_data.get('date_recorded', datetime.now().date()),
            dream_data.get('dream_date', datetime.now().date()),
            dream_data.get('mood_before', 5),
            dream_data.get('mood_after', 5),
            dream_data.get('sleep_quality', 5),
            dream_data.get('lucid_dream', False),
            dream_data.get('nightmare', False),
            dream_data.get('recurring', False),
            json.dumps(dream_data.get('tags', [])),
            json.dumps(dream_data.get('emotions', [])),
            json.dumps(dream_data.get('themes', [])),
            json.dumps(dream_data.get('people', [])),
            json.dumps(dream_data.get('locations', [])),
            json.dumps(dream_data.get('objects', [])),
            json.dumps(dream_data.get('colors', []))
        ))
        
        dream_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        self.update_statistics()
        return dream_id or 0
    
    def get_dream(self, dream_id: int) -> Optional[Dict]:
        """Get a specific dream by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM dreams WHERE id = ?', (dream_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(cursor, row)
        return None
    
    def get_all_dreams(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict]:
        """Get all dreams with optional pagination"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM dreams ORDER BY date_recorded DESC, created_at DESC'
        if limit:
            query += f' LIMIT {limit} OFFSET {offset}'
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(cursor, row) for row in rows]
    
    def search_dreams(self, search_term: str, search_fields: Optional[List[str]] = None) -> List[Dict]:
        """Search dreams by content, title, or other fields"""
        if search_fields is None:
            search_fields = ['title', 'content', 'tags', 'themes', 'emotions']
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        conditions = []
        params = []
        
        for field in search_fields:
            conditions.append(f"{field} LIKE ?")
            params.append(f"%{search_term}%")
        
        query = f"SELECT * FROM dreams WHERE {' OR '.join(conditions)} ORDER BY date_recorded DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(cursor, row) for row in rows]
    
    def filter_dreams(self, filters: Dict) -> List[Dict]:
        """Filter dreams based on various criteria"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        conditions = []
        params = []
        
        if filters.get('start_date'):
            conditions.append('date_recorded >= ?')
            params.append(filters['start_date'])
        
        if filters.get('end_date'):
            conditions.append('date_recorded <= ?')
            params.append(filters['end_date'])
        
        if filters.get('lucid_dream') is not None:
            conditions.append('lucid_dream = ?')
            params.append(filters['lucid_dream'])
        
        if filters.get('nightmare') is not None:
            conditions.append('nightmare = ?')
            params.append(filters['nightmare'])
        
        if filters.get('recurring') is not None:
            conditions.append('recurring = ?')
            params.append(filters['recurring'])
        
        if filters.get('min_mood'):
            conditions.append('mood_after >= ?')
            params.append(filters['min_mood'])
        
        if filters.get('max_mood'):
            conditions.append('mood_after <= ?')
            params.append(filters['max_mood'])
        
        where_clause = ' AND '.join(conditions) if conditions else '1=1'
        query = f"SELECT * FROM dreams WHERE {where_clause} ORDER BY date_recorded DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(cursor, row) for row in rows]
    
    def update_dream(self, dream_id: int, dream_data: Dict) -> bool:
        """Update an existing dream entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build dynamic update query
        fields = []
        params = []
        
        for key, value in dream_data.items():
            if key in ['tags', 'emotions', 'themes', 'people', 'locations', 'objects', 'colors']:
                fields.append(f"{key} = ?")
                params.append(json.dumps(value))
            else:
                fields.append(f"{key} = ?")
                params.append(value)
        
        fields.append("updated_at = ?")
        params.append(datetime.now())
        params.append(dream_id)
        
        query = f"UPDATE dreams SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, params)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            self.update_statistics()
        
        return success
    
    def delete_dream(self, dream_id: int) -> bool:
        """Delete a dream entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete related analysis first
        cursor.execute('DELETE FROM dream_analysis WHERE dream_id = ?', (dream_id,))
        
        # Delete the dream
        cursor.execute('DELETE FROM dreams WHERE id = ?', (dream_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            self.update_statistics()
        
        return success
    
    def add_analysis(self, dream_id: int, analysis_data: Dict) -> int:
        """Add analysis results for a dream"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO dream_analysis (
                dream_id, sentiment_score, emotion_scores, key_themes, word_frequency
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            dream_id,
            analysis_data.get('sentiment_score', 0.0),
            json.dumps(analysis_data.get('emotion_scores', {})),
            json.dumps(analysis_data.get('key_themes', [])),
            json.dumps(analysis_data.get('word_frequency', {}))
        ))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return analysis_id or 0
    
    def get_statistics(self) -> Dict:
        """Get dream statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get basic counts
        cursor.execute('SELECT COUNT(*) FROM dreams')
        total_dreams = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM dreams WHERE lucid_dream = 1')
        lucid_dreams = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM dreams WHERE nightmare = 1')
        nightmares = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM dreams WHERE recurring = 1')
        recurring_dreams = cursor.fetchone()[0]
        
        # Get averages
        cursor.execute('SELECT AVG(mood_before), AVG(mood_after), AVG(sleep_quality) FROM dreams')
        averages = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_dreams': total_dreams,
            'lucid_dreams': lucid_dreams,
            'nightmares': nightmares,
            'recurring_dreams': recurring_dreams,
            'avg_mood_before': round(averages[0] or 0, 2),
            'avg_mood_after': round(averages[1] or 0, 2),
            'avg_sleep_quality': round(averages[2] or 0, 2)
        }
    
    def update_statistics(self):
        """Update the statistics table"""
        stats = self.get_statistics()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if statistics record exists
        cursor.execute('SELECT id FROM dream_statistics WHERE user_id = ?', ('default',))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute('''
                UPDATE dream_statistics SET
                    total_dreams = ?, lucid_dreams = ?, nightmares = ?, recurring_dreams = ?,
                    avg_mood_before = ?, avg_mood_after = ?, avg_sleep_quality = ?,
                    last_updated = ?
                WHERE user_id = ?
            ''', (
                stats['total_dreams'], stats['lucid_dreams'], stats['nightmares'],
                stats['recurring_dreams'], stats['avg_mood_before'], stats['avg_mood_after'],
                stats['avg_sleep_quality'], datetime.now(), 'default'
            ))
        else:
            cursor.execute('''
                INSERT INTO dream_statistics (
                    user_id, total_dreams, lucid_dreams, nightmares, recurring_dreams,
                    avg_mood_before, avg_mood_after, avg_sleep_quality
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                'default', stats['total_dreams'], stats['lucid_dreams'], stats['nightmares'],
                stats['recurring_dreams'], stats['avg_mood_before'], stats['avg_mood_after'],
                stats['avg_sleep_quality']
            ))
        
        conn.commit()
        conn.close()
    
    def _row_to_dict(self, cursor, row) -> Dict:
        """Convert database row to dictionary"""
        columns = [description[0] for description in cursor.description]
        result = dict(zip(columns, row))
        
        # Parse JSON fields
        json_fields = ['tags', 'emotions', 'themes', 'people', 'locations', 'objects', 'colors']
        for field in json_fields:
            if result.get(field):
                try:
                    result[field] = json.loads(result[field])
                except json.JSONDecodeError:
                    result[field] = []
            else:
                result[field] = []
        
        return result
    
    def get_dream_trends(self, days: int = 30) -> Dict:
        """Get dream trends over specified number of days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                date_recorded,
                COUNT(*) as dream_count,
                AVG(mood_after) as avg_mood,
                AVG(sleep_quality) as avg_sleep,
                SUM(CASE WHEN lucid_dream = 1 THEN 1 ELSE 0 END) as lucid_count,
                SUM(CASE WHEN nightmare = 1 THEN 1 ELSE 0 END) as nightmare_count
            FROM dreams 
            WHERE date_recorded >= date('now', '-{} days')
            GROUP BY date_recorded
            ORDER BY date_recorded
        '''.format(days))
        
        rows = cursor.fetchall()
        conn.close()
        
        return {
            'dates': [row[0] for row in rows],
            'dream_counts': [row[1] for row in rows],
            'avg_moods': [row[2] for row in rows],
            'avg_sleep': [row[3] for row in rows],
            'lucid_counts': [row[4] for row in rows],
            'nightmare_counts': [row[5] for row in rows]
        }