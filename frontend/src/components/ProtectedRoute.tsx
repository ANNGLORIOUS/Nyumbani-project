import { Navigate } from 'react-router-dom'
import type { ReactNode } from 'react'
import type { Role, User } from '../types'
import { auth } from '../services/api'
export function ProtectedRoute({ user, roles, children }: { user: User | null; roles: Role[]; children: ReactNode }) { if (!auth.token) return <Navigate to="/login" replace />; if (!user) return <p className="p-8">Loading your workspace…</p>; if (!roles.includes(user.role) && !(user.role === 'caretaker' && roles.includes('agent'))) return <Navigate to="/" replace />; return <>{children}</> }
