import { Shield, Brain, Eye, Database, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import Layout from '@/components/Layout';

const About = () => {
  const features = [
    {
      icon: Eye,
      title: "Image Analysis",
      description: "Advanced computer vision algorithms analyze visual patterns, artifacts, and metadata to detect AI-generated images."
    },
    {
      icon: Brain,
      title: "Text Detection",
      description: "Natural language processing models examine writing patterns, coherence, and linguistic markers typical of AI-generated text."
    },
    {
      icon: Database,
      title: "Video Processing",
      description: "Frame-by-frame analysis combined with temporal consistency checks to identify AI-generated video content."
    }
  ];

  const limitations = [
    "Detection accuracy varies based on the quality and type of AI model used to generate content",
    "Newer AI models may be harder to detect as they become more sophisticated",
    "False positives and negatives are possible - use results as guidance, not absolute truth",
    "Processing time may vary depending on file size and complexity"
  ];

  return (
    <Layout>
      <div className="space-y-8 max-w-4xl mx-auto">
        {/* Hero Section */}
        <div className="text-center space-y-4 py-8">
          <div className="flex justify-center">
            <div className="p-4 bg-gradient-primary rounded-2xl shadow-custom-xl">
              <Shield size={48} className="text-primary-foreground" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-foreground">How AI Detection Works</h1>
          <p className="text-xl text-muted-foreground">
            Understanding the technology behind AI content detection
          </p>
        </div>

        {/* Introduction */}
        <Card className="shadow-custom-lg border-border/50">
          <CardContent className="p-8">
            <p className="text-lg text-foreground leading-relaxed">
              Our AI Detector uses advanced machine learning algorithms to analyze content and determine 
              whether it was created by artificial intelligence or humans. The system examines various 
              digital fingerprints, patterns, and characteristics that are typically present in AI-generated content.
            </p>
          </CardContent>
        </Card>

        {/* Features */}
        <div className="space-y-6">
          <h2 className="text-2xl font-semibold text-foreground">Detection Capabilities</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="shadow-custom-lg border-border/50 hover:shadow-custom-xl transition-all duration-300">
                <CardHeader className="text-center">
                  <div className="flex justify-center mb-4">
                    <div className="p-3 bg-primary/10 rounded-xl">
                      <feature.icon size={32} className="text-primary" />
                    </div>
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-center">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* How it Works */}
        <Card className="shadow-custom-lg border-border/50">
          <CardHeader>
            <CardTitle className="text-2xl">Detection Process</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid md:grid-cols-2 gap-8">
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-foreground">Analysis Steps</h3>
                <ol className="space-y-3">
                  <li className="flex items-start space-x-3">
                    <Badge className="bg-primary text-primary-foreground">1</Badge>
                    <span className="text-foreground">Content preprocessing and feature extraction</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <Badge className="bg-primary text-primary-foreground">2</Badge>
                    <span className="text-foreground">Pattern recognition using trained models</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <Badge className="bg-primary text-primary-foreground">3</Badge>
                    <span className="text-foreground">Confidence scoring and result classification</span>
                  </li>
                </ol>
              </div>
              
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-foreground">Result Categories</h3>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <Badge className="bg-gradient-success text-success-foreground">Real</Badge>
                    <span className="text-foreground">Likely human-generated (70%+ confidence)</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge className="bg-gradient-danger text-danger-foreground">Likely AI</Badge>
                    <span className="text-foreground">Likely AI-generated (70%+ confidence)</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Badge className="bg-neutral text-neutral-foreground">Inconclusive</Badge>
                    <span className="text-foreground">Uncertain result (&lt;70% confidence)</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Limitations */}
        <Card className="shadow-custom-lg border-border/50 border-warning/20">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-warning">
              <AlertTriangle size={24} />
              <span>Important Limitations</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {limitations.map((limitation, index) => (
                <li key={index} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-warning rounded-full mt-2 flex-shrink-0" />
                  <span className="text-foreground">{limitation}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        {/* Disclaimer */}
        <Card className="shadow-custom-lg border-border/50 bg-gradient-subtle">
          <CardContent className="p-6 text-center">
            <p className="text-foreground font-medium">
              ⚠️ <strong>Disclaimer:</strong> This tool is experimental and results may not be 100% accurate. 
              Use the results as guidance rather than definitive proof. Always verify important content through multiple sources.
            </p>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
};

export default About;