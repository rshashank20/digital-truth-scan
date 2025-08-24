import { useState, useEffect } from 'react';
import type { AnalysisResult } from '@/types';

const STORAGE_KEY = 'ai-detector-history';

export const useHistory = () => {
  const [history, setHistory] = useState<AnalysisResult[]>([]);

  useEffect(() => {
    const savedHistory = localStorage.getItem(STORAGE_KEY);
    if (savedHistory) {
      try {
        const parsed = JSON.parse(savedHistory);
        // Convert timestamp strings back to Date objects
        const historyWithDates = parsed.map((item: any) => ({
          ...item,
          timestamp: new Date(item.timestamp)
        }));
        setHistory(historyWithDates);
      } catch (error) {
        console.error('Error parsing history from localStorage:', error);
      }
    }
  }, []);

  const addToHistory = (result: AnalysisResult) => {
    const newHistory = [result, ...history].slice(0, 50); // Keep only last 50 results
    setHistory(newHistory);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newHistory));
  };

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  return { history, addToHistory, clearHistory };
};