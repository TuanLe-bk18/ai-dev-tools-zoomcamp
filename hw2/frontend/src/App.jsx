import { useState, useEffect } from 'react'
import { api } from './api'

function formatWaitTime(isoDate) {
  const diffMs = Date.now() - new Date(isoDate).getTime()
  const diffMins = Math.max(0, Math.floor(diffMs / 60000))
  if (diffMins === 0) return 'Just now'
  return `${diffMins}m ago`
}

export default function App() {
  const [parties, setParties] = useState([])
  const [filter, setFilter] = useState('active')
  const [loading, setLoading] = useState(false)

  // Form state
  const [name, setName] = useState('')
  const [partySize, setPartySize] = useState(2)
  const [phone, setPhone] = useState('')
  const [notes, setNotes] = useState('')

  async function loadParties() {
    setLoading(true)
    try {
      const data = await api.getParties(filter)
      setParties(data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadParties()
  }, [filter])

  async function handleAddParty(e) {
    e.preventDefault()
    if (!name.trim()) return

    await api.createParty({
      name,
      party_size: Number(partySize),
      phone,
      notes
    })

    setName('')
    setPartySize(2)
    setPhone('')
    setNotes('')
    await loadParties()
  }

  async function handleStatusChange(id, newStatus) {
    await api.updatePartyStatus(id, newStatus)
    await loadParties()
  }

  const activeParties = parties.filter((p) => p.status === 'waiting' || p.status === 'notified')
  const totalWaitingGuests = activeParties.reduce((sum, p) => sum + p.party_size, 0)

  return (
    <div className="container">
      <header>
        <div className="brand">
          <h1>SeatFlow</h1>
          <p>Host stand waitlist manager</p>
        </div>
        <div className="stats-bar">
          <div className="stat-item">
            <div className="stat-value">{activeParties.length}</div>
            <div className="stat-label">Parties Waiting</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{totalWaitingGuests}</div>
            <div className="stat-label">Guests Waiting</div>
          </div>
        </div>
      </header>

      <main className="grid">
        {/* Left column: Add to Waitlist Form */}
        <section className="card">
          <h2>Add Party to Waitlist</h2>
          <form onSubmit={handleAddParty}>
            <div className="form-group">
              <label htmlFor="guest-name">Guest Name *</label>
              <input
                id="guest-name"
                type="text"
                placeholder="e.g. Alex Grigorev"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="party-size">Party Size *</label>
              <input
                id="party-size"
                type="number"
                min="1"
                max="20"
                value={partySize}
                onChange={(e) => setPartySize(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="phone">Phone Number</label>
              <input
                id="phone"
                type="tel"
                placeholder="e.g. 555-0123"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="notes">Seating Notes</label>
              <textarea
                id="notes"
                rows="2"
                placeholder="e.g. Booth preferred, high chair needed"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
            </div>

            <button type="submit" className="btn-primary">
              Add to Waitlist
            </button>
          </form>
        </section>

        {/* Right column: Queue list */}
        <section className="card">
          <div className="tabs">
            <button
              className={`tab-btn ${filter === 'active' ? 'active' : ''}`}
              onClick={() => setFilter('active')}
            >
              Active Queue ({activeParties.length})
            </button>
            <button
              className={`tab-btn ${filter === 'seated' ? 'active' : ''}`}
              onClick={() => setFilter('seated')}
            >
              Seated History
            </button>
            <button
              className={`tab-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => setFilter('all')}
            >
              All Records
            </button>
          </div>

          {loading ? (
            <div className="empty-state">Loading queue...</div>
          ) : parties.length === 0 ? (
            <div className="empty-state">No parties found in this view.</div>
          ) : (
            <div>
              {parties.map((party) => (
                <div key={party.id} className="party-item">
                  <div className="party-meta">
                    <span className="party-size">{party.party_size}</span>
                    <div className="party-info">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <h3>{party.name}</h3>
                        <span className={`badge ${party.status}`}>{party.status}</span>
                      </div>
                      <p>
                        {party.phone && <span>{party.phone} • </span>}
                        <span>Wait time: {formatWaitTime(party.created_at)}</span>
                        {party.notes && <span> • <em>"{party.notes}"</em></span>}
                      </p>
                    </div>
                  </div>

                  <div className="party-actions">
                    {party.status === 'waiting' && (
                      <button
                        className="btn-action notify"
                        onClick={() => handleStatusChange(party.id, 'notified')}
                      >
                        Notify
                      </button>
                    )}
                    {(party.status === 'waiting' || party.status === 'notified') && (
                      <button
                        className="btn-action seat"
                        onClick={() => handleStatusChange(party.id, 'seated')}
                      >
                        Seat
                      </button>
                    )}
                    {(party.status === 'waiting' || party.status === 'notified') && (
                      <button
                        className="btn-action"
                        onClick={() => handleStatusChange(party.id, 'cancelled')}
                      >
                        Cancel
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}
