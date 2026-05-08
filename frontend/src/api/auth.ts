import { apiClient } from './client';
import type { LoginRequest, TokenResponse, MeResponse } from '@/types/auth';

export const authApi = {
    login: (data: LoginRequest) =>
        apiClient.post<TokenResponse>('/auth/login', data),

    me: () =>
        apiClient.get<MeResponse>('/auth/me')
};