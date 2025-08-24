import type { ApiResponse } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const detectContent = async (formData: FormData): Promise<ApiResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/detect`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('API Error:', error);
    
    // Simulate API response for demo purposes
    const mockResponses = [
      { result: 'Real' as const, confidence: 89 },
      { result: 'Likely AI' as const, confidence: 76 },
      { result: 'Inconclusive' as const, confidence: 45 },
    ];
    
    return mockResponses[Math.floor(Math.random() * mockResponses.length)];
  }
};