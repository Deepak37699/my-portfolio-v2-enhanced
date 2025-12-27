import { Router } from 'express';
import { dataManager } from '../services/dataManager.js';

const router = Router();

router.get('/projects', async (req, res) => {
  try {
    const projects = await dataManager.getAllProjects();
    res.json({ projects });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch projects' });
  }
});

router.get('/skills', async (req, res) => {
  try {
    const skills = await dataManager.getAllSkills();
    res.json({ skills });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch skills' });
  }
});

router.get('/about', async (req, res) => {
  try {
    const about = await dataManager.getAboutInfo();
    res.json({ about });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch about info' });
  }
});

router.post('/contact', async (req, res) => {
  try {
    const message = await dataManager.createMessage(req.body);
    res.status(201).json({ message: 'Message sent successfully', id: message.id });
  } catch (error) {
    res.status(500).json({ error: 'Failed to send message' });
  }
});

export default router;
