import React, { useState, useEffect } from 'react';
import {
  User,
  Mail,
  Building,
  Lock,
  KeyRound,
  CheckCircle2,
  AlertCircle,
  Shield,
  Database,
  Cpu,
  Save,
  Sparkles
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { authService } from '../services/authService';
import { Button } from '../components/Button';

export const SettingsPage = () => {
  const { user } = useAuth();

  // Profile Form State
  const [profileData, setProfileData] = useState({
    full_name: '',
    email: '',
    institution: ''
  });
  const [profileLoading, setProfileLoading] = useState(false);
  const [profileSuccess, setProfileSuccess] = useState('');
  const [profileError, setProfileError] = useState('');

  // Password Form State
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordSuccess, setPasswordSuccess] = useState('');
  const [passwordError, setPasswordError] = useState('');

  // Load user data on mount
  useEffect(() => {
    if (user) {
      setProfileData({
        full_name: user.full_name || '',
        email: user.email || '',
        institution: user.institution || 'QuantumCare Medical Institute'
      });
    }
  }, [user]);

  // Handle Profile Update
  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setProfileError('');
    setProfileSuccess('');

    const emailClean = profileData.email.trim().toLowerCase();
    const fullNameClean = profileData.full_name.trim();

    if (!fullNameClean || !emailClean) {
      setProfileError('Name and email cannot be empty.');
      return;
    }

    setProfileLoading(true);
    try {
      await authService.updateProfile({
        full_name: fullNameClean,
        email: emailClean,
        institution: profileData.institution.trim()
      });

      // Update saved email if changed
      localStorage.setItem('quantumcare_saved_email', emailClean);

      setProfileSuccess('Profile information updated and synced with MongoDB Atlas successfully!');
      setTimeout(() => setProfileSuccess(''), 4000);
    } catch (err) {
      setProfileError(err.response?.data?.detail || 'Failed to update profile.');
    } finally {
      setProfileLoading(false);
    }
  };

  // Handle Password Change
  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setPasswordError('');
    setPasswordSuccess('');

    if (passwordData.new_password.length < 6) {
      setPasswordError('New password must be at least 6 characters in length.');
      return;
    }

    if (passwordData.new_password !== passwordData.confirm_password) {
      setPasswordError('New password and confirmation do not match.');
      return;
    }

    setPasswordLoading(true);
    try {
      await authService.changePassword({
        current_password: passwordData.current_password,
        new_password: passwordData.new_password
      });

      // Update saved password in localStorage
      localStorage.setItem('quantumcare_saved_password', passwordData.new_password);

      setPasswordData({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });

      setPasswordSuccess('Password changed and updated across all databases successfully!');
      setTimeout(() => setPasswordSuccess(''), 4000);
    } catch (err) {
      setPasswordError(err.response?.data?.detail || 'Failed to change password. Please verify your current password.');
    } finally {
      setPasswordLoading(false);
    }
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto pb-12">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Account & Platform Settings</h1>
        <p className="text-sm text-slate-500 mt-1">
          Manage your clinician credentials, security preferences, and cloud database synchronization.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* ========================================================================= */}
        {/* 1. Profile Information Card */}
        {/* ========================================================================= */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-5">
          <div className="flex items-center gap-3 pb-3 border-b border-slate-100">
            <div className="p-2 rounded-xl bg-brand-50 text-brand-600">
              <User className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-slate-900">Profile Information</h2>
              <p className="text-xs text-slate-500">Update your name and primary email address</p>
            </div>
          </div>

          {profileSuccess && (
            <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-2 text-emerald-800 text-xs font-medium">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0 text-emerald-600" />
              <span>{profileSuccess}</span>
            </div>
          )}

          {profileError && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2 text-rose-800 text-xs font-medium">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-600" />
              <span>{profileError}</span>
            </div>
          )}

          <form className="space-y-4" onSubmit={handleProfileSubmit}>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <User className="h-4 w-4" />
                </div>
                <input
                  type="text"
                  required
                  value={profileData.full_name}
                  onChange={(e) => setProfileData(prev => ({ ...prev, full_name: e.target.value }))}
                  placeholder="Your full name"
                  className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Gmail / Email Address</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <Mail className="h-4 w-4" />
                </div>
                <input
                  type="email"
                  required
                  value={profileData.email}
                  onChange={(e) => setProfileData(prev => ({ ...prev, email: e.target.value }))}
                  placeholder="Your email address"
                  className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Affiliated Institution</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <Building className="h-4 w-4" />
                </div>
                <input
                  type="text"
                  value={profileData.institution}
                  onChange={(e) => setProfileData(prev => ({ ...prev, institution: e.target.value }))}
                  placeholder="Hospital / Research Institute"
                  className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                />
              </div>
            </div>

            <Button
              type="submit"
              variant="quantum"
              size="md"
              className="w-full"
              isLoading={profileLoading}
              icon={Save}
            >
              Save Profile Changes
            </Button>
          </form>
        </div>

        {/* ========================================================================= */}
        {/* 2. Security & Password Card */}
        {/* ========================================================================= */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-5">
          <div className="flex items-center gap-3 pb-3 border-b border-slate-100">
            <div className="p-2 rounded-xl bg-purple-50 text-purple-600">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-slate-900">Security & Password</h2>
              <p className="text-xs text-slate-500">Update your account password</p>
            </div>
          </div>

          {passwordSuccess && (
            <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-2 text-emerald-800 text-xs font-medium">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0 text-emerald-600" />
              <span>{passwordSuccess}</span>
            </div>
          )}

          {passwordError && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2 text-rose-800 text-xs font-medium">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-600" />
              <span>{passwordError}</span>
            </div>
          )}

          <form className="space-y-4" onSubmit={handlePasswordSubmit}>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Current Password</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <Lock className="h-4 w-4" />
                </div>
                <input
                  type="password"
                  required
                  value={passwordData.current_password}
                  onChange={(e) => setPasswordData(prev => ({ ...prev, current_password: e.target.value }))}
                  placeholder="Enter current password"
                  className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">New Password</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <KeyRound className="h-4 w-4" />
                </div>
                <input
                  type="password"
                  required
                  value={passwordData.new_password}
                  onChange={(e) => setPasswordData(prev => ({ ...prev, new_password: e.target.value }))}
                  placeholder="At least 6 characters"
                  className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Confirm New Password</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <KeyRound className="h-4 w-4" />
                </div>
                <input
                  type="password"
                  required
                  value={passwordData.confirm_password}
                  onChange={(e) => setPasswordData(prev => ({ ...prev, confirm_password: e.target.value }))}
                  placeholder="Re-enter new password"
                  className="block w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-brand-500 focus:border-brand-500 bg-white"
                />
              </div>
            </div>

            <Button
              type="submit"
              variant="secondary"
              size="md"
              className="w-full font-semibold"
              isLoading={passwordLoading}
              icon={Shield}
            >
              Update Password
            </Button>
          </form>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* 3. Cloud Database & Engine Telemetry Status */}
      {/* ========================================================================= */}
      <div className="bg-gradient-to-br from-slate-900 to-slate-800 p-6 rounded-2xl text-white shadow-md space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-brand-500/20 text-brand-400 border border-brand-400/30">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white">MongoDB Atlas Cloud Database</h3>
              <p className="text-xs text-slate-400">Persistent storage cluster for clinical scans & quantum telemetry</p>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Synced
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 border-t border-slate-700/60 text-xs">
          <div>
            <span className="text-slate-400 block mb-0.5">Database Engine</span>
            <span className="font-semibold text-slate-200">MongoDB Atlas (M0 Free Tier)</span>
          </div>
          <div>
            <span className="text-slate-400 block mb-0.5">Quantum Circuit Device</span>
            <span className="font-semibold text-slate-200">PennyLane 4-Qubit Simulator</span>
          </div>
          <div>
            <span className="text-slate-400 block mb-0.5">Vision Model</span>
            <span className="font-semibold text-slate-200">Swin-T 768D Feature Extractor</span>
          </div>
        </div>
      </div>
    </div>
  );
};
