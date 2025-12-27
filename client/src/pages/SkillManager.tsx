import React, { useEffect, useState } from 'react';
import { adminApi } from '../services/api';
import { Plus, Trash2, Edit, Award, X, Save } from 'lucide-react';

const SkillManager: React.FC = () => {
  const [skills, setSkills] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingSkill, setEditingSkill] = useState<any>(null);
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    proficiency: 80,
    icon: 'Award' // Default icon name
  });

  useEffect(() => {
    fetchSkills();
  }, []);

  const fetchSkills = async () => {
    try {
      const data = await adminApi.getSkills();
      setSkills(data);
    } catch (error) {
      console.error('Failed to fetch skills');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (skill: any = null) => {
    if (skill) {
      setEditingSkill(skill);
      setFormData({
        name: skill.name,
        category: skill.category,
        proficiency: skill.proficiency,
        icon: skill.icon || 'Award'
      });
    } else {
      setEditingSkill(null);
      setFormData({
        name: '',
        category: '',
        proficiency: 80,
        icon: 'Award'
      });
    }
    setIsModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingSkill) {
        await adminApi.updateSkill(editingSkill.id, formData);
      } else {
        await adminApi.createSkill(formData);
      }
      setIsModalOpen(false);
      fetchSkills();
    } catch (error) {
      alert('Failed to save skill');
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this skill?')) {
      try {
        await adminApi.deleteSkill(id);
        setSkills(skills.filter(s => s.id !== id));
      } catch (error) {
        alert('Failed to delete skill');
      }
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!skills) return <div className="error-message">Failed to load skills.</div>;

  return (
    <div className="manager-container">
      <div className="manager-header">
        <h2>Manage Skills</h2>
        <button className="btn btn-primary btn-sm" onClick={() => handleOpenModal()}>
          <Plus size={18} /> Add Skill
        </button>
      </div>

      <div className="admin-table-container">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Proficiency</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {skills.map((skill) => (
              <tr key={skill.id}>
                <td>
                  <div className="skill-name-cell">
                    <Award size={18} /> {skill.name}
                  </div>
                </td>
                <td>{skill.category}</td>
                <td>
                  <div className="admin-progress-bar">
                    <div className="progress-fill" style={{ width: `${skill.proficiency}%` }}></div>
                    <span>{skill.proficiency}%</span>
                  </div>
                </td>
                <td>
                  <div className="action-buttons">
                    <button className="icon-btn edit-btn" onClick={() => handleOpenModal(skill)}><Edit size={18} /></button>
                    <button 
                      className="icon-btn delete-btn" 
                      onClick={() => handleDelete(skill.id)}
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
              <h3>{editingSkill ? 'Edit Skill' : 'Add New Skill'}</h3>
              <button className="close-btn" onClick={() => setIsModalOpen(false)}><X size={24} /></button>
            </div>
            <form onSubmit={handleSubmit} className="project-form">
              <div className="form-grid">
                <div className="form-group-admin">
                  <label>Skill Name</label>
                  <input 
                    type="text" 
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                  />
                </div>
                <div className="form-group-admin">
                  <label>Category</label>
                  <input 
                    type="text" 
                    required
                    placeholder="e.g. Frontend, Backend, Tools"
                    value={formData.category}
                    onChange={(e) => setFormData({...formData, category: e.target.value})}
                  />
                </div>
                <div className="form-group-admin span-2">
                  <label>Proficiency ({formData.proficiency}%)</label>
                  <input 
                    type="range" 
                    min="0"
                    max="100"
                    step="5"
                    value={formData.proficiency}
                    onChange={(e) => setFormData({...formData, proficiency: parseInt(e.target.value)})}
                    className="admin-range-input"
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setIsModalOpen(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary"><Save size={18} /> Save Skill</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default SkillManager;
