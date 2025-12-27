import React, { useEffect, useState } from 'react';
import { portfolioApi } from '../services/api';
import { ExternalLink, Github, Folder } from 'lucide-react';

const Projects: React.FC = () => {
  const [projects, setProjects] = useState<any[]>([]);

  useEffect(() => {
    portfolioApi.getProjects().then(setProjects).catch(console.error);
  }, []);

  return (
    <div className="section-modern">
      <div className="container">
        <h2 className="section-title">My Projects</h2>
        <p className="section-subtitle">A showcase of some of my best work and personal projects.</p>
        
        <div className="projects-grid">
          {projects.map((project) => (
            <div key={project.id} className="project-card-modern">
              <div className="project-image">
                {project.image_url ? (
                  <img src={project.image_url} alt={project.title} />
                ) : (
                  <div className="project-placeholder">
                    <Folder size={48} />
                  </div>
                )}
              </div>
              <div className="project-info">
                <h3 className="project-title">{project.title}</h3>
                <p className="project-desc">{project.description}</p>
                <div className="project-tech">
                  {project.technologies?.map((tech: string) => (
                    <span key={tech} className="tech-tag">{tech}</span>
                  ))}
                </div>
                <div className="project-links">
                  {project.github_url && (
                    <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                      <Github size={20} /> Code
                    </a>
                  )}
                  {project.live_url && (
                    <a href={project.live_url} target="_blank" rel="noopener noreferrer">
                      <ExternalLink size={20} /> Live
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Projects;
