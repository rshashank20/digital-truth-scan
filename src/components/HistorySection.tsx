import { useState } from 'react';
import { History, Trash2, ChevronDown, ChevronUp } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import ResultCard from './ResultCard';
import type { AnalysisResult } from '@/types';

interface HistorySectionProps {
  history: AnalysisResult[];
  onClearHistory: () => void;
}

const HistorySection = ({ history, onClearHistory }: HistorySectionProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  if (history.length === 0) return null;

  const displayHistory = isExpanded ? history : history.slice(0, 3);

  return (
    <Card className="shadow-custom-lg border-border/50">
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="p-2 bg-primary/10 rounded-lg">
              <History size={20} className="text-primary" />
            </div>
            <CardTitle className="text-lg">Analysis History</CardTitle>
            <Badge variant="secondary" className="ml-2">
              {history.length}
            </Badge>
          </div>
          
          <Button 
            variant="outline" 
            size="sm" 
            onClick={onClearHistory}
            className="text-destructive hover:text-destructive hover:bg-destructive/10"
          >
            <Trash2 size={14} className="mr-1" />
            Clear
          </Button>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        <div className="space-y-3">
          {displayHistory.map((result, index) => (
            <ResultCard key={result.id} result={result} className="shadow-custom-md" />
          ))}
        </div>
        
        {history.length > 3 && (
          <Button
            variant="outline"
            onClick={() => setIsExpanded(!isExpanded)}
            className="w-full"
          >
            {isExpanded ? (
              <>
                <ChevronUp size={16} className="mr-2" />
                Show Less
              </>
            ) : (
              <>
                <ChevronDown size={16} className="mr-2" />
                Show {history.length - 3} More
              </>
            )}
          </Button>
        )}
      </CardContent>
    </Card>
  );
};

export default HistorySection;