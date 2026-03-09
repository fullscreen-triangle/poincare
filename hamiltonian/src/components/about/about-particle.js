import React from 'react'
import ProgressBar from '../progressBar';
import { CircularProgressbar } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';

const metricData = [
    { language: 'Synthesis', progress: 97 },
    { language: 'Mass Spec', progress: 96 },
    { language: 'Speedup', progress: 99 },
];

const progressBarData = [
    { bgcolor: "#7d7789", completed: 100, title: 'Theoretical Foundation' },
    { bgcolor: "#7d7789", completed: 75, title: 'Rust Implementation' },
    { bgcolor: "#7d7789", completed: 40, title: 'Python Bindings' },
    { bgcolor: "#7d7789", completed: 60, title: 'Documentation' },
];

const keyInsights = [
    {
        desc: "Computation is not simulation — it is navigation to pre-existing solution coordinates. The trajectory already exists. The task is coordinate resolution, not causal forward-propagation.",
        info1: "Core Principle",
        info2: "Backward Trajectory Completion"
    },
    {
        desc: "For bounded dynamical systems, three mathematical structures are identical: oscillatory structure, categorical structure, and entropic structure. Knowing any one determines the others.",
        info1: "Triple Equivalence",
        info2: "Fundamental Theorem"
    },
    {
        desc: "The stone has landed. Its trajectory existed before we calculated. Our task is not simulation but navigation — finding the coordinates where reality's answers reside.",
        info1: "Paradigm Shift",
        info2: "Post-Explanatory Epistemology"
    },
]

export default function AboutDefault({ ActiveIndex }) {
    return (
        <>
            {/* <!-- FRAMEWORK --> */}
            <div className={ActiveIndex === 1 ? "cavani_tm_section active animated flipInX" : "cavani_tm_section active hidden animated flipOutX"} id="about_">
            <div className="section_inner">
                    <div className="cavani_tm_about">
                        <div className="biography">
                            <div className="cavani_tm_title">
                                <span>The Framework</span>
                            </div>
                            <div className="wrapper">
                                <div className="left">
                                    <p><strong>Poincar&eacute; Computing</strong> is a fundamental reconceptualization of computation based on backward trajectory completion in bounded phase space.</p>
                                    <p>Instead of simulating forward from initial conditions, we navigate backward from observed final states to complete trajectories in pre-existing partition structure &mdash; achieving <strong>O(log N)</strong> complexity versus O(n&sup2; &middot; t/&Delta;t) for traditional simulation.</p>
                                </div>
                                <div className="right">
                                    <ul>
                                        <li><span className="first">License:</span><span className="second">MIT Open Source</span></li>
                                        <li><span className="first">Language:</span><span className="second">Rust + Python Bindings</span></li>
                                        <li><span className="first">Complexity:</span><span className="second">O(log N) Navigation</span></li>
                                        <li><span className="first">Paper:</span><span className="second">50+ Pages, Publication-Ready</span></li>
                                        <li><span className="first">Author:</span><span className="second">Kundai Sachikonye</span></li>
                                        <li><span className="first">Affiliation:</span><span className="second">TU Munich</span></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div className="services">
                            <div className="wrapper">
                                <div className="service_list">
                                    <div className="cavani_tm_title">
                                        <span>Core Concepts</span>
                                    </div>
                                    <div className="list">
                                        <ul>
                                            <li>Bounded Phase Space</li>
                                            <li>Poincar&eacute; Recurrence Theorem</li>
                                            <li>Finite Resolution Partitioning</li>
                                            <li>Backward Trajectory Completion</li>
                                            <li>S-Entropy Space [0,1]&sup3;</li>
                                        </ul>
                                    </div>
                                </div>
                                <div className="service_list">
                                    <div className="cavani_tm_title">
                                        <span>Key Theorems</span>
                                    </div>
                                    <div className="list">
                                        <ul>
                                            <li>Triple Equivalence Theorem</li>
                                            <li>Partition Depth Limits</li>
                                            <li>Observer Abstraction</li>
                                            <li>Ternary Addressing (3^M)</li>
                                            <li>Processor-Oscillator Duality</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="skills">
                            <div className="wrapper">
                                <div className="programming">
                                    <div className="cavani_tm_title">
                                        <span>Development Progress</span>
                                    </div>
                                    <div className="cavani_progress">
                                        {progressBarData.map((item, idx) => (
                                            <ProgressBar key={idx} bgcolor={item.bgcolor} completed={item.completed} title={item.title} />
                                        ))}
                                    </div>
                                </div>
                                <div className="language">
                                    <div className="cavani_tm_title">
                                        <span>Validated Accuracy</span>
                                    </div>
                                    <div className="circular_progress_bar">
                                        <div className='circle_holder'>
                                            {metricData.map((item, idx) => (
                                                <div key={idx}>
                                                    <div className="list_inner">
                                                        <CircularProgressbar
                                                            value={item.progress}
                                                            text={`${item.progress}%`}
                                                            strokeWidth={3}
                                                            stroke='#7d7789'
                                                            Language={item.language}
                                                            className={"list_inner"}
                                                        />
                                                        <div className="title"><span>{item.language}</span></div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="resume">
                            <div className="wrapper">
                                <div className="education">
                                    <div className="cavani_tm_title">
                                        <span>Theoretical Foundation</span>
                                    </div>
                                    <div className="list">
                                        <div className="univ">
                                            <ul>
                                                <li>
                                                    <div className="list_inner">
                                                        <div className="time">
                                                            <span>Foundation</span>
                                                        </div>
                                                        <div className="place">
                                                            <h3>Poincar&eacute; Recurrence Theorem</h3>
                                                            <span>All observable states lie on closed trajectories in bounded phase space</span>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div className="list_inner">
                                                        <div className="time">
                                                            <span>Insight</span>
                                                        </div>
                                                        <div className="place">
                                                            <h3>Finite Resolution Partitioning</h3>
                                                            <span>Real observers partition continuous space into discrete cells: N_max = &Omega;/h^d</span>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div className="list_inner">
                                                        <div className="time">
                                                            <span>Result</span>
                                                        </div>
                                                        <div className="place">
                                                            <h3>Triple Equivalence</h3>
                                                            <span>Oscillatory &equiv; Categorical &equiv; Entropic structure</span>
                                                        </div>
                                                    </div>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                <div className="experience">
                                    <div className="cavani_tm_title">
                                        <span>Implementation Milestones</span>
                                    </div>
                                    <div className="list">
                                        <div className="univ">
                                            <ul>
                                                <li>
                                                    <div className="list_inner">
                                                        <div className="time">
                                                            <span>Complete</span>
                                                        </div>
                                                        <div className="place">
                                                            <h3>Publication-Ready Paper</h3>
                                                            <span>50+ pages with rigorous mathematical treatment</span>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div className="list_inner">
                                                        <div className="time">
                                                            <span>Active</span>
                                                        </div>
                                                        <div className="place">
                                                            <h3>Rust Core Implementation</h3>
                                                            <span>space.rs, address.rs, partition.rs, trajectory.rs, navigator.rs</span>
                                                        </div>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div className="list_inner">
                                                        <div className="time">
                                                            <span>Planned</span>
                                                        </div>
                                                        <div className="place">
                                                            <h3>Domain Adapters &amp; Python Bindings</h3>
                                                            <span>Vision, Genomics, Mass Spectrometry, Processor adapters</span>
                                                        </div>
                                                    </div>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="partners">
                            <div className="cavani_tm_title">
                                <span>Related Projects</span>
                            </div>
                            <div className="list" style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', padding: '20px 0' }}>
                                <a href="https://github.com/fullscreen-triangle/helicopter" target="_blank" rel="noopener noreferrer" style={{ padding: '12px 24px', border: '1px solid rgba(125,119,137,0.3)', borderRadius: '8px', textDecoration: 'none', transition: 'all 0.3s' }}>
                                    <strong>Helicopter</strong>
                                    <br /><small>Computer Vision</small>
                                </a>
                                <a href="https://github.com/fullscreen-triangle/maxwell" target="_blank" rel="noopener noreferrer" style={{ padding: '12px 24px', border: '1px solid rgba(125,119,137,0.3)', borderRadius: '8px', textDecoration: 'none', transition: 'all 0.3s' }}>
                                    <strong>Maxwell</strong>
                                    <br /><small>Processor Architecture</small>
                                </a>
                                <a href="https://github.com/fullscreen-triangle/gospel" target="_blank" rel="noopener noreferrer" style={{ padding: '12px 24px', border: '1px solid rgba(125,119,137,0.3)', borderRadius: '8px', textDecoration: 'none', transition: 'all 0.3s' }}>
                                    <strong>Gospel</strong>
                                    <br /><small>Genomic Analysis</small>
                                </a>
                                <a href="https://github.com/fullscreen-triangle/lavoisier" target="_blank" rel="noopener noreferrer" style={{ padding: '12px 24px', border: '1px solid rgba(125,119,137,0.3)', borderRadius: '8px', textDecoration: 'none', transition: 'all 0.3s' }}>
                                    <strong>Lavoisier</strong>
                                    <br /><small>Mass Spectrometry</small>
                                </a>
                            </div>
                        </div>
                        <div className="testimonials">
                            <div className="cavani_tm_title">
                                <span>Key Insights</span>
                            </div>
                            <div className="list">
                                <ul className="">
                                    <li>
                                        <Swiper
                                            slidesPerView={1}
                                            spaceBetween={30}
                                            loop={true}
                                            className="custom-class"
                                            breakpoints={{
                                                768: {
                                                    slidesPerView: 2,
                                                }
                                            }}
                                        >
                                            {keyInsights.map((item, i) => (
                                                <SwiperSlide key={i}>
                                                    <div className="list_inner">
                                                        <div className="text">
                                                            <i className="icon-quote-left" />
                                                            <p>{item.desc}</p>
                                                        </div>
                                                        <div className="details">
                                                            <div className="info">
                                                                <h3>{item.info1}</h3>
                                                                <span>{item.info2}</span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </SwiperSlide>
                                            ))}
                                        </Swiper>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {/* <!-- FRAMEWORK --> */}
        </>
    )
}
