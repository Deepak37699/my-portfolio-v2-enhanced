import React, { useEffect, useState } from 'react';
import { portfolioApi } from '../services/api';
import { Award } from 'lucide-react';

const Skills: React.FC = () => {
  const [skills, setSkills] = useState<any[]>([]);

  useEffect(() => {
    portfolioApi.getSkills().then(setSkills).catch(console.error);
  }, []);

  return (
    <div className="section-modern">
      <div className="container">
        <h2 className="section-title">My Skills</h2>
        <p className="section-subtitle">A collection of my technical expertise and proficiencies.</p>
        
        <div className="skills-grid">
          {skills.map((skill) => (
            <div key={skill.id} className="skill-card">
              <Award className="skill-icon" size={32} />
              <h3 className="skill-name">{skill.name}</h3>
              <p className="skill-category">{skill.category}</p>
              <div className="skill-progress">
                <div 
                  className="skill-progress-bar" 
                  style={{ width: `${skill.proficiency}%` }}
                ></div>
              </div>
              <span className="skill-percent">{skill.proficiency}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Skills;
