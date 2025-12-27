import React, { useEffect, useState } from 'react';
import { adminApi } from '../services/api';
import { Save } from 'lucide-react';

const AboutManager: React.FC = () => {
  const [about, setAbout] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchAbout();
  }, []);

  const fetchAbout = async () => {
    try {
      const data = await adminApi.getAbout();
      setAbout(data);
    } catch (error) {
      console.error('Failed to fetch about info');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await adminApi.updateAbout(about);
      alert('Updated successfully!');
    } catch (error) {
      alert('Failed to update');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!about) return <div className="error-message">Failed to load about info.</div>;

  return (
    <div className="manager-container">
      <div className="manager-header">
        <h2>Manage Profile Info</h2>
      </div>

      <form onSubmit={handleSubmit} className="about-form-modern">
        <div className="form-sections">
          <div className="form-section">
            <h3 className="section-subtitle-admin">Basic Information</h3>
            <div className="form-group-admin">
              <label>Full Name</label>
              <input 
                type="text" 
                value={about.name}
                onChange={(e) => setAbout({...about, name: e.target.value})}
              />
            </div>
            <div className="form-group-admin">
              <label>Title</label>
              <input 
                type="text" 
                value={about.title}
                onChange={(e) => setAbout({...about, title: e.target.value})}
              />
            </div>
            <div className="form-group-admin">
              <label>Location</label>
              <input 
                type="text" 
                value={about.location}
                onChange={(e) => setAbout({...about, location: e.target.value})}
              />
            </div>
          </div>

          <div className="form-section">
            <h3 className="section-subtitle-admin">Biography</h3>
            <div className="form-group-admin">
              <textarea 
                rows={10}
                value={about.bio}
                onChange={(e) => setAbout({...about, bio: e.target.value})}
              ></textarea>
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary" disabled={saving}>
            <Save size={20} /> {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AboutManager;
