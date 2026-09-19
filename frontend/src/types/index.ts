export type Role = 'tenant' | 'owner' | 'agent' | 'caretaker' | 'admin'
export interface User { id: number; username: string; email: string; role: Role; phone_number?: string }
export interface Property { id: number; name: string; property_type: string; location: string; county: string; neighborhood: string; rent_price: string; bedrooms: number; bathrooms: number; available_units: number; status: string; description: string; amenities: string[]; images: { image: string; is_cover: boolean }[] }
export interface Payment { id: number; amount: string; status: string; created_at: string; property: number; rent_record?: number }
export interface Maintenance { id: number; issue_type: string; description: string; status: string; created_at: string }
