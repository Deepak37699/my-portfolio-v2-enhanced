import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { v4 as uuidv4 } from 'uuid';

import type { Project, Skill, ContactMessage, AboutInfo, User } from '../models/types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.join(__dirname, '../../../data');

export class DataManager {
  private async readJson<T>(filename: string): Promise<T> {
    try {
      const filePath = path.join(DATA_DIR, filename);
      const data = await fs.readFile(filePath, 'utf-8');
      return JSON.parse(data);
    } catch (error) {
      const key = filename.split('.')[0] || 'data';
      return { [key]: [] } as unknown as T;
    }
  }

  private async writeJson<T>(filename: string, data: T): Promise<void> {
    try {
      const filePath = path.join(DATA_DIR, filename);
      await fs.writeFile(filePath, JSON.stringify(data, null, 2), 'utf-8');
    } catch (error) {
      console.error(`Error writing ${filename}:`, error);
      throw error;
    }
  }

  // Project operations
  async getAllProjects(): Promise<Project[]> {
    const data = await this.readJson<{ projects: Project[] }>('projects.json');
    return data.projects || [];
  }

  async createProject(project: Omit<Project, 'id' | 'created_date'>): Promise<Project> {
    const data = await this.readJson<{ projects: Project[] }>('projects.json');
    const newProject: Project = {
      ...project,
      id: uuidv4(),
      created_date: new Date().toISOString()
    };
    data.projects.push(newProject);
    await this.writeJson('projects.json', data);
    return newProject;
  }

  async updateProject(id: string, updates: Partial<Project>): Promise<Project | null> {
    const data = await this.readJson<{ projects: Project[] }>('projects.json');
    const index = data.projects.findIndex(p => p.id === id);
    if (index === -1) return null;
    data.projects[index] = { ...data.projects[index]!, ...updates };
    await this.writeJson('projects.json', data);
    return data.projects[index]!;
  }

  async deleteProject(id: string): Promise<boolean> {
    const data = await this.readJson<{ projects: Project[] }>('projects.json');
    const initialLength = data.projects.length;
    data.projects = data.projects.filter(p => p.id !== id);
    if (data.projects.length === initialLength) return false;
    await this.writeJson('projects.json', data);
    return true;
  }

  // Skill operations
  async getAllSkills(): Promise<Skill[]> {
    const data = await this.readJson<{ skills: Skill[] }>('skills.json');
    return data.skills || [];
  }

  async createSkill(skill: Omit<Skill, 'id'>): Promise<Skill> {
    const data = await this.readJson<{ skills: Skill[] }>('skills.json');
    const newSkill: Skill = { ...skill, id: uuidv4() };
    data.skills.push(newSkill);
    await this.writeJson('skills.json', data);
    return newSkill;
  }

  async updateSkill(id: string, updates: Partial<Skill>): Promise<Skill | null> {
    const data = await this.readJson<{ skills: Skill[] }>('skills.json');
    const index = data.skills.findIndex(s => s.id === id);
    if (index === -1) return null;
    data.skills[index] = { ...data.skills[index]!, ...updates };
    await this.writeJson('skills.json', data);
    return data.skills[index]!;
  }

  async deleteSkill(id: string): Promise<boolean> {
    const data = await this.readJson<{ skills: Skill[] }>('skills.json');
    const initialLength = data.skills.length;
    data.skills = data.skills.filter(s => s.id !== id);
    if (data.skills.length === initialLength) return false;
    await this.writeJson('skills.json', data);
    return true;
  }

  // About operations
  async getAboutInfo(): Promise<AboutInfo | null> {
    const data = await this.readJson<{ about: AboutInfo }>('about.json');
    return data.about || null;
  }

  async updateAboutInfo(info: AboutInfo): Promise<AboutInfo> {
    await this.writeJson('about.json', { about: info });
    return info;
  }

  // Message operations
  async getAllMessages(): Promise<ContactMessage[]> {
    const data = await this.readJson<{ messages: ContactMessage[] }>('messages.json');
    return data.messages || [];
  }

  async createMessage(message: Omit<ContactMessage, 'id' | 'created_date' | 'is_read'>): Promise<ContactMessage> {
    const data = await this.readJson<{ messages: ContactMessage[] }>('messages.json');
    const newMessage: ContactMessage = {
      ...message,
      id: uuidv4(),
      created_date: new Date().toISOString(),
      is_read: false
    };
    data.messages.push(newMessage);
    await this.writeJson('messages.json', data);
    return newMessage;
  }
  
  // User operations
  async getUserByUsername(username: string): Promise<User | null> {
    const data = await this.readJson<{ users: User[] }>('users.json');
    return data.users.find(u => u.username === username) || null;
  }
}

export const dataManager = new DataManager();
