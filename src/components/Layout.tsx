import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, Info } from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-background">
      <nav className="sticky top-0 z-50 border-b border-border bg-card/95 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center space-x-2 group">
              <div className="p-2 bg-gradient-primary rounded-lg shadow-custom-md group-hover:shadow-custom-lg transition-all duration-300">
                <Shield size={20} className="text-primary-foreground" />
              </div>
              <span className="text-xl font-semibold text-foreground">AI Detector</span>
            </Link>
            
            <div className="flex items-center space-x-4">
              <Link 
                to="/" 
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  location.pathname === '/' 
                    ? 'bg-primary text-primary-foreground shadow-custom-md' 
                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                }`}
              >
                Detect
              </Link>
              <Link 
                to="/about" 
                className={`flex items-center space-x-1 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  location.pathname === '/about' 
                    ? 'bg-primary text-primary-foreground shadow-custom-md' 
                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                }`}
              >
                <Info size={16} />
                <span>About</span>
              </Link>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      
      <footer className="border-t border-border mt-24">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-muted-foreground">
            <p>⚠️ <strong>Disclaimer:</strong> Results are experimental and may not be 100% accurate.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;