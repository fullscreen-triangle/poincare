import { useState, useEffect, useRef } from 'react'
import Isotope from 'isotope-layout'
import Modal from 'react-modal';

const applications = [
    {
        category: "vision",
        title: "Computer Vision",
        subtitle: "Helicopter",
        description: "12 measurement modalities reducing 10\u2076\u2070 possibilities to 1 unique state through categorical completion.",
        detail1: "Computer vision through Poincar\u00E9 Computing treats each image as an observation in bounded phase space. Instead of training neural networks on millions of examples, we navigate directly to the categorical coordinates of what is observed.",
        detail2: "The Observer abstraction provides 12 measurement modalities \u2014 from edge detection to spectral analysis \u2014 each reducing the partition space. Combined, they collapse 10\u2076\u2070 possible states to a single unique identification.",
        detail3: "Implemented in the Helicopter project (github.com/fullscreen-triangle/helicopter). Achieves real-time performance without GPU acceleration by replacing forward inference with coordinate navigation.",
        link: "https://github.com/fullscreen-triangle/helicopter"
    },
    {
        category: "genomics",
        title: "Genomic Analysis",
        subtitle: "Gospel",
        description: "Cardinal transformation A\u2192(0,+1), T\u2192(0,-1), G\u2192(+1,0), C\u2192(-1,0) with 10\u00B9\u2076\u00D7 speedup.",
        detail1: "DNA sequences are converted to phase space trajectories using the cardinal transformation, mapping each nucleotide to a 2D direction vector. This transforms sequence comparison from string alignment to trajectory navigation.",
        detail2: "Variant detection becomes a partition coordinate displacement problem. Instead of aligning billions of base pairs, we detect where the trajectory deviates from the reference partition structure.",
        detail3: "Achieves 10\u00B9\u2076\u00D7 speedup over brute-force approaches. Whole genome analysis completes in seconds rather than hours. Implemented in Gospel (github.com/fullscreen-triangle/gospel).",
        link: "https://github.com/fullscreen-triangle/gospel"
    },
    {
        category: "massspec",
        title: "Mass Spectrometry",
        subtitle: "Lavoisier",
        description: "96.3% accuracy on 4,271 compounds with zero free parameters using partition coordinates.",
        detail1: "Mass-to-charge ratios are partition coordinates in disguise. Each m/z peak in a spectrum maps directly to quantum numbers (n, \u2113, m, s) in the categorical hierarchy.",
        detail2: "Chemical identification reduces from spectral library matching (O(N) comparisons) to coordinate lookup (O(log N)). The framework identifies compounds by navigating to their S-entropy coordinates.",
        detail3: "Validated on 4,271 compounds with 96.3% accuracy \u2014 using zero free parameters. Every prediction comes directly from the mathematical structure. Implemented in Lavoisier (github.com/fullscreen-triangle/lavoisier).",
        link: "https://github.com/fullscreen-triangle/lavoisier"
    },
    {
        category: "processor",
        title: "Processor Architecture",
        subtitle: "Maxwell",
        description: "Hardware thermal fluctuations as virtual gas molecules; jitter as S-entropy position measurement.",
        detail1: "The processor-oscillator duality reveals that CPU thermal fluctuations are not noise \u2014 they are measurements. Each thermal jitter corresponds to a position in S-entropy space.",
        detail2: "Cache coherency becomes trivial when memory address equals semantic content. The framework provides a content-addressed architecture where data is stored at its natural partition coordinate.",
        detail3: "This reframes computer architecture: CPUs are not instruction executors but partition navigators. Memory hierarchies reflect the natural depth structure of the S-entropy space. Implemented in Maxwell (github.com/fullscreen-triangle/maxwell).",
        link: "https://github.com/fullscreen-triangle/maxwell"
    },
    {
        category: "synthesis",
        title: "Program Synthesis",
        subtitle: "Core Framework",
        description: "96.9% accuracy (31/32 correct), median synthesis time 0.19ms Python, <1\u03BCs Rust.",
        detail1: "Program synthesis from input-output examples demonstrates the framework at its purest. Given a set of examples, the target program exists as a coordinate in partition space.",
        detail2: "Instead of searching through program space or using machine learning, we navigate backward from the observed input-output behavior to the program's S-entropy coordinates.",
        detail3: "Achieves 96.9% accuracy on test cases. Median synthesis time: 0.19ms in Python, <1\u03BCs in Rust. The 190\u00D7 Rust speedup validates that the bottleneck is navigation, not computation.",
        link: "https://github.com/fullscreen-triangle/poincare"
    },
    {
        category: "dynamics",
        title: "Dynamical Systems",
        subtitle: "Validation Suite",
        description: "N-body problems, Lorenz attractor, harmonic oscillator \u2014 validated against analytical solutions.",
        detail1: "The validation suite tests backward trajectory completion against known analytical solutions. The harmonic oscillator, the simplest bounded system, provides exact comparisons.",
        detail2: "The Lorenz attractor tests the framework on chaotic systems. Despite sensitivity to initial conditions, backward completion reconstructs complete trajectories from final observations.",
        detail3: "N-body problems demonstrate scaling behavior. For N=10\u2076 particles, the framework completes trajectories in ~13 operations compared to ~10\u00B2\u00B9 for direct simulation \u2014 a speedup of approximately 10\u00B2\u2070\u00D7.",
        link: "https://github.com/fullscreen-triangle/poincare"
    }
];

export default function PortfolioDefault({ ActiveIndex, Animation }) {

    const [modalOpen, setModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState(null);

    const isotope = useRef()
    const [filterKey, setFilterKey] = useState('*')

    useEffect(() => {
        setTimeout(() => {
            isotope.current = new Isotope(".filter-container", {
                itemSelector: ".filter-item",
                layoutMode: "fitRows",
            });
        }, 500);
        return () => isotope.current && isotope.current.destroy();
    }, []);

    useEffect(() => {
        if (isotope.current) {
            filterKey === '*'
                ? isotope.current.arrange({ filter: '*' })
                : isotope.current.arrange({ filter: `.${filterKey}` })
        }
    }, [filterKey])

    const handleFilterKeyChange = key => () => setFilterKey(key)

    function openModal(app) {
        setModalContent(app);
        setModalOpen(true);
    }

    return (
        <>
            {/* <!-- APPLICATIONS --> */}
            <div className={ActiveIndex === 2 ? `cavani_tm_section active animated ${Animation ? Animation : "fadeInUp"}` : "cavani_tm_section hidden animated"} id="portfolio_">
                <div className="section_inner">
                    <div className="cavani_tm_portfolio">
                        <div className="cavani_tm_title">
                            <span>Applications</span>
                        </div>

                        <div className="portfolio_filter">
                            <ul>
                                <li><a href='#' onClick={handleFilterKeyChange('*')} className={filterKey === '*' ? 'current' : ''}>All</a></li>
                                <li><a href='#' onClick={handleFilterKeyChange('vision')}>Vision</a></li>
                                <li><a href='#' onClick={handleFilterKeyChange('genomics')}>Genomics</a></li>
                                <li><a href='#' onClick={handleFilterKeyChange('massspec')}>Mass Spec</a></li>
                                <li><a href='#' onClick={handleFilterKeyChange('processor')}>Processor</a></li>
                                <li><a href='#' onClick={handleFilterKeyChange('synthesis')}>Synthesis</a></li>
                            </ul>
                        </div>
                        <div className="portfolio_list">
                            <div className="filter-container">
                                {applications.map((app, i) => (
                                    <div key={i} className={`filter-item ${app.category}`}>
                                        <div className="list_inner">
                                            <div className="image" onClick={() => openModal(app)} style={{ cursor: 'pointer' }}>
                                                <img src="img/thumbs/1-1.jpg" alt="" />
                                                <div className="main" style={{
                                                    background: `linear-gradient(135deg, hsl(${i * 60}, 40%, 15%) 0%, hsl(${i * 60 + 30}, 30%, 25%) 100%)`,
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'center',
                                                }} />
                                                <span className="icon"><i className="icon-doc-text-inv"></i></span>
                                                <div className="details">
                                                    <h3>{app.title}</h3>
                                                    <span>{app.subtitle}</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {/* <!-- /APPLICATIONS --> */}

            {modalContent && (
                <Modal
                    isOpen={modalOpen}
                    onRequestClose={() => setModalOpen(false)}
                    contentLabel="Application Details"
                    className="mymodal"
                    overlayClassName="myoverlay"
                    closeTimeoutMS={300}
                    openTimeoutMS={300}
                >
                    <div className="cavani_tm_modalbox opened">
                        <div className="box_inner">
                            <div className="close" onClick={() => setModalOpen(false)}>
                                <a href="#">
                                    <i className="icon-cancel" />
                                </a>
                            </div>
                            <div className="description_wrap">
                                <div className="popup_details">
                                    <div className="portfolio_main_title">
                                        <h3>{modalContent.title}</h3>
                                        <span>{modalContent.subtitle}</span>
                                    </div>
                                    <div className="main_details">
                                        <div className="textbox">
                                            <p>{modalContent.detail1}</p>
                                            <p>{modalContent.detail2}</p>
                                            <p>{modalContent.detail3}</p>
                                        </div>
                                        <div className="detailbox">
                                            <ul>
                                                <li>
                                                    <span className="first">Domain</span>
                                                    <span>{modalContent.category}</span>
                                                </li>
                                                <li>
                                                    <span className="first">Project</span>
                                                    <span>{modalContent.subtitle}</span>
                                                </li>
                                                <li>
                                                    <span className="first">Source</span>
                                                    <span><a href={modalContent.link} target="_blank" rel="noopener noreferrer">GitHub</a></span>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </Modal>
            )}
        </>
    )
}
