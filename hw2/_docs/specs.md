# SeatFlow - Restaurant Waitlist Manager Specification

Single-screen waitlist manager for restaurant host stands. Replaces pen-and-paper clipboards with an uncluttered queue board.

## 1. Problem & Objectives
During peak meal rushes, hosts struggle to track party arrival order, table sizing needs, and guest status using paper clipboards. SeatFlow provides a real-time digital queue to register parties, track wait times, and seat guests quickly.

## 2. Core User Stories
- **Add party to queue:** Host inputs guest name, party size (number of seats), phone number, and optional seating notes (e.g. "needs high chair", "outdoor preferred").
- **View active waitlist:** Host reviews waiting parties sorted chronologically (FIFO: longest waiting first). Each entry displays elapsed wait time and status badge.
- **Progress party state:** Host updates party state with a single click:
  - `waiting` -> `notified` (guest called or texted)
  - `notified` -> `seated` (guest taken to table)
  - `waiting`/`notified` -> `cancelled` (guest walked away / no-show)
- **Queue metrics summary:** Quick header counters showing total waiting parties, total waiting guests, and average wait time.

## 3. Non-Goals (Out of Scope for v1)
- Automated SMS dispatching (Twilio integration).
- Table layout / floor plan mapping.
- Multi-location tenant auth or host logins.
- Online public self-registration link.

## 4. Data Model

### Party Entity
| Field | Type | Required | Constraints / Default | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `id` | Integer | Yes | Primary Key, Auto-increment | Internal identifier |
| `name` | String(100) | Yes | Non-empty | Guest or party contact name |
| `party_size` | Integer | Yes | >= 1 | Number of seats required |
| `phone` | String(20) | No | Optional | Phone number for contact |
| `notes` | String(255) | No | Empty by default | Dietary/seating requirements |
| `status` | Enum | Yes | `waiting`, `notified`, `seated`, `cancelled` | Default: `waiting` |
| `created_at` | DateTime | Yes | UTC timestamp of registration | Used for FIFO queue ordering |
| `updated_at` | DateTime | Yes | UTC timestamp of last modification | Updated on state transition |

## 5. API Contract Draft (REST)

- `GET /api/parties`: List parties. Query params: `status` (optional filter, defaults to active: `waiting,notified`).
- `POST /api/parties`: Register a new party. Body: `{ name, party_size, phone?, notes? }`.
- `PATCH /api/parties/{id}`: Update status or details. Body: `{ status?, notes?, party_size? }`.
- `DELETE /api/parties/{id}`: Hard delete record (admin cleanup).

## 6. UI Structure (Single Screen)
- **Top Bar:** App title (`SeatFlow`), live queue stats (Waiting parties, Waiting guests).
- **Left Panel / Modal:** "Add Guest" form (Name, Party Size, Phone, Notes, "Add to Waitlist" button).
- **Main Area:** Waitlist cards or table sorted by arrival time, showing:
  - Position number, Name, Party Size badge.
  - Minutes elapsed since arrival.
  - Action buttons: [Notify], [Seat], [Cancel].
