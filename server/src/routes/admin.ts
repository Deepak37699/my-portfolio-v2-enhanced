import { Router } from 'express';
import { dataManager } from '../services/dataManager.js';
import { authenticateToken } from '../middleware/auth.js';

const router = Router();

// Apply auth middleware to all admin routes
router.use(authenticateToken);

// --- Projects ---
router.get('/projects', async (req, res) => {
  try {
    const projects = await dataManager.getAllProjects();
    res.json({ projects });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch projects' });
  }
});

router.post('/projects', async (req, res) => {
  try {
    const project = await dataManager.createProject(req.body);
    res.status(201).json(project);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create project' });
  }
});

router.patch('/projects/:id', async (req, res) => {
  try {
    const project = await dataManager.updateProject(req.params.id, req.body);
    if (!project) return res.status(404).json({ error: 'Project not found' });
    res.json(project);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update project' });
  }
});

router.delete('/projects/:id', async (req, res) => {
  try {
    const success = await dataManager.deleteProject(req.params.id);
    if (!success) return res.status(404).json({ error: 'Project not found' });
    res.status(204).send();
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete project' });
  }
});

// --- Skills ---
router.get('/skills', async (req, res) => {
  try {
    const skills = await dataManager.getAllSkills();
    res.json({ skills });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch skills' });
  }
});

router.post('/skills', async (req, res) => {
  try {
    const skill = await dataManager.createSkill(req.body);
    res.status(201).json(skill);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create skill' });
  }
});

router.patch('/skills/:id', async (req, res) => {
  try {
    const skill = await dataManager.updateSkill(req.params.id, req.body);
    if (!skill) return res.status(404).json({ error: 'Skill not found' });
    res.json(skill);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update skill' });
  }
});

router.delete('/skills/:id', async (req, res) => {
  try {
    const success = await dataManager.deleteSkill(req.params.id);
    if (!success) return res.status(404).json({ error: 'Skill not found' });
    res.status(204).send();
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete skill' });
  }
});

// --- Messages ---
router.get('/messages', async (req, res) => {
  try {
    const messages = await dataManager.getAllMessages();
    res.json({ messages });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch messages' });
  }
});

// --- About ---
router.get('/about', async (req, res) => {
  try {
    const about = await dataManager.getAboutInfo();
    res.json({ about });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch about info' });
  }
});

router.put('/about', async (req, res) => {
  try {
    const about = await dataManager.updateAboutInfo(req.body);
    res.json(about);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update about info' });
  }
});

export default router;
