import React, { useEffect, useState } from 'react';
import { adminApi } from '../services/api';
import { Plus, Trash2, Edit, X, Save } from 'lucide-react';

const ProjectManager: React.FC = () => {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<any>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    technologies: '',
    github_link: '',
    live_link: '',
    image_url: ''
  });

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const data = await adminApi.getProjects();
      setProjects(data);
    } catch (error) {
      console.error('Failed to fetch projects');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (project: any = null) => {
    if (project) {
      setEditingProject(project);
      setFormData({
        title: project.title,
        description: project.description,
        category: project.category,
        technologies: project.technologies.join(', '),
        github_link: project.github_link || '',
        live_link: project.live_link || '',
        image_url: project.image_url || ''
      });
    } else {
      setEditingProject(null);
      setFormData({
        title: '',
        description: '',
        category: '',
        technologies: '',
        github_link: '',
        live_link: '',
        image_url: ''
      });
    }
    setIsModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const projectData = {
      ...formData,
      technologies: formData.technologies.split(',').map(t => t.trim()).filter(t => t !== '')
    };

    try {
      if (editingProject) {
        await adminApi.updateProject(editingProject.id, projectData);
      } else {
        await adminApi.createProject(projectData);
      }
      setIsModalOpen(false);
      fetchProjects();
    } catch (error) {
      alert('Failed to save project');
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await adminApi.deleteProject(id);
        setProjects(projects.filter(p => p.id !== id));
      } catch (error) {
        alert('Failed to delete project');
      }
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="manager-container">
      <div className="manager-header">
        <h2>Manage Projects</h2>
        <button className="btn btn-primary btn-sm" onClick={() => handleOpenModal()}>
          <Plus size={18} /> Add Project
        </button>
      </div>

      <div className="admin-table-container">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Category</th>
              <th>Technologies</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {projects.map((project) => (
              <tr key={project.id}>
                <td>{project.title}</td>
                <td>{project.category}</td>
                <td>
                  <div className="tech-tags">
                    {project.technologies?.slice(0, 3).map((t: string) => (
                      <span key={t} className="tech-tag">{t}</span>
                    ))}
                    {project.technologies?.length > 3 && '...'}
                  </div>
                </td>
                <td>
                  <div className="action-buttons">
                    <button className="icon-btn edit-btn" onClick={() => handleOpenModal(project)}><Edit size={18} /></button>
                    <button 
                      className="icon-btn delete-btn" 
                      onClick={() => handleDelete(project.id)}
                    ><Trash2 size={18} /></button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{editingProject ? 'Edit Project' : 'Add New Project'}</h3>
              <button className="close-btn" onClick={() => setIsModalOpen(false)}><X size={24} /></button>
            </div>
            <form onSubmit={handleSubmit} className="project-form">
              <div className="form-grid">
                <div className="form-group-admin">
                  <label>Title</label>
                  <input 
                    type="text" 
                    required
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                  />
                </div>
                <div className="form-group-admin">
                  <label>Category</label>
                  <input 
                    type="text" 
                    required
                    value={formData.category}
                    onChange={(e) => setFormData({...formData, category: e.target.value})}
                  />
                </div>
                <div className="form-group-admin span-2">
                  <label>Description</label>
                  <textarea 
                    rows={3}
                    required
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                  ></textarea>
                </div>
                <div className="form-group-admin span-2">
                  <label>Technologies (comma separated)</label>
                  <input 
                    type="text" 
                    required
                    placeholder="React, TypeScript, Node.js"
                    value={formData.technologies}
                    onChange={(e) => setFormData({...formData, technologies: e.target.value})}
                  />
                </div>
                <div className="form-group-admin">
                  <label>GitHub Link</label>
                  <input 
                    type="url" 
                    value={formData.github_link}
                    onChange={(e) => setFormData({...formData, github_link: e.target.value})}
                  />
                </div>
                <div className="form-group-admin">
                  <label>Live Link</label>
                  <input 
                    type="url" 
                    value={formData.live_link}
                    onChange={(e) => setFormData({...formData, live_link: e.target.value})}
                  />
                </div>
                <div className="form-group-admin span-2">
                  <label>Image URL</label>
                  <input 
                    type="text" 
                    value={formData.image_url}
                    onChange={(e) => setFormData({...formData, image_url: e.target.value})}
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary"><Save size={18} /> Save Project</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProjectManager;
