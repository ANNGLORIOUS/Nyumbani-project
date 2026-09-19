import { useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { ProtectedRoute } from './components/ProtectedRoute'
import { DashboardLayout } from './layouts/DashboardLayout'
import { Login, Register } from './pages/Auth'
import { AdminDashboard, AgentDashboard, LandlordDashboard, TenantDashboard } from './pages/Dashboards'
import { Home } from './pages/Home'
import { api, auth } from './services/api'
import type { User } from './types'

function AppRoutes() { const [user, setUser] = useState<User | null>(null); useEffect(() => { if (auth.token) api.me().then(setUser).catch(auth.clear) }, []); const guarded = (roles: User['role'][], page: ReactNode) => <ProtectedRoute user={user} roles={roles}>{user && <DashboardLayout user={user}>{page}</DashboardLayout>}</ProtectedRoute>; return <Routes><Route path="/" element={<Home />} /><Route path="/login" element={<Login />} /><Route path="/register" element={<Register />} /><Route path="/dashboard/landlord" element={guarded(['owner'], <LandlordDashboard />)} /><Route path="/dashboard/tenant" element={guarded(['tenant'], <TenantDashboard />)} /><Route path="/dashboard/agent" element={guarded(['agent'], <AgentDashboard />)} /><Route path="/dashboard/admin" element={guarded(['admin'], <AdminDashboard />)} /></Routes> }
export default function App() { return <BrowserRouter><AppRoutes /></BrowserRouter> }
