import { Fragment, useEffect, useState } from "react";
import Modal from "react-modal";
const News = ({ ActiveIndex, animation }) => {
  const [isOpen4, setIsOpen4] = useState(false);
  const [modalContent, setModalContent] = useState({});

  useEffect(() => {
    var lists = document.querySelectorAll(".news_list > ul > li");
    let box = document.querySelector(".cavani_fn_moving_box");
    if (!box) {
      let body = document.querySelector("body");
      let div = document.createElement("div");
      div.classList.add("cavani_fn_moving_box");
      body.appendChild(div);
    }

    lists.forEach((list) => {
      list.addEventListener("mouseenter", (event) => {
        box.classList.add("opened");
        var imgURL = list.getAttribute("data-img");
        box.style.backgroundImage = `url(${imgURL})`;
        box.style.top = event.clientY - 50 + "px";
        if (imgURL === "") {
          box.classList.remove("opened");
          return false;
        }
      });
      list.addEventListener("mouseleave", () => {
        box.classList.remove("opened");
      });
    });
  }, []);

  function toggleModalFour(value) {
    setIsOpen4(!isOpen4);
    setModalContent(value);
  }
  const newsData = [
    {
      img: "img/news/1.jpg",
      tag: "Core Paper",
      date: "2025",
      comments: "50+ pages",
      title: "Backward Trajectory Completion in Bounded Phase Space",
      text1:
        "The foundational paper of Poincar\u00E9 Computing. Establishes the mathematical framework for backward trajectory completion, proving that computation in bounded phase space reduces to coordinate navigation rather than forward simulation.",
      text2:
        "Introduces the S-Entropy Space [0,1]\u00B3, the Triple Equivalence Theorem, and demonstrates O(log N) complexity for trajectory completion. Provides rigorous proofs connecting partition structure to quantum mechanical observables.",
      text3:
        "Validates the framework across multiple domains including program synthesis (96.9% accuracy), mass spectrometry (96.3% on 4,271 compounds), and genomic analysis (10\u00B9\u2076\u00D7 speedup over brute force).",
    },
    {
      img: "img/news/2.jpg",
      tag: "Theory",
      date: "2025",
      comments: "Foundation",
      title: "Poincar\u00E9 Categorical Computing",
      text1:
        "Establishes the categorical foundations of the computational framework. Introduces the processor-oscillator duality showing that any bounded computational process is equivalent to a set of coupled oscillators.",
      text2:
        "Derives the Moon property: in bounded phase space, every trajectory is periodic. This means every computation has a finite, predictable structure that can be navigated rather than simulated.",
      text3:
        "Connects to practical computation through the observation that memory addresses equal semantic content \u2014 a revolutionary insight for cache coherency and content-addressed computing architectures.",
    },
    {
      img: "img/news/3.jpg",
      tag: "Philosophy",
      date: "2025",
      comments: "Epistemology",
      title: "Post-Explanatory Epistemology",
      text1:
        "Explores the philosophical implications of Poincar\u00E9 Computing. If computation is navigation to pre-existing coordinates rather than forward derivation, what does this mean for knowledge itself?",
      text2:
        "Introduces the concept of post-explanatory knowledge: systems can know answers without proving them. Solutions exist as coordinates in partition space before any derivation is performed.",
      text3:
        "Addresses G\u00F6del's Incompleteness from a new angle: formal systems are incomplete because proofs navigate a subset of the full partition space. The answers exist; the limitation is in the navigation, not the territory.",
    },
    {
      img: "img/news/4.jpg",
      tag: "Application",
      date: "2025",
      comments: "Genomics",
      title: "Nucleic Acid Computing",
      text1:
        "Applies the Poincar\u00E9 framework to genomic analysis through the cardinal transformation: A\u2192(0,+1), T\u2192(0,-1), G\u2192(+1,0), C\u2192(-1,0), converting DNA sequences to navigable phase space trajectories.",
      text2:
        "Demonstrates 10\u00B9\u2076\u00D7 speedup over brute-force variant detection by treating genomic variants as partition coordinate displacements rather than sequence alignment problems.",
      text3:
        "Implemented in the Gospel project (github.com/fullscreen-triangle/gospel), providing a complete variant detection pipeline that processes whole genomes in seconds rather than hours.",
    },
    {
      img: "img/news/5.jpg",
      tag: "Application",
      date: "2025",
      comments: "Chemistry",
      title: "Mass Computing",
      text1:
        "Complete mass spectrometry analysis framework using partition coordinates. Maps m/z peaks to quantum numbers (n, \u2113, m, s) achieving 96.3% accuracy on 4,271 compounds with zero free parameters.",
      text2:
        "The key insight: mass-to-charge ratios are partition coordinates in disguise. Each peak in a mass spectrum corresponds to a specific location in the categorical hierarchy of the S-entropy space.",
      text3:
        "Implemented in the Lavoisier project (github.com/fullscreen-triangle/lavoisier). Demonstrates that chemical identification reduces to coordinate lookup rather than spectral library matching.",
    },
    {
      img: "img/news/6.jpg",
      tag: "Theory",
      date: "2025",
      comments: "41 Phenomena",
      title: "Partition Depth Limits",
      text1:
        "Five fundamental theorems that explain 41 physical and computational phenomena with zero free parameters. From the fine structure constant to CPU cache hierarchies, all emerge from partition depth constraints.",
      text2:
        "Demonstrates that the maximum partition depth of any bounded system is determined by the ratio of system energy to ground state energy, providing a universal complexity bound.",
      text3:
        "This paper provides the strongest evidence for the framework's validity: explaining diverse phenomena across physics, chemistry, biology, and computer science from a single mathematical structure with no tunable parameters.",
    },
  ];
  return (
    <Fragment>
      <div
        className={
          ActiveIndex === 3
            ? `cavani_tm_section active animated ${animation ? animation : "fadeInUp"
            }`
            : "cavani_tm_section hidden animated"
        }
        id="news__"
      >
        <div className="section_inner">
          <div className="cavani_tm_news">
            <div className="cavani_tm_title">
              <span>Publications &amp; Research</span>
            </div>
            <div className="news_list">
              <ul>
                {newsData.map((news, i) => (
                  <li data-img="" key={i}>
                    <div className="list_inner">
                      <span className="number">{`${i <= 9 ? 0 : ""}${i + 1
                        }`}</span>
                      <div className="details">
                        <div className="extra_metas">
                          <ul>
                            <li>
                              <span>{news.date}</span>
                            </li>
                            <li>
                              <span>
                                <a
                                  href="#"
                                  onClick={() => toggleModalFour(news)}
                                >
                                  {news.tag}
                                </a>
                              </span>
                            </li>
                            <li>
                              <span>
                                <a
                                  href="#"
                                  onClick={() => toggleModalFour(news)}
                                >
                                  {news.comments}
                                </a>
                              </span>
                            </li>
                          </ul>
                        </div>
                        <div className="post_title">
                          <h3>
                            <a href="#" onClick={() => toggleModalFour(news)}>
                              {news.title}
                            </a>
                          </h3>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
      {modalContent && (
        <Modal
          isOpen={isOpen4}
          onRequestClose={toggleModalFour}
          contentLabel="My dialog"
          className="mymodal"
          overlayClassName="myoverlay"
          closeTimeoutMS={300}
          openTimeoutMS={300}
        >
          <div className="cavani_tm_modalbox opened">
            <div className="box_inner">
              <div className="close" onClick={toggleModalFour}>
                <a href="#">
                  <i className="icon-cancel"></i>
                </a>
              </div>
              <div className="description_wrap">
                <div className="news_popup_informations">
                  <div className="details">
                    <div className="meta">
                      <ul>
                        <li><span>{modalContent.date}</span></li>
                        <li><span><a href="#">{modalContent.tag}</a></span></li>
                        <li><span><a href="#">{modalContent.comments}</a></span></li>
                      </ul>
                    </div>
                    <div className="title">
                      <h3>{modalContent.title}</h3>
                    </div>
                  </div>
                  <div className="text">
                    <p>{modalContent.text1}</p>
                    <p>{modalContent.text2}</p>
                    <p>{modalContent.text3}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Modal>
      )}
    </Fragment>
  );
};
export default News;
