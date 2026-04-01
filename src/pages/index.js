import React from 'react';
import Layout from '@theme/Layout';

export default function Home() {
  const logoText = 'Digital Evolution for Education';
  const bodyText = 'Avida-ED is an award-winning educational application developed at Michigan State University for undergraduate biology courses. Researchers and educators designed Avida-ED to help students learn about evolution and scientific methods by allowing them to design and perform experiments to test hypotheses about evolutionary mechanisms using evolving digital organisms.';
  const kalturaThumbnailAt10s =
    'https://cfvod.kaltura.com/p/811482/sp/81148200/thumbnail/entry_id/1_rdyd9cnv/width/1280/height/720/vid_sec/10';
  const iframeSrc = `https://cdnapisec.kaltura.com/p/811482/sp/81148200/embedIframeJs/uiconf_id/27551951/partner_id/811482?iframeembed=true&playerId=kaltura_player&entry_id=1_rdyd9cnv&flashvars[streamerType]=auto&flashvars[localizationCode]=en&flashvars[leadWithHTML5]=true&flashvars[sideBarContainer.plugin]=true&flashvars[sideBarContainer.position]=left&flashvars[sideBarContainer.clickToClose]=true&flashvars[chapters.plugin]=true&flashvars[chapters.layout]=vertical&flashvars[chapters.thumbnailRotator]=false&flashvars[streamSelector.plugin]=true&flashvars[EmbedPlayer.SpinnerTarget]=videoHolder&flashvars[dualScreen.plugin]=true&flashvars[thumbnailUrl]=${encodeURIComponent(
    kalturaThumbnailAt10s,
  )}&wid=1_jhy13lc6`;

  return (
    <Layout title="Avida-ED" description="Digital evolution for education">
      <main>
        <section className="homeHero">
          <div className="container homeHero__container">
            <div className="homeHero__top">
              <div className="homeHero__intro">
                <img
                  className="homeHero__logo"
                  src="img/avida-ed-logo.png"
                  alt="Avida-ED logo"
                />
                <h1 className="homeHero__title">{logoText}</h1>
              </div>

              <div className="homeHero__videoBand">
                <div className="homeHero__videoWrap" aria-label="Avida-ED overview video">
                  <iframe
                    className="homeHero__video"
                    src={iframeSrc}
                    title="Avida-ED Overview Video"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  />
                </div>
              </div>
            </div>

            <div className="contentColumn homeHero__body">
              <p className="homeHero__blurb">{bodyText}</p>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
