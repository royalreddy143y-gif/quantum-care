import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Cpu, Lock, Mail, KeyRound, ArrowRight, ArrowLeft, AlertCircle, CheckCircle2, Sparkles } from 'lucide-react';
import { authService } from '../services/authService';
import { Button } from '../components/Button';

export const ForgotPasswordPage = () => {
  const [step, setStep] = useState(1); // 1: Request Code, 2: Reset Password, 3: Success
  const [email, setEmail] = useState('');
  const [resetCode, setResetCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [serverNotice, setServerNotice] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Step 1: Request Reset Code
  const handleRequestCode = async (e) => {
    e.preventDefault();
    setError('');
    setServerNotice('');
    const emailClean = email.trim().toLowerCase();

    if (!emailClean) {
      setError('Please enter your registered email address.');
      return;
    }

    setLoading(true);
    try {
      const res = await authService.forgotPassword(emailClean);
      if (res.reset_code) {
        setResetCode(res.reset_code);
        setServerNotice(`Verification code generated: ${res.reset_code}`);
      }
      setStep(2);
    } catch (err) {
      setError(err.response?.data?.detail || 'No account found with this email.');
    } finally {
      setLoading(false);
    }
  };

  // Step 2: Reset Password
  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError('');

    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      await authService.resetPassword({
        email: email.trim().toLowerCase(),
        reset_code: resetCode.trim(),
        new_password: newPassword
      });

      // Update saved credentials
      localStorage.setItem('quantumcare_saved_email', email.trim().toLowerCase());
      localStorage.setItem('quantumcare_saved_password', newPassword);

      setStep(3);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reset password. Please check your verification code.');
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
        <h2 className="text-2xl font-bold text-slate-900">
          {step === 3 ? 'Password Reset Complete' : 'Reset Your Password'}
        </h2>
        <p className="mt-1 text-xs text-slate-500">
          {step === 1 && 'Enter your email to receive a secure recovery code'}
          {step === 2 && 'Enter your verification code and set your new password'}
          {step === 3 && 'Your password has been successfully updated across all databases'}
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md px-4">
        <div className="bg-white py-8 px-6 shadow-xl shadow-slate-200/50 rounded-2xl border border-slate-100 sm:px-10 space-y-6">
          
          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2 text-rose-800 text-xs font-medium">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-600" />
              <span>{error}</span>
            </div>
          )}

          {serverNotice && step === 2 && (
            <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-2 text-emerald-800 text-xs font-medium">
              <Sparkles className="w-4 h-4 flex-shrink-0 text-emerald-600" />
              <span>{serverNotice}</span>
            </div>
          )}

          {/* STEP 1: Enter Email */}
          {step === 1 && (
            <form className="space-y-4" onSubmit={handleRequestCode}>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Registered Gmail / Email</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <Mail className="h-4 w-4" />
                  </div>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your account email"
                    className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                  />
                </div>
              </div>

              <Button
                type="submit"
                variant="quantum"
                size="lg"
                className="w-full"
                isLoading={loading}
                icon={ArrowRight}
              >
                Send Recovery Code
              </Button>
            </form>
          )}

          {/* STEP 2: Enter Code & New Password */}
          {step === 2 && (
            <form className="space-y-4" onSubmit={handleResetPassword}>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">6-Digit Recovery Code</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <KeyRound className="h-4 w-4" />
                  </div>
                  <input
                    type="text"
                    required
                    maxLength={6}
                    value={resetCode}
                    onChange={(e) => setResetCode(e.target.value)}
                    placeholder="Enter 6-digit code"
                    className="block w-full pl-9 pr-3 py-2 text-sm font-mono tracking-wider border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">New Password</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <Lock className="h-4 w-4" />
                  </div>
                  <input
                    type="password"
                    required
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="At least 6 characters"
                    className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Confirm New Password</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                    <Lock className="h-4 w-4" />
                  </div>
                  <input
                    type="password"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter new password"
                    className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                  />
                </div>
              </div>

              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setStep(1)}
                  className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 border border-slate-200 rounded-lg"
                >
                  Back
                </button>
                <Button
                  type="submit"
                  variant="quantum"
                  size="lg"
                  className="flex-1"
                  isLoading={loading}
                  icon={CheckCircle2}
                >
                  Save New Password
                </Button>
              </div>
            </form>
          )}

          {/* STEP 3: Success Confirmation */}
          {step === 3 && (
            <div className="text-center space-y-4 py-4">
              <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto shadow-xs">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <p className="text-sm text-slate-600">
                Your password has been successfully updated and synced with MongoDB Atlas. You can now sign in with your new credentials.
              </p>
              <Button
                variant="quantum"
                size="lg"
                className="w-full"
                onClick={() => navigate('/login')}
                icon={ArrowRight}
              >
                Proceed to Sign In
              </Button>
            </div>
          )}

          <div className="pt-2 text-center text-xs text-slate-500">
            Remembered your password?{' '}
            <Link to="/login" className="font-semibold text-brand-600 hover:text-brand-700">
              Back to Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
