import api from './api';

export const authService = {
  async login(email, password) {
    const response = await api.post('/auth/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('qc_token', response.data.access_token);
      localStorage.setItem('qc_user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async register(userData) {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  async forgotPassword(email) {
    const response = await api.post('/auth/forgot-password', { email });
    return response.data;
  },

  async resetPassword(payload) {
    const response = await api.post('/auth/reset-password', payload);
    return response.data;
  },

  async updateProfile(profileData) {
    const response = await api.put('/auth/profile', profileData);
    if (response.data) {
      localStorage.setItem('qc_user', JSON.stringify(response.data));
    }
    return response.data;
  },

  async changePassword(passwordData) {
    const response = await api.put('/auth/change-password', passwordData);
    return response.data;
  },

  async logout() {
    try {
      await api.post('/auth/logout');
    } catch (e) {
      // ignore
    } finally {
      localStorage.removeItem('qc_token');
      localStorage.removeItem('qc_user');
    }
  },

  getCurrentUser() {
    const userStr = localStorage.getItem('qc_user');
    return userStr ? JSON.parse(userStr) : null;
  },

  getToken() {
    return localStorage.getItem('qc_token');
  },

  async getProfile() {
    const response = await api.get('/auth/me');
    localStorage.setItem('qc_user', JSON.stringify(response.data));
    return response.data;
  }
};
