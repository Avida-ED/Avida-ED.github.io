import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';

const config: Config = {
  title: 'Avida-ED',
  tagline: 'Digital evolution for science education',
  favicon: 'img/favicon.ico',

  // GitHub user/org site hosted at the domain root.
  url: 'https://avida-ed.github.io',
  baseUrl: '/',

  organizationName: 'Avida-ED',
  projectName: 'Avida-ED.github.io',
  trailingSlash: true,

  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'throw'
    }
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en']
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: 'docs',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/Avida-ED/Avida-ED.github.io/edit/main/',
          showLastUpdateAuthor: false,
          showLastUpdateTime: true
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css'
        }
      }
    ]
  ],

  themeConfig: {
    navbar: {
      title: 'Avida-ED',
      items: [
        { to: '/', label: 'Home', position: 'left' },
        { to: '/docs/get-started/', label: 'Get Started', position: 'left' },
        { to: '/docs/curriculum/', label: 'Curriculum', position: 'left' },
        { to: '/docs/teachers/', label: 'For Teachers', position: 'left' },
        { to: '/docs/students/', label: 'For Students', position: 'left' },
        { to: '/docs/videos/', label: 'Videos & Guides', position: 'left' },
        { to: '/docs/support/', label: 'Support', position: 'left' },
        { to: '/docs/about/', label: 'About', position: 'left' },
        {
          href: 'https://github.com/Avida-ED/Avida-ED.github.io',
          label: 'GitHub',
          position: 'right'
        }
      ]
    },

    footer: {
      style: 'light',
      links: [
        {
          title: 'Use Avida-ED',
          items: [
            { label: 'Get Started', to: '/docs/get-started/' },
            { label: 'Curriculum', to: '/docs/curriculum/' },
            { label: 'Offline & Download', to: '/docs/get-started/offline-and-download/' },
            { label: 'Teacher Quick Start', to: '/docs/teachers/quick-start/' },
            { label: 'Student First Steps', to: '/docs/students/first-steps/' }
          ]
        },
        {
          title: 'Help & Access',
          items: [
            { label: 'Support', to: '/docs/support/' },
            { label: 'Instructor FAQ', to: '/docs/support/instructor-faq/' },
            { label: 'Accessibility', to: '/docs/support/accessibility/' }
          ]
        },
        {
          title: 'About',
          items: [
            { label: 'What is Avida-ED?', to: '/docs/about/' },
            { label: 'Research Background', to: '/docs/about/research-background/' },
            { label: 'How to Cite', to: '/docs/about/how-to-cite/' }
          ]
        }
      ],
      copyright:
        `Copyright © ${new Date().getFullYear()} Avida-ED contributors. Content licensed as noted.`
    },

    // Good baseline; verify contrast in custom.css
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula
    },

    colorMode: {
      respectPrefersColorScheme: true
    }
  }
};

export default config;
