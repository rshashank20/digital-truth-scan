import { useCallback, useState } from 'react';
import { Upload, File, Image, Video } from 'lucide-react';
import { cn } from '@/lib/utils';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  accept?: string;
  disabled?: boolean;
}

const FileUpload = ({ onFileSelect, accept = "image/*,video/*", disabled = false }: FileUploadProps) => {
  const [isDragOver, setIsDragOver] = useState(false);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    
    if (disabled) return;

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      onFileSelect(files[0]);
    }
  }, [onFileSelect, disabled]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!disabled) {
      setIsDragOver(true);
    }
  }, [disabled]);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      onFileSelect(files[0]);
    }
  }, [onFileSelect]);

  const getFileIcon = () => {
    if (accept.includes('image')) return <Image size={32} className="text-primary" />;
    if (accept.includes('video')) return <Video size={32} className="text-primary" />;
    return <File size={32} className="text-primary" />;
  };

  return (
    <div
      className={cn(
        "relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 cursor-pointer group",
        isDragOver 
          ? "border-primary bg-primary/5 shadow-custom-lg scale-[1.02]" 
          : "border-border hover:border-primary/50 hover:bg-primary/5",
        disabled && "opacity-50 cursor-not-allowed"
      )}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onClick={() => !disabled && document.getElementById('file-input')?.click()}
    >
      <input
        id="file-input"
        type="file"
        accept={accept}
        onChange={handleFileInput}
        className="hidden"
        disabled={disabled}
      />
      
      <div className="flex flex-col items-center space-y-4">
        <div className={cn(
          "p-4 rounded-full transition-all duration-300",
          isDragOver ? "bg-primary shadow-custom-md" : "bg-primary/10 group-hover:bg-primary/20"
        )}>
          {isDragOver ? (
            <Upload size={32} className="text-primary-foreground" />
          ) : (
            getFileIcon()
          )}
        </div>
        
        <div className="space-y-2">
          <p className="text-lg font-medium text-foreground">
            {isDragOver ? "Drop your file here" : "Upload a file"}
          </p>
          <p className="text-sm text-muted-foreground">
            Drag & drop or click to browse
          </p>
          <p className="text-xs text-muted-foreground">
            Supports images and videos (max 10MB)
          </p>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;