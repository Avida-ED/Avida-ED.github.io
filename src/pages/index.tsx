
import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

function Card(props: { title: string; children: React.ReactNode; to: string }) {
  return (
    <div className="col col--4">
      <div className="aeCard">
        <h3>{props.title}</h3>
        <p>{props.children}</p>
        <Link className="button button--secondary button--sm" to={props.to}>
          Start here
        </Link>
      </div>
    </div>
  );
}

export default function Home(): JSX.Element {
  const launchV4 = 'https://avida-ed.github.io/avida-ed4/'; // TODO
  const launchV3 = 'https://avida-ed.github.io/avida-ed3/'; // TODO

  return (
    <Layout>
      <main>
        <section className="aeHero">
          <div className="container">
            <h1 className="aeHeroTitle">Teach evolution by observing it happen.</h1>
            <p className="aeHeroSubtitle">
              Avida-ED enables students to run real-time digital evolution experiments and investigate natural selection,
              mutation, and adaptation using scientific reasoning and data.
            </p>
            <div className="aeHeroButtons">
              <a className="button button--primary button--lg" href={launchV4}>
                Launch Avida-ED 4
              </a>
              <a className="button button--outline button--lg" href={launchV3}>
                Launch Avida-ED 3 (Legacy)
              </a>
              <Link className="button button--secondary button--lg" to="/docs/get-started/">
                Get started in 10 minutes
              </Link>
            </div>
            <p className="aeHeroNote">
              New to Avida-ED? Start with <Link to="/docs/get-started/choose-version/">choosing a version</Link> and the{' '}
              <Link to="/docs/get-started/first-experiment/">first experiment</Link>.
            </p>
          </div>
        </section>

        <section className="aeSection">
          <div className="container">
            <h2>Start here</h2>
            <div className="row">
              <Card title="For Teachers" to="/docs/teachers/">
                Plan a complete classroom activity—from a single lab period to a multi-week inquiry project.
              </Card>
              <Card title="For Students" to="/docs/students/">
                Learn how to run experiments, collect data, and complete typical class assignments.
              </Card>
              <Card title="Curriculum & Guides" to="/docs/curriculum/">
                Browse lesson packs, classroom activities, and data-analysis guidance you can use immediately.
              </Card>
            </div>
          </div>
        </section>

        <section className="aeSection">
          <div className="container">
            <h2>What Avida-ED teaches</h2>
            <ul>
              <li>How variation, inheritance, and selection drive evolutionary change</li>
              <li>How to design experiments and test hypotheses with data</li>
              <li>How population-level patterns emerge from individual-level processes</li>
              <li>How scientific explanations are built, evaluated, and revised</li>
            </ul>

            <div className="aeCallout">
              <p>
                Looking for classroom-ready materials? See <Link to="/docs/curriculum/">Curriculum</Link>,{' '}
                <Link to="/docs/teachers/quick-start/">Teacher Quick Start</Link>, and the{' '}
                <Link to="/docs/get-started/troubleshooting/">Troubleshooting checklist</Link>.
              </p>
            </div>
          </div>
        </section>

        <section className="aeSection">
          <div className="container">
            <h2>Guides and support</h2>
            <p>
              Use the <Link to="/docs/videos/">Videos &amp; Guides</Link> section for walkthroughs with transcripts, or go
              directly to <Link to="/docs/support/">Support</Link> for instructor and student FAQs.
            </p>
          </div>
        </section>

        <section className="aeSection">
          <div className="container">
            <h2>Credibility and reuse</h2>
            <p>
              Avida-ED is used in classrooms and outreach programs to support evolution and nature-of-science instruction.
              For citations and attribution guidance, see <Link to="/docs/about/how-to-cite/">How to Cite Avida-ED</Link>{' '}
              and <Link to="/docs/about/research-background/">Research Background</Link>.
            </p>
          </div>
        </section>
      </main>
    </Layout>
  );
}
