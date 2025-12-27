import React, { useEffect, useState } from 'react';
import { portfolioApi } from '../services/api';
import { ArrowRight, Github, Linkedin } from 'lucide-react';

const Home: React.FC = () => {
  const [about, setAbout] = useState<any>(null);

  useEffect(() => {
    portfolioApi.getAbout().then(setAbout).catch(console.error);
  }, []);

  if (!about) return <div className="loading">Loading...</div>;

  return (
    <div className="home-page">
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">
              Hi, I'm <span className="text-gradient">{about.name}</span>
            </h1>
            <h2 className="hero-subtitle">{about.title}</h2>
            <p className="hero-bio">{about.bio}</p>
            <div className="hero-actions">
              <a href="#projects" className="btn btn-primary">
                View My Work <ArrowRight size={20} />
              </a>
              <div className="social-links">
                {about.social_links?.github && (
                  <a href={about.social_links.github} target="_blank" rel="noopener noreferrer">
                    <Github size={24} />
                  </a>
                )}
                {about.social_links?.linkedin && (
                  <a href={about.social_links.linkedin} target="_blank" rel="noopener noreferrer">
                    <Linkedin size={24} />
                  </a>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
