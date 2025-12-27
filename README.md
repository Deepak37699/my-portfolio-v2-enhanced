# Modern Portfolio Web Application

A premium, full-stack portfolio application built with a modern tech stack. This project features a React frontend with Framer Motion for smooth animations and a Node.js/Express backend with JSON-based data management.

## 🚀 Tech Stack

- **Frontend**: React 19, Vite, TypeScript, Tailwind CSS, Framer Motion, Lucide React
- **Backend**: Node.js, Express 5, TypeScript, JWT Authentication
- **Storage**: JSON file-based storage for easy portability
- **PWA**: Progressive Web App support with `vite-plugin-pwa`

## 📁 Project Structure

```text
my-portfolio/
├── client/              # React frontend
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Page components (About, Contact, etc.)
│   │   ├── services/    # API services
│   │   └── App.tsx      # Main entry point
│   └── package.json
├── server/              # Node.js backend
│   ├── src/
│   │   ├── routes/      # API endpoints
│   │   ├── middleware/  # Auth and other middlewares
│   │   └── index.ts     # Express server entry
│   └── package.json
├── data/                # JSON data storage
└── render.yaml          # Deployment configuration
```

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Deepak37699/my-portfolio-v2-enhanced.git
cd my-portfolio
```

### 2. Setup Backend
```bash
cd server
npm install
cp .env.example .env  # Configure your environment variables
npm run dev
```

### 3. Setup Frontend
```bash
cd ../client
npm install
npm run dev
```

## 🌐 Usage

- **Portfolio**: `http://localhost:5173`
- **Admin Dashboard**: `http://localhost:5173/admin` (Requires login)
- **API Health**: `http://localhost:8000/health`

## 📄 License

This project is licensed under the MIT License.
