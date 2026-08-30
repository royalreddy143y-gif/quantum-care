import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Cpu, Lock, Mail, ArrowRight, AlertCircle, CheckCircle2, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/Button';

export const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(true);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  // Preload saved credentials from localStorage
  useEffect(() => {
    const savedEmail = localStorage.getItem('quantumcare_saved_email');
    const savedPassword = localStorage.getItem('quantumcare_saved_password');
    if (savedEmail) {
      setEmail(savedEmail);
    }
    if (savedPassword) {
      setPassword(savedPassword);
    }
  }, []);

  const handleFillDemo = () => {
    setEmail('demo@quantumcare.org');
    setPassword('QuantumCare2025!');
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const emailClean = email.trim().toLowerCase();
    
    if (!emailClean || !password) {
      setError('Please enter your email and password.');
      return;
    }

    setLoading(true);
    try {
      await login(emailClean, password);
      
      // Store credentials if remember me is enabled
      if (rememberMe) {
        localStorage.setItem('quantumcare_saved_email', emailClean);
        localStorage.setItem('quantumcare_saved_password', password);
      } else {
        localStorage.removeItem('quantumcare_saved_email');
        localStorage.removeItem('quantumcare_saved_password');
      }

      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Incorrect email or password. Please verify your credentials or use the demo account.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-slate-50">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Link to="/" className="inline-flex items-center gap-2 mb-4">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-brand-600 to-purple-600 text-white shadow-md">
            <Cpu className="w-6 h-6" />
          </div>
          <span className="text-2xl font-black text-slate-900 tracking-tight">QuantumCare</span>
        </Link>
        <h2 className="text-2xl font-bold text-slate-900">Sign In</h2>
        <p className="mt-1 text-xs text-slate-500">
          Enter your credentials to access the quantum diagnostic suite
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md px-4">
        <div className="bg-white py-8 px-6 shadow-xl shadow-slate-200/50 rounded-2xl border border-slate-100 sm:px-10 space-y-6">
          
          {/* Quick Demo Fill Banner */}
          <div className="p-3 bg-brand-50 border border-brand-200/60 rounded-xl flex items-center justify-between text-brand-900 text-xs">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-brand-600 flex-shrink-0" />
              <span>Testing the platform?</span>
            </div>
            <button
              type="button"
              onClick={handleFillDemo}
              className="px-2.5 py-1 text-xs font-semibold bg-brand-600 hover:bg-brand-700 text-white rounded-lg transition-colors shadow-sm"
            >
              Fill Demo Login
            </button>
          </div>

          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2 text-rose-800 text-xs font-medium">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-600" />
              <span>{error}</span>
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Gmail / Email</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <Mail className="h-4 w-4" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your Gmail address"
                  className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <Lock className="h-4 w-4" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                />
              </div>
            </div>

            <div className="flex items-center justify-between text-xs">
              <label className="flex items-center gap-2 cursor-pointer text-slate-600 select-none">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="w-4 h-4 rounded text-brand-600 focus:ring-brand-500 border-slate-300"
                />
                <span>Remember my credentials</span>
              </label>
            </div>

            <Button
              type="submit"
              variant="quantum"
              size="lg"
              className="w-full"
              isLoading={loading}
              icon={ArrowRight}
            >
              Sign In
            </Button>
          </form>

          <div className="pt-2 text-center text-xs text-slate-500">
            Don't have an account?{' '}
            <Link to="/register" className="font-semibold text-brand-600 hover:text-brand-700">
              Create account
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
