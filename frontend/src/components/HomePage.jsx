import React, { Suspense } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { FiShield } from 'react-icons/fi';

// Spline is imported conditionally to prevent issues if the package isn't installed
let Spline;
try {
  Spline = React.lazy(() => import('@splinetool/react-spline'));
} catch (err) {
  console.warn('Spline package not found. Using fallback background.');
}

const FloatingWord = ({ word, initialX, initialY }) => {
  // Generate random positions across the entire viewport
  const randomPosition = () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    scale: Math.random() * 0.5 + 0.5, // Random size between 0.5 and 1
    opacity: Math.random() * 0.15 + 0.05 // Random opacity between 0.05 and 0.2
  });

  // Generate 5 random positions for the animation path
  const positions = Array.from({ length: 5 }, randomPosition);
  
  return (
    <motion.div
      className="fixed text-white font-medium pointer-events-none select-none"
      style={{
        fontSize: `${Math.random() * 1.5 + 1.5}rem`, // Random size between 1.5rem and 3rem (25% smaller)
      }}
      initial={{
        x: positions[0].x,
        y: positions[0].y,
        scale: positions[0].scale,
        opacity: positions[0].opacity
      }}
      animate={{
        x: positions.map(p => p.x),
        y: positions.map(p => p.y),
        scale: positions.map(p => p.scale),
        opacity: positions.map(p => p.opacity),
        rotate: [0, 45, -45, 20, 0],
      }}
      transition={{
        duration: Math.random() * 20 + 25, // Random duration between 25-45 seconds
        repeat: Infinity,
        repeatType: "reverse",
        ease: "linear"
      }}
    >
      {word}
    </motion.div>
  );
};

const FloatingWordsLayer = () => {
  const words = [
    "FAKE", "REAL", "100%", "20%", "AI", "DEEP",
    "TRUE", "FALSE", "DETECT", "SCAN", "CHECK", "VERIFY",
    "ML", "ANALYSIS", "NEURAL", "GAN", "SYNTHETIC", "AUTHENTIC",
    "DIGITAL", "CYBER", "SECURITY", "ALERT", "DETECTION", "DATA"
  ];

  return (
    <div className="fixed inset-0 z-[5] overflow-hidden">
      {words.map((word, index) => (
        <FloatingWord
          key={index}
          word={word}
          initialX={Math.random() * window.innerWidth}
          initialY={Math.random() * window.innerHeight}
        />
      ))}
    </div>
  );
};

const SplineLoader = () => (
  <div className="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm z-50">
    <div className="text-2xl text-white">Loading 3D Scene...</div>
  </div>
);

const HomePage = () => {
  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-x-hidden pt-16">
      {/* Spline Background */}
      {Spline && (
        <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-screen h-screen pointer-events-none z-[1]">
          <Suspense fallback={<SplineLoader />}>
            <Spline scene="https://prod.spline.design/U1tyedoZPBALOQFo/scene.splinecode" />
          </Suspense>
        </div>
      )}

      {/* Floating Words Layer */}
      <FloatingWordsLayer />

      {/* Main Content */}
      <div className="relative z-10">
        {/* Hero Section */}
        <section className="min-h-screen flex items-center justify-center px-6 md:px-12">
          <div className="max-w-[1800px] w-full mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-center md:text-left"
            >
              <h1 className="text-6xl md:text-8xl lg:text-[9rem] xl:text-[11rem] leading-[0.9] tracking-tight text-white mb-6 uppercase font-bold">
                EDGE
                <br />
                <span className="text-red-500">SENTINEL</span>
              </h1>
              <p className="text-xl md:text-2xl mb-8 text-gray-300">
                Advanced Cybersecurity Threat Detection
              </p>
              <div className="flex flex-col md:flex-row items-center md:items-start gap-8 justify-center md:justify-start">
                <Link 
                  to="/auth" 
                  className="btn-red-primary text-lg px-8 py-4"
                >
                  Try Now
                </Link>
                <Link 
                  to="/dashboard" 
                  className="btn-red-outline text-lg px-8 py-4"
                >
                  Enhanced Dashboard
                </Link>
                <div className="text-white/70 text-base font-light tracking-wide">
                  AI-powered threat detection system
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 px-6 md:px-12">
          <div className="max-w-6xl mx-auto">
            <motion.h2 
              className="text-4xl font-bold mb-16 text-center text-white"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
            >
              Advanced Detection Features
            </motion.h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  className="card card-hover"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  viewport={{ once: true }}
                  whileHover={{ y: -5, transition: { duration: 0.2 } }}
                >
                  <h3 className="text-xl font-semibold mb-4 text-white">{feature.title}</h3>
                  <p className="text-gray-400">{feature.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-20 px-6 md:px-12">
          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <motion.div
                className="text-center"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
              >
                <div className="text-4xl font-bold text-white mb-2">95%</div>
                <div className="text-gray-400">Detection Accuracy</div>
              </motion.div>
              <motion.div
                className="text-center"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.1 }}
              >
                <div className="text-4xl font-bold text-white mb-2">&lt;1s</div>
                <div className="text-gray-400">Response Time</div>
              </motion.div>
              <motion.div
                className="text-center"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2 }}
              >
                <div className="text-4xl font-bold text-white mb-2">24/7</div>
                <div className="text-gray-400">Monitoring</div>
              </motion.div>
              <motion.div
                className="text-center"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.3 }}
              >
                <div className="text-4xl font-bold text-white mb-2">5+</div>
                <div className="text-gray-400">Detection Methods</div>
              </motion.div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

const features = [
  {
    title: "High Accuracy Detection",
    description: "Our advanced AI algorithms can detect even the most sophisticated cybersecurity threats with an accuracy of over 95%."
  },
  {
    title: "Rapid Analysis",
    description: "Get results within seconds, allowing you to quickly identify and respond to potential threats."
  },
  {
    title: "Multi-Model Approach",
    description: "We use multiple detection models to cross-verify results, reducing false positives."
  },
  {
    title: "Continuous Learning",
    description: "Our system continuously learns from new threat techniques to stay ahead of malicious actors."
  },
  {
    title: "Detailed Reports",
    description: "Receive comprehensive reports on detected threats with detailed technical information."
  },
  {
    title: "Privacy Focused",
    description: "All network traffic is processed securely and analyzed with privacy in mind."
  }
];

export default HomePage; 