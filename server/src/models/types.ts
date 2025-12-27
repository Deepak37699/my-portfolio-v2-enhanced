export interface Project {
  id: string;
  title: string;
  description: string;
  image_url?: string;
  technologies: string[];
  github_url?: string;
  live_url?: string;
  featured: boolean;
  created_date: string;
}

export interface Skill {
  id: string;
  name: string;
  category: string;
  proficiency: number;
  icon_name?: string;
}

export interface ContactMessage {
  id: string;
  name: string;
  email: string;
  subject: string;
  message: string;
  created_date: string;
  is_read: boolean;
}

export interface AboutInfo {
  name: string;
  title: string;
  bio: string;
  location: string;
  email: string;
  phone?: string;
  social_links: {
    github?: string;
    linkedin?: string;
    twitter?: string;
  };
  education: Array<{
    id: string;
    institution: string;
    degree: string;
    period: string;
    description?: string;
  }>;
  experience: Array<{
    id: string;
    company: string;
    job_title: string;
    period: string;
    description?: string;
  }>;
}

export interface User {
  username: string;
  email?: string;
  hashed_password: string;
  is_active: boolean;
  created_date: string;
}
