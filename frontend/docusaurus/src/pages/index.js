import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';
import { useState, useEffect } from 'react';
import RagChatbot from '../components/RagChatbot';
import LanguageSwitcher from '../components/LanguageSwitcher';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();

  // Table of Contents data
  const tableOfContents = [
    {
      title: "Introduction to Physical AI",
      slug: "intro-to-physical-ai",
      description: "Core concepts of Physical AI and its applications"
    },
    {
      title: "Basics of Humanoid Robotics",
      slug: "basics-humanoid-robotics",
      description: "Fundamentals of humanoid robot design and control"
    },
    {
      title: "ROS 2 Fundamentals",
      slug: "ros2-fundamentals",
      description: "Robot Operating System for robotics development"
    },
    {
      title: "Digital Twin Simulation (Gazebo + Isaac)",
      slug: "digital-twin-simulation",
      description: "Simulation environments for robot development"
    },
    {
      title: "Vision-Language-Action Systems",
      slug: "vision-language-action",
      description: "Multimodal AI systems for robotics"
    },
    {
      title: "Capstone: Simple AI-Robot Pipeline",
      slug: "capstone-pipeline",
      description: "Complete pipeline from perception to action"
    }
  ];

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>

        {/* Table of Contents Section */}
        <div className={styles.tocSection}>
          <h2 className="toc-title">Textbook Contents</h2>
          <div className={styles.tocGrid}>
            {tableOfContents.map((chapter, index) => (
              <div key={index} className={styles.tocItem}>
                <Link
                  className="button button--outline button--secondary"
                  to={`/docs/${chapter.slug}`}
                >
                  <span className={styles.tocNumber}>{index + 1}.</span>
                  <span className={styles.tocText}>{chapter.title}</span>
                </Link>
                <p className={styles.tocDescription}>{chapter.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  const [currentLanguage, setCurrentLanguage] = useState('en');

  const handleLanguageChange = (langCode) => {
    setCurrentLanguage(langCode);
    // In a real implementation, this would trigger a page language change
    console.log(`Switched to language: ${langCode}`);
  };

  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="AI-Native Textbook with RAG Chatbot for Physical AI & Humanoid Robotics">
      <HomepageHeader />
      <main>
        <div className="container">
          <div className="row">
            <div className="col col--6">
              <div className="padding-horiz--md">
                <h2>Physical AI & Humanoid Robotics</h2>
                <p>
                  This AI-Native textbook combines cutting-edge research with interactive learning experiences.
                  Explore concepts in Physical AI, humanoid robotics, and embodied intelligence through our
                  comprehensive curriculum.
                </p>
                <ul>
                  <li>Interactive textbook content with RAG-powered search</li>
                  <li>AI-powered chatbot for instant Q&A</li>
                  <li>Multi-language support (English & Urdu)</li>
                  <li>Personalized learning paths</li>
                </ul>
              </div>
            </div>
            <div className="col col--6">
              <div className="padding-horiz--md">
                <div className={styles.languageSelector}>
                  <h3>Language</h3>
                  <LanguageSwitcher
                    currentLanguage={currentLanguage}
                    onLanguageChange={handleLanguageChange}
                  />
                </div>
                <div style={{ marginTop: '2rem' }}>
                  <h3>AI-Powered Learning Assistant</h3>
                  <p>
                    Ask questions about the textbook content and get answers based on the material.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      <RagChatbot />
    </Layout>
  );
}