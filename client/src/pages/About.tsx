import React, { useEffect, useState } from 'react';
import { portfolioApi } from '../services/api';
import { GraduationCap, Briefcase, MapPin } from 'lucide-react';

const About: React.FC = () => {
  const [about, setAbout] = useState<any>(null);

  useEffect(() => {
    portfolioApi.getAbout().then(setAbout).catch(console.error);
  }, []);

  if (!about) return <div className="loading">Loading...</div>;

  return (
    <div className="section-modern">
      <div className="container">
        <h2 className="section-title">About Me</h2>
        
        <div className="about-content">
          <div className="about-text">
            <p className="bio-lead">{about.bio}</p>
            <div className="personal-info">
              <div className="info-item">
                <MapPin size={20} /> <span>{about.location}</span>
              </div>
            </div>
          </div>

          <div className="timeline-container">
            <div className="timeline-section">
              <h3 className="timeline-title"><Briefcase /> Experience</h3>
              <div className="timeline">
                {about.experience?.map((exp: any) => (
                  <div key={exp.id} className="timeline-item">
                    <h4 className="item-title">{exp.job_title}</h4>
                    <p className="item-subtitle">{exp.company} | {exp.period}</p>
                    <p className="item-desc">{exp.description}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="timeline-section">
              <h3 className="timeline-title"><GraduationCap /> Education</h3>
              <div className="timeline">
                {about.education?.map((edu: any) => (
                  <div key={edu.id} className="timeline-item">
                    <h4 className="item-title">{edu.degree}</h4>
                    <p className="item-subtitle">{edu.institution} | {edu.period}</p>
                    <p className="item-desc">{edu.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
