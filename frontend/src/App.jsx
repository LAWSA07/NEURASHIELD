import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import HomePage from './components/HomePage';
import EnhancedDashboard from './components/EnhancedDashboard';
import EnhancedDetectionModules from './components/EnhancedDetectionModules';
import MalwareTestSuite from './components/MalwareTestSuite';
import Auth from './components/Auth';
import Footer from './components/Footer';
import SimpleAlertsPage from './pages/SimpleAlertsPage';

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <div className="flex flex-col min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-gray-900">
          <Navbar />
          <main className="flex-grow px-4">
            <Routes>
              {/* Public routes */}
              <Route path="/auth" element={<Auth />} />
              
              {/* Direct alert monitoring page - no auth required */}
              <Route path="/alerts-simple" element={<SimpleAlertsPage />} />
              
              {/* Protected routes */}
              <Route path="/" element={
                <ProtectedRoute>
                  <HomePage />
                </ProtectedRoute>
              } />
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <EnhancedDashboard />
                </ProtectedRoute>
              } />
              
              {/* Enhanced Detection Modules */}
              <Route path="/detection-modules" element={
                <ProtectedRoute>
                  <EnhancedDetectionModules />
                </ProtectedRoute>
              } />
              
              {/* Malware Test Suite */}
              <Route path="/test-suite" element={
                <ProtectedRoute>
                  <MalwareTestSuite />
                </ProtectedRoute>
              } />
              
              {/* Catch-all route redirects to home */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </AuthProvider>
    </Router>
  );
};

export default App; 