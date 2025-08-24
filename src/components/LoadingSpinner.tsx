import { Loader2, Shield } from 'lucide-react';

interface LoadingSpinnerProps {
  message?: string;
}

const LoadingSpinner = ({ message = "Analyzing content..." }: LoadingSpinnerProps) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-primary rounded-full opacity-20 animate-ping"></div>
        <div className="relative p-4 bg-gradient-primary rounded-full shadow-custom-lg">
          <Shield size={24} className="text-primary-foreground" />
        </div>
      </div>
      
      <div className="flex items-center space-x-2">
        <Loader2 size={16} className="animate-spin text-primary" />
        <span className="text-sm font-medium text-foreground">{message}</span>
      </div>
      
      <div className="w-48 h-1 bg-secondary rounded-full overflow-hidden">
        <div className="h-full bg-gradient-primary rounded-full animate-pulse"></div>
      </div>
    </div>
  );
};

export default LoadingSpinner;