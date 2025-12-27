import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import morgan from 'morgan';
import portfolioRoutes from './routes/portfolio.js';
import adminRoutes from './routes/admin.js';
import authRoutes from './routes/auth.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(morgan('dev'));
app.use(cors());
app.use(express.json());

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api', portfolioRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', message: 'Node.js Portfolio API is running' });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
