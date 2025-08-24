import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { FileText, Sparkles } from 'lucide-react';

interface TextAnalyzerProps {
  onAnalyze: (text: string) => void;
  disabled?: boolean;
}

const TextAnalyzer = ({ onAnalyze, disabled = false }: TextAnalyzerProps) => {
  const [text, setText] = useState('');

  const handleSubmit = () => {
    if (text.trim() && !disabled) {
      onAnalyze(text.trim());
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      handleSubmit();
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2 mb-4">
        <div className="p-2 bg-primary/10 rounded-lg">
          <FileText size={20} className="text-primary" />
        </div>
        <h3 className="text-lg font-semibold text-foreground">Text Analysis</h3>
      </div>
      
      <div className="relative">
        <Textarea
          placeholder="Paste your text here to check if it's AI-generated..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          className="min-h-[120px] resize-none border-border focus:border-primary focus:ring-primary/20 transition-all duration-200"
        />
        
        {text.length > 0 && (
          <div className="absolute bottom-3 right-3 text-xs text-muted-foreground">
            {text.length} characters
          </div>
        )}
      </div>
      
      <Button 
        onClick={handleSubmit}
        disabled={!text.trim() || disabled}
        className="w-full bg-gradient-primary hover:shadow-custom-lg transition-all duration-300 group"
      >
        <Sparkles size={16} className="mr-2 group-hover:animate-pulse" />
        Analyze Text
      </Button>
      
      <p className="text-xs text-muted-foreground text-center">
        Press Cmd/Ctrl + Enter to analyze quickly
      </p>
    </div>
  );
};

export default TextAnalyzer;