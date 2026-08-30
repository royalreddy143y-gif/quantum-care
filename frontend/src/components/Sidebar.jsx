import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  PlusCircle,
  Users,
  History,
  Settings,
  Cpu,
  LogOut
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'New Analysis', path: '/analyses/new', icon: PlusCircle },
    { label: 'Patients', path: '/patients', icon: Users },
    { label: 'Analyses History', path: '/history', icon: History },
    { label: 'Settings', path: '/settings', icon: Settings },
  ];

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <aside className="w-64 bg-white border-r border-slate-200 min-h-screen flex flex-col justify-between p-4 flex-shrink-0">
      <div className="space-y-6">
        {/* Brand Header */}
        <Link to="/dashboard" className="flex items-center gap-2.5 px-2 py-1">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-brand-600 to-purple-600 text-white shadow-md">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-slate-900 tracking-tight">QuantumCare</h1>
            <p className="text-[10px] uppercase font-semibold text-brand-600 tracking-wider">Hybrid Quantum AI</p>
          </div>
        </Link>

        {/* Navigation Items */}
        <nav className="space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-brand-50 text-brand-700 font-semibold shadow-xs'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-brand-600' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Footer Info & User Card */}
      <div className="space-y-4 pt-4 border-t border-slate-100">
        {/* Engine Status Indicator */}
        <div className="rounded-xl bg-gradient-to-br from-slate-900 to-slate-800 p-3 text-white shadow-sm">
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-300 font-medium">Engine Status</span>
            <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 px-1.5 py-0.5 rounded text-[10px] font-bold">
              Active (4 Qubits)
            </span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1 leading-tight">
            Hybrid Quantum-Classical Neural Network
          </p>
        </div>

        {/* User Card linking to Settings */}
        <div className="flex items-center justify-between px-2">
          <Link
            to="/settings"
            className="flex items-center gap-2.5 overflow-hidden flex-1 group hover:opacity-80 transition-opacity"
            title="Open Account Settings"
          >
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-brand-500 to-purple-500 text-white flex items-center justify-center font-bold text-xs shadow-xs">
              {user?.full_name?.charAt(0) || 'U'}
            </div>
            <div className="truncate">
              <p className="text-xs font-semibold text-slate-900 truncate group-hover:text-brand-600 transition-colors">
                {user?.full_name || 'User'}
              </p>
              <p className="text-[10px] text-slate-500 truncate">
                {user?.email || 'Authenticated'}
              </p>
            </div>
          </Link>
          <button
            onClick={handleLogout}
            className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors ml-1"
            title="Sign Out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
};
