// HTTP API Client connecting Frontend to FastAPI Backend

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = {
  async getParties(statusFilter = 'active') {
    const url = new URL(`${API_BASE_URL}/api/parties`)
    if (statusFilter) {
      url.searchParams.set('status', statusFilter)
    }

    const response = await fetch(url.toString())
    if (!response.ok) {
      throw new Error(`Failed to fetch parties: ${response.statusText}`)
    }
    return response.json()
  },

  async createParty(data) {
    const response = await fetch(`${API_BASE_URL}/api/parties`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: data.name.trim(),
        party_size: Number(data.party_size) || 1,
        phone: data.phone?.trim() || null,
        notes: data.notes?.trim() || null,
      }),
    })

    if (!response.ok) {
      const err = await response.json().catch(() => ({}))
      throw new Error(err.detail || `Failed to create party: ${response.statusText}`)
    }
    return response.json()
  },

  async updatePartyStatus(id, status) {
    const response = await fetch(`${API_BASE_URL}/api/parties/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status }),
    })

    if (!response.ok) {
      const err = await response.json().catch(() => ({}))
      throw new Error(err.detail || `Failed to update party: ${response.statusText}`)
    }
    return response.json()
  },

  async deleteParty(id) {
    const response = await fetch(`${API_BASE_URL}/api/parties/${id}`, {
      method: 'DELETE',
    })

    if (!response.ok) {
      throw new Error(`Failed to delete party: ${response.statusText}`)
    }
    return response.json()
  },
}
