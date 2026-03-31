/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docsSidebar: [
    {
      type: 'category',
      label: 'Docs Example',
      link: { type: 'doc', id: 'instructors/index' },
      items: [
        { type: 'doc', id: 'instructors/quick-start', label: 'Quick Start' },
      ],
    },
    {
      type: 'category',
      label: 'Students',
      link: { type: 'doc', id: 'students/index' },
      items: [
        { type: 'doc', id: 'students/first-steps', label: 'First Steps' },
        { type: 'doc', id: 'students/course-workflow', label: 'Course Workflow' },
        { type: 'doc', id: 'students/faq', label: 'Student FAQ' },
        { type: 'doc', id: 'students/videos', label: 'Videos' },
      ],
    },
    {
      type: 'category',
      label: 'Videos',
      link: { type: 'doc', id: 'videos/index' },
      items: [
        { type: 'doc', id: 'videos/avida-ed-4-tutorial-videos', label: 'Avida-ED 4 Tutorial Videos' },
        { type: 'doc', id: 'videos/intro-to-lab-bench', label: 'Intro to Lab Bench Transcript' },
        { type: 'doc', id: 'videos/project-overview', label: 'Project Overview Transcript' },
      ],
    },
    {
      type: 'category',
      label: 'Support',
      link: { type: 'doc', id: 'support/index' },
      items: [
        { type: 'doc', id: 'support/accessibility', label: 'Accessibility' },
        { type: 'doc', id: 'support/instructor-faq', label: 'Instructor FAQ' },
        { type: 'doc', id: 'support/reporting-problems', label: 'Reporting Problems' },
        { type: 'doc', id: 'support/troubleshooting', label: 'Troubleshooting' },
      ],
    },
  ],
};

export default sidebars;
