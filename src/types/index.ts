export type DetectionResult = 'Real' | 'Likely AI' | 'Inconclusive';

export type ContentType = 'image' | 'video' | 'text';

export interface AnalysisResult {
  id: string;
  type: ContentType;
  result: DetectionResult;
  confidence: number;
  timestamp: Date;
  filename?: string;
  textPreview?: string;
}

export interface ApiResponse {
  result: DetectionResult;
  confidence: number;
}

export interface HistoryItem extends AnalysisResult {
  // Additional fields for history display if needed
}