import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Cpu, LogIn, LayoutDashboard } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Button } from './Button';

export const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200/80 bg-white/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-brand-600 to-purple-600 text-white shadow-md group-hover:shadow-lg transition-all">
            <Cpu className="w-5 h-5" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-extrabold tracking-tight bg-gradient-to-r from-slate-950 via-slate-900 to-brand-700 bg-clip-text text-transparent">
              QuantumCare
            </span>
            <span className="text-[10px] uppercase tracking-wider font-semibold text-brand-600 -mt-1">
              Hybrid QML Platform
            </span>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
          <Link to="/" className="hover:text-brand-600 transition-colors">Home</Link>
          <a href="#problem" className="hover:text-brand-600 transition-colors">Features</a>
          <a href="#solution" className="hover:text-brand-600 transition-colors">Architecture</a>
          <a href="#how-it-works" className="hover:text-brand-600 transition-colors">How It Works</a>
        </nav>

        {/* Action Buttons */}
        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <div className="flex items-center gap-3">
              <Button
                variant="primary"
                size="sm"
                icon={LayoutDashboard}
                onClick={() => navigate('/dashboard')}
              >
                Dashboard
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={logout}
              >
                Sign Out
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                icon={LogIn}
                onClick={() => navigate('/login')}
              >
                Sign In
              </Button>
              <Button
                variant="quantum"
                size="sm"
                onClick={() => navigate('/register')}
              >
                Get Started
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
