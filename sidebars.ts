import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    {
      type: 'category',
      label: 'Get Started',
      link: { type: 'doc', id: 'get-started/index' },
      items: [
        'get-started/choose-version',
        'get-started/system-requirements',
        'get-started/first-experiment',
        'get-started/troubleshooting',
        'get-started/offline-and-download'
      ]
    },
    {
      type: 'category',
      label: 'Curriculum',
      link: { type: 'doc', id: 'curriculum/index' },
      items: [
        'curriculum/classroom-activities',
        'curriculum/introduction-digital-evolution',
        'curriculum/exercise-1-random-mutation',
        'curriculum/lab-book-resources',
        'curriculum/lesson-packs',
        'curriculum/data-analysis-guides',
        'curriculum/legacy-resource-library'
      ]
    },
    {
      type: 'category',
      label: 'For Teachers',
      link: { type: 'doc', id: 'teachers/index' },
      items: ['teachers/quick-start', 'teachers/classroom-tips']
    },
    {
      type: 'category',
      label: 'For Students',
      link: { type: 'doc', id: 'students/index' },
      items: ['students/first-steps', 'students/reports-and-submission']
    },
    {
      type: 'category',
      label: 'Videos & Guides',
      link: { type: 'doc', id: 'videos/index' },
      items: [
        'videos/teacher-overview',
        'videos/student-walkthroughs',
        'videos/resource-library',
        'videos/transcripts/getting-started-video'
      ]
    },
    {
      type: 'category',
      label: 'Support',
      link: { type: 'doc', id: 'support/index' },
      items: [
        'support/instructor-faq',
        'support/student-faq',
        'support/accessibility'
      ]
    },
    {
      type: 'category',
      label: 'About',
      link: { type: 'doc', id: 'about/index' },
      items: [
        'about/research-background',
        'about/team-and-acknowledgments',
        'about/how-to-cite',
        'about/legacy-redirects'
      ]
    }
  ]
};

export default sidebars;
