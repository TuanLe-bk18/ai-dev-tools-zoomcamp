// Centralized API client (Currently mocked with localStorage persistence for prototype)

const STORAGE_KEY = 'seatflow_parties_mock'

const INITIAL_PARTIES = [
  {
    id: 1,
    name: 'Sarah Connor',
    party_size: 4,
    phone: '555-0199',
    notes: 'Needs high chair',
    status: 'waiting',
    created_at: new Date(Date.now() - 18 * 60000).toISOString(),
    updated_at: new Date(Date.now() - 18 * 60000).toISOString()
  },
  {
    id: 2,
    name: 'David Miller',
    party_size: 2,
    phone: '555-0142',
    notes: 'Window booth preferred',
    status: 'notified',
    created_at: new Date(Date.now() - 12 * 60000).toISOString(),
    updated_at: new Date(Date.now() - 2 * 60000).toISOString()
  },
  {
    id: 3,
    name: 'Elena Rostova',
    party_size: 6,
    phone: '555-0183',
    notes: 'Birthday dinner',
    status: 'waiting',
    created_at: new Date(Date.now() - 5 * 60000).toISOString(),
    updated_at: new Date(Date.now() - 5 * 60000).toISOString()
  }
]

function getStoredParties() {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(INITIAL_PARTIES))
    return INITIAL_PARTIES
  }
  try {
    return JSON.parse(raw)
  } catch {
    return INITIAL_PARTIES
  }
}

function saveStoredParties(parties) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(parties))
}

export const api = {
  async getParties(statusFilter = null) {
    await new Promise((r) => setTimeout(r, 60)) // simulate network latency
    const parties = getStoredParties()
    if (!statusFilter || statusFilter === 'all') {
      return parties
    }
    if (statusFilter === 'active') {
      return parties.filter((p) => p.status === 'waiting' || p.status === 'notified')
    }
    return parties.filter((p) => p.status === statusFilter)
  },

  async createParty(data) {
    await new Promise((r) => setTimeout(r, 80))
    const parties = getStoredParties()
    const newParty = {
      id: Date.now(),
      name: data.name.trim(),
      party_size: Number(data.party_size) || 1,
      phone: data.phone?.trim() || '',
      notes: data.notes?.trim() || '',
      status: 'waiting',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    const updated = [...parties, newParty]
    saveStoredParties(updated)
    return newParty
  },

  async updatePartyStatus(id, status) {
    await new Promise((r) => setTimeout(r, 60))
    const parties = getStoredParties()
    const index = parties.findIndex((p) => p.id === id)
    if (index === -1) throw new Error('Party not found')

    parties[index] = {
      ...parties[index],
      status,
      updated_at: new Date().toISOString()
    }
    saveStoredParties(parties)
    return parties[index]
  },

  async deleteParty(id) {
    await new Promise((r) => setTimeout(r, 60))
    const parties = getStoredParties().filter((p) => p.id !== id)
    saveStoredParties(parties)
    return { success: true }
  }
}
