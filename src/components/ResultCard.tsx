import { Clock, FileText, Image, Video, CheckCircle, AlertTriangle, HelpCircle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import type { AnalysisResult } from '@/types';

interface ResultCardProps {
  result: AnalysisResult;
  className?: string;
}

const ResultCard = ({ result, className = '' }: ResultCardProps) => {
  const getResultColor = (resultType: string) => {
    switch (resultType) {
      case 'Real':
        return {
          badge: 'bg-gradient-success text-success-foreground border-success/20',
          icon: CheckCircle,
          progress: 'bg-success'
        };
      case 'Likely AI':
        return {
          badge: 'bg-gradient-danger text-danger-foreground border-danger/20',
          icon: AlertTriangle,
          progress: 'bg-danger'
        };
      default:
        return {
          badge: 'bg-neutral text-neutral-foreground border-neutral/20',
          icon: HelpCircle,
          progress: 'bg-neutral'
        };
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'image':
        return <Image size={16} />;
      case 'video':
        return <Video size={16} />;
      case 'text':
        return <FileText size={16} />;
      default:
        return <FileText size={16} />;
    }
  };

  const getResultDisplay = (resultType: string) => {
    switch (resultType) {
      case 'Real':
        return 'Looks Real ✅';
      case 'Likely AI':
        return 'Looks AI 🤖';
      case 'Inconclusive':
        return 'Not Sure ❓';
      default:
        return resultType;
    }
  };

  const getTypeDisplay = (type: string) => {
    switch (type) {
      case 'image':
        return 'Image';
      case 'video':
        return 'Video';
      case 'text':
        return 'Text';
      default:
        return type;
    }
  };

  const colors = getResultColor(result.result);
  const ResultIcon = colors.icon;

  return (
    <Card className={`shadow-custom-lg hover:shadow-custom-xl transition-all duration-300 border-border/50 ${className}`}>
      <CardContent className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-2">
            <div className="p-2 bg-secondary rounded-lg">
              {getTypeIcon(result.type)}
            </div>
            <div>
              <h3 className="font-semibold text-foreground">{getTypeDisplay(result.type)} Analysis</h3>
              <p className="text-sm text-muted-foreground">
                {result.filename || (result.textPreview && `"${result.textPreview.slice(0, 50)}..."`)}
              </p>
            </div>
          </div>
          
          <Badge className={`${colors.badge} shadow-custom-sm flex items-center space-x-1`}>
            <ResultIcon size={14} />
            <span>{getResultDisplay(result.result)}</span>
          </Badge>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-foreground">How sure we are:</span>
            <span className="text-sm font-semibold text-foreground">{result.confidence}%</span>
          </div>
          
          <Progress 
            value={result.confidence} 
            className="h-2"
          />
          
          <div className="flex items-center space-x-1 text-xs text-muted-foreground">
            <Clock size={12} />
            <span>Checked on: {result.timestamp.toLocaleString()}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ResultCard;