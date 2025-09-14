import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { FiMenu, FiX, FiShield } from 'react-icons/fi';

const Navbar = () => {
  const { user, signOut } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 w-full px-8 py-4 flex justify-between items-center z-50 glass-red border-b border-red-primary/30">
      {/* Logo */}
      <Link to="/" className="flex items-center">
        <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center mr-2 glow-red">
          <FiShield className="text-white text-xl" />
        </div>
        <span className="text-white font-semibold text-2xl ml-2">EdgeSentinel</span>
      </Link>
      
      {/* Desktop Navigation */}
      <div className="hidden md:flex items-center gap-8">
        <Link to="/" className="text-white hover:text-red-primary transition-colors">
          Home
        </Link>
        <Link to="/dashboard" className="text-white hover:text-red-primary transition-colors">
          Dashboard
        </Link>
        <Link to="/detection-modules" className="text-white hover:text-red-primary transition-colors">
          Detection Modules
        </Link>
        <Link to="/test-suite" className="text-white hover:text-red-primary transition-colors">
          Test Suite
        </Link>

        {user ? (
          <button
            onClick={signOut}
            className="ml-4 btn-red-outline px-4 py-2"
          >
            Sign Out
          </button>
        ) : (
          <Link
            to="/auth"
            className="ml-4 btn-red-primary px-4 py-2"
          >
            Try Now
          </Link>
        )}
      </div>
      
      {/* Mobile menu button */}
      <button 
        className="md:hidden text-white"
        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
      >
        {mobileMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
      </button>
      
      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden absolute top-16 left-0 right-0 glass-red border-b border-red-primary/30 py-4 px-8">
          <div className="flex flex-col gap-4">
            <Link 
              to="/" 
              className="text-white hover:text-red-primary transition-colors py-2"
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link 
              to="/dashboard" 
              className="text-white hover:text-red-primary transition-colors py-2"
              onClick={() => setMobileMenuOpen(false)}
            >
              Dashboard
            </Link>
            <Link 
              to="/detection-modules" 
              className="text-white hover:text-red-primary transition-colors py-2"
              onClick={() => setMobileMenuOpen(false)}
            >
              Detection Modules
            </Link>
            <Link 
              to="/test-suite" 
              className="text-white hover:text-red-primary transition-colors py-2"
              onClick={() => setMobileMenuOpen(false)}
            >
              Test Suite
            </Link>
            
            {user ? (
              <button
                onClick={() => {
                  signOut();
                  setMobileMenuOpen(false);
                }}
                className="mt-2 btn-red-outline px-4 py-2"
              >
                Sign Out
              </button>
            ) : (
              <Link
                to="/auth"
                className="mt-2 btn-red-outline px-4 py-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                Try Now
              </Link>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar; 